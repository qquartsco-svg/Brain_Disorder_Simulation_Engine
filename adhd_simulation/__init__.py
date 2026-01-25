"""
ADHD Simulation Engine

Cookiie Brain Engine 기반 ADHD 전용 시뮬레이션 시스템
"""

__version__ = "1.0.0"
__author__ = "GNJz (Qquarts)"

# 핵심 엔진
from .core.adhd_engines import (
    AttentionControlEngine,
    ImpulseControlEngine,
    HyperactivityEngine
)

from .core.adhd_simulator import ADHDSimulator

# 유틸리티
from .utils.reproducibility import ReproducibleRNG, ExperimentMetadata
from .utils.statistics import StatisticalValidator
from .utils.report_generator import ReportGenerator

# 의료 관련 (선택적)
try:
    from .medical.input_validator import InputValidator
    from .medical.audit_trail import AuditTrail
except ImportError:
    pass

__all__ = [
    # 버전
    '__version__',
    '__author__',
    
    # 핵심 엔진
    'AttentionControlEngine',
    'ImpulseControlEngine',
    'HyperactivityEngine',
    'ADHDSimulator',
    
    # 유틸리티
    'ReproducibleRNG',
    'ExperimentMetadata',
    'StatisticalValidator',
    'ReportGenerator',
]
