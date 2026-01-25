# 🚀 GitHub 배포 가이드

ADHD Simulation Engine을 GitHub에 배포하는 단계별 가이드

---

## 📋 사전 준비

### 1. Git 저장소 확인

```bash
# 현재 디렉토리에서
cd /Users/jazzin/Desktop/00_BRAIN/ADHD_Simulation_Engine

# Git 상태 확인
git status
```

### 2. Git 저장소 초기화 (필요한 경우)

```bash
# Git 저장소가 없다면
git init

# .gitignore 확인
cat .gitignore
```

---

## 🚀 배포 단계

### Step 1: 파일 추가

```bash
# 모든 파일 추가
git add .

# 또는 특정 파일만 추가
git add setup.py pyproject.toml cli.py README.md LICENSE
git add *.md
git add *.py
```

### Step 2: 커밋

```bash
# 커밋 메시지와 함께 커밋
git commit -m "Package setup for GitHub deployment

- Add setup.py and pyproject.toml for package distribution
- Add CLI interface (cli.py)
- Add installation guide (INSTALLATION.md)
- Add deployment checklist (DEPLOYMENT_CHECKLIST.md)
- Update README.md with quick start guide
- Add GitHub Actions workflow for CI/CD"
```

### Step 3: GitHub 저장소 생성

1. GitHub에 로그인
2. 새 저장소 생성: https://github.com/new
3. 저장소 이름: `ADHD_Simulation_Engine`
4. 설명: "Cookiie Brain Engine 기반 ADHD 전용 시뮬레이션 시스템"
5. Public 또는 Private 선택
6. **README, .gitignore, license는 추가하지 않음** (이미 있음)
7. "Create repository" 클릭

### Step 4: 원격 저장소 연결

```bash
# 원격 저장소 추가 (URL은 실제 저장소 URL로 변경)
git remote add origin https://github.com/qquartsco-svg/ADHD_Simulation_Engine.git

# 또는 SSH 사용
git remote add origin git@github.com:qquartsco-svg/ADHD_Simulation_Engine.git

# 원격 저장소 확인
git remote -v
```

### Step 5: 브랜치 이름 설정

```bash
# 메인 브랜치 이름 설정
git branch -M main
```

### Step 6: 푸시

```bash
# 첫 푸시
git push -u origin main

# 이후 푸시
git push
```

---

## ✅ 배포 후 확인

### 1. GitHub에서 확인

- [ ] README.md가 제대로 렌더링되는지 확인
- [ ] 모든 파일이 업로드되었는지 확인
- [ ] LICENSE 파일이 있는지 확인

### 2. 클론 테스트

```bash
# 다른 디렉토리에서 클론 테스트
cd /tmp
git clone https://github.com/qquartsco-svg/ADHD_Simulation_Engine.git
cd ADHD_Simulation_Engine

# 설치 테스트
pip install -e .

# CLI 테스트
python -m adhd_simulator --help
```

---

## 📦 릴리스 태그 생성 (선택적)

### 버전 태그 생성

```bash
# 태그 생성
git tag -a v1.0.0 -m "Release version 1.0.0 - Initial package release"

# 태그 푸시
git push origin v1.0.0
```

### GitHub에서 릴리스 생성

1. GitHub 저장소 페이지로 이동
2. "Releases" 클릭
3. "Create a new release" 클릭
4. 태그 선택: `v1.0.0`
5. 제목: "v1.0.0 - Initial Release"
6. 설명 작성
7. "Publish release" 클릭

---

## 🔧 트러블슈팅

### 오류: "remote origin already exists"

```bash
# 기존 원격 저장소 제거
git remote remove origin

# 새로 추가
git remote add origin https://github.com/qquartsco-svg/ADHD_Simulation_Engine.git
```

### 오류: "failed to push some refs"

```bash
# 원격 저장소의 변경사항 가져오기
git pull origin main --allow-unrelated-histories

# 다시 푸시
git push -u origin main
```

### 오류: "authentication failed"

```bash
# Personal Access Token 사용 (GitHub Settings > Developer settings > Personal access tokens)
# 또는 SSH 키 설정
```

---

## 📚 추가 리소스

- [GitHub 가이드](https://docs.github.com/en/get-started)
- [Git 기본 명령어](https://git-scm.com/docs)
- [Semantic Versioning](https://semver.org/)

---

**✅ 배포 준비 완료!**

