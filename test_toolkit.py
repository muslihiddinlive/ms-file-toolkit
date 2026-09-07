"""
API kalitisiz tezkor tekshiruv: barcha 18 ta tool to'g'ri ishlayaptimi.

Ishga tushirish:
    python test_toolkit.py
"""

import json
import tempfile
import os

from ms_toolkit import TOOLS, dispatch


def show(label, result):
    print(f"\n--- {label} ---")
    print(json.dumps(result, ensure_ascii=False, indent=2, default=str)[:400])
    assert "error" not in result, f"{label} da xato: {result}"


def main():
    print(f"Ro'yxatga olingan tool'lar soni: {len(TOOLS)}")
    tmp = tempfile.mkdtemp(prefix="ms_toolkit_test_")

    docx_path = os.path.join(tmp, "hisobot.docx")
    xlsx_path = os.path.join(tmp, "data.xlsx")
    pptx_path = os.path.join(tmp, "taqdimot.pptx")

    show("create_docx", dispatch("create_docx", {
        "file_path": docx_path, "title": "Test hujjat",
        "paragraphs": ["Birinchi qator."], "overwrite": True,
    }))
    show("append_docx_text", dispatch("append_docx_text", {"file_path": docx_path, "text": "Qo'shimcha."}))
    show("read_docx_text", dispatch("read_docx_text", {"file_path": docx_path}))

    show("create_xlsx", dispatch("create_xlsx", {
        "file_path": xlsx_path, "headers": ["Ism", "Yosh"],
        "rows": [["Ali", 25]], "overwrite": True,
    }))
    show("read_xlsx_data", dispatch("read_xlsx_data", {"file_path": xlsx_path}))

    show("create_pptx", dispatch("create_pptx", {"file_path": pptx_path, "title": "Test", "overwrite": True}))
    show("add_pptx_slide", dispatch("add_pptx_slide", {"file_path": pptx_path, "title": "Slayd 2", "bullet_points": ["A", "B"]}))
    show("read_pptx_text", dispatch("read_pptx_text", {"file_path": pptx_path}))

    print(f"\n✅ Hammasi ishladi. Vaqtinchalik fayllar: {tmp}")


if __name__ == "__main__":
    main()
