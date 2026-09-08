Ты выступаешь как Principal Computer Vision Engineer, Robotics/Perception Architect и Technical Lead.

Твоя задача: НЕ писать реализацию и НЕ начинать кодирование.

Тебе нужно разработать максимально сильный, подробный и реалистичный инженерный план реализации тестового задания Ozon Tech + Университет Иннополис 2026 по треку Computer Vision.

Исходное тестовое задание приложено отдельным файлом. Сначала полностью изучи его.

Ключевое правило:

НИКАКОГО КОДА, пока я явно не разрешу.
НЕ запускай реализацию самостоятельно.
НЕ создавай файлы проекта.
НЕ изменяй репозиторий.
НЕ устанавливай зависимости.
НЕ выполняй команды.
НЕ делай commit/push.
Твоя задача сейчас только анализ, архитектура и планирование.

---

# 1. Цель

Нужно создать не просто демо, а инженерно убедительное решение, которое сможет хорошо выглядеть перед специалистами Ozon Tech.

Проект должен демонстрировать:

- Computer Vision;
- работу с реальными сенсорами;
- понимание геометрии камеры;
- калибровку;
- 2D/3D обработку;
- работу с depth data / point cloud, если это оправдано;
- понимание погрешностей измерения;
- проектирование production-like pipeline;
- тестирование;
- benchmark;
- техническую документацию;
- грамотный выбор hardware;
- анализ ограничений;
- воспроизводимость;
- хороший GitHub-проект.

Главный критерий:

Каждое техническое решение должно быть обосновано.

Не использовать технологии только ради демонстрации сложности.

---

# 2. Сначала разберись в исходном задании

Полностью прочитай приложенное тестовое задание.

Извлеки отдельно:

## Explicit requirements

Все требования, которые прямо написаны в задании.

## Constraints

Все ограничения:

- размеры;
- скорости;
- диапазоны;
- расстояния;
- точность;
- hardware constraints;
- timing constraints;
- формат результата.

## Evaluation criteria

Что, судя по заданию, будет оцениваться.

## Optional requirements

Что является дополнительным плюсом, но не обязательно.

## Hidden engineering requirements

Что прямо не написано, но без этого решение не будет практически работать.

Не смешивай эти четыре категории.

---

# 3. Выбор варианта

В тестовом есть несколько CV-вариантов.

Сначала оцени ВСЕ варианты.

Для каждого варианта сделай оценку по шкале 1-10:

- инженерная сложность;
- сила проекта для CV-портфолио;
- возможность сделать качественное demo без реального промышленного оборудования;
- возможность использовать классический CV;
- необходимость нейросетей;
- сложность сбора данных;
- сложность hardware;
- риск не успеть;
- насколько хорошо проект может показать знания кандидата;
- насколько убедительно результат будет выглядеть для Ozon Tech.

Создай таблицу сравнения.

После этого выбери один наиболее сильный вариант.

Если ты считаешь, что вариант 1 "Устройство для замера габаритов товара на конвейере" является лучшим, объясни почему.

Но не принимай это как данность. Проверь выбор критически.

---

# 4. Архитектурные варианты

Для выбранного задания предложи минимум 3 реалистичных архитектуры.

Например, если выбран вариант определения габаритов:

архитектура может использовать:

- RGB camera + classical geometry;
- RGB-D camera;
- stereo cameras;
- ToF;
- LiDAR;
- structured light;
- комбинацию сенсоров.

Но не ограничивайся этими вариантами.

Для каждой архитектуры укажи:

- используемые сенсоры;
- количество сенсоров;
- их физическое расположение;
- рабочую дистанцию;
- field of view;
- ожидаемый FPS;
- resolution;
- depth accuracy;
- synchronization requirements;
- освещение;
- вычислитель;
- software stack;
- preprocessing;
- calibration;
- detection;
- segmentation;
- reconstruction;
- measurement;
- filtering;
- postprocessing;
- output;
- latency.

---

# 5. Сравнение архитектур

Сделай decision matrix.

Критерии:

