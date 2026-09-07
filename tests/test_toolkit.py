"""
To'liq pytest test to'plami — barcha 36 ta tool, xavfsizlik, auto-detect,
PDF, chart va CLI uchun.

Ishga tushirish:
    pip install pytest Pillow
    pytest tests/ -v
"""

import os
import json
import pytest
from ms_toolkit import dispatch, TOOLS, REGISTRY


@pytest.fixture
def tmp_dir(tmp_path):
    return str(tmp_path)


@pytest.fixture
def sample_image(tmp_dir):
    from PIL import Image
    path = os.path.join(tmp_dir, "sample.png")
    Image.new("RGB", (80, 50), color=(100, 150, 200)).save(path)
    return path


# ---------- Umumiy ----------

def test_all_tools_registered():
    tool_names = {t["name"] for t in TOOLS}
    registry_names = set(REGISTRY.keys())
    assert tool_names == registry_names, "TOOLS va REGISTRY mos kelmayapti"
    assert len(TOOLS) >= 36


def test_unknown_tool_returns_error():
    result = dispatch("no_such_tool", {})
    assert "error" in result


# ---------- Xavfsizlik ----------

def test_blocks_system_path():
    result = dispatch("read_docx_text", {"file_path": "/etc/passwd"})
    assert "error" in result
    assert "avfsizlik" in result["error"] or "security" in result["error"].lower()


def test_blocks_null_byte():
    result = dispatch("read_docx_text", {"file_path": "test\x00.docx"})
    assert "error" in result


def test_base_dir_restricts_access(tmp_dir, monkeypatch):
    monkeypatch.setenv("MS_TOOLKIT_BASE_DIR", tmp_dir)
    outside = dispatch("get_file_info", {"file_path": "/tmp/somewhere_else/x.docx"})
    assert "error" in outside

    inside = dispatch("get_file_info", {"file_path": os.path.join(tmp_dir, "x.docx")})
    assert "error" not in inside


# ---------- DOCX ----------

def test_docx_create_and_read(tmp_dir):
    path = os.path.join(tmp_dir, "doc.docx")
    r = dispatch("create_docx", {
        "file_path": path, "title": "Sarlavha",
        "paragraphs": ["Birinchi.", "Ikkinchi."],
        "table_data": [["A", "B"], ["1", "2"]],
        "overwrite": True,
    })
    assert r["status"] == "created"

    text = dispatch("read_docx_text", {"file_path": path})
    assert "Birinchi." in text["text"]

    tables = dispatch("read_docx_tables", {"file_path": path})
    assert tables["table_count"] == 1

    meta = dispatch("get_docx_metadata", {"file_path": path})
    assert meta["paragraph_count"] >= 3


def test_docx_append_replace_heading_pagebreak_image(tmp_dir, sample_image):
    path = os.path.join(tmp_dir, "doc2.docx")
    dispatch("create_docx", {"file_path": path, "title": "T", "overwrite": True})

    assert dispatch("append_docx_text", {"file_path": path, "text": "Qoshimcha"})["status"] == "appended"
    assert dispatch("add_docx_heading", {"file_path": path, "text": "Bolim", "level": 2})["status"] == "heading_added"
    assert dispatch("add_docx_page_break", {"file_path": path})["status"] == "page_break_added"
    assert dispatch("add_docx_image", {"file_path": path, "image_path": sample_image})["status"] == "image_added"

    r = dispatch("replace_docx_text", {"file_path": path, "find": "Bolim", "replace": "Yangi"})
    assert r["replacements"] >= 1


def test_docx_create_refuses_overwrite_without_flag(tmp_dir):
    path = os.path.join(tmp_dir, "doc3.docx")
    dispatch("create_docx", {"file_path": path, "overwrite": True})
    r = dispatch("create_docx", {"file_path": path})
    assert "error" in r


# ---------- XLSX ----------

