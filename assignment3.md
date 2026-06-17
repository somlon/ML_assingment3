# Assignment 3 — 항공편 지연 예측 (Flight Delay Prediction)

> 본 문서는 `Assignment_3.pdf` 원본 명세를 마크다운으로 정리한 것입니다. 채점·제출 기준이 변경되면 본 문서를 갱신합니다.

## 1. 과제 개요

- 과제란에 업로드된 `train.csv`로 항공편 **지연 여부**를 판단하는 ML 모델을 학습한다.
- `test.csv`의 unseen data에 대해 각 샘플의 **`Not_Delayed`, `Delayed` 확률**을 예측한다.
- 예측 결과를 **CSV 파일**로 제출한다.

## 2. 평가 기준 (배점)

| 항목 | 배점 |
| --- | --- |
| EDA 및 데이터 전처리 | 30 |
| 모델 학습 | 30 |
| test set 성능 (Log-loss 기준) | 60 |

> test set 성능은 **Log-loss** 로 채점된다.

## 3. 제출

- **마감일**: 2026년 6월 17일 23:59 PM
- **딜레이 제출 불가**

### 제출 파일

| 파일명 | 내용 |
| --- | --- |
| `ML_학번_이름_HW3.docx` | 보고서 (코드 로직 + 분석 과정 설명) |
| `ML_학번_이름_HW3.ipynb` | 코드 |
| `ML_학번_HW3_test.csv` | test set 예측 결과 |

- 코드와 보고서는 **함께** 제출.
- 보고서로 코드 로직 판단이 어려우면 **0점**.

## 4. 규정

### ChatGPT / 외부 도구 사용

- ChatGPT 사용은 가능하나, **어떤 질문을 했고 어떤 답을 얻었는지** 명시해야 한다.
- 잘못된 답변에 대한 점수는 **0점**이며, 반드시 **reference check** 를 수행할 것.
- Reference 모음에 없는 부분에 대해서는 학생과 면담을 통해 random 하게 질문할 수 있으며, 답하지 못하면 **0점**.

### 데이터 사용 제한

- `train.csv` 이외의 외부 정보를 model training 또는 test set 결과 생성에 사용하면 **모델 학습 ~ test set 성능 무조건 0점**.
- `train.csv` 사용 방식은 본인 판단으로 진행한다.
- **Cross validation 은 반드시 수행한다.**

## 5. 데이터 컬럼 명세

| Column | 설명 |
| --- | --- |
| `ID` | 샘플 고유 ID |
| `Month` | 항공편 출발 월 |
| `Day_of_Month` | Month 에 해당하는 월의 날짜 |
| `Estimated_Departure_Time` | 전산 시스템 기반 측정된 출발 시간 (현지 시각, `HH:MM`) |
| `Estimated_Arrival_Time` | 전산 시스템 기반 측정된 도착 시간 (현지 시각, `HH:MM`) |
| `Cancelled` | 항공편 취소 여부 (0: 취소되지 않음, 1: 취소됨) |
| `Diverted` | 항공편 경유 여부 (0: 경유하지 않음, 1: 경유함) |
| `Origin_Airport` | 출발 공항 고유 코드 (IATA) |
| `Origin_Airport_ID` | 출발 공항 고유 ID (US DOT ID) |
| `Origin_State` | 출발 공항이 위치한 주의 이름 |
| `Destination_Airport` | 도착 공항 고유 코드 (IATA) |
| `Destination_Airport_ID` | 도착 공항 고유 ID (US DOT ID) |
| `Destination_State` | 도착 공항이 위치한 주의 이름 |
| `Distance` | 출발 ↔ 도착 공항 거리 (mile) |
| `Airline` | 운항 항공사 |
| `Carrier_Code(IATA)` | 항공사 고유 코드 (IATA, 다른 항공사가 동일 코드를 가질 수 있음) |
| `Carrier_ID(DOT)` | 항공사 고유 ID (US DOT ID) |
| `Tail_Number` | 운항 항공기 고유 등록 번호 |
| `Delay` | **타깃**. 지연 여부 (`Not_Delayed`, `Delayed`) |