- достижимость требуемой точности;
- robustness;
- latency;
- цена;
- сложность hardware;
- сложность calibration;
- чувствительность к освещению;
- чувствительность к цвету/материалу объекта;
- работа с чёрными поверхностями;
- reflective surfaces;
- прозрачными объектами;
- неправильной формой;
- motion blur;
- occlusion;
- vibrations;
- maintenance;
- scalability;
- production suitability;
- сложность реализации demo.

Поставь каждой архитектуре оценки.

После этого выбери одну.

Обязательно объясни:

Почему выбранная архитектура лучше альтернатив именно под это тестовое.

---

# 6. Hardware research plan

Не выдумывай характеристики оборудования.

Для каждого hardware-компонента укажи:

- какие характеристики нужно проверить;
- почему они важны;
- какие реальные модели стоит исследовать;
- какие альтернативы сравнить.

Например:

Camera / RGB-D:
- resolution;
- depth resolution;
- FPS;
- working range;
- depth error;
- global/rolling shutter;
- interface;
- synchronization;
- FOV;
- minimum depth distance.

Compute:
- CPU;
- GPU;
- RAM;
- power;
- interfaces;
- operating environment.

Lighting:
- тип;
- расположение;
- зачем оно нужно.

После этого предложи shortlist реальных устройств, но явно помечай:

- подтверждённый факт;
- требующее проверки;
- предположение.

Если информация требует актуальной проверки по datasheet производителя, так и напиши.

---

# 7. Физическая схема

Опиши механическую конфигурацию системы.

Нужно определить:

- где находится камера;
- высота;
- угол;
- количество камер;
- расстояние до конвейера;
- рабочая область;
- trigger zone;
- measurement zone;
- расстояние от measurement zone до следующего участка конвейера;
- освещение;
- возможные защитные корпуса;
- как исключается попадание соседнего объекта.

Создай ASCII-схему сверху и сбоку.

Пример формата:

SIDE VIEW

camera
   |
   v
----------------
    object
================ conveyor

Но сделай полноценную схему конкретно для выбранной архитектуры.

---

# 8. Полный CV pipeline

Опиши pipeline от физического объекта до результата.

В формате:

Sensor
↓
Frame acquisition
↓
Synchronization
↓
Calibration
↓
Preprocessing
↓
ROI detection
↓
Object segmentation
↓
Depth filtering
↓
Coordinate transformation
↓
Point cloud
↓
Plane removal
↓
Object point cloud
↓
Outlier removal
↓
Bounding box
↓
Metric dimensions
↓
Validation
↓
WMS / conveyor API

Для каждого этапа опиши:

- вход;
- выход;
- алгоритм;
- возможные библиотеки;
- computational complexity;
- failure modes.

---

# 9. Bounding box / measurement

Особенно подробно разберись с определением размеров объекта.

Если предметы произвольной формы, нужно определить минимальный прямоугольный параллелепипед, в который можно вписать товар.

Рассмотри:

- Axis-Aligned Bounding Box;
- Oriented Bounding Box;
- PCA;
- rotating calipers в 2D;
- convex hull;
- minimum-volume bounding box;
- Open3D OBB;
- другие подходы.

Объясни:

какой метод правильнее использовать именно здесь и почему.

Обязательно разберись с тем, что объект может лежать на конвейере под произвольным углом.

---

# 10. Calibration

Разработай отдельный calibration pipeline.

Опиши:

## Intrinsic calibration

- camera matrix;
- focal length;
- principal point;
- distortion coefficients.

## Extrinsic calibration

- camera → conveyor;
- world coordinate system.

## Depth calibration

Если используется depth camera.

## Conveyor plane calibration

Как определить плоскость ленты.

## Scale verification

Как проверять реальные миллиметры.

## Recalibration

Когда нужна повторная калибровка.

---

# 11. Error budget

Это один из самых важных разделов.

Нужно выполнить требование по точности из тестового.

Построй error budget.

Источники ошибок:

- depth sensor noise;
- calibration;
- lens distortion;
- pixel quantization;
- object segmentation;
- motion blur;
- conveyor vibration;
- reflective surfaces;
- occlusion;
- plane estimation;
- bounding-box algorithm;
- synchronization;
- temperature drift.

Для каждого:

- причина;
- примерная величина;
- как влияет на L/W/H;
- как уменьшить;
- можно ли компенсировать.

