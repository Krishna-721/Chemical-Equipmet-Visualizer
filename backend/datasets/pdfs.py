from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch

def generate_report(buffer,dataset):
    c=canvas.Canvas(buffer,pagesize=A4)
    width,height=A4

    y=height-1

    c.setFont("Helvetica-Bold",14)
    c.drawString(1*inch, y, "Chemical Equipment Report")
    y-=0.5*inch

    c.setFont("Helvetica-Bold", 10)
    c.drawString(1 * inch, y, f"Filename: {dataset.filename}")
    y -= 0.3 * inch
    c.drawString(1 * inch, y, f"Uploaded at: {dataset.uploaded_at}")
    y -= 0.5 * inch

    summary=dataset.summary or {}

    c.setFont("Helvetica-Bold", 12)
    c.drawString(1 * inch, y, "Summary Statistics")
    y -= 0.3 * inch

    # Summary section
    c.setFont("Helvetica-Bold", 12)
    c.drawString(1 * inch, y, "Summary Statistics")
    y -= 0.3 * inch

    c.setFont("Helvetica", 10)
    c.drawString(1 * inch, y, f"Total equipment: {summary.get('total_equipment')}")
    y -= 0.25 * inch
    c.drawString(1 * inch, y, f"Valid rows: {summary.get('valid_rows')}")
    y -= 0.25 * inch
    c.drawString(1 * inch, y, f"Average flowrate: {summary.get('average_flowrate')}")
    y -= 0.25 * inch
    c.drawString(1 * inch, y, f"Average pressure: {summary.get('average_pressure')}")
    y -= 0.25 * inch
    c.drawString(1 * inch, y, f"Average temperature: {summary.get('average_temperature')}")
    y -= 0.5 * inch

    # Equipment distribution
    c.setFont("Helvetica-Bold", 12)
    c.drawString(1 * inch, y, "Equipment Type Distribution")
    y -= 0.3 * inch

    c.setFont("Helvetica", 10)
    distribution = summary.get("equipment_type_distribution", {})

    for eq_type, count in distribution.items():
        c.drawString(1.2 * inch, y, f"{eq_type}: {count}")
        y -= 0.25 * inch

    c.showPage()
    c.save()