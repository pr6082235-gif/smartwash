"""PDF Invoice Generation Service"""
import os
from datetime import datetime


def generate_invoice_pdf(order, items, payment):
    """Generate professional PDF invoice"""
    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.units import mm
        from reportlab.lib import colors
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
        from reportlab.lib.enums import TA_CENTER, TA_RIGHT, TA_LEFT
        import qrcode
        from io import BytesIO
        from reportlab.platypus import Image as RLImage
        
        pdf_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static', 'pdfs')
        os.makedirs(pdf_dir, exist_ok=True)
        pdf_path = os.path.join(pdf_dir, f"invoice_{order['order_id']}.pdf")
        
        doc = SimpleDocTemplate(pdf_path, pagesize=A4,
                               rightMargin=15*mm, leftMargin=15*mm,
                               topMargin=15*mm, bottomMargin=15*mm)
        
        # Colors
        PRIMARY = colors.HexColor('#2563EB')
        ACCENT = colors.HexColor('#10B981')
        DARK = colors.HexColor('#1E293B')
        LIGHT_BG = colors.HexColor('#F8FAFC')
        BORDER = colors.HexColor('#E2E8F0')
        
        styles = getSampleStyleSheet()
        story = []
        
        # Header
        header_data = [
            [
                Paragraph('<font size="22" color="#2563EB"><b>SmartWash Pro</b></font>', styles['Normal']),
                Paragraph(f'<font size="11" color="#64748B">INVOICE</font><br/><font size="18" color="#1E293B"><b>#{order["order_id"]}</b></font>', 
                         ParagraphStyle('right', alignment=TA_RIGHT, parent=styles['Normal']))
            ]
        ]
        header_table = Table(header_data, colWidths=[90*mm, 90*mm])
        header_table.setStyle(TableStyle([
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
            ('BACKGROUND', (0,0), (-1,-1), LIGHT_BG),
            ('ROWPADDING', (0,0), (-1,-1), 8),
            ('LINEBELOW', (0,0), (-1,0), 2, PRIMARY),
        ]))
        story.append(header_table)
        story.append(Spacer(1, 5*mm))
        
        # Company & Customer info
        company_info = f"""<font size="9" color="#64748B">
        <b>SmartWash Pro</b><br/>
        Professional Laundry Services<br/>
        Owner: Suresh Gopi<br/>
        GST: 29XXXXX1234X1ZX<br/>
        Phone: +91-XXXXXXXXXX
        </font>"""
        
        customer_info = f"""<font size="9" color="#64748B">
        <b>Bill To:</b><br/>
        <font size="10" color="#1E293B"><b>{order['customer_name']}</b></font><br/>
        Phone: {order['phone']}<br/>
        {'Email: ' + order.get('email', '') + '<br/>' if order.get('email') else ''}
        </font>"""
        
        order_meta = f"""<font size="9" color="#64748B">
        <b>Order Details:</b><br/>
        Date: {order['created_at'].strftime('%d %b %Y') if hasattr(order['created_at'], 'strftime') else order['created_at']}<br/>
        Delivery: {order['delivery_date']}<br/>
        Status: <font color="#10B981"><b>{order['status'].upper()}</b></font><br/>
        Priority: {order['priority'].upper()}
        </font>"""
        
        info_data = [[
            Paragraph(company_info, styles['Normal']),
            Paragraph(customer_info, styles['Normal']),
            Paragraph(order_meta, styles['Normal'])
        ]]
        info_table = Table(info_data, colWidths=[60*mm, 60*mm, 60*mm])
        info_table.setStyle(TableStyle([
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
            ('BACKGROUND', (0,0), (-1,-1), LIGHT_BG),
            ('ROWPADDING', (0,0), (-1,-1), 6),
            ('BOX', (0,0), (-1,-1), 0.5, BORDER),
            ('LINEBEFORE', (1,0), (1,-1), 0.5, BORDER),
            ('LINEBEFORE', (2,0), (2,-1), 0.5, BORDER),
        ]))
        story.append(info_table)
        story.append(Spacer(1, 5*mm))
        
        # Items table
        item_header = [
            Paragraph('<b>Item</b>', styles['Normal']),
            Paragraph('<b>Service</b>', styles['Normal']),
            Paragraph('<b>Qty</b>', styles['Normal']),
            Paragraph('<b>Unit Price</b>', styles['Normal']),
            Paragraph('<b>Total</b>', styles['Normal'])
        ]
        
        table_data = [item_header]
        
        if items:
            for item in items:
                table_data.append([
                    item.get('item_name', '-'),
                    item.get('service_type', '-').replace('_', ' ').title(),
                    str(item.get('quantity', 1)),
                    f"₹{item.get('unit_price', 0):.2f}",
                    f"₹{item.get('total_price', 0):.2f}"
                ])
        else:
            table_data.append([
                order['service_type'].replace('_', ' ').title(),
                '-',
                str(order['dress_quantity']),
                f"₹{order['total_amount'] / max(order['dress_quantity'], 1):.2f}",
                f"₹{order['total_amount']:.2f}"
            ])
        
        items_table = Table(table_data, colWidths=[55*mm, 35*mm, 15*mm, 30*mm, 30*mm])
        items_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), PRIMARY),
            ('TEXTCOLOR', (0,0), (-1,0), colors.white),
            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
            ('FONTSIZE', (0,0), (-1,0), 9),
            ('ROWPADDING', (0,0), (-1,-1), 6),
            ('ALIGN', (2,0), (-1,-1), 'RIGHT'),
            ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, LIGHT_BG]),
            ('GRID', (0,0), (-1,-1), 0.5, BORDER),
            ('FONTSIZE', (0,1), (-1,-1), 9),
        ]))
        story.append(items_table)
        story.append(Spacer(1, 3*mm))
        
        # Totals
        totals_data = [
            ['', '', '', 'Subtotal:', f"₹{order['total_amount']:.2f}"],
            ['', '', '', f"GST (18%):", f"₹{order.get('gst_amount', 0):.2f}"],
            ['', '', '', f"Discount:", f"-₹{order.get('discount', 0):.2f}"],
        ]
        
        totals_table = Table(totals_data, colWidths=[55*mm, 35*mm, 15*mm, 30*mm, 30*mm])
        totals_table.setStyle(TableStyle([
            ('ALIGN', (3,0), (-1,-1), 'RIGHT'),
            ('FONTSIZE', (0,0), (-1,-1), 9),
            ('ROWPADDING', (0,0), (-1,-1), 4),
            ('TEXTCOLOR', (3,0), (3,-1), colors.HexColor('#64748B')),
        ]))
        story.append(totals_table)
        
        # Final amount
        final_data = [['', '', '', 
                       Paragraph('<b>TOTAL AMOUNT</b>', styles['Normal']),
                       Paragraph(f'<font size="12"><b>₹{order["final_amount"]:.2f}</b></font>', 
                                ParagraphStyle('total', alignment=TA_RIGHT, parent=styles['Normal']))]]
        final_table = Table(final_data, colWidths=[55*mm, 35*mm, 15*mm, 30*mm, 30*mm])
        final_table.setStyle(TableStyle([
            ('BACKGROUND', (3,0), (-1,-1), PRIMARY),
            ('TEXTCOLOR', (3,0), (-1,-1), colors.white),
            ('ALIGN', (3,0), (-1,-1), 'RIGHT'),
            ('ROWPADDING', (0,0), (-1,-1), 8),
        ]))
        story.append(final_table)
        story.append(Spacer(1, 5*mm))
        
        # Payment status
        if payment:
            pay_status = payment.get('payment_status', 'pending')
            pay_method = payment.get('payment_method', 'cash')
            pay_color = '#10B981' if pay_status == 'paid' else '#F59E0B'
            
            pay_info = Paragraph(
                f'<font size="9">Payment Method: <b>{pay_method.upper()}</b> &nbsp;&nbsp; '
                f'Status: <font color="{pay_color}"><b>{pay_status.upper()}</b></font></font>',
                styles['Normal']
            )
            story.append(pay_info)
        
        story.append(Spacer(1, 5*mm))
        
        # QR Code
        try:
            qr_data = f"SmartWash Pro | Order: {order['order_id']} | Amount: ₹{order['final_amount']}"
            qr = qrcode.QRCode(version=1, box_size=3, border=2)
            qr.add_data(qr_data)
            qr.make(fit=True)
            qr_img = qr.make_image(fill_color='#2563EB', back_color='white')
            qr_buffer = BytesIO()
            qr_img.save(qr_buffer, format='PNG')
            qr_buffer.seek(0)
            
            qr_rl = RLImage(qr_buffer, width=25*mm, height=25*mm)
            qr_data_text = Paragraph(
                f'<font size="8" color="#64748B">Scan to verify order<br/>{order["order_id"]}</font>',
                ParagraphStyle('qr_text', alignment=TA_CENTER, parent=styles['Normal'])
            )
            
            qr_table = Table([[qr_rl, qr_data_text]], colWidths=[30*mm, 140*mm])
            story.append(qr_table)
        except:
            pass
        
        # Footer
        story.append(Spacer(1, 5*mm))
        story.append(HRFlowable(width='100%', thickness=1, color=BORDER))
        story.append(Spacer(1, 2*mm))
        story.append(Paragraph(
            '<font size="8" color="#94A3B8">Thank you for choosing SmartWash Pro! | '
            'Owner: Suresh Gopi | Professional Laundry Management System</font>',
            ParagraphStyle('footer', alignment=TA_CENTER, parent=styles['Normal'])
        ))
        
        doc.build(story)
        return pdf_path
        
    except Exception as e:
        print(f"PDF generation error: {e}")
        raise e
