# IEEE Access Paper Final Review: Anomaly Detection Paper

**Paper:** "Unsupervised Anomaly Detection in Hospital Financial Statements: A Multi-Algorithm Consensus Approach with Explainable AI"

**Review Date:** 2026-04-05

---

## Part 1: Visual/Format Check

### ✅ LaTeX Structure and Formatting

| Item | Status | Notes |
|------|--------|-------|
| `\IEEEPARstart` in Introduction | ✅ Present | `\IEEEPARstart{H}{ospital}` correctly used |
| `\EOD` before `\end{document}` | ✅ Present | Correctly placed |
| `\history{}` present | ✅ Present | `\history{Date of publication xxxx 00, 0000...}` |
| `\doi{}` present | 🟡 Commented | `% \doi{}` - Noted as "Assigned by IEEE upon acceptance" |
| `graphicspath` set | ✅ Correct | `\graphicspath{{../figures/}}` |
| Author bios with photos | ✅ Present | Both `\IEEEbiography` blocks with `\includegraphics` |
| `xfigwd` fix | ✅ Present | Workaround for ieeeaccess.cls bug included |

### ✅ Author Block Formatting

| Item | Status | Notes |
|------|--------|-------|
| Author names uppercase | ✅ Correct | `\uppercase{Yongjun Kim}` and `\uppercase{Eun Jung Sun}` |
| ORCID in address | ✅ Present | Kim's ORCID: 0000-0003-4234-4883 |
| Corresponding author | ✅ Indicated | "(Corresponding Author: Eun Jung Sun)" |
| Email addresses | ✅ Present | Both authors have e-mail in address blocks |

### ✅ Figures

| Figure | File | Status |
|--------|------|--------|
| fig_consensus_heatmap.png | ../figures/ | ✅ Exists |
| fig_anomaly_temporal.png | ../figures/ | ✅ Exists |
| fig_shap_anomaly.png | ../figures/ | ✅ Exists |
| kim_photo.jpg | paper/ | ✅ Exists (38KB) |
| sun_photo.jpg | paper/ | ✅ Exists (19KB) |

### ✅ Tables Referenced

All tables (`tab:features`, `tab:algo_rates`, `tab:mannwhitney`, `tab:types`, `tab:overlap`, `tab:anomaly_types`, `tab:cross_type_est`, `tab:validation_summary`) are defined and referenced in text.

### No Broken LaTeX Commands Detected

No text artifacts or formatting issues found. Compilation produces clean output (only xcolor warnings from ieeeaccess.cls, which are standard).

---

## Part 2: Numerical Consistency Check

### ✅ Core Numbers: Abstract vs Body

| Statistic | Abstract | Body Text | Tables | Status |
|-----------|----------|-----------|--------|--------|
| N (total) | 827 | 827 (Section 3.1) | Table 1 caption | ✅ Consistent |
| Hospitals | 165 | 165 (Section 3.1) | - | ✅ Consistent |
| Years | 2019-2023 | 2019-2023 | - | ✅ Consistent |
| Consensus anomalies | 57 (6.9%) | 57 (6.9%) | Table 2 | ✅ Consistent |
| Temporal 2019 | 6.1% | 6.1% (Section 4.4) | - | ✅ Consistent |
| Temporal 2023 | 8.5% | 8.5% (Section 4.4) | - | ✅ Consistent |
| p-values (<0.001) | ✅ | ✅ (Table 3) | Table 3 | ✅ Consistent |
| Deficit overlap | 47.4% | 47.4% | Table 5 | ✅ Consistent |
| χ² | 0.67 | 0.67 (Section 4.6) | - | ✅ Consistent |
| p (χ²) | 0.414 | 0.414 (Section 4.6) | - | ✅ Consistent |
| Jaccard range | 0.239-0.505 | 0.239-0.505 (Section 4.2) | - | ✅ Consistent |

### ✅ Mann-Whitney Values (Table 3)

- Labor Cost Ratio: 0.575 vs 0.896 → Confirmed in text
- Admin Cost Ratio: 0.221 vs 0.409 → Confirmed in text  
- Subsidy Ratio: 0.027 vs 0.163 → Confirmed in text
- All p-values match text descriptions

### ✅ SHAP Top Features (Section 4.5)

- University hospital: 0.476
- Public hospital: 0.459
- Tertiary hospital: 0.372
- Subsidy ratio: 0.353
- Log revenue: 0.233
- Log beds: 0.224
- Admin ratio: 0.224
- Labor ratio: 0.222

All consistent between text and figure description.

### ✅ Temporal Detailed Numbers

| Year | Rate in Text |
|------|--------------|
| 2019 | 6.1% |
| 2021 | 4.8% |
| 2022 | 7.8% |
| 2023 | 8.5% |

All internally consistent.

---

## Part 3: Reference Quality

### Total References: 37 entries in refs.bib

