# dronn1k-kit

A Claude Code plugin marketplace: skills and agents for research, writing code, notes, and change reports. The plugins install through `/plugin`, live apart from your own configuration, and leave your `agents/`, `skills/`, and `CLAUDE.md` untouched.

## What's inside

| Plugin | Contents |
|---|---|
| `dk-research` | The `analyze` skill: agrees with you on the width (paths) and depth of a research question, runs `analyst` agents in parallel, and merges their findings into one answer with confidence levels and sources. |
| `dk-code` | The `engineer` agent writes code by strict rules from `rules/`, and only from a plan you approved. The `architect` agent proposes solution options and looks for flaws in an existing solution. The `code-flow` skill describes how the orchestrator works with them: plan, questions, approval, implementation. |
| `dk-notes` | The `obsidian-docs` skill: writes or tidies up notes and documentation in Markdown — in an Obsidian vault or in a project's docs folder. |
| `dk-report` | The `change-report` skill: turns a finished code change into a feature-level report for people who don't read code (QA, analysts, managers). |

## Installation

In Claude Code:

```
/plugin marketplace add dronn1kDev/claude_config
/plugin install dk-research@dronn1k-kit
/plugin install dk-code@dronn1k-kit
/plugin install dk-notes@dronn1k-kit
/plugin install dk-report@dronn1k-kit
```

Install any combination — the plugins don't depend on each other. If the repository is private, Claude Code fetches it through git, so you need access to it: an SSH key or an authenticated `gh`. Updates arrive with every commit, since the plugins have no version number.

## Usage

Plugin components are named with the plugin prefix:

- skills — `/dk-research:analyze`, `/dk-code:code-flow`, `/dk-notes:obsidian-docs`, `/dk-report:change-report`; Claude also launches them on its own, by their descriptions;
- agents — `dk-research:analyst`, `dk-code:engineer`, `dk-code:architect`.

To apply the `engineer` protocol to every coding task, add a line like "For any task that writes or changes code, first load the `dk-code:code-flow` skill and work by it" to your `~/.claude/CLAUDE.md`. A plugin can't ship a `CLAUDE.md` of its own.

**Language.** The first time you run any skill in the kit, Claude asks which language to talk to you in and stores the answer in `~/.config/dronn1k-kit/language` — one file for all plugins. To choose again, say "change language" in any language. The language applies to the conversation and to the agents' answers. `change-report` writes its report in English by default, and `obsidian-docs` writes notes in the language of the vault or project.

## Good to know

- The prompts were written by the author for personal use: around the author's habits, projects, and stack (the code rules cover the general case and Dart/Flutter).
- All agents run on the `opus` model, which is expensive.
- The code rules in `dk-code` are strict and override the project's conventions, except where the linter requires otherwise. Read [general.md](plugins/dk-code/rules/general.md) before installing.

## Repository layout

- `.claude-plugin/marketplace.json` — the marketplace definition.
- `plugins/<plugin>/` — the plugins: `.claude-plugin/plugin.json`, `skills/<name>/SKILL.md`, `agents/<name>.md`; `dk-code` also has `rules/` — the code rules: `general.md` for any language, `<language>.md` for a specific one.

Links inside a plugin point only to files of the same plugin: through `${CLAUDE_PLUGIN_ROOT}` or relative paths.

## Development

Add your clone as a local marketplace with `/plugin marketplace add <path to clone>`, then install the plugins as in "Installation". The plugins are read straight from the clone, so edits in `plugins/` take effect after `/reload-plugins`, without reinstalling. Before committing, validate the marketplace and the plugins:

```bash
claude plugin validate .
for p in plugins/dk-*; do claude plugin validate "$p"; done
```

Warnings about `version` are expected: the version is left out on purpose.
