#!/usr/bin/env python3
"""
01_anomaly_detection.py
Unsupervised Anomaly Detection in Hospital Financial Statements

Algorithms:
  1. Isolation Forest
  2. Local Outlier Factor (LOF)
  3. One-Class SVM
  4. DBSCAN (eps auto-tuned via k-distance)
  5. Autoencoder (sklearn MLPRegressor-based reconstruction error)

Analyses:
  - Per-algorithm anomaly rates & overlap
  - Consensus anomaly (≥3 algorithms agree)
  - Anomaly vs Normal financial characteristics (Mann-Whitney U)
  - Temporal pattern (COVID-era shift)
  - SHAP on Isolation Forest
  - Hospital-type distribution of anomalies
  - Overlap with supervised deficit labels
"""

import pandas as pd
import numpy as np
import os
import json
import warnings
warnings.filterwarnings("ignore")

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
from scipy import stats
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import IsolationForest
from sklearn.neighbors import LocalOutlierFactor, NearestNeighbors
from sklearn.svm import OneClassSVM
from sklearn.cluster import DBSCAN
from sklearn.neural_network import MLPRegressor

# ── Paths ──────────────────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.join(BASE_DIR, "..")
DATA_PATH = "/Users/yongjun_kim/Documents/project_hospital/data/hospital_all_clean.pkl"
FIG_DIR = os.path.join(PROJECT_DIR, "figures")
os.makedirs(FIG_DIR, exist_ok=True)

# ── Load Data ──────────────────────────────────────────────────────
df = pd.read_pickle(DATA_PATH)

YEAR = "회계연도"
ID = "요양기관번호"
NAME = "요양기관명"
MED_REV = "Ⅰ.의료수익"
MED_COST = "Ⅱ.의료비용"
LABOR = "    1.인건비"
MATERIAL = "    2.재료비"
ADMIN = "    3.관리운영비"
NET_INCOME = "    당기순이익(순손실)"
DONATION = "    13.기부금수익"
TOTAL_ASSETS = "자산총계"
TOTAL_LIAB = "부채총계"
NON_MED_REV = "Ⅳ.의료외수익"
BEDS = "병상수"
HTYPE = "종별"
ETYPE = "설립형태"

for col in [MED_REV, MED_COST, LABOR, MATERIAL, ADMIN, NET_INCOME,
            DONATION, TOTAL_ASSETS, TOTAL_LIAB, NON_MED_REV, BEDS]:
    df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

# ── Filter to balanced panel (2019-2023) ───────────────────────────
YEARS = [2019, 2020, 2021, 2022, 2023]
HOSPITAL_TYPES = ["상급종합병원", "종합병원"]
df = df[df[HTYPE].isin(HOSPITAL_TYPES) & df[YEAR].isin(YEARS)]
panel_ids = df.groupby(ID)[YEAR].nunique()
panel_ids = panel_ids[panel_ids == 5].index
df = df[df[ID].isin(panel_ids)].copy()

print(f"Balanced panel: {df[ID].nunique()} hospitals × {len(YEARS)} years = {len(df)} obs")

# ── Feature Engineering (11 features) ─────────────────────────────
df["deficit"] = (df[NET_INCOME] < 0).astype(int)
df["material_ratio"] = df[MATERIAL] / df[MED_REV].replace(0, np.nan)
df["labor_ratio"] = df[LABOR] / df[MED_REV].replace(0, np.nan)
df["admin_ratio"] = df[ADMIN] / df[MED_REV].replace(0, np.nan)
df["total_revenue"] = df[MED_REV] + df[NON_MED_REV].clip(lower=0)
df["subsidy_ratio"] = df[DONATION] / df["total_revenue"].replace(0, np.nan)
df["debt_ratio"] = df[TOTAL_LIAB] / df[TOTAL_ASSETS].replace(0, np.nan)
df["year_feat"] = df[YEAR] - 2019
df["log_revenue"] = np.log(df[MED_REV].clip(lower=1))
df["log_beds"] = np.log(df[BEDS].clip(lower=1))
df["is_university"] = (df[ETYPE] == "학교법인").astype(int)
df["is_public"] = (df[ETYPE] == "공립").astype(int)
df["is_tertiary"] = (df[HTYPE] == "상급종합병원").astype(int)

