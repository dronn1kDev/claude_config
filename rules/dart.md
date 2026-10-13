# Dart / Flutter rules

Apply on top of [general.md](general.md) to all Dart code, including Flutter.
Same priority: these beat project conventions, but the project's analyzer (`analysis_options.yaml`)
and CI win on conflict — follow them and report the conflict. Where the existing code a change
goes into is styled differently, the user picks the style per place, as general.md describes.

## D1. Primary constructors for new classes (Dart ≥ 3.13)

New classes declare their fields through a primary constructor when the project's language
version allows it. Check the lower bound of `environment: sdk:` in `pubspec.yaml` — it must
be `>= 3.13`. Below that, write classes the classic way.

Use a semicolon instead of an empty class body, so simple classes stay on one line.
Don't use a primary constructor where it doesn't fit: classes that need `late` fields,
mixin classes with constructor logic, complex multi-step initialization.
Existing classes are not converted unless the task asks for it (G13).

Reference: https://dart.dev/language/primary-constructors — check it when unsure of the syntax.

*Why:* fields and constructor in one place; no repetition of every field name three times.

## D2. `final` and `const` by default

Fields and local variables are `final` unless they must change. Constructors and widget
instances are `const` wherever possible.

*Why:* immutability removes a whole class of bugs; `const` widgets skip rebuilds.

## D3. Widgets as classes, not `_buildX()` methods

Pieces of UI are extracted into separate widget classes, not into methods that return widgets.
Extract a piece when it is reused, rebuilds on its own state, or has a meaning worth naming —
and always when `build` would exceed the 200-line layout limit of G1.

*Why:* widget classes can be `const`, rebuild independently, and show up in DevTools.

## D4. No `!` or `dynamic` without a reason

Avoid the null-assertion operator `!` — use null checks, early returns, or pattern matching.
Avoid `dynamic` — use precise types or `Object?`. If either is truly needed, comment why.

*Why:* `!` turns a type error into a runtime crash; `dynamic` switches off the type checker.

## D5. States via sealed classes and switch expressions

Model a closed set of states or results as a `sealed` class hierarchy and handle it with an
exhaustive `switch` expression, not with flag combinations or `if`/`else` chains.

*Why:* the compiler then tells you every place that must handle a new state.

## D6. Check `mounted` after `await`

In a `State` or with a `BuildContext`, after every `await` check `mounted` (or
`context.mounted`) before using `context` or calling `setState`.

*Why:* the widget may be gone by the time the future completes.

## D7. Dispose what you create

Controllers, focus nodes, stream subscriptions, timers, and animation controllers created by
a widget or object are released in its `dispose`/`close`.

*Why:* leaks and "setState after dispose" errors.

## D8. Format, analyze, test

After changes, run on the touched code: `dart format`, `flutter analyze` (or `dart analyze`
for pure Dart), and the relevant tests. If the project uses FVM (`.fvmrc` or `.fvm/` present),
prefix the commands with `fvm`. Fix what you introduced; report pre-existing issues instead
of fixing them (G13).

*Why:* the rules above are worthless if the code doesn't pass the project's own checks.
