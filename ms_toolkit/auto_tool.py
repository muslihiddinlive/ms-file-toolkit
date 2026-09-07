"""Fayl turini avtomatik aniqlab, mos reader'ni chaqiradigan yordamchi modul."""

import os

_EXT_MAP = {
    ".docx": "docx",
    ".xlsx": "xlsx",
    ".pptx": "pptx",
    ".pdf": "pdf",
    ".doc": "legacy",
    ".xls": "legacy",
    ".ppt": "legacy",
}


def get_file_info(file_path: str) -> dict:
    """Fayl haqida asosiy ma'lumot: mavjudmi, kengaytmasi, hajmi, aniqlangan turi."""
    ext = os.path.splitext(file_path)[1].lower()
    exists = os.path.exists(file_path)
    return {
        "file_path": file_path,
        "exists": exists,
        "extension": ext,
        "detected_type": _EXT_MAP.get(ext, "unknown"),
        "size_bytes": os.path.getsize(file_path) if exists else None,
    }


def read_any_file(file_path: str) -> dict:
    """Fayl kengaytmasiga qarab mos o'qish funksiyasini avtomatik tanlab chaqiradi.

    Foydalanuvchi/AI fayl turini oldindan bilmasa yoki noaniq bo'lsa foydali —
    .docx/.xlsx/.pptx va eski .doc/.xls/.ppt formatlarni avtomatik aniqlaydi.
    """
    from .docx_tool import read_docx_text
    from .xlsx_tool import read_xlsx_data
    from .pptx_tool import read_pptx_text
    from .pdf_tool import read_pdf_text
    from .legacy_tool import read_legacy_file

    if not os.path.exists(file_path):
        return {"error": f"Fayl topilmadi: {file_path}"}

    ext = os.path.splitext(file_path)[1].lower()
    kind = _EXT_MAP.get(ext)

    if kind == "docx":
        result = read_docx_text(file_path)
    elif kind == "xlsx":
        result = read_xlsx_data(file_path)
    elif kind == "pptx":
        result = read_pptx_text(file_path)
    elif kind == "pdf":
        result = read_pdf_text(file_path)
    elif kind == "legacy":
        result = read_legacy_file(file_path)
    else:
        return {"error": f"Qo'llab-quvvatlanmaydigan yoki noma'lum fayl turi: {ext or '(kengaytmasiz)'}"}

    result["detected_type"] = kind
    return result