FEATURE_COLS = [
    "material_ratio", "labor_ratio", "admin_ratio", "debt_ratio",
    "subsidy_ratio", "log_revenue", "log_beds",
    "is_university", "is_public", "is_tertiary", "year_feat",
]
FEATURE_NAMES = [
    "Material Cost Ratio", "Labor Cost Ratio", "Admin Cost Ratio",
    "Debt Ratio", "Subsidy Ratio", "Log Revenue", "Log Beds",
    "University Hospital", "Public Hospital", "Tertiary Hospital", "Year",
]

df_ml = df[[ID, NAME, YEAR, HTYPE, ETYPE, "deficit"] + FEATURE_COLS].dropna().copy()
X = df_ml[FEATURE_COLS].values.copy()

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

print(f"Analysis dataset: {X.shape[0]} obs, {X.shape[1]} features")
print(f"Deficit rate: {df_ml['deficit'].mean()*100:.1f}%\n")

# ══════════════════════════════════════════════════════════════════
# ALGORITHM 1: Isolation Forest
# ══════════════════════════════════════════════════════════════════
print("=" * 60)
print("1. Isolation Forest")
print("=" * 60)

iso = IsolationForest(contamination=0.1, random_state=42, n_estimators=200)
iso.fit(X_scaled)
df_ml["iso_score"] = iso.decision_function(X_scaled)
df_ml["iso_anomaly"] = (iso.predict(X_scaled) == -1).astype(int)
print(f"   Anomalies: {df_ml['iso_anomaly'].sum()} ({df_ml['iso_anomaly'].mean()*100:.1f}%)")

# ══════════════════════════════════════════════════════════════════
# ALGORITHM 2: Local Outlier Factor
# ══════════════════════════════════════════════════════════════════
print("\n" + "=" * 60)
print("2. Local Outlier Factor (LOF)")
print("=" * 60)

lof = LocalOutlierFactor(n_neighbors=20, contamination=0.1)
lof_labels = lof.fit_predict(X_scaled)
df_ml["lof_score"] = -lof.negative_outlier_factor_
df_ml["lof_anomaly"] = (lof_labels == -1).astype(int)
print(f"   Anomalies: {df_ml['lof_anomaly'].sum()} ({df_ml['lof_anomaly'].mean()*100:.1f}%)")

# ══════════════════════════════════════════════════════════════════
# ALGORITHM 3: One-Class SVM
# ══════════════════════════════════════════════════════════════════
print("\n" + "=" * 60)
print("3. One-Class SVM")
print("=" * 60)

ocsvm = OneClassSVM(nu=0.1, kernel="rbf", gamma="scale")
ocsvm.fit(X_scaled)
df_ml["svm_score"] = -ocsvm.decision_function(X_scaled)
df_ml["svm_anomaly"] = (ocsvm.predict(X_scaled) == -1).astype(int)
print(f"   Anomalies: {df_ml['svm_anomaly'].sum()} ({df_ml['svm_anomaly'].mean()*100:.1f}%)")

# ══════════════════════════════════════════════════════════════════
# ALGORITHM 4: DBSCAN (auto eps via k-distance)
# ══════════════════════════════════════════════════════════════════
print("\n" + "=" * 60)
print("4. DBSCAN (auto-tuned eps)")
print("=" * 60)

min_samples = 5
nn = NearestNeighbors(n_neighbors=min_samples)
nn.fit(X_scaled)
distances, _ = nn.kneighbors(X_scaled)
k_distances = np.sort(distances[:, -1])

