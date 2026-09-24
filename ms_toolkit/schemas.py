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
    {
        "name": "add_xlsx_chart",
        "description": "Excel (.xlsx) varag'iga diagramma (bar/line/pie) qo'shadi, mavjud ma'lumotlar asosida.",
        "input_schema": {
            "type": "object",
            "properties": {
                "file_path": {"type": "string", "description": ".xlsx fayl yo'li"},
                "chart_type": {"type": "string", "enum": ["bar", "line", "pie"], "description": "Diagramma turi"},
                "data_range": {"type": "string", "description": "Qiymatlar diapazoni, masalan 'B1:B5'"},
                "categories_range": {"type": "string", "description": "X o'qi/label'lar diapazoni, masalan 'A2:A5' (ixtiyoriy)"},
                "title": {"type": "string", "description": "Diagramma sarlavhasi (ixtiyoriy)"},
                "anchor_cell": {"type": "string", "description": "Diagramma joylashadigan katak (default: 'E2')"},
                "sheet_name": {"type": "string", "description": "Varaq nomi (ixtiyoriy)"},
            },
            "required": ["file_path", "chart_type", "data_range"],
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
    {
        "name": "add_pptx_chart",
        "description": "PowerPoint (.pptx) taqdimotiga diagramma (bar/line/pie) qo'shadi, berilgan kategoriyalar va seriyalar asosida.",
        "input_schema": {
            "type": "object",
            "properties": {
                "file_path": {"type": "string", "description": ".pptx fayl yo'li"},
                "chart_type": {"type": "string", "enum": ["bar", "line", "pie"], "description": "Diagramma turi"},
                "categories": {"type": "array", "items": {"type": "string"}, "description": "X o'qi label'lari"},
                "series": {
                    "type": "object",
                    "description": "Seriya nomi -> qiymatlar ro'yxati, masalan {\"Savdo\": [10, 20, 30]}",
                    "additionalProperties": {"type": "array", "items": {"type": "number"}},
                },
                "slide_index": {"type": "integer", "description": "Slayd indeksi (bo'lmasa oxirgi slayd)"},
                "title": {"type": "string", "description": "Diagramma sarlavhasi (ixtiyoriy)"},
            },
            "required": ["file_path", "chart_type", "categories", "series"],
        },
    },
    # ---------- PDF ----------
    {
        "name": "read_pdf_text",
        "description": "PDF fayldan matnni o'qib chiqaradi (barcha yoki birinchi bir necha sahifa).",
        "input_schema": {
            "type": "object",
            "properties": {
                "file_path": {"type": "string", "description": ".pdf fayl yo'li"},
                "max_pages": {"type": "integer", "description": "O'qiladigan maksimal sahifalar soni (ixtiyoriy, bo'lmasa barchasi)"},
            },
            "required": ["file_path"],
        },
    },
    {
        "name": "read_pdf_tables",
        "description": "PDF fayldagi har bir sahifadan jadvallarni ajratib oladi.",
        "input_schema": {
            "type": "object",
            "properties": {"file_path": {"type": "string", "description": ".pdf fayl yo'li"}},
            "required": ["file_path"],
        },
    },
    {
        "name": "get_pdf_metadata",
        "description": "PDF faylning metama'lumotini (sarlavha, muallif, sahifalar soni, shifrlanganmi) qaytaradi.",
        "input_schema": {
            "type": "object",
            "properties": {"file_path": {"type": "string", "description": ".pdf fayl yo'li"}},
            "required": ["file_path"],
        },
    },
    {
        "name": "create_pdf",
        "description": "Yangi PDF hujjat yaratadi — sarlavha va paragraflar bilan.",
        "input_schema": {
            "type": "object",
            "properties": {
                "file_path": {"type": "string", "description": "Yaratiladigan .pdf fayl yo'li"},
                "title": {"type": "string", "description": "Hujjat sarlavhasi (ixtiyoriy)"},
                "paragraphs": {"type": "array", "items": {"type": "string"}, "description": "Matn paragraflari (ixtiyoriy)"},
                "overwrite": {"type": "boolean", "description": "Fayl mavjud bo'lsa, ustiga yozish (default: false)"},
            },
            "required": ["file_path"],
        },
    },
    {
        "name": "merge_pdfs",
        "description": "Bir nechta PDF faylni ketma-ket bitta faylga birlashtiradi.",
        "input_schema": {
            "type": "object",
            "properties": {
                "file_paths": {"type": "array", "items": {"type": "string"}, "description": "Birlashtiriladigan PDF fayllar yo'li, tartib bo'yicha"},
                "output_path": {"type": "string", "description": "Natija saqlanadigan .pdf fayl yo'li"},
                "overwrite": {"type": "boolean", "description": "Fayl mavjud bo'lsa, ustiga yozish (default: false)"},
            },
            "required": ["file_paths", "output_path"],
        },
    },
    {
        "name": "split_pdf",
        "description": "PDF faylni har bir sahifa alohida faylga bo'ladi (page_1.pdf, page_2.pdf, ...).",
        "input_schema": {
            "type": "object",
            "properties": {
                "file_path": {"type": "string", "description": "Bo'linadigan .pdf fayl yo'li"},
                "output_dir": {"type": "string", "description": "Natija fayllar saqlanadigan papka"},
            },
            "required": ["file_path", "output_dir"],
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
    # ---------- CSV ----------
    {   'name': 'read_csv_data',
        'description': "CSV fayldan sarlavha va qatorlarni o'qiydi.",
        'input_schema': {   'type': 'object',
                            'properties': {   'file_path': {   'type': 'string',
                                                               'description': ".csv fayl yo'li"},
                                              'max_rows': {   'type': 'integer',
                                                              'description': "O'qiladigan maksimal "
                                                                             'qator soni (ixtiyoriy)'},
                                              'delimiter': {   'type': 'string',
                                                               'description': 'Ustun ajratkichi '
                                                                              "(default: ',')"}},
                            'required': ['file_path']}},
    {   'name': 'get_csv_summary',
        'description': 'CSV faylning umumiy tuzilishini (ustunlar, qatorlar soni, namuna) qaytaradi.',
        'input_schema': {   'type': 'object',
                            'properties': {   'file_path': {   'type': 'string',
                                                               'description': ".csv fayl yo'li"},
                                              'delimiter': {   'type': 'string',
                                                               'description': 'Ustun ajratkichi '
                                                                              "(default: ',')"}},
                            'required': ['file_path']}},
    {   'name': 'create_csv',
        'description': "Yangi CSV fayl yaratadi (ixtiyoriy sarlavha va boshlang'ich qatorlar bilan).",
        'input_schema': {   'type': 'object',
                            'properties': {   'file_path': {   'type': 'string',
                                                               'description': 'Yaratiladigan .csv fayl '
                                                                              "yo'li"},
                                              'headers': {   'type': 'array',
                                                             'items': {'type': 'string'},
                                                             'description': 'Ustun sarlavhalari '
                                                                            '(ixtiyoriy)'},
                                              'rows': {   'type': 'array',
                                                          'items': {   'type': 'array',
                                                                       'items': {'type': 'string'}},
                                                          'description': "Boshlang'ich qatorlar "
                                                                         '(ixtiyoriy)'},
                                              'delimiter': {   'type': 'string',
                                                               'description': 'Ustun ajratkichi '
                                                                              "(default: ',')"},
                                              'overwrite': {   'type': 'boolean',
                                                               'description': "Fayl mavjud bo'lsa, "
                                                                              'ustiga yozish (default: '
                                                                              'false)'}},
                            'required': ['file_path']}},
    {   'name': 'append_csv_rows',
        'description': "Mavjud CSV faylning oxiriga yangi qatorlar qo'shadi.",
        'input_schema': {   'type': 'object',
                            'properties': {   'file_path': {   'type': 'string',
                                                               'description': ".csv fayl yo'li"},
                                              'rows': {   'type': 'array',
                                                          'items': {   'type': 'array',
                                                                       'items': {'type': 'string'}},
                                                          'description': "Qo'shiladigan qatorlar"},
                                              'delimiter': {   'type': 'string',
                                                               'description': 'Ustun ajratkichi '
                                                                              "(default: ',')"}},
                            'required': ['file_path', 'rows']}},
    # ---------- OpenDocument (.odt/.ods/.odp) ----------
    {   'name': 'read_odt_text',
        'description': "OpenDocument Text (.odt) fayldan barcha matnni o'qiydi.",
        'input_schema': {   'type': 'object',
                            'properties': {   'file_path': {   'type': 'string',
                                                               'description': ".odt fayl yo'li"}},
                            'required': ['file_path']}},
    {   'name': 'get_ods_sheet_names',
        'description': 'OpenDocument Spreadsheet (.ods) fayldagi varaq nomlarini qaytaradi.',
        'input_schema': {   'type': 'object',
                            'properties': {   'file_path': {   'type': 'string',
                                                               'description': ".ods fayl yo'li"}},
                            'required': ['file_path']}},
    {   'name': 'read_ods_data',
        'description': "OpenDocument Spreadsheet (.ods) faylidan varaq ma'lumotlarini o'qiydi.",
        'input_schema': {   'type': 'object',
                            'properties': {   'file_path': {   'type': 'string',
                                                               'description': ".ods fayl yo'li"},
                                              'sheet_name': {   'type': 'string',
                                                                'description': "O'qiladigan varaq nomi "
                                                                               '(ixtiyoriy, default: '
                                                                               'birinchi varaq)'},
                                              'max_rows': {   'type': 'integer',
                                                              'description': "O'qiladigan maksimal "
                                                                             'qator soni (ixtiyoriy)'}},
                            'required': ['file_path']}},
    {   'name': 'read_odp_text',
        'description': "OpenDocument Presentation (.odp) fayldan har bir slayd matnini o'qiydi.",
        'input_schema': {   'type': 'object',
                            'properties': {   'file_path': {   'type': 'string',
                                                               'description': ".odp fayl yo'li"}},
                            'required': ['file_path']}},
    {   'name': 'get_odp_slide_count',
        'description': 'OpenDocument Presentation (.odp) fayldagi slaydlar sonini qaytaradi.',
        'input_schema': {   'type': 'object',
                            'properties': {   'file_path': {   'type': 'string',
                                                               'description': ".odp fayl yo'li"}},
                            'required': ['file_path']}},
    {   'name': 'create_odt',
        'description': 'Yangi OpenDocument Text (.odt) hujjat yaratadi (sarlavha + paragraflar bilan).',
        'input_schema': {   'type': 'object',
                            'properties': {   'file_path': {   'type': 'string',
                                                               'description': 'Yaratiladigan .odt fayl '
                                                                              "yo'li"},
                                              'title': {   'type': 'string',
                                                           'description': 'Hujjat sarlavhasi '
                                                                          '(ixtiyoriy)'},
                                              'paragraphs': {   'type': 'array',
                                                                'items': {'type': 'string'},
                                                                'description': 'Matn paragraflari '
                                                                               '(ixtiyoriy)'},
                                              'overwrite': {   'type': 'boolean',
                                                               'description': "Fayl mavjud bo'lsa, "
                                                                              'ustiga yozish (default: '
                                                                              'false)'}},
                            'required': ['file_path']}},
    {   'name': 'create_ods',
        'description': "Yangi OpenDocument Spreadsheet (.ods) fayl yaratadi (2-o'lchamli qatorlar "
                       "ro'yxatidan).",
        'input_schema': {   'type': 'object',
                            'properties': {   'file_path': {   'type': 'string',
                                                               'description': 'Yaratiladigan .ods fayl '
                                                                              "yo'li"},
                                              'rows': {   'type': 'array',
                                                          'items': {   'type': 'array',
                                                                       'items': {'type': 'string'}},
                                                          'description': 'Jadval qatorlari, birinchi '
                                                                         "qator sarlavha bo'lishi "
                                                                         'mumkin'},
                                              'sheet_name': {   'type': 'string',
                                                                'description': 'Varaq nomi (default: '
                                                                               "'Sheet1')"},
                                              'overwrite': {   'type': 'boolean',
                                                               'description': "Fayl mavjud bo'lsa, "
                                                                              'ustiga yozish (default: '
                                                                              'false)'}},
                            'required': ['file_path', 'rows']}},
    {   'name': 'create_odp',
        'description': 'Yangi OpenDocument Presentation (.odp) fayl yaratadi — har bir string bitta '
                       'slayd matni.',
        'input_schema': {   'type': 'object',
                            'properties': {   'file_path': {   'type': 'string',
                                                               'description': 'Yaratiladigan .odp fayl '
                                                                              "yo'li"},
                                              'slides': {   'type': 'array',
                                                            'items': {'type': 'string'},
                                                            'description': 'Har biri bitta slayd matni '
                                                                           "bo'lgan ro'yxat"},
                                              'overwrite': {   'type': 'boolean',
                                                               'description': "Fayl mavjud bo'lsa, "
                                                                              'ustiga yozish (default: '
                                                                              'false)'}},
                            'required': ['file_path', 'slides']}},
    # ---------- Rasm (Image) ----------
    {   'name': 'get_image_info',
        'description': "Rasm haqida asosiy ma'lumot: o'lcham, format, rang rejimi, hajmi.",
        'input_schema': {   'type': 'object',
                            'properties': {   'file_path': {   'type': 'string',
                                                               'description': "Rasm fayli yo'li"}},
                            'required': ['file_path']}},
    {   'name': 'read_image_text',
        'description': 'Rasmdagi matnni OCR (Tesseract) orqali ajratib oladi.',
        'input_schema': {   'type': 'object',
                            'properties': {   'file_path': {   'type': 'string',
                                                               'description': "Rasm fayli yo'li"},
                                              'lang': {   'type': 'string',
                                                          'description': 'Tesseract til kodi (default: '
                                                                         "'eng'; masalan 'eng+rus')"}},
                            'required': ['file_path']}},
    {   'name': 'convert_image',
        'description': "Rasmni boshqa formatga o'giradi va/yoki o'lchamini o'zgartiradi.",
        'input_schema': {   'type': 'object',
                            'properties': {   'file_path': {   'type': 'string',
                                                               'description': "Manba rasm fayli yo'li"},
                                              'output_path': {   'type': 'string',
                                                                 'description': 'Natija rasm fayli '
                                                                                "yo'li"},
                                              'target_format': {   'type': 'string',
                                                                   'description': 'Maqsad format '
                                                                                  "(masalan 'PNG', "
                                                                                  "'JPEG', 'WEBP'); "
                                                                                  'berilmasa '
                                                                                  'output_path '
                                                                                  'kengaytmasidan '
                                                                                  'aniqlanadi'},
                                              'width': {   'type': 'integer',
                                                           'description': 'Yangi kenglik (ixtiyoriy, '
                                                                          "proporsional o'zgaradi)"},
                                              'height': {   'type': 'integer',
                                                            'description': 'Yangi balandlik '
                                                                           '(ixtiyoriy, proporsional '
                                                                           "o'zgaradi)"},
                                              'overwrite': {   'type': 'boolean',
                                                               'description': "Fayl mavjud bo'lsa, "
                                                                              'ustiga yozish (default: '
                                                                              'false)'}},
                            'required': ['file_path', 'output_path']}},
    {   'name': 'create_thumbnail',
        'description': 'Rasmdan (proporsiyani saqlab) thumbnail (kichik nusxa) yaratadi.',
        'input_schema': {   'type': 'object',
                            'properties': {   'file_path': {   'type': 'string',
                                                               'description': "Manba rasm fayli yo'li"},
                                              'output_path': {   'type': 'string',
                                                                 'description': 'Natija thumbnail '
                                                                                "fayli yo'li"},
                                              'size': {   'type': 'integer',
                                                          'description': "Maksimal tomon o'lchami "
                                                                         'piksellarda (default: 128)'},
                                              'overwrite': {   'type': 'boolean',
                                                               'description': "Fayl mavjud bo'lsa, "
                                                                              'ustiga yozish (default: '
                                                                              'false)'}},
                            'required': ['file_path', 'output_path']}},
    # ---------- Arxiv (ZIP) ----------
    {   'name': 'list_archive_contents',
        'description': "ZIP arxiv ichidagi barcha fayllar ro'yxatini (nom, hajm) qaytaradi.",
        'input_schema': {   'type': 'object',
                            'properties': {   'file_path': {   'type': 'string',
                                                               'description': ".zip fayl yo'li"}},
                            'required': ['file_path']}},
    {   'name': 'read_archive_file',
        'description': "ZIP arxiv ichidagi bitta matnli faylni o'qib, matnini qaytaradi.",
        'input_schema': {   'type': 'object',
                            'properties': {   'file_path': {   'type': 'string',
                                                               'description': ".zip fayl yo'li"},
                                              'entry_name': {   'type': 'string',
                                                                'description': 'Arxiv ichidagi fayl '
                                                                               'nomi'},
                                              'encoding': {   'type': 'string',
                                                              'description': 'Matn kodlash formati '
                                                                             "(default: 'utf-8')"}},
                            'required': ['file_path', 'entry_name']}},
    {   'name': 'create_archive',
        'description': 'Berilgan fayllardan yangi ZIP arxiv yaratadi.',
        'input_schema': {   'type': 'object',
                            'properties': {   'output_path': {   'type': 'string',
                                                                 'description': 'Yaratiladigan .zip '
                                                                                "fayl yo'li"},
                                              'file_paths': {   'type': 'array',
                                                                'items': {'type': 'string'},
                                                                'description': "Arxivga qo'shiladigan "
                                                                               "fayllar ro'yxati"},
                                              'overwrite': {   'type': 'boolean',
                                                               'description': "Fayl mavjud bo'lsa, "
                                                                              'ustiga yozish (default: '
                                                                              'false)'}},
                            'required': ['output_path', 'file_paths']}},
    {   'name': 'extract_archive',
        'description': 'ZIP arxivni papkaga chiqaradi (zip-slip himoyasi bilan).',
        'input_schema': {   'type': 'object',
                            'properties': {   'file_path': {   'type': 'string',
                                                               'description': ".zip fayl yo'li"},
                                              'output_dir': {   'type': 'string',
                                                                'description': 'Fayllar chiqariladigan '
                                                                               'papka'}},
                            'required': ['file_path', 'output_dir']}},
    # ---------- Konvertatsiya ----------
    {   'name': 'convert_docx_to_pdf',
        'description': "Word (.docx) hujjatini PDF'ga o'giradi (LibreOffice orqali).",
        'input_schema': {   'type': 'object',
                            'properties': {   'file_path': {   'type': 'string',
                                                               'description': ".docx fayl yo'li"},
                                              'output_path': {   'type': 'string',
                                                                 'description': 'Natija .pdf fayl '
                                                                                "yo'li"},
                                              'overwrite': {   'type': 'boolean',
                                                               'description': "Fayl mavjud bo'lsa, "
                                                                              'ustiga yozish (default: '
                                                                              'false)'}},
                            'required': ['file_path', 'output_path']}},
    {   'name': 'convert_pptx_to_pdf',
        'description': "PowerPoint (.pptx) taqdimotini PDF'ga o'giradi (LibreOffice orqali).",
        'input_schema': {   'type': 'object',
                            'properties': {   'file_path': {   'type': 'string',
                                                               'description': ".pptx fayl yo'li"},
                                              'output_path': {   'type': 'string',
                                                                 'description': 'Natija .pdf fayl '
                                                                                "yo'li"},
                                              'overwrite': {   'type': 'boolean',
                                                               'description': "Fayl mavjud bo'lsa, "
                                                                              'ustiga yozish (default: '
                                                                              'false)'}},
                            'required': ['file_path', 'output_path']}},
    {   'name': 'convert_xlsx_to_pdf',
        'description': "Excel (.xlsx) faylini PDF'ga o'giradi (LibreOffice orqali).",
        'input_schema': {   'type': 'object',
                            'properties': {   'file_path': {   'type': 'string',
                                                               'description': ".xlsx fayl yo'li"},
                                              'output_path': {   'type': 'string',
                                                                 'description': 'Natija .pdf fayl '
                                                                                "yo'li"},
                                              'overwrite': {   'type': 'boolean',
                                                               'description': "Fayl mavjud bo'lsa, "
                                                                              'ustiga yozish (default: '
                                                                              'false)'}},
                            'required': ['file_path', 'output_path']}},
    {   'name': 'convert_pdf_to_images',
        'description': 'PDF faylning har bir sahifasini alohida rasm faylga aylantiradi.',
        'input_schema': {   'type': 'object',
                            'properties': {   'file_path': {   'type': 'string',
                                                               'description': ".pdf fayl yo'li"},
                                              'output_dir': {   'type': 'string',
                                                                'description': 'Rasmlar saqlanadigan '
                                                                               'papka'},
                                              'image_format': {   'type': 'string',
                                                                  'description': 'Rasm formati '
                                                                                 "(default: 'png')"},
                                              'dpi': {   'type': 'integer',
                                                         'description': 'Rasm sifati (default: 150)'}},
                            'required': ['file_path', 'output_dir']}},
    {   'name': 'convert_pptx_to_images',
        'description': 'PowerPoint taqdimotining har bir slaydini rasmga aylantiradi.',
        'input_schema': {   'type': 'object',
                            'properties': {   'file_path': {   'type': 'string',
                                                               'description': ".pptx fayl yo'li"},
                                              'output_dir': {   'type': 'string',
                                                                'description': 'Rasmlar saqlanadigan '
                                                                               'papka'},
                                              'image_format': {   'type': 'string',
                                                                  'description': 'Rasm formati '
                                                                                 "(default: 'png')"},
                                              'dpi': {   'type': 'integer',
                                                         'description': 'Rasm sifati (default: 150)'}},
                            'required': ['file_path', 'output_dir']}},
    {   'name': 'convert_xlsx_to_csv',
        'description': "Excel (.xlsx) faylning har bir varag'ini alohida CSV faylga eksport qiladi.",
        'input_schema': {   'type': 'object',
                            'properties': {   'file_path': {   'type': 'string',
                                                               'description': ".xlsx fayl yo'li"},
                                              'output_dir': {   'type': 'string',
                                                                'description': 'CSV fayllar '
                                                                               'saqlanadigan papka'},
                                              'delimiter': {   'type': 'string',
                                                               'description': 'Ustun ajratkichi '
                                                                              "(default: ',')"}},
                            'required': ['file_path', 'output_dir']}},
    # ---------- Kod / matn fayllari (.py, .js, .html, .css, .json, .csv, .txt va h.k.) ----------
    {
        "name": "read_code_file",
        "description": "Kod yoki matn faylini (.py, .js, .html, .css, .json, .csv, .txt va h.k.) to'liq o'qiydi.",
        "input_schema": {
            "type": "object",
            "properties": {
                "file_path": {"type": "string", "description": "O'qiladigan fayl yo'li"},
                "max_chars": {
                    "type": "integer",
                    "description": "Maksimal belgi soni (default: 200000), undan katta bo'lsa kesib qo'yiladi",
                },
            },
            "required": ["file_path"],
        },
    },
    {
        "name": "read_code_lines",
        "description": "Kod/matn faylining faqat berilgan qator oralig'ini o'qiydi (masalan, xatolik yuz bergan joy atrofini ko'rish uchun).",
        "input_schema": {
            "type": "object",
            "properties": {
                "file_path": {"type": "string", "description": "Fayl yo'li"},
                "start_line": {"type": "integer", "description": "Boshlanish qatori (1-based, default: 1)"},
                "end_line": {"type": "integer", "description": "Tugash qatori (inklyuziv, berilmasa faylning oxirigacha)"},
            },
            "required": ["file_path"],
        },
    },
    {
        "name": "create_code_file",
        "description": "Yangi kod/matn faylini yaratadi, kerak bo'lsa oraliq papkalarni ham avtomatik yaratadi.",
        "input_schema": {
            "type": "object",
            "properties": {
                "file_path": {"type": "string", "description": "Yaratiladigan fayl yo'li"},
                "content": {"type": "string", "description": "Fayl mazmuni (ixtiyoriy, default: bo'sh)"},
                "overwrite": {"type": "boolean", "description": "Fayl mavjud bo'lsa, ustiga yozish (default: false)"},
            },
            "required": ["file_path"],
        },
    },
    {
        "name": "append_code_text",
        "description": "Mavjud kod/matn faylining oxiriga matn qo'shadi. Fayl mavjud bo'lmasa, yangisini yaratadi.",
        "input_schema": {
            "type": "object",
            "properties": {
                "file_path": {"type": "string", "description": "Fayl yo'li"},
                "text": {"type": "string", "description": "Qo'shiladigan matn"},
                "newline_before": {"type": "boolean", "description": "Qo'shishdan oldin yangi qator qo'yish (default: true)"},
            },
            "required": ["file_path", "text"],
        },
    },
    {
        "name": "replace_code_text",
        "description": "Fayldagi 'find' matnini 'replace' bilan almashtiradi (oddiy string qidiruv, regex emas).",
        "input_schema": {
            "type": "object",
            "properties": {
                "file_path": {"type": "string", "description": "Fayl yo'li"},
                "find": {"type": "string", "description": "Qidiriladigan matn"},
                "replace": {"type": "string", "description": "Almashtiriladigan matn"},
                "save_as": {"type": "string", "description": "Boshqa faylga saqlash (ixtiyoriy, berilmasa ustiga yoziladi)"},
                "count": {"type": "integer", "description": "Nechta marta almashtirish (default: -1, hammasi)"},
            },
            "required": ["file_path", "find", "replace"],
        },
    },
    {
        "name": "insert_code_lines",
        "description": "Berilgan qator raqami oldiga yangi matn qatorini qo'shadi (1-based).",
        "input_schema": {
            "type": "object",
            "properties": {
                "file_path": {"type": "string", "description": "Fayl yo'li"},
                "line_number": {"type": "integer", "description": "Matn shu qator OLDIGA qo'yiladi (1-based)"},
                "text": {"type": "string", "description": "Qo'shiladigan matn (bir yoki bir nechta qator)"},
            },
            "required": ["file_path", "line_number", "text"],
        },
    },
    {
        "name": "delete_code_lines",
        "description": "Fayldan berilgan qator oralig'ini o'chiradi (1-based, end_line inklyuziv).",
        "input_schema": {
            "type": "object",
            "properties": {
                "file_path": {"type": "string", "description": "Fayl yo'li"},
                "start_line": {"type": "integer", "description": "O'chirish boshlanadigan qator"},
                "end_line": {"type": "integer", "description": "O'chirish tugaydigan qator (berilmasa faqat start_line o'chadi)"},
            },
            "required": ["file_path", "start_line"],
        },
    },
    {
        "name": "list_directory_files",
        "description": "Papka ichidagi kod/matn fayllarini (yo'li, hajmi, kengaytmasi bilan) ro'yxatlaydi.",
        "input_schema": {
            "type": "object",
            "properties": {
                "dir_path": {"type": "string", "description": "Ko'riladigan papka yo'li"},
                "extensions": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Faqat shu kengaytmalar (masalan ['.py', '.js']), berilmasa hammasi",
                },
                "recursive": {"type": "boolean", "description": "Ichki papkalarni ham qidirish (default: true)"},
            },
            "required": ["dir_path"],
        },
    },
    {
        "name": "search_in_files",
        "description": "Papka ichidagi kod/matn fayllarida berilgan matnni qidiradi (grep uslubida), fayl va qator raqami bilan qaytaradi.",
        "input_schema": {
            "type": "object",
            "properties": {
                "dir_path": {"type": "string", "description": "Qidiriladigan papka yo'li"},
                "query": {"type": "string", "description": "Qidiriladigan matn"},
                "extensions": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Faqat shu kengaytmalar ichida qidirish (ixtiyoriy)",
                },
                "case_sensitive": {"type": "boolean", "description": "Katta-kichik harfga sezgir qidiruv (default: false)"},
            },
            "required": ["dir_path", "query"],
        },
    },
    # ---------- Rasmlar (crop, resize, rotate, blank canvas) ----------
    {
        "name": "crop_image",
        "description": "Rasmni berilgan to'rtburchak chegaralari bo'yicha kesadi (piksellarda, yuqori chap burchak 0,0).",
        "input_schema": {
            "type": "object",
            "properties": {
                "file_path": {"type": "string", "description": "Rasm fayli yo'li"},
                "left": {"type": "integer", "description": "Chap chegara (piksel)"},
                "top": {"type": "integer", "description": "Yuqori chegara (piksel)"},
                "right": {"type": "integer", "description": "O'ng chegara (piksel)"},
                "bottom": {"type": "integer", "description": "Pastki chegara (piksel)"},
                "save_as": {"type": "string", "description": "Boshqa faylga saqlash (ixtiyoriy, berilmasa ustiga yoziladi)"},
            },
            "required": ["file_path", "left", "top", "right", "bottom"],
        },
    },
    {
        "name": "resize_image",
        "description": "Rasm o'lchamini o'zgartiradi (formatni o'zgartirmasdan). width/height dan bittasi berilsa, nisbat saqlanib ikkinchisi hisoblanadi.",
        "input_schema": {
            "type": "object",
            "properties": {
                "file_path": {"type": "string", "description": "Rasm fayli yo'li"},
                "width": {"type": "integer", "description": "Yangi kenglik (piksel, ixtiyoriy)"},
                "height": {"type": "integer", "description": "Yangi balandlik (piksel, ixtiyoriy)"},
                "save_as": {"type": "string", "description": "Boshqa faylga saqlash (ixtiyoriy, berilmasa ustiga yoziladi)"},
                "keep_aspect_ratio": {"type": "boolean", "description": "Asl nisbatni saqlash (default: true)"},
            },
            "required": ["file_path"],
        },
    },
    {
        "name": "rotate_image",
        "description": "Rasmni berilgan gradusga (soat yo'nalishiga qarshi) aylantiradi.",
        "input_schema": {
            "type": "object",
            "properties": {
                "file_path": {"type": "string", "description": "Rasm fayli yo'li"},
                "degrees": {"type": "number", "description": "Aylantirish burchagi (gradus)"},
                "save_as": {"type": "string", "description": "Boshqa faylga saqlash (ixtiyoriy, berilmasa ustiga yoziladi)"},
                "expand": {"type": "boolean", "description": "Aylantirilganda rasm o'lchamini kengaytirish (default: true)"},
            },
            "required": ["file_path", "degrees"],
        },
    },
    {
        "name": "create_image",
        "description": "Bo'sh (bir rangli) yangi rasm yaratadi — fon yoki placeholder sifatida.",
        "input_schema": {
            "type": "object",
            "properties": {
                "width": {"type": "integer", "description": "Rasm kengligi (piksel)"},
                "height": {"type": "integer", "description": "Rasm balandligi (piksel)"},
                "output_path": {"type": "string", "description": "Saqlanadigan fayl yo'li"},
                "color": {"type": "string", "description": "Rang, hex (#RRGGBB) yoki nom (masalan 'red') (default: '#FFFFFF')"},
            },
            "required": ["width", "height", "output_path"],
        },
    },
    # ---------- Internetdan ma'lumot olish (fayl yuklash, web scraping, qidiruv) ----------
    {
        "name": "download_file",
        "description": "Berilgan URL'dan faylni yuklab, diskka saqlaydi (rasm, PDF, arxiv va h.k. bo'lishi mumkin).",
        "input_schema": {
            "type": "object",
            "properties": {
                "url": {"type": "string", "description": "Yuklanadigan fayl manzili (http:// yoki https://)"},
                "output_path": {"type": "string", "description": "Fayl saqlanadigan yo'l"},
                "max_bytes": {"type": "integer", "description": "Maksimal ruxsat etilgan fayl hajmi baytda (default: 50MB)"},
                "timeout": {"type": "integer", "description": "So'rov timeout soniyada (default: 15)"},
            },
            "required": ["url", "output_path"],
        },
    },
    {
        "name": "fetch_url_text",
        "description": "URL'dan sahifaning xom (raw) matn/HTML mazmunini oladi, tozalanmagan holda.",
        "input_schema": {
            "type": "object",
            "properties": {
                "url": {"type": "string", "description": "So'rov yuboriladigan manzil (http:// yoki https://)"},
                "timeout": {"type": "integer", "description": "So'rov timeout soniyada (default: 15)"},
                "max_chars": {"type": "integer", "description": "Maksimal belgi soni (default: 200000)"},
            },
            "required": ["url"],
        },
    },
    {
        "name": "scrape_page_text",
        "description": "Web-sahifadan o'qiladigan matnni ajratib oladi (HTML teglar, skript va stillar olib tashlanadi). Sahifa sarlavhasini ham qaytaradi.",
        "input_schema": {
            "type": "object",
            "properties": {
                "url": {"type": "string", "description": "Sahifa manzili (http:// yoki https://)"},
                "timeout": {"type": "integer", "description": "So'rov timeout soniyada (default: 15)"},
                "max_chars": {"type": "integer", "description": "Maksimal belgi soni (default: 100000)"},
            },
            "required": ["url"],
        },
    },
    {
        "name": "extract_page_links",
        "description": "Web-sahifadagi barcha havolalarni (matni bilan birga, to'liq URL holida) ajratib oladi.",
        "input_schema": {
            "type": "object",
            "properties": {
                "url": {"type": "string", "description": "Sahifa manzili (http:// yoki https://)"},
                "timeout": {"type": "integer", "description": "So'rov timeout soniyada (default: 15)"},
                "same_domain_only": {"type": "boolean", "description": "Faqat bir xil domendagi havolalarni qaytarish (default: false)"},
            },
            "required": ["url"],
        },
    },
    {
        "name": "extract_page_images",
        "description": "Web-sahifadagi barcha rasm (<img>) manzillarini to'liq URL holida ajratib oladi.",
        "input_schema": {
            "type": "object",
            "properties": {
                "url": {"type": "string", "description": "Sahifa manzili (http:// yoki https://)"},
                "timeout": {"type": "integer", "description": "So'rov timeout soniyada (default: 15)"},
            },
            "required": ["url"],
        },
    },
    {
        "name": "search_web",
        "description": (
            "Internetda matn qidiruvi (kalit talab qilmaydi). Savolga to'g'ridan-to'g'ri javob "
            "bermaydi — natijada topilgan sahifalar (sarlavha, manzil, qisqa tavsif) qaytadi. "
            "So'ngra kerakli manzilni scrape_page_text yoki fetch_url_text bilan o'qing."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "Qidiriladigan so'rov matni"},
                "max_results": {"type": "integer", "description": "Maksimal natijalar soni (default: 8)"},
                "timeout": {"type": "integer", "description": "So'rov timeout soniyada (default: 15)"},
            },
            "required": ["query"],
        },
    },
    {
        "name": "get_known_changelog_url",
        "description": (
            "Ma'lum bir servis (masalan 'Telegram Bot API', 'Discord API', 'OpenAI API') uchun "
            "oldindan tayyorlangan rasmiy changelog/hujjat manzilini qaytaradi. Bu search_web'dan "
            "tezroq va ishonchliroq, chunki bevosita rasmiy manbaga ishora qiladi. Ro'yxatda yo'q "
            "servis uchun search_web ishlatishni tavsiya qiladi."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "service_name": {"type": "string", "description": "Servis nomi (masalan 'telegram bot api', 'discord api')"}
            },
            "required": ["service_name"],
        },
    },
]
