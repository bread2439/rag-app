from pathlib import Path
from src.utils.hashing import sha256_bytes
from src.utils.io import write_json, write_jsonl, safe_mkdir
from src.utils.logging import get_logger
from src.ingest.pdf_loader import load_pdf_bytes
from src.ingest.cleaners import clean_pages
from src.chunking.splitter import pages_to_chunks
from src.persistence.cache import make_paths

logger = get_logger("build")

def process_pdf(path: Path):
    pdf_bytes = path.read_bytes()
    doc_hash = sha256_bytes(pdf_bytes)
    paths = make_paths(doc_hash)
    safe_mkdir(paths.root)

    # ingest
    doc = load_pdf_bytes(pdf_bytes)
    pages = clean_pages(doc["pages"])
    write_json(paths.text_json, {"meta": doc["meta"], "pages": pages})

    # chunk
    chunks = pages_to_chunks(pages, size=900, overlap=120)
    write_jsonl(paths.chunks_jsonl, chunks)

    logger.info("Processed %s pages -> %s chunks", len(pages), len(chunks))
    logger.info("doc_hash=%s  cache=%s", doc_hash, paths.root)

if __name__ == "__main__":
    sample = Path("eval/sample_pdfs/nn_decoders_for_surface_codes.pdf")  # hard code pdf for testing
    assert sample.exists(), "Put a sample PDF at eval/sample_pdfs/your_sample.pdf"
    process_pdf(sample)
