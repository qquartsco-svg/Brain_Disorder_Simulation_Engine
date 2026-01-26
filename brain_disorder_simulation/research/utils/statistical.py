"""
통계 분석 도구

의료 연구를 위한 통계 분석 기능
- Seed Sweep (다중 시뮬레이션)
- 통제 그룹 비교
- 통계 검정 (t-test, ANOVA)
- 효과 크기 (Cohen's d)
- 신뢰구간 계산

연구 근거:
- Cohen (1988) - Statistical power analysis
- Cumming (2012) - Understanding the new statistics
- Lakens (2013) - Calculating and reporting effect sizes

참고 문헌:
- Cohen, J. (1988). Statistical power analysis for the behavioral sciences (2nd ed.)
- Cumming, G. (2012). Understanding the new statistics: Effect sizes, confidence intervals, and meta-analysis
- Lakens, D. (2013). Calculating and reporting effect sizes to facilitate cumulative science

Author: GNJz (Qquarts)
Version: 1.0.0
"""

import numpy as np
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
from scipy import stats
import warnings
warnings.filterwarnings('ignore')


@dataclass
class StatisticalResult:
    """통계 분석 결과"""
    t_statistic: float
    p_value: float
    cohens_d: float
    confidence_interval: Tuple[float, float]
    effect_size_interpretation: str
    mean_diff: float
    std_diff: float
    n1: int
    n2: int
    df: int


@dataclass
class SeedSweepResult:
    """Seed Sweep 결과"""
    results: List[Dict[str, Any]]
    n_seeds: int
    mean_values: Dict[str, float]
    std_values: Dict[str, float]
    ci_95: Dict[str, Tuple[float, float]]
    distribution_stats: Dict[str, Dict[str, float]]


