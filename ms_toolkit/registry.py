"""
Tool nomini haqiqiy Python funksiyasiga bog'laydigan registry.

AI (Claude/GPT) function-calling orqali qaytargan tool_name + inputlarni
shu yerdagi dispatch() funksiyasiga uzatasiz, u kerakli faylni o'qiydi/yozadi.

Xavfsizlik: `file_path` (va `image_path`) qiymatlari dispatch() ichida
security.resolve_safe_path() orqali tekshiriladi. MS_TOOLKIT_BASE_DIR muhit
o'zgaruvchisini o'rnatsangiz, barcha amallar faqat o'sha papka bilan cheklanadi.
"""

from .docx_tool import read_docx_text, read_docx_tables, get_docx_metadata
from .docx_writer import (
    create_docx, append_docx_text, replace_docx_text,
    add_docx_heading, add_docx_image, add_docx_page_break,
)
from .xlsx_tool import get_xlsx_sheet_names, read_xlsx_data, get_xlsx_summary
from .xlsx_writer import (
    create_xlsx, add_xlsx_sheet, append_xlsx_rows,
    set_xlsx_formula, format_xlsx_cells, freeze_xlsx_panes,
)
from .pptx_tool import read_pptx_text, get_pptx_slide_count, extract_pptx_notes
from .pptx_writer import (
    create_pptx, add_pptx_slide, add_pptx_image, set_pptx_background_color,
)
from .legacy_tool import read_legacy_file
from .auto_tool import read_any_file, get_file_info
from .security import resolve_safe_path, UnsafePathError

REGISTRY = {
    # DOCX - o'qish
    "read_docx_text": read_docx_text,
    "read_docx_tables": read_docx_tables,
    "get_docx_metadata": get_docx_metadata,
    # DOCX - yozish
    "create_docx": create_docx,
    "append_docx_text": append_docx_text,
    "replace_docx_text": replace_docx_text,
    "add_docx_heading": add_docx_heading,
    "add_docx_image": add_docx_image,
    "add_docx_page_break": add_docx_page_break,
    # XLSX - o'qish
    "get_xlsx_sheet_names": get_xlsx_sheet_names,
    "read_xlsx_data": read_xlsx_data,
    "get_xlsx_summary": get_xlsx_summary,
    # XLSX - yozish
    "create_xlsx": create_xlsx,
    "add_xlsx_sheet": add_xlsx_sheet,
    "append_xlsx_rows": append_xlsx_rows,
    "set_xlsx_formula": set_xlsx_formula,
    "format_xlsx_cells": format_xlsx_cells,
    "freeze_xlsx_panes": freeze_xlsx_panes,
    # PPTX - o'qish
    "read_pptx_text": read_pptx_text,
    "get_pptx_slide_count": get_pptx_slide_count,
    "extract_pptx_notes": extract_pptx_notes,
    # PPTX - yozish
    "create_pptx": create_pptx,
    "add_pptx_slide": add_pptx_slide,
    "add_pptx_image": add_pptx_image,
    "set_pptx_background_color": set_pptx_background_color,
    # Eski formatlar
    "read_legacy_file": read_legacy_file,
    # Auto-detect
    "read_any_file": read_any_file,
    "get_file_info": get_file_info,
}

# file_path/image_path qabul qiladigan tool'lar uchun xavfsizlik tekshiruvi
# qo'llaniladigan parametr nomlari
_PATH_PARAMS = ("file_path", "image_path", "save_as")


def dispatch(tool_name: str, tool_input: dict, base_dir: str = None) -> dict:
    """AI tomonidan chaqirilgan tool_name'ga mos funksiyani ishga tushiradi.

    Har bir fayl-yo'li parametri avval security.resolve_safe_path() orqali
    tekshiriladi (path traversal himoyasi). base_dir berilsa yoki
    MS_TOOLKIT_BASE_DIR muhit o'zgaruvchisi o'rnatilgan bo'lsa, faqat o'sha
    papka ichidagi fayllarga ruxsat beriladi.

    Xato bo'lsa exception ko'tarmaydi — {"error": "..."} qaytaradi,
    shunda AI xatoni ko'rib, foydalanuvchiga tushuntira oladi.
    """
    func = REGISTRY.get(tool_name)
    if func is None:
        return {"error": f"Noma'lum tool: {tool_name}"}

    safe_input = dict(tool_input)
    try:
        for param in _PATH_PARAMS:
            if param in safe_input and safe_input[param]:
                safe_input[param] = resolve_safe_path(safe_input[param], base_dir=base_dir)
    except UnsafePathError as e:
        return {"error": f"Xavfsizlik xatosi: {e}"}

    try:
        return func(**safe_input)
    except FileNotFoundError:
        return {"error": f"Fayl topilmadi: {safe_input.get('file_path')}"}
    except Exception as e:
        return {"error": f"{type(e).__name__}: {e}"}
