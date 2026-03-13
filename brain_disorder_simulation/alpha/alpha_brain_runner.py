"""Alpha vNext - Runner (MVP).

Baseline UnifiedDisorderSimulator를 '환경(plant)'으로 감싸서,
Controller가 매 스텝마다 액션을 결정하고, 로그를 남긴다.

주의: MVP에서는 baseline 코드의 내부 루프 파라미터를 직접 수정하지 않는다.
대신 action을 '의사결정 로그/실험 설계'로 먼저 구축한다.

다음 단계에서 plant에 적용 가능한 안전한 hook(계수 적용)을 추가한다.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional

import numpy as np

from .controller_spec import Action, ControlMode, Observation
from .self_regulation_controller import SelfRegulationController


@dataclass
class AlphaStepLog:
    t: float
    mode: str
    observation: Dict[str, Any]
    action: Dict[str, Any]


class AlphaBrainRunner:
    def __init__(self, plant, controller: SelfRegulationController):
        self.plant = plant
        self.controller = controller
        self.logs: List[AlphaStepLog] = []

    def _extract_observation(self, results: Dict[str, Any]) -> Observation:
        loop_analysis = results.get('loop_analysis', {}) or {}
        active_loops = loop_analysis.get('active_loops', {}) or {}
        loops = {k: float(v.get('mean_strength', 0.0)) for k, v in active_loops.items()}

        # Evaluation layer outputs are printed by explain_patterns in baseline;
        # for MVP, we only keep what is already in results.
        return Observation(
            energy=results.get('mean_energy') or results.get('final_energy'),
            arousal=results.get('mean_arousal'),
            attention=results.get('mean_attention'),
            impulsivity=results.get('mean_impulsivity'),
            loops=loops,
            H=None, S=None, F=None, M=None, X=None, P=None, Emerge=None,
        )

    def run_episode_adhd(self, duration: float = 30.0, task_importance: float = 0.6) -> Dict[str, Any]:
        # Run plant once (baseline). Next iteration will step-by-step control.
        results = self.plant.simulate_adhd(duration=duration, task_importance=task_importance)

        obs = self._extract_observation(results)
        # align known loops
        self.controller.known_loops = tuple(obs.loops.keys()) if obs.loops else self.controller.known_loops

        action, mode = self.controller.step(obs)
        self.logs.append(
            AlphaStepLog(
                t=float(duration),
                mode=str(mode),
                observation={
                    'attention': obs.attention,
                    'impulsivity': obs.impulsivity,
                    'loops': obs.loops,
                },
                action={
                    'suppress': action.suppress,
                    'amplify': action.amplify,
                    'control_gain': action.control_gain,
                    'recovery_gain': action.recovery_gain,
                    'noise_sigma': action.noise_sigma,
                    'noise_target': action.noise_target,
                },
            )
        )

        return {
            'baseline_results': results,
            'controller_mode': str(mode),
            'controller_action': action,
            'logs': self.logs,
        }
