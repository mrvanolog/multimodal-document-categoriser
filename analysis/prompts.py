from __future__ import annotations

from .types import Category


CLASSIFY_INSTRUCTION = (
    "You are a precise document classifier. "
    "Given an image or PDF, choose the single best category. "
    "Return ONLY valid JSON matching the provided schema."
)


def extraction_instruction(category: Category) -> str:
    base = (
        "You are an information extractor. "
        "Extract the requested fields for the "
        f"category '{category.value}'. "
        "Return ONLY valid JSON matching the schema."
    )
    return base
