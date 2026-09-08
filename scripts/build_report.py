"""Build the required Variant 1 PDF report."""

from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "output" / "pdf" / "ozon_variant_1_report.pdf"
FONT = Path("C:/Windows/Fonts/arial.ttf")


def paragraph(text: str, style: ParagraphStyle) -> Paragraph:
    return Paragraph(text, style)


def main() -> None:
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    pdfmetrics.registerFont(TTFont("Arial", str(FONT)))
    styles = getSampleStyleSheet()
    body = ParagraphStyle("BodyRu", parent=styles["BodyText"], fontName="Arial", leading=15)
    title = ParagraphStyle("TitleRu", parent=styles["Title"], fontName="Arial", leading=26)
    heading = ParagraphStyle("HeadingRu", parent=styles["Heading2"], fontName="Arial", leading=18)
    document = SimpleDocTemplate(
        str(OUTPUT), pagesize=A4, rightMargin=20 * mm, leftMargin=20 * mm, topMargin=18 * mm
    )
    story = [
        paragraph("Conveyor Dimensioning System", title),
        paragraph("Тестовое задание Ozon Tech / Университет Иннополис 2026 - вариант 1", body),
        Spacer(1, 8 * mm),
        paragraph("Задача", heading),
        paragraph(
            "Измерять длину, ширину и высоту товара на конвейере шириной 600 мм, "
            "движущемся со скоростью 1 м/с. Диапазон товара: от 10x10x10 до 400x300x300 мм; "
            "интервал между товарами - 3 с. Результат передаётся в WMS.",
            body,
        ),
        paragraph("Требование точности", heading),
        paragraph(
            "Для каждого измерения допускается абсолютная ошибка не более "
            "max(0,05*d, 5 мм), где d - эталонный размер в миллиметрах. "
            "Все три измерения должны удовлетворять этому правилу.",
            body,
        ),
        paragraph("Проектное решение", heading),
        paragraph(
            "Целевая схема использует несколько синхронизированных depth-камер, "
            "калибруемых в системе координат ленты. После удаления плоскости конвейера "
            "облака точек объединяются, фильтруются и передаются в модуль ориентированного "
            "ограничивающего параллелепипеда. WMS получает idempotent-сообщение с размерами, "
            "качеством и версией калибровки.",
            body,
        ),
        paragraph("Реализованный программный baseline", heading),
        paragraph(
            "Реализован офлайн-пайплайн на Python 3.12, NumPy и Open3D: загрузка "
            "калиброванного облака из NPZ, удаление точек ленты и расчёт ориентированного "
            "bounding box. В демонстрации синтетический товар 200x100x50 мм возвращает "
            "эти размеры. Алгоритм Open3D помечен как приближённый: он не является "
            "подтверждённым глобально точным minimum-volume bounding box для произвольной формы.",
            body,
        ),
        paragraph("Проверка и ограничения", heading),
    ]
    data = [
        ["Проверка", "Статус"],
        ["Unit и integration тесты", "см. актуальный CI-запуск"],
        ["Ruff / mypy", "пройдены"],
        ["Камеры, калибровка, точность", "нужен физический стенд"],
        ["Точный глобальный MVBB", "нужен отдельный backend или реализация"],
    ]
    table = Table(data, colWidths=[85 * mm, 85 * mm])
    table.setStyle(
        TableStyle(
            [
                ("FONTNAME", (0, 0), (-1, -1), "Arial"),
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#005B99")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#B8C4CE")),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("LEFTPADDING", (0, 0), (-1, -1), 6),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ]
        )
    )
    story.extend([table, Spacer(1, 6 * mm)])
    story.append(paragraph("Подробный план, допущения и ссылки на источники находятся в implementation_plan.md.", body))
    document.build(story)


if __name__ == "__main__":
    main()
