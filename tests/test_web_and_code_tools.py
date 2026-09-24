"""Yangi modullar uchun testlar: kod/matn fayllar, rasm (crop/resize/rotate), web (download/scrape/search).

Ishga tushirish:
    pytest tests/test_web_and_code_tools.py -v

Eslatma: tarmoq talab qiladigan testlar (download_file, search_web va h.k.
haqiqiy internetga chiqadigan holatlari) tarmoq yo'q yoki tegishli domen
bloklangan muhitda avtomatik skip qilinadi.
"""

import os
import pytest
import requests
from ms_toolkit import dispatch, TOOLS


@pytest.fixture
def tmp_dir(tmp_path):
    return str(tmp_path)


@pytest.fixture
def sample_image(tmp_dir):
    from PIL import Image
    path = os.path.join(tmp_dir, "sample.png")
    Image.new("RGB", (80, 50), color=(100, 150, 200)).save(path)
    return path


# ---------- Kod/matn fayllari (code_tool) ----------

def test_create_and_read_code_file(tmp_dir):
    path = os.path.join(tmp_dir, "app.py")
    result = dispatch("create_code_file", {"file_path": path, "content": "print('hi')\nprint('bye')\n"})
    assert result["status"] == "created"

    read = dispatch("read_code_file", {"file_path": path})
    assert read["line_count"] == 2
    assert "print('hi')" in read["content"]


def test_create_code_file_no_overwrite(tmp_dir):
    path = os.path.join(tmp_dir, "x.txt")
    dispatch("create_code_file", {"file_path": path, "content": "a"})
    result = dispatch("create_code_file", {"file_path": path, "content": "b"})
    assert "error" in result


def test_read_code_lines_range(tmp_dir):
    path = os.path.join(tmp_dir, "multi.js")
    dispatch("create_code_file", {"file_path": path, "content": "l1\nl2\nl3\nl4\nl5\n"})
    result = dispatch("read_code_lines", {"file_path": path, "start_line": 2, "end_line": 4})
    assert result["content"] == "l2\nl3\nl4\n"
    assert result["total_lines"] == 5


def test_append_code_text(tmp_dir):
    path = os.path.join(tmp_dir, "log.txt")
    dispatch("create_code_file", {"file_path": path, "content": "first"})
    result = dispatch("append_code_text", {"file_path": path, "text": "second"})
    assert result["status"] == "appended"
    read = dispatch("read_code_file", {"file_path": path})
    assert read["content"] == "first\nsecond"


def test_replace_code_text(tmp_dir):
    path = os.path.join(tmp_dir, "conf.json")
    dispatch("create_code_file", {"file_path": path, "content": '{"env": "dev"}'})
    result = dispatch("replace_code_text", {"file_path": path, "find": "dev", "replace": "prod"})
    assert result["replacements"] == 1
    read = dispatch("read_code_file", {"file_path": path})
    assert "prod" in read["content"]


def test_insert_and_delete_code_lines(tmp_dir):
    path = os.path.join(tmp_dir, "list.txt")
    dispatch("create_code_file", {"file_path": path, "content": "a\nb\nd\n"})
    dispatch("insert_code_lines", {"file_path": path, "line_number": 3, "text": "c"})
    read = dispatch("read_code_file", {"file_path": path})
    assert read["content"] == "a\nb\nc\nd\n"

    dispatch("delete_code_lines", {"file_path": path, "start_line": 2, "end_line": 2})
    read2 = dispatch("read_code_file", {"file_path": path})
    assert read2["content"] == "a\nc\nd\n"


def test_list_directory_files(tmp_dir):
    dispatch("create_code_file", {"file_path": os.path.join(tmp_dir, "a.py"), "content": "x"})
    dispatch("create_code_file", {"file_path": os.path.join(tmp_dir, "b.css"), "content": "y"})
    result = dispatch("list_directory_files", {"dir_path": tmp_dir, "extensions": [".py"]})
    assert result["file_count"] == 1
    assert result["files"][0]["extension"] == ".py"


def test_search_in_files(tmp_dir):
    dispatch("create_code_file", {"file_path": os.path.join(tmp_dir, "a.py"), "content": "def foo():\n    pass\n"})
    result = dispatch("search_in_files", {"dir_path": tmp_dir, "query": "def foo"})
    assert result["match_count"] == 1
    assert result["matches"][0]["line_number"] == 1


def test_code_file_not_found(tmp_dir):
    result = dispatch("read_code_file", {"file_path": os.path.join(tmp_dir, "nope.py")})
    assert "error" in result


def test_code_tool_blocks_system_path():
    result = dispatch("read_code_file", {"file_path": "/etc/passwd"})
    assert "error" in result


