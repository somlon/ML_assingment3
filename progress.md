# 진행 상황 (Progress Log)

> Assignment 3 (항공편 지연 예측) 작업 진행 상황 요약. 최신 업데이트가 위로 오게 한다.

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
