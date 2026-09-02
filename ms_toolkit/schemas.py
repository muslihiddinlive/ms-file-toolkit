"""
AI function-calling uchun tool schemalari.

Bu schemalar Anthropic Claude 'tools' formatiga mos.
OpenAI uchun ham deyarli bir xil (faqat "input_schema" -> "parameters" bo'ladi).
"""

TOOLS = [
    # ---------- DOCX ----------
    {
        "name": "read_docx_text",
        "description": "Word (.docx) hujjatidan barcha matnni o'qib beradi.",
        "input_schema": {
            "type": "object",
            "properties": {
                "file_path": {"type": "string", "description": ".docx fayl yo'li"}
            },
            "required": ["file_path"],
        },
    },
    {
        "name": "read_docx_tables",
        "description": "Word (.docx) hujjatidagi barcha jadvallarni o'qib beradi.",
        "input_schema": {
            "type": "object",
            "properties": {
                "file_path": {"type": "string", "description": ".docx fayl yo'li"}
            },
            "required": ["file_path"],
        },
    },
    {
        "name": "get_docx_metadata",
        "description": "Word (.docx) hujjatining metama'lumotlarini (muallif, sarlavha, sana) qaytaradi.",
        "input_schema": {
            "type": "object",
            "properties": {
                "file_path": {"type": "string", "description": ".docx fayl yo'li"}
            },
            "required": ["file_path"],
        },
    },
    # ---------- XLSX ----------
    {
        "name": "get_xlsx_sheet_names",
        "description": "Excel (.xlsx) faylidagi barcha varaq nomlarini qaytaradi.",
        "input_schema": {
            "type": "object",
            "properties": {
                "file_path": {"type": "string", "description": ".xlsx fayl yo'li"}
            },
            "required": ["file_path"],
        },
    },
    {
        "name": "read_xlsx_data",
        "description": "Excel (.xlsx) faylidan ma'lumotlarni jadval ko'rinishida o'qiydi.",
        "input_schema": {
            "type": "object",
            "properties": {
                "file_path": {"type": "string", "description": ".xlsx fayl yo'li"},
                "sheet_name": {
                    "type": "string",
                    "description": "O'qiladigan varaq nomi (ixtiyoriy, bo'lmasa faol varaq)",
                },
                "max_rows": {
                    "type": "integer",
                    "description": "Maksimal o'qiladigan qatorlar soni (default: 100)",
                },
            },
            "required": ["file_path"],
        },
    },
    {
        "name": "get_xlsx_summary",
        "description": "Excel (.xlsx) faylining har bir varag'i uchun o'lcham xulosasini beradi.",
        "input_schema": {
            "type": "object",
            "properties": {
                "file_path": {"type": "string", "description": ".xlsx fayl yo'li"}
            },
            "required": ["file_path"],
        },
    },
    # ---------- PPTX ----------
    {
        "name": "read_pptx_text",
        "description": "PowerPoint (.pptx) taqdimotidagi har bir slayddan matnni ajratib oladi.",
        "input_schema": {
            "type": "object",
            "properties": {
                "file_path": {"type": "string", "description": ".pptx fayl yo'li"}
            },
            "required": ["file_path"],
        },
    },
    {
        "name": "get_pptx_slide_count",
        "description": "PowerPoint (.pptx) taqdimotidagi slaydlar sonini qaytaradi.",
        "input_schema": {
            "type": "object",
            "properties": {
                "file_path": {"type": "string", "description": ".pptx fayl yo'li"}
            },
            "required": ["file_path"],
        },
    },
    {
        "name": "extract_pptx_notes",
        "description": "PowerPoint (.pptx) taqdimotidagi har bir slaydning speaker notes matnini oladi.",
        "input_schema": {
            "type": "object",
            "properties": {
                "file_path": {"type": "string", "description": ".pptx fayl yo'li"}
            },
            "required": ["file_path"],
        },
    },
]
