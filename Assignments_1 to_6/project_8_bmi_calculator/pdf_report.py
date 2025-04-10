from fpdf import FPDF
import datetime

def generate_pdf_report(name, bmi, category, tip):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.set_text_color(44, 62, 80)
    pdf.cell(200, 10, txt="FitTrack - BMI Health Report", ln=True, align="C")
    pdf.ln(10)

    pdf.set_text_color(0, 0, 0)
    pdf.cell(200, 10, txt=f"Name: {name}", ln=True)
    pdf.cell(200, 10, txt=f"Date: {datetime.date.today()}", ln=True)
    pdf.cell(200, 10, txt=f"BMI: {bmi}", ln=True)
    pdf.cell(200, 10, txt=f"Category: {category}", ln=True)
    pdf.multi_cell(0, 10, txt=f"Health Tip: {tip}")

    filename = f"{name}_BMI_Report.pdf"
    pdf.output(filename)
