from __future__ import annotations

import json
import re
from pathlib import Path


WABI_ROOT = Path(__file__).resolve().parents[1]
MEDIOEVO_ROOT = WABI_ROOT.parents[2]
RUN_ROOT = MEDIOEVO_ROOT / "qa_artifacts" / "release_validation" / "RUN_TREE_HEALTH_WORKBENCH_PANEL_20260518"
CLEANUP_RUN_ROOT = MEDIOEVO_ROOT / "qa_artifacts" / "release_validation" / "RUN_TREE_WORKBENCH_CODE_CLEANUP_20260518"
PANEL_ROOT = RUN_ROOT / "tree_workbench_health_panel"


def test_tree_health_state_schema_and_provider_state():
    payload = json.loads((RUN_ROOT / "TREE_HEALTH_STATE_20260518.json").read_text(encoding="utf-8"))

    assert payload["schema"] == "tree_health_workbench_panel.state.v1"
    assert payload["state_fingerprint"] == "TREE-HEALTH-WORKBENCH-PANEL-20260518"
    assert payload["tree"]["files_inventoried"] == 2243
    assert payload["tree"]["cache_files_quarantined"] == 1257
    assert payload["tree"]["direct_delete_used"] is False
    assert payload["tree"]["rollback_available"] is True
    assert payload["hashing"]["classification"] == "LIVE_LOG_LOCKED_NOT_SECRET"
    assert payload["provider"]["cloud_status"] == "SMOKE_FAIL_REDACTED"
    assert payload["provider"]["next_smoke"] == "DO_NOT_CALL"
    assert payload["publication_gate"] == "BLOCK"
    assert payload["secret_values_printed"] is False


def test_tree_health_panel_data_schema():
    payload = json.loads((PANEL_ROOT / "tree_workbench_health_data.json").read_text(encoding="utf-8"))

    assert payload["schema"] == "tree_workbench_health.panel_data.v1"
    assert payload["status"]["overall"] == "PASS_LOCAL"
    assert payload["tree_baseline"]["hash_error_classification"] == "LIVE_LOG_LOCKED_NOT_SECRET"
    assert payload["cleanup_actions"]["direct_delete_used"] is False
    assert payload["provider_health"]["cloud_status"] == "SMOKE_FAIL_REDACTED"
    assert payload["provider_health"]["next_smoke"] == "DO_NOT_CALL"
    assert payload["external_assets_used"] is False


def test_tree_health_panel_no_external_urls_or_secret_values():
    combined = "\n".join(
        [
            (PANEL_ROOT / "index.html").read_text(encoding="utf-8"),
            (PANEL_ROOT / "tree_workbench_health_data.json").read_text(encoding="utf-8"),
            (RUN_ROOT / "TREE_HEALTH_STATE_20260518.json").read_text(encoding="utf-8"),
        ]
    )

    assert "http://" not in combined
    assert "https://" not in combined
    assert "cdn" not in combined.lower()
    assert not re.search(r"(?i)nvapi-[A-Za-z0-9_-]{16,}", combined)
    assert not re.search(r"(?i)bearer\s+[A-Za-z0-9._~+/=-]{16,}", combined)
    assert "secret-value" not in combined


def test_tree_health_main_ui_integration_present():
    desktop = WABI_ROOT.parents[3]
    main_ui = desktop / "-= BRAIN_OS =-" / "apps" / "local" / "wabi_ui" / "index.html"
    text = main_ui.read_text(encoding="utf-8")

    assert "treeHealthPanel" in text
    assert "Tree Health / Workbench Health" in text
    assert "/api/tree-health" in text


def test_cleanup_rollback_manifest_still_reversible():
    manifest = json.loads((CLEANUP_RUN_ROOT / "TREE_WORKBENCH_CODE_CLEANUP_MOVE_MANIFEST.json").read_text(encoding="utf-8"))

    assert manifest["delete_direct"] is False
    assert manifest["errors"] == []
    assert len(manifest["moves"]) == 1257
    assert all(item["reversible"] is True for item in manifest["moves"])
