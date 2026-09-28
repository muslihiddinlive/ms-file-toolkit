"""PDF (rasmlardan yaratish, rasm ajratish, birlashtirish) va QR (yaratish/o'qish) testlari.

Ishga tushirish:  pytest tests/test_pdf_qr.py -v
"""

import os
import pytest
from PIL import Image, ImageDraw
from ms_toolkit import dispatch


@pytest.fixture
def tmp_dir(tmp_path):
    return str(tmp_path)


def _make_image(path, size=(300, 200), color=(200, 30, 30), mode="RGB"):
    img = Image.new(mode, size, color)
    ImageDraw.Draw(img).rectangle([10, 10, size[0] - 10, size[1] - 10], outline=(0, 0, 0), width=4)
    img.save(path)
    return path


# ---------- QR: yaratish + o'qish ----------

@pytest.mark.parametrize("qr_type,data,expected", [
    ("text", "Salom, dunyo! O'zbekiston", "Salom, dunyo! O'zbekiston"),
    ("url", "example.com/a?b=1", "https://example.com/a?b=1"),
    ("phone", "998 90 123-45-67", "tel:+998901234567"),
    ("telegram", "@paradoks", "https://t.me/paradoks"),
])
def test_qr_roundtrip(tmp_dir, qr_type, data, expected):
    path = os.path.join(tmp_dir, "qr.png")
    created = dispatch("create_qr_code", {"output_path": path, "data": data, "qr_type": qr_type})
    assert created["status"] == "created"
    assert created["content"] == expected

    read = dispatch("read_qr_code", {"image_path": path})
    assert read["found"] and read["count"] == 1
    assert read["codes"][0]["text"] == expected


def test_qr_wifi_escapes_special_chars(tmp_dir):
    path = os.path.join(tmp_dir, "wifi.png")
    created = dispatch("create_qr_code", {
        "output_path": path, "data": 'Uy;Wifi', "qr_type": "wifi",
        "password": 'p:a;ss,"1', "security": "WPA",
    })
    assert created["content"] == 'WIFI:S:Uy\\;Wifi;T:WPA;P:p\\:a\\;ss\\,\\"1;H:false;;'
    read = dispatch("read_qr_code", {"image_path": path})
    assert read["codes"][0]["kind"] == "wifi"
    assert read["codes"][0]["text"] == created["content"]


def test_qr_vcard_and_email_and_sms(tmp_dir):
    p1 = os.path.join(tmp_dir, "v.png")
    r = dispatch("create_qr_code", {"output_path": p1, "data": "Ali Valiyev", "qr_type": "vcard",
                                    "phone": "998901112233", "org": "Paradoks"})
    assert "FN:Ali Valiyev" in r["content"] and "TEL;TYPE=CELL:+998901112233" in r["content"]
    assert dispatch("read_qr_code", {"image_path": p1})["codes"][0]["kind"] == "vcard"

    p2 = os.path.join(tmp_dir, "e.png")
    r = dispatch("create_qr_code", {"output_path": p2, "data": "a@b.uz", "qr_type": "email", "subject": "Salom dunyo"})
    assert r["content"] == "mailto:a@b.uz?subject=Salom%20dunyo"

    p3 = os.path.join(tmp_dir, "s.png")
    r = dispatch("create_qr_code", {"output_path": p3, "data": "998901112233", "qr_type": "sms", "message": "Hi"})
    assert r["content"] == "SMSTO:+998901112233:Hi"


def test_qr_svg_output(tmp_dir):
    path = os.path.join(tmp_dir, "q.svg")
    assert dispatch("create_qr_code", {"output_path": path, "data": "x"})["status"] == "created"
    assert open(path, encoding="utf-8").read().lstrip().startswith(("<?xml", "<svg"))


def test_qr_errors(tmp_dir):
    path = os.path.join(tmp_dir, "q.png")
    assert "error" in dispatch("create_qr_code", {"output_path": path, "data": "x", "qr_type": "nope"})
    assert "error" in dispatch("create_qr_code", {"output_path": path, "data": ""})
    assert "error" in dispatch("create_qr_code", {"output_path": path, "data": "x" * 2500})
    assert "error" in dispatch("create_qr_code", {"output_path": os.path.join(tmp_dir, "q.jpg"), "data": "x"})
    dispatch("create_qr_code", {"output_path": path, "data": "x"})
    assert "allaqachon mavjud" in dispatch("create_qr_code", {"output_path": path, "data": "y"})["error"]
    assert "error" in dispatch("read_qr_code", {"image_path": os.path.join(tmp_dir, "yoq.png")})


