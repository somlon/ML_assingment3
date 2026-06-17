# 진행 상황 (Progress Log)

> Assignment 3 (항공편 지연 예측) 작업 진행 상황 요약. 최신 업데이트가 위로 오게 한다.

---

## 2026-06-17 — Phase 2 진행: 전처리 + XGBoost 모델링 노트북 작성·실행 시작

### 완료한 일

1. **전처리 + 모델링 노트북 작성 (`claude/elegant-wright-tx82f9` 브랜치)**
   - `notebooks/02_preprocessing_and_modeling.ipynb` 신규 작성 (31셀: markdown 15 + code 16)
   - 단일 노트북, 셀 단위 구성 (모듈 디렉터리 없이)
   - 모든 컬럼 그룹·시간대 버킷 경계·임계값·시드를 `Config` dataclass 에 집중 (하드코딩 회피)
   - 환경변수 `ASSIGNMENT3_TRAIN`, `ASSIGNMENT3_TEST`, `ASSIGNMENT3_SUBMISSION` 으로 오버라이드 지원
   - `.gitignore` 에 `submissions/` 추가
   - PR #8 (`claude/elegant-wright-tx82f9` → `develop`) 머지됨

2. **이슈 기록 (`chore/issue-submission-dir` 브랜치)**
   - 노트북 실행 중 `Config.submission_dir = Path.cwd() / "submissions"` 가 Jupyter cwd 의존 → `notebooks/submissions/` 에 생성되는 현상 발견
   - 기능적 결함은 아니나 직관성 저하
   - 규칙 #4 에 따라 `issue.md` 에 기록만 (해결 미수행)
   - PR #9 (`chore/issue-submission-dir` → `agent`) 생성

3. **로컬 환경 셋업 + 노트북 실행 검증 (셀 1~8)**
   - 로컬 conda 환경 `2026ML` 에 `xgboost-3.2.0` 설치
   - 셀 1 (라이브러리/시드): 통과
   - 셀 2 (Config + 경로): `data/` 자동 인식, `train_set.csv` / `test_set.csv` 매칭 성공
   - 셀 3 (데이터 로드): train 800,000 × 19, test 50,936 × 18, 라벨 결측 74.49% — EDA 일치
   - 셀 4 (컬럼 정리): `Cancelled`, `Diverted`, `Airline`, `ID` drop, 15컬럼 잔존
   - 셀 5 (시각 → 4분할 시간대 버킷): 오전 33.7% / 오후 32.5% / 저녁 20.5% / 새벽 2.4% / `__missing__` 10.9%, Duration mean 137분
   - 셀 6 (결측 플래그): 7개 컬럼 약 10.9% (단, `Tail_Number_is_missing` 은 항상 0 — 상수 컬럼, 무해)
   - 셀 7 (파생): Route 6,674 / Carrier_Route 20,853
   - 셀 8 (라벨/언라벨 분리): labeled 204,065 / unlabeled 595,935 / test 50,936, base rate 0.1767 (EDA 정확 일치)
   - 셀 9 (인코더 정의): 완료
   - 셀 10 (단일 split sanity): X_tr 163,252 / X_va 40,813 / 33 컬럼, 컬럼 일치 True, object 잔존 X
     - NaN 잔존: `Estimated_Duration_min` 20.47% / `Arr_Hour` 10.86% / `Dep_Hour` 10.77% — **XGBoost native missing 처리 활용 예정**

### 다음 단계 (즉시)

- 셀 11~12: **XGBoost 베이스라인 (단일 split)** Log-loss 측정
- 셀 13~14: **Stratified 5-Fold CV** (과제 필수)
- 셀 15~16: 하이퍼파라미터 튜닝 (4 후보 grid)
- 셀 17~18: 준지도 학습 (pseudo-labeling) 시도 → CV 개선 여부 판단
- 셀 19~22: 최종 학습 + test 예측 + 제출 CSV 생성

### 환경 메모

