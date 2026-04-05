# Pre-Submission Checklist — Hospital Anomaly Paper
> Auto-generated 2026-04-03

## 1. Numerical Consistency (Abstract ↔ Body ↔ Tables ↔ JSON)
| Item | Status |
|------|--------|
| N=827, 165 hospitals, 2019–2023 | ✅ All match |
| Consensus: 57 anomalies (6.9%) | ✅ Abstract/Table II/JSON |
| Temporal: 6.1%→8.5% (2019→2023) | ✅ Match (note: non-monotonic path omitted in Abstract — 2020=7.3%) |
| Mann-Whitney means (Table III vs JSON) | ✅ Rounding consistent (0.8955→0.896 etc.) |
| Deficit overlap: 47.4%, χ²=0.67, p=0.414 | ✅ All match |
| Jaccard range 0.239–0.505 | ✅ Match JSON matrix |
| SHAP top-3: Univ(0.476), Public(0.459), Tertiary(0.372) | ✅ Match JSON |
| COVID avg 6.0%, recovery avg 8.2% | ✅ (7.3+4.8)/2=6.05; (7.8+8.5)/2=8.15 |

## 2. Table/Figure References
| Ref | Cited? | Exists? |
|-----|--------|---------|
| Table I (features) | ✅ §III-A | — |
| Table II (algo_rates) | ✅ §IV-A | — |
| Table III (mannwhitney) | ✅ §IV-C | — |
| Table IV (types) | ✅ §IV-F | — |
| Table V (overlap) | ✅ §IV-G | — |
| Fig 1 (consensus_heatmap) | ✅ §IV-B | ✅ fig_consensus_heatmap.png |
| Fig 2 (temporal) | ✅ §IV-D | ✅ fig_anomaly_temporal.png |
| Fig 3 (shap) | ✅ §IV-E | ✅ fig_shap_anomaly.png |
| **placeholder.png** (bio photos) | Used | ❌ **FILE MISSING** |
| fig_anomaly_scores.png | ❌ Not used | Exists (orphan) |
| fig_anomaly_types.png | ❌ Not used | Exists (orphan) |

## 3. Reference Quality
**🔴 Likely Hallucinated (0 search results):**
- `sakurai2021anomaly` — Sakurai & Ogawa, Health Informatics J 2021 — **not found anywhere**
- `bai2023financial` — Bai & Anderson, J Health Care Finance 2023 — **no results**
- `khira2024hospital` — Khira & Bai, Health Services Research 2024 — **no results**
- `choi2022hospital` — Choi & Kim, IJERPH 2022, exact vol/page — **no results**
- `hwang2021korean` — Hwang & Park, Healthcare MDPI 2021 — **no results**

**⚠️ Self-citation:** `kim2024financial` marked "Under review" — acceptable but needs update if published/rejected.

**⚠️ Uncited bib entries (7):** hillestad2005can, bauder2017medicare, sakurai2021anomaly, khira2024hospital, pedregosa2011scikit, zimek2012survey, molnar2022interpretable

## 4. IEEE Access Format
| Requirement | Status |
|-------------|--------|
| ieeeaccess.cls | ✅ |
| `\history{}`, `\doi{}`, `\markboth{}` | ✅ |
| `\IEEEPARstart` (drop-cap 1st para) | ❌ **Missing** |
| `\EOD` (end-of-document marker) | ❌ **Missing** — add before `\end{document}` |
| IEEEbiography sections | ✅ |

## 5. Required Declarations
| Declaration | Status |
|-------------|--------|
| Funding | ⚠️ Vague `\tfootnote` — specify grant or state "no external funding" |
| Conflict of Interest | ❌ **Missing** — IEEE Access requires explicit COI statement |
| Data Availability | ❌ **Missing** — required; HIRA data is public, state URL/access method |

## 6. Author Info
| Item | Status |
|------|--------|
| Kim ORCID | ❌ **Missing** — add to `\address` |
| Sun as corresponding author | ✅ |
| Sun ORCID | ❌ **TODO** |
| Author photos | ❌ placeholder.png — replace with real photos |

## Priority Fixes (sorted)
1. **🔴 Replace/remove 5 suspect references** — biggest rejection risk
2. **🔴 Add COI + Data Availability statements**
3. **🟡 Add `\IEEEPARstart` + `\EOD`**
4. **🟡 Add ORCID for both authors**
5. **🟡 Replace placeholder author photos**
6. **🟢 Remove 7 uncited bib entries**
7. **🟢 Consider including orphan figures or removing from repo**