После этого ответь:

Реалистично ли достичь требуемой точности?

Если да:
за счёт чего.

Если нет:
какой hardware/архитектуру нужно изменить.

---

# 12. Latency budget

Конвейер движется.

Поэтому разработай timing model.

Опиши:

- скорость движения;
- время нахождения объекта в ROI;
- sensor FPS;
- acquisition time;
- preprocessing;
- segmentation;
- point cloud processing;
- measurement;
- API output.

Создай latency budget.

Например:

capture      X ms
preprocess   X ms
segmentation X ms
point cloud  X ms
measurement  X ms
API          X ms

TOTAL        X ms

Определи максимально допустимую latency.

---

# 13. Classical CV vs neural network

Очень критично оцени, нужна ли нейросеть.

Не используй DL просто потому, что это CV-проект.

Сравни:

Classical CV

vs

Neural network

Для задач:

- object detection;
- segmentation;
- depth;
- geometry.

Если нейросеть не нужна, прямо скажи это и объясни, почему classical CV здесь лучше.

Если нужна:

укажи:

- architecture;
- почему она;
- input/output;
- dataset size;
- annotation;
- augmentation;
- training;
- validation;
- metrics;
- inference hardware;
- latency.

---

# 14. Dataset

Даже если нейросети нет, нужен validation dataset.

Продумай набор тестовых объектов.

Категории:

- маленький;
- большой;
- длинный;
- плоский;
- высокий;
- неправильной формы;
- цилиндрический;
- soft package;
- reflective;
- black;
- white;
- patterned;
- partially occluded;
- повернутый на разные углы.

Для каждого укажи:

- ground truth;
- способ измерения;
- количество примеров;
- тестовые сценарии.

---

# 15. Metrics

Разработай полноценную систему метрик.

Не ограничивайся average error.

Предложи:

- MAE mm;
- MAPE;
- RMSE;
- P50;
- P95;
- P99;
- percentage within tolerance;
- latency;
- throughput;
- failure rate;
- missed object rate.

Для L/W/H отдельно.

Главная метрика должна напрямую отражать условие тестового задания.

---

# 16. Failure cases

Создай отдельную таблицу.

Колонки:

Scenario
Cause
Expected behavior
Detection
Mitigation
Severity

Обязательно включить:

- black object;
- transparent object;
- shiny object;
- very small object;
- very large object;
- two objects too close;
- partial occlusion;
- incomplete point cloud;
- motion blur;
- bad calibration;
- camera shifted;
- sensor disconnect;
- WMS unavailable.

---

# 17. Software architecture

Разработай модульную архитектуру Python-проекта.

Не пиши код.

Предложи структуру:

src/
    acquisition/
    calibration/
    preprocessing/
    segmentation/
    geometry/
    measurement/
    validation/
    api/

tests/

configs/

demo/

docs/

Опиши ответственность каждого модуля.

Обязательно:

- separation of concerns;
- dependency direction;
- configuration management;
- logging;
- error handling.

---

# 18. Dependency selection

Для каждой библиотеки объясни:

почему именно она.

Рассмотри:

- OpenCV;
- NumPy;
- SciPy;
- Open3D;
- scikit-image;
- Pydantic;
- FastAPI;
- pytest;
- Ruff;
- mypy;
- Matplotlib.

Не подключай библиотеку без необходимости.

---

# 19. Testing strategy

Разработай testing pyramid.

## Unit tests

Например:

- transforms;
- filtering;
- bounding boxes;
- dimensions;
- geometry.

## Synthetic tests

Генерируем point cloud известного размера.

Например коробка:

200 × 100 × 50 мм

Алгоритм должен вернуть размеры в заданной tolerance.

## Integration tests

sensor/frame
→ pipeline
→ dimensions.

## Regression tests

фиксированный набор данных.

## Hardware tests

если есть физический sensor.

Для каждого теста опиши acceptance criteria.

---

# 20. Synthetic demo

Так как промышленного оборудования может не быть, придумай максимально убедительный demo.

Варианты:

- записанный RGB-D dataset;
- synthetic point clouds;
- Blender simulation;
- Open3D visualization;
- prerecorded conveyor video;
- generated objects;
- live webcam simulation.

