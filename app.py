import streamlit as st
from src.utils.hashing import sha256_bytes
from src.ingest.pdf_loader import load_pdf_bytes
from src.ingest.cleaners import clean_pages
from src.chunking.splitter import pages_to_chunks
from src.persistence.cache import make_paths
from src.utils.io import write_json, write_jsonl

st.set_page_config(page_title="AI Research Companion - MVP", layout="wide")
st.title("AI Technical Research Companion (MVP - Ingestion/Chunking)")

uploaded = st.file_uploader("Upload a PDF", type=["pdf"])
if uploaded and st.button("Process Document"):
    b = uploaded.read()
    doc_hash = sha256_bytes(b)
    paths = make_paths(doc_hash)
    doc = load_pdf_bytes(b)
    pages = clean_pages(doc["pages"])
    chunks = pages_to_chunks(pages, size=900, overlap=120)
    write_json(paths.text_json, {"meta": doc["meta"], "pages": pages})
    write_jsonl(paths.chunks_jsonl, chunks)
    st.success(f"Processed {len(pages)} pages -> {len(chunks)} chunks")
    st.write(f"doc_hash: `{doc_hash}`")
    st.dataframe([{"page": c["page"], "len": c["char_len"]} for c in chunks[:10]])
