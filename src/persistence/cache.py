from pathlib import Path
from dataclasses import dataclass

DATA_DIR = Path("./data")

@dataclass(frozen=True)
class DocPaths:
    root: Path
    text_json: Path
    chunks_jsonl: Path
    chroma_dir: Path

def make_paths(doc_hash: str) -> DocPaths:
    root = DATA_DIR / doc_hash
    return DocPaths(
        root=root,
        text_json=root / "text.json",
        chunks_jsonl=root / "chunks.jsonl",
        chroma_dir=root / "chroma",
    )
