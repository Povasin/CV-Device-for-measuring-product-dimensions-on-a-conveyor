# Ozon Conveyor Dimensioning

Воспроизводимый офлайн-прототип системы измерения габаритов товара на движущемся
конвейере для варианта 1 тестового задания Ozon Tech / Университета Иннополис 2026.

Проект принимает калиброванные 3D-точки или записанные лазерные профили, приводит
их к системе координат конвейера, компенсирует движение по энкодеру, проверяет
полноту наблюдения и возвращает длину, ширину и высоту товара в миллиметрах.

> **Статус:** программное геометрическое ядро, синтетический benchmark и WMS
> outbox реализованы и покрыты тестами. Точность физического комплекса, работа с
> реальными профиломерами и exact minimum-volume bounding box требуют стендовой
> валидации и не заявляются как завершённые.

## Что реализовано

- строгий контракт `LaserProfile` для профиля, энкодера, времени и калибровки;
- объединение профилей одного товара в `ProfileBundle`;
- rigid sensor-to-conveyor transforms и компенсация движения ленты;
- DBSCAN-сегментация, удаление одиночного шума и отклонение нескольких товаров;
- quality gates для пропусков профилей, неполного ракурса и касания ROI;
- приближённый oriented bounding box через Open3D;
- проверка рабочего диапазона `10×10×10…400×300×300 мм`;
- явные статусы `valid`, `rejected`, `error`;
- SQLite outbox с идемпотентностью и повторной доставкой в WMS;
- unit-, integration- и synthetic regression-тесты;
- готовый инженерный PDF-отчёт для отправки.

## Пайплайн

```text
лазерные профили / NPZ replay
            ↓
ProfileBundle + CaptureEvidence
            ↓
sensor-to-conveyor transform
            ↓
компенсация движения по энкодеру
            ↓
DBSCAN: один товар, шум, неоднозначные события
            ↓
ObjectObservation
            ↓
Open3D approximate oriented bounding box
            ↓
MeasurementResult + operating-range validation
            ↓
SQLite outbox → transport adapter → WMS
```

Для быстрого эксперимента доступен сокращённый путь
`point cloud → удаление плоскости ленты → OBB → размеры`. Он используется demo и
синтетическим benchmark. Полный профилометрический путь проверяется интеграционным
тестом `ProfileBundle → registration → segmentation → MeasurementResult`.

## Быстрый запуск

Нужен **Python 3.12**. Самый короткий воспроизводимый способ — через
[uv](https://docs.astral.sh/uv/):

```powershell
py -3.12 -m pip install uv
uv sync --all-groups --frozen
uv run python -m scripts.run_demo
```

Ожидаемый результат:

```text
dimensions_mm=[50.0, 100.0, 200.0]
point_count=8
algorithm=open3d-face-aligned-approx
```

Синтетический benchmark по минимальному, среднему и максимальному размерам:

```powershell
uv run python -m scripts.run_benchmark
```

## Установка в обычное виртуальное окружение

Если `uv` использовать нельзя, зависимости можно установить через `pip`:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e .
python -m pip install "pytest>=8.3,<9" "ruff>=0.9,<1" "mypy>=1.15,<2" "pre-commit>=4,<5"
```

Основные библиотеки:

| Библиотека | Назначение |
|---|---|
| `numpy` | массивы, геометрия и валидация численных данных |
| `open3d==0.19.0` | DBSCAN и приближённый oriented bounding box |
| `pytest` | unit- и integration-тесты |
| `ruff` | lint и проверка форматирования |
| `mypy` | строгая статическая типизация пакета |
| `pre-commit` | локальный запуск quality gates перед коммитом |

Полный перечень версий находится в [`pyproject.toml`](pyproject.toml), а
воспроизводимый lock-файл — в [`uv.lock`](uv.lock).

## Проверка проекта

Из корня репозитория:

```powershell
uv run pytest -q
uv run ruff check src tests scripts
uv run ruff format --check src tests scripts
uv run mypy src scripts
uv lock --check
uv run python -m scripts.run_demo
uv run python -m scripts.run_benchmark
```

Опционально можно установить git hooks:

```powershell
uv run pre-commit install
uv run pre-commit run --all-files
```

## Структура репозитория

```text
src/ozon_dim/            основной Python-пакет
  acquisition/           профили, offline replay, регистрация по энкодеру
  preprocessing/         foreground и DBSCAN-сегментация
  geometry/              rigid transforms и oriented bounding box
  measurement/           контракты наблюдения, диапазон и допуск
  api/                   WMS payload, SQLite outbox и dispatcher
scripts/                 исполняемые demo и benchmark
tests/unit/              тесты изолированной логики и edge cases
tests/integration/       сквозные проверки пайплайна и отчёта
docs/                    требования, архитектура, hardware и ограничения
output/pdf/              канонический PDF-отчёт для отправки
```

Ключевые документы:

- [`docs/test-assignment.md`](docs/test-assignment.md) — исходное тестовое задание;
- [`docs/requirements.md`](docs/requirements.md) — требования и трассируемость;
- [`docs/architecture.md`](docs/architecture.md) — контракты и поток данных;
- [`docs/hardware.md`](docs/hardware.md) — выбор оборудования и стендовая программа;
- [`docs/verification.md`](docs/verification.md) — автоматические и физические проверки;
- [`docs/final_audit.md`](docs/final_audit.md) — честный статус готовности.

Готовый отчёт: [`output/pdf/ozon_variant_1_report.pdf`](output/pdf/ozon_variant_1_report.pdf).

## Ограничения

- Open3D backend имеет идентификатор `open3d-face-aligned-approx`: он не считается
  доказанным глобально точным MVBB.
- Synthetic benchmark проверяет детерминированную программную механику, но не
  погрешность сенсора, калибровки, материала товара или движения конвейера.
- Live-адаптер LMI SDK и фактический WMS transport не реализованы: их контракты
  требуют доступа к оборудованию и согласованной внешней API-схемы.
- Прозрачные, зеркальные, чёрные и деформируемые товары должны проверяться на
  физическом стенде; неподтверждённые характеристики не исключаются из метрик.

Формула допуска задания применяется отдельно к каждой стороне:

```text
T(d) = max(0.05 × d, 5 мм)
```

Подробная программа приёмки и граница доказательств описаны в
[`docs/verification.md`](docs/verification.md).
