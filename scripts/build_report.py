"""Build the self-contained Variant 1 engineering report."""

from __future__ import annotations

import os
from pathlib import Path

from reportlab.graphics.shapes import Drawing, Line, Polygon, Rect, String
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen.canvas import Canvas
from reportlab.platypus import (
    LongTable,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "output" / "pdf" / "ozon_variant_1_report.pdf"
PAGE_WIDTH, PAGE_HEIGHT = A4
BLUE = colors.HexColor("#005B99")
TEAL = colors.HexColor("#007F7B")
LIGHT_BLUE = colors.HexColor("#EAF3F8")
LIGHT_GRAY = colors.HexColor("#F3F6F8")
DARK = colors.HexColor("#1E2B36")
MUTED = colors.HexColor("#52616B")
LINE = colors.HexColor("#B8C4CE")


def resolve_font(environment_name: str, candidates: list[Path]) -> Path:
    """Find a Unicode TrueType font without binding the report to one Windows path."""
    configured = os.environ.get(environment_name)
    paths = [Path(configured)] if configured else []
    paths.extend(candidates)
    for path in paths:
        if path.is_file():
            return path
    searched = ", ".join(str(path) for path in paths)
    raise FileNotFoundError(f"No report font found. Set {environment_name}. Searched: {searched}")


def register_fonts() -> tuple[str, str]:
    regular = resolve_font(
        "OZON_REPORT_FONT",
        [
            Path("C:/Windows/Fonts/arial.ttf"),
            Path("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"),
            Path("/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf"),
        ],
    )
    bold = resolve_font(
        "OZON_REPORT_FONT_BOLD",
        [
            Path("C:/Windows/Fonts/arialbd.ttf"),
            Path("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"),
            Path("/usr/share/fonts/truetype/liberation2/LiberationSans-Bold.ttf"),
        ],
    )
    pdfmetrics.registerFont(TTFont("ReportRegular", str(regular)))
    pdfmetrics.registerFont(TTFont("ReportBold", str(bold)))
    return "ReportRegular", "ReportBold"


def make_styles(regular: str, bold: str) -> dict[str, ParagraphStyle]:
    base = getSampleStyleSheet()
    return {
        "title": ParagraphStyle(
            "ReportTitle",
            parent=base["Title"],
            fontName=bold,
            fontSize=24,
            leading=29,
            textColor=DARK,
            spaceAfter=8,
        ),
        "subtitle": ParagraphStyle(
            "ReportSubtitle",
            parent=base["BodyText"],
            fontName=regular,
            fontSize=10.5,
            leading=15,
            textColor=MUTED,
            spaceAfter=10,
        ),
        "heading": ParagraphStyle(
            "ReportHeading",
            parent=base["Heading2"],
            fontName=bold,
            fontSize=14,
            leading=18,
            textColor=BLUE,
            spaceBefore=4,
            spaceAfter=7,
        ),
        "subheading": ParagraphStyle(
            "ReportSubheading",
            parent=base["Heading3"],
            fontName=bold,
            fontSize=11,
            leading=14,
            textColor=DARK,
            spaceBefore=4,
            spaceAfter=5,
        ),
        "body": ParagraphStyle(
            "ReportBody",
            parent=base["BodyText"],
            fontName=regular,
            fontSize=9.2,
            leading=13.2,
            textColor=DARK,
            spaceAfter=6,
        ),
        "small": ParagraphStyle(
            "ReportSmall",
            parent=base["BodyText"],
            fontName=regular,
            fontSize=7.5,
            leading=10,
            textColor=MUTED,
        ),
        "table": ParagraphStyle(
            "ReportTable",
            parent=base["BodyText"],
            fontName=regular,
            fontSize=7.4,
            leading=9.3,
            textColor=DARK,
        ),
        "table_head": ParagraphStyle(
            "ReportTableHead",
            parent=base["BodyText"],
            fontName=bold,
            fontSize=7.4,
            leading=9.3,
            textColor=colors.white,
        ),
        "callout": ParagraphStyle(
            "ReportCallout",
            parent=base["BodyText"],
            fontName=regular,
            fontSize=9,
            leading=13,
            textColor=DARK,
            leftIndent=6,
            rightIndent=6,
            spaceBefore=3,
            spaceAfter=3,
        ),
        "center": ParagraphStyle(
            "ReportCenter",
            parent=base["BodyText"],
            fontName=regular,
            fontSize=9.2,
            leading=13,
            alignment=TA_CENTER,
            textColor=DARK,
        ),
        "source": ParagraphStyle(
            "ReportSource",
            parent=base["BodyText"],
            fontName=regular,
            fontSize=7.2,
            leading=9.6,
            textColor=MUTED,
            alignment=TA_LEFT,
        ),
    }


def paragraph(text: str, style: ParagraphStyle) -> Paragraph:
    return Paragraph(text, style)


def table(
    rows: list[list[str]], widths_mm: list[float], styles: dict[str, ParagraphStyle]
) -> LongTable:
    converted: list[list[Paragraph]] = []
    for row_index, row in enumerate(rows):
        style = styles["table_head"] if row_index == 0 else styles["table"]
        converted.append([paragraph(cell, style) for cell in row])
    result = LongTable(converted, colWidths=[width * mm for width in widths_mm], repeatRows=1)
    result.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), BLUE),
                ("BACKGROUND", (0, 1), (-1, -1), colors.white),
                ("GRID", (0, 0), (-1, -1), 0.35, LINE),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 5),
                ("RIGHTPADDING", (0, 0), (-1, -1), 5),
                ("TOPPADDING", (0, 0), (-1, -1), 4),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, LIGHT_GRAY]),
            ]
        )
    )
    return result