Выбери лучший вариант.

Demo должно показывать:

INPUT

→ PROCESSING

→ POINT CLOUD / SEGMENTATION

→ 3D BOUNDING BOX

→ L × W × H

План demo опиши отдельно.

---

# 21. Benchmark

Спроектируй benchmark.

Например:

1000 synthetic objects

разные:

- dimensions;
- orientation;
- noise;
- occlusion;
- missing depth;
- sensor noise.

Измерить:

accuracy
latency
failure rate.

Продумай, какие графики будут наиболее убедительными.

---

# 22. Repository

Продумай финальный GitHub repository.

README должен содержать:

- problem;
- architecture;
- hardware;
- pipeline;
- demo;
- installation;
- usage;
- tests;
- benchmark;
- limitations.

Дополнительно:

docs/
architecture diagrams
results
images
demo GIF/video

Создай рекомендуемую структуру repository.

---

# 23. Отчёт

Отдельно спроектируй структуру финального PDF.

Пример:

1. Executive summary
2. Problem
3. Requirements
4. Constraints
5. Architecture
6. Hardware
7. Sensor placement
8. Calibration
9. CV pipeline
10. Measurement algorithm
11. Compute
12. Accuracy
13. Error budget
14. Testing
15. Metrics
16. Scaling
17. Failure modes
18. Limitations
19. Conclusion

Для каждого раздела напиши:

что именно туда должно войти.

---

# 24. Implementation roadmap

Теперь разбей реализацию на этапы.

Например:

Phase 0
Problem analysis

Phase 1
Research

Phase 2
Architecture

Phase 3
Synthetic geometry prototype

Phase 4
Core pipeline

Phase 5
Dataset

Phase 6
Validation

Phase 7
Demo

Phase 8
Benchmark

Phase 9
Report

Phase 10
Final audit

Но сам определи оптимальные этапы.

Для каждого этапа:

- цель;
- задачи;
- input;
- output;
- dependencies;
- acceptance criteria;
- risks;
- что может быть делегировано дешёвой coding-модели;
- что обязательно должен проверить сильный model/reviewer.

---

# 25. Task decomposition для AI agents

Это особенно важно.

Проект будет реализовываться с помощью Codex в VS Code.

Нужно разделить работу между моделями.

## Strong reasoning model

Ей отдаём:

- architecture;
- algorithm choice;
- hardware;
- calibration;
- mathematical reasoning;
- error analysis;
- reviews;
- debugging сложных ошибок;
- final audit.

## Cheaper coding model

Ей отдаём:

- boilerplate;
- простые функции;
- unit tests;
- refactoring;
- documentation formatting;
- CLI;
- configs;
- repetitive code.

Создай таблицу:

Task
Model level
Reason
Input context required
Acceptance criteria

Главная задача:
минимизировать расход токенов, но не снижать инженерное качество.

---

# 26. Context strategy

Разработай стратегию, чтобы Codex не сжигал огромный контекст.

Опиши:

- что хранить в AGENTS.md;
- что хранить в TASK.md;
- что хранить в docs;
- что помещать в skills;
- когда запускать новый conversation/thread;
- какие файлы давать модели;
- какие не давать;
- как использовать git diff вместо чтения всего repository;
- как делать summary после каждого этапа;
- как передавать задачи дешёвой модели.

---

# 27. Codex workflow

Разработай конкретный workflow для VS Code + Codex.

Например:

User
↓
Strong model architecture
↓
TASK.md
↓
Codex implementation
↓
pytest
↓
ruff
↓
git diff
↓
strong model review
↓
fix
↓
commit

Но сделай более подробную версию.

---

# 28. MCP

Определи, какие MCP реально нужны.

Не советуй подключать всё подряд.

Рассмотри:

- GitHub MCP;
- filesystem;
- documentation;
- web/research;
- другие MCP только если они реально дают преимущество.

Для каждого:

- зачем;
- какие tools нужны;
- какие permissions дать;
- потенциальный риск;
- влияние на контекст.

Отдельно укажи MCP, которые подключать НЕ нужно.

---

# 29. Skills

Определи набор skills для Codex.

Например:

