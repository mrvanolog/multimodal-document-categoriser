from __future__ import annotations

import io
from hashlib import sha256
from pathlib import Path

from PIL import Image
from pypdf import PdfReader
from pypdf.errors import PdfReadError

from .types import ImageMeta, PdfMeta


def compute_sha256(data: bytes) -> str:
    return sha256(data).hexdigest()


# --- Image utils (Pillow) ---

def load_image_meta(path: Path) -> ImageMeta:
    with Image.open(path) as img:
        return ImageMeta(
            format=img.format,
            width=img.width,
            height=img.height,
            mode=img.mode,
        )


def normalize_image_to_jpeg_bytes(
    path: Path, max_side: int = 1600, quality: int = 85
) -> bytes:
    """Load an image, downscale if largest side > max_side, return JPEG bytes.
    Keeps aspect ratio, converts to RGB.
    """
    with Image.open(path) as img:
        img = img.convert("RGB")
        w, h = img.size
        scale = 1.0
        longest = max(w, h)
        if longest > max_side:
            scale = max_side / float(longest)
        if scale < 1.0:
            new_size = (int(w * scale), int(h * scale))
            img = img.resize(new_size, Image.Resampling.LANCZOS)
        buf = io.BytesIO()
        img.save(buf, format="JPEG", quality=quality, optimize=True)
        return buf.getvalue()


# --- PDF utils (pypdf for lightweight metadata) ---

def load_pdf_meta(path: Path) -> PdfMeta:
    try:
        reader = PdfReader(str(path))
        return PdfMeta(page_count=len(reader.pages))
    except (PdfReadError, OSError, ValueError):
        return PdfMeta()