def callout(text: str, styles: dict[str, ParagraphStyle]) -> Table:
    content = [[paragraph(text, styles["callout"])]]
    result = Table(content, colWidths=[174 * mm])
    result.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), LIGHT_BLUE),
                ("BOX", (0, 0), (-1, -1), 0.6, TEAL),
                ("LINEBEFORE", (0, 0), (0, -1), 3, TEAL),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ]
        )
    )
    return result


# fmt: off
# ReportLab scene and table data remain manually aligned with the published page design.
def front_view(regular: str, bold: str) -> Drawing:
    drawing = Drawing(490, 220)
    drawing.add(Rect(75, 25, 340, 16, fillColor=colors.HexColor("#9BA8B2"), strokeColor=None))
    drawing.add(String(245, 9, "лента 600 мм, Z=0", fontName=regular, fontSize=9, textAnchor="middle"))
    drawing.add(Rect(205, 41, 80, 90, fillColor=colors.HexColor("#DCEAF2"), strokeColor=BLUE))
    drawing.add(String(245, 84, "товар", fontName=bold, fontSize=11, textAnchor="middle"))
    drawing.add(String(245, 67, "высота до 600", fontName=regular, fontSize=8, textAnchor="middle"))
    drawing.add(Rect(215, 179, 60, 18, fillColor=BLUE, strokeColor=None))
    drawing.add(String(245, 184, "TOP", fontName=bold, fontSize=8, fillColor=colors.white, textAnchor="middle"))
    drawing.add(Line(245, 179, 245, 137, strokeColor=TEAL, strokeWidth=2))
    drawing.add(Polygon([241, 141, 249, 141, 245, 133], fillColor=TEAL, strokeColor=TEAL))
    drawing.add(String(245, 204, "Gocator 2690, Z=1300", fontName=regular, fontSize=8, textAnchor="middle"))
    drawing.add(Rect(18, 76, 50, 18, fillColor=BLUE, strokeColor=None))
    drawing.add(Rect(422, 76, 50, 18, fillColor=BLUE, strokeColor=None))
    drawing.add(String(43, 81, "LEFT", fontName=bold, fontSize=8, fillColor=colors.white, textAnchor="middle"))
    drawing.add(String(447, 81, "RIGHT", fontName=bold, fontSize=8, fillColor=colors.white, textAnchor="middle"))
    drawing.add(Line(68, 85, 196, 85, strokeColor=TEAL, strokeWidth=2))
    drawing.add(Line(422, 85, 294, 85, strokeColor=TEAL, strokeWidth=2))
    drawing.add(Polygon([192, 81, 192, 89, 200, 85], fillColor=TEAL, strokeColor=TEAL))
    drawing.add(Polygon([298, 81, 298, 89, 290, 85], fillColor=TEAL, strokeColor=TEAL))
    drawing.add(String(43, 63, "Y=-1100, Z=300", fontName=regular, fontSize=7, textAnchor="middle"))
    drawing.add(String(447, 63, "Y=+1100, Z=300", fontName=regular, fontSize=7, textAnchor="middle"))
    return drawing


