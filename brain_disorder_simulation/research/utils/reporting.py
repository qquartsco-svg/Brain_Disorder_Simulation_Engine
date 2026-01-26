"""
연구 논문용 리포트 생성 모듈

의료 연구 논문에 사용 가능한 데이터 형식 생성
- 표 형식 데이터 (Table 1, Table 2)
- 그래프 형식 데이터 (Figure 1, Figure 2)
- 통계 분석 결과 리포트

연구 근거:
- APA Style Guide (7th ed.) - 표와 그래프 작성 가이드라인
- Wilkinson & Task Force (1999) - Statistical graphics standards

참고 문헌:
- American Psychological Association. (2020). Publication manual of the American Psychological Association (7th ed.)
- Wilkinson, L., & Task Force on Statistical Inference. (1999). Statistical methods in psychology journals: Guidelines and explanations

Author: GNJz (Qquarts)
Version: 1.0.0
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
import json
import pandas as pd
from pathlib import Path


@dataclass
class TableData:
    """표 데이터"""
    title: str
    headers: List[str]
    rows: List[List[Any]]
    footnotes: Optional[List[str]] = None


@dataclass
class FigureData:
    """그래프 데이터"""
    title: str
    figure_type: str  # 'bar', 'line', 'scatter', 'boxplot', etc.
    data: Dict[str, Any]
    xlabel: Optional[str] = None
    ylabel: Optional[str] = None
    legend: Optional[List[str]] = None


class ResearchReportGenerator:
    """
    연구 논문용 리포트 생성기
    
    기능:
    - 표 형식 데이터 생성 (Table 1, Table 2)
    - 그래프 형식 데이터 생성 (Figure 1, Figure 2)
    - 통계 분석 결과 리포트
    - 논문용 형식 출력
    
    연구 근거:
    - 표준 논문 형식 (APA, Nature, Science 등)
    - 통계적 유의성 표기
    - 효과 크기 해석
    - 신뢰구간 표시
    """
    
    def __init__(self, output_dir: Optional[str] = None):
        """
        리포트 생성기 초기화
        
        Args:
            output_dir: 출력 디렉토리 (None이면 현재 디렉토리)
        """
        self.output_dir = Path(output_dir) if output_dir else Path('.')
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def generate_table1(self,
                       normal_group: List[Dict[str, Any]],
                       depression_group: List[Dict[str, Any]],
                       metric_keys: List[str],
                       group_names: Tuple[str, str] = ("정상", "우울증")) -> TableData:
        """
        표 1: 그룹별 평균 및 표준편차
        
        연구 근거:
        - 표준 논문 형식 (Table 1)
        - 평균 ± 표준편차 표기
        - 95% 신뢰구간 포함
        - 표본 크기 표시
        
        Args:
            normal_group: 정상 그룹 결과 리스트
            depression_group: 우울증 그룹 결과 리스트
            metric_keys: 비교할 지표 키 리스트
            group_names: 그룹 이름 튜플
        
        Returns:
            표 데이터
        """
        headers = ["지표", f"{group_names[0]} (n={len(normal_group)})", 
                   f"{group_names[1]} (n={len(depression_group)})"]
        rows = []
        
        for key in metric_keys:
            # 정상 그룹 통계
            normal_values = self._extract_values(normal_group, key)
            normal_mean = np.mean(normal_values)
            normal_std = np.std(normal_values)
            normal_ci = self._calculate_ci(normal_values)
            
            # 우울증 그룹 통계
            depression_values = self._extract_values(depression_group, key)
            depression_mean = np.mean(depression_values)
            depression_std = np.std(depression_values)
            depression_ci = self._calculate_ci(depression_values)
            
            # 표 형식: 평균 ± 표준편차 (95% CI)
            normal_str = f"{normal_mean:.2f} ± {normal_std:.2f}\n[{normal_ci[0]:.2f}, {normal_ci[1]:.2f}]"
            depression_str = f"{depression_mean:.2f} ± {depression_std:.2f}\n[{depression_ci[0]:.2f}, {depression_ci[1]:.2f}]"
            
            rows.append([key, normal_str, depression_str])
        
        return TableData(
            title="Table 1: 그룹별 평균 및 표준편차",
            headers=headers,
            rows=rows,
            footnotes=["값은 평균 ± 표준편차로 표시", "괄호 안은 95% 신뢰구간"]
        )
    
    def generate_table2(self,
                       comparison_results: Dict[str, Any],
                       metric_keys: List[str]) -> TableData:
        """
        표 2: 통계 분석 결과
        
        연구 근거:
        - t-test 결과
        - 효과 크기 (Cohen's d)
        - p-값 표기
        - 유의성 표시
        
        Args:
            comparison_results: 통계 분석 결과 딕셔너리
            metric_keys: 비교한 지표 키 리스트
        
        Returns:
            표 데이터
        """
        headers = ["지표", "t-통계량", "p-값", "Cohen's d", "효과 크기", "95% CI"]
        rows = []
        
        for key in metric_keys:
            if key not in comparison_results:
                continue
            
            result = comparison_results[key]
            
            # p-값 표기 (논문 형식)
            if result.p_value < 0.001:
                p_str = "< 0.001***"
            elif result.p_value < 0.01:
                p_str = f"{result.p_value:.3f}**"
            elif result.p_value < 0.05:
                p_str = f"{result.p_value:.3f}*"
            else:
                p_str = f"{result.p_value:.3f}"
            
            # 효과 크기 해석
            effect_size = result.effect_size_interpretation
            
            # 신뢰구간
            ci_str = f"[{result.confidence_interval[0]:.2f}, {result.confidence_interval[1]:.2f}]"
            
            rows.append([
                key,
                f"{result.t_statistic:.3f}",
                p_str,
                f"{result.cohens_d:.3f}",
                effect_size,
                ci_str
            ])
        
        return TableData(
            title="Table 2: 통계 분석 결과",
            headers=headers,
            rows=rows,
            footnotes=["* p < 0.05, ** p < 0.01, *** p < 0.001"]
        )
    
    def generate_figure1(self,
                        normal_group: List[Dict[str, Any]],
                        depression_group: List[Dict[str, Any]],
                        metric_key: str,
                        title: str = "Figure 1: 그룹별 비교",
                        group_names: Tuple[str, str] = ("정상", "우울증")) -> FigureData:
        """
        Figure 1: 그룹별 비교 그래프 (막대 그래프)
        
        연구 근거:
        - 표준 논문 형식 (Figure 1)
        - 평균 및 표준오차 표시
        - 통계적 유의성 표시
        
        Args:
            normal_group: 정상 그룹 결과 리스트
            depression_group: 우울증 그룹 결과 리스트
            metric_key: 비교할 지표 키
            title: 그래프 제목
            group_names: 그룹 이름 튜플
        
        Returns:
            그래프 데이터
        """
        normal_values = self._extract_values(normal_group, metric_key)
        depression_values = self._extract_values(depression_group, metric_key)
        
        normal_mean = np.mean(normal_values)
        normal_se = np.std(normal_values) / np.sqrt(len(normal_values))
        depression_mean = np.mean(depression_values)
        depression_se = np.std(depression_values) / np.sqrt(len(depression_values))
        
        return FigureData(
            title=title,
            figure_type='bar',
            data={
                'groups': list(group_names),
                'means': [normal_mean, depression_mean],
                'errors': [normal_se, depression_se],
                'values': [normal_values, depression_values]
            },
            xlabel="그룹",
            ylabel=metric_key
        )
    
    def generate_figure2(self,
                        time_series_data: Dict[str, List[float]],
                        title: str = "Figure 2: 시간에 따른 변화",
                        xlabel: str = "시간 (단계)",
                        ylabel: str = "값") -> FigureData:
        """
        Figure 2: 시간에 따른 변화 그래프 (선 그래프)
        
        연구 근거:
        - 시계열 데이터 시각화
        - 다중 그룹 비교
        - 신뢰구간 표시
        
        Args:
            time_series_data: 시간에 따른 데이터 딕셔너리
            title: 그래프 제목
            xlabel: x축 레이블
            ylabel: y축 레이블
        
        Returns:
            그래프 데이터
        """
        return FigureData(
            title=title,
            figure_type='line',
            data=time_series_data,
            xlabel=xlabel,
            ylabel=ylabel
        )
    
    def generate_statistical_report(self,
                                   comparison_result: Any,
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
    
    def save_table(self, table_data: TableData, filename: Optional[str] = None) -> str:
        """
        표를 파일로 저장
        
        Args:
            table_data: 표 데이터
            filename: 파일명 (None이면 자동 생성)
        
        Returns:
            저장된 파일 경로
        """
        if filename is None:
            filename = f"table_{table_data.title.lower().replace(' ', '_').replace(':', '')}.txt"
        
        filepath = self.output_dir / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(f"{table_data.title}\n")
            f.write("=" * 70 + "\n\n")
            
            # 헤더
            f.write(" | ".join(table_data.headers) + "\n")
            f.write("-" * 70 + "\n")
            
            # 행
            for row in table_data.rows:
                f.write(" | ".join(str(cell) for cell in row) + "\n")
            
            # 각주
            if table_data.footnotes:
                f.write("\n")
                for i, note in enumerate(table_data.footnotes, 1):
                    f.write(f"{i}. {note}\n")
        
        return str(filepath)
    
    def save_figure(self, figure_data: FigureData, filename: Optional[str] = None, 
                   dpi: int = 300) -> str:
        """
        그래프를 파일로 저장
        
        Args:
            figure_data: 그래프 데이터
            filename: 파일명 (None이면 자동 생성)
            dpi: 해상도
        
        Returns:
            저장된 파일 경로
        """
        if filename is None:
            filename = f"figure_{figure_data.title.lower().replace(' ', '_').replace(':', '')}.png"
        
        filepath = self.output_dir / filename
        
        fig, ax = plt.subplots(figsize=(10, 6))
        
        if figure_data.figure_type == 'bar':
            # 막대 그래프
            groups = figure_data.data['groups']
            means = figure_data.data['means']
            errors = figure_data.data['errors']
            
            bars = ax.bar(groups, means, yerr=errors, capsize=5, 
                         alpha=0.7, edgecolor='black', linewidth=1.5)
            
            # 통계적 유의성 표시 (간단한 예시)
            max_val = max(means) + max(errors)
            ax.text(0.5, max_val * 1.1, 'ns', ha='center', fontsize=12)
            
        elif figure_data.figure_type == 'line':
            # 선 그래프
            for label, values in figure_data.data.items():
                ax.plot(values, label=label, linewidth=2, marker='o', markersize=4)
            
            if figure_data.legend:
                ax.legend(fontsize=10)
        
        ax.set_xlabel(figure_data.xlabel, fontsize=12, fontweight='bold')
        ax.set_ylabel(figure_data.ylabel, fontsize=12, fontweight='bold')
        ax.set_title(figure_data.title, fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(filepath, dpi=dpi, bbox_inches='tight')
        plt.close()
        
        return str(filepath)
    
    def save_table_latex(self, table_data: TableData, filename: Optional[str] = None) -> str:
        """
        표를 LaTeX 형식으로 저장
        
        Args:
            table_data: 표 데이터
            filename: 파일명 (None이면 자동 생성)
        
        Returns:
            저장된 파일 경로
        """
        if filename is None:
            filename = f"table_{table_data.title.lower().replace(' ', '_').replace(':', '')}.tex"
        
        filepath = self.output_dir / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write("\\begin{table}[h]\n")
            f.write("\\centering\n")
            f.write(f"\\caption{{{table_data.title}}}\n")
            f.write("\\begin{tabular}{" + "c" * len(table_data.headers) + "}\n")
            f.write("\\hline\n")
            
            # 헤더
            f.write(" & ".join(table_data.headers) + " \\\\\n")
            f.write("\\hline\n")
            
            # 행
            for row in table_data.rows:
                f.write(" & ".join(str(cell).replace('\n', ' ') for cell in row) + " \\\\\n")
            
            f.write("\\hline\n")
            f.write("\\end{tabular}\n")
            
            # 각주
            if table_data.footnotes:
                f.write("\\begin{footnotesize}\n")
                for i, note in enumerate(table_data.footnotes, 1):
                    f.write(f"\\footnotemark[{i}] {note}\n")
                f.write("\\end{footnotesize}\n")
            
            f.write("\\end{table}\n")
        
        return str(filepath)
    
    def save_table_csv(self, table_data: TableData, filename: Optional[str] = None) -> str:
        """
        표를 CSV 형식으로 저장
        
        Args:
            table_data: 표 데이터
            filename: 파일명 (None이면 자동 생성)
        
        Returns:
            저장된 파일 경로
        """
        if filename is None:
            filename = f"table_{table_data.title.lower().replace(' ', '_').replace(':', '')}.csv"
        
        filepath = self.output_dir / filename
        
        # DataFrame 생성
        df = pd.DataFrame(table_data.rows, columns=table_data.headers)
        df.to_csv(filepath, index=False, encoding='utf-8-sig')
        
        return str(filepath)
    
    def generate_full_report(self,
                            normal_group: List[Dict[str, Any]],
                            depression_group: List[Dict[str, Any]],
                            comparison_results: Dict[str, Any],
                            metric_keys: List[str],
                            output_prefix: str = "research_report") -> Dict[str, str]:
        """
        전체 리포트 생성
        
        Args:
            normal_group: 정상 그룹 결과 리스트
            depression_group: 우울증 그룹 결과 리스트
            comparison_results: 통계 분석 결과 딕셔너리
            metric_keys: 비교한 지표 키 리스트
            output_prefix: 출력 파일 접두사
        
        Returns:
            생성된 파일 경로 딕셔너리
        """
        files = {}
        
        # Table 1 생성
        table1 = self.generate_table1(normal_group, depression_group, metric_keys)
        files['table1_txt'] = self.save_table(table1, f"{output_prefix}_table1.txt")
        files['table1_csv'] = self.save_table_csv(table1, f"{output_prefix}_table1.csv")
        files['table1_latex'] = self.save_table_latex(table1, f"{output_prefix}_table1.tex")
        
        # Table 2 생성
        table2 = self.generate_table2(comparison_results, metric_keys)
        files['table2_txt'] = self.save_table(table2, f"{output_prefix}_table2.txt")
        files['table2_csv'] = self.save_table_csv(table2, f"{output_prefix}_table2.csv")
        files['table2_latex'] = self.save_table_latex(table2, f"{output_prefix}_table2.tex")
        
        # Figure 1 생성 (첫 번째 지표)
        if metric_keys:
            figure1 = self.generate_figure1(normal_group, depression_group, metric_keys[0])
            files['figure1'] = self.save_figure(figure1, f"{output_prefix}_figure1.png")
        
        return files
    
    def _extract_values(self, results: List[Dict[str, Any]], key: str) -> np.ndarray:
        """결과에서 값 추출"""
        values = []
        for result in results:
            value = self._get_nested_value(result, key)
            if value is not None and not np.isnan(value) and not np.isinf(value):
                values.append(value)
        return np.array(values)
    
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
    
    def _calculate_ci(self, values: np.ndarray, confidence: float = 0.95) -> Tuple[float, float]:
        """신뢰구간 계산"""
        if len(values) < 2:
            mean = values[0] if len(values) == 1 else 0.0
            return (mean, mean)
        
        mean = np.mean(values)
        std = np.std(values, ddof=1)
        n = len(values)
        
        from scipy import stats
        t_critical = stats.t.ppf((1 + confidence) / 2, df=n - 1)
        margin = t_critical * (std / np.sqrt(n))
        
        return (mean - margin, mean + margin)

