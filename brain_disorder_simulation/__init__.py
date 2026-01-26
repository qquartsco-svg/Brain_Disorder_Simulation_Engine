"""
Brain Disorder Simulation Engine

뇌 질환 시뮬레이션 통합 패키지
목적: "왜 이런 상황이 발생할 수 있는가?" 원인 분석

⚠️ 주의: 이 패키지는 치료 도구가 아닙니다.
- 진단 도구 아님
- 치료 솔루션 제시 아님
- 패턴 관측 및 메커니즘 분석 목적

Author: GNJz (Qquarts)
Version: 1.0.0
"""

__version__ = "1.0.0"
__author__ = "GNJz (Qquarts)"

# 공통 엔진
from .common.negative_bias_engine import NegativeBiasEngine
from .common.cognitive_control_engine import CognitiveControlEngine
from .common.energy_depletion_engine import EnergyDepletionEngine

# 통합 시뮬레이터
from .unified.unified_simulator import UnifiedDisorderSimulator

__all__ = [
    '__version__',
    '__author__',
    
    # 공통 엔진
    'NegativeBiasEngine',
    'CognitiveControlEngine',
    'EnergyDepletionEngine',
    
    # 통합 시뮬레이터
    'UnifiedDisorderSimulator',
]

