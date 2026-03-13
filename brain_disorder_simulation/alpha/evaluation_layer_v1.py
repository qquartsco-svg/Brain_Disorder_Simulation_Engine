"""Alpha vNext - Evaluation Layer v1 (implementation).

Implements docs/alpha/EVALUATION_LAYER_v1.0.md.
All scores are in [0,1] with higher=better.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Optional

import numpy as np


def clip01(x: float) -> float:
    return float(np.clip(x, 0.0, 1.0))


@dataclass
class EvalParams:
    # targets/tolerances
    E_star: float = 0.85
    E_tol: float = 0.25
    A_star: float = 0.50
    A_tol: float = 0.25

    # weights (sum=1 constraints are assumed; not enforced here)
    alpha_E: float = 0.34
    alpha_A: float = 0.33
    alpha_L: float = 0.33

    beta_att: float = 0.34
    beta_imp: float = 0.33
    beta_rpe: float = 0.33

    # flexibility set weights (sum=1 across K)
    gamma: Optional[Dict[str, float]] = None

    # motivation weights (sum=1)
    delta_mc: float = 0.5
    delta_ec: float = 0.5

    # stress weights
    eta: Optional[Dict[str, float]] = None
    eta_delta: float = 0.0

    # emergence
    lam: float = 0.7
    tau: float = 0.6
    X_min: float = 0.2


@dataclass
class EvalScores:
    H: float
    S: float
    F: float
    M: float
    X: float
    P: float
    Emerge: float


DEFAULT_STICKY_SET = (
    'intrusive_memory',
    'avoidance',
    'negative_bias',
    'hyperarousal',
    'control_failure',
)


def evaluate(
    *,
    energy: Optional[float],
    arousal: Optional[float],
    attention: Optional[float],
    impulsivity: Optional[float],
    loops: Dict[str, float],
    d_energy: float = 0.0,
    d_arousal: float = 0.0,
    d_attention: float = 0.0,
    params: EvalParams = EvalParams(),
) -> EvalScores:
    # defaults
    energy = float(energy) if energy is not None else params.E_star
    arousal = float(arousal) if arousal is not None else params.A_star
    attention = float(attention) if attention is not None else 0.5
    impulsivity = float(impulsivity) if impulsivity is not None else 0.5

    # H_E, H_A
    H_E = clip01(1.0 - abs(energy - params.E_star) / max(1e-6, params.E_tol))
    H_A = clip01(1.0 - abs(arousal - params.A_star) / max(1e-6, params.A_tol))

    # H_L with closed normalization L_max=sum w_i
    w = params.eta or {k: 1.0 for k in loops.keys()}
    w_sum = float(sum(w.values())) if w else 1.0
    weighted = 0.0
    for k, s in loops.items():
        weighted += float(w.get(k, 0.0)) * float(s)
    H_L = clip01(1.0 - (weighted / max(1e-6, w_sum)))

    H = clip01(params.alpha_E * H_E + params.alpha_A * H_A + params.alpha_L * H_L)

    # S
    rpe_strength = float(loops.get('reward_prediction_error', loops.get('rpe', 0.0)))
    S = clip01(params.beta_att * attention + params.beta_imp * (1.0 - impulsivity) + params.beta_rpe * (1.0 - rpe_strength))

    # F
    gamma = params.gamma
    if gamma is None:
        gamma = {k: 1.0 / len(DEFAULT_STICKY_SET) for k in DEFAULT_STICKY_SET}
    sticky_sum = 0.0
    for k, g in gamma.items():
        sticky_sum += float(g) * float(loops.get(k, 0.0))
    F = clip01(1.0 - sticky_sum)

    # M
    mc = float(loops.get('motivation_collapse', 0.0))
    ec = float(loops.get('energy_collapse', 0.0))
    M = clip01(1.0 - params.delta_mc * mc - params.delta_ec * ec)

    # X
    eta = params.eta or {k: 1.0 / max(1, len(loops)) for k in loops.keys()}
    stress = 0.0
    for k, s in loops.items():
        stress += float(eta.get(k, 0.0)) * float(s)
    delta_term = clip01(abs(d_energy) + abs(d_arousal) + abs(d_attention))
    X = clip01(stress + params.eta_delta * delta_term)

    # P
    P = clip01((H + S + F + M) / 4.0)

    # Emerge
    core = clip01((P - params.lam * X - params.tau) / max(1e-6, 1.0 - params.tau))
    gate = 1.0 if X >= params.X_min else 0.0
    Emerge = clip01(core * gate)

    return EvalScores(H=H, S=S, F=F, M=M, X=X, P=P, Emerge=Emerge)
