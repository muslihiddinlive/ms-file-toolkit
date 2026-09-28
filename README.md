# ms-file-toolkit

Microsoft, OpenDocument va PDF fayllarni **o'qish va yozish** uchun Python toolkit — **AI function calling** (Claude, GPT va h.k.) uchun tayyor tool schemalari, **xavfsizlik nazorati**, **avtomatik format aniqlash**, **format konvertatsiya** va **CLI** bilan.

## O'rnatish

```bash
pip install -r requirements.txt
```

Yoki paket sifatida:

```bash
pip install -e ".[ai,dev]"
```

## Qo'llab-quvvatlanadigan formatlar

| Format | O'qish | Yozish |
| --- | --- | --- |
| `.docx` | matn, jadvallar, metama'lumot | yaratish, matn qo'shish/almashtirish, sarlavha, rasm, sahifa bo'linishi |
| `.xlsx` | varaq nomlari, ma'lumotlar, o'lcham xulosasi | yaratish, varaq/qator qo'shish, formula, formatlash, panellarni muzlatish, diagramma |
| `.pptx` | slayd matnlari, slaydlar soni, notes | yaratish, slayd/rasm qo'shish, fon rangi, diagramma |
| `.pdf` | matn, jadvallar, metama'lumot, **ichki rasmlarni chiqarish** | yaratish, **rasmlardan yaratish**, birlashtirish, bo'lish |
| `.csv` | qatorlar, sarlavha, o'lcham xulosasi | yaratish, qator qo'shish |
| `.odt` (OpenDocument Text) | matn | yaratish (sarlavha + paragraflar) |
| `.ods` (OpenDocument Spreadsheet) | varaq nomlari, ma'lumotlar | yaratish |
| `.odp` (OpenDocument Presentation) | slayd matnlari, slaydlar soni | yaratish |
| Rasm (`.png`/`.jpg`/...) | o'lcham/format ma'lumoti, **OCR** | format/o'lcham konvertatsiya, thumbnail |
| **QR kod** | **rasmdan o'qish** (lokal) | **yaratish** (matn, havola, WiFi, kontakt, SMS, email, telefon, Telegram) |
| `.zip` | tarkib ro'yxati, fayl o'qish | arxiv yaratish, chiqarish (zip-slip himoyasi bilan) |
| `.doc` / `.xls` / `.ppt` (eski) | `read_legacy_file` (LibreOffice orqali) | — |
| Har qanday (avtomatik) | `read_any_file`, `get_file_info` | — |

> Eski formatlar va konvertatsiya uchun tizimda **LibreOffice** (`soffice`) kerak: `apt-get install libreoffice`
> OCR (`read_image_text`) uchun **Tesseract** kerak: `apt-get install tesseract-ocr`

## Format konvertatsiya

```python
from ms_toolkit import dispatch

dispatch("convert_docx_to_pdf", {"file_path": "hujjat.docx", "output_path": "hujjat.pdf"})
dispatch("convert_pptx_to_images", {"file_path": "taqdimot.pptx", "output_dir": "slaydlar/"})
dispatch("convert_pdf_to_images", {"file_path": "hujjat.pdf", "output_dir": "sahifalar/"})
dispatch("convert_xlsx_to_csv", {"file_path": "hisobot.xlsx", "output_dir": "csv_export/"})
```

`convert_pptx_to_images` va `convert_pdf_to_images` tashqi system-binary talab qilmaydi (PyMuPDF orqali); `convert_*_to_pdf` funksiyalari LibreOffice orqali ishlaydi.

## Telegram guruh moderatsiyasi

