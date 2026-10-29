# Ballgame

> Public source preview: see [PUBLICATION.md](PUBLICATION.md) for actual checks, known failures and runtime limits.

## О проекте

`Ballgame` — небольшая аркада на `pygame`, построенная вокруг запуска шаров из центральной зоны и защиты арены от врагов. Во время игры по внешнему кругу появляются враги и ворота, а игрок ограниченным числом запусков пытается удерживать контроль над полем и набирать очки.

## Что реализовано

- центральная игровая арена с внутренним и внешним радиусом;
- запуск шаров по клику мышью;
- появление обычных врагов и редких боссов;
- появление ворот как отдельного игрового события;
- счётчик уничтоженных целей, оставшихся запусков и короткая игровая консоль.

## Стек и структура

- Python
- `pygame`
- основные файлы: `main.py`, `ball.py`, `enemy.py`, `gate.py`, `settings.py`

## Запуск

```bash
python main.py
```

Если зависимости ещё не установлены, обычно достаточно установить `pygame`.

## Статус

`WIP`. Проект выглядит как самостоятельный игровой прототип с уже собранным основным циклом и набором базовых механик.


## Public source status — 2026-10-29

See [PUBLICATION.md](PUBLICATION.md) for the current verification scope, prototype limitations and runtime boundaries. Earlier audit checklists describe historical work.
