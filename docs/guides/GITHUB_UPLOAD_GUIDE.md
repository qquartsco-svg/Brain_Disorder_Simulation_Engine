# GitHub 업로드 가이드

## 1단계: GitHub에서 새 저장소 생성

1. GitHub에 로그인
2. 우측 상단의 "+" 버튼 클릭 → "New repository" 선택
3. 저장소 정보 입력:
   - **Repository name**: `adhd_simulation_engine`
   - **Description**: `Cookiie Brain Engine 기반 ADHD 전용 시뮬레이션 시스템`
   - **Visibility**: Public 또는 Private 선택
   - **Initialize this repository with**: 체크하지 않음 (이미 로컬에 있음)
4. "Create repository" 클릭

## 2단계: 원격 저장소 연결

```bash
cd /Users/jazzin/Desktop/00_BRAIN/ADHD_Simulation_Engine
git remote add origin https://github.com/qquartsco-svg/adhd_simulation_engine.git
```

## 3단계: GitHub에 업로드

```bash
git push -u origin main
```

## 확인

GitHub 저장소 페이지에서 파일이 업로드되었는지 확인하세요.

---

## 문제 해결

### 브랜치 이름이 다른 경우

```bash
git branch -m main
git push -u origin main
```

### 원격 저장소가 이미 있는 경우

```bash
git remote remove origin
git remote add origin https://github.com/qquartsco-svg/adhd_simulation_engine.git
git push -u origin main
```

### 인증 문제

GitHub Personal Access Token을 사용하거나 SSH 키를 설정하세요.

---

**작성일**: 2025-01-26  
**작성자**: GNJz (Qquarts)