# Use the "knee" heuristic: pick eps at the 90th percentile of k-distances
eps_auto = np.percentile(k_distances, 90)
print(f"   Auto eps (90th pctile k-dist): {eps_auto:.3f}")

dbscan = DBSCAN(eps=eps_auto, min_samples=min_samples)
db_labels = dbscan.fit_predict(X_scaled)
df_ml["dbscan_anomaly"] = (db_labels == -1).astype(int)
n_clusters = len(set(db_labels) - {-1})
print(f"   Clusters found: {n_clusters}")
print(f"   Anomalies (noise): {df_ml['dbscan_anomaly'].sum()} ({df_ml['dbscan_anomaly'].mean()*100:.1f}%)")

# ══════════════════════════════════════════════════════════════════
# ALGORITHM 5: Autoencoder (MLPRegressor reconstruction error)
# ══════════════════════════════════════════════════════════════════
print("\n" + "=" * 60)
print("5. Autoencoder (MLPRegressor)")
print("=" * 60)

# Train an autoencoder: input → bottleneck → output (identity mapping)
ae = MLPRegressor(
    hidden_layer_sizes=(8, 4, 8),  # encoder-bottleneck-decoder
    activation="relu",
    solver="adam",
    max_iter=500,
    random_state=42,
    early_stopping=True,
    validation_fraction=0.1,
    learning_rate_init=0.001,
)
ae.fit(X_scaled, X_scaled)  # reconstruct input
X_reconstructed = ae.predict(X_scaled)
recon_error = np.mean((X_scaled - X_reconstructed) ** 2, axis=1)
df_ml["ae_score"] = recon_error

# Use 90th percentile of reconstruction error as threshold
ae_threshold = np.percentile(recon_error, 90)
df_ml["ae_anomaly"] = (recon_error > ae_threshold).astype(int)
print(f"   Reconstruction error threshold (90th pctile): {ae_threshold:.4f}")
print(f"   Anomalies: {df_ml['ae_anomaly'].sum()} ({df_ml['ae_anomaly'].mean()*100:.1f}%)")

# ══════════════════════════════════════════════════════════════════
# ANALYSIS 1: Anomaly rates & overlap
# ══════════════════════════════════════════════════════════════════
print("\n" + "=" * 60)
print("ANALYSIS 1: Algorithm Overlap")
print("=" * 60)

algo_cols = ["iso_anomaly", "lof_anomaly", "svm_anomaly", "dbscan_anomaly", "ae_anomaly"]
algo_names = ["IF", "LOF", "OCSVM", "DBSCAN", "AE"]

df_ml["n_algorithms"] = df_ml[algo_cols].sum(axis=1)
df_ml["consensus_anomaly"] = (df_ml["n_algorithms"] >= 3).astype(int)

print(f"\n   Anomaly count distribution:")
for k in range(6):
    cnt = (df_ml["n_algorithms"] == k).sum()
    pct = cnt / len(df_ml) * 100
    print(f"     Flagged by {k} algorithms: {cnt} ({pct:.1f}%)")

print(f"\n   Consensus anomalies (≥3): {df_ml['consensus_anomaly'].sum()} "
      f"({df_ml['consensus_anomaly'].mean()*100:.1f}%)")

# Pairwise overlap (Jaccard similarity)
from itertools import combinations
print(f"\n   Pairwise Jaccard similarity:")
jaccard_matrix = np.zeros((5, 5))
for i in range(5):
    for j in range(5):
        a = set(df_ml.index[df_ml[algo_cols[i]] == 1])
        b = set(df_ml.index[df_ml[algo_cols[j]] == 1])
        if len(a | b) > 0:
            jaccard_matrix[i, j] = len(a & b) / len(a | b)
        else:
            jaccard_matrix[i, j] = 0

for i, j in combinations(range(5), 2):
    print(f"     {algo_names[i]:7s} ∩ {algo_names[j]:7s}: Jaccard = {jaccard_matrix[i,j]:.3f}")

