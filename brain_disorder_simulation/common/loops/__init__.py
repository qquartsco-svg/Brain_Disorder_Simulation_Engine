"""
루프 라이브러리 (Loops Library)

공통 동역학 루프를 추상화하여 재사용 가능한 모듈로 제공

구현된 루프:
1. NegativeBiasLoop - 부정적 편향 루프 (우울증, PTSD)
2. HyperarousalLoop - 과각성 루프 (PTSD, 불안장애)
3. ControlFailureLoop - 제어 실패 루프 (우울증, ADHD)
4. EnergyCollapseLoop - 에너지 붕괴 루프 (우울증)
5. MotivationCollapseLoop - 동기 붕괴 루프 (우울증, ADHD, PTSD)
6. IntrusiveMemoryLoop - 침입 기억 루프 (PTSD, 우울증, 불안장애)
7. AvoidanceReinforcementLoop - 회피 강화 루프 (PTSD, 불안장애, OCD)

Author: GNJz (Qquarts)
Version: 1.0.0
"""

from .base_loop import (
    BaseLoop,
    LoopState,
    LoopParameters
)

from .negative_bias_loop import (
    NegativeBiasLoop,
    NegativeBiasLoopState
)

from .hyperarousal_loop import (
    HyperarousalLoop,
    HyperarousalLoopState
)

from .control_failure_loop import (
    ControlFailureLoop,
    ControlFailureLoopState
)

from .energy_collapse_loop import (
    EnergyCollapseLoop,
    EnergyCollapseLoopState
)

from .motivation_collapse_loop import (
    MotivationCollapseLoop,
    MotivationCollapseLoopState
)

from .intrusive_memory_loop import (
    IntrusiveMemoryLoop,
    IntrusiveMemoryLoopState,
    TraumaticMemory
)

from .avoidance_reinforcement_loop import (
    AvoidanceReinforcementLoop,
    AvoidanceReinforcementLoopState
)

from .attention_instability_loop import (
    AttentionInstabilityLoop,
    AttentionInstabilityLoopState
)

from .reward_prediction_error_loop import (
    RewardPredictionErrorLoop,
    RewardPredictionErrorLoopState
)

__all__ = [
    # Base classes
    'BaseLoop',
    'LoopState',
    'LoopParameters',
    
    # Negative Bias Loop
    'NegativeBiasLoop',
    'NegativeBiasLoopState',
    
    # Hyperarousal Loop
    'HyperarousalLoop',
    'HyperarousalLoopState',
    
    # Control Failure Loop
    'ControlFailureLoop',
    'ControlFailureLoopState',
    
    # Energy Collapse Loop
    'EnergyCollapseLoop',
    'EnergyCollapseLoopState',
    
    # Motivation Collapse Loop
    'MotivationCollapseLoop',
    'MotivationCollapseLoopState',
    
    # Intrusive Memory Loop
    'IntrusiveMemoryLoop',
    'IntrusiveMemoryLoopState',
    'TraumaticMemory',
    
    # Avoidance Reinforcement Loop
    'AvoidanceReinforcementLoop',
    'AvoidanceReinforcementLoopState',

    # Attention Instability Loop
    'AttentionInstabilityLoop',
    'AttentionInstabilityLoopState',

    # Reward Prediction Error Loop
    'RewardPredictionErrorLoop',
    'RewardPredictionErrorLoopState',
]