# ---------- Rasmlar: crop/resize/rotate/create_image (image_tool qo'shimchalari) ----------

def test_crop_image(sample_image, tmp_dir):
    out = os.path.join(tmp_dir, "cropped.png")
    result = dispatch("crop_image", {"file_path": sample_image, "left": 10, "top": 10, "right": 50, "bottom": 40, "save_as": out})
    assert result["width"] == 40
    assert result["height"] == 30
    info = dispatch("get_image_info", {"file_path": out})
    assert info["width"] == 40 and info["height"] == 30


def test_crop_image_invalid_bounds(sample_image):
    result = dispatch("crop_image", {"file_path": sample_image, "left": 0, "top": 0, "right": 9999, "bottom": 9999})
    assert "error" in result


def test_resize_image_keep_aspect(sample_image, tmp_dir):
    out = os.path.join(tmp_dir, "resized.png")
    result = dispatch("resize_image", {"file_path": sample_image, "width": 40, "save_as": out})
    assert result["width"] == 40
    assert result["height"] == 25  # 80x50 -> 40x25, aspect saqlangan


def test_resize_image_no_dims_error(sample_image):
    result = dispatch("resize_image", {"file_path": sample_image})
    assert "error" in result


def test_rotate_image(sample_image, tmp_dir):
    out = os.path.join(tmp_dir, "rotated.png")
    result = dispatch("rotate_image", {"file_path": sample_image, "degrees": 90, "save_as": out})
    assert result["status"] == "rotated"
    info = dispatch("get_image_info", {"file_path": out})
    assert info["width"] == 50 and info["height"] == 80  # 90 gradus, expand=true


def test_create_image(tmp_dir):
    out = os.path.join(tmp_dir, "blank.png")
    result = dispatch("create_image", {"width": 100, "height": 60, "output_path": out, "color": "#00FF00"})
    assert result["status"] == "created"
    info = dispatch("get_image_info", {"file_path": out})
    assert info["width"] == 100 and info["height"] == 60


def test_image_tool_blocks_system_path():
    result = dispatch("crop_image", {"file_path": "/etc/passwd", "left": 0, "top": 0, "right": 10, "bottom": 10})
    assert "error" in result


# ---------- convert_image RGBA -> JPG shaffoflik tuzatishi ----------

def test_convert_rgba_to_jpg_no_black_background(tmp_dir):
    """image_writer.convert_image RGBA'ni JPG'ga o'girganda oq fonga qo'yishi kerak
    (to'g'ridan-to'g'ri .convert('RGB') emas, bu shaffof joylarni qora qilib qo'yardi)."""
    from PIL import Image
    rgba_path = os.path.join(tmp_dir, "transparent.png")
    Image.new("RGBA", (20, 20), (255, 0, 0, 0)).save(rgba_path)  # to'liq shaffof
    out = os.path.join(tmp_dir, "flat.jpg")
    result = dispatch("convert_image", {"file_path": rgba_path, "output_path": out})
    assert result["status"] == "converted"

    with Image.open(out) as img:
        pixel = img.convert("RGB").getpixel((10, 10))
    assert pixel == (255, 255, 255), f"Shaffof piksel oq emas, balki {pixel} (qora fon xatosi qaytgan bo'lishi mumkin)"


# ---------- Internet: SSRF himoyasi (tarmoqsiz ishlaydigan testlar) ----------

def test_resolve_safe_url_blocks_loopback():
    from ms_toolkit.security import resolve_safe_url, UnsafeUrlError
    with pytest.raises(UnsafeUrlError):
        resolve_safe_url("http://127.0.0.1:8000/x")


def test_resolve_safe_url_blocks_link_local():
    from ms_toolkit.security import resolve_safe_url, UnsafeUrlError
    with pytest.raises(UnsafeUrlError):
        resolve_safe_url("http://169.254.169.254/latest/meta-data/")


def test_resolve_safe_url_blocks_private_range():
    from ms_toolkit.security import resolve_safe_url, UnsafeUrlError
    with pytest.raises(UnsafeUrlError):
        resolve_safe_url("http://10.0.0.5/internal")


def test_resolve_safe_url_blocks_non_http_scheme():
    from ms_toolkit.security import resolve_safe_url, UnsafeUrlError
    with pytest.raises(UnsafeUrlError):
        resolve_safe_url("ftp://example.com/file")


def test_resolve_safe_url_allows_public_domain():
    from ms_toolkit.security import resolve_safe_url
    assert resolve_safe_url("https://raw.githubusercontent.com/x") == "https://raw.githubusercontent.com/x"