# ══════════════════════════════════════════════════════════════════
# ANALYSIS 2: Anomaly vs Normal — Financial Characteristics
# ══════════════════════════════════════════════════════════════════
print("\n" + "=" * 60)
print("ANALYSIS 2: Consensus Anomaly vs Normal (Mann-Whitney U)")
print("=" * 60)

anomaly_mask = df_ml["consensus_anomaly"] == 1
normal_mask = df_ml["consensus_anomaly"] == 0

stats_results = []
print(f"\n   {'Feature':25s}  {'Normal':>10s}  {'Anomaly':>10s}  {'U-stat':>10s}  {'p-value':>10s}  {'Sig':>4s}")
print("   " + "-" * 75)

for fc, fn in zip(FEATURE_COLS, FEATURE_NAMES):
    vals_normal = df_ml.loc[normal_mask, fc].values
    vals_anomaly = df_ml.loc[anomaly_mask, fc].values
    u_stat, p_val = stats.mannwhitneyu(vals_anomaly, vals_normal, alternative="two-sided")
    sig = "***" if p_val < 0.001 else "**" if p_val < 0.01 else "*" if p_val < 0.05 else ""
    mean_n = np.mean(vals_normal)
    mean_a = np.mean(vals_anomaly)
    print(f"   {fn:25s}  {mean_n:10.4f}  {mean_a:10.4f}  {u_stat:10.0f}  {p_val:10.4f}  {sig:>4s}")
    stats_results.append({
        "feature": fn, "mean_normal": round(mean_n, 4), "mean_anomaly": round(mean_a, 4),
        "u_stat": round(u_stat, 1), "p_value": round(p_val, 4), "significant": sig != ""
    })

# ══════════════════════════════════════════════════════════════════
# ANALYSIS 3: Temporal Pattern (COVID era)
# ══════════════════════════════════════════════════════════════════
print("\n" + "=" * 60)
print("ANALYSIS 3: Temporal Anomaly Pattern")
print("=" * 60)

temporal_data = []
for yr in YEARS:
    yr_mask = df_ml[YEAR] == yr
    n_total = yr_mask.sum()
    for ac, an in zip(algo_cols, algo_names):
        n_anom = df_ml.loc[yr_mask, ac].sum()
        temporal_data.append({"year": yr, "algorithm": an, "n_anomaly": int(n_anom),
                              "rate": n_anom / n_total * 100 if n_total > 0 else 0})
    n_cons = df_ml.loc[yr_mask, "consensus_anomaly"].sum()
    temporal_data.append({"year": yr, "algorithm": "Consensus", "n_anomaly": int(n_cons),
                          "rate": n_cons / n_total * 100 if n_total > 0 else 0})

temporal_df = pd.DataFrame(temporal_data)
print("\n   Year-by-year consensus anomaly rate:")
for yr in YEARS:
    row = temporal_df[(temporal_df["year"] == yr) & (temporal_df["algorithm"] == "Consensus")]
    print(f"     {yr}: {row['n_anomaly'].values[0]} anomalies ({row['rate'].values[0]:.1f}%)")

# Pre/Post COVID comparison
pre_covid = df_ml[df_ml[YEAR] == 2019]["consensus_anomaly"].mean()
post_covid = df_ml[df_ml[YEAR].isin([2020, 2021])]["consensus_anomaly"].mean()
post_recovery = df_ml[df_ml[YEAR].isin([2022, 2023])]["consensus_anomaly"].mean()
print(f"\n   Pre-COVID (2019): {pre_covid*100:.1f}%")
print(f"   COVID peak (2020-2021): {post_covid*100:.1f}%")
print(f"   Recovery (2022-2023): {post_recovery*100:.1f}%")

# ══════════════════════════════════════════════════════════════════
# ANALYSIS 4: SHAP on Isolation Forest
# ══════════════════════════════════════════════════════════════════
print("\n" + "=" * 60)
print("ANALYSIS 4: SHAP on Isolation Forest")
print("=" * 60)

