import os
from datetime import datetime


def generate_pdf(summary: str, output_path: str) -> str:
    """
    Generate a professional styled PDF medical report.
    Uses ReportLab with custom styles.
    """
    try:
        from reportlab.platypus import (
            SimpleDocTemplate, Paragraph, Spacer, HRFlowable, Table, TableStyle
        )
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.pagesizes import A4
        from reportlab.lib.units import cm
        from reportlab.lib import colors
        from reportlab.lib.enums import TA_CENTER, TA_LEFT

        doc = SimpleDocTemplate(
            output_path,
            pagesize=A4,
            rightMargin=2*cm,
            leftMargin=2*cm,
            topMargin=2*cm,
            bottomMargin=2*cm,
        )

        styles = getSampleStyleSheet()

        # custom styles
        title_style = ParagraphStyle(
            "MediTitle",
            parent=styles["Title"],
            fontSize=22,
            textColor=colors.HexColor("#1e40af"),
            spaceAfter=6,
            alignment=TA_CENTER,
        )
        subtitle_style = ParagraphStyle(
            "MediSubtitle",
            parent=styles["Normal"],
            fontSize=11,
            textColor=colors.HexColor("#64748b"),
            spaceAfter=4,
            alignment=TA_CENTER,
        )
        heading_style = ParagraphStyle(
            "MediHeading",
            parent=styles["Heading2"],
            fontSize=13,
            textColor=colors.HexColor("#1e40af"),
            spaceBefore=14,
            spaceAfter=6,
            borderPad=4,
        )
        body_style = ParagraphStyle(
            "MediBody",
            parent=styles["BodyText"],
            fontSize=10,
            leading=16,
            textColor=colors.HexColor("#1e293b"),
        )
        disclaimer_style = ParagraphStyle(
            "Disclaimer",
            parent=styles["Normal"],
            fontSize=8,
            textColor=colors.HexColor("#94a3b8"),
            alignment=TA_CENTER,
        )

        elements = []

        # ── header ──
        elements.append(Spacer(1, 0.3*cm))
        elements.append(Paragraph("🩺 MediScan AI", title_style))
        elements.append(Paragraph("AI Medical Analysis Report", subtitle_style))
        elements.append(Paragraph(
            f"Generated: {datetime.now().strftime('%d %B %Y, %I:%M %p')}",
            subtitle_style,
        ))
        elements.append(Spacer(1, 0.4*cm))
        elements.append(HRFlowable(width="100%", thickness=2, color=colors.HexColor("#3b82f6")))
        elements.append(Spacer(1, 0.5*cm))

        # ── body: parse markdown-ish sections ──
        lines = summary.split("\n")
        for line in lines:
            line = line.strip()
            if not line:
                elements.append(Spacer(1, 0.2*cm))
                continue
            if line.startswith("## "):
                elements.append(Paragraph(line[3:], heading_style))
            elif line.startswith("# "):
                elements.append(Paragraph(line[2:], heading_style))
            elif line.startswith("- ") or line.startswith("* "):
                elements.append(Paragraph(f"• {line[2:]}", body_style))
            elif line.startswith("**") and line.endswith("**"):
                bold_style = ParagraphStyle("Bold", parent=body_style, fontName="Helvetica-Bold")
                elements.append(Paragraph(line.strip("*"), bold_style))
            else:
                # convert inline ** bold ** to ReportLab XML
                formatted = line.replace("**", "<b>", 1)
                count = 0
                while "**" in formatted:
                    formatted = formatted.replace("**", "</b>" if count % 2 == 0 else "<b>", 1)
                    count += 1
                try:
                    elements.append(Paragraph(formatted, body_style))
                except Exception:
                    elements.append(Paragraph(line, body_style))

        # ── footer ──
        elements.append(Spacer(1, 1*cm))
        elements.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#e2e8f0")))
        elements.append(Spacer(1, 0.3*cm))
        elements.append(Paragraph(
            "⚠️ DISCLAIMER: This AI-generated report is for informational purposes only and does not constitute "
            "medical advice, diagnosis, or treatment. Always consult a qualified healthcare professional. "
            "MediScan AI is not liable for any health decisions made based on this report.",
            disclaimer_style,
        ))

        doc.build(elements)
        return output_path

    except ImportError:
        # fallback: plain text file if ReportLab not installed
        txt_path = output_path.replace(".pdf", ".txt")
        with open(txt_path, "w") as f:
            f.write("MediScan AI — Medical Analysis Report\n")
            f.write("=" * 50 + "\n")
            f.write(f"Generated: {datetime.now().strftime('%d %B %Y, %I:%M %p')}\n\n")
            f.write(summary)
            f.write("\n\nDISCLAIMER: AI-generated — not a substitute for professional medical advice.\n")
        return txt_path