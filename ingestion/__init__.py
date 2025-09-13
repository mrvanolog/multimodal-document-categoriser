"""
Ingestion package

Responsibilities:
- File type detection and safe reading
- Lightweight preprocessing (e.g., image normalization)
- Constructing LLM-friendly content blocks (image/file/text)
- Producing a consistent IngestedFile metadata object

Public API will be expanded as modules are implemented.
"""

from typing import TYPE_CHECKING

__all__ = [
    "IngestedFile",
    "ImageMeta",
    "PdfMeta",
    "LLMTextBlock",
    "LLMImageBlock",
    "LLMFileBlock",
]


def __getattr__(name: str):  # pragma: no cover - lazy export convenience
    if name in __all__:
        from . import types as _types

        return getattr(_types, name)
    raise AttributeError(name)


if TYPE_CHECKING:  # for type checkers only
    from .types import (  # noqa: F401
        IngestedFile,
        ImageMeta,
        PdfMeta,
        LLMTextBlock,
        LLMImageBlock,
        LLMFileBlock,
    )
