"""
공통 코어 모듈

공통 엔진 및 통합 시뮬레이터
의료 연구용과 엔지니어링 관점 모두에서 사용

Author: GNJz (Qquarts)
Version: 1.0.0
"""

__version__ = "1.0.0"
__author__ = "GNJz (Qquarts)"

# 공통 엔진은 기존 경로 유지
from ..common.negative_bias_engine import NegativeBiasEngine
from ..common.cognitive_control_engine import CognitiveControlEngine
from ..common.energy_depletion_engine import EnergyDepletionEngine

# 통합 시뮬레이터
from ..unified.unified_simulator import UnifiedDisorderSimulator

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

