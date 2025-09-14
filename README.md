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

**Note:** The `data/` directory contains a set of example documents (`.pdf`, `.png`, `.jpeg`) that you can use to test the application. `analysis_results.json` contains an example output of the application for these files.

## Assumptions and Design Decisions

- **LLM Provider**: The application is built to use OpenAI-compatible APIs, with OpenRouter as the default provider for model flexibility. The `DocAnalyser` can be easily configured to point to a different service.
- **Structured Output**: We rely on the `json_schema` feature of modern LLMs to enforce a strict, predictable output format for both classification and data extraction. This is crucial for the reliability of the system.
- **Modularity**: The project is divided into clear, separate components: `ingestion` for file handling, `analysis` for AI-powered logic, and a Streamlit app for the user interface. This separation makes the system easier to maintain and extend.
- **Temporary File Handling**: The Streamlit app stores uploaded files in a `temp_uploads` directory, which is automatically cleaned up upon application exit using the `atexit` module.

## Known Limitations and Possible Improvements

- **Synchronous Processing**: The Streamlit app processes uploaded files one by one in a blocking manner. For a large number of files, this could lead to a slow user experience.
  - **Improvement**: Implement asynchronous processing using background workers to analyse files without blocking the main UI thread.
- **Basic Error Handling**: The error handling is currently quite general.
  - **Improvement**: Implement more specific error handling for API-related issues (e.g., authentication failures, rate limits, model not found) to provide clearer feedback to the user.
- **Basic File Handling**: Currently all files are stored in a single folder in the repository.
  - **Improvement**: Add a file handler class that works with files and can be modified to store them in different locations: locally, in a database, etc.
  - **Improvement**: Add database that will store files permanently (e.g. PostgreSQL) or temporary (e.g. Redis).
- **PDF Processing Strategy**: The app currently relies on the LLM's native ability to process PDF files. A workaround was added to force routing to `openai/gpt-4o` to ensure compatibility.
  - **Improvement**: A more robust approach would be to use a library like `PyMuPDF` to extract text and images from PDFs during the ingestion phase. This would increase compatibility with models that don't natively support the `file` content type.
- **Validation Module**: The originally planned `validation` module has not been implemented.
  - **Improvement**: Create a validation module to perform secondary checks on the extracted data, potentially using `Pydantic` for schema validation or implementing custom business logic rules.
  - **Improvement**: Create a library of documents with expected outputs and evaluate using 3rd party tools, e.g. LangSmith.

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