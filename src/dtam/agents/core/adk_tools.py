"""ADK-facing tool wrappers around deterministic services."""

from __future__ import annotations

import json
from typing import Any

from .enums import OperatingMode
from .models import DigitalTwinObservation, ProposedAction


def assess_digital_twin(observation_json: str, mode: str = "") -> dict[str, Any]:
    """Run the full digital-twin assessment pipeline.

    Args:
        observation_json: JSON string for DigitalTwinObservation.
        mode: Optional override: observe|recommend. Empty keeps observation mode.

    Returns:
        Serialized DigitalTwinAssessment dictionary.
    """
    from .orchestrator import run_assessment

    payload = json.loads(observation_json)
    obs = DigitalTwinObservation.model_validate(payload)
    op_mode = OperatingMode(mode) if mode else None
    result = run_assessment(obs, mode=op_mode)
    return result.model_dump(mode="json")


def assess_from_twin_scanner(
    scanner_id: str = "simulated_scanner",
    mode: str = "observe",
    predict_horizon_s: float = 0.0,
) -> dict[str, Any]:
    """Read the DTAM twin (adapter → SystemState) and run assessment.

    Bridges `estimate_twin_state` into DigitalTwinObservation without changing
    twin physics. Prefer this when live scanner/sim data is available.
    """
    from dtam.tools.state_estimation import estimate_twin_state

    from .orchestrator import run_assessment
    from .twin_bridge import observation_from_twin_tool_payload

    twin_payload = estimate_twin_state(
        scanner_id=scanner_id,
        predict_horizon_s=predict_horizon_s,
    )
    if not twin_payload.get("ok", False):
        return twin_payload
    obs = observation_from_twin_tool_payload(twin_payload)
    if mode:
        obs = obs.model_copy(update={"operating_mode": OperatingMode(mode)})
    result = run_assessment(obs)
    return {
        "ok": True,
        "tool": "assess_from_twin_scanner",
        "data": {
            "twin": twin_payload.get("data"),
            "assessment": result.model_dump(mode="json"),
        },
    }


def run_thermal_analysis(observation_json: str) -> dict[str, Any]:
    """Analyze thermal domain of an observation JSON string."""
    from ..thermal_agent.service import analyze_thermal

    obs = DigitalTwinObservation.model_validate(json.loads(observation_json))
    return analyze_thermal(obs).model_dump(mode="json")


def run_magnet_analysis(observation_json: str) -> dict[str, Any]:
    """Analyze magnet/B0 domain of an observation JSON string."""
    from ..magnet_agent.service import analyze_magnet

    obs = DigitalTwinObservation.model_validate(json.loads(observation_json))
    return analyze_magnet(obs).model_dump(mode="json")


def run_emi_analysis(observation_json: str) -> dict[str, Any]:
    """Analyze EMI domain of an observation JSON string."""
    from ..emi_agent.service import analyze_emi

    obs = DigitalTwinObservation.model_validate(json.loads(observation_json))
    return analyze_emi(obs).model_dump(mode="json")


def run_rf_analysis(observation_json: str) -> dict[str, Any]:
    """Analyze RF domain of an observation JSON string."""
    from ..rf_agent.service import analyze_rf

    obs = DigitalTwinObservation.model_validate(json.loads(observation_json))
    return analyze_rf(obs).model_dump(mode="json")


def run_motion_analysis(observation_json: str) -> dict[str, Any]:
    """Analyze motion domain of an observation JSON string."""
    from ..motion_tracking.service import analyze_motion

    obs = DigitalTwinObservation.model_validate(json.loads(observation_json))
    return analyze_motion(obs).model_dump(mode="json")


def run_safety_validation(actions_json: str, mode: str = "recommend") -> dict[str, Any]:
    """Validate proposed actions with deterministic safety policy.

    Args:
        actions_json: JSON list of ProposedAction objects.
        mode: Operating mode string (observe|recommend|act).
    """
    from ..safety_agent.service import evaluate_actions

    actions = [ProposedAction.model_validate(a) for a in json.loads(actions_json)]
    decisions, assessment = evaluate_actions(actions, mode=OperatingMode(mode))
    return {
        "decisions": [d.model_dump(mode="json") for d in decisions],
        "assessment": assessment.model_dump(mode="json"),
    }