def test_xlsx_create_and_read(tmp_dir):
    path = os.path.join(tmp_dir, "data.xlsx")
    r = dispatch("create_xlsx", {
        "file_path": path, "headers": ["Ism", "Yosh"],
        "rows": [["Ali", 25], ["Vali", 30]], "overwrite": True,
    })
    assert r["status"] == "created"

    data = dispatch("read_xlsx_data", {"file_path": path})
    assert data["row_count"] == 2

    names = dispatch("get_xlsx_sheet_names", {"file_path": path})
    assert "Sheet1" in names["sheet_names"]

    summary = dispatch("get_xlsx_summary", {"file_path": path})
    assert summary["sheets"][0]["max_row"] == 3


def test_xlsx_sheet_rows_formula_format_freeze(tmp_dir):
    path = os.path.join(tmp_dir, "data2.xlsx")
    dispatch("create_xlsx", {"file_path": path, "headers": ["A"], "rows": [[1], [2]], "overwrite": True})

    assert dispatch("add_xlsx_sheet", {"file_path": path, "sheet_name": "S2", "headers": ["X"]})["status"] == "sheet_added"
    assert dispatch("append_xlsx_rows", {"file_path": path, "rows": [[3]]})["status"] == "appended"
    assert dispatch("set_xlsx_formula", {"file_path": path, "cell": "B1", "formula": "SUM(A1:A3)"})["status"] == "formula_set"
    assert dispatch("format_xlsx_cells", {"file_path": path, "cell_range": "A1:A1", "bold": True, "bg_color": "FFFF00"})["status"] == "formatted"
    assert dispatch("freeze_xlsx_panes", {"file_path": path, "cell": "A2"})["status"] == "panes_frozen"


# ---------- PPTX ----------

def test_pptx_create_and_read(tmp_dir):
    path = os.path.join(tmp_dir, "slides.pptx")
    r = dispatch("create_pptx", {"file_path": path, "title": "Sarlavha", "subtitle": "Sub", "overwrite": True})
    assert r["status"] == "created"

    r2 = dispatch("add_pptx_slide", {"file_path": path, "title": "Slayd2", "bullet_points": ["A", "B"], "notes": "izoh"})
    assert r2["slide_count"] == 2

    text = dispatch("read_pptx_text", {"file_path": path})
    assert text["slide_count"] == 2

    count = dispatch("get_pptx_slide_count", {"file_path": path})
    assert count["slide_count"] == 2

    notes = dispatch("extract_pptx_notes", {"file_path": path})
    assert notes["notes"][1]["notes"] == "izoh"


def test_pptx_image_and_background(tmp_dir, sample_image):
    path = os.path.join(tmp_dir, "slides2.pptx")
    dispatch("create_pptx", {"file_path": path, "title": "T", "overwrite": True})

    r = dispatch("add_pptx_image", {"file_path": path, "image_path": sample_image, "width_inches": 2.0})
    assert r["status"] == "image_added"

    r2 = dispatch("set_pptx_background_color", {"file_path": path, "slide_index": 0, "hex_color": "E6F1FB"})
    assert r2["status"] == "background_set"


# ---------- Auto-detect ----------

def test_read_any_file_and_info(tmp_dir):
    path = os.path.join(tmp_dir, "auto.docx")
    dispatch("create_docx", {"file_path": path, "title": "Auto", "overwrite": True})

    info = dispatch("get_file_info", {"file_path": path})
    assert info["detected_type"] == "docx"
    assert info["exists"] is True

    result = dispatch("read_any_file", {"file_path": path})
    assert result["detected_type"] == "docx"
    assert "Auto" in result["text"]


def test_read_any_file_unknown_extension(tmp_dir):
    path = os.path.join(tmp_dir, "file.xyz")
    with open(path, "w") as f:
        f.write("test")
    result = dispatch("read_any_file", {"file_path": path})
    assert "error" in result


def test_read_any_file_missing():
    result = dispatch("read_any_file", {"file_path": "/tmp/does_not_exist_xyz.docx"})
    assert "error" in result


# ---------- PDF ----------

