from __future__ import annotations

import math
import re
import unicodedata
from collections import Counter, defaultdict
from typing import Dict, Iterable, List, Mapping, Sequence, Set, Tuple

STOPWORDS = {
    # ES
    "que", "como", "para", "por", "con", "una", "uno", "los", "las", "del", "de", "la", "el",
    "y", "o", "a", "en", "se", "no", "si", "es", "un", "al", "lo", "su", "sus", "mas",
    "menos", "esto", "esta", "este", "estos", "estas", "desde", "sobre", "entre", "cuando",
    "donde", "porque", "pero", "sin", "ser", "son", "fue", "hay", "tiene", "puede", "todo",
    "todos", "todas", "tambien", "solo", "misma", "mismo", "hacer", "cada", "otro", "otra",
    "otros", "otras", "ya", "muy", "asi", "ese", "esa", "eso", "aqui", "alli", "ahi",
    # EN
    "the", "and", "for", "with", "that", "this", "from", "are", "was", "were", "have", "has",
    "had", "not", "but", "you", "your", "into", "between", "where", "when", "what", "which",
    "then", "than", "also", "only", "there", "their", "them", "they", "will", "would", "could",
    "should", "can", "may", "might", "all", "any", "each", "other", "same", "more", "less",
}

WORD_RE = re.compile(r"[a-zA-ZáéíóúüñÁÉÍÓÚÜÑ0-9_\-]{3,}")
SENT_RE = re.compile(r"(?<=[.!?。！？])\s+")


def normalize(text: str) -> str:
    text = text or ""
    text = text.replace("\u2011", "-").replace("\u2013", "-").replace("\u2014", "-")
    text = unicodedata.normalize("NFKD", text)
    text = "".join(c for c in text if not unicodedata.combining(c))
    return text.lower()


def tokens(text: str, min_len: int = 3, keep_numbers: bool = False) -> List[str]:
    out = []
    for m in WORD_RE.finditer(normalize(text)):
        t = m.group(0).strip("_- ")
        if len(t) < min_len:
            continue
        if not keep_numbers and t.isdigit():
            continue
        if t in STOPWORDS:
            continue
        out.append(t)
    return out


def sentences(text: str) -> List[str]:
    chunks = SENT_RE.split((text or "").replace("\n", " "))
    return [c.strip() for c in chunks if len(c.strip()) > 20]


def ngrams(seq: Sequence[str], n: int = 2) -> List[str]:
    return [" ".join(seq[i : i + n]) for i in range(max(0, len(seq) - n + 1))]


def concept_counter(text: str, max_ngram: int = 2) -> Counter:
    ts = tokens(text)
    c = Counter(ts)
    for n in range(2, max_ngram + 1):
        for g in ngrams(ts, n):
            c[g] += 1
    return c


def top_terms(text: str, k: int = 30, max_ngram: int = 2) -> List[Tuple[str, int]]:
    return concept_counter(text, max_ngram=max_ngram).most_common(k)


def jaccard_distance(a: Iterable[str], b: Iterable[str]) -> float:
    A, B = set(a), set(b)
    if not A and not B:
        return 0.0
    if not A or not B:
        return 1.0
    return 1.0 - (len(A & B) / len(A | B))


def weighted_jaccard_distance(a: Mapping[str, float], b: Mapping[str, float]) -> float:
    keys = set(a) | set(b)
    if not keys:
        return 0.0
    mn = sum(min(float(a.get(k, 0.0)), float(b.get(k, 0.0))) for k in keys)
    mx = sum(max(float(a.get(k, 0.0)), float(b.get(k, 0.0))) for k in keys)
    if mx <= 0:
        return 0.0
    return 1.0 - mn / mx


def cosine(a: Mapping[str, float], b: Mapping[str, float]) -> float:
    keys = set(a) | set(b)
    if not keys:
        return 0.0
    dot = sum(float(a.get(k, 0.0)) * float(b.get(k, 0.0)) for k in keys)
    na = math.sqrt(sum(float(v) ** 2 for v in a.values()))
    nb = math.sqrt(sum(float(v) ** 2 for v in b.values()))
    if na <= 0 or nb <= 0:
        return 0.0
    return dot / (na * nb)


def tfidf(counters: Sequence[Counter], min_df: int = 1) -> List[Dict[str, float]]:
    n = len(counters)
    df: Dict[str, int] = defaultdict(int)
    for c in counters:
        for term in c:
            df[term] += 1
    vecs: List[Dict[str, float]] = []
    for c in counters:
        total = sum(c.values()) or 1
        v: Dict[str, float] = {}
        for term, count in c.items():
            if df[term] < min_df:
                continue
            idf = math.log((1 + n) / (1 + df[term])) + 1.0
            v[term] = (count / total) * idf
        vecs.append(v)
    return vecs


def rarity_scores(counters: Sequence[Counter]) -> Dict[str, float]:
    """0 frecuente, 1 raro dentro del corpus."""
    n = len(counters)
    if n == 0:
        return {}
    df: Dict[str, int] = defaultdict(int)
    for c in counters:
        for term in c:
            df[term] += 1
    return {term: 1.0 - (freq / n) for term, freq in df.items()}


def surrounding_sentences(text: str, terms: Iterable[str], max_items: int = 5) -> List[str]:
    wanted = [normalize(t) for t in terms if t]
    out = []
    for s in sentences(text):
        ns = normalize(s)
        if any(w in ns for w in wanted):
            out.append(s[:500])
        if len(out) >= max_items:
            break
    return out
