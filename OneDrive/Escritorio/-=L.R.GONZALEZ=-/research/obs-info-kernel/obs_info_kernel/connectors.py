from __future__ import annotations

import json
import time
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Dict, List, Mapping, Optional

from .core import Source


class HttpClient:
    def __init__(
        self,
        user_agent: str = "ObservacionismoResearchKernel/0.1 (research; respectful)",
        cache_dir: str | Path | None = None,
        ttl_seconds: int = 86400,
        min_interval_seconds: float = 1.0,
        fixtures: Optional[Mapping[str, str]] = None,
    ):
        self.user_agent = user_agent
        self.cache_dir = Path(cache_dir) if cache_dir else None
        self.ttl_seconds = max(0, int(ttl_seconds))
        self.min_interval_seconds = max(0.0, float(min_interval_seconds))
        self.fixtures = dict(fixtures or {})
        self.last_status: Dict[str, object] = {}
        self._last_request_at = 0.0

    def get(self, url: str, timeout: int = 20, retries: int = 2) -> Optional[str]:
        if url in self.fixtures:
            body = self.fixtures[url]
            self._write_cache(url, body)
            self.last_status = {"url": url, "source": "fixture", "ok": True}
            return body

        cached = self._read_cache(url, allow_stale=False)
        if cached is not None:
            self.last_status = {"url": url, "source": "cache", "ok": True}
            return cached

        for attempt in range(retries + 1):
            try:
                self._respect_rate_limit()
                req = urllib.request.Request(url, headers={"User-Agent": self.user_agent})
                with urllib.request.urlopen(req, timeout=timeout) as resp:
                    body = resp.read().decode("utf-8", errors="ignore")
                    self._write_cache(url, body)
                    self.last_status = {
                        "url": url,
                        "source": "network",
                        "ok": True,
                        "attempt": attempt + 1,
                    }
                    return body
            except Exception as exc:
                if attempt >= retries:
                    stale = self._read_cache(url, allow_stale=True)
                    if stale is not None:
                        self.last_status = {
                            "url": url,
                            "source": "stale_cache",
                            "ok": True,
                            "error": str(exc),
                        }
                        return stale
                    self.last_status = {
                        "url": url,
                        "source": "network",
                        "ok": False,
                        "attempt": attempt + 1,
                        "error": str(exc),
                    }
                    return None
                time.sleep(1.5 * (2 ** attempt))
        return None

    def _cache_path(self, url: str) -> Optional[Path]:
        if not self.cache_dir:
            return None
        import hashlib

        digest = hashlib.sha256(url.encode("utf-8", errors="ignore")).hexdigest()
        return self.cache_dir / f"{digest}.json"

    def _read_cache(self, url: str, allow_stale: bool) -> Optional[str]:
        path = self._cache_path(url)
        if not path or not path.exists():
            return None
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            return None
        age = time.time() - float(data.get("created_at", 0))
        if not allow_stale and self.ttl_seconds and age > self.ttl_seconds:
            return None
        body = data.get("body")
        return body if isinstance(body, str) else None

    def _write_cache(self, url: str, body: str) -> None:
        path = self._cache_path(url)
        if not path:
            return
        path.parent.mkdir(parents=True, exist_ok=True)
        payload = {"url": url, "created_at": time.time(), "body": body}
        path.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")

    def _respect_rate_limit(self) -> None:
        if self.min_interval_seconds <= 0:
            return
        now = time.monotonic()
        wait = self.min_interval_seconds - (now - self._last_request_at)
        if wait > 0:
            time.sleep(wait)
        self._last_request_at = time.monotonic()


class OpenAlexConnector:
    BASE = "https://api.openalex.org/works"

    def __init__(self, http: Optional[HttpClient] = None, mailto: str = "research@example.com"):
        self.http = http or HttpClient()
        self.mailto = mailto

    def search(self, query: str, max_results: int = 10, low_citation_first: bool = False) -> List[Source]:
        q = urllib.parse.quote(query)
        sort = "cited_by_count:asc" if low_citation_first else "relevance_score:desc"
        url = f"{self.BASE}?search={q}&per_page={max_results}&sort={sort}&mailto={urllib.parse.quote(self.mailto)}"
        data = self.http.get(url)
        if not data:
            return []
        try:
            items = json.loads(data).get("results", [])
        except Exception:
            return []
        out: List[Source] = []
        for it in items:
            title = it.get("title") or "OpenAlex result"
            abstract = it.get("abstract") or ""
            authors = [a.get("author", {}).get("display_name", "") for a in it.get("authorships", [])[:5]]
            year = it.get("publication_year")
            citations = it.get("cited_by_count", 0)
            doi = (it.get("doi") or "").replace("https://doi.org/", "")
            out.append(
                Source.make(
                    title=title,
                    text=f"{title}\n{abstract}",
                    domain="openalex_low_cited" if low_citation_first else "openalex",
                    year=year,
                    url=doi or it.get("id", ""),
                    citations=citations,
                    authors=authors,
                    raw_id=it.get("id", ""),
                    source_type="academic",
                )
            )
        return out


class ArxivConnector:
    BASE = "https://export.arxiv.org/api/query"

    def __init__(self, http: Optional[HttpClient] = None):
        self.http = http or HttpClient()

    def search(self, query: str, max_results: int = 10) -> List[Source]:
        q = urllib.parse.quote(query)
        url = f"{self.BASE}?search_query=all:{q}&max_results={max_results}&sortBy=relevance"
        data = self.http.get(url)
        if not data:
            return []
        try:
            root = ET.fromstring(data)
        except Exception:
            return []
        ns = {"a": "http://www.w3.org/2005/Atom"}
        out: List[Source] = []
        for entry in root.findall("a:entry", ns):
            title = (entry.findtext("a:title", default="", namespaces=ns) or "").strip()
            summary = (entry.findtext("a:summary", default="", namespaces=ns) or "").strip()
            link = (entry.findtext("a:id", default="", namespaces=ns) or "").strip()
            published = (entry.findtext("a:published", default="", namespaces=ns) or "").strip()
            year = int(published[:4]) if published[:4].isdigit() else None
            authors = [n.text or "" for n in entry.findall("a:author/a:name", ns)[:5]]
            out.append(
                Source.make(
                    title=title or "arXiv result",
                    text=f"{title}\n{summary}",
                    domain="arxiv",
                    year=year,
                    url=link,
                    authors=authors,
                    source_type="preprint",
                )
            )
        return out
