"""Alpha vNext - Controlled ADHD episode (step-by-step MVP).

This runs a lightweight ADHD loop similar to UnifiedDisorderSimulator.simulate_adhd,
but allows controller action to perturb loop strengths in a safe, bounded way.

Baseline code is not modified; this is a separate experiment harness.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Tuple

import numpy as np

from ..disorders.adhd.adhd_engines import AttentionControlEngine, ImpulseControlEngine, HyperactivityEngine
from ..utils.reproducibility import ReproducibleRNG

from .controller_spec import Observation
from .evaluation_layer_v1 import EvalParams, evaluate
from .self_regulation_controller import SelfRegulationController


@dataclass
class ControlledStep:
    t: float
    mode: str
    obs: Dict[str, Any]
    act: Dict[str, Any]


def _apply_action_to_loop_strength(loop_strength: float, suppress: float, amplify: float, noise: float) -> float:
    # bounded, smooth perturbation
    x = float(loop_strength)
    x = x * (1.0 - 0.5 * float(suppress))
    x = x + 0.15 * float(amplify)
    x = x + float(noise)
    return float(np.clip(x, 0.0, 1.0))


def run_controlled_adhd_episode(
    *,
    duration: float = 30.0,
    task_importance: float = 0.6,
    seed: int = 42,
    controller: SelfRegulationController,
    eval_params: EvalParams = EvalParams(),
) -> Dict[str, Any]:
    rng = ReproducibleRNG(seed=seed)

    attention_engine = AttentionControlEngine(rng=rng.get_rng('adhd_attention'))
    impulse_engine = ImpulseControlEngine(rng=rng.get_rng('adhd_impulse'))
    hyper_engine = HyperactivityEngine(rng=rng.get_rng('adhd_hyperactivity'))

    dt = 0.1
    steps = int(duration / dt)

    # local loop strengths (start from engines' internal loops if present)
    loop_strengths: Dict[str, float] = {
        'attention_instability': float(getattr(attention_engine.loop, 'get_strength', lambda: 0.0)()),
        'reward_prediction_error': float(getattr(impulse_engine.loop, 'get_strength', lambda: 0.0)()),
    }

    controller.known_loops = tuple(loop_strengths.keys())

    logs: List[ControlledStep] = []

    # time-series metrics
    attention_scores: List[float] = []
    impulse_scores: List[float] = []
    hyper_scores: List[float] = []

    current_energy = 70.0

    last_energy = current_energy
    last_arousal = 0.5
    last_attention = 0.5

    for step in range(steps):
        t = step * dt

        # generate task/distractions every 1s
        if step % 10 == 0:
            rdist = rng.get_rng('adhd_distraction')
            distractions = []
            n_dist = int(rdist.integers(0, 4))
            for _ in range(n_dist):
                distractions.append({
                    'intensity': float(rdist.random()),
                    'relevance': float(0.3 + 0.7 * rdist.random()),
                })

            task = {'importance': float(np.clip(task_importance + rdist.normal(0, 0.1), 0.1, 1.0))}

            att = attention_engine.maintain_attention(task=task, distractions=distractions, time_elapsed=t)

            rrew = rng.get_rng('adhd_reward')
            immediate = float(0.2 + 0.8 * rrew.random())
            delayed = float(immediate + 0.1 + 0.8 * rrew.random())
            delay_time = float(5.0 + 55.0 * rrew.random())

            imp = impulse_engine.control_impulse(
                immediate_reward=immediate,
                delayed_reward=delayed,
                delay_time=delay_time,
                goal_context={'strength': float(0.2 + 0.6 * rrew.random())},
            )

            hyper = hyper_engine.calculate_hyperactivity(
                current_energy=current_energy,
                task_demand=task.get('importance', 0.5),
                time_elapsed=t,
            )
            current_energy = float(hyper['next_energy'])

            attention_scores.append(float(att['attention_score']))
            impulse_scores.append(float(imp['impulse_score']))
            hyper_scores.append(float(hyper['hyperactivity_score']))

            # compute deltas for stress
            dE = current_energy - last_energy
            dA = 0.0  # ADHD harness does not simulate arousal yet
            dAtt = float(att['attention_score']) - last_attention

            # evaluate
            scores = evaluate(
                energy=float(np.clip(current_energy / 100.0, 0.0, 1.0)),  # normalize to 0..1 for v1
                arousal=last_arousal,
                attention=float(att['attention_score']),
                impulsivity=float(imp['impulse_score']),
                loops={
                    'attention_instability': loop_strengths['attention_instability'],
                    'reward_prediction_error': loop_strengths['reward_prediction_error'],
                },
                d_energy=dE,
                d_arousal=dA,
                d_attention=dAtt,
                params=eval_params,
            )

            obs = Observation(
                energy=float(np.clip(current_energy / 100.0, 0.0, 1.0)),
                arousal=last_arousal,
                attention=float(att['attention_score']),
                impulsivity=float(imp['impulse_score']),
                loops=dict(loop_strengths),
                H=scores.H, S=scores.S, F=scores.F, M=scores.M, X=scores.X, P=scores.P, Emerge=scores.Emerge,
            )

            action, mode = controller.step(obs)

            # apply action to loop strengths (safe bounded)
            noise_val = 0.0
            if action.noise_sigma and action.noise_target:
                noise_val = float(np.random.default_rng(seed + step).normal(0.0, action.noise_sigma))

            for k in loop_strengths.keys():
                sup = float(action.suppress.get(k, 0.0))
                amp = float(action.amplify.get(k, 0.0))
                n = noise_val if action.noise_target == k else 0.0
                loop_strengths[k] = _apply_action_to_loop_strength(loop_strengths[k], sup, amp, n)

            logs.append(
                ControlledStep(
                    t=float(t),
                    mode=str(mode),
                    obs={
                        'H': scores.H,
                        'S': scores.S,
                        'F': scores.F,
                        'M': scores.M,
                        'X': scores.X,
                        'P': scores.P,
                        'Emerge': scores.Emerge,
                        'attention': float(att['attention_score']),
                        'impulsivity': float(imp['impulse_score']),
                        'energy': float(current_energy / 100.0),
                        'loops': dict(loop_strengths),
                    },
                    act={
                        'mode': str(mode),
                        'suppress': dict(action.suppress),
                        'amplify': dict(action.amplify),
                        'noise_sigma': action.noise_sigma,
                        'noise_target': action.noise_target,
                    },
                )
            )

            last_energy = current_energy
            last_attention = float(att['attention_score'])

    results = {
        'mean_attention': float(np.mean(attention_scores)) if attention_scores else 0.0,
        'mean_impulsivity': float(np.mean(impulse_scores)) if impulse_scores else 0.0,
        'mean_hyperactivity': float(np.mean(hyper_scores)) if hyper_scores else 0.0,
    }

    return {
        'summary': results,
        'final_loop_strengths': loop_strengths,
        'steps': logs,
    }