- 로컬 작업 디렉터리: `C:\Users\ftqwe\anaconda3\envs\JUPYTER\ML PRO\ML_assingment3`
- 커널 환경: `C:\Users\ftqwe\anaconda3\envs\2026ML\python.exe` (폴더 이름과 무관)
- Jupyter cwd: `notebooks/` → 제출 폴더가 `notebooks/submissions/` 에 생성됨 (issue.md 기록됨)

### 브랜치 / PR 추가 분

| 브랜치 | 역할 | 상태 |
| --- | --- | --- |
| `claude/elegant-wright-tx82f9` | 전처리·모델링 노트북 작성 | 머지 후 보존 |
| `chore/issue-submission-dir` | submission_dir 이슈 기록 | PR #9 (대기) |
| `docs/progress-phase2-start` | Phase 2 진행 로그 업데이트 | 본 PR |

| PR | 제목 | 상태 |
| --- | --- | --- |
| #8 | Add preprocessing & XGBoost modeling notebook | merged → develop |
| #9 | Record submission_dir cwd dependency issue | open → agent |

---

## 2026-06-16 — Phase 1 완료: EDA 노트북 작성·문서화

### 완료한 일

1. **레포지토리 초기 셋업 (`agent` 브랜치)**
   - `rules.md`: 에이전트 기본 규칙 5종 정의 (전문가 수준 / 단계별 출력 확인 / 하드코딩 금지 / 이슈 기록 / 규칙 업데이트 가능성)
   - `issue.md`: 이슈 기록 템플릿
   - `.claude/hooks/session-start.sh`: 세션 시작 시 `rules.md`를 자동 컨텍스트로 주입하는 SessionStart 훅
   - `.claude/settings.json`: 훅 등록
   - PR #1 (`agent` → `main`) 머지됨

2. **과제 명세 정리 (`docs/assignment-3-spec` 브랜치)**
   - `assignment3.md`: PDF 명세를 마크다운으로 정리 (배점·제출·데이터 컬럼·체크리스트)
   - PR #2 (`docs/assignment-3-spec` → `agent`) 머지됨

3. **EDA 노트북 작성 (`develop` 브랜치)**
   - `notebooks/01_train_set_eda.ipynb`: 800,000 행 × 19 컬럼 train set 분석
   - `.gitignore`: `data/*.csv`, `*.ipynb_checkpoints` 등 제외
   - `data/README.md`: 데이터 폴더 가이드
   - PR #3 (`develop` → `main`) — **close 처리** (별도 머지 없이 develop 자체를 작업 베이스로 유지)

4. **데이터 파일명 보정 (`fix/dataset-filenames` 브랜치)**
   - `TRAIN_FILENAME = "train_set.csv"`, `TEST_FILENAME = "test_set.csv"` 변수로 명시
   - 환경변수 `ASSIGNMENT3_TRAIN`, `ASSIGNMENT3_TEST` 로 오버라이드 가능
   - 정확 매칭 실패 시 키워드 매칭 폴백 유지
   - PR #4 (`fix/dataset-filenames` → `develop`) 머지됨

5. **셀별 분석/전처리 주석 추가 (`docs/cell-annotations` 브랜치)**
   - 25/25 코드 셀 상단에 `# >>> [분석 노트] ... # <<<` 블록 삽입
   - 셀 단위 분석 의도·전처리 목적·후속 활용 포인트 기록
   - PR #5 (`docs/cell-annotations` → `develop`) 머지됨

### EDA 핵심 결과 (요약)

- **데이터 규모**: train 800,000 × 19, test 50,936 × 18
- **타깃(`Delay`)**: 약 74% 미라벨 → semi-supervised setting
- **클래스 불균형**: 라벨된 데이터 중 `Not_Delayed` ≈ 82.3% / `Delayed` ≈ 17.7%
- **결측**:
  - 시각·항공사·주 등 7개 컬럼이 약 10.9% 결측
  - 결측 컬럼들 간 동시 결측 상관은 낮음 → 독립적 결측 메커니즘 추정
  - 결측 자체가 타깃에 주는 신호는 미약 (Δ < 0.006)
