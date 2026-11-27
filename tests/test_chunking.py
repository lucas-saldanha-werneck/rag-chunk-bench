import pytest

from chunkbench.chunking import fixed, paragraphs, sentences


def test_fixed_sizes_and_no_loss():
    text = " ".join(f"w{i}" for i in range(95))
    chunks = fixed(text, 40)
    assert [len(c.split()) for c in chunks] == [40, 40, 15]
    assert " ".join(chunks) == text


def test_fixed_overlap_repeats_words():
    text = " ".join(f"w{i}" for i in range(60))
    chunks = fixed(text, 40, 10)
    assert chunks[0].split()[-10:] == chunks[1].split()[:10]
    assert chunks[-1].split()[-1] == "w59"


def test_fixed_bad_args():
    with pytest.raises(ValueError):
        fixed("a b c", 5, 5)
    with pytest.raises(ValueError):
        fixed("a b c", 0)


def test_fixed_empty_text():
    assert fixed("", 10) == [""] or fixed("", 10) == []


def test_sentences_never_cut_a_sentence():
    text = "Um dois três. Quatro cinco seis sete. Oito nove."
    chunks = sentences(text, 5)
    assert chunks == ["Um dois três.", "Quatro cinco seis sete.", "Oito nove."]


def test_sentences_packs_short_ones():
    chunks = sentences("A b. C d. E f.", 4)
    assert chunks == ["A b. C d.", "E f."]


def test_paragraphs_split_on_blank_line():
    assert paragraphs("a\nb\n\n\nc\n") == ["a\nb", "c"]
