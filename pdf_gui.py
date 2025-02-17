# pdf_gui.py
import tkinter as tk
from tkinter import filedialog, messagebox
from merge_pdfs import merge_pdfs
from split_pdfs import split_pdf
from extract_text import extract_text
from rotate_pdfs import rotate_pdf
from add_watermark import add_watermark
from reorder_pdf import reorder_pdf
from encrypt_pdf import encrypt_pdf, decrypt_pdf

def browse_files(multiple=False):
    if multiple:
        files = filedialog.askopenfilenames(filetypes=[("PDF Files", "*.pdf")])
        return list(files)
    else:
        file = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
        return file

def save_file():
    file = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF Files", "*.pdf")])
    return file

def merge_action():
    files = browse_files(multiple=True)
    if not files:
        return
    output_file = save_file()
    if not output_file:
        return
    merge_pdfs(files, output_file)
    messagebox.showinfo("Success", f"Merged PDF saved to {output_file}")

def split_action():
    input_file = browse_files()
    if not input_file:
        return
    start_page = int(start_page_entry.get())
    end_page = int(end_page_entry.get())
    output_file = save_file()
    if not output_file:
        return
    split_pdf(input_file, start_page, end_page, output_file)
    messagebox.showinfo("Success", f"Split PDF saved to {output_file}")

def extract_text_action():
    input_file = browse_files()
    if not input_file:
        return
    text = extract_text(input_file)
    messagebox.showinfo("Extracted Text", text)

def rotate_action():
    input_file = browse_files()
    if not input_file:
        return
    angle = int(rotation_entry.get())
    output_file = save_file()
    if not output_file:
        return
    rotate_pdf(input_file, output_file, angle)
    messagebox.showinfo("Success", f"Rotated PDF saved to {output_file}")

def watermark_action():
    input_file = browse_files()
    if not input_file:
        return
    watermark_file = browse_files()
    if not watermark_file:
        return
    output_file = save_file()
    if not output_file:
        return
    add_watermark(input_file, watermark_file, output_file)
    messagebox.showinfo("Success", f"Watermarked PDF saved to {output_file}")

def reorder_action():
    input_file = browse_files()
    if not input_file:
        return
    
    # Create a dialog for entering page order
    dialog = tk.Toplevel(root)
    dialog.title("Enter Page Order")
    dialog.geometry("300x150")
    
    tk.Label(dialog, text="Enter page numbers separated by commas\n(e.g., 3,1,2):").pack(pady=10)
    order_entry = tk.Entry(dialog, width=30)
    order_entry.pack(pady=10)
    
    def process():
        try:
            page_order = [int(x.strip()) for x in order_entry.get().split(',')]
            output_file = save_file()
            if output_file:
                reorder_pdf(input_file, page_order, output_file)
                messagebox.showinfo("Success", f"Reordered PDF saved to {output_file}")
            dialog.destroy()
        except ValueError as e:
            messagebox.showerror("Error", str(e))
    
    tk.Button(dialog, text="Reorder", command=process).pack(pady=10)

def encrypt_action():
    input_file = browse_files()
    if not input_file:
        return
    
    # Create a dialog for entering passwords
    dialog = tk.Toplevel(root)
    dialog.title("PDF Encryption")
    dialog.geometry("300x200")
    
    tk.Label(dialog, text="User Password:").pack(pady=5)
    user_pass = tk.Entry(dialog, width=30, show="*")
    user_pass.pack(pady=5)
    
    tk.Label(dialog, text="Owner Password (optional):").pack(pady=5)
    owner_pass = tk.Entry(dialog, width=30, show="*")
    owner_pass.pack(pady=5)
    
    def process():
        output_file = save_file()
        if output_file:
            owner_password = owner_pass.get() if owner_pass.get() else None
            encrypt_pdf(input_file, output_file, user_pass.get(), owner_password)
            messagebox.showinfo("Success", f"Encrypted PDF saved to {output_file}")
        dialog.destroy()
    
    tk.Button(dialog, text="Encrypt", command=process).pack(pady=10)

def decrypt_action():
    input_file = browse_files()
    if not input_file:
        return
    
    # Create a dialog for entering password
    dialog = tk.Toplevel(root)
    dialog.title("PDF Decryption")
    dialog.geometry("300x150")
    
    tk.Label(dialog, text="Enter Password:").pack(pady=5)
    password = tk.Entry(dialog, width=30, show="*")
    password.pack(pady=5)
    
    def process():
        try:
            output_file = save_file()
            if output_file:
                decrypt_pdf(input_file, output_file, password.get())
                messagebox.showinfo("Success", f"Decrypted PDF saved to {output_file}")
                dialog.destroy()
        except ValueError as e:
            messagebox.showerror("Error", str(e))
    
    tk.Button(dialog, text="Decrypt", command=process).pack(pady=10)

# Create the GUI
root = tk.Tk()
root.title("PDF Manipulator")
root.geometry("400x700")  # Increased height to accommodate new buttons

# Buttons
tk.Button(root, text="Merge PDFs", command=merge_action, width=20).pack(pady=10)
tk.Button(root, text="Split PDF", command=split_action, width=20).pack(pady=10)

tk.Label(root, text="Start Page:").pack()
start_page_entry = tk.Entry(root, width=10)
start_page_entry.pack()

tk.Label(root, text="End Page:").pack()
end_page_entry = tk.Entry(root, width=10)
end_page_entry.pack()

tk.Button(root, text="Extract Text", command=extract_text_action, width=20).pack(pady=10)

tk.Label(root, text="Rotation Angle:").pack()
rotation_entry = tk.Entry(root, width=10)
rotation_entry.pack()

tk.Button(root, text="Rotate PDF", command=rotate_action, width=20).pack(pady=10)
tk.Button(root, text="Add Watermark", command=watermark_action, width=20).pack(pady=10)
tk.Button(root, text="Reorder Pages", command=reorder_action, width=20).pack(pady=10)
tk.Button(root, text="Encrypt PDF", command=encrypt_action, width=20).pack(pady=10)
tk.Button(root, text="Decrypt PDF", command=decrypt_action, width=20).pack(pady=10)

root.mainloop()