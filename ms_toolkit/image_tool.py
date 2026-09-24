"""Rasm fayllarini o'qish va OCR (matn ajratib olish) funksiyalari.

`get_image_info` faqat Pillow talab qiladi (mavjud dependency).
`read_image_text` OCR uchun `pytesseract` va tizimda **tesseract-ocr**
dasturi o'rnatilgan bo'lishini talab qiladi:
    Ubuntu/Debian: `apt-get install tesseract-ocr`
    pip: `pip install pytesseract`
"""

import os
from PIL import Image

try:
    import pytesseract
    _OCR_AVAILABLE = True
except ImportError:
    _OCR_AVAILABLE = False


def get_image_info(file_path: str) -> dict:
    """Rasm haqida asosiy ma'lumot: o'lcham, format, rang rejimi, hajmi."""
    if not os.path.exists(file_path):
        return {"error": f"Fayl topilmadi: {file_path}"}

    with Image.open(file_path) as img:
        return {
            "file_path": file_path,
            "width": img.width,
            "height": img.height,
            "format": img.format,
            "mode": img.mode,
            "size_bytes": os.path.getsize(file_path),
        }


def read_image_text(file_path: str, lang: str = "eng") -> dict:
    """Rasmdagi matnni OCR (Tesseract) orqali ajratib oladi.

    `lang` — Tesseract til kodi (masalan "eng", "rus", "uzb"; "+" bilan bir nechtasi:
    "eng+rus"). Kerakli til paketi tizimda o'rnatilgan bo'lishi kerak
    (`apt-get install tesseract-ocr-uzb` va h.k.).
    """
    if not _OCR_AVAILABLE:
        return {"error": "pytesseract o'rnatilmagan: pip install pytesseract"}
    if not os.path.exists(file_path):
        return {"error": f"Fayl topilmadi: {file_path}"}

    try:
        with Image.open(file_path) as img:
            text = pytesseract.image_to_string(img, lang=lang)
    except pytesseract.TesseractNotFoundError:
        return {
            "error": (
                "tesseract-ocr tizimda topilmadi. O'rnating: "
                "apt-get install tesseract-ocr"
            )
        }
    except Exception as e:
        return {"error": f"{type(e).__name__}: {e}"}

    return {"file_path": file_path, "text": text.strip(), "lang": lang}
