"""Alpha vNext - Controller spec types.

Baseline(연구/의료용 시뮬레이터)은 수정하지 않고, Alpha 레이어에서만 사용.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Dict, Optional


class ControlMode(str, Enum):
    STABILIZE = "stabilize"
    EXPLORE = "explore"
    EXPLOIT = "exploit"
    RESET = "reset"


@dataclass
class Observation:
    # core state
    energy: Optional[float] = None
    arousal: Optional[float] = None
    attention: Optional[float] = None
    impulsivity: Optional[float] = None

    # loop strengths (0..1)
    loops: Dict[str, float] = None  # type: ignore

    # evaluation layer scores (0..1)
    H: Optional[float] = None
    S: Optional[float] = None
    F: Optional[float] = None
    M: Optional[float] = None
    X: Optional[float] = None
    P: Optional[float] = None
    Emerge: Optional[float] = None


@dataclass
class Action:
    # suppress/amplify coefficients per loop (0..1)
    suppress: Dict[str, float]
    amplify: Dict[str, float]

    # optional global gains
    control_gain: float = 1.0
    recovery_gain: float = 1.0

    # optional noise injection
    noise_sigma: float = 0.0
    noise_target: Optional[str] = None


@dataclass
class Guardrails:
    energy_min: float = 0.3
    loop_cap: float = 0.9
    explore_max_steps: int = 10
    recovery_deadline_steps: int = 20
    homeostasis_safe: float = 0.7


@dataclass
class TransitionThresholds:
    # explore entry
    P_min: float = 0.6
    X_max: float = 0.4
    X_min_for_emerge: float = 0.2

    # stabilize trigger
    H_critical: float = 0.4
    X_critical: float = 0.8

    # exploit
    Emerge_good: float = 0.7
