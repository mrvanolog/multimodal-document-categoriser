from __future__ import annotations

from typing import Dict

from .types import DocCategory

# TODO: expand fields based on real-world data
FIELDS = {
    DocCategory.INVOICE: {
        "invoice_number": {"type": ["string", "null"]},
        "invoice_date": {"type": ["string", "null"]},
        "total": {"type": ["number", "null"]},
        "items": {
            "type": ["array", "null"],
            "items": {
                "type": "object",
                "properties": {
                    "description": {"type": "string"},
                    "quantity": {"type": "number"},
                    "unit_price": {"type": "number"},
                    "total_price": {"type": "number"},
                },
                "required": ["description", "quantity", "unit_price", "total_price"],
                "additionalProperties": False,
            },
        },
        "vendor": {"type": ["string", "null"]},
        "address": {"type": ["string", "null"]},
    },
    DocCategory.MARKETPLACE_LISTING_SCREENSHOT: {
        "title": {"type": ["string", "null"]},
        "price": {"type": ["string", "null"]},
        "location": {"type": ["string", "null"]},
        "item_characteristics": {
            "type": ["array", "null"],
            "items": {"type": "string"},
        },
        "item_description": {"type": ["string", "null"]},
        "seller_name": {"type": ["string", "null"]},
    },
    DocCategory.CHAT_SCREENSHOT: {
        "participants": {
            "type": ["array", "null"],
            "items": {"type": "string"},
        },
        "timestamp": {"type": ["string", "null"]},
        "messages": {
            "type": ["array", "null"],
            "items": {
                "type": "object",
                "properties": {
                    "sender": {"type": "string"},
                    "text": {"type": "string"},
                    "time": {"type": "string"},
                },
                "required": ["sender", "text", "time"],
                "additionalProperties": False,
            },
        },
    },
    DocCategory.WEBSITE_SCREENSHOT: {
        "url": {"type": ["string", "null"]},
        "title": {"type": ["string", "null"]},
        "website_type": {"type": ["string", "null"]},
    },
}


def classification_schema() -> Dict:
    return {
        "type": "object",
        "properties": {
            "category": {
                "type": "string",
                "enum": [c.value for c in DocCategory],
            },
            "confidence": {"type": "number", "minimum": 0, "maximum": 1},
        },
        "required": ["category", "confidence"],
        "additionalProperties": False,
    }


def extraction_schema_for(category: DocCategory) -> Dict:
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
