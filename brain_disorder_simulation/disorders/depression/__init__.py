"""
우울증 특화 모듈

우울증 전용 엔진 및 시뮬레이터
"""

from .motivation_engine import MotivationEngine, MotivationState
from .depression_simulator import DepressionSimulator
from .depression_tasks import (
    MotivationCollapseTask,
    RuminationPersistenceTask,
    EffortBasedDecisionMakingTask,
    TaskResult
)

__all__ = [
    'MotivationEngine',
    'MotivationState',
    'DepressionSimulator',
    'MotivationCollapseTask',
    'RuminationPersistenceTask',
    'EffortBasedDecisionMakingTask',
    'TaskResult',
]