def test_download_file_blocks_ssrf_via_dispatch(tmp_dir):
    result = dispatch("download_file", {"url": "http://127.0.0.1/secret", "output_path": os.path.join(tmp_dir, "x.txt")})
    assert "error" in result


def test_fetch_url_text_blocks_ssrf_via_dispatch():
    result = dispatch("fetch_url_text", {"url": "http://localhost/admin"})
    assert "error" in result


def test_scrape_page_text_blocks_ssrf_via_dispatch():
    result = dispatch("scrape_page_text", {"url": "http://192.168.1.1/"})
    assert "error" in result


# ---------- get_known_changelog_url (tarmoqsiz, lug'at asosida) ----------

def test_get_known_changelog_url_exact_match():
    result = dispatch("get_known_changelog_url", {"service_name": "telegram bot api"})
    assert result["match"] == "exact"
    assert result["url"] == "https://core.telegram.org/bots/api-changelog"


def test_get_known_changelog_url_case_insensitive():
    result = dispatch("get_known_changelog_url", {"service_name": "Telegram Bot API"})
    assert result["match"] == "exact"


def test_get_known_changelog_url_partial_match():
    result = dispatch("get_known_changelog_url", {"service_name": "telegram"})
    assert result["match"] == "partial"
    assert any("telegram" in s["service"] for s in result["suggestions"])


def test_get_known_changelog_url_no_match():
    result = dispatch("get_known_changelog_url", {"service_name": "some totally unknown thing xyz"})
    assert result["match"] == "none"
    assert "hint" in result


# ---------- Internet: haqiqiy tarmoq talab qiladigan testlar (offline'da avtomatik skip) ----------

def _network_available():
    import socket
    try:
        socket.setdefaulttimeout(3)
        socket.gethostbyname("raw.githubusercontent.com")
        return True
    except OSError:
        return False


_NETWORK_OK = _network_available()
_SKIP_REASON = "Tarmoq mavjud emas yoki bloklangan"


@pytest.mark.skipif(not _NETWORK_OK, reason=_SKIP_REASON)
def test_download_file_real(tmp_dir):
    out = os.path.join(tmp_dir, "readme.md")
    result = dispatch("download_file", {
        "url": "https://raw.githubusercontent.com/muslihiddinlive/ms-file-toolkit/main/README.md",
        "output_path": out,
    })
    assert result["status"] == "downloaded"
    assert os.path.exists(out)
    assert result["size_bytes"] > 0


@pytest.mark.skipif(not _NETWORK_OK, reason=_SKIP_REASON)
def test_fetch_url_text_real():
    result = dispatch("fetch_url_text", {
        "url": "https://raw.githubusercontent.com/muslihiddinlive/ms-file-toolkit/main/README.md",
        "max_chars": 300,
    })
    assert "ms-file-toolkit" in result["text"]


@pytest.mark.skipif(not _NETWORK_OK, reason=_SKIP_REASON)
def test_download_file_size_limit_real(tmp_dir):
    out = os.path.join(tmp_dir, "toosmall.md")
    result = dispatch("download_file", {
        "url": "https://raw.githubusercontent.com/muslihiddinlive/ms-file-toolkit/main/README.md",
        "output_path": out,
        "max_bytes": 10,
    })
    assert "error" in result
    assert not os.path.exists(out)


def _duckduckgo_reachable():
    """DNS emas, haqiqiy HTTP so'rovi orqali tekshiradi — ba'zi konteyner
    muhitlarida DNS ishlaydi, lekin egress proksisi domenni bloklaydi."""
    try:
        r = requests.get("https://html.duckduckgo.com/html/", params={"q": "ping"}, timeout=5)
        return r.status_code != 403 or "allowlist" not in r.text.lower()
    except Exception:
        return False


@pytest.mark.skipif(not _duckduckgo_reachable(), reason="DuckDuckGo domeni bu muhitda ochilmaydi")
def test_search_web_real():
    result = dispatch("search_web", {"query": "Telegram Bot API changelog", "max_results": 5})
    assert "result_count" in result
    assert result["result_count"] >= 1


# ---------- Umumiy: yangi tool'lar ro'yxatga qo'shilganini tasdiqlash ----------

def test_new_tools_registered():
    names = {t["name"] for t in TOOLS}
    expected = {
        "read_code_file", "read_code_lines", "create_code_file", "append_code_text",
        "replace_code_text", "insert_code_lines", "delete_code_lines",
        "list_directory_files", "search_in_files",
        "crop_image", "resize_image", "rotate_image", "create_image",
        "download_file", "fetch_url_text", "scrape_page_text",
        "extract_page_links", "extract_page_images", "search_web", "get_known_changelog_url",
    }
    assert expected.issubset(names)