[`tg-mod-functions`](https://pypi.org/project/tg-mod-functions/) ning 25 ta moderatsiya tool'i
(ban, mute, warn, promote, join-request, lockdown, reaction va h.k.) fayl tool'lari bilan bir xil
`dispatch()` orqali ishlaydi:

`pip install ms-file-toolkit` hammasini birga o'rnatadi (alohida extra kerak emas).

```python
from aiogram import Bot
from ms_toolkit import TOOLS, dispatch, configure_telegram, telegram_tool_schemas

bot = Bot(token="...")
configure_telegram(
    bot,
    protected_user_ids={123456789},   # AI hech qachon tegolmaydigan akkauntlar
    warns_path="warns.json",          # ogohlantirishlar restart'dan keyin saqlanadi
)

all_tools = TOOLS + telegram_tool_schemas()   # Claude'ga beriladigan to'liq ro'yxat
dispatch("ban_user", {"chat_id": -100123, "user_id": 42, "minutes": 60})
# -> {"ok": True, "message": "..."}
```

Guruh yaratuvchisi (creator) va `protected_user_ids` dagi akkauntlar har doim himoyalangan: AI
adashsa yoki aldansa ham ularga ban/mute/kick/warn/demote qilib bo'lmaydi.
`configure_telegram()` chaqirilmaguncha bu tool'lar yoqilmaydi va fayl tool'lariga ta'sir qilmaydi.
Python 3.10+ talab qilinadi.

## PDF va QR (v0.8.0)

```python
from ms_toolkit import dispatch

# Rasmlardan PDF (har rasm — alohida sahifa). page_size: "original" (default) yoki "a4"
dispatch("create_pdf_from_images", {"image_paths": ["1.jpg", "2.png"], "output_path": "natija.pdf", "page_size": "a4"})

# PDF ICHIDAGI rasmlarni chiqarish (takroriylar bir marta, juda kichiklari o'tkaziladi)
dispatch("extract_pdf_images", {"file_path": "hujjat.pdf", "output_dir": "rasmlar/"})

# PDF birlashtirish
dispatch("merge_pdfs", {"file_paths": ["a.pdf", "b.pdf"], "output_path": "birga.pdf"})

# QR yaratish: text | url | phone | email | wifi | sms | vcard | telegram
dispatch("create_qr_code", {"output_path": "wifi.png", "data": "UyWifi", "qr_type": "wifi", "password": "12345678"})
dispatch("create_qr_code", {"output_path": "kontakt.png", "data": "Ali Valiyev", "qr_type": "vcard", "phone": "998901112233"})

# QR o'qish (rasm/foto, internetsiz)
dispatch("read_qr_code", {"image_path": "foto.jpg"})
# -> {"found": True, "codes": [{"text": "WIFI:S:UyWifi;...", "format": "QRCode", "kind": "wifi"}]}
```

QR yaratish `segno` (sof Python), o'qish `zxing-cpp` (tayyor wheel) orqali — tashqi API va qo'shimcha tizim kutubxonalari
kerak emas. WiFi nomi/parolidagi maxsus belgilar (`; , : " \`) avtomatik escape qilinadi.

## Xavfsizlik

Fayl yo'llari AI tomonidan tanlanadi, shuning uchun **path traversal** himoyasi bor (`ms_toolkit/security.py`) — bu himoya yangi qo'shilgan barcha tool'larga (CSV, OpenDocument, rasm, arxiv, konvertatsiya) avtomatik qo'llaniladi:

```bash
export MS_TOOLKIT_BASE_DIR=/home/bot/user_files
```

```python
dispatch("read_docx_text", {"file_path": "../../etc/passwd"})
# -> {"error": "Xavfsizlik xatosi: ..."}
```

ZIP arxivlarni chiqarishda (`extract_archive`) qo'shimcha **zip-slip** himoyasi bor — arxiv ichidagi hech qanday yozuv `output_dir` tashqarisiga chiqib keta olmaydi.

## CLI

```bash
ms-toolkit list
ms-toolkit run create_docx '{"file_path": "a.docx", "title": "Salom", "overwrite": true}'
ms-toolkit run read_any_file '{"file_path": "hujjat.xlsx"}'
```

## Testlar

```bash
pip install -e ".[dev]"
pytest tests/ -v          # 40 ta test (23 asosiy + 17 kengaytirilgan)
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

## Barcha tool'lar ro'yxati (62 ta)

- **DOCX (9):** `read_docx_text`, `read_docx_tables`, `get_docx_metadata`, `create_docx`, `append_docx_text`, `replace_docx_text`, `add_docx_heading`, `add_docx_image`, `add_docx_page_break`
- **XLSX (10):** `get_xlsx_sheet_names`, `read_xlsx_data`, `get_xlsx_summary`, `create_xlsx`, `add_xlsx_sheet`, `append_xlsx_rows`, `set_xlsx_formula`, `format_xlsx_cells`, `freeze_xlsx_panes`, `add_xlsx_chart`
- **PPTX (8):** `read_pptx_text`, `get_pptx_slide_count`, `extract_pptx_notes`, `create_pptx`, `add_pptx_slide`, `add_pptx_image`, `set_pptx_background_color`, `add_pptx_chart`
- **PDF (8):** `read_pdf_text`, `read_pdf_tables`, `get_pdf_metadata`, `extract_pdf_images`, `create_pdf`, `create_pdf_from_images`, `merge_pdfs`, `split_pdf`
- **QR (2):** `create_qr_code`, `read_qr_code`
- **CSV (4):** `read_csv_data`, `get_csv_summary`, `create_csv`, `append_csv_rows`
- **OpenDocument (8):** `read_odt_text`, `get_ods_sheet_names`, `read_ods_data`, `read_odp_text`, `get_odp_slide_count`, `create_odt`, `create_ods`, `create_odp`
- **Rasm (4):** `get_image_info`, `read_image_text`, `convert_image`, `create_thumbnail`
- **Arxiv (4):** `list_archive_contents`, `read_archive_file`, `create_archive`, `extract_archive`
- **Konvertatsiya (6):** `convert_docx_to_pdf`, `convert_pptx_to_pdf`, `convert_xlsx_to_pdf`, `convert_pdf_to_images`, `convert_pptx_to_images`, `convert_xlsx_to_csv`
- **Eski formatlar (1):** `read_legacy_file`
- **Auto-detect (2):** `read_any_file`, `get_file_info`

## Struktura

```
ms_toolkit/
  __init__.py
  docx_tool.py / docx_writer.py
  xlsx_tool.py / xlsx_writer.py
  pptx_tool.py / pptx_writer.py
  pdf_tool.py / pdf_writer.py
  csv_tool.py / csv_writer.py
  opendoc_tool.py / opendoc_writer.py   # .odt/.ods/.odp
  image_tool.py / image_writer.py       # rasm + OCR
  archive_tool.py / archive_writer.py   # ZIP
  convert_tool.py                       # format konvertatsiya
  legacy_tool.py
  auto_tool.py
  security.py
  cli.py
  schemas.py
  registry.py
tests/
pyproject.toml
requirements.txt
```

## Litsenziya

MIT
