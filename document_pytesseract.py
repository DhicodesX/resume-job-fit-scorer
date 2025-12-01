# document_pytesseract.py

import pytesseract
from PIL import Image
import os

# Optional: import pdf2image if installed
try:
    from pdf2image import convert_from_path
    PDF_SUPPORT = True
except ImportError:
    PDF_SUPPORT = False

# Set path to Tesseract executable
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def extract_text(file_path):
    """
    Extract text from an image or PDF file.
    Works on Windows. Requires Poppler installed for PDFs.
    """
    ext = os.path.splitext(file_path)[1].lower()  # Get file extension
    text = ""

    try:
        if ext in ['.jpg', '.jpeg', '.png']:
            # Image file
            img = Image.open(file_path)
            text = pytesseract.image_to_string(img)

        elif ext == '.pdf' and PDF_SUPPORT:
            # PDF file
            pages = convert_from_path(file_path)  # Poppler must be in PATH
            for page in pages:
                text += pytesseract.image_to_string(page)

        else:
            print(f"Unsupported file type: {ext} or pdf2image not installed.")
    
    except Exception as e:
        print(f"Error extracting text: {e}")
    
    return text

