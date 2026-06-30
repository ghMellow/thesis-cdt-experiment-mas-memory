## Branch: exp/test-1
**Data analisi:** 2026-06-25
**Task totali:** 9 task distinti (12 file base totali con varianti short/long)

### Catalog

| Task file | NF | Topic/Vuln | Varianti | Regex `\|.+`? |
|-----------|----|-----------|---------|----|
| task1_math_int.md | Math | Aritmetica intera — conteggio connessioni settori 5G | base+sol | ❌ |
| task2_math_real.md | Math | Statistica — media e deviazione standard throughput antenna | base+sol | ❌ |
| task3_anomaly.md | Anomaly | Classificazione stato nodo 5G (NORMAL / MINOR / CRITICAL) su KPI RF | base+sol | ❌ |
| task4_rootcause.md | RootCause | Root cause analysis: degradazione SINR post-firmware update AMF | base+sol | ❌ |
| task5_vuln_pcf.md | PCF | CORS misconfiguration + assenza autenticazione su OAM handler `/am-policy/:supi` | base+sol | ❌ |
| task6_vuln_amf_short.md | AMF | Information disclosure: `reqbody + err.Error()` esposto in risposta HTTP | short+sol | ❌ |
| task6_vuln_amf_long.md | AMF | Idem + visione file completo SBI (UE context transfer, N1N2, AMF status subscription) | long+sol | ❌ |
| task7_vuln_udm_short.md | UDM | Missing SUPI validation in `HandleGetSmfSelectData` (assente vs presente in `HandleGetAmData`) | short+sol | ❌ |
| task7_vuln_udm_long.md | UDM | Idem + file SDM completo: subscriber data management, SUPI/GPSI handlers | long+sol | ❌ |
| task8_vuln_udr_short.md | UDR | Missing `return` dopo errori + `Deserialize` passato per valore invece di puntatore | short+sol | ❌ |
| task8_vuln_udr_long.md | UDR | Idem + file completo UDR data repository; importa `"regexp"` ma senza regex literal `\|.+` | long+sol | ❌ |
| task9_vuln_cross.md | Cross-NF | Meta-task: snippet AMF (info disclosure) + UDM (missing SUPI) + UDR (missing return + wrong deserialize) | base+sol | ❌ |

### Anomalie / Note

- **Struttura short/long invece di base/full:** unico branch con questa variante naming — non esiste `task6_vuln_amf.md` base, solo `_short` e `_long`
- **AMF vulnerability = info disclosure** (error details esposti) — completamente diversa da tutti gli altri branch (main: missing default switch; biased: type mismatch; blind: Content-Type panic; exp/test-2: assente)
- **UDR task8** importa `"regexp"` nel codice Go incluso ma non la usa per validare ueId — la regex vulnerabile non emerge
- **task9 cross-NF** è meta-task di sintesi (come in main), ma copre vulnerabilità diverse da main (no regex, no CORS)
- Nessuna variante `_full` — la granularità è short vs long
