---
name: obsidian-docs
description: Write or reformat documentation and notes as Markdown files in an Obsidian vault or a project's docs folder — feature docs, architecture decisions, how-tos, reference pages, meeting notes, research notes, and guides of any kind (games, life hacks). Two modes - create a new note from the conversation, or reformat an existing note without changing its meaning. Use whenever the user asks to document something, write it up, make a note or a guide, "write the docs", "document this", "describe it in Obsidian", "make a note", "make a guide", "tidy up this note". Prefer this over Claude Docs or Word unless the user names that format.
---

# Obsidian docs

Good documentation is found, trusted, and read. Found — it sits where the reader looks and is
linked from related notes. Trusted — it says what is true, when, and from where. Read — the
point is in the first lines and the rest is easy to scan. Every step below serves one of these.

## 0. Language

Talk to the user in the language they chose for this kit:

1. Read `~/.config/dronn1k-kit/language` (`cat ~/.config/dronn1k-kit/language 2>/dev/null`).
   Its single line is the language name in English, e.g. `Russian` or `English`.
2. If the file is missing or empty, or the user asks to change the language (in whatever
   language they ask), ask with AskUserQuestion, phrased in the language of the user's
   message: which language to talk in. Options: Russian, English, and the language of this
   message, each named in the language of the user's message; AskUserQuestion's own "Other"
   lets the user type any language. Resolve the answer to a language name in English, then
   `mkdir -p ~/.config/dronn1k-kit` and write that name to `~/.config/dronn1k-kit/language`,
   replacing what was there.
3. Use that language for everything you say to the user here: questions, the rules line in
   step 1, the list of changes, the final report. Sample phrases below are in English —
   translate them.

The language of the note itself is decided separately: the language of the vault or project
(step 1); only if that can't be determined, the chosen language.

## 1. Find where the docs live and what rules apply

Work out the place from the session's context — the working directory and any added
directories — before writing anything.

**An Obsidian vault** — a directory with `.obsidian/` and no code project around it:
work in that vault, by its rules. Learn them from the vault itself:
- `README.md`, `CLAUDE.md`, or a notes-about-the-vault file, if any.
- `.obsidian/app.json` — `useMarkdownLinks` (wiki-links vs Markdown links), `newLinkFormat`,
  `attachmentFolderPath`, `newFileFolderPath`.
- `.obsidian/templates.json` — the templates folder; read the templates in it.
- `.obsidian/community-plugins.json` — e.g. Dataview means index notes may use queries.
- Five to ten existing notes close to the topic: their folders, file names, frontmatter keys,
  tags, heading style. Existing practice beats the defaults in this skill.

**A code project** — `pubspec.yaml`, `package.json`, `.git`, and so on: look for instructions
on writing docs — `CLAUDE.md`, `AGENTS.md`, `CONTRIBUTING.md`, `docs/README.md`, a docs
style guide — and for an existing `docs/` folder whose notes show the conventions.
If found, follow them. If not, ask the user with AskUserQuestion where the note should go
(e.g. `docs/` in the project, an Obsidian vault path, elsewhere) and which link style to use.
Recommend Markdown links for docs inside a repository — wiki-links break on GitHub/Bitbucket.

**Neither, or both and it's unclear which** — ask, same way.

Where the found place has no rules of its own for something, use
[references/conventions.md](references/conventions.md). Say in one line which rules you're
following, in the chosen language: "Writing to the `Work` vault, by its rules: wiki-links, Latin tags."

## 2. Pick the mode

- **Create** — the user wants something written up: a feature, a decision, a guide, the
  result of this conversation.
- **Reformat** — the user points at an existing note to put in order.

## 3a. Create

1. **Type.** Pick the note type from [references/templates.md](references/templates.md):
   feature, decision, howto, reference, research, meeting, guide, note. If it's genuinely
   ambiguous, ask together with any other question — not separately.
2. **Check for an existing note on the topic.** Search the docs location by title words,
   tags, and key terms. If a note already covers it, propose updating that note instead of
   creating a second one — duplicates are how documentation stops being trusted.
3. **Gather the content.** From the conversation, the code, the user's material. For guides
   and anything from the web, keep the sources and the version or date the facts apply to
   (game patch, app version). Never invent a fact to fill a template section — drop the
   section or mark the gap: `> [!question] Not found out: …`.
4. **Write** by the type's template and the conventions: frontmatter, H1, the point in the
   first lines, short sections, Obsidian features where they help.
5. **Link.** Link to related notes you found. If the area has an index note (MOC), add the
   new note to it — that's the one edit to another note you may make without asking. Any
   other note that should link back: list it in the final message instead of editing it.
6. **Check** (step 4).

## 3b. Reformat

The content belongs to the user. Change the form, not the meaning:
- Keep every fact, example, and link. Don't delete, don't rewrite claims, don't "improve"
  conclusions. Fix obvious typos only.
- Do: add or fix frontmatter, restructure headings, put the point on top, turn walls of text
  into lists or tables, turn warnings and tips into callouts, a Mermaid diagram where the
  text describes a flow, wiki-links to notes that exist.
- If something looks wrong or outdated, don't fix it — add `> [!question]` with what's
  suspicious, and mention it in your message.

Before writing, show the user a short list of what will change and ask with AskUserQuestion
whether to apply it ("Apply" / "Don't apply"). For a long note, show the new outline
instead of every change.

## 4. Check before you finish

- Frontmatter is valid YAML; dates are `YYYY-MM-DD`; `updated` is today on reformat.
- Every `[[link]]` points to a note that exists, or is intentionally a placeholder for a
  note worth writing — say which.
- No near-duplicate note exists with a similar title.
- New tags: if a tag is used nowhere else in the vault, check for an existing synonym
  (`flutter` vs `Flutter` vs `dart-flutter`) and use that instead.
- Attachments (images, files) are in the vault's attachment folder.

Don't commit — if the docs location is a git repository, committing stays with the user.

## 5. Report

One short message: the file path as a link, the type, what it links to, and anything left
for the user — notes that should link back, open questions, suspicious facts from reformat.
