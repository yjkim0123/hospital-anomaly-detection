#!/usr/bin/env python3
"""
02_zscore_comparison.py
Compare Altman Z''-score distress classification with unsupervised consensus anomalies.

This analysis shows that:
1. Consensus anomalies capture DIFFERENT hospitals than Z-score distress
2. The overlap is partial, suggesting unsupervised methods detect patterns beyond traditional models
3. Chi-squared test of association between Z-score distress and consensus anomaly status

Reference: Altman, E.I. (2002). Revisiting Credit Scoring Models in a Basel II Environment.
"""

import pandas as pd
import numpy as np
import os
import json
from scipy import stats

# ── Paths ──────────────────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.join(BASE_DIR, "..")
DATA_PATH = "/Users/yongjun_kim/Documents/project_hospital/data/hospital_all_clean.pkl"
CONSENSUS_PATH = os.path.join(PROJECT_DIR, "code", "consensus_anomalies.csv")
OUTPUT_DIR = os.path.join(PROJECT_DIR, "data")
os.makedirs(OUTPUT_DIR, exist_ok=True)
OUTPUT_PATH = os.path.join(OUTPUT_DIR, "zscore_results.json")

# ── Load Data ──────────────────────────────────────────────────────
df = pd.read_pickle(DATA_PATH)
consensus_df = pd.read_csv(CONSENSUS_PATH)
print(f"Loaded hospital data: {df.shape}")
print(f"Consensus anomalies: {len(consensus_df)}")

# ── Column Mappings ────────────────────────────────────────────────
YEAR = "회계연도"
ID = "요양기관번호"
NAME = "요양기관명"
HTYPE = "종별"
ETYPE = "설립형태"

# Financial items for Z-score
CURRENT_ASSETS = "Ⅰ.유동자산"
CURRENT_LIAB = "Ⅰ.유동부채"
TOTAL_ASSETS = "자산총계"
TOTAL_LIAB = "부채총계"
EQUITY = "자본총계"
RETAINED_EARNINGS = "Ⅳ.이익잉여금(결손금)"
OPERATING_INCOME = "Ⅲ.의료이익(손실)"
NET_INCOME = "    당기순이익(순손실)"

# Convert to numeric
numeric_cols = [CURRENT_ASSETS, CURRENT_LIAB, TOTAL_ASSETS, TOTAL_LIAB, 
                EQUITY, RETAINED_EARNINGS, OPERATING_INCOME, NET_INCOME]
for col in numeric_cols:
    df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

# ── Filter to balanced panel (2019-2023) ───────────────────────────
YEARS = [2019, 2020, 2021, 2022, 2023]
HOSPITAL_TYPES = ["상급종합병원", "종합병원"]
df = df[df[HTYPE].isin(HOSPITAL_TYPES) & df[YEAR].isin(YEARS)]
panel_ids = df.groupby(ID)[YEAR].nunique()
panel_ids = panel_ids[panel_ids == 5].index
df = df[df[ID].isin(panel_ids)].copy()

print(f"Balanced panel: {df[ID].nunique()} hospitals × {len(YEARS)} years = {len(df)} obs")

# ══════════════════════════════════════════════════════════════════
# Compute Altman Z''-score
# ══════════════════════════════════════════════════════════════════
print("\n" + "=" * 60)
print("Computing Altman Z''-score")
print("=" * 60)

# X1 = Working Capital / Total Assets
df["working_capital"] = df[CURRENT_ASSETS] - df[CURRENT_LIAB]
df["X1"] = df["working_capital"] / df[TOTAL_ASSETS].replace(0, np.nan)

# X2 = Retained Earnings / Total Assets
df["X2"] = df[RETAINED_EARNINGS] / df[TOTAL_ASSETS].replace(0, np.nan)

# X3 = EBIT / Total Assets
df["X3"] = df[OPERATING_INCOME] / df[TOTAL_ASSETS].replace(0, np.nan)

# X4 = Book Value of Equity / Total Liabilities
df["X4"] = df[EQUITY] / df[TOTAL_LIAB].replace(0, np.nan)

# Z''-score formula
df["zscore"] = 6.56 * df["X1"] + 3.26 * df["X2"] + 6.72 * df["X3"] + 1.05 * df["X4"]
df["zscore_distress"] = (df["zscore"] < 1.1).astype(int)
df["deficit"] = (df[NET_INCOME] < 0).astype(int)

# ══════════════════════════════════════════════════════════════════
# Merge with Consensus Anomalies
# ══════════════════════════════════════════════════════════════════
print("\n" + "=" * 60)
print("Merging with Consensus Anomalies")
print("=" * 60)

