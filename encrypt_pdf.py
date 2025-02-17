# encrypt_pdf.py
from PyPDF2 import PdfReader, PdfWriter

def encrypt_pdf(input_file, output_file, user_password, owner_password=None):
    """
    Encrypt a PDF file with password protection.
    
    Args:
        input_file (str): Path to input PDF file
        output_file (str): Path to save the encrypted PDF
        user_password (str): Password required to open and view the PDF
        owner_password (str, optional): Password for full permissions. If None, same as user_password
    """
    reader = PdfReader(input_file)
    writer = PdfWriter()

    # Add all pages to the writer
    for page in reader.pages:
        writer.add_page(page)
    
    # If no owner password is specified, use the user password
    owner_password = owner_password or user_password
    
    # Encrypt the PDF
    writer.encrypt(user_password=user_password, 
                  owner_password=owner_password,
                  use_128bit=True)
    
    # Save the encrypted PDF
    with open(output_file, 'wb') as output_pdf:
        writer.write(output_pdf)

def decrypt_pdf(input_file, output_file, password):
    """
    Decrypt a PDF file using the provided password.
    
    Args:
        input_file (str): Path to encrypted PDF file
        output_file (str): Path to save the decrypted PDF
        password (str): Password to decrypt the PDF (can be user or owner password)
    
    Raises:
        ValueError: If the password is incorrect
    """
    reader = PdfReader(input_file)
    writer = PdfWriter()
    
    # Check if PDF is encrypted
    if not reader.is_encrypted:
        raise ValueError("The PDF is not encrypted")

    # Try to decrypt with provided password
    try:
        reader.decrypt(password)
    except:
        raise ValueError("Incorrect password")

    # Add all pages to the writer
    for page in reader.pages:
        writer.add_page(page)
    
    # Save the decrypted PDF
    with open(output_file, 'wb') as output_pdf:
        writer.write(output_pdf)