- CV engineering;
- hardware research;
- technical research;
- testing;
- report;
- code review.

Для каждого:

- назначение;
- когда активировать;
- какую информацию туда положить;
- чего там быть не должно.

Не создавай skills ради количества.

---

# 30. Hooks / automatic quality gates

Разработай hooks.

После изменения Python:

ruff
→ tests
→ type checks при необходимости.

Перед commit:

tests
lint
git diff --check
secret scanning.

Предложи минимальный, но эффективный набор.

---

# 31. Git strategy

Проект небольшой, поэтому не усложняй Git workflow.

Предложи:

- ветки;
- commit strategy;
- naming;
- когда делать PR;
- когда нужен reviewer.

Не превращай тестовое в корпоративный GitFlow.

---

# 32. Final audit

В конце проекта должен запускаться аудит.

Создай checklist минимум из 30 пунктов.

Категории:

- requirements;
- CV;
- geometry;
- hardware;
- error handling;
- metrics;
- tests;
- performance;
- docs;
- GitHub;
- PDF;
- reproducibility.

---

# 33. Red Team review

После составления плана сам атакуй свой план.

Представь, что ты Senior CV Engineer из Ozon Tech и хочешь отклонить кандидата.

Ответь:

- где решение выглядит слишком академично;
- где слишком сложно;
- где нет доказательств;
- где hardware unrealistic;
- где accuracy не подтверждена;
- где demo ничего не доказывает;
- где есть buzzword engineering;
- где можно упростить;
- где нужно углубить.

После критики внеси улучшения в план.

---

# 34. Формат финального ответа

Ответ должен иметь следующую структуру:

1. Executive summary
2. Разбор исходного задания
3. Сравнение трёх CV-вариантов
4. Рекомендуемый вариант
5. Requirements
6. Constraints
7. Proposed architecture
8. Architecture alternatives
9. Decision matrix
10. Hardware
11. Sensor placement
12. Calibration
13. CV pipeline
14. Measurement algorithm
15. Classical CV vs DL
16. Error budget
17. Latency budget
18. Dataset
19. Metrics
20. Failure cases
21. Software architecture
22. Repository structure
23. Testing strategy
24. Demo
25. Benchmark
26. PDF report structure
27. Development roadmap
28. AI-agent task decomposition
29. Context/token strategy
30. Codex workflow
31. MCP
32. Skills
33. Hooks
34. Git workflow
35. Final audit checklist
36. Red Team critique
37. Improved final plan

Используй:

- таблицы;
- схемы;
- decision matrices;
- checklist;
- dependency graph;
- Mermaid, где это полезно.

---

# 35. Жёсткие ограничения

НЕ ПИШИ КОД.

НЕ НАЧИНАЙ РЕАЛИЗАЦИЮ.

НЕ ИЗМЕНЯЙ ФАЙЛЫ.

НЕ УСТАНАВЛИВАЙ НИЧЕГО.

НЕ ДЕЛАЙ GIT OPERATIONS.

НЕ ВЫДУМЫВАЙ РЕЗУЛЬТАТЫ ЭКСПЕРИМЕНТОВ.

НЕ ВЫДУМЫВАЙ ХАРАКТЕРИСТИКИ ОБОРУДОВАНИЯ.

НЕ УТВЕРЖДАЙ, ЧТО ТРЕБУЕМАЯ ТОЧНОСТЬ ДОСТИГНУТА, ПОКА ЭТО НЕ ПОДТВЕРЖДЕНО.

НЕ ИСПОЛЬЗУЙ НЕЙРОСЕТЬ, ЕСЛИ ОНА НЕ НУЖНА.

НЕ ДОБАВЛЯЙ ТЕХНОЛОГИЮ ТОЛЬКО ПОТОМУ, ЧТО ОНА ВЫГЛЯДИТ СЛОЖНО.

Если не хватает информации:
зафиксируй assumption и объясни, как его проверить.

Главная цель:

сделать план, по которому другой AI-агент сможет реализовать проект пошагово без необходимости каждый раз заново принимать архитектурные решения.

План должен быть настолько конкретным, чтобы после его утверждения реализация в основном состояла из выполнения чётко определённых задач и проверки acceptance criteria.