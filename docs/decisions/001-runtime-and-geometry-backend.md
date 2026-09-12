# ADR 001: Python 3.12 и Open3D 0.19 как baseline geometry backend

## Контекст

На рабочей станции установлен Python 3.14, но базовый stack тестового проекта требует воспроизводимый 3D backend. Нужны NumPy, Open3D, тестовый runner, linter и type checker.

## Варианты

1. Использовать системный Python 3.14 и development wheel Open3D.
2. Использовать Python 3.12 и стабильный Open3D 0.19.0.
3. Отказаться от Open3D и сразу написать собственный 3D backend.

## Решение

Выбран Python 3.12 в изолированном `uv`-окружении и Open3D 0.19.0. Это минимальная стабильная база для point cloud, визуализации, hull и baseline OBB; критический MVBB-method остаётся за адаптером и проходит независимые тесты до использования в pipeline.

## Обоснование и источники

- **Подтверждённый факт:** релиз Open3D 0.19.0 публикует wheel `cp312-win_amd64` и заявляет поддержку Python 3.12: [Open3D release 0.19](https://github.com/isl-org/Open3D/releases).
- **Подтверждённый факт:** Python 3.14 на Windows не поддерживается стабильным Open3D 0.19.0: [Open3D discussion](https://github.com/isl-org/Open3D/discussions/7456).
- **Подтверждённый результат P1:** в созданной среде импортируются NumPy и Open3D 0.19.0; pytest, Ruff и mypy доступны. OpenCV, Pydantic и ReportLab исключены как неиспользуемые прямые зависимости рабочего CV-пайплайна.
- **Подтверждённый результат P1:** в установленном Open3D 0.19.0 `open3d.t.geometry.OrientedBoundingBox` содержит `create_from_points`, но `MethodOBBCreate` отсутствует. Следовательно, `MINIMAL_JYLANKI` нельзя использовать как API pinned runtime.

## Последствия

- Runtime проекта закреплён на `>=3.12,<3.13`.
- Нельзя использовать API из документации Open3D `latest`, пока его нет в закреплённой версии.
- Production pipeline не зависит напрямую от Open3D MVBB API. P3 создаёт отдельный adapter, выбирает альтернативный backend либо фиксирует собственный алгоритм новым ADR после независимых тестов.
