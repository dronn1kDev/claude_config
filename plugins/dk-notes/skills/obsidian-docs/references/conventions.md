# Default conventions

Used only where the vault or project has no rule of its own. Existing practice wins.

## Files and folders

- **File name = note title**, human-readable, in the note's language:
  `Оплата картой.md`, `Elden Ring — билд на кровотечение.md`. No dates in names, except
  dated notes: research and meetings get a `YYYY-MM-DD ` prefix.
- **Folders by area, not by type**: `Работа/Acme/`, `Игры/`, `Дом/`. The type lives in
  frontmatter, so one area holds its features, decisions, and guides together.
- **One index note per area (MOC)** named after the area (`Игры/Игры.md`): a short intro and
  links to the area's notes, grouped by type or sub-topic. With Dataview installed, a query
  may replace the manual list.

## Frontmatter

```yaml
---
type: guide            # feature | decision | howto | reference | research | meeting | guide | note
status: active         # draft | active | outdated
tags: [games/elden-ring, build]
created: 2026-10-07
updated: 2026-10-07
related: ["[[Elden Ring]]"]
source: https://…      # guides and references taken from the web; omit otherwise
version: "1.16"        # what the facts apply to: game patch, app or library version; omit if n/a
aliases: [кровотечение билд]   # optional, alternative names to find the note by
---
```

- Keys in this order; omit a key rather than leave it empty (except `tags`).
- `status: outdated` instead of deleting — and a callout on top saying what replaced it.

## Tags

- Latin, lowercase, kebab-case; hierarchy with `/`: `work/acme`, `games/elden-ring`,
  `flutter/state`.
- Tags are for topics. The note's kind is `type`, its state is `status` — not tags.
- At most five per note. Reuse existing tags before inventing new ones.

## Links

- **In a vault:** wiki-links `[[Note]]`, `[[Note#Section]]`, `[[Note|text]]`. Link the first
  mention of a concept that has its own note, not every mention.
- **In a repository's docs:** relative Markdown links `[text](../path/file.md)`.
- Embed with `![[Note#Section]]` only when the embedded part must stay in sync; otherwise link.

## Page structure

1. One H1 — the title.
2. The point in 1–3 lines right under it: what this is and the main takeaway.
   For long notes, a `> [!summary]` callout.
3. H2 sections, H3 at most. A section longer than a screen gets split or summarized.
4. Short paragraphs; lists for enumerations; numbered lists for steps; tables for
   comparisons and parameters.
5. Write in the language of the vault or project; if it can't be determined, in the language
   from `~/.config/dronn1k-kit/language`.

## Obsidian features — when to use them

| Feature | Use for |
|---|---|
| `> [!note]` | side information worth noticing |
| `> [!tip]` | tricks, shortcuts, "лайфхак" moments in guides |
| `> [!warning]` / `> [!danger]` | pitfalls, irreversible steps, things that break |
| `> [!example]` | a worked example |
| `> [!question]` | unknowns, unverified facts, open questions |
| `> [!summary]` | the takeaway of a long note |
| Mermaid (` ```mermaid `) | flows, state machines, sequences, simple architecture — when prose would need more than ~5 sentences to describe it |
| Tasks `- [ ]` | action items in meetings and plans |
| Code blocks with language | commands, config, code — never untagged |
| Foldable callout `> [!tip]-` | long optional detail that would clutter the page |

Don't decorate: no emoji in headings, no callout for ordinary text, no diagram that repeats
a three-item list.
