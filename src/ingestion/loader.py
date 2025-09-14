from __future__ import annotations

import os
from pathlib import Path
from typing import Iterator, List, Sequence

from .llm_blocks import file_to_blocks
from .mime import guess_mime, is_supported
from .preprocess import compute_sha256, load_image_meta, load_pdf_meta
from .types import IngestedFile


def _iter_files(paths: Sequence[Path]) -> Iterator[Path]:
    for p in paths:
        if p.is_dir():
            for root, _dirs, files in os.walk(p):
                for name in files:
                    yield Path(root) / name
        else:
            yield p


def discover(paths: Sequence[Path]) -> List[Path]:
    out: List[Path] = []
    for p in _iter_files(paths):
        if is_supported(p):
            out.append(p)
    return out


def ingest_path(path: Path) -> IngestedFile:
    mime = guess_mime(path)
    data = path.read_bytes()
    meta_img = load_image_meta(path) if mime.startswith("image/") else None
    meta_pdf = load_pdf_meta(path) if mime == "application/pdf" else None

    blocks = file_to_blocks(path, mime)
    return IngestedFile(
        path=path,
        mime_type=mime,
        size_bytes=len(data),
        sha256=compute_sha256(data),
        image=meta_img,
        pdf=meta_pdf,
        blocks=blocks,
    )


def ingest(paths: Sequence[Path]) -> List[IngestedFile]:
    files = discover(paths)
    return [ingest_path(p) for p in files]
