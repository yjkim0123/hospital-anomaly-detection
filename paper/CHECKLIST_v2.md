# CHECKLIST v2 — Hospital Anomaly Paper (12p, v4)
_2026-04-03_

## 🔴 Critical: Reference Hallucinations (3건)

| Bib Key | 문제 | 수정 필요 |
|---|---|---|
| `holmes2021predictors` | 저자 **Holmes/Zhao/Pink → 실제 Enumah SJ & Chang DC** (PubMed 34161840 확인). J Surg Res 267:251-259 맞지만 저자 완전히 다름 | 저자 수정 or 올바른 Holmes 논문으로 교체 |
| `park2022expanding` | 저자 **Park/Seo/Lee → 실제 Yun E, Ko HJ, Ahn B, Lee H, Jang WM, Lee JY**. 페이지도 2065-2073 → **2031-2042** (PMC 9637364) | 저자+페이지 수정 |
| `song2023covid` | 저널 **Health Policy and Technology → 실제 Yonsei Medical Journal** (DOI: 10.3349/ymj.2022.0481). volume/pages도 다름 | 저널+서지정보 전면 수정 |

## 🟡 숫자 불일치

- **N=827 vs 165×5=825**: "balanced panel of 165 hospitals × 5 years" → 825인데 본문은 827. "two hospitals have minor missing" 이면 ≤825여야 함. → **N 또는 hospital 수 재확인**
- `kim2024financial`: bib에 `note={Under review}` + PeerJ CS vol.10 p.e2345 동시 기재 → 출판됐으면 Under review 삭제, 미출판이면 서지정보 수정

## 🟡 미완성 항목

- **Sun ORCID**: `% TODO: Add Sun's ORCID here` 주석 남아있음
- **Author photos**: `placeholder.png` 2건 → 실제 사진 교체 필요
- **DOI**: `10.1109/ACCESS.2026.0000000` placeholder

## 🟡 Orphan Bib Entries (본문 미인용 5건)

`hillestad2005can`, `bauder2017medicare`, `pedregosa2011scikit`, `zimek2012survey`, `molnar2022interpretable` — 본문에서 \cite 안 됨 → 삭제 or 인용 추가

## ✅ 확인 완료

- **검증된 참고문헌**: hilal2022(ESA✓), ngai2011(DSS✓), altman1968✓, lord2020(INQUIRY✓), holmes2017(J Rural Health✓), langabeer2018(Hospital Topics✓), oner2024(ISAF/Wiley✓), ruff2021(Proc IEEE✓), west2016(C&S✓), schmidl2022(VLDB✓), aggarwal2017_ensembles(Springer✓)
- **테이블 내부합산**: Table IV(827✓, 57✓), Table V(overlap 정상), Table VI(41/35/22✓)
- **통계 수치**: 57/827=6.9%✓, 342/827=41.4%✓, 27/57=47.4%✓
- **Consensus 분포 합계**: 78.6+10.6+3.9+2.1+2.3+2.5=100.0%✓
- **COI/Funding/Data Availability**: 모두 포함
- **IEEE Access 포맷**: `\documentclass{ieeeaccess}` ✓, biographies ✓, keywords ✓
- **새 Table V, VI**: 본문 내 정상 참조 (\ref 확인)