### 타깃(`Delay`) 특이사항

- 예측해야 하는 타깃.
- **다수 데이터에 레이블이 존재하지 않음** (semi-supervised setting).
- **준지도 학습**을 통해 레이블링할 수 있다.

## 6. 데이터 예시

### `train.csv` (일부)

```
TRAIN_000001,9,9,1145.0,1316.0,0,0,SEA,14747,Washington,MFR,13264,Oregon,352.0,Horizon Air,AS,19687.0,N430QX,
TRAIN_000002,4,10,825.0,1005.0,0,0,DEN,11292,Colorado,OAK,13796,California,957.0,Southwest Airlines Co.,WN,19393.0,N216WR,
TRAIN_000003,10,19,954.0,1158.0,0,0,CLT,11057,North Carolina,ALB,10257,New York,646.0,,AA,19805.0,N881NN,
TRAIN_000004,4,29,1920.0,2247.0,0,0,EWR,11618,New Jersey,SJC,14831,,2548.0,United Air Lines Inc.,UA,19977.0,N76288,
TRAIN_000005,5,26,635.0,1100.0,0,0,PHX,14107,Arizona,HOU,12191,Texas,1020.0,Southwest Airlines Co.,WN,19393.0,N730SW,
TRAIN_000006,10,24,718.0,1059.0,0,0,DFW,11298,Texas,MCO,13204,Florida,985.0,,AA,19805.0,N961AN,Not_Delayed
TRAIN_000007,9,19,1135.0,1305.0,0,0,CLT,11057,North Carolina,PIT,14122,Pennsylvania,366.0,American Airlines Inc.,AA,19805.0,N823AW,
TRAIN_000008,5,5,954.0,1151.0,0,0,BOS,10721,Massachusetts,RDU,14492,North Carolina,612.0,JetBlue Airways,,20409.0,N197JB,Not_Delayed
TRAIN_000009,9,19,1205.0,1345.0,0,0,IND,12339,Indiana,OAK,13796,California,1933.0,Southwest Airlines Co.,WN,19393.0,N7742B,Not_Delayed
```

> 마지막 컬럼(`Delay`)이 비어 있는 행이 다수 존재 — 준지도 학습 대상.

### 제출용 `test.csv` 출력 예시

```
ID,Not_Delayed,Delayed
TEST_000000,0,1
TEST_000001,0,1
TEST_000002,0.4,0.6
TEST_000003,0,1
TEST_000004,0,1
TEST_000005,0,1
TEST_000006,0,1
TEST_000007,0,1
TEST_000008,0,1
TEST_000009,0,1
TEST_000010,0.2,0.8
```

- 헤더: `ID,Not_Delayed,Delayed`
- 각 행은 샘플 ID 와 두 클래스에 대한 **확률** (각 행에서 두 값의 합이 1이 되어야 함).

## 7. 체크리스트

- [ ] EDA 수행 및 결측치/이상치/카디널리티 점검
- [ ] 데이터 전처리 (시각 파싱, 결측 처리, 인코딩, 스케일링 등)
- [ ] 준지도 학습(필요 시) 으로 unlabeled 데이터 활용
- [ ] **Cross validation 수행**
- [ ] 모델 학습 및 하이퍼파라미터 튜닝 (Log-loss 기준)
- [ ] `test.csv` 예측 확률 산출 (`Not_Delayed`, `Delayed`)
- [ ] 제출 CSV 포맷 검증 (헤더, ID 순서, 확률 합)
- [ ] 보고서 (`.docx`) 작성 — 코드 로직 + 분석 과정
- [ ] ChatGPT 사용 시 질문/답변 reference 정리
- [ ] 파일명 규칙 확인: `ML_학번_이름_HW3.docx`, `ML_학번_이름_HW3.ipynb`, `ML_학번_HW3_test.csv`
