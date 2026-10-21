
import fitz


def extract_text_from_pdf(pdf_path):
    """Extract text from a PDF and preserve page numbers."""
    extracted_pages = []

    with fitz.open(pdf_path) as pdf:
        for page_number, page in enumerate(pdf, start=1):
            text = page.get_text("text")

            if text.strip():
                extracted_pages.append({
                    "page": page_number,
                    "text": text.strip()
                })

    return extracted_pages
