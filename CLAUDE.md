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
  2. Run `engineer` without an approved plan — it returns a plan and edits nothing. If the user already chose an approach (e.g. an `architect` option), pass it along.
  3. Write the engineer's plan to the plan file unchanged and call ExitPlanMode so the user approves it in the plan UI.
  4. On feedback, send it to the same engineer (SendMessage) for a revised plan and repeat step 3.
  5. Only after approval, run `engineer` with `Approved plan:` followed by the approved plan text. Never pass `Approved plan:` for a plan the user hasn't approved.
  6. If the engineer stops on a material deviation, its amendment goes through approval the same way.
- A plan the user wrote themselves and told you to execute counts as approved.
- Relay the engineer's report including rule violations and failed checks. The engineer never commits; commits happen only when the user asks.
