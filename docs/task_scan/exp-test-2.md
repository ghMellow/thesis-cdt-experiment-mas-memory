## Branch: exp/test-2
**Data analisi:** 2026-06-25
**Task totali:** 8 (solo file base, 16 totali con _sol)

### Catalog

| Task file | NF | Topic/Vuln | Varianti | Regex `\|.+`? |
|-----------|----|-----------|---------|----|
| task1_math_int.md | Math | Calcolo connessioni 5G (aritmetica intera) | base+sol | ❌ |
| task2_math_real.md | Math | Media e deviazione standard throughput antenna | base+sol | ❌ |
| task3_anomaly.md | Anomaly | Classificazione anomalia nodo 5G (RSRP, packet loss, throughput, temp, handover) | base+sol | ❌ |
| task4_rootcause.md | RootCause | Root cause analysis degradazione SINR/HARQ post-firmware-update | base+sol | ❌ |
| task5_vuln_missing_return.md | UDR | Missing `return` after 404 in Gin handlers — esecuzione continua dopo errore HTTP | base+sol | ❌ |
| task6_vuln_logic_bug.md | UDR | Silent data loss: pass-by-value a `Deserialize` + missing `return` dopo errore | base+sol | ❌ |
| task7_vuln_cors.md | PCF | CORS misconfiguration + memory leak da `router.Use()` chiamata a ogni request (middleware accumulation) | base+sol | ❌ |
| task8_vuln_cross_nf.md | Cross-NF (UDM→UDR) | Missing input validation in UDM `HandleGetSmfSelectData` propagata a UDR downstream | base+sol | ❌ |

### Anomalie / Note

- **PCF CORS slittato a task7** (vs task5 in tutti gli altri branch) — numerazione diversa
- **AMF completamente assente** — unico branch senza nessun task sull'AMF
- **2 task UDR** (task5 e task6) entrambi sulla stessa NF: missing return e logic bug Deserialize
- **task7 PCF** aggiunge una seconda vulnerabilità unica: memory leak da `router.Use()` dentro handler — non presente in nessun altro branch
- **task8 cross-NF** è l'unico che mostra una catena UDM→UDR (propagazione input non validato)
- Solo variante base+sol, nessuna extra
