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


def crop_image(file_path: str, left: int, top: int, right: int, bottom: int, save_as: str = None) -> dict:
    """Rasmni berilgan to'rtburchak (left, top, right, bottom) bo'yicha kesadi.

    Koordinatalar piksellarda, yuqori chap burchak (0, 0) dan boshlanadi.
    save_as berilmasa, asl faylning ustiga yoziladi.
    """
    if not os.path.exists(file_path):
        return {"error": f"Fayl topilmadi: {file_path}"}

    with Image.open(file_path) as img:
        w, h = img.size
        if not (0 <= left < right <= w and 0 <= top < bottom <= h):
            return {
                "error": (
                    f"Noto'g'ri crop chegaralari: rasm o'lchami {w}x{h}, "
                    f"berilgan ({left},{top},{right},{bottom})"
                )
            }
        cropped = img.crop((left, top, right, bottom))
        out_path = save_as or file_path
        os.makedirs(os.path.dirname(os.path.abspath(out_path)) or ".", exist_ok=True)
        cropped.save(out_path)

    return {
        "file_path": out_path,
        "status": "cropped",
        "width": right - left,
        "height": bottom - top,
    }


def resize_image(file_path: str, width: int = None, height: int = None, save_as: str = None, keep_aspect_ratio: bool = True) -> dict:
    """Rasm o'lchamini o'zgartiradi (image_writer.convert_image'dan farqli o'laroq, formatni o'zgartirmaydi).

    width yoki height dan faqat bittasi berilsa va keep_aspect_ratio=True bo'lsa,
    ikkinchisi asl nisbatga qarab avtomatik hisoblanadi. Ikkalasi ham berilsa va
    keep_aspect_ratio=True bo'lsa, rasm shu ikkalasiga sig'adigan tarzda (aspect
    ratio buzilmasdan) kichraytiriladi.
    """
    if not os.path.exists(file_path):
        return {"error": f"Fayl topilmadi: {file_path}"}
    if width is None and height is None:
        return {"error": "width yoki height dan kamida bittasi berilishi kerak"}

    with Image.open(file_path) as img:
        orig_w, orig_h = img.size

        if keep_aspect_ratio:
            if width and height:
                img.thumbnail((width, height), Image.LANCZOS)
                new_w, new_h = img.size
            elif width:
                new_w = width
                new_h = round(orig_h * (width / orig_w))
                img = img.resize((new_w, new_h), Image.LANCZOS)
            else:
                new_h = height
                new_w = round(orig_w * (height / orig_h))
                img = img.resize((new_w, new_h), Image.LANCZOS)
        else:
            new_w = width or orig_w
            new_h = height or orig_h
            img = img.resize((new_w, new_h), Image.LANCZOS)

        out_path = save_as or file_path
        os.makedirs(os.path.dirname(os.path.abspath(out_path)) or ".", exist_ok=True)
        img.save(out_path)

    return {"file_path": out_path, "status": "resized", "width": new_w, "height": new_h}


def rotate_image(file_path: str, degrees: float, save_as: str = None, expand: bool = True) -> dict:
    """Rasmni soat yo'nalishiga qarshi (counter-clockwise) berilgan gradusga aylantiradi."""
    if not os.path.exists(file_path):
        return {"error": f"Fayl topilmadi: {file_path}"}

    with Image.open(file_path) as img:
        rotated = img.rotate(degrees, expand=expand)
        out_path = save_as or file_path
        os.makedirs(os.path.dirname(os.path.abspath(out_path)) or ".", exist_ok=True)
        rotated.save(out_path)

    return {"file_path": out_path, "status": "rotated", "degrees": degrees, "width": rotated.width, "height": rotated.height}


def create_image(width: int, height: int, output_path: str, color: str = "#FFFFFF") -> dict:
    """Bo'sh (bir rangli) yangi rasm yaratadi — masalan fon yoki placeholder sifatida.

    color: "#RRGGBB" hex format yoki "red", "blue" kabi nom.
    """
    ext = os.path.splitext(output_path)[1].lower().lstrip(".")
    fmt_map = {"jpg": "JPEG", "jpeg": "JPEG", "png": "PNG", "webp": "WEBP", "bmp": "BMP", "gif": "GIF"}
    target_format = fmt_map.get(ext, "PNG")

    mode = "RGB" if target_format == "JPEG" else "RGBA"
    img = Image.new(mode, (width, height), color)
    os.makedirs(os.path.dirname(os.path.abspath(output_path)) or ".", exist_ok=True)
    img.save(output_path, format=target_format)

    return {"file_path": output_path, "status": "created", "width": width, "height": height}
