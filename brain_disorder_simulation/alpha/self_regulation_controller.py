"""Alpha vNext - SelfRegulationController (MVP state machine).

- Plant: existing Disorder/Unified simulator
- Alpha layer: controller decides suppress/amplify/noise under guardrails.

MVP policy: rule-based state machine.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Tuple

import numpy as np

from .controller_spec import Action, ControlMode, Guardrails, Observation, TransitionThresholds


@dataclass
class ControllerState:
    mode: ControlMode = ControlMode.STABILIZE
    explore_steps: int = 0
    recovery_steps: int = 0
    best_emerge: float = 0.0
    best_action: Action = None  # type: ignore


class SelfRegulationController:
    def __init__(
        self,
        guardrails: Guardrails = Guardrails(),
        thresholds: TransitionThresholds = TransitionThresholds(),
        known_loops: Tuple[str, ...] = (),
        seed: int = 0,
    ):
        self.guardrails = guardrails
        self.thresholds = thresholds
        self.rng = np.random.default_rng(seed)
        self.state = ControllerState(mode=ControlMode.STABILIZE)
        self.known_loops = tuple(known_loops)

    def _blank_action(self) -> Action:
        return Action(
            suppress={k: 0.0 for k in self.known_loops},
            amplify={k: 0.0 for k in self.known_loops},
            control_gain=1.0,
            recovery_gain=1.0,
            noise_sigma=0.0,
            noise_target=None,
        )

    def _guardrail_violation(self, obs: Observation) -> bool:
        if obs.energy is not None and obs.energy < self.guardrails.energy_min:
            return True
        # cap check (if provided)
        if obs.loops:
            for v in obs.loops.values():
                if v is not None and v > self.guardrails.loop_cap:
                    return True
        return False

    def step(self, obs: Observation) -> Tuple[Action, ControlMode]:
        """Compute action & next mode based on observation."""

        # emergency reset
        if self._guardrail_violation(obs) or (obs.H is not None and obs.H < self.thresholds.H_critical) or (obs.X is not None and obs.X > self.thresholds.X_critical):
            self.state.mode = ControlMode.RESET

        if self.state.mode == ControlMode.RESET:
            act = self._blank_action()
            # strong suppress, strong recovery
            for k in act.suppress:
                act.suppress[k] = 1.0
                act.amplify[k] = 0.0
            act.control_gain = 1.2
            act.recovery_gain = 1.5
            act.noise_sigma = 0.0
            self.state.explore_steps = 0
            self.state.recovery_steps = 0
            # after reset, go stabilize
            self.state.mode = ControlMode.STABILIZE
            return act, ControlMode.RESET

        # mode switching logic
        if self.state.mode == ControlMode.STABILIZE:
            # enter explore only if baseline healthy enough
            if (obs.P is not None and obs.X is not None and obs.energy is not None and
                obs.P >= self.thresholds.P_min and obs.X <= self.thresholds.X_max and obs.energy >= self.guardrails.energy_min):
                self.state.mode = ControlMode.EXPLORE
                self.state.explore_steps = 0

        elif self.state.mode == ControlMode.EXPLORE:
            self.state.explore_steps += 1
            # record best emergence
            if obs.Emerge is not None and obs.Emerge > self.state.best_emerge:
                self.state.best_emerge = float(obs.Emerge)
            # stop explore conditions
            if (obs.Emerge is not None and obs.Emerge >= self.thresholds.Emerge_good) or self.state.explore_steps >= self.guardrails.explore_max_steps:
                self.state.mode = ControlMode.EXPLOIT
                self.state.recovery_steps = 0

        elif self.state.mode == ControlMode.EXPLOIT:
            self.state.recovery_steps += 1
            # if stabilized enough, return stabilize
            if obs.H is not None and obs.H >= self.guardrails.homeostasis_safe:
                self.state.mode = ControlMode.STABILIZE
            # if cannot recover in time, reset
            if self.state.recovery_steps >= self.guardrails.recovery_deadline_steps:
                self.state.mode = ControlMode.RESET

        # action policy per mode
        act = self._blank_action()
        mode = self.state.mode

        if mode == ControlMode.STABILIZE:
            # suppress top stressed loops
            if obs.loops:
                top = sorted(obs.loops.items(), key=lambda kv: kv[1], reverse=True)[:2]
                for k, _v in top:
                    if k in act.suppress:
                        act.suppress[k] = 0.7
            act.recovery_gain = 1.2
            act.control_gain = 1.1

        elif mode == ControlMode.EXPLORE:
            # controlled collapse: pick 1-2 loops to mildly amplify + inject small noise
            if obs.loops:
                candidates = list(obs.loops.keys())
                if candidates:
                    pick = self.rng.choice(candidates)
                    if pick in act.amplify:
                        act.amplify[pick] = 0.3
                    act.noise_sigma = 0.03
                    act.noise_target = pick
            # relax control a bit
            act.control_gain = 0.9

        elif mode == ControlMode.EXPLOIT:
            # reduce noise, keep mild suppression, prioritize recovery
            if obs.loops:
                top = sorted(obs.loops.items(), key=lambda kv: kv[1], reverse=True)[:2]
                for k, _v in top:
                    if k in act.suppress:
                        act.suppress[k] = 0.5
            act.noise_sigma = 0.0
            act.recovery_gain = 1.3
            act.control_gain = 1.1

        return act, mode
