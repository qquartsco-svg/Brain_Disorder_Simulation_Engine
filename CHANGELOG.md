# Changelog

모든 주요 변경사항은 이 파일에 기록됩니다.

형식은 [Keep a Changelog](https://keepachangelog.com/ko/1.0.0/)를 따릅니다.
이 프로젝트는 [Semantic Versioning](https://semver.org/lang/ko/)을 따릅니다.

## [1.0.0] - 2025-01-27

### 추가됨
- **Phase 1: 구조 분리**
  - research/, engineering/, core/ 디렉토리 생성
  - 의료 연구용 vs 엔지니어링 관점 분리

- **Phase 2-1: 신경전달물질 시스템**
  - `DopamineSystem`: 도파민 시스템 모델링 (Tonic/Phasic)
  - `SerotoninSystem`: 세로토닌 시스템 모델링 (SSRI 효과 포함)
  - `NorepinephrineSystem`: 노르에피네프린 시스템 모델링
  - `NeurotransmitterSystem`: 통합 신경전달물질 시스템

- **Phase 2-2: 생체지표 매핑**
  - `FMRIBiomarkerExtractor`: fMRI 활성화 패턴 추출
  - `EEGBiomarkerExtractor`: EEG 파워 스펙트럼 추출
  - `HRVBiomarkerExtractor`: HRV 지표 추출
  - `BiomarkerExtractor`: 통합 생체지표 추출기

- **Phase 2-3: 통계 분석 도구**
  - `StatisticalAnalyzer`: 통계 분석 클래스
  - `seed_sweep()`: 다중 시뮬레이션 실행
  - `compare_groups()`: 두 그룹 비교 (t-test, Cohen's d)
  - `compare_multiple_groups()`: 다중 그룹 비교 (ANOVA)
  - `generate_statistical_report()`: 통계 리포트 생성

- **Phase 3: 임상 스케일 통합**
  - `HAMDMapper`: HAM-D (17항목) 매핑
  - `BDIMapper`: BDI (21항목) 매핑
  - `PHQ9Mapper`: PHQ-9 (9항목) 매핑
  - `ClinicalScaleMapper`: 통합 임상 스케일 매퍼
  - 입력값 범위 방어 (np.clip)
  - 경고 문구 추가 (시뮬레이션 기반, 임상 진단 아님)

- **Phase 4-1: 연구 논문용 데이터 생성**
  - `ResearchReportGenerator`: 연구 리포트 생성기
  - `generate_table1()`: 그룹별 평균 및 표준편차
  - `generate_table2()`: 통계 분석 결과
  - `generate_figure1()`: 그룹별 비교 그래프
  - `generate_figure2()`: 시간에 따른 변화 그래프
  - LaTeX, CSV 형식 출력 지원

- **Phase 4-2: 검증 및 문서화**
  - `BiologicalValidityValidator`: 생물학적 타당성 검증
  - `ClinicalRelevanceValidator`: 임상적 관련성 검증
  - `ReproducibilityValidator`: 연구 재현성 검증
  - `ComprehensiveValidator`: 통합 검증기

- **테스트 및 실행 파일**
  - `test_research_modules.py`: 연구 모듈 통합 테스트
  - `run_depression_simulation.py`: 우울증 시뮬레이션 실행
  - `run_simulation.py`: 통합 시뮬레이터 실행

- **문서**
  - `README.md`: 프로젝트 개요 및 사용법
  - `ENGINE_CAPABILITIES.md`: 엔진 활용 가능한 기능 설명
  - `PHAM_BLOCKCHAIN_SIGNATURE.md`: 블록체인 서명
  - `CHANGELOG.md`: 변경 이력
  - `LICENSE`: MIT License

### 개선됨
- 임상 스케일 매핑에 입력값 범위 방어 추가
- 모든 임상 스케일 리포트에 경고 문구 추가
- 코드 문서화 강화 (연구 근거, 참고 문헌)

### 보안
- 입력값 범위 검증 (np.clip)으로 수치 폭주 방지
- 경고 문구로 임상 오해 방지

---

## [Unreleased]

### 계획 중
- 불안 장애 시뮬레이터
- 공존 질환 시뮬레이션
- 머신러닝 기반 패턴 분석
- 시간 시리즈 분석
- 네트워크 분석

---

**형식 참고**:
- `추가됨`: 새로운 기능
- `변경됨`: 기존 기능의 변경
- `개선됨`: 기존 기능의 개선
- `제거됨`: 제거된 기능
- `보안`: 보안 관련 변경

