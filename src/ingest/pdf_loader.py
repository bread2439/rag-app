from __future__ import annotations
from pathlib import Path
from typing import List, Dict, Any
import io

import PyPDF2
import pdfplumber

from src.utils.logging import get_logger
logger = get_logger(__name__)

class PDFLoadError(Exception): ...
class PDFEncryptedError(PDFLoadError): ...

def load_pdf_bytes(pdf_bytes: bytes) -> Dict[str, Any]:
    """
    Returns:
      {
        "num_pages": int,
        "pages": [{"page": i, "text": "..."}],
        "meta": {...}
      }
    Raises:
      PDFEncryptedError if encrypted without password.
    """
    # encryption check (fast)
    try:
        reader = PyPDF2.PdfReader(io.BytesIO(pdf_bytes))
        if reader.is_encrypted:
            raise PDFEncryptedError("PDF is encrypted; cannot extract text.")
    except Exception as e:
        logger.warning("PyPDF2 check failed: %s", e)

    # extract with pdfplumber (better layout)
    pages: List[dict] = []
    with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
        meta = pdf.metadata or {}
        for i, page in enumerate(pdf.pages, start=1):
            try:
                txt = page.extract_text(x_tolerance=1, y_tolerance=1) or ""
            except Exception as e:
                logger.warning("Failed page %s: %s", i, e)
                txt = ""
            pages.append({"page": i, "text": txt})

    return {
        "num_pages": len(pages),
        "pages": pages,
        "meta": meta,
    }
