# Global instructions

## Git

- Write commit messages in English.

## Analysis and research

- When asked to analyze, research, or investigate a question ("проанализируй", "исследуй", "изучи", "ресёрч"), use the `analyze` skill. It settles width (paths) with the user, defaults depth to standard, and runs `analyst` subagents in parallel.

## Architecture

- When asked for solution options ("как лучше сделать", "предложи варианты") or to review a solution for flaws and uncovered cases, delegate to the `architect` subagent instead of answering directly. It doesn't see the conversation, so pass the mode (options/review), the task, constraints, what's already decided, and relevant file paths or the solution text. Relay its result without trimming the scenarios; if it gives options, offer the user a choice.

## Writing code

- Any code-writing task goes to the `engineer` subagent. The only exception is a trivial 1–2 line edit, which you make yourself — but still by the rules in `/Users/dronn1k/claude_config/rules/` (`general.md` plus the language file; read them first).
- The engineer never works without a plan the user approved. Flow:
  1. Enter plan mode (EnterPlanMode).
  2. Run `engineer` without an approved plan — it edits nothing and returns either a plan followed by "# Справка для исполнителя" (a handoff of facts it found), or "Вопросы перед планом". If the user already chose an approach (e.g. an `architect` option), pass it along.
  3. If it returned questions: ask the user with AskUserQuestion — one question per item, its options as options, the recommended one first and marked "(Recommended)". Send the answers to the same engineer (SendMessage) so it continues with its context; repeat until it returns a plan.
  4. Write only the plan — from `# План:` up to `# Справка для исполнителя` — to the plan file unchanged and call ExitPlanMode so the user approves it in the plan UI. Keep the handoff; don't show it to the user unless they ask.
  5. On feedback, send it to the same engineer (SendMessage) for a revised plan (it may ask questions again — step 3) and repeat step 4. Always use the handoff from its latest answer.
  6. Only after approval, run a new `engineer` with, verbatim: `Task:` — the user's original request; `Approved plan:` — the approved plan; `Handoff (facts, not approved; plan wins):` — the latest handoff. Never paraphrase or trim the plan or the handoff. Never pass `Approved plan:` for a plan the user hasn't approved.
  7. If the engineer stops on a material deviation, its amendment goes through approval the same way. The next engineer gets the task, the plan, the approved amendment, the handoff, and the previous engineer's report on what is already done.
- A plan the user wrote themselves and told you to execute counts as approved.
- Relay the engineer's report including rule violations and failed checks. The engineer never commits; commits happen only when the user asks.
