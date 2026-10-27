---
name: analyze
description: Run a structured analysis or research of a question — settle its width (which paths/angles to investigate, 1–3 by default) and depth (quick / standard / deep), launch one `analyst` subagent per path in parallel, then merge their findings into one answer with confidence levels and sources. Use this whenever the user asks to analyze, research, investigate, study, or compare something — "проанализируй", "исследуй", "изучи вопрос", "разберись, что лучше", "сделай ресёрч", "analyze", "research", "investigate" — even if they don't mention width or depth. Not for static code analysis tools (flutter/dart analyze, linters) or for reviewing a diff.
---

# Analyze

The user wants answers they can act on, and two things decide the shape of the work:
**width** — which paths the research goes down — and **depth** — how long it takes and how
well-verified the result is. The user picks the width; depth defaults to standard. Everything
else here is about running the paths in parallel and merging them honestly.

## 1. Read the request

Pull out of the user's message:

- **Question** — what they want to know.
- **Goal** — what decision or understanding the answer is for. Often implied; if it is
  genuinely unclear and would change what counts as important, ask (step 2).
- **Width** — paths the user named explicitly ("посмотри с точки зрения цены и поддержки",
  "по трём направлениям: …"). Take them as given, any number.
- **Depth** — "быстро", "на скорую руку" → quick; "глубоко", "основательно", "подробно" →
  deep; otherwise **standard**.
- **Save** — "сохрани", "в обсидиан", "в research" → save; "не сохраняй" → don't; otherwise
  offer it in one plain-text line after the answer (step 6).

**Check earlier research first.** List `~/.claude/claude_config/research/` and grep it
for the topic. If a related note exists, read it, tell the user in one line, and use it:
skip what is already settled, and have the analysts focus on what is new or was left open.

## 2. Settle the width (and goal, if unclear)

If the user named the paths, go to step 3 without asking.

Otherwise propose paths with AskUserQuestion, `multiSelect: true`:

- 2–4 options, each a distinct angle the question can be attacked from — not the same angle
  phrased differently. Good axes: viewpoint (user / business / engineering), source type
  (public data / internal docs / our code), dimension (cost / risk / speed), alternative
  (option A / option B / status quo).
- Recommend 1–3 by marking them "(Recommended)" and listing them first. Offer a fourth only
  when the question clearly has more than three meaningful angles.
- Each option's description says in one line what that path covers and where it will look.
- The user can type their own path via "Other" — treat it as a path like any other.

If the goal is unclear, add it as a second question in the same AskUserQuestion call, so the
user answers everything at once.

Don't ask about depth. Announce it instead (step 3) so the user can change it if they want.

## 3. Announce and launch

One line to the user before launching, so they know what to expect:

> Запускаю 3 аналитика (цена, поддержка, миграция), глубина: стандарт, ~5–10 мин.

Then launch **all paths in one message**, one Agent call per path, `subagent_type: "analyst"`,
running in the background. Pick the model by depth:

| Depth | `model` | Budget per path | Expected wait |
|---|---|---|---|
| quick | `sonnet` | 2–3 sources, no cross-check | ~1–3 min |
| standard | `opus` | 5–10 sources, key claims confirmed twice | ~5–10 min |
| deep | `opus` | 10–20+, primary sources, everything cross-checked, plus a critic pass (step 4) | ~15–30+ min |

Each analyst's prompt must stand alone — it does not see this conversation:

```
Question: <the full question>
Goal: <what the answer is for>
Path: <name> — <what this path covers and what it does NOT cover (the other paths)>
Depth: <quick|standard|deep>
Sources: <which fit this path: web / project code at <path> / Notion / Gmail>
Prior research: <summary of a related note from research/, or "none">
```

Choose sources per path: public facts → web; "how it works in our project" → project code;
"what was already discussed or decided" → Notion, mail. Jira/Confluence need the Atlassian
connector authorized first; if a path needs them and they're unavailable, say so.

While the analysts run, stay available — the user may add context or change the plan.

## 4. Deep only: critic pass

When all paths are done at depth **deep**, launch one more `analyst` with the draft
conclusions from all paths under "Draft conclusions to challenge" (critic mode). Fold its
result into the synthesis: downgrade or drop conclusions it breaks, and say so.

## 5. Merge and answer

Don't paste the analysts' reports one after another — the value is in the merge. Answer in
the user's language, in this shape:

```
## <Вопрос, коротко>

**Коротко:** <the answer in 2–3 lines — what to do or what is true, with overall confidence>

*Ширина: <paths> · Глубина: <level> · <date>*

### Где пути сходятся
- [уверенность] [факт|вывод|предположение] <conclusion supported from several paths> — [n]

### Где расходятся
- <conflict> — <which path says what, and which side the evidence favors, or why it's unresolved>

### По путям
**<Path 1>** — <the 2–4 most important findings, with labels and sources>
**<Path 2>** — …

### Открытые вопросы
- <what is still unclear> → <which path to dig deeper, and how>

### Источники
[1] <title> — <url> (<date>)
```

- Keep the labels from the analysts: confidence (высокая / средняя / низкая) and type
  (факт / вывод / предположение). Raise confidence only when independent paths agree;
  lower it when they conflict.
- Renumber sources into one list; drop duplicates.
- Drop "Где расходятся" if nothing conflicts — but say so in one line; agreement is a finding.
- End "Открытые вопросы" with an offer the user can accept in one phrase, e.g.
  «Могу копнуть путь „миграция" глубже».
- If an analyst failed or ran out of budget, say which path is incomplete and why.

## 6. Save (offer unless told)

If the user didn't say whether to save, end the answer with one plain-text line offering it,
e.g. «Сохранить в Obsidian? Скажи „сохрани", если нужно.» Don't use AskUserQuestion here —
the user replies in chat only if they want it saved. Keep the analysts' full reports in
context until then, so a later "сохрани" can still write them.

To save, write `~/.claude/claude_config/research/<YYYY-MM-DD> <short title>.md`:

```markdown
---
type: research
date: <YYYY-MM-DD>
question: "<the question>"
goal: "<goal>"
paths: [<path 1>, <path 2>]
depth: <quick|standard|deep>
tags: [research]
---

<the merged answer from step 5>

## Отчёты по путям

<each analyst's full report, as returned>
```

If a related note was found in step 1, link it with `[[<note name>]]` in a "Связанное"
line under the frontmatter — inside research notes wiki-links are the right tool, since
they live in Obsidian. The `research/` folder is gitignored, so saved notes stay local.
