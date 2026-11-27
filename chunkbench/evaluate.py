import json
from pathlib import Path

from .bm25 import BM25, tokenize
from .chunking import STRATEGIES


def load_docs(folder: Path) -> dict[str, str]:
    return {p.stem: p.read_text(encoding="utf-8") for p in sorted(folder.glob("*.txt"))}


def load_questions(path: Path) -> list[dict]:
    return json.loads(path.read_text(encoding="utf-8"))


def contains_answer(chunk: str, answer: str) -> bool:
    """True when the answer words appear in the chunk as one run, in order."""
    a, c = tokenize(answer), tokenize(chunk)
    return any(c[i:i + len(a)] == a for i in range(len(c) - len(a) + 1))


def run(docs: dict[str, str], questions: list[dict], strategy: str, k: int = 3) -> dict:
    cut = STRATEGIES[strategy]
    chunks = [(name, c) for name, text in docs.items() for c in cut(text)]
    index = BM25([c for _, c in chunks])
    hits, misses = 0, []
    for q in questions:
        top = index.top(q["question"], k)
        if any(contains_answer(chunks[i][1], q["answer"]) for i in top):
            hits += 1
        else:
            misses.append(q["id"])
    return {
        "strategy": strategy,
        "chunks": len(chunks),
        "hit_at_k": hits / len(questions),
        "hits": hits,
        "total": len(questions),
        "misses": misses,
    }


def compare(docs, questions, k: int = 3) -> list[dict]:
    return [run(docs, questions, s, k) for s in STRATEGIES]


def to_markdown(rows: list[dict], k: int) -> str:
    out = [f"| strategy | chunks | hit@{k} | missed questions |", "|---|---|---|---|"]
    for r in sorted(rows, key=lambda r: -r["hit_at_k"]):
        out.append(f"| {r['strategy']} | {r['chunks']} | {r['hits']}/{r['total']} | {', '.join(r['misses']) or '-'} |")
    return "\n".join(out)
