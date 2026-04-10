# Revision TODO — Paper 1: Unsupervised Anomaly Detection

Extracted from `~/Documents/BRUTAL_REVIEW.md` (2026-04-05).
**Verdict:** MAJOR REVISION (borderline REJECT).

This is a working checklist for the next revision round. Each item has a **claim under attack**, the **action required**, and an **effort estimate** so you can triage.

---

## 🔴 Fatal flaws (must address before resubmit)

### F1. 3/5 consensus threshold is unjustified
- **Under attack:** "An observation is classified as a consensus anomaly if $C_i \geq 3$"
- **Action:**
  - Add full sensitivity sweep: report results at thresholds 2/5, 3/5, 4/5 (quantitative comparison)
  - Add weighted voting variant (by per-algorithm confidence / reconstruction error)
  - Principled justification: either empirical (AUC-like metric vs external validation) or theoretical (error-rate bound)
- **Effort:** 2–3 days. Mostly re-running existing pipeline with different thresholds.
- **Priority:** P0

### F2. "Label-free" claim is false
- **Under attack:** contamination=0.1, DBSCAN ε at 90th percentile, validation against deficit labels
- **Action options (pick one):**
  - (a) Drop "label-free" framing entirely. Rebrand as semi-supervised / weakly-supervised
  - (b) Keep unsupervised framing but run ablation: what happens with contamination=auto, contamination=0.05, contamination=0.15? Show consensus is stable
  - (c) Honest comparison to fully supervised baseline (e.g., logistic regression on deficit label) — show your method works when labels aren't available
- **Effort:** 1 day for writing; 2 days if running (b) or (c)
- **Priority:** P0

### F3. Circular validation
- **Under attack:** Anomalies found to have unusual features; "validated" by showing they have unusual feature values
- **Action:**
  - Add **external validation**: were any of the 57 anomaly hospitals actually investigated, closed, or flagged by MOHW? Check Korean news archives, KHIDI announcements.
  - Or: validate against FUTURE data — if you add 2024 data, do the 2019-2023 anomalies have higher closure/restructuring rates?
  - Address the $\chi^2 = 0.67$ non-correlation honestly: either your anomalies capture a different signal than deficits (then what signal?), or you're capturing noise.
- **Effort:** 3–5 days (requires new data gathering)
- **Priority:** P0