# Create consensus anomaly flag from the CSV
consensus_set = set(zip(consensus_df[ID], consensus_df[YEAR]))
df["consensus_anomaly"] = df.apply(
    lambda row: 1 if (row[ID], row[YEAR]) in consensus_set else 0, axis=1
)

n_total = len(df)
n_distress = df["zscore_distress"].sum()
n_anomaly = df["consensus_anomaly"].sum()

print(f"\nTotal observations: {n_total}")
print(f"Z-score distress (Z'' < 1.1): {n_distress} ({n_distress/n_total*100:.1f}%)")
print(f"Consensus anomalies (≥3 algorithms): {n_anomaly} ({n_anomaly/n_total*100:.1f}%)")

# ══════════════════════════════════════════════════════════════════
# Overlap Analysis
# ══════════════════════════════════════════════════════════════════
print("\n" + "=" * 60)
print("Overlap Analysis: Z-score Distress vs Consensus Anomaly")
print("=" * 60)

# Four quadrants
both = ((df["zscore_distress"] == 1) & (df["consensus_anomaly"] == 1)).sum()
distress_only = ((df["zscore_distress"] == 1) & (df["consensus_anomaly"] == 0)).sum()
anomaly_only = ((df["zscore_distress"] == 0) & (df["consensus_anomaly"] == 1)).sum()
neither = ((df["zscore_distress"] == 0) & (df["consensus_anomaly"] == 0)).sum()

print(f"\n  Contingency Table:")
print(f"  {'':25s}  {'Anomaly=0':>12s}  {'Anomaly=1':>12s}")
print("  " + "-" * 52)
print(f"  {'Z-score Distress=0':25s}  {neither:12d}  {anomaly_only:12d}")
print(f"  {'Z-score Distress=1':25s}  {distress_only:12d}  {both:12d}")

print(f"\n  Overlap statistics:")
if n_distress > 0:
    pct_distress_also_anomaly = both / n_distress * 100
    print(f"  % of Z-score distressed also consensus anomaly: {pct_distress_also_anomaly:.1f}%")
if n_anomaly > 0:
    pct_anomaly_also_distress = both / n_anomaly * 100
    print(f"  % of consensus anomalies also Z-score distressed: {pct_anomaly_also_distress:.1f}%")

# Jaccard similarity
union = both + distress_only + anomaly_only
jaccard = both / union if union > 0 else 0
print(f"  Jaccard similarity (overlap / union): {jaccard:.3f}")

# ══════════════════════════════════════════════════════════════════
# Chi-squared Test
# ══════════════════════════════════════════════════════════════════
print("\n" + "=" * 60)
print("Chi-squared Test of Association")
print("=" * 60)

contingency = pd.crosstab(df["zscore_distress"], df["consensus_anomaly"])
chi2, p_chi, dof, expected = stats.chi2_contingency(contingency)

print(f"\n  Chi-squared statistic: {chi2:.2f}")
print(f"  Degrees of freedom: {dof}")
print(f"  p-value: {p_chi:.4f}")
print(f"  Significant at α=0.05: {'Yes' if p_chi < 0.05 else 'No'}")

# Phi coefficient (correlation for 2x2)
phi = np.sqrt(chi2 / n_total)
print(f"  Phi coefficient: {phi:.3f}")

# ══════════════════════════════════════════════════════════════════
# Additional Analysis: What makes them different?
# ══════════════════════════════════════════════════════════════════
print("\n" + "=" * 60)
print("Comparing Different Groups")
print("=" * 60)

# Group 1: Z-score distress only (not anomaly)
g1 = df[(df["zscore_distress"] == 1) & (df["consensus_anomaly"] == 0)]
# Group 2: Consensus anomaly only (not Z-score distress)
g2 = df[(df["zscore_distress"] == 0) & (df["consensus_anomaly"] == 1)]
# Group 3: Both
g3 = df[(df["zscore_distress"] == 1) & (df["consensus_anomaly"] == 1)]
# Group 4: Neither
g4 = df[(df["zscore_distress"] == 0) & (df["consensus_anomaly"] == 0)]

groups = {"Distress only": g1, "Anomaly only": g2, "Both": g3, "Neither": g4}

print(f"\n  Group characteristics (deficit rate):")
for name, grp in groups.items():
    if len(grp) > 0:
        deficit_rate = grp["deficit"].mean() * 100
        print(f"    {name:15s}: {len(grp):4d} obs, deficit rate = {deficit_rate:.1f}%")

