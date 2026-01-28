#!/bin/bash

# GitHub 배포 스크립트
# Brain Disorder Simulation Engine v1.0.0

set -e  # 오류 발생 시 중단

echo "============================================================"
echo "🚀 GitHub 배포 시작"
echo "============================================================"
echo ""

# 현재 디렉토리 확인
PROJECT_DIR="/Users/jazzin/Desktop/00_BRAIN/ADHD_Simulation_Engine"
cd "$PROJECT_DIR"

# 1. Git 상태 확인
echo "1️⃣ Git 상태 확인..."
if ! git status &>/dev/null; then
    echo "   ⚠️  Git 저장소가 초기화되지 않았습니다."
    echo "   Git 저장소를 초기화하시겠습니까? (y/n)"
    read -r response
    if [[ "$response" =~ ^[Yy]$ ]]; then
        git init
        echo "   ✅ Git 저장소 초기화 완료"
    else
        echo "   ❌ 배포를 중단합니다."
        exit 1
    fi
fi

# 2. 변경사항 확인
echo ""
echo "2️⃣ 변경사항 확인..."
git status --short

# 3. .gitignore 확인
echo ""
echo "3️⃣ .gitignore 확인..."
if [ ! -f .gitignore ]; then
    echo "   ⚠️  .gitignore 파일이 없습니다. 생성합니다..."
    cat > .gitignore << 'EOF'
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual Environment
venv/
ENV/
env/

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# Test outputs
test_output/
*.png
!docs/**/*.png

# Logs
*.log
audit_logs/

# Temporary files
*.tmp
*.bak
EOF
    echo "   ✅ .gitignore 생성 완료"
else
    echo "   ✅ .gitignore 존재"
fi

# 4. 모든 변경사항 추가
echo ""
echo "4️⃣ 변경사항 스테이징..."
git add .

# 5. 커밋 메시지
echo ""
echo "5️⃣ 커밋 생성..."
COMMIT_MSG="Release v1.0.0: Research-Ready Release

- 루프 라이브러리 모듈화 완료
- 기존 엔진 리팩터링 완료
- UnifiedDisorderSimulator 루프 통합 완료
- 배포 준비 완료
- 문서 완비
- 통합 테스트 통과"

git commit -m "$COMMIT_MSG" || {
    echo "   ⚠️  커밋할 변경사항이 없거나 이미 커밋되었습니다."
}

# 6. 원격 저장소 확인
echo ""
echo "6️⃣ 원격 저장소 확인..."
if ! git remote | grep -q origin; then
    echo "   ⚠️  원격 저장소가 설정되지 않았습니다."
    echo "   GitHub 저장소 URL을 입력하세요:"
    echo "   예: https://github.com/qquartsco-svg/Brain_Disorder_Simulation_Engine.git"
    read -r remote_url
    if [ -n "$remote_url" ]; then
        git remote add origin "$remote_url"
        echo "   ✅ 원격 저장소 추가 완료"
    else
        echo "   ❌ 원격 저장소 URL이 필요합니다."
        exit 1
    fi
else
    echo "   ✅ 원격 저장소 존재"
    git remote -v
fi

# 7. 태그 생성
echo ""
echo "7️⃣ 릴리스 태그 생성..."
if git tag | grep -q "v1.0.0"; then
    echo "   ⚠️  v1.0.0 태그가 이미 존재합니다."
    echo "   태그를 삭제하고 다시 생성하시겠습니까? (y/n)"
    read -r response
    if [[ "$response" =~ ^[Yy]$ ]]; then
        git tag -d v1.0.0
        git push origin :refs/tags/v1.0.0 2>/dev/null || true
    else
        echo "   ✅ 기존 태그 사용"
        SKIP_TAG=true
    fi
fi

if [ "$SKIP_TAG" != "true" ]; then
    git tag -a v1.0.0 -m "v1.0.0 - Research-Ready Release

첫 공식 릴리스
- 루프 라이브러리 모듈화
- 엔진 리팩터링 완료
- 통합 시뮬레이터 완성
- 연구/교육용 배포 준비 완료"
    echo "   ✅ 태그 생성 완료"
fi

# 8. 푸시 확인
echo ""
echo "8️⃣ 푸시 준비..."
echo "   다음 명령어를 실행하시겠습니까?"
echo ""
echo "   git push -u origin main    # (또는 master)"
echo "   git push origin v1.0.0     # 태그 푸시"
echo ""
echo "   자동으로 푸시하시겠습니까? (y/n)"
read -r response

if [[ "$response" =~ ^[Yy]$ ]]; then
    # 브랜치 확인
    CURRENT_BRANCH=$(git branch --show-current 2>/dev/null || echo "main")
    if [ -z "$CURRENT_BRANCH" ]; then
        CURRENT_BRANCH="main"
        git branch -M main 2>/dev/null || true
    fi
    
    echo ""
    echo "   📤 코드 푸시 중..."
    git push -u origin "$CURRENT_BRANCH" || {
        echo "   ⚠️  푸시 실패. 브랜치 이름을 확인하세요."
        echo "   현재 브랜치: $CURRENT_BRANCH"
        exit 1
    }
    
    echo ""
    echo "   📤 태그 푸시 중..."
    git push origin v1.0.0 || {
        echo "   ⚠️  태그 푸시 실패"
        exit 1
    }
    
    echo ""
    echo "============================================================"
    echo "✅ GitHub 배포 완료!"
    echo "============================================================"
    echo ""
    echo "다음 단계:"
    echo "1. GitHub 저장소에서 'Releases' → 'Draft a new release' 클릭"
    echo "2. Tag: v1.0.0 선택"
    echo "3. Title: v1.0.0 - Research-Ready Release"
    echo "4. Description: RELEASE_NOTES_v1.0.0.md 내용 복사"
    echo "5. 'Publish release' 클릭"
    echo ""
    echo "저장소 설정:"
    echo "- Description: GITHUB_REPOSITORY_DESCRIPTION.md 참고"
    echo "- Topics: 문서에 명시된 Topics 추가"
    echo ""
else
    echo ""
    echo "============================================================"
    echo "✅ 준비 완료!"
    echo "============================================================"
    echo ""
    echo "다음 명령어를 수동으로 실행하세요:"
    echo ""
    CURRENT_BRANCH=$(git branch --show-current 2>/dev/null || echo "main")
    echo "   git push -u origin $CURRENT_BRANCH"
    echo "   git push origin v1.0.0"
    echo ""
fi

