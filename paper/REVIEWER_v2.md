# REVIEWER SIMULATION v2 — Hospital Anomaly (12p, v4)
_2026-04-03 | v1 baseline: 6.7/10, Minor Revision_

---

## R1: ML / Anomaly Detection Expert

**Score: 7.5 / 10** (v1 → +0.8)

**강점**
1. **5-알고리즘 컨센서스 + Jaccard 분석**: 단일 알고리즘 한계를 체계적으로 극복. 중간 수준 일치도(0.24–0.50)가 다양성 확보를 실증
2. **Case Study 이상치 분류학(Type C/S/Z)**: v1에 없던 핵심 기여. 탐지→해석→정책까지 연결되어 실용성 대폭 향상

**약점**
1. **Temporal independence 가정**: §V-G에서 시계열 패턴을 논하면서도 hospital-year를 독립 관측치로 처리. 패널 내 자기상관 무시는 anomaly persistence 분석의 신뢰성 약화 → Limitation에 언급은 했으나 robustness check(e.g., hospital-level clustering) 부재
2. **Contamination=0.1 사전 고정**: 감도분석(0.05/0.10/0.15)이 추가됐지만 3개 값만 테스트. Data-driven 선택(e.g., elbow method on score distribution)이 없음

**판정: Minor Revision** — v1 대비 Case Study와 Validation이 크게 보강. 시계열 독립성 한계를 실험적으로 보완하면 Accept 가능

---

## R2: Healthcare Finance / 의료경영

**Score: 7.8 / 10** (v1 → +1.1)

**강점**
1. **COVID 보조금 타이밍 검증**: 2021년 anomaly dip(4.8%) → 2023년 8.5% 패턴이 실제 보조금 규모($674M→$2B)와 정합. 외부 타당성 대폭 강화
2. **공립병원 구조조정 사례**: 국립의료원·강릉·속초 의료원 등 실명 사례가 정책 함의를 구체화. 언론 보도와 일치하는 외부 검증

**약점**
1. **Case mix / 환자 특성 미반영**: Feature 11개 중 환자 중증도·보험 유형·외래비율 없음. Holmes 2017이 지적한 핵심 변수 누락 → 비용 이상치가 환자 구성 차이인지 운영 비효율인지 구분 불가
2. **한국 특수성 일반화 한계**: HIRA 공시 기반이라 의료체계가 다른 국가 적용성 불명. Future work에 cross-national 언급은 있으나 framework 이식성 근거 부족

**판정: Minor Revision → Accept 근접** — v1의 최대 약점(validation 부족)이 해소. Case mix 한계 인정 + 향후 확장 계획 보강으로 Accept 충분

---

## R3: IEEE Access Associate Editor

**Score: 7.2 / 10** (v1 → +0.5)

**강점**
1. **분량·구조 적정**: 8p→12p 확장이 Case Study·Validation·Future Work로 균형 있게 배분. IEEE Access 포맷 준수
2. **Reproducibility**: Data source(HIRA) 명시, 알고리즘 하이퍼파라미터 전부 기재, code available upon request

**약점**
1. **참고문헌 오류 3건**: `holmes2021`(저자 불일치), `park2022`(저자+페이지), `song2023`(저널 오류) — 출판 전 반드시 수정 필수. Hallucination 의심
2. **Orphan references 5건 + placeholder 잔존**: 미인용 bib 5개, Sun ORCID TODO, placeholder 사진, dummy DOI — 완성도 부족

**판정: Minor Revision** — 기술적 기여는 충분하나 서지 오류가 심각. 수정 후 최종 확인 1라운드면 Accept

---

## 종합

| | R1 (ML) | R2 (의료) | R3 (편집) | **평균** |
|---|---|---|---|---|
| v1 | 6.7 | 6.7 | 6.7 | **6.7** |
| **v2** | **7.5** | **7.8** | **7.2** | **7.5** |

**v1→v2 주요 개선**: Related Work 확장, Case Study 3유형 분류, COVID 검증, 공립 사례, 감도분석, 제한점 확대
**Accept까지 남은 것**: ① 참고문헌 오류 3건 수정 ② N=827 불일치 확인 ③ placeholder/TODO 정리

**예상 판정: Minor Revision (→ 1회 수정 후 Accept)**
