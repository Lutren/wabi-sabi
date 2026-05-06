"""Artifact records and graph projection for the local motor."""

from __future__ import annotations

from typing import Any

from .contracts import ARTIFACT_RECORD_SCHEMA
from .snapshot import canonical_sha256


def create_artifact_record(
    kind: str,
    title: str,
    content: dict[str, Any],
    *,
    parents: list[str] | None = None,
    evidence: list[dict[str, str]] | None = None,
    status: str = "draft",
    scores: dict[str, float] | None = None,
) -> dict[str, Any]:
    body = {
        "kind": kind,
        "title": title,
        "content": content,
        "parents": parents or [],
        "evidence": evidence or [],
    }
    content_sha256 = canonical_sha256(body)
    return {
        "schema": ARTIFACT_RECORD_SCHEMA,
        "artifact_id": "art_" + content_sha256[:16],
        "kind": kind,
        "title": title,
        "content_sha256": content_sha256,
        "lineage": {
            "derived_from": parents or [],
            "supports": [item.get("sha256", "") for item in evidence or [] if item.get("sha256")],
        },
        "status": status,
        "scores": scores or {},
        "content": content,
        "evidence": evidence or [],
    }


def project_artifact_graph(artifacts: list[dict[str, Any]]) -> dict[str, Any]:
    nodes = []
    edges = []
    for artifact in artifacts:
        artifact_id = str(artifact["artifact_id"])
        nodes.append(
            {
                "artifact_id": artifact_id,
                "kind": artifact.get("kind", "unknown"),
                "status": artifact.get("status", "unknown"),
                "content_sha256": artifact.get("content_sha256", ""),
            }
        )
        lineage = artifact.get("lineage", {})
        for parent in lineage.get("derived_from", []):
            edges.append({"from": parent, "to": artifact_id, "edge_type": "derived_from"})
        for support in lineage.get("supports", []):
            edges.append({"from": support, "to": artifact_id, "edge_type": "supports"})
    return {"nodes": nodes, "edges": edges, "node_count": len(nodes), "edge_count": len(edges)}
