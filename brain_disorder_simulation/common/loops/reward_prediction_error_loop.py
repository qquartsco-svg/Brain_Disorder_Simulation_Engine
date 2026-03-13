""" 
보상 예측 오차 루프 (Reward Prediction Error Loop)

ADHD의 핵심: 기대한 보상과 실제 보상의 불일치(RPE)가 커지면서
충동적 선택/강화 학습이 불안정해지는 메커니즘을 루프 단위로 추상화.

핵심 메커니즘(폐루프):
예측 오차↑ → 보상 신호 불안정/학습 왜곡 → 즉각 보상 선호↑ → 오차 패턴 강화

Author: GNJz (Qquarts)
Version: 1.0.0
"""

import numpy as np
from typing import Dict, Optional
from dataclasses import dataclass

from .base_loop import BaseLoop, LoopState, LoopParameters


@dataclass
class RewardPredictionErrorLoopState(LoopState):
    """RPE 루프 상태"""
    mean_abs_rpe: float = 0.0      # 최근 |RPE| 평균
    positive_rpe: float = 0.0      # 최근 양의 RPE 경향
    negative_rpe: float = 0.0      # 최근 음의 RPE 경향
    volatility: float = 0.0        # RPE 변동성
    impulsivity_bias: float = 0.0  # 즉각 보상 편향 (0.0 ~ 1.0)


class RewardPredictionErrorLoop(BaseLoop):
    """보상 예측 오차 루프"""

    def __init__(
        self,
        initial_rpe_instability: float = 0.0,
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
            name="RewardPredictionErrorLoop",
            parameters=parameters,
            rng=rng,
        )

        self.rpe_state = RewardPredictionErrorLoopState()
        self._ewma_abs = 0.0
        self._ewma_var = 0.0
        self._last_rpe = 0.0

        if initial_rpe_instability > 0:
            self.state.loop_strength = float(np.clip(initial_rpe_instability, 0.0, 1.0))
            self._update_from_strength(self.state.loop_strength)

    def _update_from_strength(self, strength: float):
        strength = float(np.clip(strength, 0.0, 1.0))
        # 강도가 높을수록 impulsivity_bias 증가
        self.rpe_state.impulsivity_bias = float(np.clip(0.2 + 0.8 * strength, 0.0, 1.0))

    def observe(self, expected_reward: float, received_reward: float, dt: float = 0.1) -> Dict:
        """RPE 관측 및 루프 트리거"""
        expected_reward = float(expected_reward)
        received_reward = float(received_reward)

        rpe = received_reward - expected_reward
        abs_rpe = abs(rpe)

        self._ewma_abs = 0.95 * self._ewma_abs + 0.05 * abs_rpe
        # 변동성(단순): rpe 변화량의 ewma
        dr = abs(rpe - self._last_rpe)
        self._ewma_var = 0.9 * self._ewma_var + 0.1 * dr
        self._last_rpe = rpe

        # 누적 경향
        if rpe >= 0:
            self.rpe_state.positive_rpe = float(np.clip(0.9 * self.rpe_state.positive_rpe + 0.1 * rpe, 0.0, 1.0))
        else:
            self.rpe_state.negative_rpe = float(np.clip(0.9 * self.rpe_state.negative_rpe + 0.1 * (-rpe), 0.0, 1.0))

        self.rpe_state.mean_abs_rpe = float(np.clip(self._ewma_abs, 0.0, 1.0))
        self.rpe_state.volatility = float(np.clip(self._ewma_var, 0.0, 1.0))

        # 트리거 강도: abs_rpe와 변동성 기반
        intensity = float(np.clip(0.6 * abs_rpe + 0.4 * self.rpe_state.volatility, 0.0, 1.0))
        if intensity > 0.15:
            self.trigger(intensity=intensity, context={"rpe": rpe, "abs_rpe": abs_rpe})

        super().update(dt=dt)
        self._update_from_strength(self.state.loop_strength)

        return {
            "rpe": rpe,
            "mean_abs_rpe": self.rpe_state.mean_abs_rpe,
            "volatility": self.rpe_state.volatility,
            "loop_strength": self.state.loop_strength,
            "impulsivity_bias": self.rpe_state.impulsivity_bias,
        }

    def get_modifiers(self) -> Dict[str, float]:
        s = self.state.loop_strength
        # loop_strength가 높을수록 discount_rate↑, impulse_threshold↓
        return {
            "discount_multiplier": float(1.0 + 1.0 * s),
            "threshold_shift": float(-0.2 * s),
            "impulse_bias": float(self.rpe_state.impulsivity_bias),
        }

    def _trigger_condition(self, context: Optional[Dict] = None) -> bool:
        if context is None:
            return False
        return abs(float(context.get("abs_rpe", 0.0))) > 0.3

    def _update_dynamics(self, dt: float, context: Optional[Dict] = None):
        _ = dt
        _ = context

    def _apply_loop_effect(self, intensity: float, context: Optional[Dict] = None) -> Dict:
        _ = context
        # 효과: 변동성이 커지고 편향 증가
        self.rpe_state.volatility = float(np.clip(self.rpe_state.volatility + 0.05 * float(intensity), 0.0, 1.0))
        self._update_from_strength(self.state.loop_strength)
        return {
            "volatility": self.rpe_state.volatility,
            "impulsivity_bias": self.rpe_state.impulsivity_bias,
        }

    def _calculate_score(self) -> float:
        score = (
            self.rpe_state.mean_abs_rpe * 0.5
            + self.rpe_state.volatility * 0.3
            + self.rpe_state.impulsivity_bias * 0.2
        )
        return float(np.clip(score, 0.0, 1.0))

    def _analyze_patterns(self) -> Dict:
        return {
            "mean_abs_rpe": self.rpe_state.mean_abs_rpe,
            "volatility": self.rpe_state.volatility,
            "impulsivity_bias": self.rpe_state.impulsivity_bias,
            "loop_strength": self.state.loop_strength,
            "rpe_instability": self._calculate_score(),
        }

    def get_state(self) -> RewardPredictionErrorLoopState:
        return self.rpe_state
