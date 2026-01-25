#!/bin/bash
# ADHD Simulation Engine 실행 스크립트

# 현재 디렉토리 설정
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Cookiie Brain Engine 경로 설정
COOKIIE_BRAIN_PATH="${COOKIIE_BRAIN_PATH:-$(dirname "$SCRIPT_DIR")/Cookiie_Brain_Engine}"
export COOKIIE_BRAIN_PATH

echo "======================================================================"
echo "🧠 ADHD Simulation Engine 실행"
echo "======================================================================"
echo ""
echo "📁 작업 디렉토리: $SCRIPT_DIR"
echo "📁 Cookiie Brain 경로: $COOKIIE_BRAIN_PATH"
echo ""

# Python 경로 확인
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3를 찾을 수 없습니다."
    exit 1
fi

# 실행
python3 adhd_simulator.py "$@"
