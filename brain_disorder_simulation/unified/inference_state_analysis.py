"""Inference State Analysis

질환(루프) 시뮬레이션 결과를 '추론 상태(Inference State)' 관점에서 해석.

핵심 아이디어:
- NormativeData (정상 대조군) 기반 Z-score로 '정상 대비 이탈/회복'을 정량화
- 루프 강도(버그/붕괴) 대비 성능(지표)이 좋아지는 구간을 '창발/보상(emergence/compensation)'으로 탐지

⚠️ 연구/교육용 분석이며 의학적 진단이 아님.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Optional, Tuple

import numpy as np

from ..medical.normative_data import NormativeData, Gender


@dataclass
class InferenceAxes:
    homeostasis: float
    signal_to_noise: float
    flexibility: float
    motivation: float


def _clip01(x: float) -> float:
    return float(np.clip(x, 0.0, 1.0))


def compute_normative_zscores(
    results: Dict[str, Any],
    age: int = 18,
    gender: Gender = Gender.MALE,
    normative: Optional[NormativeData] = None,
) -> Dict[str, Any]:
    """결과 dict에서 가능한 범위 내에서 normative z-score를 계산."""
    normative = normative or NormativeData()

    out: Dict[str, Any] = {
        'age': age,
        'gender': gender.value,
        'zscores': {},
        'percentiles': {},
    }

    # ADHD 지표
    if 'mean_attention' in results:
        z = normative.calculate_z_score(results['mean_attention'], 'attention', age, gender)
        out['zscores']['attention'] = z
        out['percentiles']['attention'] = normative._z_to_percentile(z)

    if 'mean_impulsivity' in results:
        # impulsivity는 낮을수록 좋지만, NormativeData는 impulsivity 자체로 정의됨
        z = normative.calculate_z_score(results['mean_impulsivity'], 'impulsivity', age, gender)
        out['zscores']['impulsivity'] = z
        out['percentiles']['impulsivity'] = normative._z_to_percentile(z)

    if 'mean_hyperactivity' in results:
        z = normative.calculate_z_score(results['mean_hyperactivity'], 'hyperactivity', age, gender)
        out['zscores']['hyperactivity'] = z
        out['percentiles']['hyperactivity'] = normative._z_to_percentile(z)

    return out


def compute_optimized_inference_axes(
    results: Dict[str, Any],
    loop_analysis: Optional[Dict[str, Any]] = None,
) -> InferenceAxes:
    """프로젝트 내 엔진/루프 결과 키에 맞춘 4축 점수(0~1).

    - homeostasis: 에너지/각성/루프 과열 억제
    - signal_to_noise: attention 높고 impulsivity 낮음
    - flexibility: intrusive/avoidance/negative_bias 등 고착 루프 낮음
    - motivation: motivation collapse 낮고 goal-directed가 유지되는 방향

    (현재 결과 dict가 질환별로 키가 다르므로, 가능한 키만으로 근사)
    """
    loop_analysis = loop_analysis or results.get('loop_analysis', {}) or {}
    active_loops = loop_analysis.get('active_loops', {}) or {}

    # 기본값
    homeostasis = 0.5
    snr = 0.5
    flexibility = 0.5
    motivation = 0.5

    # ADHD 기반
    if 'mean_attention' in results:
        snr = _clip01(0.2 + 0.8 * float(results['mean_attention']))
    if 'mean_impulsivity' in results:
        snr = _clip01(snr * (1.0 - 0.6 * float(results['mean_impulsivity'])))

    # PTSD 기반 고착 루프
    sticky = 0.0
    for k in ('intrusive_memory', 'avoidance', 'negative_bias', 'hyperarousal'):
        if k in active_loops:
            sticky += float(active_loops[k].get('mean_strength', 0.0))
    flexibility = _clip01(1.0 - 0.7 * sticky)

    # Depression 기반
    dep_sticky = 0.0
    for k in ('energy_collapse', 'motivation_collapse', 'control_failure', 'negative_bias'):
        if k in active_loops:
            dep_sticky += float(active_loops[k].get('mean_strength', 0.0))
    motivation = _clip01(1.0 - 0.6 * dep_sticky)

    # homeostasis: 전체 루프 과열이 낮을수록 좋다
    total = 0.0
    for v in active_loops.values():
        total += float(v.get('mean_strength', 0.0))
    homeostasis = _clip01(1.0 - min(1.0, total / 3.0))

    return InferenceAxes(
        homeostasis=homeostasis,
        signal_to_noise=snr,
        flexibility=flexibility,
        motivation=motivation,
    )


def compute_emergence_index(
    results: Dict[str, Any],
    loop_analysis: Optional[Dict[str, Any]] = None,
) -> Dict[str, float]:
    """버그(루프) 강도 대비 성능이 유지/상승되는 패턴을 '창발(보상)'로 근사.

    단순 정의(연구용):
    - stress: 주요 루프들의 mean_strength 평균
    - performance: (attention↑, impulsivity↓, flexibility↑, motivation↑) 합성
    - emergence = performance - stress (0~1로 클리핑)

    즉, 루프가 높은데도 성능이 높으면 '보상적 창발' 가능성이 높다고 본다.
    """
    loop_analysis = loop_analysis or results.get('loop_analysis', {}) or {}
    active_loops = loop_analysis.get('active_loops', {}) or {}

    strengths = [float(v.get('mean_strength', 0.0)) for v in active_loops.values()]
    stress = float(np.mean(strengths)) if strengths else 0.0

    axes = compute_optimized_inference_axes(results, loop_analysis)
    performance = float(np.mean([axes.homeostasis, axes.signal_to_noise, axes.flexibility, axes.motivation]))

    emergence = _clip01(0.5 + 0.8 * (performance - stress))

    return {
        'stress_index': _clip01(stress),
        'performance_index': _clip01(performance),
        'emergence_index': emergence,
    }