### ✅ Verified Real References (Sample Verification)

| Reference | Status | Notes |
|-----------|--------|-------|
| liu2008isolation | ✅ Real | Foundational Isolation Forest paper |
| breunig2000lof | ✅ Real | LOF paper, SIGMOD 2000 |
| lundberg2017unified | ✅ Real | SHAP paper, NeurIPS 2017 |
| chandola2009anomaly | ✅ Real | ACM Computing Surveys anomaly detection review |
| oner2024hospital | ✅ Real | Verified - Wiley ISAF 2024/2025 |
| park2022expanding (Yun et al.) | ✅ Real | Verified - Risk Management Healthcare Policy 2022 |
| holmes2021predictors (Enumah & Chang) | ✅ Real | Verified - J Surgical Research 2021 |
| schmidl2022anomaly | ✅ Real | Verified - VLDB Endowment 2022 |

### 🔴 ISSUE: Problematic Reference

| Reference | Issue |
|-----------|-------|
| **kim2024financial** | Says "Under review" in note field but is cited as if published. The paper claims PeerJ Computer Science vol 10, page e2345, year 2024. This appears to be a self-citation to unpublished/unverified work. |

### ✅ Citation/Bib Key Alignment

All cited references have corresponding bib entries. No undefined citations detected.

### 🟡 Uncited References

The following bib entries exist but are not cited in the tex file:
- altman1968financial
- ngai2011application
- ahmed2016survey
- arrieta2020explainable
- Several others used in COVID paper but not this one

**Verdict:** These unused entries should be cleaned from refs.bib before submission.

### 🟡 Naming Convention Issue

The bib key `holmes2021predictors` is named after Holmes but the actual paper is by Enumah & Chang. While the bib entry content is correct, this is confusing. Consider renaming to `enumah2021predictors`.

---

## Part 4: Reviewer Simulation

### Reviewer 1: ML/Anomaly Detection Expert

**Assessment:** Accept with Minor Revisions

**Strengths:**
1. Sound methodological approach using consensus of 5 complementary algorithms
2. Appropriate choice of algorithms spanning different anomaly detection paradigms (isolation-based, density-based, boundary-based, reconstruction-based)
3. SHAP integration provides excellent interpretability
4. Jaccard analysis of inter-algorithm agreement is a nice contribution

**Weaknesses:**
1. Contamination parameter set to 0.1 for all algorithms without justification - why not cross-validate?
2. DBSCAN ε tuning via 90th percentile is heuristic; sensitivity analysis would strengthen claims
3. Autoencoder architecture (11→8→4→8→11) is shallow - have you tried deeper architectures?

**Questions:**
1. How sensitive are results to the consensus threshold (≥3)? What about ≥2 or ≥4?
2. Have you compared against more recent deep anomaly detection methods (e.g., Deep SVDD, neural network-based autoencoders with attention)?
3. Why apply SHAP only to Isolation Forest? Would SHAP on the consensus ensemble provide different insights?

---

### Reviewer 2: Healthcare Finance Domain Expert

**Assessment:** Accept with Minor Revisions

**Strengths:**
1. Excellent domain understanding - distinction between structural anomaly vs. profitability is novel
2. Temporal analysis spanning pre-COVID, pandemic, and recovery periods is valuable
3. Case study section with anomaly taxonomy (Type C/S/Z) provides actionable insights
4. Policy implications are thoughtful and practical

**Weaknesses:**
1. The finding that public hospitals dominate anomalies (54.4%) is unsurprising - this is well-known in Korean healthcare
2. External validation against actual regulatory actions or hospital closures would strengthen claims
3. The anonymized case study limits replicability

**Questions:**
1. Have you validated against HIRA's own financial risk indicators or ratings?
2. What proportion of the persistently anomalous hospitals received actual regulatory intervention?
3. The 47.4% overlap with deficits - is this overlap random, or do anomaly+deficit hospitals have distinct profiles?

---

### Reviewer 3: Methodology/Statistics Expert

**Assessment:** Accept with Minor Revisions

**Strengths:**
1. Mann-Whitney U test is appropriate for non-normal distributions
2. Chi-squared test for independence between anomaly and deficit status is correctly applied
3. Jaccard similarity is an appropriate measure for binary agreement
4. Sample size (N=827) provides reasonable statistical power

**Weaknesses:**
1. No correction for multiple comparisons in Table 3 (11 features tested)
2. The panel structure means observations are not independent - temporal autocorrelation not addressed
3. Claiming p=0.414 shows "no association" is technically incorrect (failure to reject null ≠ evidence of no effect)

**Questions:**
1. Have you considered Bonferroni or FDR correction for the 11 Mann-Whitney tests?
2. What is the intra-class correlation (ICC) across years for the same hospital?
3. Would a mixed-effects model accounting for hospital clustering change the significance patterns?
4. The consensus anomaly rate varies by year (4.8% to 8.5%) - is this statistically significant variation?

