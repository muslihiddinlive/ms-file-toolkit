"""Yangi modullar uchun testlar: CSV, OpenDocument, rasm/OCR, arxiv, konvertatsiya.

Ishga tushirish:
    pytest tests/test_expansion.py -v

Eslatma: OCR testlari tizimda `tesseract-ocr` o'rnatilgan bo'lishini talab qiladi
(agar o'rnatilmagan bo'lsa, mos testlar avtomatik skip qilinadi). Konvertatsiya
testlari (`convert_*_to_pdf`, `*_to_images`) tizimda `soffice` (LibreOffice)
borligini talab qiladi.
"""

import os
import shutil
import pytest
from ms_toolkit import dispatch


def _has_binary(name: str) -> bool:
    return shutil.which(name) is not None


@pytest.fixture
def tmp_dir(tmp_path):
    return str(tmp_path)


# ---------- CSV ----------

def test_csv_create_and_read(tmp_dir):
    path = os.path.join(tmp_dir, "data.csv")
    result = dispatch("create_csv", {
        "file_path": path,
        "headers": ["ism", "yosh"],
        "rows": [["Ali", "20"], ["Vali", "25"]],
        "overwrite": True,
    })
    assert result["status"] == "created"

    read = dispatch("read_csv_data", {"file_path": path})
    assert read["headers"] == ["ism", "yosh"]
    assert read["row_count"] == 2

    summary = dispatch("get_csv_summary", {"file_path": path})
    assert summary["column_count"] == 2


def test_csv_append(tmp_dir):
    path = os.path.join(tmp_dir, "data.csv")
    dispatch("create_csv", {"file_path": path, "headers": ["a"], "overwrite": True})
    result = dispatch("append_csv_rows", {"file_path": path, "rows": [["1"], ["2"]]})
    assert result["added_row_count"] == 2
    read = dispatch("read_csv_data", {"file_path": path})
    assert read["row_count"] == 2


def test_csv_create_refuses_overwrite_without_flag(tmp_dir):
    path = os.path.join(tmp_dir, "data.csv")
    dispatch("create_csv", {"file_path": path, "overwrite": True})
    result = dispatch("create_csv", {"file_path": path})
    assert "error" in result


# ---------- OpenDocument ----------

def test_odt_create_and_read(tmp_dir):
    path = os.path.join(tmp_dir, "doc.odt")
    result = dispatch("create_odt", {
        "file_path": path, "title": "Sarlavha", "paragraphs": ["P1", "P2"], "overwrite": True,
    })
    assert result["status"] == "created"

    read = dispatch("read_odt_text", {"file_path": path})
    assert "Sarlavha" in read["text"]
    assert "P1" in read["text"] and "P2" in read["text"]


def test_ods_create_and_read(tmp_dir):
    path = os.path.join(tmp_dir, "sheet.ods")
    result = dispatch("create_ods", {
        "file_path": path, "rows": [["a", "b"], ["1", "2"]], "sheet_name": "Data", "overwrite": True,
    })
    assert result["status"] == "created"

    names = dispatch("get_ods_sheet_names", {"file_path": path})
    assert names["sheet_names"] == ["Data"]

    data = dispatch("read_ods_data", {"file_path": path})
    assert data["row_count"] == 2


def test_odp_create_and_read(tmp_dir):
    path = os.path.join(tmp_dir, "slides.odp")
    result = dispatch("create_odp", {"file_path": path, "slides": ["S1", "S2", "S3"], "overwrite": True})
    assert result["status"] == "created"

    count = dispatch("get_odp_slide_count", {"file_path": path})
    assert count["slide_count"] == 3

    text = dispatch("read_odp_text", {"file_path": path})
    assert text["slides"] == ["S1", "S2", "S3"]


# ---------- Rasm (image) ----------

@pytest.fixture
def sample_image(tmp_dir):
    from PIL import Image
    path = os.path.join(tmp_dir, "sample.png")
    Image.new("RGB", (120, 60), color=(200, 100, 50)).save(path)
    return path


def test_get_image_info(sample_image):
    result = dispatch("get_image_info", {"file_path": sample_image})
    assert result["width"] == 120
    assert result["height"] == 60
    assert result["format"] == "PNG"


def test_convert_image(sample_image, tmp_dir):
    out = os.path.join(tmp_dir, "out.jpg")
    result = dispatch("convert_image", {"file_path": sample_image, "output_path": out, "width": 60})
    assert result["status"] == "converted"
    assert result["width"] == 60
    assert os.path.exists(out)


def test_create_thumbnail(sample_image, tmp_dir):
    out = os.path.join(tmp_dir, "thumb.png")
    result = dispatch("create_thumbnail", {"file_path": sample_image, "output_path": out, "size": 32})
    assert result["status"] == "created"
    assert max(result["width"], result["height"]) <= 32


