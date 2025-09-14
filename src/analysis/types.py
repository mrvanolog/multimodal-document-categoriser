from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Dict, Optional


class DocCategory(str, Enum):
    INVOICE = "invoice"
    MARKETPLACE_LISTING_SCREENSHOT = "marketplace_listing_screenshot"
    CHAT_SCREENSHOT = "chat_screenshot"
    WEBSITE_SCREENSHOT = "website_screenshot"
    OTHER = "other"


@dataclass
class ClassificationResult:
    category: DocCategory
    confidence: float


@dataclass
class ExtractionResult:
    fields: Dict[str, object]
    raw_text: Optional[str] = None


@dataclass
class AnalysisResult:
    category: DocCategory
    confidence: float
    fields: Dict[str, object]
    raw_text: Optional[str] = None

    def to_dict(self) -> Dict[str, object]:
        """Convert AnalysisResult to a dictionary for JSON serialization."""
        return {
            "category": self.category.value,
            "confidence": self.confidence,
            "fields": self.fields,
            "raw_text": self.raw_text,
        }
