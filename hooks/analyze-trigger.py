#!/usr/bin/env python3
"""UserPromptSubmit hook: remind Claude to use the `analyze` skill on analysis/research requests."""
import json
import re
import sys

TRIGGER = re.compile(
    r"проанализ|анализ\w*|исследу|исследова|изучи|ресё?рч|ресерч"
    r"|\banaly[sz]|\bresearch|\binvestigat",
    re.IGNORECASE,
)
# Static-analysis tooling, not a research request.
EXCLUDE = re.compile(r"(flutter|dart)\s+analyze|analysis_options|статическ\w+\s+анализ", re.IGNORECASE)

REMINDER = (
    "This message may be a request to analyze or research a question. If it is, follow the "
    "`analyze` skill: settle width (paths) and depth (default: standard), launch one `analyst` "
    "subagent per path in parallel, merge the results. If it is not (e.g. running a linter, "
    "reviewing a diff, a passing mention), ignore this note."
)


def main() -> None:
    try:
        prompt = json.load(sys.stdin).get("prompt", "")
    except Exception:
        return
    if prompt.lstrip().startswith("/") or EXCLUDE.search(prompt) or not TRIGGER.search(prompt):
        return
    json.dump(
        {"hookSpecificOutput": {"hookEventName": "UserPromptSubmit", "additionalContext": REMINDER}},
        sys.stdout,
    )


if __name__ == "__main__":
    main()
