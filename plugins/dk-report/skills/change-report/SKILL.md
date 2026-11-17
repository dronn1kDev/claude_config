---
name: change-report
description: Turn a completed code change into a non-technical, feature-level task report in English — describing WHICH user-facing features and screens were touched, not which files or functions. Use this whenever the user asks for a report, summary, changelog, MR/PR description, Jira comment, or "explain what changed for someone who doesn't read code" about work that was just finished. Also use it when the user asks for the change list "as features", "for a manager/QA/analyst", "in plain language", or says the previous answer was too technical — even if they never say the word "report".
---

# Feature-level change report

## Language

Talk to the user in the language they chose for this kit:

1. Read `~/.config/dronn1k-kit/language` (`cat ~/.config/dronn1k-kit/language 2>/dev/null`).
   Its single line is the language name, e.g. `Русский` or `English`.
2. If the file is missing or empty, or the user asks to change the language ("смени язык",
   "change language"), ask with AskUserQuestion, phrased in the language of the user's
   message: which language to talk in. Options: «Русский», «English», and «the language of
   this message» (named in that language); AskUserQuestion's own "Other" lets the user type
   any language. Resolve the answer to a language name, then
   `mkdir -p ~/.config/dronn1k-kit` and write that name to `~/.config/dronn1k-kit/language`,
   replacing what was there.
3. Use that language for everything you say to the user around the report: questions (e.g.
   whether a file belongs to the task) and comments.

The chosen language does not apply to the report itself: the report is in English by default,
and in another language only when the user asks for it (see step 5).

## Why this exists

After a change is finished, the person who has to read about it is usually not the person
who wrote it: a QA engineer planning regression, an analyst writing release notes, a manager
approving a merge request. A list of file paths and line numbers is useless to them. What they
need is the answer to one question: **which parts of the product should I now look at?**

So the job is a translation job. Every changed line lives inside some user-visible feature.
Find that feature, name it the way it appears in the product, and group the results so the
reader can walk through them like a test plan.

## Workflow

### 1. Establish exactly what changed

Never write the report from memory of the conversation alone — memory drifts and misses places.
Re-derive the change list from the repository:

- `git diff` / `git diff --staged` / `git diff <base>...HEAD` for the working change
- `git diff --stat` to see the full file list at a glance

Include changes that were already made before you joined the task (staged or committed by
someone else as part of the same task) if they belong to the same piece of work — the report
describes the task, not one person's share of it.

Separate the task's own changes from unrelated noise already present in the working tree
(generated files, dependency bumps, someone else's WIP). If you are unsure whether a modified
file belongs to the task, ask rather than silently including it.

### 2. Map each change site to a user-facing feature

For each changed location, work outward from the code until you reach something a user would
recognize. Useful signals, roughly in order of reliability:

- Screen titles and labels: localization keys, header text, button captions
- Analytics event descriptions (`trackButtonClick(description: ...)` and similar) — these are
  often already written in product language
- The route/navigation entry point: who pushes this screen, and from where
- Directory and class names as a last resort — they hint at the domain but often lag behind
  the product ("oldPayments" is still just "payments" to a user)

Then name the feature the way the product names it: *"Card block / unblock — SMS code
confirmation screen"*, not *"CABlockCardOTPScreen"*.

### 3. Trace shared code to every flow it serves

This is the step that is easiest to skip and most costly to get wrong. A change inside a shared
screen, widget, or helper silently changes every flow that uses it, and those flows are exactly
what QA needs to retest.

When a changed file looks generic (a shared screen, a common widget, a utility), search for its
usages and list the flows it is reached from. Present it as one entry with the affected flows
named underneath, and say plainly that the fix applies to all of them.

### 4. Write the report

Use this structure. It is a default, not a cage — drop a section that would be empty, and add
one if the change genuinely needs it (for example a "Migration / rollout notes" section for
something that needs a config change on release).

```markdown
# Task Report: <what was done, in product terms>

## Objective
One short paragraph: what was changed and why, plus what explicitly stays the same
(position, behavior, data) so the reader knows what NOT to worry about.

## Scope of Changes
Grouped by product area (**Cards**, **Payments**, **Settings**, ...), numbered continuously
across groups so items can be referenced by number.
1. **Feature name** — which screen or step of the flow was touched

## Intentionally Excluded
Places that look like they should have been changed but were not, each with the reason
(out of scope by decision, no change needed, handled separately).

## Result
Counts, what was and was not verified, and any known blockers.
```

### 5. Keep it honest and readable

- **No code identifiers.** No file paths, class names, function names, or line numbers. If you
  feel the urge to include one, it usually means step 2 was not finished.
- **No attribution.** Write about the work, not about who did which part — no "I", no "the user
  did this part". The reader cares about the product, and mixed attribution invites questions
  that the report cannot answer.
- **Say what was not verified.** If tests were not run, or the app could not be launched, state
  it in one plain sentence with the reason. A report that quietly implies more confidence than
  exists is worse than no report.
- **"Intentionally excluded" is not optional filler.** When a reviewer notices an untouched
  spot that looks similar, their first assumption is that it was missed. Naming those spots
  up front prevents that whole round trip.
- Write the report in English by default, whatever language you talk to the user in. If the
  user asks for another language, write the report in that language and keep the same
  structure.
- Output the report as markdown in the chat reply so it can be pasted straight into a merge
  request or ticket. Only write it to a file if the user asks for a file.

## Example of the translation step

The change: an underline was removed from a "Resend code" button in eleven places.

Raw material — what the diff shows:

```
lib/ui/screens/cardDetails/actions/block/block_otp.dart:252
lib/ui/screens/otp_screens/otp_by_sms.dart:266
```

What ends up in the report:

> **Cards**
> 1. **Card block / unblock** — SMS code confirmation screen
>
> **Shared SMS confirmation screen**
> 2. **Universal SMS code entry screen**, reused across several flows: card PIN change,
>    viewing card details, confirming operations pending approval, and cardless cash
>    withdrawal. The fix here applies automatically to all of these.

The second entry is the whole point of step 3: nothing in the diff says "cardless cash
withdrawal", and nobody would have retested it.
