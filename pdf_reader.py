def extract_text_from_pdf(pdf_path: str) -> str:
    """
    Extract text from a PDF medical document.
    Tries PyPDF2 first, then pdfplumber for better table extraction.
    """
    text = ""

    # ── Try pdfplumber (better for tables/columns) ──
    try:
        import pdfplumber
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        if text.strip():
            return text.strip()
    except ImportError:
        pass
    except Exception:
        pass

    # ── Fallback: PyPDF2 ──
    try:
        from PyPDF2 import PdfReader
        reader = PdfReader(pdf_path)
        for page in reader.pages:
            extracted = page.extract_text()
            if extracted:
                text += extracted + "\n"
        if text.strip():
            return text.strip()
    except ImportError:
        pass
    except Exception as e:
        return f"PDF extraction error: {e}"

    return text.strip() or "(Could not extract text from PDF — the file may be scanned/image-based. Try uploading as JPG/PNG.)"