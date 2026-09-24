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
    set_xlsx_formula, format_xlsx_cells, freeze_xlsx_panes, add_xlsx_chart,
)
from .pptx_tool import read_pptx_text, get_pptx_slide_count, extract_pptx_notes
from .pptx_writer import (
    create_pptx, add_pptx_slide, add_pptx_image, set_pptx_background_color, add_pptx_chart,
)
from .pdf_tool import read_pdf_text, read_pdf_tables, get_pdf_metadata
from .pdf_writer import create_pdf, merge_pdfs, split_pdf
from .legacy_tool import read_legacy_file
from .auto_tool import read_any_file, get_file_info
from .csv_tool import read_csv_data, get_csv_summary
from .csv_writer import create_csv, append_csv_rows
from .opendoc_tool import (
    read_odt_text, get_ods_sheet_names, read_ods_data,
    read_odp_text, get_odp_slide_count,
)
from .opendoc_writer import create_odt, create_ods, create_odp
from .image_tool import get_image_info, read_image_text, crop_image, resize_image, rotate_image, create_image
from .image_writer import convert_image, create_thumbnail
from .archive_tool import list_archive_contents, read_archive_file
from .archive_writer import create_archive, extract_archive
from .convert_tool import (
    convert_docx_to_pdf, convert_pptx_to_pdf, convert_xlsx_to_pdf,
    convert_pdf_to_images, convert_pptx_to_images, convert_xlsx_to_csv,
)
from .code_tool import (
    read_code_file, read_code_lines, create_code_file, append_code_text,
    replace_code_text, insert_code_lines, delete_code_lines,
    list_directory_files, search_in_files,
)
from .web_tool import (
    download_file, fetch_url_text, scrape_page_text,
    extract_page_links, extract_page_images,
    search_web, get_known_changelog_url,
)
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
    "add_xlsx_chart": add_xlsx_chart,
    # PPTX - o'qish
    "read_pptx_text": read_pptx_text,
    "get_pptx_slide_count": get_pptx_slide_count,
    "extract_pptx_notes": extract_pptx_notes,
    # PPTX - yozish
    "create_pptx": create_pptx,
    "add_pptx_slide": add_pptx_slide,
    "add_pptx_image": add_pptx_image,
    "set_pptx_background_color": set_pptx_background_color,
    "add_pptx_chart": add_pptx_chart,
    # PDF - o'qish
    "read_pdf_text": read_pdf_text,
    "read_pdf_tables": read_pdf_tables,
    "get_pdf_metadata": get_pdf_metadata,
    # PDF - yozish
    "create_pdf": create_pdf,
    "merge_pdfs": merge_pdfs,
    "split_pdf": split_pdf,
    # Eski formatlar
    "read_legacy_file": read_legacy_file,
    # Auto-detect
    "read_any_file": read_any_file,
    "get_file_info": get_file_info,
    # CSV
    "read_csv_data": read_csv_data,
    "get_csv_summary": get_csv_summary,
    "create_csv": create_csv,
    "append_csv_rows": append_csv_rows,
    # OpenDocument (.odt/.ods/.odp)
    "read_odt_text": read_odt_text,
    "get_ods_sheet_names": get_ods_sheet_names,
    "read_ods_data": read_ods_data,
    "read_odp_text": read_odp_text,
    "get_odp_slide_count": get_odp_slide_count,
    "create_odt": create_odt,
    "create_ods": create_ods,
    "create_odp": create_odp,
    # Rasm (image)
    "get_image_info": get_image_info,
    "read_image_text": read_image_text,
    "convert_image": convert_image,
    "create_thumbnail": create_thumbnail,
    "crop_image": crop_image,
    "resize_image": resize_image,
    "rotate_image": rotate_image,
    "create_image": create_image,
    # Arxiv (ZIP)
    "list_archive_contents": list_archive_contents,
    "read_archive_file": read_archive_file,
    "create_archive": create_archive,
    "extract_archive": extract_archive,
    # Konvertatsiya
    "convert_docx_to_pdf": convert_docx_to_pdf,
    "convert_pptx_to_pdf": convert_pptx_to_pdf,
    "convert_xlsx_to_pdf": convert_xlsx_to_pdf,
    "convert_pdf_to_images": convert_pdf_to_images,
    "convert_pptx_to_images": convert_pptx_to_images,
    "convert_xlsx_to_csv": convert_xlsx_to_csv,
    # Kod/matn fayllari (.py, .js, .html, .css, .json, .csv, .txt va h.k.)
    "read_code_file": read_code_file,
    "read_code_lines": read_code_lines,
    "create_code_file": create_code_file,
    "append_code_text": append_code_text,
    "replace_code_text": replace_code_text,
    "insert_code_lines": insert_code_lines,
    "delete_code_lines": delete_code_lines,
    "list_directory_files": list_directory_files,
    "search_in_files": search_in_files,
    # Internetdan ma'lumot olish (fayl yuklash, web scraping, qidiruv)
    "download_file": download_file,
    "fetch_url_text": fetch_url_text,
    "scrape_page_text": scrape_page_text,
    "extract_page_links": extract_page_links,
    "extract_page_images": extract_page_images,
    "search_web": search_web,
    "get_known_changelog_url": get_known_changelog_url,
}

# file_path/image_path qabul qiladigan tool'lar uchun xavfsizlik tekshiruvi
# qo'llaniladigan parametr nomlari (scalar yo'llar)
_PATH_PARAMS = ("file_path", "image_path", "save_as", "output_path", "output_dir", "dir_path")
# ro'yxat (list) ko'rinishidagi fayl yo'llari (masalan merge_pdfs)
_PATH_LIST_PARAMS = ("file_paths",)


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
        for param in _PATH_LIST_PARAMS:
            if param in safe_input and safe_input[param]:
                safe_input[param] = [resolve_safe_path(p, base_dir=base_dir) for p in safe_input[param]]
    except UnsafePathError as e:
        return {"error": f"Xavfsizlik xatosi: {e}"}

    try:
        return func(**safe_input)
    except FileNotFoundError:
        return {"error": f"Fayl topilmadi: {safe_input.get('file_path')}"}
    except Exception as e:
        return {"error": f"{type(e).__name__}: {e}"}