### F4. Public hospital confound
- **Under attack:** 54.4% of anomalies are public hospitals (vs 23.3% baseline); SHAP says ownership is #1 driver
- **Action:**
  - Run analysis **stratified by ownership**: does anomaly detection still find meaningful outliers WITHIN public hospitals alone? Within private alone?
  - Compare with a trivial baseline: "flag all public hospitals" — show your method does better (or admit it doesn't and pivot the contribution)
  - Be explicit about what remains after controlling for ownership
- **Effort:** 2 days
- **Priority:** P0

---

## 🟠 Statistical sins

### S1. Multiple comparison problem (Table 3)
- 11 Mann-Whitney tests; Bonferroni mentioned but adjusted p-values not shown
- **Action:** Report both raw and Bonferroni-adjusted p-values explicitly; only discuss features that survive correction
- **Effort:** 2 hours

### S2. No confidence intervals
- Anomaly rate 6.9% reported without CI; "6.1% → 8.5%" temporal trend has no trend test
- **Action:**
  - Bootstrap 95% CI for all reported rates
  - Cochran-Armitage trend test or Mann-Kendall for temporal claim
- **Effort:** 4 hours

### S3. Contamination self-fulfilling
- contamination=0.1 mechanically forces ~10% anomaly rate
- **Action:** Cover this in F2 response. Add explicit sensitivity to contamination in {0.05, 0.1, 0.15}
- **Effort:** 0 (merged with F2)

### S4. Small sample subgroups
- National: n=5 (40% anomaly = 2 hospitals), Social welfare: n=10, Foundation: n=50
- **Action:** Either merge small subgroups or drop them from the subgroup analysis. State minimum n threshold explicitly.
- **Effort:** 1 hour

### S5. Autoencoder details missing
- Architecture 11→8→4→8→11 unjustified; no train/val split; reconstruction threshold arbitrary
- **Action:**
  - Justify architecture (or tune with held-out validation)
  - Report train/val loss curves in supplementary
  - Sensitivity to 90th/85th/95th percentile threshold
- **Effort:** 1 day

---

## 🟡 Writing fixes (cheap wins)

### W1. Strip overclaiming language
- Remove "propose multi-algorithm consensus framework" → "apply multi-algorithm consensus"
- Remove "offering a complementary surveillance tool" unless you can cite a regulator using it
- Replace "novel" where contribution is application

### W2. Add missing related work
- Altman Z-score and financial distress literature (Lord 2020, Holmes 2017, Langabeer 2018)
- Explain why unsupervised > supervised for this task (or why not)

### W3. Section VI.E contradiction
- "anomaly does not carry a negative connotation" contradicts "surveillance tool" framing
- **Action:** Pick one framing and be consistent. Either it's a surveillance tool (and anomalies are bad) or a structural characterization tool (and drop surveillance language).

---

## 🟢 Reproducibility

### R1. Data description mismatches
- 827 observations claimed but 165×5=825 — explain the 2 extras
- "minor missing observations" not explained
- Feature selection 236→11 not transparent

### R2. Random seeds
- Specify for ALL algorithms (IF, LOF, OCSVM, autoencoder, DBSCAN)

### R3. Ethics
- Section V names specific hospitals (National Medical Center etc.) — was IRB obtained for identification? If not, anonymize or get approval retroactively.

---

## 🔵 Impact ("So what?")

To convert LOW practical impact → publishable impact, add at least one of:
- [ ] Forward prediction on 2024 data (any of your 57 anomalies actually hit trouble?)
- [ ] Comparison with simple rule-based alternatives (e.g., labor cost ratio > 0.8)
- [ ] Economic analysis: cost of surveillance vs benefit of early detection
- [ ] Validated lead time for early warning

---

## 💣 The 10 embarrassing questions (dry-run defense)

Prepare 1-paragraph answers to these before submission. If you can't answer confidently, that section of the paper isn't ready:

1. Why is 3/5 the magic threshold? → **F1**
2. How is contamination=0.1 different from assuming 10% anomaly rate? → **F2**
3. If public hospitals differ structurally, aren't you just detecting "public-ness"? → **F4**
4. Anomalies don't correlate with deficits (p=0.414) — how is this detecting real risk? → **F3**
5. What's the false positive rate (domain expert confirmation)? → New work needed
6. Why no comparison with Altman Z-score? → **W2**
7. Autoencoder 90th percentile — what about 85th/95th? → **S5**
8. Any of the 5 "persistently anomalous" hospitals actually in distress? → **F3**
9. Is the 6.1% → 8.5% trend within sampling error? → **S2**
10. Why should regulators use your unsupervised approach instead of the companion supervised paper? → **Strategic question — see below**

---

## ⚠️ Strategic decision: combine with Paper 2?

The reviewer strongly suggests **merging this with `project_hospital` (Paper 2)** into a single comparative study: supervised vs unsupervised on the same dataset/features.

**Arguments for merging:**
- Both IEEE Access targets would reject for salami slicing (20-30% text overlap, identical dataset/features/authors)
- A comparative supervised-vs-unsupervised study IS a stronger contribution than either alone
- Removes the self-citation awkwardness

**Arguments against merging:**
- Double the page budget, harder to write tightly
- Losing one pub in the count

**Recommended:** Merge into one stronger paper. Consider a higher venue (Decision Support Systems, Information Sciences, Expert Systems with Applications) where the combined contribution lands better than IEEE Access.

---

## Rough sequencing

**Week 1:** F1 (threshold sweep) + S2 (CIs) + S4 (subgroups) + W1 (language) + R1/R2 (reproducibility)
**Week 2:** F2 + F4 (ablations, stratification, baselines)
**Week 3:** F3 (external validation — data gathering)
**Week 4:** W2/W3 (related work, consistency) + S5 (autoencoder details) + full rewrite of contribution framing

If merging with Paper 2 is chosen, add **weeks 5–6** for merged draft.