class StatisticalAnalyzer:
    """
    통계 분석 도구
    
    기능:
    - 다중 시뮬레이션 (Seed Sweep)
    - 통제 그룹 비교
    - 통계 검정 (t-test, ANOVA)
    - 효과 크기 (Cohen's d)
    - 신뢰구간 계산
    
    연구 근거:
    - 임상 연구에서 표준적으로 사용되는 통계 방법
    - 효과 크기는 Cohen (1988) 기준 사용
    - 신뢰구간은 95% 기준
    """
    
    def __init__(self):
        """통계 분석기 초기화"""
        pass
    
    def seed_sweep(self, 
                   simulator_func,
                   n_seeds: int = 100,
                   seed_start: int = 0,
                   **simulator_params) -> SeedSweepResult:
        """
        다중 시뮬레이션 실행 (Seed Sweep)
        
        연구 근거:
        - 시뮬레이션의 재현성 검증
        - 결과의 분포 분석
        - 통계적 신뢰도 확보
        
        Args:
            simulator_func: 시뮬레이터 함수 또는 클래스
            n_seeds: 시드 개수
            seed_start: 시작 시드 번호
            **simulator_params: 시뮬레이터 파라미터
        
        Returns:
            Seed Sweep 결과
        """
        results = []
        
        print(f"🔄 Seed Sweep 실행 중... (n={n_seeds})")
        
        for i, seed in enumerate(range(seed_start, seed_start + n_seeds)):
            try:
                # 시뮬레이터 실행
                if callable(simulator_func):
                    # 함수인 경우
                    result = simulator_func(seed=seed, **simulator_params)
                else:
                    # 클래스인 경우
                    simulator = simulator_func(seed=seed, **simulator_params)
                    result = simulator.simulate_full_assessment()
                
                results.append(result)
                
                # 진행 상황 출력
                if (i + 1) % 20 == 0:
                    print(f"  진행: {i + 1}/{n_seeds} ({100 * (i + 1) / n_seeds:.1f}%)")
                    
            except Exception as e:
                print(f"⚠️  Seed {seed} 실패: {e}")
                continue
        
        print(f"✅ Seed Sweep 완료: {len(results)}/{n_seeds} 성공")
        
        # 통계 계산
        if not results:
            raise ValueError("시뮬레이션 결과가 없습니다")
        
        # 결과에서 숫자 값 추출
        numeric_keys = self._extract_numeric_keys(results[0])
        
        mean_values = {}
        std_values = {}
        ci_95 = {}
        distribution_stats = {}
        
        for key in numeric_keys:
            values = [self._get_nested_value(r, key) for r in results]
            values = [v for v in values if v is not None and not np.isnan(v) and not np.isinf(v)]
            
            if len(values) > 0:
                mean_values[key] = np.mean(values)
                std_values[key] = np.std(values)
                ci_95[key] = self._calculate_confidence_interval(values, confidence=0.95)
                
                # 분포 통계
                distribution_stats[key] = {
                    'min': np.min(values),
                    'max': np.max(values),
                    'median': np.median(values),
                    'q25': np.percentile(values, 25),
                    'q75': np.percentile(values, 75),
                    'skewness': stats.skew(values) if len(values) > 2 else 0.0,
                    'kurtosis': stats.kurtosis(values) if len(values) > 2 else 0.0
                }
        
        return SeedSweepResult(
            results=results,
            n_seeds=len(results),
            mean_values=mean_values,
            std_values=std_values,
            ci_95=ci_95,
            distribution_stats=distribution_stats
        )
    
    def compare_groups(self,
                      group1: List[Dict[str, Any]],
                      group2: List[Dict[str, Any]],
                      metric_key: str,
                      alpha: float = 0.05) -> StatisticalResult:
        """
        두 그룹 비교
        
        연구 근거:
        - 독립 표본 t-test 사용
        - 효과 크기는 Cohen's d
        - 95% 신뢰구간 계산
        
        Args:
            group1: 첫 번째 그룹 결과 리스트
            group2: 두 번째 그룹 결과 리스트
            metric_key: 비교할 지표 키 (예: 'energy', 'motivation')
            alpha: 유의수준 (기본값: 0.05)
        
        Returns:
            통계 분석 결과
        """
        # 값 추출
        values1 = [self._get_nested_value(r, metric_key) for r in group1]
        values2 = [self._get_nested_value(r, metric_key) for r in group2]
        
        # NaN, Inf 제거
        values1 = [v for v in values1 if v is not None and not np.isnan(v) and not np.isinf(v)]
        values2 = [v for v in values2 if v is not None and not np.isnan(v) and not np.isinf(v)]
        
        if len(values1) < 2 or len(values2) < 2:
            raise ValueError(f"그룹 크기가 너무 작습니다: group1={len(values1)}, group2={len(values2)}")
        
        values1 = np.array(values1)
        values2 = np.array(values2)
        
        # t-test
        t_stat, p_value = stats.ttest_ind(values1, values2)
        
        # Cohen's d
        cohens_d = self._calculate_cohens_d(values1, values2)
        
        # 효과 크기 해석
        effect_size_interpretation = self._interpret_effect_size(cohens_d)
        
        # 평균 차이
        mean_diff = np.mean(values1) - np.mean(values2)
        
        # 표준편차 차이
        std_diff = np.std(values1) - np.std(values2)
        
        # 자유도
        df = len(values1) + len(values2) - 2
        
        # 신뢰구간
        ci = self._calculate_confidence_interval_diff(values1, values2, confidence=1 - alpha)
        
        return StatisticalResult(
            t_statistic=t_stat,
            p_value=p_value,
            cohens_d=cohens_d,
            confidence_interval=ci,
            effect_size_interpretation=effect_size_interpretation,
            mean_diff=mean_diff,
            std_diff=std_diff,
            n1=len(values1),
            n2=len(values2),
            df=df
        )
    
    def compare_multiple_groups(self,
                                groups: Dict[str, List[Dict[str, Any]]],
                                metric_key: str,
                                alpha: float = 0.05) -> Dict[str, Any]:
        """
        다중 그룹 비교 (ANOVA)
        
        연구 근거:
        - 일원 분산분석 (One-way ANOVA)
        - 사후 검정 (Tukey HSD)
        
        Args:
            groups: 그룹 이름과 결과 리스트 딕셔너리
            metric_key: 비교할 지표 키
            alpha: 유의수준
        
        Returns:
            ANOVA 결과
        """
        # 값 추출
        group_values = {}
        for group_name, group_results in groups.items():
            values = [self._get_nested_value(r, metric_key) for r in group_results]
            values = [v for v in values if v is not None and not np.isnan(v) and not np.isinf(v)]
            if len(values) > 0:
                group_values[group_name] = np.array(values)
        
        if len(group_values) < 2:
            raise ValueError("그룹이 2개 미만입니다")
        
        # ANOVA
        f_stat, p_value = stats.f_oneway(*group_values.values())
        
        # 그룹별 통계
        group_stats = {}
        for group_name, values in group_values.items():
            group_stats[group_name] = {
                'n': len(values),
                'mean': np.mean(values),
                'std': np.std(values),
                'ci_95': self._calculate_confidence_interval(values, confidence=0.95)
            }
        
        return {
            'f_statistic': f_stat,
            'p_value': p_value,
            'significant': p_value < alpha,
            'group_stats': group_stats,
            'n_groups': len(group_values)
        }
    
    def _calculate_cohens_d(self, group1: np.ndarray, group2: np.ndarray) -> float:
        """
        Cohen's d 계산
        
        연구 근거:
        - Cohen (1988) 기준
        - d = (M1 - M2) / pooled_std
        
        해석:
        - |d| < 0.2: 작은 효과
        - 0.2 ≤ |d| < 0.5: 중간 효과
        - 0.5 ≤ |d| < 0.8: 큰 효과
        - |d| ≥ 0.8: 매우 큰 효과
        """
        n1, n2 = len(group1), len(group2)
        mean1, mean2 = np.mean(group1), np.mean(group2)
        std1, std2 = np.std(group1, ddof=1), np.std(group2, ddof=1)
        
        # Pooled standard deviation
        pooled_std = np.sqrt(((n1 - 1) * std1**2 + (n2 - 1) * std2**2) / (n1 + n2 - 2))
        
        if pooled_std == 0:
            return 0.0
        
        cohens_d = (mean1 - mean2) / pooled_std
        
        return cohens_d
    
    def _interpret_effect_size(self, cohens_d: float) -> str:
        """효과 크기 해석"""
        abs_d = abs(cohens_d)
        
        if abs_d < 0.2:
            return "작은 효과 (negligible)"
        elif abs_d < 0.5:
            return "중간 효과 (small)"
        elif abs_d < 0.8:
            return "큰 효과 (medium)"
        else:
            return "매우 큰 효과 (large)"
    
    def _calculate_confidence_interval(self,
                                       values: np.ndarray,
                                       confidence: float = 0.95) -> Tuple[float, float]:
        """신뢰구간 계산"""
        if len(values) < 2:
            return (values[0], values[0]) if len(values) == 1 else (0.0, 0.0)
        
        mean = np.mean(values)
        std = np.std(values, ddof=1)
        n = len(values)
        
        # t-분포 사용
        t_critical = stats.t.ppf((1 + confidence) / 2, df=n - 1)
        margin = t_critical * (std / np.sqrt(n))
        
        return (mean - margin, mean + margin)
    
    def _calculate_confidence_interval_diff(self,
                                           group1: np.ndarray,
                                           group2: np.ndarray,
                                           confidence: float = 0.95) -> Tuple[float, float]:
        """두 그룹 평균 차이의 신뢰구간"""
        mean1, mean2 = np.mean(group1), np.mean(group2)
        std1, std2 = np.std(group1, ddof=1), np.std(group2, ddof=1)
        n1, n2 = len(group1), len(group2)
        
        # 표준 오차
        se = np.sqrt((std1**2 / n1) + (std2**2 / n2))
        
        # 자유도 (Welch's correction)
        df = ((std1**2 / n1 + std2**2 / n2)**2) / \
             ((std1**2 / n1)**2 / (n1 - 1) + (std2**2 / n2)**2 / (n2 - 1))
        df = max(1, int(df))
        
        # t-분포 사용
        t_critical = stats.t.ppf((1 + confidence) / 2, df=df)
        margin = t_critical * se
        
        mean_diff = mean1 - mean2
        
        return (mean_diff - margin, mean_diff + margin)
    
    def _extract_numeric_keys(self, result: Dict[str, Any]) -> List[str]:
        """결과에서 숫자 값 키 추출"""
        numeric_keys = []
        
        def extract_keys(obj, prefix=""):
            if isinstance(obj, dict):
                for key, value in obj.items():
                    full_key = f"{prefix}.{key}" if prefix else key
                    if isinstance(value, (int, float, np.number)):
                        numeric_keys.append(full_key)
                    elif isinstance(value, dict):
                        extract_keys(value, full_key)
                    elif isinstance(value, list):
                        if len(value) > 0 and isinstance(value[0], (int, float, np.number)):
                            numeric_keys.append(full_key)
        
        extract_keys(result)
        return numeric_keys
    
    def _get_nested_value(self, result: Dict[str, Any], key: str) -> Optional[float]:
        """중첩된 딕셔너리에서 값 추출"""
        keys = key.split('.')
        value = result
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return None
        
        if isinstance(value, (int, float, np.number)):
            return float(value)
        elif isinstance(value, list) and len(value) > 0:
            if isinstance(value[0], (int, float, np.number)):
                return float(np.mean(value))
        
        return None
    
    def generate_statistical_report(self,
                                   comparison_result: StatisticalResult,
                                   metric_name: str = "지표") -> str:
        """
        통계 분석 리포트 생성
        
        Args:
            comparison_result: 통계 분석 결과
            metric_name: 지표 이름
        
        Returns:
            리포트 문자열
        """
        report = f"""
{'=' * 70}
통계 분석 결과: {metric_name}
{'=' * 70}

그룹 정보:
  - 그룹 1: n = {comparison_result.n1}
  - 그룹 2: n = {comparison_result.n2}
  - 자유도: df = {comparison_result.df}

주요 통계:
  - 평균 차이: {comparison_result.mean_diff:.4f}
  - 표준편차 차이: {comparison_result.std_diff:.4f}

통계 검정:
  - t-통계량: t({comparison_result.df}) = {comparison_result.t_statistic:.4f}
  - p-값: p = {comparison_result.p_value:.6f}
  - 유의성: {'유의함' if comparison_result.p_value < 0.05 else '유의하지 않음'} 
    (α = 0.05)

효과 크기:
  - Cohen's d: {comparison_result.cohens_d:.4f}
  - 해석: {comparison_result.effect_size_interpretation}

신뢰구간 (95%):
  - [{comparison_result.confidence_interval[0]:.4f}, 
     {comparison_result.confidence_interval[1]:.4f}]

{'=' * 70}
"""
        return report


# 편의 함수
def seed_sweep(simulator_func, n_seeds: int = 100, **params) -> SeedSweepResult:
    """Seed Sweep 실행"""
    analyzer = StatisticalAnalyzer()
    return analyzer.seed_sweep(simulator_func, n_seeds=n_seeds, **params)


def compare_groups(group1: List[Dict], group2: List[Dict], metric_key: str) -> StatisticalResult:
    """두 그룹 비교"""
    analyzer = StatisticalAnalyzer()
    return analyzer.compare_groups(group1, group2, metric_key)

