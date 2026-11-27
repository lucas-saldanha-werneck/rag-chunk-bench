"""Three ways to cut a document into chunks. Sizes are counted in words."""
import re


def fixed(text: str, size: int = 40, overlap: int = 0) -> list[str]:
    if size <= 0 or not 0 <= overlap < size:
        raise ValueError("need size > 0 and 0 <= overlap < size")
    words = text.split()
    step = size - overlap
    chunks = []
    for start in range(0, len(words), step):
        chunks.append(" ".join(words[start:start + size]))
        if start + size >= len(words):
            break
    return chunks


def sentences(text: str, size: int = 40) -> list[str]:
    """Pack whole sentences until a chunk reaches `size` words."""
    parts = re.split(r"(?<=[.!?])\s+", text.strip())
    chunks, current, count = [], [], 0
    for s in parts:
        n = len(s.split())
        if current and count + n > size:
            chunks.append(" ".join(current))
            current, count = [], 0
        current.append(s)
        count += n
    if current:
        chunks.append(" ".join(current))
    return chunks


def paragraphs(text: str) -> list[str]:
    return [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]


STRATEGIES = {
    "fixed-20": lambda t: fixed(t, 20),
    "fixed-40": lambda t: fixed(t, 40),
    "fixed-40-overlap-10": lambda t: fixed(t, 40, 10),
    "sentences-40": lambda t: sentences(t, 40),
    "paragraphs": paragraphs,
}
