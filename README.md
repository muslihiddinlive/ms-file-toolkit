# ms-file-toolkit

Microsoft fayllarni va PDF'larni **o'qish va yozish** uchun Python toolkit — **AI function calling** (Claude, GPT va h.k.) uchun tayyor tool schemalari, **xavfsizlik nazorati**, **avtomatik format aniqlash** va **CLI** bilan.

## O'rnatish

```bash
pip install -r requirements.txt
```

Yoki paket sifatida (PyPI'ga chiqarishga tayyor, CLI bilan birga o'rnatiladi):

```bash
pip install -e ".[ai,dev]"
```

## Qo'llab-quvvatlanadigan formatlar

| Format                        | O'qish                                        | Yozish                                                                             |
| ------------------------------ | ------------------------------------------------ | --------------------------------------------------------------------------------------- |
| `.docx`                         | matn, jadvallar, metama'lumot                     | yaratish, matn qo'shish/almashtirish, sarlavha, rasm, sahifa bo'linishi                |
| `.xlsx`                         | varaq nomlari, ma'lumotlar, o'lcham xulosasi      | yaratish, varaq/qator qo'shish, formula, formatlash, panellarni muzlatish, **diagramma** |
| `.pptx`                         | slayd matnlari, slaydlar soni, notes              | yaratish, slayd/rasm qo'shish, fon rangi, **diagramma**                                 |
| `.pdf`                          | matn, jadvallar, metama'lumot                     | yaratish, birlashtirish (merge), bo'lish (split)                                        |
| `.doc` / `.xls` / `.ppt` (eski) | `read_legacy_file` — LibreOffice orqali            | —                                                                                          |
| **Har qanday (avtomatik)**       | `read_any_file`, `get_file_info`                   | —                                                                                          |

> Eski formatlar uchun tizimda **LibreOffice** (`soffice`) kerak: `apt-get install libreoffice`

## Xavfsizlik

Fayl yo'llari AI tomonidan tanlanadi, shuning uchun **path traversal** himoyasi o'rnatilgan (`ms_toolkit/security.py`):

```bash
export MS_TOOLKIT_BASE_DIR=/home/bot/user_files   # faqat shu papka ichidagi fayllarga ruxsat
```

```python
dispatch("read_docx_text", {"file_path": "../../etc/passwd"})
# -> {"error": "Xavfsizlik xatosi: ..."}
```

## CLI (terminal orqali)

```bash
ms-toolkit list                                                    # barcha tool'lar ro'yxati
ms-toolkit run create_docx '{"file_path": "a.docx", "title": "Salom", "overwrite": true}'
ms-toolkit run read_any_file '{"file_path": "hujjat.xlsx"}'
```

## Tez boshlash (API kalitisiz)

```bash
pip install -e ".[dev]"
pytest tests/ -v          # 23 ta test
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
        print(dispatch(block.name, block.input))
```

To'liq agentic misol: [`example.py`](example.py).

## Diagramma qo'shish misoli

```python
from ms_toolkit import dispatch

dispatch("add_xlsx_chart", {
    "file_path": "hisobot.xlsx", "chart_type": "bar",
    "data_range": "B1:B5", "categories_range": "A2:A5", "title": "Oylik savdo",
})

dispatch("add_pptx_chart", {
    "file_path": "taqdimot.pptx", "chart_type": "pie",
    "categories": ["A", "B", "C"], "series": {"2026": [40, 35, 25]},
})
```

## Barcha tool'lar ro'yxati (36 ta)

**DOCX (9):** `read_docx_text`, `read_docx_tables`, `get_docx_metadata`, `create_docx`, `append_docx_text`, `replace_docx_text`, `add_docx_heading`, `add_docx_image`, `add_docx_page_break`
**XLSX (10):** `get_xlsx_sheet_names`, `read_xlsx_data`, `get_xlsx_summary`, `create_xlsx`, `add_xlsx_sheet`, `append_xlsx_rows`, `set_xlsx_formula`, `format_xlsx_cells`, `freeze_xlsx_panes`, `add_xlsx_chart`
**PPTX (8):** `read_pptx_text`, `get_pptx_slide_count`, `extract_pptx_notes`, `create_pptx`, `add_pptx_slide`, `add_pptx_image`, `set_pptx_background_color`, `add_pptx_chart`
**PDF (6):** `read_pdf_text`, `read_pdf_tables`, `get_pdf_metadata`, `create_pdf`, `merge_pdfs`, `split_pdf`
**Eski formatlar (1):** `read_legacy_file`
**Auto-detect (2):** `read_any_file`, `get_file_info`

## Struktura

```
ms_toolkit/
  __init__.py       # TOOLS, dispatch export qiladi
  docx_tool.py / docx_writer.py     # Word
  xlsx_tool.py / xlsx_writer.py     # Excel (+ chart)
  pptx_tool.py / pptx_writer.py     # PowerPoint (+ chart)
  pdf_tool.py / pdf_writer.py        # PDF
  legacy_tool.py                       # Eski formatlar
  auto_tool.py                          # Avtomatik format aniqlash
  security.py                            # Path-traversal himoyasi
  cli.py                                   # Terminal interfeysi (ms-toolkit)
  schemas.py                                # AI uchun tool schemalari
  registry.py                                 # tool_name -> funksiya dispatcher
example.py, test_toolkit.py, tests/            # Misollar va testlar
pyproject.toml                                    # pip/PyPI paketlash + CLI entry point
```

## PyPI'ga chiqarish

```bash
pip install build twine
python -m build
twine upload dist/*
```

## Litsenziya

MIT
