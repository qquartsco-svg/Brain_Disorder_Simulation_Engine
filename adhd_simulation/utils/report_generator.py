"""
실험 리포트 자동 생성 시스템

시뮬레이션 결과를 표준 형식으로 리포트 생성
"""

import json
import numpy as np
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


class ReportGenerator:
    """
    실험 리포트 생성기
    
    JSON, PNG, Markdown 형식으로 리포트 자동 생성
    """
    
    def __init__(self, output_dir: str = '.'):
        """
        리포트 생성기 초기화
        
        Args:
            output_dir: 출력 디렉토리
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def generate_report(self, results: Dict, experiment_metadata: Optional[Dict] = None,
                       output_prefix: str = 'adhd_simulation') -> Dict[str, str]:
        """
        종합 리포트 생성
        
        Args:
            results: 시뮬레이션 결과
            experiment_metadata: 실험 메타데이터
            output_prefix: 출력 파일 접두사
        
        Returns:
            생성된 파일 경로 딕셔너리
        """
        output_files = {}
        
        # JSON 리포트
        json_path = self.output_dir / f"{output_prefix}_report.json"
        self._generate_json_report(results, experiment_metadata, json_path)
        output_files['json'] = str(json_path)
        
        # Markdown 리포트
        md_path = self.output_dir / f"{output_prefix}_report.md"
        self._generate_markdown_report(results, experiment_metadata, md_path)
        output_files['markdown'] = str(md_path)
        
        # PNG 시각화
        png_path = self.output_dir / f"{output_prefix}_visualization.png"
        self._generate_visualization(results, png_path)
        output_files['png'] = str(png_path)
        
        return output_files
    
    def _generate_json_report(self, results: Dict, metadata: Optional[Dict],
                             filepath: Path):
        """JSON 리포트 생성"""
        report = {
            'timestamp': datetime.now().isoformat(),
            'experiment_metadata': metadata,
            'results': results,
            'summary': self._generate_summary(results)
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False, default=str)
    
    def _generate_markdown_report(self, results: Dict, metadata: Optional[Dict],
                                  filepath: Path):
        """Markdown 리포트 생성"""
        lines = []
        
        # 헤더
        lines.append("# ADHD Simulation Report")
        lines.append("")
        lines.append(f"**Generated**: {datetime.now().isoformat()}")
        lines.append("")
        
        # 실험 메타데이터
        if metadata:
            lines.append("## Experiment Metadata")
            lines.append("")
            lines.append(f"- **Experiment ID**: {metadata.get('experiment_id', 'N/A')}")
            lines.append(f"- **Seed**: {metadata.get('seed', 'N/A')}")
            lines.append(f"- **Git Commit**: {metadata.get('git_commit', 'N/A')}")
            lines.append("")
        
        # 결과 요약
        lines.append("## Results Summary")
        lines.append("")
        
        if 'assessment' in results:
            assessment = results['assessment']
            lines.append(f"### Assessment")
            lines.append("")
            lines.append(f"- **Summary**: {assessment.get('assessment', 'N/A')}")
            lines.append(f"- **Confidence**: {assessment.get('confidence', 0.0):.2f}")
            lines.append("")
            
            if 'scores' in assessment:
                lines.append("### Scores")
                lines.append("")
                for key, value in assessment['scores'].items():
                    lines.append(f"- **{key}**: {value:.3f}")
                lines.append("")
        
        # 상태공간 출력
        if 'state_space' in results:
            state_space = results['state_space']
            lines.append("### State Space")
            lines.append("")
            if state_space.get('state_vector'):
                for key, value in state_space['state_vector'].items():
                    if isinstance(value, (int, float)):
                        lines.append(f"- **{key}**: {value:.3f}")
            lines.append("")
        
        # 통계적 신뢰도
        if 'statistical_confidence' in results:
            conf = results['statistical_confidence']
            lines.append("### Statistical Confidence")
            lines.append("")
            if 'confidence' in conf:
                for key, value in conf['confidence'].items():
                    lines.append(f"- **{key}**: {value:.2%}")
            lines.append("")
        
        # 면책 조항
        lines.append("## Disclaimer")
        lines.append("")
        lines.append("⚠️ **This is a research tool, not a medical diagnostic device.**")
        lines.append("")
        lines.append("This simulation is for research and educational purposes only.")
        lines.append("It does NOT provide diagnosis, prediction, or treatment recommendations.")
        lines.append("")
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines))
    
    def _generate_visualization(self, results: Dict, filepath: Path):
        """시각화 생성"""
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        
        # 1. 점수 비교
        ax1 = axes[0, 0]
        if 'assessment' in results and 'scores' in results['assessment']:
            scores = results['assessment']['scores']
            labels = list(scores.keys())
            values = list(scores.values())
            ax1.bar(labels, values, color=['#FF6B6B', '#4ECDC4', '#FFD93D'], alpha=0.7)
            ax1.set_ylabel('Score')
            ax1.set_title('ADHD Scores')
            ax1.set_ylim(0, 1.0)
            ax1.grid(axis='y', alpha=0.3)
        
        # 2. 상태공간 (3D 투영)
        ax2 = axes[0, 1]
        if 'state_space' in results and results['state_space'].get('state_vector'):
            state = results['state_space']['state_vector']
            if state:
                # attention, arousal, energy를 2D로 투영
                attention = state.get('attention', 0.5)
                arousal = state.get('arousal', 0.5)
                energy = state.get('energy', 0.5) / 100.0 if state.get('energy', 0) > 0 else 0.5
                
                ax2.scatter([attention], [arousal], s=energy*500, 
                           c=[energy], cmap='viridis', alpha=0.7)
                ax2.set_xlabel('Attention')
                ax2.set_ylabel('Arousal')
                ax2.set_title('State Space (2D Projection)')
                ax2.set_xlim(0, 1)
                ax2.set_ylim(0, 1)
                ax2.grid(True, alpha=0.3)
        
        # 3. 통계적 신뢰도
        ax3 = axes[1, 0]
        if 'statistical_confidence' in results:
            conf = results['statistical_confidence']
            if 'confidence' in conf:
                labels = list(conf['confidence'].keys())
                values = list(conf['confidence'].values())
                ax3.bar(labels, values, color='green', alpha=0.7)
                ax3.set_ylabel('Confidence')
                ax3.set_title('Statistical Confidence')
                ax3.set_ylim(0, 1.0)
                ax3.grid(axis='y', alpha=0.3)
        
        # 4. 요약 텍스트
        ax4 = axes[1, 1]
        ax4.axis('off')
        summary_text = "ADHD Simulation Report\n\n"
        if 'assessment' in results:
            summary_text += f"Assessment: {results['assessment'].get('assessment', 'N/A')}\n"
            summary_text += f"Confidence: {results['assessment'].get('confidence', 0.0):.2f}\n"
        summary_text += "\n⚠️ Research tool only.\nNot a medical diagnostic device."
        ax4.text(0.1, 0.5, summary_text, fontsize=10, 
                verticalalignment='center', family='monospace')
        
        plt.tight_layout()
        plt.savefig(filepath, dpi=150, bbox_inches='tight')
        plt.close()
    
    def _generate_summary(self, results: Dict) -> Dict:
        """요약 생성"""
        summary = {
            'timestamp': datetime.now().isoformat(),
            'has_assessment': 'assessment' in results,
            'has_state_space': 'state_space' in results,
            'has_statistical_confidence': 'statistical_confidence' in results
        }
        
        if 'assessment' in results:
            summary['assessment'] = results['assessment'].get('assessment', 'N/A')
            summary['confidence'] = results['assessment'].get('confidence', 0.0)
        
        return summary