def test_pdf_create_read_metadata(tmp_dir):
    path = os.path.join(tmp_dir, "doc.pdf")
    r = dispatch("create_pdf", {"file_path": path, "title": "Sarlavha", "paragraphs": ["Birinchi."], "overwrite": True})
    assert r["status"] == "created"

    text = dispatch("read_pdf_text", {"file_path": path})
    assert "Birinchi." in text["text"]

    meta = dispatch("get_pdf_metadata", {"file_path": path})
    assert meta["page_count"] == 1
    assert meta["encrypted"] is False

    tables = dispatch("read_pdf_tables", {"file_path": path})
    assert tables["table_count"] == 0


def test_pdf_merge_and_split(tmp_dir):
    p1 = os.path.join(tmp_dir, "a.pdf")
    p2 = os.path.join(tmp_dir, "b.pdf")
    dispatch("create_pdf", {"file_path": p1, "title": "A", "overwrite": True})
    dispatch("create_pdf", {"file_path": p2, "title": "B", "overwrite": True})

    merged = os.path.join(tmp_dir, "merged.pdf")
    r = dispatch("merge_pdfs", {"file_paths": [p1, p2], "output_path": merged, "overwrite": True})
    assert r["status"] == "merged"

    meta = dispatch("get_pdf_metadata", {"file_path": merged})
    assert meta["page_count"] == 2

    out_dir = os.path.join(tmp_dir, "split")
    r2 = dispatch("split_pdf", {"file_path": merged, "output_dir": out_dir})
    assert len(r2["output_files"]) == 2


def test_pdf_merge_blocks_path_traversal(tmp_dir):
    p1 = os.path.join(tmp_dir, "a.pdf")
    dispatch("create_pdf", {"file_path": p1, "overwrite": True})
    result = dispatch("merge_pdfs", {"file_paths": [p1, "/etc/passwd"], "output_path": os.path.join(tmp_dir, "out.pdf")})
    assert "error" in result


# ---------- Chart'lar ----------

def test_xlsx_chart(tmp_dir):
    path = os.path.join(tmp_dir, "chart.xlsx")
    dispatch("create_xlsx", {"file_path": path, "headers": ["Oy", "Savdo"], "rows": [["Yan", 100], ["Fev", 150]], "overwrite": True})

    r = dispatch("add_xlsx_chart", {
        "file_path": path, "chart_type": "bar",
        "data_range": "B1:B3", "categories_range": "A2:A3", "title": "Test",
    })
    assert r["status"] == "chart_added"

    r_bad = dispatch("add_xlsx_chart", {"file_path": path, "chart_type": "unknown", "data_range": "B1:B3"})
    assert "error" in r_bad


def test_pptx_chart(tmp_dir):
    path = os.path.join(tmp_dir, "chart.pptx")
    dispatch("create_pptx", {"file_path": path, "title": "T", "overwrite": True})

    r = dispatch("add_pptx_chart", {
        "file_path": path, "chart_type": "pie",
        "categories": ["A", "B"], "series": {"S1": [10, 20]}, "title": "Test",
    })
    assert r["status"] == "chart_added"

    r_bad = dispatch("add_pptx_chart", {"file_path": path, "chart_type": "unknown", "categories": [], "series": {}})
    assert "error" in r_bad


# ---------- CLI ----------

def test_cli_run_success(tmp_dir):
    import subprocess
    path = os.path.join(tmp_dir, "cli.docx")
    result = subprocess.run(
        ["python3", "-m", "ms_toolkit.cli", "run", "create_docx", json.dumps({"file_path": path, "overwrite": True})],
        capture_output=True, text=True,
    )
    assert result.returncode == 0
    assert "created" in result.stdout


def test_cli_run_unknown_tool():
    import subprocess
    result = subprocess.run(
        ["python3", "-m", "ms_toolkit.cli", "run", "no_such_tool", "{}"],
        capture_output=True, text=True,
    )
    assert result.returncode == 1


def test_cli_list():
    import subprocess
    result = subprocess.run(["python3", "-m", "ms_toolkit.cli", "list"], capture_output=True, text=True)
    assert result.returncode == 0
    assert "create_docx" in result.stdout
