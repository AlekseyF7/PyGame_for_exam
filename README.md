# PyGame_for_exam — Doodle Jump

Игра для экзамена по программированию за 2 семестр.
2D вертикальный платформер-«прыгун» на PyGame с архитектурой MVC.

## Требования

- Python 3.11+
- pygame (см. `requirements.txt`)

## Установка и запуск

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m src.main
```

## Управление

- `←` / `→` или `A` / `D` — движение влево/вправо (есть переход через край экрана)
- Прыжок автоматический при приземлении на платформу
- `Esc` — пауза / выход в меню
- `Enter` — играть / заново

## Тесты

```bash
python -m unittest discover -s tests
```

## Архитектура (MVC)

- `src/models/` — чистая логика без pygame (физика, генерация уровня, состояние, счёт)
- `src/views/` — отрисовка pygame, загрузка ассетов (`AssetManager`)
- `src/controllers/` — игровой цикл, ввод, сцены
- `src/services/` — сохранение рекордов/настроек (JSON)

Подробности и анализ под критерии экзамена: `docs/PROJECT_PLAN.md`.
