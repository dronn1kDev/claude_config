# General coding rules

Apply to code in any language. They take priority over the project's own conventions
(CLAUDE.md, style guides) — with one exception: if a rule conflicts with the project's linter,
analyzer, or CI and following the rule would make them fail, follow the linter and report the
conflict.

When the existing code a change goes into is written differently from what a rule requires,
the user decides, separately for each such place, which style wins — never the one writing
the code:

- **our style** — the rule applies, and the existing code of that place is brought to the
  same style as part of the task;
- **the project's style** — the new code follows the existing code, and the rule is dropped
  for that place.

Two styles side by side in one place are never the answer.

A rule may be broken only with a reason stated in the final report. Never silently.

## G1. Short function bodies

Keep a function body within **15–20 lines of code**. A longer body is a sign it does more
than one thing — split it into named steps.

**Layout is the exception: up to 200 lines.** A layout function is one whose body is a
declarative UI tree — a Flutter `build` method or another method returning a widget tree,
a JSX/TSX render, a SwiftUI `body`, a Compose `@Composable`, an HTML template. The exception
covers the tree only. Logic inside it — event handlers longer than a single call, data
transformations, non-trivial conditions — is extracted into ordinary functions, which keep
the 15–20 line limit.

How to count, for both limits: blank lines, comment lines, and lines that contain only
closing brackets and punctuation (`}`, `),`, `]);`) are not counted.

*Why:* logic must fit on one screen to be understood without scrolling back. A UI tree reads
top to bottom like a document, and splitting it too early scatters one screen across files.

## G2. Blank lines separate meaning

Use blank lines to split a function into its logical parts: preparation, the main work,
the result. Code that belongs together stays together; unrelated steps are visibly apart.

*Why:* the reader sees the structure before reading the details.

## G3. Meaningful names, up to 4 words

Fields, variables, methods, and classes get names that say what they are or do, in **no more
than four words** (`userName`, `loadOrderHistory`, `maxRetryCount`). If a good name needs more,
the thing is probably doing too much.

A class whose behaviour applies only to one customer, build, or platform says so in its name
(`JKBWalletCardsFilter`), so the restriction is visible at every call site and needs no comment.
To stay within four words, drop details from the class name and carry them in member names
instead: the filter is `JKBWalletCardsFilter`, and what it filters by lives in
`excludedStatusCodes`. A collection's name says what the code does with it (`excluded…`),
not only what it holds.

*Why:* names are most of the documentation code ever gets.

## G4. Booleans read as questions

Boolean fields and variables are phrased as yes/no questions: `isActive`, `hasAccess`,
`canBeClosed`, `shouldBeOpened`. Never `active`, `flag`, `status`, `check`.

*Why:* `if (isActive)` reads as a sentence; `if (active)` makes the reader guess the type.

## G5. Early return over nesting

Handle invalid and edge cases first and return; keep the main path unindented.
Nesting deeper than **2–3 levels** must be restructured.

*Why:* every level of nesting is one more condition the reader has to hold in mind.

## G6. At most 3–4 parameters

A function takes no more than three or four parameters. Beyond that, group related ones into
an object (a parameters class, a record, a config). Optional named parameters with a default
value don't count toward the limit — callers don't pass them, so they can't be mixed up.

*Why:* long parameter lists get called with arguments in the wrong order.

## G7. No magic numbers or strings

Literals with meaning become named constants: `maxRetryCount = 3`, not a bare `3`.
Obvious values (`0`, `1`, empty string, `-1` as "not found" where idiomatic) are fine inline.

Elements of a named collection of codes stay literals, each with a short comment saying what
the code means — no separate constant per element. A separate named constant is for a value
used on its own or in more than one place.

*Why:* the name explains the value and gives one place to change it.

## G8. Methods start with a verb; boolean methods ask

Method and function names start with a verb: `loadUser`, `calculateTotal`, `sendInvite`.
Methods that return a boolean follow G4: `isValid()`, `hasPermission()`, `canSubmit()`.

*Why:* a verb tells the reader the call does something; a question tells them it only checks.

## G9. No abbreviations

Write words in full: `button`, not `btn`; `message`, not `msg`; `index`, not `idx`.
Allowed: universally known abbreviations (`id`, `url`, `api`, `json`, `http`, `ui`),
conventional loop counters (`i`, `j`) in short loops, and names of customers, products, and
brands spelled the way they spell themselves (`JKB`).

*Why:* abbreviations save typing once and cost reading every time.

## G10. Comments explain why; no leftovers

Comments explain intent, constraints, and non-obvious decisions — not what the next line does.
One "what" comment is allowed: the meaning of a literal code in a collection (G7), since the
code itself can't show it.
Don't leave commented-out code, debug output (`print`, `console.log`), or TODOs without a
ticket reference.

**Doc comments only when the task is documentation.** Doc comments — `///` in Dart, `/** */`
in Java/Kotlin/JS/TS, docstrings in Python, and the like — are written only when the task
explicitly asks to document the code. Otherwise don't add them to new code, and don't extend
existing ones. When an existing doc comment on code you change becomes false, fix that
statement and nothing more. A non-obvious "why" that can't wait for documentation goes into
an ordinary comment next to the line it explains.

*Why:* the code already says what; only a comment can say why. Leftovers rot. A doc comment
written along the way mostly retells the name and the body, and goes stale with them.

## G11. Never swallow errors

Every caught error is either handled (recovered from, shown to the user, or deliberately
ignored with a comment saying why) or rethrown. An empty `catch` is not allowed.

*Why:* a swallowed error turns a crash you can debug into a wrong state you can't.

## G12. Reuse before writing

Before writing a helper, search the project for an existing one that does the same job.
Extend it if it nearly fits rather than writing a parallel version.

*Why:* two helpers for one job drift apart and both get bugs.

## G13. Change only what the task needs

Stay inside the task's scope. No drive-by refactoring, renaming, or reformatting of unrelated
code. If something nearby clearly needs fixing, mention it in the report instead. Restyling a
place the user chose to bring to our style (see the top of this file) is part of the task,
not a drive-by.

*Why:* a focused diff is reviewable; a sprawling one hides the real change.

## G14. Tests for new logic

New logic gets tests if the project has a test setup. Follow the project's existing test
style and location. If no test infrastructure exists, say so in the report rather than
creating one.

*Why:* untested logic is logic someone will break without noticing.
