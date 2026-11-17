---
name: code-flow
description: The protocol for any task that writes or changes code — run the `dk-code:engineer` agent through a read-only planning phase, get the user's approval of its plan in plan mode, then run a fresh engineer to implement it. Load this before launching `dk-code:engineer` and for any request to write, fix, add, change, or refactor code ("напиши", "исправь", "добавь", "переделай", "отрефактори", "implement", "fix", "add", "refactor"). Also covers asking the `dk-code:architect` agent for solution options or a review of a solution ("как лучше сделать", "предложи варианты", "посмотри решение на недочёты").
---

# Code flow

Code is written by the `dk-code:engineer` agent, and never without a plan the user approved.
This skill is the orchestrator's side of that contract: how to run the engineer, how to read
its answers, and how the plan gets approved.

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
3. Use that language for everything you say to the user here, and pass it to every agent you
   launch as a `Language: <language>` line. The agents then write their answers in it too.

## Trivial edits

Any code-writing task goes to `dk-code:engineer`. The only exception is a trivial 1–2 line
edit, which you make yourself — but still by the rules in `${CLAUDE_PLUGIN_ROOT}/rules/`
(`general.md` plus the file for the language, e.g. `dart.md`; read them first).

## Reading the engineer's answers

The engineer writes in the chosen language, so its headings are translated. Recognize each
answer by its role, not by an exact string:

- **Questions** — a first-level heading meaning "questions before the plan" (Russian
  sample: «Вопросы перед планом»), then numbered questions, each with options and, except for style
  questions, a line with the recommended option.
- **No changes needed** — a first-level heading meaning "no changes needed" («Изменений не
  требуется»), with the reasons and, optionally, a section of things noticed along the way
  («Замечено попутно»).
- **Plan** — an answer with exactly two first-level headings. The first opens the plan
  («План: …»), the second opens the handoff («Справка для исполнителя»). The plan is
  everything from the first heading up to the second; the handoff is everything from the
  second heading to the end. If the answer has a different number of first-level headings,
  don't guess where to cut: ask the same engineer (SendMessage) to resend it in that shape.

## Flow

1. Run `dk-code:engineer` without an approved plan, before entering plan mode — its PLAN
   phase is read-only anyway. Give it the task, the context, the relevant paths, and
   `Language: <language>`. If the user already chose an approach (e.g. an architect option),
   pass it along. It returns questions, a plan with a handoff, or "no changes needed".
2. If it returned questions: ask the user with AskUserQuestion (outside plan mode) — one
   question per item, its options as options, the recommended one first and marked
   "(Recommended)" in the chosen language. Style-conflict questions — exactly two options,
   "our style" vs "the project's style" at a given place (Russian sample: «Наше оформление» /
   «Оформление проекта») — go to the user as they are, with no recommendation; never answer
   them yourself or carry an earlier answer over to another place. Send the answers to the
   same engineer (SendMessage) so it continues with its context; repeat until it returns a
   plan or "no changes needed".
3. If it returned "no changes needed": relay its findings to the user as an analysis
   answer — no plan mode, no plan file, no ExitPlanMode. Items it noticed along the way can
   be offered as follow-ups.
4. Once it returns a plan: enter plan mode (EnterPlanMode), write only the plan — from its
   first-level heading up to the handoff's — to the plan file unchanged, and call
   ExitPlanMode so the user approves it in the plan UI. Keep the handoff; don't show it to
   the user unless they ask.
5. On feedback (plan mode stays on), send it to the same engineer (SendMessage) for a revised
   plan (it may ask questions again — step 2), rewrite the plan file and call ExitPlanMode
   again. Always use the handoff from its latest answer.
6. Only after approval, run a new `dk-code:engineer` with these parts, the plan and the
   handoff verbatim:

   ```
   Task: <the user's original request>
   Language: <language>
   Approved plan:
   <the approved plan>
   Handoff (facts, not approved; plan wins):
   <the latest handoff>
   ```

   Never paraphrase or trim the plan or the handoff. Never pass `Approved plan:` for a plan
   the user hasn't approved.
7. If the engineer stops on a material deviation, its amendment goes through approval the
   same way. The next engineer gets the task, the language, the plan, the approved
   amendment, the handoff, and the previous engineer's report on what is already done.

- A plan the user wrote themselves and told you to execute counts as approved.
- Relay the engineer's report including rule violations and failed checks. The engineer
  never commits; commits happen only when the user asks.

## Architect

When the user asks for solution options ("как лучше сделать", "предложи варианты") or for a
review of a solution for flaws and uncovered cases, delegate to the `dk-code:architect` agent
instead of answering directly. It doesn't see the conversation, so pass the mode
(options/review), the task, constraints, what's already decided, the relevant file paths or
the solution text, and `Language: <language>`. Relay its result without trimming the
scenarios; if it gives options, offer the user a choice, and pass the chosen one to the
engineer in step 1.
