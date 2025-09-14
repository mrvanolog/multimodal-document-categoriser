import atexit
import json
import os
import shutil
from pathlib import Path

import streamlit as st

from src.analysis.analyser import DocAnalyser
from src.ingestion.loader import ingest

# --- Cleanup Function ---
TEMP_DIR = Path("temp_uploads")

def cleanup():
    """Remove the temporary directory on script exit."""
    if TEMP_DIR.exists():
        shutil.rmtree(TEMP_DIR)
        print(f"Cleaned up temporary directory: {TEMP_DIR}")

atexit.register(cleanup)


st.set_page_config(page_title="Document Analyser", layout="wide")

st.title("📄 Multimodal Document Analyser")
st.markdown("""
Upload your documents (images or PDFs) to automatically classify them and extract structured information.
This tool uses AI to understand the content of your files.
""")

# --- API Key Handling ---
if 'api_key' not in st.session_state:
    st.session_state.api_key = os.getenv("OPENROUTER_API_KEY")

if not st.session_state.api_key:
    st.warning("🔑 OpenRouter API key not found.")
    api_key_input = st.text_input(
        "Please enter your OpenRouter API key to proceed:",
        type="password",
        help="You can get your key from https://openrouter.ai/keys"
    )
    if api_key_input:
        st.session_state.api_key = api_key_input
        st.rerun()

# --- Main App Logic (only if API key is present) ---
if not st.session_state.get('api_key'):
    st.info("Please provide an API key to use the application.")
    st.stop()


if "analyser" not in st.session_state:
    with st.spinner("Initializing Analyser..."):
        st.session_state.analyser = DocAnalyser(api_key=st.session_state.api_key)

if "results" not in st.session_state:
    st.session_state.results = {}

uploaded_files = st.file_uploader(
    "Choose files to analyse",
    accept_multiple_files=True,
    type=["png", "jpg", "jpeg", "pdf"]
)

if uploaded_files:
    TEMP_DIR.mkdir(exist_ok=True)

    for uploaded_file in uploaded_files:
        file_path = TEMP_DIR / uploaded_file.name
        if file_path.name not in st.session_state.results:
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())

            with st.spinner(f"Analysing {uploaded_file.name}..."):
                try:
                    ingested_doc = ingest([file_path])[0]
                    analysis_result = st.session_state.analyser.analyse(ingested_doc)
                    st.session_state.results[file_path.name] = analysis_result.to_dict()
                    st.success(f"Successfully analysed {uploaded_file.name}")
                except Exception as e:
                    st.error(f"Error analysing {uploaded_file.name}: {e}")

if st.session_state.results:
    st.header("Analysis Results")

    if st.button("Save Results to JSON"):
        with open("analysis_results.json", "w") as f:
            json.dump(st.session_state.results, f, indent=2)
        st.success("Results saved to analysis_results.json")

    for filename, result in st.session_state.results.items():
        with st.expander(f"**{filename}** - Category: `{result['category']}` (Confidence: {result['confidence']:.2f})"):
            st.json(result["fields"])
            with st.container():
                st.subheader("Raw Text")
                st.text(result["raw_text"])