- **운영 변수**:
  - `Cancelled`, `Diverted` 는 train 전체에서 0 단일값 → 사실상 무정보
  - `Tail_Number` 카디널리티 6,422 (high) → frequency / target encoding 필요
- **항공사 식별자**: `Airline` ↔ `Carrier_ID(DOT)` 1:1 단일매핑 100% → 중복 정보
- **그룹별 지연율**:
  - 월별: 6~8월(여름) 높음(0.20~0.22), 9~10월 낮음(0.14~0.15)
  - 출발 hour: 후반 시간대로 갈수록 누적 지연 경향
  - 출/도착 주: New Jersey, Puerto Rico, New York 등 동부 노선 높음
  - Distance decile: 약한 비단조 관계
- **시간 파생**: `Estimated_Duration_min` (도착 − 출발, overnight 보정) — 평균 약 141분

### 브랜치 / PR 정리

| 브랜치 | 역할 | 상태 |
| --- | --- | --- |
| `main` | 기본 브랜치 (rules + 훅) | 활성 |
| `agent` | 규칙·문서 집계 브랜치 | 활성 |
| `develop` | EDA·전처리·모델링 작업 브랜치 | 활성 (최신 `4dcc515`) |
| `docs/assignment-3-spec` | 명세 정리 | 머지 후 보존 |
| `fix/dataset-filenames` | 파일명 보정 | 머지 후 보존 |
| `docs/cell-annotations` | 셀 주석 추가 | 머지 후 보존 |

| PR | 제목 | 상태 |
| --- | --- | --- |
| #1 | Add agent base rules and SessionStart hook | merged → main |
| #2 | Add Assignment 3 spec summary | merged → agent |
| #3 | Add train set EDA notebook | closed (재정리 후 #4·#5 로 대체) |
| #4 | Fix dataset filenames in EDA notebook | merged → develop |
| #5 | Annotate EDA notebook cells with analysis/preprocessing notes | merged → develop |

### 적용된 규칙 준수 사항

- **하드코딩 금지**: 데이터 경로·파일명·컬럼·타깃 모두 변수화 (환경변수 오버라이드 지원)
- **단계별 출력 확인**: 모든 셋업/머지/푸시 단계에서 사용자 확인 후 진행
- **이슈 기록**: 별도 이슈 발생 없음 (issue.md 비어 있음)
- **세션 자동 로드**: SessionStart 훅으로 매 세션 시작 시 `rules.md` 컨텍스트 주입

---

## 다음 단계 (Phase 2 후보)

1. **전처리 파이프라인 모듈화**
   - 시각(`HH:MM`) → 분/시 파생
   - `*_is_missing` 플래그
   - 항공사 식별자 중복 제거 (`Carrier_ID(DOT)` 유지)
   - 고카디널리티(`Tail_Number`) target / frequency encoding
   - `Cancelled` / `Diverted` 컬럼 제거 (단일값)

2. **모델링 노트북 (`notebooks/02_modeling.ipynb`)**
   - Stratified K-Fold 교차검증 (과제 명시 필수 항목)
   - 베이스라인: Logistic Regression
   - 메인: LightGBM / XGBoost (결측·고카디널리티 강건)
   - 평가지표: **Log-loss** (채점 기준)

3. **준지도 학습**
   - pseudo-labeling: 베이스 모델 확률로 미라벨 데이터 자기학습
   - confidence threshold 튜닝

4. **제출 산출물**
   - `ML_학번_HW3_test.csv`: `ID,Not_Delayed,Delayed` 확률
   - `ML_학번_이름_HW3.ipynb`: 정리된 최종 노트북
   - `ML_학번_이름_HW3.docx`: 보고서 (코드 로직 + 분석 과정)
