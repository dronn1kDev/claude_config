# Templates by note type

Section skeletons. Section names are Russian samples; in a note in another language,
translate them, keeping the structure.
Drop a section that would be empty — never pad it. Frontmatter per
[conventions.md](conventions.md), with `type` set to the template's name.

## feature — how a product feature works

```
# <Feature as the user knows it>
<1–3 lines: what it lets the user do>

## Зачем
## Как это выглядит для пользователя
<flow from the user's side; Mermaid for a multi-step flow>
## Как устроено
<components, data flow, links to code — file paths, not code dumps>
## Состояния и ошибки
<table: state / when / what the user sees>
## Ограничения
## Связанное
```

## decision — an architecture or product decision (ADR)

```
# <Decision as a statement: «Храним токены в Keychain»>
<1–2 lines: what was decided>

## Контекст
<the problem and the forces at play>
## Решение
## Рассмотренные варианты
<table: option / pros / cons / why not>
## Последствия
<what gets easier, what gets harder, what to watch>
```

`status`: `active` while in force, `outdated` when replaced — with a link to the replacement.

## howto — instructions to get a task done

```
# <Как сделать X>
<1 line: the result you'll have at the end>

## Что нужно заранее
## Шаги
1. …   ← one action per step; commands in code blocks
## Как проверить
## Если не получилось
<symptom → cause → fix>
```

## reference — facts to look up

```
# <Topic>
<1–2 lines: what's here and when to look>

## <Main table or list of facts>
## Детали
## Источники
```

## research — results of an analysis

Same format as the `analyze` skill produces (Коротко / Где пути сходятся / Где расходятся /
По путям / Открытые вопросы / Источники). Keep the confidence and fact/inference labels.

## meeting — notes from a meeting or call

```
# YYYY-MM-DD <Topic>
**Участники:** …

## Решения
## Задачи
- [ ] <кто> — <что> — <к какому сроку>
## Обсуждали
## Открытые вопросы
```

Decisions and tasks come first — that's what people come back for.

## guide — how to get good at something (games, life hacks, hobbies)

```
# <What the guide achieves: «Elden Ring — билд на кровотечение»>
<1–3 lines: what you get and for whom>

> [!info] Актуально для: <game patch / app version / date checked>

## Что понадобится
## Пошагово
## Советы
> [!tip] …
## Частые ошибки
> [!warning] …
## Источники
```

Guides go stale fastest: always fill `version` or the «Актуально для» line, and `source`.

## note — anything that fits no other type

```
# <Title>
<1–3 lines: the point>

## <Sections as the content needs>
## Связанное
```
