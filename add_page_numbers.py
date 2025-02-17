from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import io

def add_page_numbers(input_pdf, output_pdf):
    reader = PdfReader(input_pdf)
    writer = PdfWriter()

    for page_num in range(len(reader.pages)):
        packet = io.BytesIO()
        can = canvas.Canvas(packet, pagesize=letter)
        can.setFont("Helvetica", 12)
        can.drawString(550, 20, str(page_num + 1))  # Position of the page number
        can.save()

        packet.seek(0)
        new_pdf = PdfReader(packet)
        page = reader.pages[page_num]
        page.merge_page(new_pdf.pages[0])
        writer.add_page(page)

    with open(output_pdf, "wb") as output_file:
        writer.write(output_file)

if __name__ == "__main__":
    input_pdf = "input.pdf"  # Replace with your PDF file
    output_pdf = "output_numbered.pdf"
    add_page_numbers(input_pdf, output_pdf)
    print("Page numbers added successfully!")