@pytest.mark.skipif(not _has_binary("tesseract"), reason="tesseract-ocr o'rnatilmagan")
def test_read_image_text_ocr(tmp_dir):
    from PIL import Image, ImageDraw
    path = os.path.join(tmp_dir, "ocr.png")
    img = Image.new("RGB", (300, 80), color=(255, 255, 255))
    ImageDraw.Draw(img).text((10, 20), "Salom Dunyo", fill=(0, 0, 0))
    img.save(path)

    result = dispatch("read_image_text", {"file_path": path})
    assert "error" not in result
    assert "Salom" in result["text"] or "Dunyo" in result["text"]


# ---------- Arxiv (ZIP) ----------

def test_archive_create_list_read_extract(tmp_dir):
    f1 = os.path.join(tmp_dir, "a.txt")
    f2 = os.path.join(tmp_dir, "b.txt")
    with open(f1, "w") as f:
        f.write("hello")
    with open(f2, "w") as f:
        f.write("world")

    zip_path = os.path.join(tmp_dir, "arch.zip")
    result = dispatch("create_archive", {"output_path": zip_path, "file_paths": [f1, f2], "overwrite": True})
    assert result["entry_count"] == 2

    listing = dispatch("list_archive_contents", {"file_path": zip_path})
    assert listing["entry_count"] == 2

    content = dispatch("read_archive_file", {"file_path": zip_path, "entry_name": "a.txt"})
    assert content["text"] == "hello"

    out_dir = os.path.join(tmp_dir, "extracted")
    extracted = dispatch("extract_archive", {"file_path": zip_path, "output_dir": out_dir})
    assert set(extracted["extracted_files"]) == {"a.txt", "b.txt"}
    assert os.path.exists(os.path.join(out_dir, "a.txt"))


def test_archive_missing_entry(tmp_dir):
    f1 = os.path.join(tmp_dir, "a.txt")
    with open(f1, "w") as f:
        f.write("x")
    zip_path = os.path.join(tmp_dir, "arch.zip")
    dispatch("create_archive", {"output_path": zip_path, "file_paths": [f1], "overwrite": True})

    result = dispatch("read_archive_file", {"file_path": zip_path, "entry_name": "missing.txt"})
    assert "error" in result


# ---------- Konvertatsiya ----------

@pytest.mark.skipif(not _has_binary("soffice"), reason="LibreOffice (soffice) o'rnatilmagan")
def test_convert_docx_to_pdf(tmp_dir):
    docx_path = os.path.join(tmp_dir, "doc.docx")
    dispatch("create_docx", {"file_path": docx_path, "title": "T", "paragraphs": ["p"], "overwrite": True})

    pdf_path = os.path.join(tmp_dir, "doc.pdf")
    result = dispatch("convert_docx_to_pdf", {"file_path": docx_path, "output_path": pdf_path, "overwrite": True})
    assert result["status"] == "converted"
    assert os.path.exists(pdf_path)


@pytest.mark.skipif(not _has_binary("soffice"), reason="LibreOffice (soffice) o'rnatilmagan")
def test_convert_pptx_to_images(tmp_dir):
    pptx_path = os.path.join(tmp_dir, "slides.pptx")
    dispatch("create_pptx", {"file_path": pptx_path, "overwrite": True})
    dispatch("add_pptx_slide", {"file_path": pptx_path, "title": "S1", "content": "text"})

    out_dir = os.path.join(tmp_dir, "imgs")
    result = dispatch("convert_pptx_to_images", {"file_path": pptx_path, "output_dir": out_dir})
    assert result["status"] == "converted"
    assert result["page_count"] >= 1


def test_convert_pdf_to_images(tmp_dir):
    pdf_path = os.path.join(tmp_dir, "doc.pdf")
    dispatch("create_pdf", {"file_path": pdf_path, "title": "T", "paragraphs": ["p1", "p2"], "overwrite": True})

    out_dir = os.path.join(tmp_dir, "imgs")
    result = dispatch("convert_pdf_to_images", {"file_path": pdf_path, "output_dir": out_dir})
    assert result["status"] == "converted"
    assert result["page_count"] == 1


def test_convert_xlsx_to_csv(tmp_dir):
    xlsx_path = os.path.join(tmp_dir, "data.xlsx")
    dispatch("create_xlsx", {"file_path": xlsx_path, "overwrite": True})
    dispatch("append_xlsx_rows", {"file_path": xlsx_path, "rows": [["a", "b"], ["1", "2"]]})

    out_dir = os.path.join(tmp_dir, "csvs")
    result = dispatch("convert_xlsx_to_csv", {"file_path": xlsx_path, "output_dir": out_dir})
    assert result["status"] == "converted"
    assert result["sheet_count"] >= 1


# ---------- Yangi tool'lar ham xavfsizlik nazoratidan o'tishi kerak ----------

def test_new_tools_registered_in_security_check():
    result = dispatch("extract_archive", {"file_path": "/etc/passwd", "output_dir": "/tmp/x"})
    assert "error" in result
