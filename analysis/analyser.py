from __future__ import annotations

import json
import os
from typing import Dict, List, Optional

from openai import OpenAI
import requests

from ingestion.types import IngestedFile

from .prompts import CLASSIFY_INSTRUCTION, extraction_instruction
from .schemas import classification_schema, extraction_schema_for
from .types import AnalysisResult, Category, ClassificationResult, ExtractionResult


class DocAnalyser:
    """Encapsulates client, classification, and extraction logic.

    Usage:
        analyser = DocAnalyser()
        cls = analyser.classify(ingested)
        ext = analyser.extract(ingested, cls.category)
    """

    def __init__(
        self,
        model: str = "openai/gpt-4o",
        base_url: str = "https://openrouter.ai/api/v1",
        api_key: Optional[str] = None,
    ) -> None:
        self.model = model
        self.client = OpenAI(
            base_url=base_url,
            api_key=api_key or os.getenv("OPENROUTER_API_KEY"),
        )

    def _chat_json(self, blocks: List[dict], schema: Dict) -> Dict:
        r = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": blocks}],
            response_format={
                "type": "json_schema",
                "json_schema": {"name": "schema", "schema": schema},
            },
        )
        content = r.choices[0].message.content

        return json.loads(content)

    def _prepend_instruction(self, instruction: str, blocks: List[dict]) -> List[dict]:
        return [{"type": "text", "text": instruction}, *blocks]

    def classify(self, doc: IngestedFile) -> ClassificationResult:
        """Classify the document into a specific category.

        Args:
            doc (IngestedFile): The document to classify.

        Returns:
            ClassificationResult: The result of the classification.
        """
        blocks = self._prepend_instruction(CLASSIFY_INSTRUCTION, doc.blocks)
        js = self._chat_json(blocks, classification_schema())
        try:
            category = Category(js.get("category"))  # type: ignore[arg-type]
        except ValueError:
            category = Category.OTHER
        conf = float(js.get("confidence", 0.0))

        return ClassificationResult(category=category, confidence=conf)

    def extract(
        self, doc: IngestedFile, category: Category
    ) -> ExtractionResult:
        """Extract structured information from the document.

        Args:
            doc (IngestedFile): The document to extract from.
            category (Category): The category of the document.

        Returns:
            ExtractionResult: The result of the extraction.
        """
        schema = extraction_schema_for(category)
        blocks = self._prepend_instruction(
            extraction_instruction(category),
            doc.blocks,
        )
        js = self._chat_json(blocks, schema)
        fields = js.get("fields", {}) if isinstance(js, dict) else {}
        raw_text = js.get("raw_text") if isinstance(fields, dict) else None

        return ExtractionResult(
            fields=fields,
            raw_text=raw_text,
        )

    def analyse(self, doc: IngestedFile) -> AnalysisResult:
        """Classify and extract information from the document.

        Args:
            doc (IngestedFile): The document to analyse.
        Returns:
            AnalysisResult: The combined result of classification and extraction.
        """
        cls = self.classify(doc)
        ext = self.extract(doc, cls.category)

        return AnalysisResult(
            category=cls.category,
            confidence=cls.confidence,
            fields=ext.fields,
            raw_text=ext.raw_text,
        )

    def api_key_usage(self) -> Dict:
        """Check the current API key usage."""
        r = requests.get(
            "https://openrouter.ai/api/v1/key",
            headers={"Authorization": f"Bearer {os.environ['OPENROUTER_API_KEY']}"},
            timeout=10,
        )

        return r.json()
