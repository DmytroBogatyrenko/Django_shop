import io

from django.http import HttpResponse
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import (
    SimpleDocTemplate, Table, TableStyle,
    Paragraph, Spacer, HRFlowable,
)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os


def generate_order_pdf(order):

    buffer = io.BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=2*cm,
        leftMargin=2*cm,
        topMargin=2*cm,
        bottomMargin=2*cm,
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Normal'],
        fontSize=20,
        fontName='Helvetica-Bold',
        textColor=colors.HexColor('#1a3a2a'),
        spaceAfter=6,
    )

    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Normal'],
        fontSize=11,
        fontName='Helvetica-Bold',
        textColor=colors.HexColor('#c9a84c'),
        spaceBefore=12,
        spaceAfter=4,
    )

    normal_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontSize=9,
        fontName='Helvetica',
        textColor=colors.HexColor('#333333'),
    )

    muted_style = ParagraphStyle(
        'CustomMuted',
        parent=styles['Normal'],
        fontSize=8,
        fontName='Helvetica',
        textColor=colors.HexColor('#888888'),
    )

    story = []

    story.append(Paragraph('TSYTADEL', title_style))
    story.append(Paragraph('Kramnytsya Relikviyi', muted_style))
    story.append(Spacer(1, 0.3*cm))
    story.append(HRFlowable(
        width="100%", thickness=1,
        color=colors.HexColor('#c9a84c'), spaceAfter=8,
    ))

    story.append(Paragraph(f'RAKHUNOK #{order.id}', heading_style))

    info_data = [
        ['Data stvorennya:', order.created_at.strftime('%d.%m.%Y %H:%M')],
        ['Status:', order.get_status_display()],
    ]
    if order.estimated_delivery:
        info_data.append(
            ['Ochikuvana dostavka:', order.estimated_delivery.strftime('%d.%m.%Y')]
        )

    info_table = Table(info_data, colWidths=[5*cm, 12*cm])
    info_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#888888')),
        ('TEXTCOLOR', (1, 0), (1, -1), colors.HexColor('#333333')),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(info_table)
    story.append(Spacer(1, 0.4*cm))

    try:
        addr = order.shipping_address
        story.append(Paragraph('ADRESA DOSTAVKY', heading_style))

        addr_data = [
            ['Oderzhuval:', f'{addr.first_name} {addr.last_name}'],
            ['Email:', addr.email],
            ['Telefon:', addr.phone],
            ['Misto:', addr.city],
            ['Adresa:', addr.address],
            ['Indeks:', addr.postal_code],
        ]
        addr_table = Table(addr_data, colWidths=[4*cm, 13*cm])
        addr_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#888888')),
            ('TEXTCOLOR', (1, 0), (1, -1), colors.HexColor('#333333')),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ]))
        story.append(addr_table)
        story.append(Spacer(1, 0.4*cm))
    except Exception:
        pass

    story.append(Paragraph('TOVARY', heading_style))

    items_data = [['Nazva tovaru', 'Kil-kist', 'Tsina', 'Suma']]

    for item in order.items.all():
        items_data.append([
            item.product_name,
            str(item.quantity),
            f'{item.price} hrn',
            f'{item.get_total_price()} hrn',
        ])

    items_table = Table(
        items_data,
        colWidths=[9*cm, 2.5*cm, 3*cm, 2.5*cm],
    )
    items_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1a3a2a')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor('#c9a84c')),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 9),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.HexColor('#333333')),
        ('ALIGN', (1, 0), (-1, -1), 'CENTER'),
        ('ALIGN', (0, 0), (0, -1), 'LEFT'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#dddddd')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f9f9f9')]),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(items_table)
    story.append(Spacer(1, 0.3*cm))

    total_data = []

    if order.discount:
        total_data.append(
            ['Znyzhka (promokod):', f'-{order.discount}%']
        )

    total_data.append(['RAZOM DO SPLATY:', f'{order.total_price} hrn'])

    total_table = Table(total_data, colWidths=[13*cm, 4*cm])
    total_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -2), 'Helvetica'),
        ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('TEXTCOLOR', (0, -1), (-1, -1), colors.HexColor('#1a3a2a')),
        ('ALIGN', (0, 0), (-1, -1), 'RIGHT'),
        ('TOPPADDING', (0, -1), (-1, -1), 6),
        ('LINEABOVE', (0, -1), (-1, -1), 1, colors.HexColor('#c9a84c')),
    ]))
    story.append(total_table)

    story.append(Spacer(1, 1*cm))
    story.append(HRFlowable(
        width="100%", thickness=0.5,
        color=colors.HexColor('#dddddd'), spaceAfter=6,
    ))
    story.append(Paragraph(
        '2026 Orden Tsytadeli · Dyakuyemo za pokupku!',
        muted_style,
    ))

    doc.build(story)

    buffer.seek(0)

    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = (
        f'attachment; filename="order_{order.id}.pdf"'
    )
    return response