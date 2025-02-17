# add_page_numbers.py
from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import io

def add_page_numbers(input_pdf, output_pdf, start_number=1, position="bottom-right", font_size=12):
    """
    Add page numbers to a PDF file.
    
    Args:
        input_pdf (str): Path to input PDF file
        output_pdf (str): Path to save the numbered PDF
        start_number (int): Starting page number (default: 1)
        position (str): Position of page numbers ('bottom-right', 'bottom-center', 'bottom-left')
        font_size (int): Font size for page numbers (default: 12)
    """
    reader = PdfReader(input_pdf)
    writer = PdfWriter()
    
    # Get page size from first page
    first_page = reader.pages[0]
    page_width = float(first_page.mediabox.width)
    page_height = float(first_page.mediabox.height)
    
    # Define positions
    positions = {
        "bottom-right": (page_width - 50, 30),
        "bottom-center": (page_width/2, 30),
        "bottom-left": (50, 30)
    }
    
    if position not in positions:
        position = "bottom-right"
    
    x, y = positions[position]
    
    for page_num in range(len(reader.pages)):
        # Create page number overlay
        packet = io.BytesIO()
        can = canvas.Canvas(packet, pagesize=(page_width, page_height))
        can.setFont("Helvetica", font_size)
        
        # Draw page number
        number = str(page_num + start_number)
        can.drawString(x, y, number)
        can.save()
        
        # Merge number with page
        packet.seek(0)
        number_pdf = PdfReader(packet)
        page = reader.pages[page_num]
        page.merge_page(number_pdf.pages[0])
        writer.add_page(page)
    
    # Save the numbered PDF
    with open(output_pdf, "wb") as output_file:
        writer.write(output_file)