from __future__ import annotations

from typing import Dict

from .types import Category

FIELDS = {
    Category.INVOICE: {
        "invoice_number": {"type": ["string", "null"]},
        "total": {"type": ["string", "null"]},
        "date": {"type": ["string", "null"]},
        "vendor": {"type": ["string", "null"]},
    },
    Category.MARKETPLACE_LISTING_SCREENSHOT: {
        "title": {"type": ["string", "null"]},
        "price": {"type": ["string", "null"]},
        "location": {"type": ["string", "null"]},
    },
    Category.CHAT_SCREENSHOT: {
        "participants": {
            "type": ["array", "null"],
            "items": {"type": "string"},
        },
        "timestamp": {"type": ["string", "null"]},
    },
    Category.WEBSITE_SCREENSHOT: {
        "url": {"type": ["string", "null"]},
        "title": {"type": ["string", "null"]},
    },
}


def classification_schema() -> Dict:
    return {
        "type": "object",
        "properties": {
            "category": {
                "type": "string",
                "enum": [c.value for c in Category],
            },
            "confidence": {"type": "number", "minimum": 0, "maximum": 1},
        },
        "required": ["category", "confidence"],
        "additionalProperties": False,
    }


def extraction_schema_for(category: Category) -> Dict:
    fields = FIELDS.get(category, {"text": {"type": "string"}})

    return {
        "type": "object",
        "properties": {
            "fields": {
                "type": "object",
                "properties": fields,
                "required": list(fields.keys()),
                "additionalProperties": True,
            },
            "raw_text": {
                "type": "string",
                "description": "Full extracted text (OCR) from the file/image"
            },
        },
        "required": ["fields", "raw_text"],
        "additionalProperties": False,
    }
