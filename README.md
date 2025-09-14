# Multimodal Document Categoriser

This repository contains a small project to build a multimodal document categoriser and extractor using LLMs.

## Streamlit Web App

The project includes a Streamlit web interface for easy interaction.

### Running the App

1.  **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

2.  **Set API Key:**

    The application requires an OpenRouter API key. You can either set it as an environment variable:

    ```bash
    export OPENROUTER_API_KEY="your-key-here"
    ```

    Or you can enter it directly in the application when prompted.

3.  **Run the app:**

    ```bash
    streamlit run app.py
    ```

This will launch the web application in your browser. You can then upload documents for analysis.

## Components

### Ingestion module

The ingestion package normalizes supported files (images, PDFs), collects lightweight metadata, and prepares OpenAI-style content blocks for downstream LLM calls.

Supported inputs:
- Images: PNG, JPG, JPEG, WEBP, BMP, TIF, TIFF (converted to optimized JPEG for prompting)
- PDFs: attached as data URIs for models that can parse PDFs

Example:

```python
from pathlib import Path
from src.ingestion.loader import ingest

files = ingest([Path("data/")])
for f in files:
	print(f.path.name, f.mime_type, f.size_bytes, f.sha256)
	# LLM-ready blocks
	for b in f.blocks:
		print(b["type"])  # text | image_url | file
```

### Analysis module

DocAnalyser wraps classification and extraction using OpenAI-compatible models via OpenRouter. It consumes ingestion blocks and returns structured results.

Example:

```python
from pathlib import Path
from src.ingestion.loader import ingest
from src.analysis.analyser import DocAnalyser

docs = ingest([Path("data/")])
analyser = DocAnalyser()

results = {}
for d in docs:
    print(d.path.name)
    res = analyser.analyse(d)
    print(f"Category: {res.category.value}, Confidence: {res.confidence}")
    results[d.path.name] = res
```