try:
    import shap

    explainer = shap.TreeExplainer(iso)
    shap_values = explainer.shap_values(X_scaled)

    mean_abs_shap = np.abs(shap_values).mean(axis=0)
    shap_order = np.argsort(-mean_abs_shap)

    print(f"\n   Feature importance (mean |SHAP|):")
    for idx in shap_order:
        print(f"     {FEATURE_NAMES[idx]:25s}: {mean_abs_shap[idx]:.4f}")

    has_shap = True
except ImportError:
    print("   shap not installed; skipping SHAP analysis.")
    has_shap = False

# ══════════════════════════════════════════════════════════════════
# ANALYSIS 5: Hospital Type Distribution
# ══════════════════════════════════════════════════════════════════
print("\n" + "=" * 60)
print("ANALYSIS 5: Anomaly by Hospital Type")
print("=" * 60)

print("\n   By Establishment Type (설립형태):")
etype_stats = df_ml.groupby(ETYPE).agg(
    total=("consensus_anomaly", "count"),
    anomalies=("consensus_anomaly", "sum")
).assign(rate=lambda x: x["anomalies"] / x["total"] * 100)
for etype, row in etype_stats.iterrows():
    print(f"     {etype:12s}: {row['anomalies']:.0f}/{row['total']:.0f} ({row['rate']:.1f}%)")

print("\n   By Hospital Grade (종별):")
htype_stats = df_ml.groupby(HTYPE).agg(
    total=("consensus_anomaly", "count"),
    anomalies=("consensus_anomaly", "sum")
).assign(rate=lambda x: x["anomalies"] / x["total"] * 100)
for htype, row in htype_stats.iterrows():
    print(f"     {htype:12s}: {row['anomalies']:.0f}/{row['total']:.0f} ({row['rate']:.1f}%)")

# ══════════════════════════════════════════════════════════════════
# ANALYSIS 6: Overlap with Supervised Deficit Labels
# ══════════════════════════════════════════════════════════════════
print("\n" + "=" * 60)
print("ANALYSIS 6: Anomaly vs Deficit Overlap")
print("=" * 60)

n_deficit = df_ml["deficit"].sum()
n_anomaly = df_ml["consensus_anomaly"].sum()
n_both = ((df_ml["deficit"] == 1) & (df_ml["consensus_anomaly"] == 1)).sum()
n_deficit_only = ((df_ml["deficit"] == 1) & (df_ml["consensus_anomaly"] == 0)).sum()
n_anomaly_only = ((df_ml["deficit"] == 0) & (df_ml["consensus_anomaly"] == 1)).sum()

print(f"\n   Deficit hospitals: {n_deficit}")
print(f"   Consensus anomalies: {n_anomaly}")
print(f"   Both (deficit + anomaly): {n_both}")
print(f"   Deficit only (not anomaly): {n_deficit_only}")
print(f"   Anomaly only (not deficit): {n_anomaly_only}")
if n_deficit > 0:
    print(f"\n   % of deficit hospitals flagged as anomaly: {n_both/n_deficit*100:.1f}%")
if n_anomaly > 0:
    print(f"   % of anomalies that are in deficit: {n_both/n_anomaly*100:.1f}%")

# Chi-squared test
contingency = pd.crosstab(df_ml["deficit"], df_ml["consensus_anomaly"])
chi2, p_chi, dof, expected = stats.chi2_contingency(contingency)
print(f"\n   Chi-squared test: χ²={chi2:.2f}, p={p_chi:.4f}")

# Per-algorithm overlap with deficit
print(f"\n   Per-algorithm overlap with deficit:")
for ac, an in zip(algo_cols, algo_names):
    overlap = ((df_ml["deficit"] == 1) & (df_ml[ac] == 1)).sum()
    total_anom = df_ml[ac].sum()
    deficit_in_anom = overlap / total_anom * 100 if total_anom > 0 else 0
    print(f"     {an:7s}: {overlap}/{total_anom} anomalies are in deficit ({deficit_in_anom:.1f}%)")

