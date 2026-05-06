from obs_info_kernel import Source, ObservacionismoResearchKernel
from obs_info_kernel.anti_information import AntiInformationMiner
from obs_info_kernel.connectors import ArxivConnector, HttpClient, OpenAlexConnector
from obs_info_kernel.dark_information import DarkInformationMiner
from obs_info_kernel.operator_profile import OperatorProfiler
from obs_info_kernel.topology import OperatorTopology


def demo_sources():
    return [
        Source.make("neuro", "conciencia integracion informacion prediccion actualizacion", "neuro"),
        Source.make("contempla", "observacion atencion residuo sesgo actualizacion", "contempla"),
        Source.make("ia", "agente contexto ruido jamming compuerta actualizacion", "ia"),
    ]


def test_anti_information_runs():
    report = AntiInformationMiner().mine(demo_sources(), min_coverage=0.34)
    assert report["summary"]["sources"] == 3
    assert "anti_score_mean" in report["summary"]
    assert "findings" in report


def test_dark_information_runs():
    report = DarkInformationMiner().mine("actualizacion residuo", demo_sources())
    assert report["summary"]["sources"] == 3
    assert "ranked_sources" in report
    assert report["ranked_sources"][0]["dark_state"] in {"dark_candidate", "dark_testable", "dark_validated", "dark_rejected"}
    assert "testability" in report["ranked_sources"][0]


def test_operator_profiler_runs():
    profile = OperatorProfiler().build(demo_sources()[0])
    assert profile.source_id
    assert "actualizacion" in profile.k_vector
    assert 0.0 <= profile.r_source <= 1.0


def test_operator_topology_cij_is_bounded():
    profiles = OperatorProfiler().build_many(demo_sources())
    topology = OperatorTopology().build(profiles, threshold=0.0)
    assert topology["status"] == "OPERATIONAL_PROXY_NOT_PROOF"
    assert topology["nodes"]
    assert topology["edges"]
    for edge in topology["edges"]:
        assert 0.0 <= edge["c_ij"] <= 1.0
    assert "not evidence" in topology["claim_boundary"]


def test_orchestrator_runs(tmp_path):
    (tmp_path / "a.md").write_text("observacion residuo actualizacion", encoding="utf-8")
    (tmp_path / "b.md").write_text("jamming sesgo compuerta informacion", encoding="utf-8")
    k = ObservacionismoResearchKernel(out_dir=tmp_path / "out")
    sources = k.load_sources_from_dir(tmp_path)
    report = k.analyze("residuo informacion", sources)
    assert report["estado_psi"]["R"] >= 0
    assert report["operator_atlas"]["profiles"] == 2
    assert report["operator_topology"]["status"] == "OPERATIONAL_PROXY_NOT_PROOF"
    assert "hypotheses" in report
    assert (tmp_path / "out" / "SESSION_FINGERPRINT.json").exists()


def test_orchestrator_no_sources_is_controlled(tmp_path):
    k = ObservacionismoResearchKernel(out_dir=tmp_path / "out")
    report = k.analyze("residuo informacion", [])
    assert report["run_status"]["status"] == "NO_SOURCES"
    assert report["run_status"]["claim_policy"] == "no_claims_without_sources"
    assert report["top_findings"][0]["kind"] == "warning"
    assert "No sources available" in (tmp_path / "out" / "observacionismo_research_report.md").read_text(encoding="utf-8")


def test_http_client_fixture_writes_cache_and_reuses_it(tmp_path):
    url = "https://example.invalid/api?q=residuo"
    first = HttpClient(cache_dir=tmp_path, fixtures={url: '{"ok": true}'}, min_interval_seconds=0)
    assert first.get(url) == '{"ok": true}'
    assert first.last_status["source"] == "fixture"

    second = HttpClient(cache_dir=tmp_path, ttl_seconds=3600, min_interval_seconds=0)
    assert second.get(url) == '{"ok": true}'
    assert second.last_status["source"] == "cache"


def test_openalex_connector_uses_fixture_without_network(tmp_path):
    url = "https://api.openalex.org/works?search=residuo&per_page=1&sort=relevance_score:desc&mailto=research%40example.com"
    payload = {
        "results": [
            {
                "title": "Residue test",
                "abstract": "A controlled fixture about residue.",
                "publication_year": 2026,
                "cited_by_count": 0,
                "id": "https://openalex.org/W1",
            }
        ]
    }
    http = HttpClient(cache_dir=tmp_path, fixtures={url: __import__("json").dumps(payload)}, min_interval_seconds=0)
    sources = OpenAlexConnector(http=http).search("residuo", max_results=1)
    assert len(sources) == 1
    assert sources[0].title == "Residue test"
    assert sources[0].metadata["source_type"] == "academic"


def test_arxiv_connector_uses_fixture_without_network(tmp_path):
    url = "https://export.arxiv.org/api/query?search_query=all:residuo&max_results=1&sortBy=relevance"
    payload = """<?xml version="1.0" encoding="UTF-8"?>
<feed xmlns="http://www.w3.org/2005/Atom">
  <entry>
    <id>http://arxiv.org/abs/2601.00001</id>
    <title>Residue fixture</title>
    <summary>Controlled fixture for offline connector tests.</summary>
    <published>2026-01-01T00:00:00Z</published>
    <author><name>Test Author</name></author>
  </entry>
</feed>"""
    http = HttpClient(cache_dir=tmp_path, fixtures={url: payload}, min_interval_seconds=0)
    sources = ArxivConnector(http=http).search("residuo", max_results=1)
    assert len(sources) == 1
    assert sources[0].title == "Residue fixture"
    assert sources[0].metadata["source_type"] == "preprint"
