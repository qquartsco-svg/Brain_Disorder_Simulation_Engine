"""
통계적 검증 모듈

시뮬레이션 결과의 통계적 분석 및 신뢰도 계산
"""

import numpy as np
from typing import Dict, List, Tuple, Optional
from collections import deque


class StatisticalValidator:
    """
    통계적 검증 클래스
    
    Seed sweep 기반 신뢰도 계산 및 분포 분석
    """
    
    def __init__(self):
        self.sweep_results = {
            'attention': [],
            'impulsivity': [],
            'hyperactivity': []
        }
    
    def add_sweep_result(self, attention: float, impulsivity: float, 
                        hyperactivity: float):
        """Seed sweep 결과 추가"""
        self.sweep_results['attention'].append(attention)
        self.sweep_results['impulsivity'].append(impulsivity)
        self.sweep_results['hyperactivity'].append(hyperactivity)
    
    def calculate_confidence_distribution(self, 
                                        thresholds: Optional[Dict[str, float]] = None) -> Dict:
        """
        분포 기반 일관성 점수 계산 (의료 기준: 통계적 무효성 방지)
        
        ⚠️ 주의: "신뢰도"가 아닌 "시뮬레이션 일관성 점수"로 표현
        임상적 신뢰도와 혼동 방지
        
        Args:
            thresholds: 각 점수별 임계값 (기본값 사용)
        
        Returns:
            일관성 점수 및 분포 정보
        """
        if thresholds is None:
            thresholds = {
                'attention': 0.7,
                'impulsivity': 0.6,
                'hyperactivity': 0.6
            }
        
        # 의료 기준: "신뢰도" 대신 "일관성 점수" 사용
        consistency_scores = {}
        distributions = {}
        
        # 의료 기준: 수치적 안전성 상수
        EPSILON = 1e-10  # 분산 0 판단 기준
        
        for key in ['attention', 'impulsivity', 'hyperactivity']:
            scores = self.sweep_results[key]
            
            if len(scores) == 0:
                consistency_scores[key] = 0.0
                distributions[key] = {
                    'mean': 0.0,
                    'std': 0.0,
                    'min': 0.0,
                    'max': 0.0,
                    'median': 0.0,
                    'variance': 0.0,
                    'is_valid': False,
                    'reason': 'no_data'
                }
                continue
            
            scores_array = np.array(scores)
            
            # 의료 기준: NaN/Inf 제거
            valid_mask = np.isfinite(scores_array)
            if not np.all(valid_mask):
                scores_array = scores_array[valid_mask]
                if len(scores_array) == 0:
                    consistency_scores[key] = 0.0
                    distributions[key] = {
                        'mean': 0.0,
                        'std': 0.0,
                        'min': 0.0,
                        'max': 0.0,
                        'median': 0.0,
                        'variance': 0.0,
                        'is_valid': False,
                        'reason': 'all_nan_or_inf'
                    }
                    continue
            
            # 의료 기준: 분산 0 체크 (상수 데이터)
            variance = float(np.var(scores_array))
            std = float(np.std(scores_array))
            
            if variance < EPSILON:
                # 분산이 0이면 통계적 의미 없음
                consistency_scores[key] = 0.0
                distributions[key] = {
                    'mean': float(np.mean(scores_array)),
                    'std': 0.0,
                    'min': float(scores_array[0]),
                    'max': float(scores_array[0]),
                    'median': float(scores_array[0]),
                    'variance': 0.0,
                    'is_valid': False,
                    'reason': 'zero_variance'
                }
                continue
            
            threshold = thresholds[key]
            
            # 임계값을 넘는 비율 (일관성 점수)
            above_threshold = np.sum(scores_array > threshold)
            consistency_scores[key] = above_threshold / len(scores_array)
            
            # 분포 통계
            distributions[key] = {
                'mean': float(np.mean(scores_array)),
                'std': std,
                'min': float(np.min(scores_array)),
                'max': float(np.max(scores_array)),
                'median': float(np.median(scores_array)),
                'q25': float(np.percentile(scores_array, 25)),
                'q75': float(np.percentile(scores_array, 75)),
                'variance': variance,
                'is_valid': True,
                'reason': 'valid'
            }
        
        return {
            'consistency_score': consistency_scores,  # "confidence" → "consistency_score"
            'distributions': distributions,
            'n_samples': len(self.sweep_results['attention'])
        }
    
    def calculate_confidence_intervals(self, alpha: float = 0.05) -> Dict:
        """
        신뢰구간 계산
        
        Args:
            alpha: 유의수준 (기본값 0.05 = 95% 신뢰구간)
        
        Returns:
            신뢰구간 정보
        """
        intervals = {}
        
        for key in ['attention', 'impulsivity', 'hyperactivity']:
            scores = np.array(self.sweep_results[key])
            
            if len(scores) == 0:
                intervals[key] = {'lower': 0.0, 'upper': 0.0, 'mean': 0.0}
                continue
            
            mean = np.mean(scores)
            std = np.std(scores)
            n = len(scores)
            
            # t-분포 기반 신뢰구간 (n이 작을 때)
            try:
                from scipy import stats
                if n < 30:
                    t_critical = stats.t.ppf(1 - alpha/2, df=n-1)
                    margin = t_critical * std / np.sqrt(n)
                else:
                    # 정규분포 근사 (z-분포)
                    z_critical = stats.norm.ppf(1 - alpha/2)
                    margin = z_critical * std / np.sqrt(n)
            except ImportError:
                # scipy가 없으면 정규분포 근사 사용
                z_critical = 1.96  # 95% 신뢰구간
                margin = z_critical * std / np.sqrt(n)
            
            intervals[key] = {
                'mean': float(mean),
                'lower': float(mean - margin),
                'upper': float(mean + margin),
                'margin': float(margin)
            }
        
        return intervals
    
    def reset(self):
        """결과 초기화"""
        self.sweep_results = {
            'attention': [],
            'impulsivity': [],
            'hyperactivity': []
        }


