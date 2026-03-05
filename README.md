# Computer Vision Tutorial

Computer Vision 실습 과제를 `lectureXX` 단위로 **통합 관리**하는 저장소이다.  
루트 `README.md`는 전체 강의 산출물의 형식, 제출 기준, 검수 기준을 중앙에서 관리하는 기준 문서로 사용한다.

## 1) 통합 관리 원칙
- 모든 강의는 동일한 폴더/파일 규격을 따른다.
- 모든 강의는 동일한 README 제출 포맷을 따른다.
- 실행 환경은 루트 `requirements.txt` 하나로 통합 관리한다.
- 결과 이미지는 각 강의의 `results/` 폴더에 모아 관리한다.

## 2) 표준 디렉터리 구조
```text
computer_vision_tutorial/
├── README.md                 # 통합 기준 문서(현재 파일)
├── requirements.txt          # 공통 실행 의존성
├── lecture01/
│   ├── e1.py
│   ├── e2.py
│   ├── e3.py
│   ├── results/
│   └── README.md
├── lecture02/
│   ├── e1.py
│   ├── ...
│   ├── results/
│   └── README.md
└── ...
```

## 3) 환경 표준 (공통)
1. conda 환경 생성
```bash
conda create -n cv_tutorial python=3.10 -y
```
2. 환경 활성화
```bash
conda activate cv_tutorial
```
3. 의존성 설치
```bash
pip install -r requirements.txt
```

## 4) Lecture 산출물 규격
각 `lectureXX`는 아래 조건을 반드시 만족해야 한다.

- 파일명: 과제 번호 순서대로 `e1.py`, `e2.py`, `e3.py` ...
- 실행성: 각 스크립트는 단독 실행 가능해야 함
- 입력 명시: 실행 인자(예: 이미지 경로)를 명확히 받도록 구현
- 결과 관리: 실행 결과 이미지는 `lectureXX/results/`에 저장

## 5) Lecture README 표준 포맷
각 `lectureXX/README.md`는 아래 순서를 고정으로 사용한다.

1. 문제 정의  
2. 문제 해결 메소드  
3. 실제 코드 (핵심 코드 포함)  
4. 실행 결과 (결과 이미지 첨부)  
5. 논의 (요구사항을 어떻게 만족했는지 항목별 설명)

## 6) 제출 전 통합 체크리스트
- `requirements.txt`가 최신이며 실제 사용 패키지만 포함하는가
- 각 `lectureXX`에 `README.md`가 존재하는가
- 각 README가 1~5 표준 섹션 순서를 지키는가
- `3. 실제 코드`에 핵심 코드가 포함되어 있는가
- `4. 실행 결과`에 결과 이미지가 첨부되어 있는가
- `5. 논의`에 요구사항 만족 근거가 항목별로 작성되어 있는가

## 7) 실행 예시
```bash
python lecture01/e1.py <image_path>
python lecture01/e2.py <image_path>
python lecture01/e3.py <image_path>
```
