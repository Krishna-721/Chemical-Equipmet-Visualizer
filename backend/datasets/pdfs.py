from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

def generate_report(buffer, dataset):
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    text = c.beginText(40, height - 40)
    text.setFont("Helvetica", 11)

    # Title
    text.setFont("Helvetica-Bold", 16)
    text.textLine("Chemical Equipment Report")
    text.textLine("")

    text.setFont("Helvetica", 11)
    text.textLine(f"Filename: {dataset.filename}")
    text.textLine(f"Uploaded at: {dataset.uploaded_at}")
    text.textLine("")

    summary = dataset.summary

    # Summary section
    text.setFont("Helvetica-Bold", 13)
    text.textLine("Summary Statistics")
    text.textLine("")

    text.setFont("Helvetica", 11)
    text.textLine(f"Total equipment: {summary['total_equipment']}")
    text.textLine(f"Valid rows: {summary['valid_rows']}")
    text.textLine(f"Average flowrate: {summary['average_flowrate']:.2f}")
    text.textLine(f"Average pressure: {summary['average_pressure']:.2f}")
    text.textLine(f"Average temperature: {summary['average_temperature']:.2f}")
    text.textLine("")

    # Validation section
    invalid = summary["total_equipment"] - summary["valid_rows"]
    ratio = (summary["valid_rows"] / summary["total_equipment"]) * 100

    text.setFont("Helvetica-Bold", 13)
    text.textLine("Data Validation Summary")
    text.textLine("")

    text.setFont("Helvetica", 11)
    text.textLine(f"Total rows: {summary['total_equipment']}")
    text.textLine(f"Valid rows: {summary['valid_rows']}")
    text.textLine(f"Invalid rows: {invalid}")
    text.textLine(f"Validity ratio: {ratio:.2f}%")
    text.textLine("")

    # Distribution
    text.setFont("Helvetica-Bold", 13)
    text.textLine("Equipment Type Distribution")
    text.textLine("")

    text.setFont("Helvetica", 11)
    for k, v in summary["equipment_type_distribution"].items():
        text.textLine(f"{k}: {v}")

    c.drawText(text)
    c.showPage()
    c.save()