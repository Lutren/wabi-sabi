"""GEODIA Social Observatory local research MVP."""

from .contracts import (
    ARTIFACT_RECORD_SCHEMA,
    BEHAVIOR_SIGNATURE_SCHEMA,
    DUAT_CONWAY_SIMULATION_SCHEMA,
    DUAT_HEALTH_WINDOW_SCHEMA,
    DUAT_V2_INTAKE_SCHEMA,
    EPOCH_MODEL_SCHEMA,
    LOCAL_SOURCE_INTAKE_SCHEMA,
    OBSERVATION_EVENT_SCHEMA,
    ROUTE_DECISION_SCHEMA,
    SCENARIO_REPORT_SCHEMA,
    SOURCE_SNAPSHOT_SCHEMA,
)
from .behavior import analyze_behavior_signature
from .duat_sim import run_duat_conway_simulation
from .duat_v2_intake import build_duat_v2_intake
from .router import RequestFeatures, decide_route
from .source_registry import build_local_source_intake
from .model import build_epoch_model, build_scenario_report, run_backtest
from .snapshot import create_snapshot_from_fixture

__all__ = [
    "ARTIFACT_RECORD_SCHEMA",
    "BEHAVIOR_SIGNATURE_SCHEMA",
    "DUAT_CONWAY_SIMULATION_SCHEMA",
    "DUAT_HEALTH_WINDOW_SCHEMA",
    "DUAT_V2_INTAKE_SCHEMA",
    "EPOCH_MODEL_SCHEMA",
    "LOCAL_SOURCE_INTAKE_SCHEMA",
    "OBSERVATION_EVENT_SCHEMA",
    "ROUTE_DECISION_SCHEMA",
    "SCENARIO_REPORT_SCHEMA",
    "SOURCE_SNAPSHOT_SCHEMA",
    "RequestFeatures",
    "analyze_behavior_signature",
    "build_epoch_model",
    "build_local_source_intake",
    "build_duat_v2_intake",
    "build_scenario_report",
    "create_snapshot_from_fixture",
    "decide_route",
    "run_backtest",
    "run_duat_conway_simulation",
]
