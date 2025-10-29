from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import datetime
import os

def generate_pdf_report(patient_name, age, exercise_name, performance_score, feedback_text):
    """
    Generates a simple PDF report for a patient's exercise performance.
    Saves it as 'report_<patient_name>.pdf' inside the 'data/reports/' folder.
    """

    # Create folder if it doesn't exist
    os.makedirs("data/reports", exist_ok=True)

    # File path
    file_name = f"data/reports/report_{patient_name.replace(' ', '_')}.pdf"

    # Create a new PDF
    c = canvas.Canvas(file_name, pagesize=letter)
    width, height = letter

    # Title
    c.setFont("Helvetica-Bold", 20)
    c.drawString(200, 750, "MediMotion Exercise Report")

    # Line
    c.line(50, 740, 550, 740)

    # Patient Info
    c.setFont("Helvetica", 12)
    c.drawString(50, 710, f"Name: {patient_name}")
    c.drawString(50, 690, f"Age: {age}")
    c.drawString(50, 670, f"Exercise: {exercise_name}")
    c.drawString(50, 650, f"Performance Score: {performance_score}")
    c.drawString(50, 630, f"Feedback: {feedback_text}")

    # Footer with timestamp
    c.setFont("Helvetica-Oblique", 10)
    c.drawString(50, 580, f"Generated on: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    c.save()

    return file_name
