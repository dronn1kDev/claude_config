# Templates by note type

Section skeletons. Section names are in English; in a note in another language,
translate them, keeping the structure.
Drop a section that would be empty — never pad it. Frontmatter per
[conventions.md](conventions.md), with `type` set to the template's name.

## feature — how a product feature works

```
# <Feature as the user knows it>
<1–3 lines: what it lets the user do>

## Why
## What the user sees
<flow from the user's side; Mermaid for a multi-step flow>
## How it works
<components, data flow, links to code — file paths, not code dumps>
## States and errors
<table: state / when / what the user sees>
## Limitations
## Related
```

## decision — an architecture or product decision (ADR)

```
# <Decision as a statement: "Store tokens in the Keychain">
<1–2 lines: what was decided>

## Context
<the problem and the forces at play>
## Decision
## Options considered
<table: option / pros / cons / why not>
## Consequences
<what gets easier, what gets harder, what to watch>
```

`status`: `active` while in force, `outdated` when replaced — with a link to the replacement.

## howto — instructions to get a task done

```
# <How to do X>
<1 line: the result you'll have at the end>

## Prerequisites
## Steps
1. …   ← one action per step; commands in code blocks
## How to check
## If it didn't work
<symptom → cause → fix>
```

## reference — facts to look up

```
# <Topic>
<1–2 lines: what's here and when to look>

## <Main table or list of facts>
## Details
## Sources
```

## research — results of an analysis

Same format as the `analyze` skill produces (In short / Where the paths agree / Where they disagree /
By path / Open questions / Sources). Keep the confidence and fact/inference labels.

## meeting — notes from a meeting or call

```
# YYYY-MM-DD <Topic>
**Participants:** …

## Decisions
## Tasks
- [ ] <who> — <what> — <by when>
## Discussed
## Open questions
```

Decisions and tasks come first — that's what people come back for.

## guide — how to get good at something (games, life hacks, hobbies)

```
# <What the guide achieves: "Elden Ring — bleed build">
<1–3 lines: what you get and for whom>

> [!info] Valid for: <game patch / app version / date checked>

## What you need
## Step by step
## Tips
> [!tip] …
## Common mistakes
> [!warning] …
## Sources
```

Guides go stale fastest: always fill `version` or the "Valid for" line, and `source`.

## note — anything that fits no other type

```
# <Title>
<1–3 lines: the point>

## <Sections as the content needs>
## Related
```