---

## Part 5: Risk Assessment

| Risk Category | Rating | Justification |
|--------------|--------|---------------|
| **Desk Reject Risk** | 🟢 Low | Paper is well-formatted, follows IEEE Access guidelines, clear contribution |
| **Hallucinated Reference Risk** | 🟡 Medium | kim2024financial is problematic (claims published but marked "under review"); other refs verified |
| **Numerical Inconsistency Risk** | 🟢 Low | All numbers cross-checked and consistent |
| **Novelty Concern Risk** | 🟡 Medium | Consensus anomaly detection is not novel; application to hospital finance is the contribution |
| **Scope Fit Risk** | 🟢 Low | IEEE Access publishes healthcare informatics and financial ML papers |

---

## Part 6: Comparison with COVID Paper

### Data Description Overlap

| Element | Anomaly Paper | COVID Paper | Overlap Concern |
|---------|---------------|-------------|-----------------|
| Sample size | 165 hospitals, N=827 | 165 hospitals, N=825 | ⚠️ Same hospitals, slight N difference |
| Time period | 2019-2023 | 2019-2023 | ⚠️ Identical |
| Data source | HIRA/KHIDI | KHIDI/HASPA | ⚠️ Same source |
| Feature count | 11 features | 11 features | ⚠️ Similar approach |

### Contribution Distinction

| Anomaly Paper | COVID Paper |
|---------------|-------------|
| **Unsupervised** multi-algorithm consensus | **Supervised** ML framework with XAI |
| Detects **structural** anomalies | Predicts **binary** deficit outcome |
| Focus on **unexplained** financial patterns | Focus on **predictive** accuracy |
| Consensus mechanism is the innovation | Framework reusability is the innovation |

### Self-Plagiarism Risk Assessment

**Risk Level: 🟡 MEDIUM**

**Concerns:**
1. Both papers use nearly identical data (165 hospitals, 2019-2023, same source)
2. Both papers have 11 features with similar feature engineering
3. Both papers use SHAP for explainability
4. Both papers have the same authors
5. Data description sections have similar structure and language

**Mitigating Factors:**
1. Research questions are fundamentally different (supervised vs. unsupervised)
2. Anomaly paper explicitly cites COVID paper as kim2024financial
3. Methodological contributions are distinct
4. Tables and figures are different

**Recommendations:**
1. 🔴 Cross-reference the COVID paper explicitly in the data description (add a sentence like "The same dataset was used in [kim2024financial] for a different analytical purpose")
2. 🟡 Consider rewording the data description section to reduce textual similarity
3. 🟡 Run self-plagiarism checker before submission

---

## Summary of Issues

### 🔴 CRITICAL (Must Fix Before Submission)

1. **kim2024financial reference**: Claims "Under review" but cited as published with volume/page numbers. Either:
   - Update if actually published
   - Change to "submitted" or remove volume/page
   - Remove the citation if it creates circular reference concerns

### 🟡 IMPORTANT (Should Fix)

1. **Uncited references in refs.bib**: Clean up ~15 unused bib entries to prevent reviewer confusion

2. **Bib key naming**: `holmes2021predictors` should be `enumah2021predictors` for clarity

3. **Missing \doi{}**: Currently commented out - this is fine for submission but confirm IEEE Access process

4. **Cross-reference COVID paper**: Add explicit acknowledgment that same dataset used for different purpose to preempt self-plagiarism concerns

5. **Multiple comparison correction**: Address the 11 Mann-Whitney tests issue (mention in limitations or apply Bonferroni)

6. **Statistical language**: "No significant association" (p=0.414) should be phrased as "we found no evidence of association" to be technically correct

### 🟢 MINOR (Nice to Fix)

1. **Sensitivity analysis**: Add brief discussion of consensus threshold choice (≥3 vs other thresholds)

2. **Autoencoder justification**: Add brief justification for architecture choice

3. **DBSCAN epsilon**: Add sentence about sensitivity to epsilon parameter

4. **Intra-hospital correlation**: Mention temporal autocorrelation in limitations section

5. **Author bios**: Consider adding ORCID for Dr. Sun if available

---

## Final Verdict

**Overall Assessment: READY FOR SUBMISSION with minor fixes**

The paper is well-written, methodologically sound, and makes a clear contribution to healthcare financial surveillance. The key findings (6.9% consensus anomalies, 47.4% deficit overlap, temporal patterns) are clearly presented and internally consistent.

**Priority Actions:**
1. Fix kim2024financial reference (🔴 CRITICAL)
2. Clean refs.bib (🟡 IMPORTANT)  
3. Add COVID paper cross-reference in data section (🟡 IMPORTANT)

After these fixes, the paper should be ready for IEEE Access submission.

---

*Review completed by automated analysis system*
