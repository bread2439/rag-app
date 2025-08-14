from pathlib import Path
import json
from typing import Any

def safe_mkdir(p: Path) -> None:
    p.mkdir(parents=True, exist_ok=True)

def write_json(p: Path, obj: Any) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(obj, ensure_ascii=False, indent=2), encoding="utf-8")

def read_json(p: Path) -> Any:
    return json.loads(p.read_text(encoding="utf-8"))

def write_jsonl(p: Path, rows: list[dict]) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