def test_read_qr_from_photo_like_image(tmp_dir):
    """Haqiqiy hayotdagidek: QR kichraytirilgan, oq qog'oz ustida, biroz aylantirilgan."""
    qr_path = os.path.join(tmp_dir, "qr.png")
    dispatch("create_qr_code", {"output_path": qr_path, "data": "https://t.me/paradoks", "size": 400})
    qr = Image.open(qr_path).convert("RGB").resize((160, 160))
    paper = Image.new("RGB", (640, 480), (235, 235, 225))
    paper.paste(qr.rotate(7, expand=True, fillcolor=(235, 235, 225)), (200, 140))
    photo = os.path.join(tmp_dir, "photo.jpg")
    paper.save(photo, quality=70)
    read = dispatch("read_qr_code", {"image_path": photo})
    assert read["found"] and read["codes"][0]["text"] == "https://t.me/paradoks"


def test_read_qr_no_code_and_not_an_image(tmp_dir):
    blank = _make_image(os.path.join(tmp_dir, "blank.png"))
    r = dispatch("read_qr_code", {"image_path": blank})
    assert r["found"] is False and r["count"] == 0
    bad = os.path.join(tmp_dir, "bad.png")
    open(bad, "wb").write(b"not an image")
    assert "error" in dispatch("read_qr_code", {"image_path": bad})


# ---------- Rasmlardan PDF ----------

def test_images_to_pdf_original_and_a4(tmp_dir):
    a = _make_image(os.path.join(tmp_dir, "a.jpg"), (400, 300))
    b = _make_image(os.path.join(tmp_dir, "b.png"), (200, 500), (10, 120, 200))
    import fitz

    out = os.path.join(tmp_dir, "orig.pdf")
    r = dispatch("create_pdf_from_images", {"image_paths": [a, b], "output_path": out})
    assert r["status"] == "created" and r["page_count"] == 2
    with fitz.open(out) as d:
        assert len(d) == 2
        assert d[0].rect.width > d[0].rect.height   # landscape rasm — landscape sahifa
        assert d[1].rect.height > d[1].rect.width

    out2 = os.path.join(tmp_dir, "a4.pdf")
    r = dispatch("create_pdf_from_images", {"image_paths": [a, b], "output_path": out2, "page_size": "a4"})
    assert r["page_size"] == "a4"
    with fitz.open(out2) as d:
        assert abs(d[1].rect.width - 595) < 2 and abs(d[1].rect.height - 842) < 2   # portrait A4
        assert abs(d[0].rect.width - 842) < 2                                       # landscape A4


