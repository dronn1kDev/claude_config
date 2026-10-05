# Claude config

Этот vault подключён к Claude Code через симлинки из `~/.claude`.

- `skills/<имя>/SKILL.md` — скиллы (фронтматтер: `name`, `description`)
- `agents/<имя>.md` — сабагенты
- `commands/<имя>.md` — слэш-команды
- `hooks/` — скрипты хуков (не подключены; включаются в `~/.claude/settings.json`, он в vault не хранится)
- `research/` — сохранённые результаты аналитика (в .gitignore)
- `CLAUDE.md` — глобальные инструкции для всех проектов

Ссылки внутри скиллов делать относительными путями, а не [[wiki-links]].