# ══════════════════════════════════════════════════════════════════
# FIGURES
# ══════════════════════════════════════════════════════════════════
print("\n" + "=" * 60)
print("GENERATING FIGURES")
print("=" * 60)

plt.rcParams.update({
    "font.size": 10,
    "axes.titlesize": 12,
    "axes.labelsize": 11,
    "figure.dpi": 150,
})

# ── Figure 1: Anomaly Score Distributions ──
fig, axes = plt.subplots(2, 3, figsize=(14, 8))

# IF scores
ax = axes[0, 0]
ax.hist(df_ml["iso_score"], bins=50, color="#3498db", alpha=0.7, edgecolor="white")
ax.axvline(x=df_ml.loc[df_ml["iso_anomaly"]==1, "iso_score"].max(), color="red",
           linestyle="--", label="Threshold")
ax.set_title("(a) Isolation Forest")
ax.set_xlabel("Anomaly Score")
ax.set_ylabel("Frequency")
ax.legend()

# LOF scores
ax = axes[0, 1]
ax.hist(df_ml["lof_score"], bins=50, color="#e74c3c", alpha=0.7, edgecolor="white")
ax.set_title("(b) Local Outlier Factor")
ax.set_xlabel("LOF Score")
ax.set_ylabel("Frequency")

# SVM scores
ax = axes[0, 2]
ax.hist(df_ml["svm_score"], bins=50, color="#2ecc71", alpha=0.7, edgecolor="white")
ax.set_title("(c) One-Class SVM")
ax.set_xlabel("Distance to Boundary")
ax.set_ylabel("Frequency")

# AE scores
ax = axes[1, 0]
ax.hist(df_ml["ae_score"], bins=50, color="#9b59b6", alpha=0.7, edgecolor="white")
ax.axvline(x=ae_threshold, color="red", linestyle="--", label="Threshold (90th)")
ax.set_title("(d) Autoencoder")
ax.set_xlabel("Reconstruction Error")
ax.set_ylabel("Frequency")
ax.legend()

# Consensus count distribution
ax = axes[1, 1]
counts = [int((df_ml["n_algorithms"] == k).sum()) for k in range(6)]
colors = ["#95a5a6", "#bdc3c7", "#f39c12", "#e74c3c", "#c0392b", "#8e44ad"]
bars = ax.bar(range(6), counts, color=colors, edgecolor="white")
ax.set_xlabel("Number of Algorithms Agreeing")
ax.set_ylabel("Count")
ax.set_title("(e) Consensus Distribution")
ax.set_xticks(range(6))
for bar, count in zip(bars, counts):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 5,
            str(count), ha="center", va="bottom", fontsize=9)

# Anomaly vs Normal boxplot for top feature
ax = axes[1, 2]
if has_shap:
    top_feat_idx = shap_order[0]
else:
    top_feat_idx = 0  # material_ratio
top_feat = FEATURE_COLS[top_feat_idx]
top_feat_name = FEATURE_NAMES[top_feat_idx]
data_plot = [df_ml.loc[normal_mask, top_feat].values, df_ml.loc[anomaly_mask, top_feat].values]
bp = ax.boxplot(data_plot, labels=["Normal", "Anomaly"], patch_artist=True,
                boxprops=dict(facecolor="#3498db", alpha=0.6),
                medianprops=dict(color="red"))
bp["boxes"][1].set_facecolor("#e74c3c")
ax.set_title(f"(f) {top_feat_name}")
ax.set_ylabel("Value")

plt.tight_layout()
plt.savefig(os.path.join(FIG_DIR, "fig_anomaly_scores.png"), dpi=300, bbox_inches="tight")
plt.close()
print("   Saved: fig_anomaly_scores.png")

