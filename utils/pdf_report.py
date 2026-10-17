import io
from datetime import datetime

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle


def generate_pdf_report(result_data):
    """Generate a downloadable PDF screening report."""
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, topMargin=0.6 * inch, bottomMargin=0.6 * inch)
    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "ReportTitle",
        parent=styles["Heading1"],
        fontSize=20,
        textColor=colors.HexColor("#4f46e5"),
        spaceAfter=16,
    )
    heading_style = ParagraphStyle(
        "SectionHeading",
        parent=styles["Heading2"],
        fontSize=13,
        textColor=colors.HexColor("#1e293b"),
        spaceBefore=12,
        spaceAfter=8,
    )
    body_style = ParagraphStyle(
        "Body",
        parent=styles["BodyText"],
        fontSize=10,
        leading=14,
        textColor=colors.HexColor("#334155"),
    )

    story = [
        Paragraph("Resume Screening Report", title_style),
        Paragraph(f"Generated on {datetime.now().strftime('%B %d, %Y at %I:%M %p')}", body_style),
        Spacer(1, 0.2 * inch),
    ]

    summary_rows = [
        ["Filename", result_data.get("filename", "N/A")],
        ["Predicted Category", result_data.get("prediction", "N/A")],
        ["Confidence Score", f"{result_data.get('confidence', 0)}%"],
        ["ATS Score", f"{result_data.get('ats_score', 0)} / 100 ({result_data.get('ats_rating', 'N/A')})"],
        ["Word Count", str(result_data.get("word_count", 0))],
        ["Character Count", str(result_data.get("char_count", 0))],
        ["Resume Length", result_data.get("resume_length", "N/A")],
        ["Upload Time", result_data.get("upload_time", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))],
    ]

    summary_table = Table(summary_rows, colWidths=[2.2 * inch, 4.3 * inch])
    summary_table.setStyle(
        TableStyle([
            ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#eef2ff")),
            ("TEXTCOLOR", (0, 0), (-1, -1), colors.HexColor("#1e293b")),
            ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
            ("FONTNAME", (1, 0), (1, -1), "Helvetica"),
            ("FONTSIZE", (0, 0), (-1, -1), 10),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("LEFTPADDING", (0, 0), (-1, -1), 8),
            ("RIGHTPADDING", (0, 0), (-1, -1), 8),
            ("TOPPADDING", (0, 0), (-1, -1), 6),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ])
    )
    story.extend([Paragraph("Screening Summary", heading_style), summary_table, Spacer(1, 0.15 * inch)])

    detected_skills = result_data.get("detected_skills", [])
    missing_skills = result_data.get("missing_skills", [])
    job_recommendations = result_data.get("job_recommendations", [])
    improvement_tips = result_data.get("improvement_tips", [])

    story.append(Paragraph("Detected Skills", heading_style))
    story.append(
        Paragraph(
            ", ".join(detected_skills) if detected_skills else "No technical skills detected.",
            body_style,
        )
    )

    story.append(Paragraph("Missing Skills", heading_style))
    story.append(
        Paragraph(
            ", ".join(missing_skills) if missing_skills else "No major skill gaps identified.",
            body_style,
        )
    )

    story.append(Paragraph("Recommended Job Roles (Top Fits)", heading_style))
    if job_recommendations:
        for rec in job_recommendations:
            role_text = f"<b>{rec['role']}</b> — <b>{rec['match_percentage']}% Match</b><br/>" \
                        f"<i>Reason:</i> {rec['explanation']}<br/>" \
                        f"<b>Matched Skills:</b> {', '.join(rec['matched_skills'])}<br/>"
            if rec.get("missing_skills"):
                role_text += f"<b>Missing Recommended Skills:</b> {', '.join(rec['missing_skills'])}"
            story.append(Paragraph(role_text, body_style))
            story.append(Spacer(1, 0.08 * inch))
    else:
        story.append(Paragraph("No job recommendations match your profile with at least 40% compatibility.", body_style))

    potential_career_paths = result_data.get("potential_career_paths", [])
    story.append(Paragraph("Potential Career Paths (Missing Core Skills)", heading_style))
    if potential_career_paths:
        for path in potential_career_paths:
            path_text = f"<b>{path['role']}</b> — <b>{path['match_percentage']}% Match</b><br/>" \
                        f"<b>Missing Core (Mandatory) Skills:</b> <font color='red'><b>{', '.join(path['missing_mandatory'])}</b></font>"
            story.append(Paragraph(path_text, body_style))
            story.append(Spacer(1, 0.08 * inch))
    else:
        story.append(Paragraph("No potential career paths flagged.", body_style))

    story.append(Paragraph("ATS Improvement Tips", heading_style))
    for tip in improvement_tips:
        story.append(Paragraph(f"• {tip}", body_style))

    doc.build(story)
    buffer.seek(0)
    return buffer
