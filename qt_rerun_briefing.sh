#!/bin/bash

# RRD 뷰어와 브리핑 팝업을 실행하는 스크립트 (PyQt5 모던 UI 버전)
# QA 기능이 추가된 버전 (ChatGPT API 사용)

# 입력 인자 확인
if [ "$#" -lt 1 ]; then
    echo "사용법: $0 <rrd_file> [model_path] [language]"
    echo ""
    echo "인자:"
    echo "  rrd_file      - Rerun 뷰어로 열 RRD 파일 경로"
    echo "  model_path    - (선택) SpatialLM 모델 경로 (기본값: manycore-research/SpatialLM-Llama-1B)"
    echo "  language      - (선택) 브리핑 언어 (english/korean, 기본값: korean)"
    echo ""
    echo "예시: $0 scene0002_00.rrd"
    echo ""
    echo "새로운 기능: 브리핑 생성 후 ChatGPT API를 통한 질문-답변 가능"
    echo "참고: 질문-답변 기능을 사용하려면 OpenAI API 키가 필요합니다."
    exit 1
fi

# 기본값 설정
RRD_FILE=$1
MODEL_PATH=${2:-"manycore-research/SpatialLM-Llama-1B"}
LANGUAGE=${3:-"korean"}

# conda 환경 활성화
eval "$(conda shell.bash hook)"
conda activate spatiallm

echo "SpatialLM 환경이 활성화되었습니다."

# 필요한 라이브러리 설치 여부 확인
check_and_install_lib() {
    local lib=$1
    local pkg=${2:-$lib}
    
    if ! python -c "import $lib" &> /dev/null; then
        echo "$lib 라이브러리가 필요합니다. 설치하시겠습니까? (y/n)"
        read answer
        if [ "$answer" == "y" ] || [ "$answer" == "Y" ]; then
            echo "$pkg 설치 중..."
            pip install $pkg
        else
            echo "$pkg 설치가 필요합니다. 다음 명령으로 설치하세요:"
            echo "pip install $pkg"
            exit 1
        fi
    fi
}

# 필요한 라이브러리 확인
echo "필요한 라이브러리 확인 중..."
check_and_install_lib "PyQt5"
check_and_install_lib "markdown"
check_and_install_lib "torch"
check_and_install_lib "transformers"
check_and_install_lib "requests"  # ChatGPT API 요청용
check_and_install_lib "configparser"  # 설정 파일 관리용

echo "브리핑 및 ChatGPT QA 시스템 실행 중..."
echo "RRD 파일: $RRD_FILE"
echo "언어: $LANGUAGE"
echo "모델: $MODEL_PATH"
echo ""
echo "주의: 브리핑 생성 후 ChatGPT API를 통해 3D 공간에 대한 질문을 할 수 있습니다."
echo "질문-답변 기능을 사용하려면 OpenAI API 키 설정이 필요합니다."
echo ""

# PyQt5 기반 브리핑 뷰어 실행
python qt_rerun_briefing.py -i "$RRD_FILE" -m "$MODEL_PATH" -l "$LANGUAGE" 