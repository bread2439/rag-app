from pathlib import Path
from src.ingest.pdf_loader import load_pdf_bytes
from src.ingest.cleaners import clean_pages
from src.chunking.splitter import pages_to_chunks

def test_extract_and_chunk():
    p = Path("eval/sample_pdfs/your_sample.pdf")
    if not p.exists():  # allow test to skip if sample not present in CI
        return
    doc = load_pdf_bytes(p.read_bytes())
    assert doc["num_pages"] >= 1
    pages = clean_pages(doc["pages"])
    chunks = pages_to_chunks(pages, size=900, overlap=120)
    assert len(chunks) >= 1
    # check metadata presence
    assert {"page","chunk_idx","text"}.issubset(chunks[0].keys())
