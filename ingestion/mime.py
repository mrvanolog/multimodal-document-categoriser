from __future__ import annotations

import mimetypes
from pathlib import Path
from typing import Set


IMAGE_EXTS: Set[str] = {
    ".png",
    ".jpg",
    ".jpeg",
    ".webp",
    ".bmp",
    ".tif",
    ".tiff",
}
PDF_EXTS: Set[str] = {".pdf"}


def guess_mime(path: Path) -> str:
    # Prefer extension-based guess (cross-platform)
    mime, _ = mimetypes.guess_type(str(path))
    if mime:
        return mime
    # Fallback simple heuristics
    ext = path.suffix.lower()
    if ext in IMAGE_EXTS:
        return f"image/{ext.lstrip('.')}" if ext != ".jpg" else "image/jpeg"
    if ext in PDF_EXTS:
        return "application/pdf"
    return "application/octet-stream"


def is_supported(path: Path) -> bool:
    ext = path.suffix.lower()
    return ext in IMAGE_EXTS or ext in PDF_EXTS
