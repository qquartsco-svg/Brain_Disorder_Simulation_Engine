# GitHub 배포 가이드

**작성일**: 2025-01-28  
**버전**: v1.0.0

---

## 🚀 빠른 배포 (자동 스크립트 사용)

### 방법 1: 배포 스크립트 실행 (권장)

```bash
cd /Users/jazzin/Desktop/00_BRAIN/ADHD_Simulation_Engine
./deploy_to_github.sh
```

스크립트가 다음을 자동으로 수행합니다:
1. Git 상태 확인
2. .gitignore 확인/생성
3. 변경사항 스테이징
4. 커밋 생성
5. 태그 생성 (v1.0.0)
6. 원격 저장소 확인
7. 푸시 (선택)

---

## 📝 수동 배포 (단계별)

### 1. Git 저장소 확인

```bash
cd /Users/jazzin/Desktop/00_BRAIN/ADHD_Simulation_Engine

# Git 상태 확인
git status

# 원격 저장소 확인
git remote -v
```

### 2. 원격 저장소 설정 (처음만)

```bash
# GitHub 저장소 URL 추가
git remote add origin https://github.com/qquartsco-svg/Brain_Disorder_Simulation_Engine.git

# 또는 SSH 사용
git remote add origin git@github.com:qquartsco-svg/Brain_Disorder_Simulation_Engine.git
```

### 3. 변경사항 커밋

```bash
# 모든 변경사항 추가
git add .

# 커밋
git commit -m "Release v1.0.0: Research-Ready Release

- 루프 라이브러리 모듈화 완료
- 기존 엔진 리팩터링 완료
- UnifiedDisorderSimulator 루프 통합 완료
- 배포 준비 완료"
```

### 4. 태그 생성

```bash
# 태그 생성
git tag -a v1.0.0 -m "v1.0.0 - Research-Ready Release

첫 공식 릴리스
- 루프 라이브러리 모듈화
- 엔진 리팩터링 완료
- 통합 시뮬레이터 완성
- 연구/교육용 배포 준비 완료"
```

### 5. 푸시

```bash
# 메인 브랜치 푸시
git push -u origin main
# 또는
git push -u origin master

# 태그 푸시
git push origin v1.0.0
```

---

## 🏷️ GitHub 릴리스 생성

### 1. GitHub 저장소 접속
- https://github.com/qquartsco-svg/Brain_Disorder_Simulation_Engine

### 2. Releases 페이지
- 저장소 → "Releases" → "Draft a new release" 클릭

### 3. 릴리스 정보 입력
- **Tag**: `v1.0.0` 선택
- **Release title**: `v1.0.0 - Research-Ready Release`
- **Description**: `RELEASE_NOTES_v1.0.0.md` 파일 내용 복사/붙여넣기

### 4. 릴리스 발행
- "Publish release" 클릭

---

## ⚙️ 저장소 설정

### Description
```
Cookiie Brain Engine 기반 뇌 질환 시뮬레이션 통합 시스템. ADHD, 우울증, PTSD 등 다양한 뇌 질환의 메커니즘을 시뮬레이션하는 연구/교육용 플랫폼. ⚠️ 의학적 진단 도구 아님.
```

### Topics (태그)
```
brain-simulation
cognitive-neuroscience
adhd-simulation
depression-simulation
ptsd-simulation
computational-modeling
research-tool
educational-tool
python
neuroscience
psychiatry
simulation-engine
loop-dynamics
cognitive-dynamics
```

### Features
- ✅ Issues: 활성화
- ✅ Discussions: 활성화 (선택)
- ✅ Wiki: 선택사항
- ✅ Projects: 선택사항

---

## ✅ 배포 후 확인사항

### 1. 저장소 접근 확인
- [ ] 저장소가 Public으로 설정되어 있는지 확인
- [ ] README.md가 정상적으로 표시되는지 확인
- [ ] 모든 파일이 업로드되었는지 확인

### 2. 릴리스 확인
- [ ] v1.0.0 태그가 생성되었는지 확인
- [ ] 릴리스 노트가 정상적으로 표시되는지 확인
- [ ] 다운로드 링크가 작동하는지 확인

### 3. 문서 확인
- [ ] README.md의 링크가 정상 작동하는지 확인
- [ ] 설치 방법이 명확한지 확인
- [ ] Cookiie Brain Engine 의존성 명시 확인

---

## 🔧 문제 해결

### 푸시 실패 시

```bash
# 원격 저장소 강제 업데이트 (주의: 기존 내용 덮어씀)
git push -u origin main --force

# 태그 강제 푸시
git push origin v1.0.0 --force
```

### 태그 삭제 후 재생성

```bash
# 로컬 태그 삭제
git tag -d v1.0.0

# 원격 태그 삭제
git push origin :refs/tags/v1.0.0

# 태그 재생성
git tag -a v1.0.0 -m "v1.0.0 - Research-Ready Release"
git push origin v1.0.0
```

### 브랜치 이름 확인

```bash
# 현재 브랜치 확인
git branch --show-current

# 브랜치 이름 변경
git branch -M main
```

---

## 📋 배포 체크리스트

배포 전 최종 확인:
- [x] 코드 품질 확인
- [x] 통합 테스트 통과
- [x] 문서 완비
- [x] README 의존성 명시 강화
- [x] 릴리스 노트 작성
- [ ] Git 커밋 완료
- [ ] 태그 생성 완료
- [ ] GitHub 푸시 완료
- [ ] 릴리스 생성 완료
- [ ] 저장소 설정 완료

---

## 🎉 배포 완료 후

배포가 완료되면:
1. 저장소 URL 공유 가능
2. 다른 연구자들이 사용 가능
3. 이슈/피드백 받을 수 있음
4. 협업 가능

---

**작성일**: 2025-01-28

