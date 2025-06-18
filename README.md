# SpatialLM - 3D 전술작전 브리핑 시스템

<!-- markdownlint-disable first-line-h1 -->
<!-- markdownlint-disable html -->
<!-- markdownlint-disable no-duplicate-header -->

<div align="center">
  <img src="figures/logo_light.png#gh-light-mode-only" width="60%" alt="SpatialLM" />
  <img src="figures/logo_dark.png#gh-dark-mode-only" width="60%" alt="SpatialLM" />
</div>
<hr style="margin-top: 0; margin-bottom: 8px;">
<div align="center" style="margin-top: 0; padding-top: 0; line-height: 1;">
    <a href="https://manycore-research.github.io/SpatialLM" target="_blank" style="margin: 2px;"><img alt="Project"
    src="https://img.shields.io/badge/🌐%20Website-SpatialLM-ffc107?color=42a5f5&logoColor=white" style="display: inline-block; vertical-align: middle;"/></a>
    <a href="https://github.com/sinus-phi/SpatialLM" target="_blank" style="margin: 2px;"><img alt="GitHub"
    src="https://img.shields.io/badge/GitHub-SpatialLM-24292e?logo=github&logoColor=white" style="display: inline-block; vertical-align: middle;"/></a>
</div>
<div align="center" style="line-height: 1;">
    <a href="https://huggingface.co/manycore-research/SpatialLM-Llama-1B" target="_blank" style="margin: 2px;"><img alt="Hugging Face"
    src="https://img.shields.io/badge/%F0%9F%A4%97%20Hugging%20Face-SpatialLM%201B-ffc107?color=ffc107&logoColor=white" style="display: inline-block; vertical-align: middle;"/></a>
    <a href="https://huggingface.co/datasets/manycore-research/SpatialLM-Testset" target="_blank" style="margin: 2px;"><img alt="Dataset"
    src="https://img.shields.io/badge/%F0%9F%A4%97%20Dataset-SpatialLM-ffc107?color=ffc107&logoColor=white" style="display: inline-block; vertical-align: middle;"/></a>
</div>

## 📋 프로젝트 소개

**SpatialLM**은 3D 포인트클라우드 데이터를 분석하여 **전술작전 브리핑**을 생성하는 혁신적인 AI 시스템입니다. 이 시스템은 사용자가 3D로 재구성된 포인트클라우드 정보를 시각적으로 확인하면서, LLM 에이전트와 상호작용하여 전술작전을 계획하고 수립할 수 있는 통합 플랫폼을 제공합니다.

### 🌟 주요 특징

- **3D 공간 이해**: 포인트클라우드 데이터에서 벽, 문, 창문, 가구 등의 3D 구조 자동 인식
- **전술 브리핑 생성**: ChatGPT API를 활용한 상세한 전술적 분석 및 작전 계획 자동 생성
- **대화형 Q&A**: 실시간으로 전술적 질문에 대한 답변 제공
- **한국어 UI**: 완전한 한국어 사용자 인터페이스 지원
- **실시간 3D 시각화**: Rerun을 통한 3D 포인트클라우드 및 레이아웃 실시간 시각화
- **코드 생성 및 실행**: 시각화 및 분석을 위한 Python 코드 자동 생성 및 실행

### 🎯 시스템 기능

1. **공간 구조 분석**: 3D 포인트클라우드에서 건축 요소와 객체 자동 감지
2. **전술적 평가**: 공간의 방어/공격 지점, 이동 경로, 시야각 분석
3. **위험 요소 식별**: 맹점, 병목지점, 위험 구역 자동 탐지
4. **장비 추천**: 공간 특성에 맞는 최적의 장비 및 무기 추천
5. **팀 배치 계획**: 인원 배치 및 역할 분담 제안
6. **통신 계획**: 무선 통신 효율성 및 중계 위치 분석

## 🚀 빠른 시작

### 시스템 요구사항

- Python 3.11
- PyTorch 2.4.1
- CUDA 12.4 이상
- Ubuntu/Linux (권장)
- 16GB 이상 RAM
- NVIDIA GPU (8GB VRAM 이상 권장)

### 설치 방법

#### 1. 저장소 복제
```bash
git clone https://github.com/sinus-phi/SpatialLM.git
cd SpatialLM
```

#### 2. Conda 환경 설정
```bash
# CUDA 12.4를 지원하는 conda 환경 생성
conda create -n spatiallm python=3.11
conda activate spatiallm
conda install -y nvidia/label/cuda-12.4.0::cuda-toolkit conda-forge::sparsehash
```

#### 3. 종속성 설치
```bash
# Poetry를 사용한 종속성 설치
pip install poetry && poetry config virtualenvs.create false --local
poetry install
poe install-torchsparse  # TorchSparse 빌드 (시간이 소요됨)
```

#### 4. 추가 종속성 (브리핑 시스템용)
```bash
# PyQt5 및 추가 패키지 설치
pip install PyQt5 markdown requests configparser
```

### 사용 방법

