# Calibrazione TEXTUAL_PASS_RATIO (passo 1a, doc judge_rubric/08)

- Ripetizioni: **12** (4 task, config ['1A'])
- Escluse (M1 indefinito, n_target_cves=0): 3 — ['task9_vuln_cross']
- M1@any positivi (≥1 CVE trovata): 12/12 — M1-strict positivi (tutte le CVE target): 9/12
- Distribuzione normalized_score: min 0.00 / mediana 0.78 / max 1.00
- Soglia attuale 0.7: accordo con M1@any 0.50 (FP 0, FF 6) — con M1-strict 0.75 (FP 0, FF 3)
- Accordo massimo con M1@any 0.92 sul plateau [0.05–0.40] — con M1-strict 1.00 sul plateau [0.45–0.65]

| soglia | accordo M1@any | FP | FF | accordo M1-strict | FP | FF |
|---|---|---|---|---|---|---|
| 0.05 | 0.92 | 0 | 1 | 0.83 | 2 | 0 |
| 0.10 | 0.92 | 0 | 1 | 0.83 | 2 | 0 |
| 0.15 | 0.92 | 0 | 1 | 0.83 | 2 | 0 |
| 0.20 | 0.92 | 0 | 1 | 0.83 | 2 | 0 |
| 0.25 | 0.92 | 0 | 1 | 0.83 | 2 | 0 |
| 0.30 | 0.92 | 0 | 1 | 0.83 | 2 | 0 |
| 0.35 | 0.92 | 0 | 1 | 0.83 | 2 | 0 |
| 0.40 | 0.92 | 0 | 1 | 0.83 | 2 | 0 |
| 0.45 | 0.75 | 0 | 3 | 1.00 | 0 | 0 |
| 0.50 | 0.75 | 0 | 3 | 1.00 | 0 | 0 |
| 0.55 | 0.75 | 0 | 3 | 1.00 | 0 | 0 |
| 0.60 | 0.75 | 0 | 3 | 1.00 | 0 | 0 |
| 0.65 | 0.75 | 0 | 3 | 1.00 | 0 | 0 |
| 0.70 | 0.50 | 0 | 6 | 0.75 | 0 | 3 | ←
| 0.75 | 0.50 | 0 | 6 | 0.75 | 0 | 3 |
| 0.80 | 0.42 | 0 | 7 | 0.67 | 0 | 4 |
| 0.85 | 0.42 | 0 | 7 | 0.67 | 0 | 4 |
| 0.90 | 0.33 | 0 | 8 | 0.58 | 0 | 5 |
| 0.95 | 0.33 | 0 | 8 | 0.58 | 0 | 5 |
| 1.00 | 0.33 | 0 | 8 | 0.58 | 0 | 5 |

| task | rep | norm. score | verdetto salvato | M1@any | M1-strict |
|---|---|---|---|---|---|
| task5_vuln_pcf | 1 | 1.00 | correct | ✅ | ✅ |
| task5_vuln_pcf | 2 | 0.89 | correct | ✅ | ✅ |
| task5_vuln_pcf | 3 | 0.78 | correct | ✅ | ✅ |
| task6_vuln_udr_full | 1 | 0.44 | wrong | ✅ | ❌ |
| task6_vuln_udr_full | 2 | 0.00 | wrong | ✅ | ❌ |
| task6_vuln_udr_full | 3 | 0.44 | wrong | ✅ | ❌ |
| task7_vuln_amf_full | 1 | 1.00 | correct | ✅ | ✅ |
| task7_vuln_amf_full | 2 | 1.00 | correct | ✅ | ✅ |
| task7_vuln_amf_full | 3 | 1.00 | correct | ✅ | ✅ |
| task8_vuln_udm_full | 1 | 0.67 | wrong | ✅ | ✅ |
| task8_vuln_udm_full | 2 | 0.67 | wrong | ✅ | ✅ |
| task8_vuln_udm_full | 3 | 0.67 | wrong | ✅ | ✅ |
