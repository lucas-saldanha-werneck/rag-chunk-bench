import argparse
from pathlib import Path

from .evaluate import compare, load_docs, load_questions, to_markdown


def main(argv=None) -> int:
    root = Path(__file__).resolve().parent.parent / "data"
    p = argparse.ArgumentParser(description="Compare chunking strategies with BM25 retrieval.")
    p.add_argument("--docs", type=Path, default=root / "example_docs")
    p.add_argument("--questions", type=Path, default=root / "example_questions.json")
    p.add_argument("-k", type=int, default=3, help="chunks retrieved per question")
    a = p.parse_args(argv)
    rows = compare(load_docs(a.docs), load_questions(a.questions), a.k)
    print(to_markdown(rows, a.k))
    return 0
