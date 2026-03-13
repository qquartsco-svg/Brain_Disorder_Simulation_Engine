""" 
주의 불안정 루프 (Attention Instability Loop)

ADHD의 핵심: 주의가 유지되지 못하고 흔들리는(variability, dropout) 메커니즘을
루프 단위로 추상화한 모듈.

핵심 메커니즘(폐루프):
주의 저하/드롭아웃 → 과제 성과 저하/스트레스↑ → 주의 회복 실패 → 더 잦은 드롭아웃

Author: GNJz (Qquarts)
Version: 1.0.0
"""

import numpy as np
from typing import Dict, Optional
from dataclasses import dataclass

from .base_loop import BaseLoop, LoopState, LoopParameters


@dataclass
class AttentionInstabilityLoopState(LoopState):
    """주의 불안정 루프 상태"""
    attention_level: float = 1.0          # 현재 주의 수준 (0.0 ~ 1.0)
    distraction_sensitivity: float = 1.0  # 분산 민감도 배수 (1.0 ~ 3.0)
    dropout_rate: float = 0.0             # 최근 드롭아웃 비율(0.0 ~ 1.0)
    variability: float = 0.0              # 최근 변동성(0.0 ~ 1.0)
    fatigue: float = 0.0                  # 피로/인지 소진(0.0 ~ 1.0)


class AttentionInstabilityLoop(BaseLoop):
    """주의 불안정 루프"""

    def __init__(
        self,
        initial_instability: float = 0.0,
        parameters: Optional[LoopParameters] = None,
        rng: Optional[np.random.Generator] = None,
    ):
        if parameters is None:
            parameters = LoopParameters(
                loop_gain=0.05,
                loop_decay=0.98,
                loop_threshold=0.3,
                max_strength=1.0,
                min_strength=0.0,
            )

        super().__init__(
            name="AttentionInstabilityLoop",
            parameters=parameters,
            rng=rng,
        )

        self.att_state = AttentionInstabilityLoopState()
        self._ewma_var = 0.0
        self._ewma_dropout = 0.0

        if initial_instability > 0:
            self.state.loop_strength = float(np.clip(initial_instability, 0.0, 1.0))
            self._update_from_strength(self.state.loop_strength)

    def _update_from_strength(self, strength: float):
        strength = float(np.clip(strength, 0.0, 1.0))
        self.att_state.attention_level = float(np.clip(1.0 - 0.7 * strength, 0.0, 1.0))
        self.att_state.distraction_sensitivity = float(1.0 + 2.0 * strength)
        self.att_state.fatigue = float(np.clip(self.att_state.fatigue + 0.05 * strength, 0.0, 1.0))

    def observe(
        self,
        attention_score: float,
        distraction_level: float,
        dt: float = 0.1,
        threshold: float = 0.5,
    ) -> Dict:
        attention_score = float(np.clip(attention_score, 0.0, 1.0))
        distraction_level = float(max(distraction_level, 0.0))

        dropout = 1.0 if attention_score < threshold else 0.0
        self._ewma_dropout = 0.95 * self._ewma_dropout + 0.05 * dropout

        dev = abs(attention_score - self.att_state.attention_level)
        self._ewma_var = 0.9 * self._ewma_var + 0.1 * dev

        self.att_state.dropout_rate = float(np.clip(self._ewma_dropout, 0.0, 1.0))
        self.att_state.variability = float(np.clip(self._ewma_var, 0.0, 1.0))

        intensity = 0.0
        if dropout > 0:
            intensity = max(intensity, 0.6 + 0.4 * min(1.0, distraction_level))
        else:
            intensity = max(intensity, 0.2 * min(1.0, distraction_level))

        if intensity > 0.0:
            self.trigger(
                intensity=float(np.clip(intensity, 0.0, 1.0)),
                context={
                    "attention_score": attention_score,
                    "distraction_level": distraction_level,
                    "dropout": dropout,
                },
            )

        super().update(dt=dt)
        self._update_from_strength(self.state.loop_strength)

        return {
            "loop_strength": self.state.loop_strength,
            "dropout_rate": self.att_state.dropout_rate,
            "variability": self.att_state.variability,
            "distraction_sensitivity": self.att_state.distraction_sensitivity,
        }

    def get_modifiers(self) -> Dict[str, float]:
        s = self.state.loop_strength
        return {
            "decay_multiplier": float(1.0 + 1.5 * s),
            "recovery_multiplier": float(max(0.2, 1.0 - 0.8 * s)),
            "distraction_multiplier": float(1.0 + 2.0 * s),
            "noise_sigma": float(0.01 + 0.05 * s),
        }

    def _trigger_condition(self, context: Optional[Dict] = None) -> bool:
        if context is None:
            return False
        return bool(context.get("dropout", 0) == 1 or context.get("distraction_level", 0.0) > 0.7)

    def _update_dynamics(self, dt: float, context: Optional[Dict] = None):
        _ = dt
        _ = context

    def _apply_loop_effect(self, intensity: float, context: Optional[Dict] = None) -> Dict:
        _ = context
        self.att_state.fatigue = float(np.clip(self.att_state.fatigue + 0.1 * float(intensity), 0.0, 1.0))
        self._update_from_strength(self.state.loop_strength)
        return {
            "attention_level": self.att_state.attention_level,
            "distraction_sensitivity": self.att_state.distraction_sensitivity,
            "fatigue": self.att_state.fatigue,
        }

    def _calculate_score(self) -> float:
        score = (
            self.att_state.dropout_rate * 0.4
            + self.att_state.variability * 0.3
            + self.att_state.fatigue * 0.2
            + self.state.loop_strength * 0.1
        )
        return float(np.clip(score, 0.0, 1.0))

    def _analyze_patterns(self) -> Dict:
        return {
            "dropout_rate": self.att_state.dropout_rate,
            "variability": self.att_state.variability,
            "fatigue": self.att_state.fatigue,
            "loop_strength": self.state.loop_strength,
            "instability_severity": self._calculate_score(),
        }

    def get_state(self) -> AttentionInstabilityLoopState:
        return self.att_state
