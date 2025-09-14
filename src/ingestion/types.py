from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Literal, Optional, TypedDict, Union


# ----- LLM content block types (OpenAI-style) -----

class _ImageURL(TypedDict):
    url: str  # data URI or http(s) URL


class LLMTextBlock(TypedDict):
    type: Literal["text"]
    text: str


class LLMImageBlock(TypedDict):
    type: Literal["image_url"]
    image_url: _ImageURL


class _FilePayload(TypedDict):
    filename: str
    file_data: str  # data URI for PDFs


class LLMFileBlock(TypedDict):
    type: Literal["file"]
    file: _FilePayload


LLMBlock = Union[LLMTextBlock, LLMImageBlock, LLMFileBlock]


# ----- Ingested file metadata -----

@dataclass
class ImageMeta:
    format: Optional[str] = None  # e.g., JPEG, PNG
    width: Optional[int] = None
    height: Optional[int] = None
    mode: Optional[str] = None  # e.g., RGB, L


@dataclass
class PdfMeta:
    page_count: Optional[int] = None


@dataclass
class IngestedFile:
    # input
    path: Path
    mime_type: str

    # derived
    size_bytes: Optional[int] = None
    sha256: Optional[str] = None

    # modality-specific metadata
    image: Optional[ImageMeta] = None
    pdf: Optional[PdfMeta] = None

    # ready-to-send content blocks for LLMs
    blocks: List[LLMBlock] = field(default_factory=list)

    # arbitrary extra information
    extra: Dict[str, object] = field(default_factory=dict)
