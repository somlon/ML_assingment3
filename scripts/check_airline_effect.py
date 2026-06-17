"""항공사별 항공편 지연율 차이의 통계적 유의성 검증.

train_set.csv 만 사용. test_set 은 참조하지 않음 (과제 규정 준수).

수행 분석:
  1. 항공사별 표본 크기 / 지연율 / 95% Wilson 신뢰구간
  2. 전체 항공사 × Delay 카이제곱 독립성 검정 + Cramer's V
  3. 각 항공사 vs 나머지 2-proportion z-test (Bonferroni 보정)

규칙 준수:
  - 컬럼명/임계값/파일명은 모두 변수로 분리 (하드코딩 금지)
  - 데이터 경로/파일명은 환경변수 오버라이드 지원
    (ASSIGNMENT3_DATA_DIR, ASSIGNMENT3_TRAIN)
"""
from __future__ import annotations

import os
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

TRAIN_FILENAME = os.environ.get("ASSIGNMENT3_TRAIN", "train_set.csv")
TARGET_COL = "Delay"
POSITIVE_LABEL = "Delayed"

# 항공사 식별 컬럼 우선순위 (EDA 에서 Airline ↔ Carrier_ID(DOT) 1:1 매핑 확인됨)
AIRLINE_COL_CANDIDATES = ("Airline", "Carrier_ID(DOT)", "Carrier_Code(IATA)")

MIN_SAMPLES_PER_AIRLINE = 100
SIGNIFICANCE_ALPHA = 0.05
MISSING_LABEL = "__missing__"


def resolve_data_dir() -> Path:
    env = os.environ.get("ASSIGNMENT3_DATA_DIR")
    if env:
        return Path(env).expanduser().resolve()
    here = Path.cwd()
    for cand in [here / "data", here.parent / "data", here]:
        if cand.exists() and (cand / TRAIN_FILENAME).exists():
            return cand.resolve()
    raise FileNotFoundError(
        f"{TRAIN_FILENAME} not found. Set ASSIGNMENT3_DATA_DIR to its parent dir."
    )


def pick_airline_col(df: pd.DataFrame) -> str:
    for c in AIRLINE_COL_CANDIDATES:
        if c in df.columns:
            return c
    raise KeyError(f"No airline column among {AIRLINE_COL_CANDIDATES}")


def wilson_ci(p: float, n: int, alpha: float = SIGNIFICANCE_ALPHA) -> tuple[float, float]:
    if n == 0:
        return (np.nan, np.nan)
    z = stats.norm.ppf(1 - alpha / 2)
    denom = 1 + z ** 2 / n
    centre = (p + z ** 2 / (2 * n)) / denom
    half = z * np.sqrt(p * (1 - p) / n + z ** 2 / (4 * n ** 2)) / denom
    return (centre - half, centre + half)


def two_proportion_ztest(d_a: int, n_a: int, d_b: int, n_b: int) -> tuple[float, float]:
    p_a = d_a / n_a if n_a else 0.0
    p_b = d_b / n_b if n_b else 0.0
    p_pool = (d_a + d_b) / (n_a + n_b) if (n_a + n_b) else 0.0
    se = np.sqrt(p_pool * (1 - p_pool) * (1 / n_a + 1 / n_b)) if (n_a and n_b) else 0.0
    if se == 0:
        return 0.0, 1.0
    z = (p_a - p_b) / se
    p_val = 2 * (1 - stats.norm.cdf(abs(z)))
    return z, p_val


def main() -> None:
    data_dir = resolve_data_dir()
    train_path = data_dir / TRAIN_FILENAME
    print(f"[load] {train_path}")

    df = pd.read_csv(train_path)
    print(f"  shape: {df.shape}")

    labeled = df[df[TARGET_COL].notna()].copy()
    labeled[TARGET_COL] = (labeled[TARGET_COL] == POSITIVE_LABEL).astype(int)
    base_rate = labeled[TARGET_COL].mean()
    print(f"  labeled rows: {len(labeled):,}  (base rate = {base_rate:.4f})")

    airline_col = pick_airline_col(labeled)
    n_missing = labeled[airline_col].isna().sum()
    print(f"\n[airline column] {airline_col}")
    print(f"  결측: {n_missing:,} ({n_missing/len(labeled)*100:.2f}%)")

    air = labeled[airline_col].fillna(MISSING_LABEL).astype(str)
    y = labeled[TARGET_COL].astype(int)

    # 1) 항공사별 표본·지연율·신뢰구간
    grouped = pd.DataFrame({
        "n": y.groupby(air).size(),
        "delayed": y.groupby(air).sum(),
    })
    grouped["rate"] = grouped["delayed"] / grouped["n"]
    ci = grouped.apply(lambda r: pd.Series(wilson_ci(r["rate"], int(r["n"])),
                                           index=["ci_lo", "ci_hi"]), axis=1)
    grouped = grouped.join(ci).sort_values("rate")
    grouped["diff_vs_base"] = grouped["rate"] - base_rate

    big = grouped[grouped["n"] >= MIN_SAMPLES_PER_AIRLINE].copy()
    print(f"\n[항공사별 지연율 — 표본 ≥ {MIN_SAMPLES_PER_AIRLINE}, n_airlines = {len(big)}]")
    print(big.to_string(float_format=lambda v: f"{v:.4f}"))

    # 2) Chi-square 독립성 검정 + Cramer's V
    contingency = pd.crosstab(air, y)
    chi2, p_chi2, dof, _ = stats.chi2_contingency(contingency)
    n_total = int(contingency.values.sum())
    cramer_v = float(np.sqrt(chi2 / (n_total * (min(contingency.shape) - 1))))
    print(f"\n[Chi-square (전체 항공사 × Delay)]")
    print(f"  χ²    = {chi2:.2f}")
    print(f"  dof   = {dof}")
    print(f"  p     = {p_chi2:.3e}")
    print(f"  Cramer's V = {cramer_v:.4f}  (작음:0.1 / 중간:0.3 / 큼:0.5)")
    verdict = "유의함" if p_chi2 < SIGNIFICANCE_ALPHA else "유의하지 않음"
    print(f"  → α={SIGNIFICANCE_ALPHA}: {verdict}")

    # 3) 항공사 vs 나머지 (Bonferroni)
    total_d = int(y.sum())
    total_n = len(y)
    n_tests = len(big)
    bonf = SIGNIFICANCE_ALPHA / max(n_tests, 1)

    rows = []
    for name, row in big.iterrows():
        n_a, d_a = int(row["n"]), int(row["delayed"])
        z, p_val = two_proportion_ztest(d_a, n_a, total_d - d_a, total_n - n_a)
        rows.append({
            "airline": name, "n": n_a, "rate": d_a / n_a,
            "diff": d_a / n_a - (total_d - d_a) / (total_n - n_a),
            "z": z, "p": p_val, "sig_bonf": p_val < bonf,
        })
    pair_df = pd.DataFrame(rows).sort_values("z")
    print(f"\n[항공사별 vs 나머지 — 2-proportion z-test, Bonferroni α={bonf:.2e}]")
    print(pair_df.to_string(index=False, float_format=lambda v: f"{v:.4f}"))
    print(f"\n  → 유의한 항공사 수: {int(pair_df['sig_bonf'].sum())} / {n_tests}")


if __name__ == "__main__":
    main()
