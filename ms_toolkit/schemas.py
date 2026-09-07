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
    {
        "name": "create_docx",
        "description": "Yangi Word (.docx) hujjat yaratadi — sarlavha, paragraflar va ixtiyoriy jadval bilan.",
        "input_schema": {
            "type": "object",
            "properties": {
                "file_path": {"type": "string", "description": "Yaratiladigan .docx fayl yo'li"},
                "title": {"type": "string", "description": "Hujjat sarlavhasi (ixtiyoriy)"},
                "paragraphs": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Matn paragraflari ro'yxati (ixtiyoriy)",
                },
                "table_data": {
                    "type": "array",
                    "items": {"type": "array", "items": {"type": "string"}},
                    "description": "Jadval uchun 2-o'lchamli ro'yxat, birinchi qator sarlavha (ixtiyoriy)",
                },
                "overwrite": {"type": "boolean", "description": "Fayl mavjud bo'lsa, ustiga yozish (default: false)"},
            },
            "required": ["file_path"],
        },
    },
    {
        "name": "append_docx_text",
        "description": "Mavjud Word (.docx) hujjatining oxiriga yangi paragraf matn qo'shadi.",
        "input_schema": {
            "type": "object",
            "properties": {
                "file_path": {"type": "string", "description": ".docx fayl yo'li"},
                "text": {"type": "string", "description": "Qo'shiladigan matn"},
                "bold": {"type": "boolean", "description": "Matnni qalin qilib qo'shish (default: false)"},
            },
            "required": ["file_path", "text"],
        },
    },
    {
        "name": "replace_docx_text",
        "description": "Word (.docx) hujjatidagi barcha berilgan matnni boshqasi bilan almashtiradi.",
        "input_schema": {
            "type": "object",
            "properties": {
                "file_path": {"type": "string", "description": ".docx fayl yo'li"},
                "find": {"type": "string", "description": "Qidiriladigan matn"},
                "replace": {"type": "string", "description": "Almashtiriladigan matn"},
                "save_as": {"type": "string", "description": "Yangi fayl sifatida saqlash yo'li (ixtiyoriy)"},
            },
            "required": ["file_path", "find", "replace"],
        },
    },
    {
        "name": "add_docx_heading",
        "description": "Mavjud Word (.docx) hujjatiga sarlavha (heading, 1-9 daraja) qo'shadi.",
        "input_schema": {
            "type": "object",
            "properties": {
                "file_path": {"type": "string", "description": ".docx fayl yo'li"},
                "text": {"type": "string", "description": "Sarlavha matni"},
                "level": {"type": "integer", "description": "Sarlavha darajasi 1-9 (default: 1)"},
            },
            "required": ["file_path", "text"],
        },
    },
    {
        "name": "add_docx_image",
        "description": "Mavjud Word (.docx) hujjatining oxiriga rasm qo'shadi.",
        "input_schema": {
            "type": "object",
            "properties": {
                "file_path": {"type": "string", "description": ".docx fayl yo'li"},
                "image_path": {"type": "string", "description": "Qo'shiladigan rasm fayli yo'li"},
                "width_inches": {"type": "number", "description": "Rasm kengligi dyuymda (default: 6.0)"},
            },
            "required": ["file_path", "image_path"],
        },
    },
    {
        "name": "add_docx_page_break",
        "description": "Mavjud Word (.docx) hujjatining oxiriga sahifa bo'linishi (page break) qo'shadi.",
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
    {
        "name": "create_xlsx",
        "description": "Yangi Excel (.xlsx) fayl yaratadi — sarlavhalar va qatorlar bilan.",
        "input_schema": {
            "type": "object",
            "properties": {
                "file_path": {"type": "string", "description": "Yaratiladigan .xlsx fayl yo'li"},
                "sheet_name": {"type": "string", "description": "Varaq nomi (default: Sheet1)"},
                "headers": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Ustun sarlavhalari (ixtiyoriy)",
                },
                "rows": {
                    "type": "array",
                    "items": {"type": "array"},
                    "description": "Qatorlar ro'yxati, har biri bitta qatorni ifodalaydi (ixtiyoriy)",
                },
                "overwrite": {"type": "boolean", "description": "Fayl mavjud bo'lsa, ustiga yozish (default: false)"},
            },
            "required": ["file_path"],
        },
    },
    {
        "name": "add_xlsx_sheet",
        "description": "Mavjud Excel (.xlsx) fayliga yangi varaq (sheet) qo'shadi.",
        "input_schema": {
            "type": "object",
            "properties": {
                "file_path": {"type": "string", "description": ".xlsx fayl yo'li"},
                "sheet_name": {"type": "string", "description": "Yangi varaq nomi"},
                "headers": {"type": "array", "items": {"type": "string"}, "description": "Ustun sarlavhalari (ixtiyoriy)"},
                "rows": {"type": "array", "items": {"type": "array"}, "description": "Qatorlar (ixtiyoriy)"},
            },
            "required": ["file_path", "sheet_name"],
        },
    },
    {
        "name": "append_xlsx_rows",
        "description": "Mavjud Excel (.xlsx) faylning bir varag'iga oxiriga yangi qatorlar qo'shadi.",
        "input_schema": {
            "type": "object",
            "properties": {
                "file_path": {"type": "string", "description": ".xlsx fayl yo'li"},
                "rows": {"type": "array", "items": {"type": "array"}, "description": "Qo'shiladigan qatorlar"},
                "sheet_name": {"type": "string", "description": "Varaq nomi (ixtiyoriy, bo'lmasa faol varaq)"},
            },
            "required": ["file_path", "rows"],
        },
    },
    {
        "name": "set_xlsx_formula",
        "description": "Excel (.xlsx) faylida belgilangan katakka formula yozadi (masalan '=SUM(A1:A10)').",
        "input_schema": {
            "type": "object",
            "properties": {
                "file_path": {"type": "string", "description": ".xlsx fayl yo'li"},
                "cell": {"type": "string", "description": "Katak manzili, masalan 'B5'"},
                "formula": {"type": "string", "description": "Excel formulasi, masalan '=SUM(A1:A10)'"},
                "sheet_name": {"type": "string", "description": "Varaq nomi (ixtiyoriy, bo'lmasa faol varaq)"},
            },
            "required": ["file_path", "cell", "formula"],
        },
    },
    {
        "name": "format_xlsx_cells",
        "description": "Excel (.xlsx) faylida katak diapazoniga formatlash qo'llaydi (qalin matn va/yoki fon rangi).",
        "input_schema": {
            "type": "object",
            "properties": {
                "file_path": {"type": "string", "description": ".xlsx fayl yo'li"},
                "cell_range": {"type": "string", "description": "Katak diapazoni, masalan 'A1:C1'"},
                "bold": {"type": "boolean", "description": "Matnni qalin qilish (ixtiyoriy)"},
                "bg_color": {"type": "string", "description": "6 xonali hex fon rangi, masalan 'FFFF00' (ixtiyoriy)"},
                "sheet_name": {"type": "string", "description": "Varaq nomi (ixtiyoriy)"},
            },
            "required": ["file_path", "cell_range"],
        },
    },
    {
        "name": "freeze_xlsx_panes",
        "description": "Excel (.xlsx) varag'ida sarlavha qator/ustunlarini muzlatadi (scroll qilganda ko'rinib turadi).",
        "input_schema": {
            "type": "object",
            "properties": {
                "file_path": {"type": "string", "description": ".xlsx fayl yo'li"},
                "cell": {"type": "string", "description": "Muzlatish chegarasi, masalan 'A2' (default: 'A2')"},
                "sheet_name": {"type": "string", "description": "Varaq nomi (ixtiyoriy)"},
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
    {
        "name": "create_pptx",
        "description": "Yangi PowerPoint (.pptx) taqdimot yaratadi, sarlavha slaydi bilan boshlanadi.",
        "input_schema": {
            "type": "object",
            "properties": {
                "file_path": {"type": "string", "description": "Yaratiladigan .pptx fayl yo'li"},
                "title": {"type": "string", "description": "Sarlavha slaydi matni (ixtiyoriy)"},
                "subtitle": {"type": "string", "description": "Kichik sarlavha matni (ixtiyoriy)"},
                "overwrite": {"type": "boolean", "description": "Fayl mavjud bo'lsa, ustiga yozish (default: false)"},
            },
            "required": ["file_path"],
        },
    },
    {
        "name": "add_pptx_slide",
        "description": "Mavjud PowerPoint (.pptx) taqdimotiga sarlavha va bullet-point matnli yangi slayd qo'shadi.",
        "input_schema": {
            "type": "object",
            "properties": {
                "file_path": {"type": "string", "description": ".pptx fayl yo'li"},
                "title": {"type": "string", "description": "Slayd sarlavhasi (ixtiyoriy)"},
                "bullet_points": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Slayd matni uchun bullet-point qatorlari (ixtiyoriy)",
                },
                "notes": {"type": "string", "description": "Speaker notes matni (ixtiyoriy)"},
            },
            "required": ["file_path"],
        },
    },
    {
        "name": "add_pptx_image",
        "description": "PowerPoint (.pptx) taqdimotiga rasm qo'shadi (belgilangan slaydga yoki oxirgisiga).",
        "input_schema": {
            "type": "object",
            "properties": {
                "file_path": {"type": "string", "description": ".pptx fayl yo'li"},
                "image_path": {"type": "string", "description": "Qo'shiladigan rasm fayli yo'li"},
                "slide_index": {"type": "integer", "description": "Slayd indeksi (0 dan boshlanadi; bo'lmasa oxirgi slayd)"},
                "left_inches": {"type": "number", "description": "Chapdan masofa dyuymda (default: 1.0)"},
                "top_inches": {"type": "number", "description": "Yuqoridan masofa dyuymda (default: 1.5)"},
                "width_inches": {"type": "number", "description": "Rasm kengligi dyuymda (ixtiyoriy, bo'lmasa asl o'lcham)"},
            },
            "required": ["file_path", "image_path"],
        },
    },
    {
        "name": "set_pptx_background_color",
        "description": "PowerPoint (.pptx) taqdimotida belgilangan slaydning fon rangini o'rnatadi.",
        "input_schema": {
            "type": "object",
            "properties": {
                "file_path": {"type": "string", "description": ".pptx fayl yo'li"},
                "slide_index": {"type": "integer", "description": "Slayd indeksi (0 dan boshlanadi)"},
                "hex_color": {"type": "string", "description": "6 xonali hex rang kodi, masalan 'FFFFFF'"},
            },
            "required": ["file_path", "slide_index", "hex_color"],
        },
    },
    # ---------- Avtomatik aniqlash ----------
    {
        "name": "read_any_file",
        "description": (
            "Fayl kengaytmasiga qarab (.docx/.xlsx/.pptx yoki eski .doc/.xls/.ppt) "
            "mos o'qish funksiyasini avtomatik tanlab ishlatadi. Fayl turi noaniq bo'lganda foydali."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "file_path": {"type": "string", "description": "Fayl yo'li (istalgan qo'llab-quvvatlanadigan format)"}
            },
            "required": ["file_path"],
        },
    },
    {
        "name": "get_file_info",
        "description": "Fayl haqida asosiy ma'lumot qaytaradi: mavjudmi, kengaytmasi, hajmi, aniqlangan turi.",
        "input_schema": {
            "type": "object",
            "properties": {
                "file_path": {"type": "string", "description": "Tekshiriladigan fayl yo'li"}
            },
            "required": ["file_path"],
        },
    },
    # ---------- Eski formatlar (.doc / .xls / .ppt) ----------
    {
        "name": "read_legacy_file",
        "description": (
            "Eski Microsoft formatidagi (.doc, .xls, .ppt) faylni avtomatik "
            "aniqlab, yangi formatga o'girib, matn/ma'lumotlarini o'qiydi."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": ".doc, .xls yoki .ppt fayl yo'li",
                }
            },
            "required": ["file_path"],
        },
    },
]
