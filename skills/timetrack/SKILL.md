---
name: timetrack
description: Log worked hours into the ZigZag "TimeTrack" Notion database from the user's Russian shorthand, and answer questions about the hours already logged. Use this whenever the user reports time spent on ZZAP tasks in any form — "31-го ZZAP-3: 2; ZZAP-2: 1", "с 10 по 14 августа ZZAP-1 по 4 часа", "запиши 6 часов на ZZAP-9 за вчера" — and also when they ask how many hours went somewhere ("сколько часов за август", "разбивка по задачам", "где пробелы в трекере", "сколько недобрал до 40"). Trigger on bare date+task+number lines even when no verb like "запиши" is present: when ZZAP tickets are involved such a line is always a time entry.
---

# TimeTrack

The user logs their ZigZag hours in a Notion database and dictates them in a compressed
Russian shorthand. This skill is about reading that shorthand correctly and turning it into
rows — and about reading the rows back when they ask what the month looked like.

The shorthand is terse because the user already knows what they worked on; the ambiguity is
all in the dates. Most of what follows is about resolving dates the way they mean them.

## The database

| | |
|---|---|
| Database | **TimeTrack** (Work Area → ZigZag → TimeTrack) |
| Data source | `collection://3cf95d8a-b393-806e-8d9b-000ba9ef1b8c` |
| URL | https://app.notion.com/p/dronn1k/3cf95d8ab3938059940bf1351665cc24 |

Three properties:

- `Task name` — title, holds the bare ticket key: `ZZAP-1`, `ZZAP-7`. Nothing else, no description.
  Work with no ticket behind it (tooling, agents, general fixes, merges) is logged as `no-task`.
- `Time spend` — number, hours for that one day. Fractions are fine (`1.5`).
- `Date` — a single date, never a range. Set it via the expanded column `date:Date:start`.

**One row = one task on one day.** Two tasks on the same day are two rows, not one row with
a combined number — the whole point of the table is that hours stay attributable per ticket.

### Reaching the Notion tools

The Notion MCP tools are deferred and their server prefix is a hash that differs between
machines, so don't hardcode names. Load them with ToolSearch by keyword:

```
ToolSearch query: "+notion create pages query data sources fetch"
```

You need `create-pages` (writing), `query-data-sources` (reading), and occasionally `fetch`
(re-deriving the data source id if the one above ever stops resolving — fetch the database
URL and read the `<data-source url="collection://…">` tag).

## Reading the shorthand

Real examples from the user, and what each means:

**Range, one task, hours per day:**
```
Сделай записи с 10-го августа по 14-ое. ZZAP-1 по 4 часа
```
→ five rows, ZZAP-1, 4 hours *each*. `по 4 часа` distributes; it is never a total to split.

**Range with a per-day override in parentheses:**
```
с 17 по 20 августа, ZZAP-2 по 6 (17-го 4 часа)
```
→ 17th = 4, 18th–20th = 6. The parenthetical overrides that one day only.

**One day, several tasks, separated by `;`:**
```
28 ZZAP-3: 2; ZZAP-4: 4
```
→ two rows on the 28th.

**One day per line:**
```
24-го ZZAP-9: 6.
25-го ZZAP-1: 6.
26 ZZAP-9: 3.
```
→ three rows. Trailing periods are punctuation, not decimals — `ZZAP-9: 6.` is 6 hours.

The pattern underneath all of these is `<date> <task>: <hours>`, with `по N` meaning "N per
day" and `;` separating tasks within a day. Ordinal suffixes (`10-го`, `14-ое`), a bare
number (`28`), and a full date all mean the same thing.

## Resolving dates

The user almost never says the year and often drops the month, so:

- **Month omitted** → carry over the month from the entries earlier in the conversation.
  In a fresh conversation with no such context, ask rather than guess.
- **Year omitted** → the most recent occurrence in the past. In September 2026, "10 августа"
  is 2026-08-10; in January, "20 декабря" is the previous year. These are timesheets being
  filled in after the fact, so a future date is nearly always a misreading.
- **Ranges cover working days only** — skip Saturday and Sunday unless the user names a
  weekend date explicitly. Say which days you used in the confirmation so a genuine weekend
  shift is easy to spot and correct.
- **Relative dates** ("вчера", "в понедельник") resolve against today's date. Compute them
  with `date -j -v-1d "+%Y-%m-%d"` rather than counting in your head, and state the resulting
  date in the confirmation.

Weekday alignment is a cheap sanity check on the year: if a claimed working-day range lands
on a weekend, you probably picked the wrong year. Verify before writing:

```bash
for d in 10 11 12 13 14; do date -j -f "%Y-%m-%d" "2026-08-$d" "+%Y-%m-%d %a"; done
```

## Writing entries

1. **Check the target dates first.** Query the data source for rows on the dates you are
   about to write:

   ```sql
   SELECT "Task name", "Time spend", "date:Date:start"
   FROM "collection://3cf95d8a-b393-806e-8d9b-000ba9ef1b8c"
   WHERE "date:Date:start" BETWEEN ? AND ?
   ORDER BY "date:Date:start"
   ```

   If anything is already there, stop and show it before writing:

   > На 28.08 уже есть: ZZAP-3 — 2 ч. Добавить к существующим, заменить или пропустить?

   Silent duplicates are the one failure mode that's genuinely expensive here — the user
   discovers them a month later when the totals don't match their invoice. Clean dates need
   no confirmation, though: just write.

2. **Create all rows in a single `create-pages` call**, with the data source as parent and
   `allow_async: false` so the result confirms what actually landed. Each page:

   ```json
   {"properties": {"Task name": "ZZAP-1", "Time spend": 4, "date:Date:start": "2026-08-10"}}
   ```

3. **Confirm with a table**, weekday included, plus the hours added and the new running total:

   ```
   Добавил 6 записей, 28 часов:

   | Дата | Task name | Time spend |
   |---|---|---|
   | Пн 17.08.2026 | ZZAP-2 | 4 |
   | …

   Итого в базе 11 строк, 48 часов.
   ```

   The weekday and the running total are what let the user catch a wrong year or a
   double-entry at a glance, which is why they're worth the extra query.

## Summaries and gaps

Read with `query-data-sources` in SQL mode. Useful shapes:

```sql
-- hours per task for a month
SELECT "Task name", SUM("Time spend") AS hours
FROM "collection://3cf95d8a-b393-806e-8d9b-000ba9ef1b8c"
WHERE "date:Date:start" BETWEEN '2026-08-01' AND '2026-08-31'
GROUP BY "Task name" ORDER BY hours DESC

-- hours per day
SELECT "date:Date:start" AS day, SUM("Time spend") AS hours
FROM "collection://3cf95d8a-b393-806e-8d9b-000ba9ef1b8c"
GROUP BY day ORDER BY day
```

Present sums as a table with a total row. Round only for display; never round what you write.

**Gaps.** When the user asks what's missing — or when a summary makes it obvious — compare
the logged days against the working days in the period and report:

- working days (Mon–Fri) in the range with no rows at all;
- days logged below 8 hours, and the shortfall;
- weeks totalling under 40, with the number missing.

Report gaps as observations, not corrections. A short day is usually a real short day, and
the user is the only one who knows whether a blank Tuesday was a holiday or a forgotten
entry. Never fill a gap on your own initiative — writing to a tracker without being asked
is exactly the thing to avoid here.

## Boundaries

Only write when the user actually reports hours. Reading, summing, and pointing out gaps are
free; creating, editing, or deleting rows happens on an explicit request. If a request would
delete or overwrite existing rows, show what will be lost and get a yes first — Notion rows
removed this way are not conveniently recoverable.