def test_images_to_pdf_transparent_png_gets_white_background(tmp_dir):
    import fitz

    png = os.path.join(tmp_dir, "t.png")
    Image.new("RGBA", (100, 100), (0, 0, 0, 0)).save(png)  # to'liq shaffof
    out = os.path.join(tmp_dir, "t.pdf")
    assert dispatch("create_pdf_from_images", {"image_paths": [png], "output_path": out})["status"] == "created"
    with fitz.open(out) as d:
        pix = d[0].get_pixmap()
        assert pix.pixel(pix.width // 2, pix.height // 2)[:3] == (255, 255, 255)  # qora emas, oq


def test_images_to_pdf_errors(tmp_dir):
    out = os.path.join(tmp_dir, "x.pdf")
    assert "error" in dispatch("create_pdf_from_images", {"image_paths": [], "output_path": out})
    assert "error" in dispatch("create_pdf_from_images", {"image_paths": [os.path.join(tmp_dir, "yoq.png")], "output_path": out})
    bad = os.path.join(tmp_dir, "bad.png")
    open(bad, "wb").write(b"nope")
    assert "error" in dispatch("create_pdf_from_images", {"image_paths": [bad], "output_path": out})
    good = _make_image(os.path.join(tmp_dir, "g.png"))
    assert "error" in dispatch("create_pdf_from_images", {"image_paths": [good], "output_path": out, "page_size": "b5"})
    dispatch("create_pdf_from_images", {"image_paths": [good], "output_path": out})
    assert "allaqachon mavjud" in dispatch("create_pdf_from_images", {"image_paths": [good], "output_path": out})["error"]


def test_images_to_pdf_path_security(tmp_dir):
    """image_paths ro'yxati ham base_dir bilan cheklanadi."""
    inside = _make_image(os.path.join(tmp_dir, "in.png"))
    r = dispatch(
        "create_pdf_from_images",
        {"image_paths": [inside, "/etc/passwd"], "output_path": os.path.join(tmp_dir, "o.pdf")},
        base_dir=tmp_dir,
    )
    assert "Xavfsizlik" in r["error"]


# ---------- PDF ichidagi rasmlarni chiqarish ----------

def test_extract_pdf_images(tmp_dir):
    a = _make_image(os.path.join(tmp_dir, "a.jpg"), (400, 300))
    b = _make_image(os.path.join(tmp_dir, "b.png"), (300, 300), (0, 200, 0))
    pdf = os.path.join(tmp_dir, "in.pdf")
    dispatch("create_pdf_from_images", {"image_paths": [a, b], "output_path": pdf})

    out_dir = os.path.join(tmp_dir, "extracted")
    r = dispatch("extract_pdf_images", {"file_path": pdf, "output_dir": out_dir})
    assert r["image_count"] == 2 and r["page_count"] == 2
    assert {i["page"] for i in r["images"]} == {1, 2}
    for item in r["images"]:
        assert os.path.getsize(item["path"]) > 0
        Image.open(item["path"]).verify()   # haqiqiy, ochiladigan rasm


def test_extract_pdf_images_dedup_and_small_filter(tmp_dir):
    import fitz

    big = os.path.join(tmp_dir, "big.png")
    _make_image(big, (300, 300))
    tiny = os.path.join(tmp_dir, "tiny.png")
    _make_image(tiny, (20, 20))
    pdf = os.path.join(tmp_dir, "d.pdf")
    doc = fitz.open()
    for _ in range(2):   # bir xil rasm ikki sahifada
        page = doc.new_page()
        page.insert_image(fitz.Rect(50, 50, 250, 250), filename=big)
        page.insert_image(fitz.Rect(300, 50, 320, 70), filename=tiny)
    doc.save(pdf)
    doc.close()

    r = dispatch("extract_pdf_images", {"file_path": pdf, "output_dir": os.path.join(tmp_dir, "o")})
    assert r["image_count"] == 1          # takroriy bir marta
    assert r["skipped_small"] == 1        # kichigi o'tkazib yuborildi


def test_extract_pdf_images_none_found_gives_hint(tmp_dir):
    pdf = os.path.join(tmp_dir, "text.pdf")
    dispatch("create_pdf", {"file_path": pdf, "title": "Faqat matn", "paragraphs": ["salom"]})
    r = dispatch("extract_pdf_images", {"file_path": pdf, "output_dir": os.path.join(tmp_dir, "o")})
    assert r["image_count"] == 0 and "convert_pdf_to_images" in r["note"]


def test_extract_pdf_images_errors(tmp_dir):
    assert "error" in dispatch("extract_pdf_images", {"file_path": os.path.join(tmp_dir, "yoq.pdf"), "output_dir": tmp_dir})


# ---------- PDF birlashtirish (mavjud funksiya, regressiya uchun) ----------

def test_merge_pdfs_page_counts(tmp_dir):
    p1, p2 = os.path.join(tmp_dir, "1.pdf"), os.path.join(tmp_dir, "2.pdf")
    dispatch("create_pdf", {"file_path": p1, "title": "Bir", "paragraphs": ["a"]})
    im = _make_image(os.path.join(tmp_dir, "i.png"))
    dispatch("create_pdf_from_images", {"image_paths": [im, im, im], "output_path": p2})
    out = os.path.join(tmp_dir, "m.pdf")
    r = dispatch("merge_pdfs", {"file_paths": [p1, p2], "output_path": out})
    assert r["status"] == "merged"
    assert dispatch("get_pdf_metadata", {"file_path": out})["page_count"] == 4
