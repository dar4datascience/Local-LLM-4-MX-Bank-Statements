import pdfplumber
from pathlib import Path
from .ocr import extract_text_with_ocr


MIN_TEXT_THRESHOLD = 100


def extract_text_from_pdf(pdf_path: Path) -> str:
    """
    Extract text from PDF. Try pdfplumber first, fall back to OCR if insufficient text.
    """
    text_parts = []
    
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text_parts.append(page_text)
        
        combined_text = "\n".join(text_parts)
        
        if len(combined_text.strip()) < MIN_TEXT_THRESHOLD:
            print(f"  → Insufficient text ({len(combined_text)} chars), falling back to OCR")
            return extract_text_with_ocr(pdf_path)
        
        return combined_text
    
    except Exception as e:
        print(f"  → pdfplumber failed: {e}, trying OCR")
        return extract_text_with_ocr(pdf_path)
