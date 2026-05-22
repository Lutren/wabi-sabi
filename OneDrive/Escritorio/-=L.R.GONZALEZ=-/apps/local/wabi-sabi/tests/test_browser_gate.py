from wabi_sabi.core.browser_gate import build_browser_gate_policy, evaluate_browser_request


def test_browser_gate_allows_local_and_read_only_targets(tmp_path):
    policy = build_browser_gate_policy(tmp_path)

    assert policy["schema"] == "wabi.browser_gate.v1"
    assert policy["decision_context"]["mode"] == "COMPLETO_GATEADO"

    local = evaluate_browser_request("http://localhost:3000", "inspect")
    public = evaluate_browser_request("https://example.com/docs", "read")
    extract = evaluate_browser_request("https://example.com/docs", "extract")

    assert local["gate"] == "APPROVE"
    assert "local_browser_target" in local["reasons"]
    assert public["gate"] == "APPROVE"
    assert "public_read_only_browser_target" in public["reasons"]
    assert extract["gate"] == "APPROVE"


def test_browser_gate_reviews_or_blocks_risky_browser_actions():
    login = evaluate_browser_request("https://example.com/login", "read")
    billing = evaluate_browser_request("https://example.com/settings/billing", "submit payment")

    assert login["gate"] == "REVIEW"
    assert billing["gate"] == "BLOCK"
    assert any(reason.startswith("review_term:") for reason in billing["reasons"])
