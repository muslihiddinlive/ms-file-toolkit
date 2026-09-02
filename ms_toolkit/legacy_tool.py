"""
Eski Microsoft formatlarini (.doc, .xls, .ppt) LibreOffice (soffice) yordamida
yangi formatga (.docx, .xlsx, .pptx) konvertatsiya qilib, keyin mavjud
docx_tool / xlsx_tool / pptx_tool funksiyalari bilan o'qish uchun modul.

Talab: tizimda `soffice` (LibreOffice) o'rnatilgan bo'lishi kerak.
"""

import os
import subprocess
import tempfile
import uuid

_LEGACY_MAP = {
    ".doc": "docx",
    ".xls": "xlsx",
    ".ppt": "pptx",
}


def is_legacy_format(file_path: str) -> bool:
    """Fayl eski (.doc/.xls/.ppt) formatdami — shuni tekshiradi."""
    ext = os.path.splitext(file_path)[1].lower()
    return ext in _LEGACY_MAP


def convert_legacy_file(file_path: str, timeout: int = 60) -> str:
    """Eski formatdagi faylni vaqtinchalik papkada yangi formatga o'giradi.

    Qaytaradi: yangi (.docx/.xlsx/.pptx) faylning to'liq yo'li.
    Chaqiruvchi tugagach vaqtinchalik faylni o'zi tozalashi kerak (yoki
    read_legacy_file wrapper'idan foydalaning — u avtomatik tozalaydi).
    """
    ext = os.path.splitext(file_path)[1].lower()
    if ext not in _LEGACY_MAP:
        raise ValueError(f"Qo'llab-quvvatlanmaydigan eski format: {ext}")

    target_format = _LEGACY_MAP[ext]
    out_dir = os.path.join(tempfile.gettempdir(), f"ms_toolkit_legacy_{uuid.uuid4().hex}")
    os.makedirs(out_dir, exist_ok=True)

    result = subprocess.run(
        [
            "soffice",
            "--headless",
            "--convert-to",
            target_format,
            "--outdir",
            out_dir,
            file_path,
        ],
        capture_output=True,
        text=True,
        timeout=timeout,
    )

    if result.returncode != 0:
        raise RuntimeError(f"LibreOffice konvertatsiya xatosi: {result.stderr or result.stdout}")

    base_name = os.path.splitext(os.path.basename(file_path))[0]
    converted_path = os.path.join(out_dir, f"{base_name}.{target_format}")

    if not os.path.exists(converted_path):
        raise RuntimeError(
            f"Konvertatsiya qilingan fayl topilmadi: {converted_path} (chiqish: {result.stdout})"
        )

    return converted_path


def read_legacy_file(file_path: str) -> dict:
    """Eski (.doc/.xls/.ppt) faylni avtomatik aniqlab, mos reader bilan o'qiydi.

    Ichki ravishda yangi formatga o'giradi, tegishli o'qish funksiyasini
    chaqiradi va natijaga original fayl yo'li va formatni qo'shib qaytaradi.
    """
    from .docx_tool import read_docx_text
    from .xlsx_tool import read_xlsx_data
    from .pptx_tool import read_pptx_text

    ext = os.path.splitext(file_path)[1].lower()
    if ext not in _LEGACY_MAP:
        return {"error": f"Qo'llab-quvvatlanmaydigan eski format: {ext}"}

    if not os.path.exists(file_path):
        return {"error": f"Fayl topilmadi: {file_path}"}

    converted_path = None
    try:
        converted_path = convert_legacy_file(file_path)
        target_format = _LEGACY_MAP[ext]

        if target_format == "docx":
            result = read_docx_text(converted_path)
        elif target_format == "xlsx":
            result = read_xlsx_data(converted_path)
        else:
            result = read_pptx_text(converted_path)

        result["original_file"] = file_path
        result["original_format"] = ext
        return result
    except subprocess.TimeoutExpired:
        return {"error": "Konvertatsiya vaqti tugadi (timeout)"}
    except Exception as e:
        return {"error": f"{type(e).__name__}: {e}"}
    finally:
        if converted_path and os.path.exists(converted_path):
            out_dir = os.path.dirname(converted_path)
            try:
                os.remove(converted_path)
                os.rmdir(out_dir)
            except OSError:
                pass