def top_view(regular: str, bold: str) -> Drawing:
    drawing = Drawing(490, 145)
    drawing.add(Line(55, 58, 455, 58, strokeColor=colors.HexColor("#9BA8B2"), strokeWidth=12))
    drawing.add(String(455, 38, "X: движение ленты", fontName=regular, fontSize=8, textAnchor="end"))
    positions = [(100, "trigger", "-350"), (175, "left", "-150"), (245, "top", "0"), (315, "right", "+150")]
    for x, name, coordinate in positions:
        drawing.add(Line(x, 78, x, 44, strokeColor=TEAL, strokeWidth=2))
        drawing.add(String(x, 92, name, fontName=bold, fontSize=8, textAnchor="middle"))
        drawing.add(String(x, 104, f"X={coordinate}", fontName=regular, fontSize=7, textAnchor="middle"))
    drawing.add(String(245, 13, "Разнесение сечений требует компенсации движения энкодером", fontName=regular, fontSize=8, textAnchor="middle"))
    return drawing


def footer(canvas: Canvas, document: SimpleDocTemplate) -> None:
    canvas.saveState()
    canvas.setStrokeColor(LINE)
    canvas.line(18 * mm, 13 * mm, PAGE_WIDTH - 18 * mm, 13 * mm)
    canvas.setFillColor(MUTED)
    canvas.setFont("ReportRegular", 7.5)
    canvas.drawString(18 * mm, 8 * mm, "Ozon Tech CV - Variant 1 - engineering proposal")
    canvas.drawRightString(PAGE_WIDTH - 18 * mm, 8 * mm, f"Страница {document.page}")
    canvas.restoreState()


