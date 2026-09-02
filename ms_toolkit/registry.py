"""
Tool nomini haqiqiy Python funksiyasiga bog'laydigan registry.

AI (Claude/GPT) function-calling orqali qaytargan tool_name + inputlarni
shu yerdagi dispatch() funksiyasiga uzatasiz, u kerakli faylni tahlil qilib beradi.
"""

from .docx_tool import read_docx_text, read_docx_tables, get_docx_metadata
from .xlsx_tool import get_xlsx_sheet_names, read_xlsx_data, get_xlsx_summary
from .pptx_tool import read_pptx_text, get_pptx_slide_count, extract_pptx_notes

REGISTRY = {
    "read_docx_text": read_docx_text,
    "read_docx_tables": read_docx_tables,
    "get_docx_metadata": get_docx_metadata,
    "get_xlsx_sheet_names": get_xlsx_sheet_names,
    "read_xlsx_data": read_xlsx_data,
    "get_xlsx_summary": get_xlsx_summary,
    "read_pptx_text": read_pptx_text,
    "get_pptx_slide_count": get_pptx_slide_count,
    "extract_pptx_notes": extract_pptx_notes,
}


def dispatch(tool_name: str, tool_input: dict) -> dict:
    """AI tomonidan chaqirilgan tool_name'ga mos funksiyani ishga tushiradi.

    Xato bo'lsa exception ko'tarmaydi — {"error": "..."} qaytaradi,
    shunda AI xatoni ko'rib, foydalanuvchiga tushuntira oladi.
    """
    func = REGISTRY.get(tool_name)
    if func is None:
        return {"error": f"Noma'lum tool: {tool_name}"}
    try:
        return func(**tool_input)
    except FileNotFoundError:
        return {"error": f"Fayl topilmadi: {tool_input.get('file_path')}"}
    except Exception as e:
        return {"error": f"{type(e).__name__}: {e}"}
