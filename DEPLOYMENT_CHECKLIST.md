# 📋 GitHub 배포 체크리스트

GitHub 배포를 위한 최종 확인 사항

---

## ✅ 완료된 항목

### 패키지 설정
- [x] `setup.py` 작성
- [x] `pyproject.toml` 작성
- [x] `MANIFEST.in` 작성
- [x] `requirements.txt` 정리

### 명령줄 인터페이스
- [x] `cli.py` 작성
- [x] `adhd_simulator.py`에 main() 함수 추가

### 문서화
- [x] `INSTALLATION.md` 작성
- [x] `README.md`에 빠른 시작 섹션 추가
- [x] `.gitignore` 확인

### CI/CD (선택적)
- [x] GitHub Actions 워크플로우 템플릿 추가

---

## 📝 배포 전 확인 사항

### 1. 파일 확인

```bash
# 필수 파일 확인
ls -la setup.py pyproject.toml requirements.txt README.md LICENSE
```

### 2. 패키지 빌드 테스트

```bash
# 패키지 빌드
python -m pip install build
python -m build

# 빌드 결과 확인
ls -la dist/
```

### 3. 설치 테스트

```bash
# 가상 환경에서 테스트 설치
python -m venv test_env
source test_env/bin/activate  # Windows: test_env\Scripts\activate
pip install dist/adhd_simulation_engine-1.0.0-py3-none-any.whl

# import 테스트
python -c "from adhd_simulator import ADHDSimulator; print('✅ 설치 성공!')"
```

### 4. CLI 테스트

```bash
# CLI 실행 테스트
python -m adhd_simulator --help
python -m adhd_simulator --version
```

---

## 🚀 GitHub 배포 단계

### 1. Git 저장소 초기화 (아직 안 했다면)

```bash
git init
git add .
git commit -m "Initial commit: ADHD Simulation Engine v1.0.0"
```

### 2. GitHub 저장소 생성

1. GitHub에서 새 저장소 생성
2. 저장소 URL 확인

### 3. 원격 저장소 연결

```bash
git remote add origin https://github.com/qquartsco-svg/ADHD_Simulation_Engine.git
git branch -M main
git push -u origin main
```

### 4. 릴리스 태그 생성 (선택적)

```bash
git tag -a v1.0.0 -m "Release version 1.0.0"
git push origin v1.0.0
```

---

## 📦 PyPI 배포 (선택적)

### 1. PyPI 계정 생성

https://pypi.org/account/register/

### 2. 빌드 및 업로드

```bash
# 빌드
python -m build

# 업로드 (테스트)
python -m twine upload --repository testpypi dist/*

# 업로드 (실제)
python -m twine upload dist/*
```

---

## ✅ 배포 후 확인

### 1. README 렌더링 확인
- GitHub에서 README.md가 제대로 렌더링되는지 확인

### 2. 설치 가이드 테스트
- 다른 환경에서 설치 가이드대로 설치 테스트

### 3. 이슈 템플릿 (선택적)
- `.github/ISSUE_TEMPLATE/` 디렉토리 생성
- 버그 리포트, 기능 요청 템플릿 추가

---

## 🎯 배포 완료 기준

- [ ] 모든 필수 파일이 저장소에 포함됨
- [ ] README.md가 제대로 렌더링됨
- [ ] 설치 가이드가 작동함
- [ ] CLI가 정상 작동함
- [ ] 라이선스 파일 포함됨
- [ ] 면책 조항 명시됨

---

## 📚 추가 리소스

- [GitHub Packages 가이드](https://docs.github.com/en/packages)
- [PyPI 가이드](https://packaging.python.org/tutorials/packaging-projects/)
- [Semantic Versioning](https://semver.org/)

---

**✅ 체크리스트 완료 후 GitHub에 배포 가능!**

