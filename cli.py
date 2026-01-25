"""
ADHD Simulation Engine - Command Line Interface

명령줄에서 시뮬레이션을 실행하기 위한 CLI
"""

import argparse
import sys
import json
from pathlib import Path
from typing import Optional


def main():
    """메인 CLI 함수"""
    parser = argparse.ArgumentParser(
        description="ADHD Simulation Engine - Cookiie Brain Engine 기반 ADHD 시뮬레이션",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
예제:
  # 기본 시뮬레이션 실행
  python -m adhd_simulator

  # 설정 파일 지정
  python -m adhd_simulator --config config.json

  # 결과 저장 경로 지정
  python -m adhd_simulator --output results/

  # 시드 지정 (재현성)
  python -m adhd_simulator --seed 42

  # 나이/성별 지정
  python -m adhd_simulator --age 15 --gender male
        """
    )
    
    parser.add_argument(
        '--config',
        type=str,
        help='설정 파일 경로 (JSON 또는 YAML)'
    )
    
    parser.add_argument(
        '--output',
        type=str,
        default='results',
        help='결과 저장 디렉토리 (기본값: results)'
    )
    
    parser.add_argument(
        '--seed',
        type=int,
        help='랜덤 시드 (재현성을 위해)'
    )
    
    parser.add_argument(
        '--age',
        type=int,
        default=15,
        help='시뮬레이션 대상 나이 (기본값: 15)'
    )
    
    parser.add_argument(
        '--gender',
        type=str,
        choices=['male', 'female', 'other'],
        default='male',
        help='시뮬레이션 대상 성별 (기본값: male)'
    )
    
    parser.add_argument(
        '--scenario',
        type=str,
        choices=['normal', 'adhd', 'severe_adhd'],
        default='adhd',
        help='시뮬레이션 시나리오 (기본값: adhd)'
    )
    
    parser.add_argument(
        '--no-visualization',
        action='store_true',
        help='시각화 생성 안 함'
    )
    
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='상세 로그 출력'
    )
    
    parser.add_argument(
        '--version',
        action='version',
        version='ADHD Simulation Engine 1.0.0'
    )
    
    args = parser.parse_args()
    
    # adhd_simulator 모듈 import
    try:
        from adhd_simulator import ADHDSimulator
    except ImportError as e:
        print(f"❌ 오류: 모듈을 불러올 수 없습니다: {e}", file=sys.stderr)
        print("💡 해결: Cookiie Brain Engine이 설치되어 있는지 확인하세요.", file=sys.stderr)
        sys.exit(1)
    
    # 출력 디렉토리 생성
    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print("=" * 70)
    print("🧠 ADHD Simulation Engine")
    print("=" * 70)
    print(f"시나리오: {args.scenario}")
    print(f"나이: {args.age}, 성별: {args.gender}")
    if args.seed:
        print(f"시드: {args.seed}")
    print(f"결과 저장: {output_dir}")
    print("=" * 70)
    print()
    
    try:
        # 시뮬레이터 초기화
        simulator = ADHDSimulator(
            age=args.age,
            gender=args.gender,
            seed=args.seed
        )
        
        # 시뮬레이션 실행
        print("🚀 시뮬레이션 시작...")
        results = simulator.simulate_full_adhd_assessment(
            scenario=args.scenario,
            save_results=True,
            output_dir=str(output_dir)
        )
        
        print()
        print("✅ 시뮬레이션 완료!")
        print()
        
        # 결과 요약 출력
        if 'scores' in results:
            scores = results['scores']
            print("📊 결과 요약:")
            print(f"  주의력 결핍: {scores.get('attention_deficit', 0.0):.3f}")
            print(f"  충동성: {scores.get('impulsivity', 0.0):.3f}")
            print(f"  과잉행동: {scores.get('hyperactivity', 0.0):.3f}")
            print()
        
        # 시각화 생성
        if not args.no_visualization:
            print("📈 시각화 생성 중...")
            try:
                simulator.visualize_results(results, save_path=str(output_dir / "adhd_simulation_results.png"))
                print(f"  ✅ 시각화 저장: {output_dir / 'adhd_simulation_results.png'}")
            except Exception as e:
                print(f"  ⚠️ 시각화 생성 실패: {e}")
        
        print()
        print(f"💾 모든 결과가 저장되었습니다: {output_dir}")
        print("=" * 70)
        
    except Exception as e:
        print(f"❌ 오류 발생: {e}", file=sys.stderr)
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()

