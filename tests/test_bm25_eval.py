from pathlib import Path

from chunkbench.bm25 import BM25, tokenize
from chunkbench.cli import main
from chunkbench.evaluate import compare, contains_answer, load_docs, load_questions, run

DATA = Path(__file__).resolve().parent.parent / "data"


def test_tokenize_keeps_accents():
    assert tokenize("Férias, 30 dias!") == ["férias", "30", "dias"]


def test_bm25_ranks_matching_doc_first():
    idx = BM25(["gato preto dorme", "cachorro corre no parque", "o gato come peixe"])
    assert idx.top("cachorro parque", 1) == [1]
    assert set(idx.top("gato", 2)) == {0, 2}


def test_bm25_unknown_query_does_not_crash():
    assert len(BM25(["a b", "c d"]).top("zzz", 2)) == 2


def test_contains_answer_needs_the_run_in_order():
    assert contains_answer("posso vender dez dias de férias", "vender dez dias")
    assert not contains_answer("dez dias para vender", "vender dez dias")


def test_run_counts_hits_and_lists_misses():
    docs = {"d": "A senha tem catorze caracteres.\n\nO ar-condicionado fica a vinte graus."}
    qs = [
        {"id": "a", "question": "quantos caracteres a senha tem", "answer": "catorze caracteres"},
        {"id": "b", "question": "qual a cor do céu", "answer": "azul claro"},
    ]
    r = run(docs, qs, "paragraphs", k=1)
    assert (r["hits"], r["total"], r["misses"]) == (1, 2, ["b"])


def test_example_data_loads():
    docs, qs = load_docs(DATA / "example_docs"), load_questions(DATA / "example_questions.json")
    assert len(docs) == 4 and len(qs) == 16
    for q in qs:
        assert any(contains_answer(t, q["answer"]) for t in docs.values()), q["id"]


def test_compare_is_deterministic():
    docs, qs = load_docs(DATA / "example_docs"), load_questions(DATA / "example_questions.json")
    assert compare(docs, qs) == compare(docs, qs)


def test_cli_prints_table(capsys):
    assert main([]) == 0
    out = capsys.readouterr().out
    assert "| strategy |" in out and "paragraphs" in out


def test_whole_sentences_beat_tiny_fixed_chunks_on_example_data():
    docs, qs = load_docs(DATA / "example_docs"), load_questions(DATA / "example_questions.json")
    assert run(docs, qs, "sentences-40")["hits"] > run(docs, qs, "fixed-20")["hits"]
