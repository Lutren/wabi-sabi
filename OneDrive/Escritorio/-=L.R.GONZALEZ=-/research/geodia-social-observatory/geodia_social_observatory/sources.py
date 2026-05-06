"""Source allowlist and epistemic policy for social snapshots."""

from __future__ import annotations

from dataclasses import dataclass


class SourcePolicyError(ValueError):
    """Raised when a fixture or live source is outside the allowlist."""


@dataclass(frozen=True)
class SourcePolicy:
    source_id: str
    label: str
    url_prefixes: tuple[str, ...]
    role: str
    license_notice: str
    classification_floor: str
    requires_api_key: bool = False
    special_notice: str = ""


ALLOWED_SOURCES: dict[str, SourcePolicy] = {
    "world_bank_indicators": SourcePolicy(
        source_id="world_bank_indicators",
        label="World Bank Indicators API",
        url_prefixes=(
            "https://api.worldbank.org/",
            "https://datahelpdesk.worldbank.org/knowledgebase/articles/889392-about-the-indicators-api-documentation",
        ),
        role="indicator_source",
        license_notice="Review World Bank data terms before live publication.",
        classification_floor="CERTEZA",
    ),
    "imf_data": SourcePolicy(
        source_id="imf_data",
        label="IMF Data APIs",
        url_prefixes=("https://data.imf.org/",),
        role="indicator_source",
        license_notice="Review IMF API and dataset terms before live publication.",
        classification_floor="CERTEZA",
    ),
    "oecd_api": SourcePolicy(
        source_id="oecd_api",
        label="OECD API",
        url_prefixes=("https://www.oecd.org/", "https://sdmx.oecd.org/"),
        role="indicator_source",
        license_notice="Review OECD data terms before live publication.",
        classification_floor="CERTEZA",
    ),
    "eurostat_sdmx": SourcePolicy(
        source_id="eurostat_sdmx",
        label="Eurostat SDMX API",
        url_prefixes=("https://ec.europa.eu/eurostat/", "https://ec.europa.eu/eurostat/api/"),
        role="indicator_source",
        license_notice="Review Eurostat reuse and attribution rules before live publication.",
        classification_floor="CERTEZA",
    ),
    "fred_api": SourcePolicy(
        source_id="fred_api",
        label="FRED API",
        url_prefixes=("https://fred.stlouisfed.org/", "https://api.stlouisfed.org/"),
        role="indicator_source",
        license_notice="FRED requires an API key for live use; include no-endorsement notice.",
        classification_floor="CERTEZA",
        requires_api_key=True,
        special_notice="Do not store API keys in fixtures, manifests or release artifacts.",
    ),
    "owid_grapher": SourcePolicy(
        source_id="owid_grapher",
        label="Our World in Data Grapher API",
        url_prefixes=("https://ourworldindata.org/grapher/",),
        role="indicator_source",
        license_notice="Review the original provider license for each OWID dataset.",
        classification_floor="CERTEZA",
        special_notice="OWID can aggregate third-party datasets; provider license review is mandatory.",
    ),
    "gdelt_doc_2": SourcePolicy(
        source_id="gdelt_doc_2",
        label="GDELT DOC 2.0",
        url_prefixes=("https://api.gdeltproject.org/api/v2/doc/doc", "https://blog.gdeltproject.org/"),
        role="media_narrative_signal_only",
        license_notice="Use as media narrative signal only; do not treat as raw social fact.",
        classification_floor="INFERENCIA",
        special_notice="GDELT claims must remain narrative/media-signal claims unless corroborated.",
    ),
}


def get_source_policy(source_id: str) -> SourcePolicy:
    try:
        return ALLOWED_SOURCES[source_id]
    except KeyError as exc:
        raise SourcePolicyError(f"source is not allowlisted: {source_id}") from exc


def validate_source(source_id: str, source_url: str) -> SourcePolicy:
    policy = get_source_policy(source_id)
    if not source_url.startswith(policy.url_prefixes):
        raise SourcePolicyError(f"source URL is outside allowlist for {source_id}: {source_url}")
    return policy


def source_catalog() -> list[dict[str, object]]:
    return [
        {
            "source_id": policy.source_id,
            "label": policy.label,
            "role": policy.role,
            "url_prefixes": list(policy.url_prefixes),
            "license_notice": policy.license_notice,
            "classification_floor": policy.classification_floor,
            "requires_api_key": policy.requires_api_key,
            "special_notice": policy.special_notice,
        }
        for policy in ALLOWED_SOURCES.values()
    ]
