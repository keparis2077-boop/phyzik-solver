"""
pdf_report.py — генерация PDF-отчётов по решённым задачам
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm, inch
from reportlab.lib.colors import HexColor
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY

# Совместимость с разными версиями reportlab
try:
    from reportlab.lib.pagesizes import a4 as a4_size
except ImportError:
    a4_size = A4
from datetime import datetime


# Цвета
PRIMARY = HexColor('#6366f1')
PRIMARY_LIGHT = HexColor('#eef2ff')
TEXT = HexColor('#1e293b')
TEXT_SECONDARY = HexColor('#64748b')
BORDER = HexColor('#e2e8f0')


def create_pdf_report(task_name, category, steps, results, explanation, username=None, filename=None):
    """
    Создаёт PDF-отчёт по решённой задаче.
    
    Args:
        task_name: название задачи
        category: категория
        steps: список шагов решения
        results: словарь результатов {ключ: значение}
        explanation: пояснение
        username: имя пользователя
        filename: имя файла (опционально)
    
    Returns:
        путь к сохранённому PDF-файлу
    """
    if filename is None:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'fizik_report_{timestamp}.pdf'
    
    doc = SimpleDocTemplate(
        filename,
        pagesize=a4_size,
        rightMargin=20*mm,
        leftMargin=20*mm,
        topMargin=20*mm,
        bottomMargin=20*mm,
    )
    
    container = []
    
    # Стили
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=PRIMARY,
        spaceAfter=12*mm,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold',
    )
    
    subtitle_style = ParagraphStyle(
        'CustomSubtitle',
        parent=styles['Normal'],
        fontSize=14,
        textColor=TEXT_SECONDARY,
        spaceAfter=8*mm,
        alignment=TA_CENTER,
        fontName='Helvetica',
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=16,
        textColor=PRIMARY,
        spaceBefore=10*mm,
        spaceAfter=6*mm,
        fontName='Helvetica-Bold',
    )
    
    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['Normal'],
        fontSize=12,
        textColor=TEXT,
        spaceAfter=4*mm,
        alignment=TA_JUSTIFY,
        leading=18,
        fontName='Helvetica',
    )
    
    step_style = ParagraphStyle(
        'CustomStep',
        parent=styles['Normal'],
        fontSize=12,
        textColor=TEXT,
        spaceAfter=3*mm,
        leftIndent=10*mm,
        leading=16,
        fontName='Helvetica',
    )
    
    # Заголовок
    container.append(Paragraph('ФИЗИК-СОЛВЕР', styles['Heading1']))
    container.append(Spacer(1, 3*mm))
    container.append(Paragraph(f'Отчёт по задаче', subtitle_style))
    container.append(Spacer(1, 5*mm))
    
    # Название задачи
    container.append(Paragraph(task_name, styles['Heading2']))
    container.append(Spacer(1, 3*mm))
    
    # Информация
    info_data = [
        [Paragraph('<b>Категория:</b>', styles['Normal']), Paragraph(category, styles['Normal'])],
        [Paragraph('<b>Дата:</b>', styles['Normal']), Paragraph(datetime.now().strftime('%d.%m.%Y %H:%M'), styles['Normal'])],
    ]
    if username:
        info_data.append([Paragraph('<b>Пользователь:</b>', styles['Normal']), Paragraph(username, styles['Normal'])])
    
    info_table = Table(info_data, colWidths=[30*mm, 100*mm])
    info_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), PRIMARY_LIGHT),
        ('TEXTCOLOR', (0, 0), (0, -1), TEXT),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        (' BORDER', (0, 0), (-1, -1), 1, BORDER),
        ('CELLPADDING', (0, 0), (-1, -1), 4),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    container.append(info_table)
    container.append(Spacer(1, 8*mm))
    
    # Ход решения
    container.append(Paragraph('Ход решения', heading_style))
    for i, step in enumerate(steps, 1):
        container.append(Paragraph(f'<b>{i}.</b> {step}', step_style))
    
    container.append(Spacer(1, 6*mm))
    
    # Ответ
    container.append(Paragraph('Ответ', heading_style))
    result_lines = []
    for key, value in results.items():
        result_lines.append(f'<b>{key}</b> = {value}')
    
    result_text = '<br/>'.join(result_lines)
    result_style = ParagraphStyle(
        'Result',
        parent=styles['Normal'],
        fontSize=14,
        textColor=PRIMARY,
        fontName='Helvetica-Bold',
        backcolor=PRIMARY_LIGHT,
        borderPadding=6*mm,
    )
    container.append(Paragraph(result_text, result_style))
    
    container.append(Spacer(1, 6*mm))
    
    # Пояснение
    container.append(Paragraph('Пояснение', heading_style))
    container.append(Paragraph(explanation, body_style))
    
    # Подвал
    container.append(Spacer(1, 15*mm))
    footer_style = ParagraphStyle(
        'Footer',
        parent=styles['Normal'],
        fontSize=9,
        textColor=TEXT_SECONDARY,
        alignment=TA_CENTER,
        fontName='Helvetica',
    )
    container.append(Paragraph('Создано в системе Физик-Солвер • fizik-solver.ru', footer_style))
    
    # Построение PDF
    doc.build(container)
    
    return filename
