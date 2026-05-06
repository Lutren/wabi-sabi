"""Stable contract names for GEODIA Social Observatory."""

SOURCE_SNAPSHOT_SCHEMA = "claudio.social_source_snapshot.v1"
EPOCH_MODEL_SCHEMA = "claudio.social_epoch_model.v1"
SCENARIO_REPORT_SCHEMA = "claudio.social_scenario_report.v1"
LOCAL_SOURCE_INTAKE_SCHEMA = "motor.local_source_intake.v1"
OBSERVATION_EVENT_SCHEMA = "motor.observation_event.v1"
ARTIFACT_RECORD_SCHEMA = "motor.artifact_record.v1"
ROUTE_DECISION_SCHEMA = "motor.route_decision.v1"
BEHAVIOR_SIGNATURE_SCHEMA = "motor.behavior_signature.v1"
DUAT_HEALTH_WINDOW_SCHEMA = "motor.duat_health_window.v1"
DUAT_CONWAY_SIMULATION_SCHEMA = "motor.duat_conway_simulation.v1"
DUAT_V2_INTAKE_SCHEMA = "motor.duat_v2_intake.v1"

CLASSIFICATIONS = ("CERTEZA", "INFERENCIA", "INCOGNITA")


def claim(classification: str, statement: str, evidence: list[dict[str, str]]) -> dict[str, object]:
    if classification not in CLASSIFICATIONS:
        raise ValueError(f"invalid classification: {classification}")
    return {
        "classification": classification,
        "statement": statement,
        "evidence": evidence,
    }
