from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
import os

def create_report(summary, findings):
    """Generate a PDF report."""
    try:
        output_path = "data\\test_outputs\\report.pdf"
        doc = SimpleDocTemplate(output_path, pagesize=letter)
        styles = getSampleStyleSheet()
        story = []
        
        story.append(Paragraph("Summary", styles['Heading1']))
        story.append(Paragraph(summary, styles['Normal']))
        story.append(Spacer(1, 12))
        
        story.append(Paragraph("Key Findings", styles['Heading1']))
        story.append(Paragraph(findings.replace('\n', '<br/>'), styles['Normal']))
        
        doc.build(story)
        return output_path
    except Exception as e:
        return f"Error generating report: {e}"