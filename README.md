# 🛠️ ms-file-toolkit

[![PyPI version](https://badge.fury.io/py/ms-file-toolkit.svg)](https://pypi.org/project/ms-file-toolkit/)
[![Python Version](https://img.shields.io/pypi/pyversions/ms-file-toolkit.svg)](https://pypi.org/project/ms-file-toolkit/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Tests](https://img.shields.io/badge/Tests-23%20Passed-brightgreen.svg)]()
[![PyPI Downloads](https://img.shields.io/pypi/dm/ms-file-toolkit.svg)](https://pypi.org/project/ms-file-toolkit/)

**`ms-file-toolkit`** is a complete, secure, production-grade file manipulation library for Python. Read, write, convert, and manage **Word (DOCX)**, **Excel (XLSX)**, **PowerPoint (PPTX)**, and **PDF** documents through a single unified interface — with a CLI, built-in path-traversal protection, and ready-made AI function-calling schemas for Claude, GPT, and other LLM agents.

Originally built to give AI agents (like Claude) safe, structured read/write access to Office and PDF files without shelling out to fragile scripts — now usable as a standalone library or CLI tool for any Python project.

```bash
pip install ms-file-toolkit
```

---

## ⚡ Features

| Format | Functions | Highlights |
|---|---|---|
| **📄 Word (`.docx`)** | 9 | Read text/tables/metadata · create documents · append/replace text · headings · insert images · page breaks |
| **📊 Excel (`.xlsx`)** | 10 | Read sheets/data/summary · create workbooks · formulas (`=SUM(...)`) · cell styling (bold, fill color) · frozen panes · charts (bar/line/pie) |
| **🎞️ PowerPoint (`.pptx`)** | 8 | Read slide text/notes · build decks from scratch · insert slides/images · background color · charts (bar/line/pie) |
| **📕 PDF** | 6 | Extract text/tables · read metadata · create PDFs · merge · split into pages |
| **🕰️ Legacy (`.doc`/`.xls`/`.ppt`)** | 1 | Automatic conversion via LibreOffice |
| **🔮 Smart routing** | 2 | `read_any_file()` auto-detects format · `get_file_info()` for quick metadata |

**36 functions in total**, all exposed as both plain Python calls and AI-agent tool schemas.

Also included:

- 🛡️ **Built-in security** — every `file_path` is validated against directory-traversal attacks (`../../etc/passwd` is rejected automatically); optionally sandbox all I/O to one folder with `MS_TOOLKIT_BASE_DIR`.
- 🤖 **AI-agent ready** — `TOOLS` exports pre-built JSON schemas compatible with Anthropic's tool-use / Claude API and OpenAI function calling out of the box.
- 💻 **CLI included** — run any function straight from your terminal: `ms-toolkit run <function> '<json-args>'`.
- ✅ **Tested** — 23 pytest cases covering every function, security edge cases, and the CLI.

---

## 📦 Installation

```bash
pip install ms-file-toolkit
```

With AI (Claude API) integration extras:

```bash
pip install "ms-file-toolkit[ai]"
```

For development (running the test suite):

```bash
pip install "ms-file-toolkit[dev]"
```

> 📌 Legacy format support (`.doc`, `.xls`, `.ppt`) requires **LibreOffice** to be installed on the system (`apt-get install libreoffice` on Debian/Ubuntu).

---

## 🚀 Quick start

### As a plain Python library

```python
from ms_toolkit.docx_writer import create_docx, add_docx_image
from ms_toolkit.xlsx_writer import create_xlsx, set_xlsx_formula, add_xlsx_chart
from ms_toolkit.pptx_writer import create_pptx, add_pptx_chart
from ms_toolkit.pdf_writer import create_pdf, merge_pdfs

create_docx("report.docx", title="Monthly Report", paragraphs=["Q1 summary..."])
add_docx_image("report.docx", "logo.png", width_inches=2.0)

create_xlsx("sales.xlsx", headers=["Month", "Revenue"], rows=[["Jan", 1000], ["Feb", 1500]])
set_xlsx_formula("sales.xlsx", "C1", "=SUM(B:B)")
add_xlsx_chart("sales.xlsx", chart_type="bar", data_range="B1:B3", categories_range="A2:A3")

create_pdf("summary.pdf", title="Summary", paragraphs=["Everything looks good."])
```

### Via the tool dispatcher (great for AI agents)

```python
from ms_toolkit import TOOLS, dispatch

result = dispatch("read_any_file", {"file_path": "unknown_document.xlsx"})
print(result)  # auto-detects it's XLSX and reads it
```

### With Claude (Anthropic) function calling

```python
import anthropic
from ms_toolkit import TOOLS, dispatch

client = anthropic.Anthropic()

response = client.messages.create(
    model="claude-sonnet-5",
    max_tokens=1024,
    tools=TOOLS,
    messages=[{"role": "user", "content": "How many rows are in sales.xlsx?"}],
)

for block in response.content:
    if block.type == "tool_use":
        print(dispatch(block.name, block.input))
```

See [`example.py`](example.py) for a full agentic tool-use loop.

### From the command line

```bash
ms-toolkit list
ms-toolkit run create_docx '{"file_path": "hello.docx", "title": "Hi", "overwrite": true}'
ms-toolkit run read_any_file '{"file_path": "hello.docx"}'
```

---

## 🛡️ Security

Since file paths in an AI-agent context are often chosen by the model itself, every path-like argument (`file_path`, `image_path`, `output_path`, `output_dir`, lists of paths) is validated before use:

- Null bytes are rejected outright.
- By default, paths resolving into sensitive system directories (`/etc/`, `/root/`, `/proc/`, etc.) are blocked.
- Set `MS_TOOLKIT_BASE_DIR` to restrict **all** file operations to a single directory — recommended for any multi-user or bot deployment:

```bash
export MS_TOOLKIT_BASE_DIR=/srv/app/user_files
```

```python
dispatch("read_docx_text", {"file_path": "../../etc/passwd"})
# -> {"error": "Xavfsizlik xatosi: ..."}  (path rejected)
```

---

## 📚 Full function list (36)

**DOCX:** `read_docx_text`, `read_docx_tables`, `get_docx_metadata`, `create_docx`, `append_docx_text`, `replace_docx_text`, `add_docx_heading`, `add_docx_image`, `add_docx_page_break`

**XLSX:** `get_xlsx_sheet_names`, `read_xlsx_data`, `get_xlsx_summary`, `create_xlsx`, `add_xlsx_sheet`, `append_xlsx_rows`, `set_xlsx_formula`, `format_xlsx_cells`, `freeze_xlsx_panes`, `add_xlsx_chart`

**PPTX:** `read_pptx_text`, `get_pptx_slide_count`, `extract_pptx_notes`, `create_pptx`, `add_pptx_slide`, `add_pptx_image`, `set_pptx_background_color`, `add_pptx_chart`

**PDF:** `read_pdf_text`, `read_pdf_tables`, `get_pdf_metadata`, `create_pdf`, `merge_pdfs`, `split_pdf`

**Legacy:** `read_legacy_file`

**Auto-detect:** `read_any_file`, `get_file_info`

---

## 🧪 Testing

```bash
pip install "ms-file-toolkit[dev]"
git clone https://github.com/muslihiddinlive/ms-file-toolkit.git
cd ms-file-toolkit
pytest tests/ -v
```

23 tests cover every function, path-traversal defenses, and the CLI.

---

## 📁 Project structure

```
ms_toolkit/
  __init__.py        # exports TOOLS, dispatch, REGISTRY
  docx_tool.py / docx_writer.py    # Word
  xlsx_tool.py / xlsx_writer.py    # Excel (+ charts)
  pptx_tool.py / pptx_writer.py    # PowerPoint (+ charts)
  pdf_tool.py / pdf_writer.py      # PDF
  legacy_tool.py       # .doc/.xls/.ppt via LibreOffice
  auto_tool.py          # format auto-detection
  security.py            # path-traversal protection
  cli.py                   # `ms-toolkit` command
  schemas.py                # AI tool schemas
  registry.py                 # tool_name -> function dispatcher
example.py                     # full Claude API agentic example
tests/                           # pytest suite
pyproject.toml                     # packaging + CLI entry point
```

---

## 🤝 Contributing

Issues and pull requests are welcome. Please run the test suite before submitting a PR.

## 📄 License

MIT — see [LICENSE](LICENSE) for details.