# ── Figure 2: Consensus Heatmap (Jaccard matrix) ──
fig, ax = plt.subplots(figsize=(7, 6))
mask = np.zeros_like(jaccard_matrix, dtype=bool)
# np.fill_diagonal(mask, True)  # keep diagonal visible
sns.heatmap(jaccard_matrix, annot=True, fmt=".2f", cmap="YlOrRd",
            xticklabels=algo_names, yticklabels=algo_names,
            vmin=0, vmax=1, ax=ax, linewidths=0.5,
            cbar_kws={"label": "Jaccard Similarity"})
ax.set_title("Algorithm Agreement: Pairwise Jaccard Similarity", fontsize=12, fontweight="bold")
plt.tight_layout()
plt.savefig(os.path.join(FIG_DIR, "fig_consensus_heatmap.png"), dpi=300, bbox_inches="tight")
plt.close()
print("   Saved: fig_consensus_heatmap.png")

# ── Figure 3: Temporal Anomaly Pattern ──
fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# (a) Per-algorithm anomaly rate by year
ax = axes[0]
for an in algo_names:
    subset = temporal_df[temporal_df["algorithm"] == an]
    ax.plot(subset["year"], subset["rate"], marker="o", label=an, linewidth=1.5)
ax.axvspan(2020, 2021, alpha=0.1, color="red", label="COVID peak")
ax.set_xlabel("Year")
ax.set_ylabel("Anomaly Rate (%)")
ax.set_title("(a) Per-Algorithm Anomaly Rate by Year")
ax.legend(fontsize=8, ncol=2)
ax.set_xticks(YEARS)

# (b) Consensus anomaly rate by year
ax = axes[1]
cons_temporal = temporal_df[temporal_df["algorithm"] == "Consensus"]
ax.bar(cons_temporal["year"], cons_temporal["rate"], color="#e74c3c", alpha=0.7, edgecolor="white")
ax.axvspan(2019.5, 2021.5, alpha=0.1, color="red")
ax.set_xlabel("Year")
ax.set_ylabel("Consensus Anomaly Rate (%)")
ax.set_title("(b) Consensus Anomaly Rate (≥3 Algorithms)")
ax.set_xticks(YEARS)
for i, row in cons_temporal.iterrows():
    ax.text(row["year"], row["rate"] + 0.3, f'{row["rate"]:.1f}%', ha="center", fontsize=9)

plt.tight_layout()
plt.savefig(os.path.join(FIG_DIR, "fig_anomaly_temporal.png"), dpi=300, bbox_inches="tight")
plt.close()
print("   Saved: fig_anomaly_temporal.png")

# ── Figure 4: SHAP on Isolation Forest ──
if has_shap:
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    # (a) SHAP bar chart
    ax = axes[0]
    sorted_idx = np.argsort(mean_abs_shap)
    ax.barh(range(len(FEATURE_NAMES)), mean_abs_shap[sorted_idx], color="#3498db")
    ax.set_yticks(range(len(FEATURE_NAMES)))
    ax.set_yticklabels([FEATURE_NAMES[i] for i in sorted_idx], fontsize=9)
    ax.set_xlabel("Mean |SHAP value|")
    ax.set_title("(a) Feature Importance (Isolation Forest)")

    # (b) SHAP beeswarm
    ax = axes[1]
    X_df = pd.DataFrame(X_scaled, columns=FEATURE_NAMES)
    plt.sca(ax)
    shap.summary_plot(shap_values, X_df, show=False, max_display=11)
    ax.set_title("(b) SHAP Value Distribution")

    plt.tight_layout()
    plt.savefig(os.path.join(FIG_DIR, "fig_shap_anomaly.png"), dpi=300, bbox_inches="tight")
    plt.close()
    print("   Saved: fig_shap_anomaly.png")