#### 1. 기본 추론 (포인트클라우드 → 레이아웃)
```bash
# 예제 포인트클라우드 다운로드
huggingface-cli download manycore-research/SpatialLM-Testset pcd/scene0000_00.ply --repo-type dataset --local-dir .

# 레이아웃 추론 실행
python inference.py --point_cloud pcd/scene0000_00.ply --output scene0000_00.txt --model_path manycore-research/SpatialLM-Llama-1B
```

#### 2. 3D 시각화
```bash
# 예측된 레이아웃을 Rerun 형식으로 변환
python visualize.py --point_cloud pcd/scene0000_00.ply --layout scene0000_00.txt --save scene0000_00.rrd

# 3D 시각화 실행
rerun scene0000_00.rrd
```

#### 3. **🎖️ 전술 브리핑 시스템 실행 (메인 기능)**
```bash
# 통합 브리핑 시스템 실행 (최종 완성본)
python qt_rerun_briefing.py -i scene0000_00.rrd
```

이 명령을 실행하면:
- 3D 포인트클라우드가 Rerun 뷰어에서 자동으로 열립니다
- 한국어 UI의 브리핑 창이 표시됩니다
- ChatGPT를 통한 상세한 전술 분석이 자동 생성됩니다
- 실시간 Q&A를 통해 추가 전술적 질문을 할 수 있습니다

## 🛠️ 주요 구성 요소

### 핵심 파일들

- **`qt_rerun_briefing.py`**: 🎯 **메인 시스템** - 3D 시각화와 AI 브리핑을 통합한 완성된 전술작전 시스템
- **`inference.py`**: 포인트클라우드에서 3D 레이아웃 구조 추론
- **`visualize.py`**: 3D 시각화 및 Rerun 파일 생성
- **`spatiallm/`**: SpatialLM 모델 및 관련 유틸리티

### 브리핑 시스템 기능

1. **자동 공간 분석**: 포인트클라우드에서 전술적으로 중요한 요소들을 자동 식별
2. **ChatGPT 통합**: OpenAI GPT 모델을 활용한 상세한 전술 브리핑 생성
3. **실시간 상호작용**: 질문-답변을 통한 실시간 전술 조언
4. **시각화 코드 생성**: 특수 키워드("IIFA")를 통한 분석 코드 자동 생성 및 실행
5. **한국어 지원**: 완전한 한국어 UI 및 한글 폰트 지원

## 📊 지원하는 분석 항목

### 전술적 분석 영역
- **공간 구조 분석**: 벽체, 출입구, 창문 위치 및 치수
- **접근점 분석**: 모든 출입구의 접근 난이도 및 위험도 평가
- **이동 및 시야 분석**: 이동 경로, 시야각, 맹점 분석
- **물체 및 장애물 분석**: 엄폐물, 방어 등급, 탄도학적 보호 평가
- **전술적 위치 평가**: 최적 방어/공격 위치 및 통제 지점
- **환경 분석**: 조명, 음향, 통신 조건 평가
- **장비 추천**: 공간 특성에 최적화된 무기 및 장비 제안
- **작전 계획**: 팀 구성, 역할 분담, 타임라인 제안

## 🎨 사용자 인터페이스

### 한국어 UI 특징
- **완전한 한국어 지원**: 모든 메뉴, 버튼, 메시지가 한국어로 표시
- **한글 폰트 자동 설정**: NanumGothic 등 한글 폰트 자동 로드
- **직관적인 레이아웃**: 브리핑 영역과 Q&A 영역으로 구분된 현대적 UI
- **실시간 스트리밍**: ChatGPT 응답의 실시간 스트리밍 표시
- **마크다운 렌더링**: 구조화된 브리핑 정보의 깔끔한 표시

### UI 구성 요소
1. **3D 뷰어**: Rerun을 통한 포인트클라우드 3D 시각화
2. **브리핑 패널**: AI 생성 전술 브리핑 표시
3. **Q&A 패널**: 실시간 질문-답변 인터페이스
4. **설정 패널**: API 키 설정 및 모델 선택
5. **도구 모음**: 폰트 크기, 뷰 모드 등 설정

## ⚙️ 설정 및 구성