class CircularBuffer:
    """
    순환 버퍼
    
    O(1) 삽입/삭제로 메모리 효율적인 히스토리 관리
    """
    
    def __init__(self, maxsize: int):
        """
        순환 버퍼 초기화
        
        Args:
            maxsize: 최대 크기
        """
        self.buffer = deque(maxlen=maxsize)
        self.maxsize = maxsize
    
    def append(self, value: float):
        """값 추가 (O(1))"""
        self.buffer.append(value)
    
    def get_window(self, window_size: int) -> np.ndarray:
        """
        최근 window_size개 값 반환
        
        Args:
            window_size: 윈도우 크기
        
        Returns:
            NumPy 배열
        """
        if len(self.buffer) < window_size:
            return np.array(list(self.buffer))
        return np.array(list(self.buffer)[-window_size:])
    
    def get_all(self) -> np.ndarray:
        """모든 값 반환"""
        return np.array(list(self.buffer))
    
    def get_variance(self, window_size: Optional[int] = None) -> float:
        """
        분산 계산
        
        Args:
            window_size: 윈도우 크기 (None이면 전체)
        
        Returns:
            분산 값
        """
        if window_size is None:
            data = self.get_all()
        else:
            data = self.get_window(window_size)
        
        if len(data) == 0:
            return 0.0
        
        return float(np.var(data))
    
    def get_mean(self, window_size: Optional[int] = None) -> float:
        """평균 계산"""
        if window_size is None:
            data = self.get_all()
        else:
            data = self.get_window(window_size)
        
        if len(data) == 0:
            return 0.0
        
        return float(np.mean(data))
    
    def clear(self):
        """버퍼 비우기"""
        self.buffer.clear()
    
    def __len__(self) -> int:
        return len(self.buffer)

