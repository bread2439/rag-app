from __future__ import annotations
from typing import List, Dict

def split_text(text: str, size: int = 900, overlap: int = 120) -> List[str]:
    """
    naive sliding-window on paragraphs; robust enough for MVP.
    """
    if not text:
        return []

    # prefer paragraph boundaries when possible
    paras = [p.strip() for p in text.split("\n\n") if p.strip()]
    chunks: List[str] = []
    buf: List[str] = []
    curr_len = 0

    def flush():
        nonlocal buf, curr_len
        if buf:
            chunks.append("\n\n".join(buf).strip())
            buf, curr_len = [], 0

    for para in paras:
        L = len(para)
        # if single para > size, hard-split it
        if L > size:
            idx = 0
            while idx < L:
                end = min(idx + size, L)
                chunks.append(para[idx:end])
                idx = max(end - overlap, end)
            continue

        if curr_len + L + 2 <= size:
            buf.append(para)
            curr_len += L + 2
        else:
            flush()
            buf = [para]
            curr_len = L + 2
    flush()

    # add overlaps between adjacent chunks
    if overlap and chunks:
        with_ov: List[str] = []
        for i, ch in enumerate(chunks):
            if i == 0:
                with_ov.append(ch)
            else:
                prev = with_ov[-1]
                ov = prev[-overlap:]
                with_ov.append((ov + ch) if ov not in ch[:overlap] else ch)
        chunks = with_ov
    return chunks

def pages_to_chunks(pages: List[Dict], size=900, overlap=120) -> List[Dict]:
    out: List[Dict] = []
    for p in pages:
        pieces = split_text(p["text"], size=size, overlap=overlap)
        for j, piece in enumerate(pieces):
            out.append({
                "page": p["page"],
                "chunk_idx": j,
                "text": piece,
                "char_len": len(piece)
            })
    return out
