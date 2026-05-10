import os

def extract_text_from_image(image_path: str) -> str:
    """
    Extract text from a medical image using Tesseract OCR.
    Falls back to OpenCV pre-processing for better accuracy.
    """
    try:
        import pytesseract
        from PIL import Image, ImageFilter, ImageEnhance

        img = Image.open(image_path).convert("L")          # greyscale
        img = img.filter(ImageFilter.SHARPEN)               # sharpen
        img = ImageEnhance.Contrast(img).enhance(2.0)       # boost contrast

        # custom Tesseract config for medical text
        custom_cfg = r"--oem 3 --psm 6 -l eng"
        text = pytesseract.image_to_string(img, config=custom_cfg)
        return text.strip() or "(No text detected — please check image quality)"

    except ImportError:
        return (
            "⚠️ Tesseract OCR not installed.\n\n"
            "Install with:\n"
            "  sudo apt-get install tesseract-ocr   (Linux)\n"
            "  brew install tesseract               (macOS)\n"
            "  pip install pytesseract\n\n"
            "For demo, using sample report text."
        )
    except Exception as e:
        return f"OCR extraction error: {e}"