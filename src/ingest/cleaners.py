import re
from typing import List, Dict

_HEADER_FOOTER_RE = re.compile(r"^\s*(page\s*\d+|\d+\s*/\s*\d+)\s*$", re.I)

def normalize_whitespace(text: str) -> str:
    # collapse multiple spaces, normalize newlines
    text = text.replace("\r", "")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()

def strip_headers_footers(lines: List[str]) -> List[str]:
    return [ln for ln in lines if not _HEADER_FOOTER_RE.match(ln.strip())]

def clean_page_text(raw: str) -> str:
    if not raw:
        return ""
    lines = [l for l in raw.split("\n")]
    lines = strip_headers_footers(lines)
    text = "\n".join(lines)
    return normalize_whitespace(text)

def clean_pages(pages: List[Dict]) -> List[Dict]:
    return [{"page": p["page"], "text": clean_page_text(p["text"])} for p in pages]
