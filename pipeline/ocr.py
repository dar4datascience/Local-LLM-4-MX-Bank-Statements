import pytesseract
from PIL import Image
from pdf2image import convert_from_path
from pathlib import Path


def extract_text_with_ocr(pdf_path: Path) -> str:
    """
    Extract text from image-based PDF using Tesseract OCR.
    """
    try:
        images = convert_from_path(pdf_path)
        text_parts = []
        
        for i, image in enumerate(images):
            print(f"    OCR page {i+1}/{len(images)}")
            page_text = pytesseract.image_to_string(image, lang='spa')
            text_parts.append(page_text)
        
        return "\n".join(text_parts)
    
    except Exception as e:
        print(f"  → OCR failed: {e}")
        return ""
