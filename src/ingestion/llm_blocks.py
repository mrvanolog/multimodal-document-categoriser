from __future__ import annotations

import base64
from pathlib import Path
from typing import List

from .preprocess import normalize_image_to_jpeg_bytes
from .types import LLMFileBlock, LLMImageBlock, LLMTextBlock


def to_text_block(text: str) -> LLMTextBlock:
    return {"type": "text", "text": text}


def _to_data_uri(mime: str, data: bytes) -> str:
    b64 = base64.b64encode(data).decode("utf-8")
    return f"data:{mime};base64,{b64}"


def image_path_to_block(path: Path, max_side: int = 1600) -> LLMImageBlock:
    jpeg_bytes = normalize_image_to_jpeg_bytes(path, max_side=max_side)
    data_uri = _to_data_uri("image/jpeg", jpeg_bytes)
    return {"type": "image_url", "image_url": {"url": data_uri}}


def pdf_path_to_block(path: Path) -> LLMFileBlock:
    data = path.read_bytes()
    data_uri = _to_data_uri("application/pdf", data)
    return {
        "type": "file",
        "file": {"filename": path.name, "file_data": data_uri},
    }


def file_to_blocks(path: Path, mime: str) -> List[dict]:
    if mime.startswith("image/"):
        return [image_path_to_block(path)]
    if mime == "application/pdf":
        return [pdf_path_to_block(path)]
    raise ValueError(f"Unsupported mime type: {mime} for {path}")