def build_story(styles: dict[str, ParagraphStyle], regular: str, bold: str) -> list[object]:
    story: list[object] = []
    story.extend(
        [
            Spacer(1, 12 * mm),
            paragraph("Измерение габаритов товара на конвейере", styles["title"]),
            paragraph("Вариант 1 - аудит проекта и промышленная конфигурация сенсоров", styles["subtitle"]),
            callout(
                "<b>Статус:</b> реализовано офлайн геометрическое ядро и контракты "
                "профилометрического контура. Физическая установка, метрологическая "
                "точность и exact MVBB пока не подтверждены.",
                styles,
            ),
            Spacer(1, 7 * mm),
            paragraph("Цель и критерий", styles["heading"]),
            paragraph(
                "Система должна определить три габарита товара на ленте шириной 600 мм "
                "при скорости 1 м/с. Для каждого размера принимается допуск "
                "|d_hat - d| <= max(0.05 d, 5 мм). Успех требует одновременного "
                "выполнения условия по всем трём осям; отказы, пропуски и дубли входят "
                "в знаменатель метрики.",
                styles["body"],
            ),
            paragraph("Итог аудита", styles["heading"]),
            table(
                [
                    ["Сильная сторона", "Незакрытый риск"],
                    ["Малые модули, воспроизводимое окружение, классическая геометрия, SQLite outbox.", "Ранее частичное облако, два товара и выброс могли выдать правдоподобные неверные размеры."],
                    ["Open3D baseline теперь прямо назван приближённым.", "Требование глобально точного minimum-volume box не доказано и остаётся открытым."],
                    ["Валидация входов, immutability калибровки, quality gates и тесты добавлены.", "Нет live acquisition, межсенсорной калибровки, измеренных материалов и WMS endpoint."],
                ],
                [82, 92],
                styles,
            ),
            Spacer(1, 7 * mm),
            paragraph("Рекомендация", styles["heading"]),
            paragraph(
                "Основной кандидат для квалификационного стенда - три синхронизированных "
                "лазерных профиломера LMI Gocator 2690 Remastered, общий энкодер SICK "
                "DFS60E-S4EA01024, датчик прохода SICK WL4SL-3P2232 и LMI Master 810. "
                "Профиль + энкодер соответствует новому контракту программного контура.",
                styles["body"],
            ),
        ]
    )
    story.append(PageBreak())

    story.extend(
        [
            paragraph("Комплект сенсоров", styles["heading"]),
            table(
                [
                    ["Роль", "Модель", "Количество", "Обоснование"],
                    ["Геометрия", "LMI Gocator 2690 Remastered", "3", "3700 точек в профиле, поле 385-2000 мм, диапазон глубины 1550 мм, GigE, IP67."],
                    ["Ход ленты", "SICK DFS60E-S4EA01024, 1037697", "1", "1024 импульса/оборот и 6-канальный HTL. Привязывает профиль к фактическому перемещению."],
                    ["Триггер", "SICK WL4SL-3P2232, 1061561 + PL20A", "1", "Ретроотражающий датчик: пятно 1 мм на 500 мм, отклик <= 0,5 мс по datasheet."],
                    ["Синхронизация", "LMI Master 810", "1", "Общая синхронизация головок, положения энкодера и I/O."],
                    ["Вычислитель", "Advantech MIC-770 V3, 32 ГБ RAM, SSD", "1", "Промышленное семейство; CPU и хранилище уточняются по измеренному потоку и температуре."],
                ],
                [25, 43, 15, 91],
                styles,
            ),
            Spacer(1, 6 * mm),
            paragraph("Паспортные характеристики Gocator 2690", styles["subheading"]),
            table(
                [
                    ["Параметр", "Значение", "Интерпретация"],
                    ["Профиль", "3700 точек; 900 Гц при полном поле; до 10 кГц после оптимизации", "Максимальная частота зависит от области и режима."],
                    ["Поле и шаг", "385-2000 мм; 0,124-0,550 мм", "Предварительно покрывает ленту и минимальные объекты."],
                    ["Z", "clearance 325 мм; range 1550 мм; repeatability 12 мкм", "Repeatability на эталоне не равна ошибке готового габарита."],
                    ["Линейность", "±0,08 % диапазона, около ±1,24 мм", "Только один вклад в error budget; не использовать как обещание R06."],
                ],
                [32, 55, 87],
                styles,
            ),
            Spacer(1, 5 * mm),
            callout(
                "Паспортные характеристики получены в определённой конфигурации и на "
                "эталонной поверхности. Результат на товаре дополнительно зависит от "
                "материала, экспозиции, обеих границ, калибровки и полноты наблюдения.",
                styles,
            ),
            Spacer(1, 5 * mm),
            paragraph("Почему не RealSense D455 как основной выбор", styles["subheading"]),
            paragraph(
                "D455 удобен для недорогого прототипа, но заявление менее 2 % на 4 м не "
                "доказывает миллиметровую точность в рабочей зоне, а широкое поле уменьшает "
                "число пикселей на объекте 10 мм. Gocator 2380 имеет меньшую плотность "
                "профиля; Micro-Epsilon scanCONTROL 30x0-600 требует иной компоновки из-за "
                "диапазона глубины 530-1010 мм.",
                styles["body"],
            ),
        ]
    )
    story.append(PageBreak())

    story.extend(
        [
            paragraph("Физическое расположение", styles["heading"]),
            paragraph("Система координат: X - движение ленты, Y - поперёк, Z - вверх от ленты. Проектное рабочее сечение: 600 x 600 мм.", styles["body"]),
            front_view(regular, bold),
            Spacer(1, 2 * mm),
            top_view(regular, bold),
            Spacer(1, 5 * mm),
            table(
                [
                    ["Узел", "Оптическая точка, мм", "Ориентация"],
                    ["Верхний Gocator", "(0, 0, 1300)", "Вниз; линия вдоль Y."],
                    ["Левый Gocator", "(-150, -1100, 300)", "К центру; линия вдоль Z."],
                    ["Правый Gocator", "(+150, +1100, 300)", "К центру; линия вдоль Z."],
                    ["Датчик прохода", "(-350, -400, 5)", "На отражатель в (-350, +400, 5)."],
                    ["Энкодер", "Возле зоны измерения", "Подпружиненное колесо по ленте."],
                ],
                [38, 52, 84],
                styles,
            ),
            Spacer(1, 6 * mm),
            paragraph("Покрытие", styles["subheading"]),
            paragraph("Для крайних паспортных значений используется линейная оценка W(d) = 385 + (2000 - 385) / 1550 x (d - 325).", styles["body"]),
            table(
                [
                    ["Высота поверхности", "Дистанция верхней головы", "Ширина поля"],
                    ["0 мм", "1300 мм", "1400,9 мм"],
                    ["300 мм", "1000 мм", "1088,3 мм"],
                    ["600 мм", "700 мм", "775,7 мм"],
                ],
                [50, 63, 61],
                styles,
            ),
            paragraph(
                "На высоте 600 мм запас составляет около 87,9 мм с каждой стороны ленты. "
                "Боковые головки видят вертикальное поле около 879,9-1505 мм на дистанции "
                "800-1400 мм. Это предварительная оптическая проверка, не CAD-подтверждение "
                "отсутствия затенений корпусом, бортами и товаром.",
                styles["body"],
            ),
        ]
    )
    story.append(PageBreak())

    story.extend(
        [
            paragraph("Синхронизация и программный конвейер", styles["heading"]),
            paragraph("При окружности колеса 200 мм и счёте 4 x 1024 шаг равен 0,04883 мм/отсчёт. Захват через 25 отсчётов даёт 1,221 мм между профилями и 819,2 профиля/с на 1 м/с.", styles["body"]),
            table(
                [
                    ["Этап", "Реализованный контракт", "Защита от ложного размера"],
                    ["Захват", "LaserProfile: sensor_id, time, encoder, points, mask, intensity, calibration_id.", "NaN/Inf, несовпадающие маски и изменяемые данные отклоняются."],
                    ["Регистрация", "p_ref = T_i p_i - [s(t)-s(t_ref), 0, 0].", "Используется жёсткая конечная матрица; масштабирование матрицей запрещено."],
                    ["Сегментация", "DBSCAN: одна поддержанная компонента.", "Одиночный выброс удаляется; два товара дают rejected."],
                    ["Наблюдаемость", "CaptureEvidence: ракурсы, пропуски, ROI, компоненты.", "Неполное облако не попадает в OBB."],
                    ["Геометрия", "Open3D face-aligned approximate OBB.", "Копланарное/пустое облако получает диагностическую причину."],
                    ["Доставка", "SQLite outbox с measurement_id.", "False только для дубликата; другие integrity errors не скрываются."],
                ],
                [31, 70, 73],
                styles,
            ),
            Spacer(1, 7 * mm),
            paragraph("Статус результата", styles["subheading"]),
            paragraph(
                "MeasurementResult хранит valid/rejected/error, причину, число точек и для "
                "valid - размеры, центр, ориентацию и идентификатор алгоритма. В WMS может "
                "попасть только valid с тремя конечными положительными размерами. Высота над "
                "лентой не выводится из порядка канонически отсортированных рёбер OBB.",
                styles["body"],
            ),
            callout(
                "Параметры DBSCAN, граница ROI, окружность колеса и допустимые пропуски "
                "нельзя зашивать как физические константы. Их нужно определить по записанным "
                "профилям и трассировать с версией калибровки.",
                styles,
            ),
        ]
    )
    story.append(PageBreak())

    story.extend(
        [
            paragraph("Открытые пункты и программа квалификации", styles["heading"]),
            table(
                [
                    ["Требование", "Текущий статус", "Что нужно для закрытия"],
                    ["R02 exact MVBB", "Открыто", "Сравнить с независимым верифицированным MVBB backend на аналитических и реальных облаках."],
                    ["R03/R04 диапазон и 1 м/с", "Открыто", "One-head gate и CAD, затем трёхголовый стенд на крайних габаритах."],
                    ["R06 точность", "Открыто", "Независимый ground truth и 5400 предъявлений; считать bias, max, P95/P99, отказы и пропуски."],
                    ["R07 WMS", "Частично", "Согласовать endpoint, auth, contract ответа, retry и SLA; измерить latency до подтверждения."],
                    ["R08 оборудование", "Проектно готово", "Проверить конкретную ревизию, CAD, безопасность и коммерческие условия."],
                ],
                [34, 35, 105],
                styles,
            ),
            Spacer(1, 7 * mm),
            paragraph("Порядок испытаний", styles["subheading"]),
            paragraph("1. Одна головка: 10-30 мм, края поля, белые и чёрные материалы, 1 м/с, экспозиция <= 250 мкс и фактическая частота.", styles["body"]),
            paragraph("2. Три головки: межсенсорная калибровка, взаимные помехи, Master/encoder sync, сохранение формы последовательного скана.", styles["body"]),
            paragraph("3. Приёмка: 36 категорий/образцов x 5 углов x 3 положения по Y x 10 повторов = 5400 предъявлений. Статика и 0,5 м/с используются для диагностики.", styles["body"]),
            paragraph("4. В отчёт попадают максимальная ошибка, систематическое смещение, P95/P99, доля rejected, пропуски профилей и задержка WMS. Интервал 3 с не определяет latency сортировки без расстояния до следующего узла.", styles["body"]),
            Spacer(1, 5 * mm),
            callout(
                "Три профиломера не гарантируют форму прозрачного, зеркального или "
                "деформируемого товара и не наблюдают нижнюю поверхность. Исключать эти "
                "предъявления из метрики нельзя: неподтверждённый случай должен быть отказом.",
                styles,
            ),
        ]
    )
    story.append(PageBreak())

    story.extend(
        [
            paragraph("Источники и трассируемость", styles["heading"]),
            paragraph("Все характеристики оборудования ниже - паспортные данные производителя. Цены, сроки поставки и физические результаты не оценивались.", styles["body"]),
            table(
                [
                    ["Источник", "Использование"],
                    ["LMI Gocator 2600 Series и каталог LMI 2026", "2690: поле, диапазон, точки профиля, частота, интерфейс, repeatability и линейность."],
                    ["LMI Networking / Master", "Роль Master 810 в синхронизации сенсоров, энкодера и I/O."],
                    ["SICK DFS60E-S4EA01024 datasheet", "1024 импульса/оборот и HTL-интерфейс энкодера."],
                    ["SICK WL4SL-3P2232 datasheet", "Ретроотражающий датчик, пятно и время отклика."],
                    ["LMI exposure guidance", "Проверка экспозиции как физический gate, а не гарантированный режим."],
                    ["RealSense D455, Gocator 2300, Micro-Epsilon scanCONTROL 30x0-600", "Сравнение альтернатив и ограничения выбранной компоновки."],
                ],
                [68, 106],
                styles,
            ),
            Spacer(1, 7 * mm),
            paragraph("URL первичных источников", styles["subheading"]),
            paragraph("https://lmi3d.com/series/gocator-2600-series/", styles["source"]),
            paragraph("https://lmi3d.com/wp-content/uploads/2026/01/BROCHURE_3D_Smart_Sensors_US_WEB.pdf", styles["source"]),
            paragraph("https://lmi3d.com/technology/networking/", styles["source"]),
            paragraph("https://www.sick.com/media/pdf/1/61/861/dataSheet_DFS60E-S4EA01024_1037697_en.pdf", styles["source"]),
            paragraph("https://www.sick.com/media/pdf/0/50/050/dataSheet_WL4SL-3P2232_1061561_en.pdf", styles["source"]),
            paragraph("https://support.lmi3d.com/hc/en-us/articles/360033661771-Choosing-proper-exposure-time-for-Gocator-line-profiler-G2xxx", styles["source"]),
            paragraph("https://www.realsenseai.com/products/real-sense-depth-camera-d455f/", styles["source"]),
            paragraph("https://lmi3d.com/wp-content/uploads/2019-03/DATASHEET_Gocator_2300_US_WEB.pdf", styles["source"]),
            paragraph("https://www.micro-epsilon.com/fileadmin/download/products/dat--scanCONTROL-30x0-430-600--en.pdf", styles["source"]),
            Spacer(1, 8 * mm),
            paragraph("Состояние программной валидации", styles["heading"]),
            paragraph(
                "Репозиторий содержит unit и integration тесты, Ruff, mypy, uv.lock check, "
                "pre-commit и GitHub Actions workflow. Их успешное выполнение доказывает "
                "только программные инварианты. Перед production-утверждением требуется "
                "стендовая программа из предыдущего раздела.",
                styles["body"],
            ),
        ]
    )
    return story


# fmt: on
def main() -> None:
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    regular, bold = register_fonts()
    styles = make_styles(regular, bold)
    document = SimpleDocTemplate(
        str(OUTPUT),
        pagesize=A4,
        rightMargin=18 * mm,
        leftMargin=18 * mm,
        topMargin=17 * mm,
        bottomMargin=18 * mm,
        title="Conveyor Dimensioning System - Variant 1",
        author="Ozon Tech CV project",
    )
    document.build(build_story(styles, regular, bold), onFirstPage=footer, onLaterPages=footer)


if __name__ == "__main__":
    main()
