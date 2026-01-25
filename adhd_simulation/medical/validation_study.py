"""
검증 연구 설계 모듈

임상 검증을 위한 통계 분석 도구
민감도/특이도, ROC 곡선, 교차 검증 등
"""

import numpy as np
from typing import Dict, List, Tuple, Optional
from scipy import stats
import warnings
warnings.filterwarnings('ignore')


class ValidationStudy:
    """
    검증 연구 분석 클래스
    
    임상 검증을 위한 통계 분석 수행
    """
    
    def __init__(self):
        """검증 연구 분석기 초기화"""
        self.true_labels = []  # 실제 라벨 (전문의 평가)
        self.predicted_scores = []  # 예측 점수 (시뮬레이션)
        self.predicted_labels = []  # 예측 라벨 (임계값 기반)
    
    def add_result(self, true_label: int, predicted_score: float, threshold: float = 0.7):
        """
        검증 결과 추가
        
        Args:
            true_label: 실제 라벨 (1: ADHD, 0: 정상)
            predicted_score: 예측 점수 (0.0 ~ 1.0)
            threshold: 임계값 (기본값 0.7)
        """
        self.true_labels.append(true_label)
        self.predicted_scores.append(predicted_score)
        self.predicted_labels.append(1 if predicted_score >= threshold else 0)
    
    def calculate_sensitivity_specificity(self, threshold: Optional[float] = None) -> Dict:
        """
        민감도(Sensitivity) 및 특이도(Specificity) 계산
        
        Args:
            threshold: 임계값 (None이면 최적 임계값 사용)
        
        Returns:
            민감도/특이도 및 관련 지표
        """
        if len(self.true_labels) == 0:
            return {
                'sensitivity': 0.0,
                'specificity': 0.0,
                'ppv': 0.0,
                'npv': 0.0,
                'accuracy': 0.0,
                'threshold': threshold or 0.7,
                'n_samples': 0
            }
        
        true_array = np.array(self.true_labels)
        scores_array = np.array(self.predicted_scores)
        
        if threshold is None:
            # 최적 임계값 찾기 (Youden's J statistic)
            threshold = self._find_optimal_threshold()
        
        predicted_array = (scores_array >= threshold).astype(int)
        
        # 혼동 행렬 (Confusion Matrix)
        tp = np.sum((true_array == 1) & (predicted_array == 1))  # True Positive
        tn = np.sum((true_array == 0) & (predicted_array == 0))  # True Negative
        fp = np.sum((true_array == 0) & (predicted_array == 1))  # False Positive
        fn = np.sum((true_array == 1) & (predicted_array == 0))  # False Negative
        
        # 민감도 (Sensitivity) = TP / (TP + FN)
        sensitivity = tp / (tp + fn) if (tp + fn) > 0 else 0.0
        
        # 특이도 (Specificity) = TN / (TN + FP)
        specificity = tn / (tn + fp) if (tn + fp) > 0 else 0.0
        
        # 양성 예측도 (PPV, Positive Predictive Value) = TP / (TP + FP)
        ppv = tp / (tp + fp) if (tp + fp) > 0 else 0.0
        
        # 음성 예측도 (NPV, Negative Predictive Value) = TN / (TN + FN)
        npv = tn / (tn + fn) if (tn + fn) > 0 else 0.0
        
        # 정확도 (Accuracy) = (TP + TN) / (TP + TN + FP + FN)
        accuracy = (tp + tn) / len(true_array) if len(true_array) > 0 else 0.0
        
        return {
            'sensitivity': float(sensitivity),
            'specificity': float(specificity),
            'ppv': float(ppv),
            'npv': float(npv),
            'accuracy': float(accuracy),
            'threshold': float(threshold),
            'confusion_matrix': {
                'tp': int(tp),
                'tn': int(tn),
                'fp': int(fp),
                'fn': int(fn)
            },
            'n_samples': len(true_array)
        }
    
    def calculate_roc_curve(self, num_points: int = 100) -> Dict:
        """
        ROC 곡선 계산
        
        Args:
            num_points: 곡선 점 개수
        
        Returns:
            ROC 곡선 데이터 및 AUC
        """
        if len(self.true_labels) == 0:
            return {
                'fpr': [],
                'tpr': [],
                'auc': 0.0,
                'thresholds': []
            }
        
        true_array = np.array(self.true_labels)
        scores_array = np.array(self.predicted_scores)
        
        # 임계값 범위
        thresholds = np.linspace(0, 1, num_points)
        
        tpr = []  # True Positive Rate (Sensitivity)
        fpr = []  # False Positive Rate (1 - Specificity)
        
        for threshold in thresholds:
            predicted = (scores_array >= threshold).astype(int)
            
            tp = np.sum((true_array == 1) & (predicted == 1))
            fn = np.sum((true_array == 1) & (predicted == 0))
            fp = np.sum((true_array == 0) & (predicted == 1))
            tn = np.sum((true_array == 0) & (predicted == 0))
            
            tpr_val = tp / (tp + fn) if (tp + fn) > 0 else 0.0
            fpr_val = fp / (fp + tn) if (fp + tn) > 0 else 0.0
            
            tpr.append(tpr_val)
            fpr.append(fpr_val)
        
        # AUC 계산 (Trapezoidal rule)
        auc = np.trapz(tpr, fpr)
        
        return {
            'fpr': [float(x) for x in fpr],
            'tpr': [float(x) for x in tpr],
            'auc': float(auc),
            'thresholds': [float(x) for x in thresholds]
        }
    
    def calculate_agreement(self, expert_scores: List[float]) -> Dict:
        """
        전문의 평가와의 일치도 계산
        
        Args:
            expert_scores: 전문의 평가 점수 목록
        
        Returns:
            일치도 분석 결과
        """
        if len(self.predicted_scores) != len(expert_scores):
            return {
                'correlation': 0.0,
                'icc': 0.0,
                'bland_altman': {
                    'mean_diff': 0.0,
                    'std_diff': 0.0,
                    'limits_of_agreement': [0.0, 0.0]
                }
            }
        
        pred_array = np.array(self.predicted_scores)
        expert_array = np.array(expert_scores)
        
        # 상관계수 (Pearson)
        correlation = float(np.corrcoef(pred_array, expert_array)[0, 1])
        
        # Intraclass Correlation Coefficient (ICC)
        # 간단한 버전 (실제로는 더 복잡한 계산 필요)
        icc = self._calculate_icc_simple(pred_array, expert_array)
        
        # Bland-Altman 분석
        differences = pred_array - expert_array
        mean_diff = float(np.mean(differences))
        std_diff = float(np.std(differences))
        limits = [mean_diff - 1.96 * std_diff, mean_diff + 1.96 * std_diff]
        
        return {
            'correlation': correlation,
            'icc': icc,
            'bland_altman': {
                'mean_diff': mean_diff,
                'std_diff': std_diff,
                'limits_of_agreement': limits
            },
            'n_samples': len(pred_array)
        }
    
    def _find_optimal_threshold(self) -> float:
        """
        최적 임계값 찾기 (Youden's J statistic)
        
        Returns:
            최적 임계값
        """
        if len(self.true_labels) == 0:
            return 0.7
        
        true_array = np.array(self.true_labels)
        scores_array = np.array(self.predicted_scores)
        
        thresholds = np.linspace(0, 1, 100)
        best_threshold = 0.7
        best_j = -1
        
        for threshold in thresholds:
            predicted = (scores_array >= threshold).astype(int)
            
            tp = np.sum((true_array == 1) & (predicted == 1))
            fn = np.sum((true_array == 1) & (predicted == 0))
            fp = np.sum((true_array == 0) & (predicted == 1))
            tn = np.sum((true_array == 0) & (predicted == 0))
            
            sensitivity = tp / (tp + fn) if (tp + fn) > 0 else 0.0
            specificity = tn / (tn + fp) if (tn + fp) > 0 else 0.0
            
            # Youden's J = Sensitivity + Specificity - 1
            j = sensitivity + specificity - 1
            
            if j > best_j:
                best_j = j
                best_threshold = threshold
        
        return float(best_threshold)
    
    def _calculate_icc_simple(self, pred: np.ndarray, expert: np.ndarray) -> float:
        """
        간단한 ICC 계산 (실제로는 더 정교한 방법 필요)
        
        Args:
            pred: 예측 점수
            expert: 전문의 점수
        
        Returns:
            ICC 값
        """
        # 간단한 버전: 일치도 기반
        # 실제 ICC는 더 복잡한 공식 필요
        mean_pred = np.mean(pred)
        mean_expert = np.mean(expert)
        
        if np.std(pred) == 0 or np.std(expert) == 0:
            return 0.0
        
        # 간단한 상관계수 기반 근사
        correlation = np.corrcoef(pred, expert)[0, 1]
        return float(correlation)
    
    def generate_validation_report(self) -> Dict:
        """
        검증 연구 리포트 생성
        
        Returns:
            종합 검증 리포트
        """
        if len(self.true_labels) == 0:
            return {
                'status': 'no_data',
                'message': '검증 데이터가 없습니다'
            }
        
        # 민감도/특이도
        sensitivity_specificity = self.calculate_sensitivity_specificity()
        
        # ROC 곡선
        roc = self.calculate_roc_curve()
        
        return {
            'sensitivity_specificity': sensitivity_specificity,
            'roc_curve': roc,
            'n_samples': len(self.true_labels),
            'status': 'complete'
        }
    
    def calculate_statistical_significance(self) -> Dict:
        """
        통계적 유의성 검정
        
        Returns:
            통계 검정 결과
        """
        if len(self.true_labels) < 10:
            return {
                'status': 'insufficient_data',
                'message': '최소 10개 샘플 필요'
            }
        
        true_array = np.array(self.true_labels)
        scores_array = np.array(self.predicted_scores)
        
        # 그룹 분리
        adhd_scores = scores_array[true_array == 1]
        normal_scores = scores_array[true_array == 0]
        
        if len(adhd_scores) == 0 or len(normal_scores) == 0:
            return {
                'status': 'insufficient_groups',
                'message': '두 그룹 모두 데이터 필요'
            }
        
        # t-검정 (정규성 가정)
        try:
            from scipy import stats
            t_stat, p_value = stats.ttest_ind(adhd_scores, normal_scores)
            
            # 효과 크기 (Cohen's d)
            pooled_std = np.sqrt(
                ((len(adhd_scores) - 1) * np.var(adhd_scores) + 
                 (len(normal_scores) - 1) * np.var(normal_scores)) /
                (len(adhd_scores) + len(normal_scores) - 2)
            )
            cohens_d = (np.mean(adhd_scores) - np.mean(normal_scores)) / pooled_std if pooled_std > 0 else 0.0
            
            # 효과 크기 해석
            if abs(cohens_d) < 0.2:
                effect_size_interpretation = 'negligible'
            elif abs(cohens_d) < 0.5:
                effect_size_interpretation = 'small'
            elif abs(cohens_d) < 0.8:
                effect_size_interpretation = 'medium'
            else:
                effect_size_interpretation = 'large'
            
            return {
                'status': 'complete',
                't_statistic': float(t_stat),
                'p_value': float(p_value),
                'significant': p_value < 0.05,
                'cohens_d': float(cohens_d),
                'effect_size': effect_size_interpretation,
                'adhd_mean': float(np.mean(adhd_scores)),
                'normal_mean': float(np.mean(normal_scores)),
                'adhd_std': float(np.std(adhd_scores)),
                'normal_std': float(np.std(normal_scores))
            }
        except ImportError:
            return {
                'status': 'scipy_required',
                'message': 'scipy 패키지 필요'
            }
    
    def calculate_positive_likelihood_ratio(self) -> float:
        """
        양성 우도비 (Positive Likelihood Ratio) 계산
        
        LR+ = Sensitivity / (1 - Specificity)
        
        Returns:
            LR+: 양성 우도비
        """
        metrics = self.calculate_sensitivity_specificity()
        sensitivity = metrics['sensitivity']
        specificity = metrics['specificity']
        
        if (1 - specificity) == 0:
            return float('inf') if sensitivity > 0 else 0.0
        
        return float(sensitivity / (1 - specificity))
    
    def calculate_negative_likelihood_ratio(self) -> float:
        """
        음성 우도비 (Negative Likelihood Ratio) 계산
        
        LR- = (1 - Sensitivity) / Specificity
        
        Returns:
            LR-: 음성 우도비
        """
        metrics = self.calculate_sensitivity_specificity()
        sensitivity = metrics['sensitivity']
        specificity = metrics['specificity']
        
        if specificity == 0:
            return float('inf') if (1 - sensitivity) > 0 else 0.0
        
        return float((1 - sensitivity) / specificity)
    
    def calculate_f1_score(self) -> float:
        """
        F1 Score 계산
        
        F1 = 2 * (Precision * Recall) / (Precision + Recall)
        
        Returns:
            F1 score
        """
        metrics = self.calculate_sensitivity_specificity()
        precision = metrics['ppv']  # Precision = PPV
        recall = metrics['sensitivity']  # Recall = Sensitivity
        
        if (precision + recall) == 0:
            return 0.0
        
        f1 = 2 * (precision * recall) / (precision + recall)
        return float(f1)
    
    def reset(self):
        """결과 초기화"""
        self.true_labels = []
        self.predicted_scores = []
        self.predicted_labels = []