# Z-score comparison by group
print(f"\n  Mean Z''-score by group:")
for name, grp in groups.items():
    if len(grp) > 0:
        mean_z = grp["zscore"].mean()
        print(f"    {name:15s}: mean Z'' = {mean_z:.2f}")

# ══════════════════════════════════════════════════════════════════
# Hospital Type Distribution
# ══════════════════════════════════════════════════════════════════
print("\n" + "=" * 60)
print("Hospital Type Distribution")
print("=" * 60)

print(f"\n  Z-score distress by establishment type:")
for etype in df[ETYPE].unique():
    subset = df[df[ETYPE] == etype]
    distress_rate = subset["zscore_distress"].mean() * 100
    print(f"    {etype:12s}: {distress_rate:.1f}%")

print(f"\n  Consensus anomaly by establishment type:")
for etype in df[ETYPE].unique():
    subset = df[df[ETYPE] == etype]
    anomaly_rate = subset["consensus_anomaly"].mean() * 100
    print(f"    {etype:12s}: {anomaly_rate:.1f}%")

# ══════════════════════════════════════════════════════════════════
# Key Finding: Complementary Nature
# ══════════════════════════════════════════════════════════════════
print("\n" + "=" * 60)
print("KEY FINDING: Complementary Detection")
print("=" * 60)

# Hospitals flagged by at least one method
union_flagged = df[(df["zscore_distress"] == 1) | (df["consensus_anomaly"] == 1)]
only_zscore = df[(df["zscore_distress"] == 1) & (df["consensus_anomaly"] == 0)]
only_anomaly = df[(df["zscore_distress"] == 0) & (df["consensus_anomaly"] == 1)]

print(f"\n  Total hospitals flagged by at least one method: {len(union_flagged)}")
print(f"  Flagged ONLY by Z-score (not anomaly): {len(only_zscore)} ({len(only_zscore)/len(union_flagged)*100:.1f}%)")
print(f"  Flagged ONLY by anomaly (not Z-score): {len(only_anomaly)} ({len(only_anomaly)/len(union_flagged)*100:.1f}%)")
print(f"  Flagged by BOTH methods: {both} ({both/len(union_flagged)*100:.1f}%)")

# Deficit rates in these groups
print(f"\n  Deficit rates among flagged groups:")
print(f"    Z-score only:  {only_zscore['deficit'].mean()*100:.1f}%")
print(f"    Anomaly only:  {only_anomaly['deficit'].mean()*100:.1f}%")
print(f"    Both:          {g3['deficit'].mean()*100:.1f}%")
print(f"    Neither:       {g4['deficit'].mean()*100:.1f}%")

# ══════════════════════════════════════════════════════════════════
# Save Results
# ══════════════════════════════════════════════════════════════════
results = {
    "zscore_statistics": {
        "mean": round(df["zscore"].mean(), 3),
        "std": round(df["zscore"].std(), 3),
        "distress_rate": round(n_distress / n_total * 100, 1),
    },
    "consensus_anomaly_rate": round(n_anomaly / n_total * 100, 1),
    "overlap": {
        "both": int(both),
        "distress_only": int(distress_only),
        "anomaly_only": int(anomaly_only),
        "neither": int(neither),
        "pct_distress_also_anomaly": round(both / n_distress * 100, 1) if n_distress > 0 else 0,
        "pct_anomaly_also_distress": round(both / n_anomaly * 100, 1) if n_anomaly > 0 else 0,
        "jaccard_similarity": round(jaccard, 3),
    },
    "chi_squared_test": {
        "chi2": round(chi2, 2),
        "p_value": round(p_chi, 4),
        "dof": int(dof),
        "phi_coefficient": round(phi, 3),
        "significant": bool(p_chi < 0.05),
    },
    "deficit_rates_by_group": {
        "distress_only": round(g1["deficit"].mean() * 100, 1) if len(g1) > 0 else None,
        "anomaly_only": round(g2["deficit"].mean() * 100, 1) if len(g2) > 0 else None,
        "both": round(g3["deficit"].mean() * 100, 1) if len(g3) > 0 else None,
        "neither": round(g4["deficit"].mean() * 100, 1) if len(g4) > 0 else None,
    },
    "complementary_detection": {
        "total_flagged": int(len(union_flagged)),
        "only_zscore": int(len(only_zscore)),
        "only_anomaly": int(len(only_anomaly)),
        "both": int(both),
    },
}

with open(OUTPUT_PATH, "w") as f:
    json.dump(results, f, indent=2)
print(f"\n  Results saved to: {OUTPUT_PATH}")

print("\n" + "=" * 60)
print("DONE")
print("=" * 60)
