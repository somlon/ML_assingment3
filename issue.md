# 이슈 기록

작업 중 발생한 이슈를 기록한다. 해결(수행)은 사용자가 지시할 때까지 진행하지 않는다.

## 기록 형식

```
## [YYYY-MM-DD HH:MM] 이슈 제목
- 발생 위치: <파일/모듈/명령어>
- 증상: <관찰된 동작/에러 메시지>
- 원인 추정: <분석 내용>
- 해결안(미수행): <제안된 해결 방법>
- 상태: 대기 / 진행 / 완료
```

---

<!-- 이 아래에 이슈를 추가한다 -->

## [2026-06-17 14:00] 제출 폴더가 notebooks/ 하위에 생성됨
- 발생 위치: `notebooks/02_preprocessing_and_modeling.ipynb` — `Config.submission_dir` (셀 4, "1. 환경 설정 및 데이터 로드")
- 증상: Jupyter 실행 시 `Path.cwd()`가 `notebooks/` 를 반환하므로, 제출 폴더가 프로젝트 루트가 아닌 `notebooks/submissions/` 에 생성됨
  - 예: `C:\...\ML_assingment3\notebooks\submissions\ML_HW3_test.csv`
  - 기대: `C:\...\ML_assingment3\submissions\ML_HW3_test.csv`
- 원인 추정: `field(default_factory=lambda: Path.cwd() / "submissions")` 가 노트북 실행 위치(cwd) 기준으로 동작. `notebooks/` 폴더에서 Jupyter 를 띄우는 일반적 워크플로와 충돌
- 영향: 제출 CSV 생성·`.gitignore` 매칭은 정상 동작 (기능적 결함은 아님). 다만 제출 산출물이 노트북 폴더 하위에 묻혀 찾기 어려움
- 해결안(미수행):
  1. `Config.submission_dir` 기본값을 **프로젝트 루트** 기준으로 잡기. 예: 데이터 디렉터리 탐색에 사용한 `resolve_data_dir()` 와 동일한 패턴으로 `resolve_project_root()` 도입
  2. 환경변수 `ASSIGNMENT3_PROJECT_ROOT` 추가해 명시적 오버라이드 지원
  3. (대안) 노트북 내부에서 `Path.cwd().name == "notebooks"` 조건으로 보정하는 방식은 하드코딩 성격이 있어 비권장
- 상태: 대기
