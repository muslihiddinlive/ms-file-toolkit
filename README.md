# ms-file-toolkit

Microsoft fayllarni (Word, Excel, PowerPoint) tahlil qiluvchi Python toolkit — **AI function calling** (Claude, GPT va h.k.) uchun tayyor tool schemalari bilan.

## O'rnatish

```bash
pip install -r requirements.txt
```

## Qo'llab-quvvatlanadigan formatlar

| Format | Funksiyalar |
|---|---|
| `.docx` | matn o'qish, jadvallarni o'qish, metama'lumot |
| `.xlsx` | varaq nomlari, ma'lumotlarni o'qish, o'lcham xulosasi |
| `.pptx` | slayd matnlari, slaydlar soni, speaker notes |

## Tez boshlash (function calling bilan)

```python
from ms_toolkit import TOOLS, dispatch
import anthropic

client = anthropic.Anthropic()

response = client.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=1024,
    tools=TOOLS,
    messages=[{"role": "user", "content": "test.xlsx faylida nechta qator bor?"}],
)

for block in response.content:
    if block.type == "tool_use":
        result = dispatch(block.name, block.input)
        print(result)
```

To'liq ishlaydigan misol uchun [`example.py`](example.py) ga qarang.

## To'g'ridan-to'g'ri (AI'siz) ishlatish

```python
from ms_toolkit.docx_tool import read_docx_text
from ms_toolkit.xlsx_tool import read_xlsx_data
from ms_toolkit.pptx_tool import read_pptx_text

print(read_docx_text("hujjat.docx"))
print(read_xlsx_data("jadval.xlsx"))
print(read_pptx_text("slaydlar.pptx"))
```

## Struktura

```
ms_toolkit/
  __init__.py      # TOOLS, dispatch export qiladi
  docx_tool.py      # Word funksiyalari
  xlsx_tool.py      # Excel funksiyalari
  pptx_tool.py      # PowerPoint funksiyalari
  schemas.py        # AI uchun tool schemalari (input_schema formatida)
  registry.py       # tool_name -> funksiya dispatcher
example.py          # Claude API bilan to'liq ishlaydigan misol
```

## Rejalashtirilgan (keyingi bosqichlar)

- [ ] `.doc` / `.xls` / `.ppt` (eski formatlar) qo'llab-quvvatlash
- [ ] Fayl yozish/generatsiya funksiyalari (hozircha faqat o'qish)
- [ ] PyPI'ga paket sifatida chiqarish
