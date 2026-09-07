# ms-file-toolkit

Microsoft fayllarni (Word, Excel, PowerPoint) **o'qish va yozish** uchun Python toolkit — **AI function calling** (Claude, GPT va h.k.) uchun tayyor tool schemalari, **xavfsizlik nazorati** va **avtomatik format aniqlash** bilan.

## O'rnatish

```bash
pip install -r requirements.txt
```

Yoki paket sifatida (PyPI'ga chiqarishga tayyor):

```bash
pip install -e .              # asosiy
pip install -e ".[ai,dev]"     # + Claude API demo + testlar uchun
```

## Qo'llab-quvvatlanadigan formatlar

| Format                        | O'qish                                    | Yozish                                                                         |
| ------------------------------ | -------------------------------------------- | --------------------------------------------------------------------------------- |
| `.docx`                         | matn, jadvallar, metama'lumot                | yaratish, matn qo'shish/almashtirish, sarlavha, rasm, sahifa bo'linishi           |
| `.xlsx`                         | varaq nomlari, ma'lumotlar, o'lcham xulosasi | yaratish, varaq/qator qo'shish, formula, katak formatlash, panellarni muzlatish  |
| `.pptx`                         | slayd matnlari, slaydlar soni, notes         | yaratish, slayd/rasm qo'shish, fon rangi                                          |
| `.doc` / `.xls` / `.ppt` (eski) | `read_legacy_file` — LibreOffice orqali      | —                                                                                    |
| **Har qanday (avtomatik)**       | `read_any_file`, `get_file_info`             | —                                                                                    |

> Eski formatlar uchun tizimda **LibreOffice** (`soffice`) kerak: `apt-get install libreoffice`

## Xavfsizlik

Fayl yo'llari AI tomonidan tanlanadi, shuning uchun **path traversal** himoyasi o'rnatilgan (`ms_toolkit/security.py`):

- Standart holatda `/etc/`, `/root/`, `/proc/` kabi tizim papkalari bloklanadi.
- Kuchliroq cheklov uchun `MS_TOOLKIT_BASE_DIR` muhit o'zgaruvchisini o'rnating — shunda **faqat shu papka ichidagi** fayllarga ruxsat beriladi:

```bash
export MS_TOOLKIT_BASE_DIR=/home/bot/user_files
```

```python
from ms_toolkit import dispatch
dispatch("read_docx_text", {"file_path": "../../etc/passwd"})
# -> {"error": "Xavfsizlik xatosi: ..."}
```

## Tez boshlash (API kalitisiz)

```bash
pip install -e ".[dev]"
pytest tests/ -v          # 15 ta test — barcha tool + xavfsizlik + auto-detect
python test_toolkit.py    # tezkor smoke-test
```

## Function calling bilan (Claude API)

```python
from ms_toolkit import TOOLS, dispatch
import anthropic

client = anthropic.Anthropic()

response = client.messages.create(
    model="claude-sonnet-5",
    max_tokens=1024,
    tools=TOOLS,
    messages=[{"role": "user", "content": "test.xlsx faylida nechta qator bor?"}],
)

for block in response.content:
    if block.type == "tool_use":
        result = dispatch(block.name, block.input)
        print(result)
```

To'liq agentic misol uchun [`example.py`](example.py):

```bash
export ANTHROPIC_API_KEY=...
python example.py "/tmp/hisobot.docx yarat, sarlavhasi 'Hisobot' bo'lsin"
```

## Auto-detect (fayl turini o'zi aniqlaydi)

```python
from ms_toolkit import dispatch

info = dispatch("get_file_info", {"file_path": "noma_malum.docx"})
# {"exists": true, "extension": ".docx", "detected_type": "docx", "size_bytes": 12345}

result = dispatch("read_any_file", {"file_path": "noma_malum.docx"})
# avtomatik read_docx_text() ni chaqiradi
```

## To'g'ridan-to'g'ri (AI'siz) ishlatish

```python
from ms_toolkit.docx_writer import create_docx, add_docx_image
from ms_toolkit.xlsx_writer import create_xlsx, set_xlsx_formula
from ms_toolkit.pptx_writer import create_pptx, add_pptx_image

create_docx("hujjat.docx", title="Sarlavha", paragraphs=["Birinchi paragraf."])
add_docx_image("hujjat.docx", "logo.png", width_inches=2.0)

create_xlsx("jadval.xlsx", headers=["Ism", "Yosh"], rows=[["Ali", 25]])
set_xlsx_formula("jadval.xlsx", "C1", "=SUM(B:B)")

create_pptx("slaydlar.pptx", title="Taqdimot")
add_pptx_image("slaydlar.pptx", "logo.png")
```

## Barcha tool'lar ro'yxati (28 ta)

**DOCX (9):** `read_docx_text`, `read_docx_tables`, `get_docx_metadata`, `create_docx`, `append_docx_text`, `replace_docx_text`, `add_docx_heading`, `add_docx_image`, `add_docx_page_break`
**XLSX (9):** `get_xlsx_sheet_names`, `read_xlsx_data`, `get_xlsx_summary`, `create_xlsx`, `add_xlsx_sheet`, `append_xlsx_rows`, `set_xlsx_formula`, `format_xlsx_cells`, `freeze_xlsx_panes`
**PPTX (7):** `read_pptx_text`, `get_pptx_slide_count`, `extract_pptx_notes`, `create_pptx`, `add_pptx_slide`, `add_pptx_image`, `set_pptx_background_color`
**Eski formatlar (1):** `read_legacy_file`
**Auto-detect (2):** `read_any_file`, `get_file_info`

## Struktura

```
ms_toolkit/
  __init__.py       # TOOLS, dispatch export qiladi
  docx_tool.py       # Word o'qish
  docx_writer.py      # Word yozish (matn, jadval, sarlavha, rasm, page break)
  xlsx_tool.py         # Excel o'qish
  xlsx_writer.py        # Excel yozish (formula, formatlash, freeze panes)
  pptx_tool.py           # PowerPoint o'qish
  pptx_writer.py          # PowerPoint yozish (rasm, fon rangi)
  legacy_tool.py           # Eski formatlar konvertatsiyasi
  auto_tool.py              # Avtomatik format aniqlash
  security.py                # Path-traversal himoyasi
  schemas.py                  # AI uchun tool schemalari
  registry.py                  # tool_name -> funksiya dispatcher (xavfsizlik bilan)
example.py                      # Claude API bilan to'liq agentic misol
test_toolkit.py                   # API kalitisiz tezkor smoke-test
tests/test_toolkit.py               # To'liq pytest to'plami (15 test)
pyproject.toml                       # pip/PyPI paketlash
```

## PyPI'ga chiqarish

```bash
pip install build twine
python -m build
twine upload dist/*
```

## Litsenziya

MIT