# ── Figure 5 (Bonus): Anomaly by Hospital Type ──
fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# (a) By establishment type
ax = axes[0]
etype_sorted = etype_stats.sort_values("rate", ascending=True)
ax.barh(etype_sorted.index, etype_sorted["rate"], color="#3498db", alpha=0.7)
ax.set_xlabel("Consensus Anomaly Rate (%)")
ax.set_title("(a) By Establishment Type")
for i, (idx, row) in enumerate(etype_sorted.iterrows()):
    ax.text(row["rate"] + 0.3, i, f'{row["anomalies"]:.0f}/{row["total"]:.0f}', va="center", fontsize=8)

# (b) By hospital grade
ax = axes[1]
htype_sorted = htype_stats.sort_values("rate", ascending=True)
ax.barh(htype_sorted.index, htype_sorted["rate"], color="#e74c3c", alpha=0.7)
ax.set_xlabel("Consensus Anomaly Rate (%)")
ax.set_title("(b) By Hospital Grade")
for i, (idx, row) in enumerate(htype_sorted.iterrows()):
    ax.text(row["rate"] + 0.3, i, f'{row["anomalies"]:.0f}/{row["total"]:.0f}', va="center", fontsize=8)

plt.tight_layout()
plt.savefig(os.path.join(FIG_DIR, "fig_anomaly_types.png"), dpi=300, bbox_inches="tight")
plt.close()
print("   Saved: fig_anomaly_types.png")

# ══════════════════════════════════════════════════════════════════
# SAVE RESULTS
# ══════════════════════════════════════════════════════════════════
results = {
    "dataset": {
        "n_hospitals": int(df_ml[ID].nunique()),
        "n_obs": int(len(df_ml)),
        "years": YEARS,
        "deficit_rate": round(df_ml["deficit"].mean() * 100, 1),
    },
    "algorithm_anomaly_rates": {
        an: round(df_ml[ac].mean() * 100, 1)
        for ac, an in zip(algo_cols, algo_names)
    },
    "consensus": {
        "n_anomalies": int(df_ml["consensus_anomaly"].sum()),
        "rate": round(df_ml["consensus_anomaly"].mean() * 100, 1),
    },
    "temporal_consensus": {
        str(yr): round(temporal_df[(temporal_df["year"]==yr) & (temporal_df["algorithm"]=="Consensus")]["rate"].values[0], 1)
        for yr in YEARS
    },
    "deficit_overlap": {
        "n_deficit": int(n_deficit),
        "n_anomaly": int(n_anomaly),
        "n_both": int(n_both),
        "pct_deficit_flagged": round(n_both/n_deficit*100, 1) if n_deficit > 0 else 0,
        "pct_anomaly_in_deficit": round(n_both/n_anomaly*100, 1) if n_anomaly > 0 else 0,
        "chi2": round(chi2, 2),
        "chi2_p": round(p_chi, 4),
    },
    "mann_whitney_results": stats_results,
    "jaccard_matrix": jaccard_matrix.tolist(),
}

if has_shap:
    results["shap_importance"] = {
        FEATURE_NAMES[i]: round(float(mean_abs_shap[i]), 4) for i in shap_order
    }

out_path = os.path.join(PROJECT_DIR, "code", "anomaly_results.json")
with open(out_path, "w") as f:
    json.dump(results, f, indent=2, ensure_ascii=False)
print(f"\n   Results saved to: {out_path}")

# Save consensus anomaly list
anomaly_list = df_ml[df_ml["consensus_anomaly"] == 1][[NAME, ID, YEAR, HTYPE, ETYPE, "deficit", "n_algorithms"]].copy()
anomaly_list.to_csv(os.path.join(PROJECT_DIR, "code", "consensus_anomalies.csv"), index=False, encoding="utf-8-sig")
print(f"   Consensus anomaly list saved: consensus_anomalies.csv")

print("\n" + "=" * 60)
print("ALL DONE!")
print("=" * 60)