### ChatGPT API 설정
1. OpenAI API 키 획득 (https://platform.openai.com/api-keys)
2. 브리핑 시스템 실행 시 API 설정 다이얼로그에서 키 입력
3. 지원 모델: GPT-4, GPT-4-turbo, GPT-3.5-turbo

### 모델 설정
```bash
# 다른 SpatialLM 모델 사용
python qt_rerun_briefing.py -i scene.rrd -m manycore-research/SpatialLM-Qwen-0.5B
```

## 📂 프로젝트 구조

```
SpatialLM/
├── qt_rerun_briefing.py        # 🎯 메인 브리핑 시스템
├── inference.py                # 포인트클라우드 추론
├── visualize.py               # 3D 시각화
├── spatiallm/                 # 모델 라이브러리
│   ├── model/                 # AI 모델
│   ├── layout/                # 레이아웃 처리
│   └── pcd/                   # 포인트클라우드 처리
├── fonts/                     # 한글 폰트
├── figures/                   # 로고 및 이미지
├── SpatialLM-Testset/        # 테스트 데이터셋
└── processed_results/         # 처리 결과
```

## 🧪 테스트 및 평가

### 테스트 데이터셋 다운로드
```bash
huggingface-cli download manycore-research/SpatialLM-Testset --repo-type dataset --local-dir SpatialLM-Testset
```

### 성능 평가 실행
```bash
# 전체 테스트셋에 대한 추론 실행
python inference.py --point_cloud SpatialLM-Testset/pcd --output SpatialLM-Testset/pred --model_path manycore-research/SpatialLM-Llama-1B

# 성능 평가
python eval.py --metadata SpatialLM-Testset/test.csv --gt_dir SpatialLM-Testset/layout --pred_dir SpatialLM-Testset/pred --label_mapping SpatialLM-Testset/benchmark_categories.tsv
```

## 🚨 문제 해결

### 일반적인 문제들

#### GPU 메모리 부족
```bash
# GPU 메모리 사용량 최적화 설정이 이미 적용되어 있습니다
# inference.py에서 메모리 효율성을 위한 설정:
# - torch.float16 사용
# - GPU 메모리 90% 제한
# - expandable_segments 활성화
```

#### PyQt5 설치 오류
```bash
# Ubuntu/Debian
sudo apt-get install python3-pyqt5

# CentOS/RHEL
sudo yum install python3-qt5
```

#### 한글 폰트 문제
폰트가 제대로 표시되지 않으면 `fonts/` 디렉토리의 NanumGothic 폰트가 자동으로 로드됩니다.

#### ChatGPT API 오류
- API 키가 올바른지 확인
- API 사용량 한도 확인
- 네트워크 연결 상태 확인

## 📈 성능 벤치마크

SpatialLM-Testset에서의 성능:

| **Method**       | **SpatialLM-Llama-1B** | **SpatialLM-Qwen-0.5B** |
| ---------------- | ---------------------- | ----------------------- |
| **Floorplan**    | **mean IoU**           |                         |
| wall             | 78.62                  | 74.81                   |
| **Objects**      | **F1 @.25 IoU (3D)**   |                         |
| bed              | 95.24                  | 93.75                   |
| sofa             | 65.50                  | 66.15                   |
| dining table     | 54.26                  | 56.10                   |

## 🤝 기여 방법

1. 이 저장소를 포크합니다
2. 새로운 기능 브랜치를 생성합니다 (`git checkout -b feature/새기능`)
3. 변경사항을 커밋합니다 (`git commit -am '새기능 추가'`)
4. 브랜치에 푸시합니다 (`git push origin feature/새기능`)
5. Pull Request를 생성합니다

## 📜 라이선스

- **SpatialLM-Llama-1B**: Llama3.2 라이선스 하에 배포
- **SpatialLM-Qwen-0.5B**: Apache 2.0 라이선스 하에 배포
- **SceneScript 포인트클라우드 인코더**: CC-BY-NC-4.0 라이선스
- **TorchSparse**: MIT 라이선스

## 👨‍💻 개발자 정보

- **개발자**: sinus-phi
- **이메일**: pjw9825@gmail.com
- **GitHub**: https://github.com/sinus-phi/SpatialLM

## 🙏 감사의 말

이 프로젝트는 다음 오픈소스 프로젝트들을 기반으로 합니다:

[Llama3.2](https://github.com/meta-llama) | [Qwen2.5](https://github.com/QwenLM/Qwen2.5) | [Transformers](https://github.com/huggingface/transformers) | [SceneScript](https://github.com/facebookresearch/scenescript) | [TorchSparse](https://github.com/mit-han-lab/torchsparse) | [Rerun](https://rerun.io/)

---

## 🎖️ 전술작전 브리핑 시스템 - 추가 정보

### 시스템의 독특한 특징

1. **군사 전술 특화**: 일반적인 3D 분석이 아닌 전술작전에 특화된 분석 제공
2. **한국어 완벽 지원**: 모든 인터페이스와 분석 결과가 한국어로 제공
3. **실시간 상호작용**: ChatGPT와의 실시간 대화를 통한 상세한 전술 조언
4. **코드 생성 기능**: 특수 키워드를 통한 분석 코드 자동 생성 및 실행
5. **통합 시각화**: 3D 포인트클라우드와 AI 분석을 하나의 인터페이스에서 제공

### 전술적 분석의 깊이

시스템은 다음과 같은 상세한 전술적 분석을 제공합니다:

- **정량적 위험 평가**: 각 위치별 노출 확률과 위험도 수치화
- **최적 경로 계산**: 이동 시간과 위험도를 고려한 최적 경로 제안
- **장비 효율성 분석**: 공간 특성에 따른 장비별 효율성 평가
- **통신 품질 예측**: 공간 구조에 따른 무선 통신 효율성 분석
- **팀 배치 최적화**: 인원수와 역할에 따른 최적 배치 제안

이 시스템은 전술 훈련, 작전 계획, 공간 분석 등 다양한 용도로 활용할 수 있는 혁신적인 AI 도구입니다.
