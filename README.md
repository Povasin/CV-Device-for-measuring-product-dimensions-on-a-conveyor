# Ozon Conveyor Dimensioning

Инженерный проект для варианта 1 тестового задания Ozon Tech / Университет Иннополис 2026: определение габаритов товара на движущемся конвейере.

Полный план, требования, допущения и текущая задача находятся в [`implementation_plan.md`](implementation_plan.md), [`docs/requirements.md`](docs/requirements.md), [`docs/assumptions.md`](docs/assumptions.md) и [`TASK.md`](TASK.md).

Реализация находится в ранней фазе: точность реального сенсора пока не подтверждена экспериментом.
# Conveyor Dimensioning System - вариант 1

Проект реализует проверяемый офлайн baseline для измерения габаритов товара на
конвейере из калиброванного облака точек. Объект отделяется от плоскости ленты,
после чего Open3D строит ориентированный bounding box. Этот backend **приближённый**:
он не заявляется как глобально точный minimum-volume bounding box.

Для нескольких сенсоров `ozon_dim.fusion.fuse_point_clouds` применяет переданные
жёсткие преобразования и объединяет уже синхронизированные облака. Оценка самих
преобразований и синхронизация требуют аппаратного стенда.

## Быстрый запуск

```powershell
uv sync --all-groups
uv run pytest -q
uv run python -m scripts.run_demo
uv run python -m scripts.run_benchmark
uv run python scripts/build_report.py
```

Демо выдаёт `[50.0, 100.0, 200.0]` мм для синтетического товара
`200 x 100 x 50` мм. Отчёт создаётся в
`output/pdf/ozon_variant_1_report.pdf`.

`run_benchmark` проверяет идеальные синтетические случаи, включая границы
диапазона. Он не подтверждает точность физических измерений; границы этой
проверки описаны в `docs/verification.md`.

## Проверки

```powershell
uv run ruff check src tests scripts
uv run mypy src scripts
uv lock --check
```

Требования, допущения и ограничения стендовой валидации приведены в
`docs/requirements.md`, `docs/assumptions.md` и `implementation_plan.md`.
