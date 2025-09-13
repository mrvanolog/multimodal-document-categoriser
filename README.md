# multimodal-document-categoriser

This repository contains a small project to build a multimodal document categorizer and extractor using LLMs.

## Ingestion module

The ingestion package normalizes supported files (images, PDFs), collects lightweight metadata, and prepares OpenAI-style content blocks for downstream LLM calls.

Supported inputs:
- Images: PNG, JPG, JPEG, WEBP, BMP, TIF, TIFF (converted to optimized JPEG for prompting)
- PDFs: attached as data URIs for models that can parse PDFs

Quick start:

```python
from pathlib import Path
from ingestion.loader import ingest

files = ingest([Path("data/")])
for f in files:
	print(f.path.name, f.mime_type, f.size_bytes, f.sha256)
	# LLM-ready blocks
	for b in f.blocks:
		print(b["type"])  # text | image_url | file
```

## Analysis module

DocAnalyser wraps classification and extraction using OpenAI-compatible models via OpenRouter. It consumes ingestion blocks and returns structured results.

Example:

```python
from pathlib import Path
from ingestion.loader import ingest
from analysis.analyser import DocAnalyser

docs = ingest([Path("data/")])
analyser = DocAnalyser()

for d in docs:
    print(d.path.name)
    res = analyser.analyse(d)
    print(f"Category: {res.category.value}, Confidence: {res.confidence}")
    print(f"Fields: {res.fields}")
    print(f"Raw text: {res.raw_text}")
    print("-" * 30)
```