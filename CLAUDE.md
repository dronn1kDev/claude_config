# Global instructions

## Git

- Write commit messages in English.

## Analysis and research

- When asked to analyze, research, or investigate a question ("проанализируй", "исследуй", "изучи", "ресёрч"), use the `analyze` skill. It settles width (paths) with the user, defaults depth to standard, and runs `analyst` subagents in parallel.

## Architecture

- When asked for solution options ("как лучше сделать", "предложи варианты") or to review a solution for flaws and uncovered cases, delegate to the `architect` subagent instead of answering directly. It doesn't see the conversation, so pass the mode (options/review), the task, constraints, what's already decided, and relevant file paths or the solution text. Relay its result without trimming the scenarios; if it gives options, offer the user a choice.
