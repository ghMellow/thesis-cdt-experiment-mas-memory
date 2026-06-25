## Branch: main
**Data analisi:** 2026-06-25
**Task totali:** 9 (solo file base, escluse varianti)

### Catalog

| Task file | NF | Topic/Vuln | Varianti | Regex `\|.+`? |
|-----------|----|-----------|---------|----|
| task1_math_int.md | Math | Integer arithmetic (connessioni 5G, risultato intero) | base+sol | ❌ |
| task2_math_real.md | Math | Calcolo media aritmetica e deviazione standard campionaria (throughput antenna) | base+sol | ❌ |
| task3_anomaly.md | Anomaly | Classificazione stato nodo 5G (NORMAL / MINOR_ANOMALY / CRITICAL_ANOMALY) su parametri RF | base+sol | ❌ |
| task4_rootcause.md | RootCause | Root cause analysis degradazione SINR/HARQ post firmware update | base+sol | ❌ |
| task5_vuln_pcf.md | PCF | CORS misconfiguration (AllowAllOrigins+AllowCredentials, doppi header ridondanti) | base+sol | ❌ |
| task6_vuln_udr.md | UDR | Regex catch-all `\|.+` in ueId validation (CVE GHSA-6gxq-gpr8-xgjp) + missing return after 404 in influenceData handler | base+sol+full+full_sol | ✅ |
| task7_vuln_amf.md | AMF | Missing return/default in switch branch (Content-Type non gestito), inconsistent error handling | base+sol+full+full_sol | ❌ |
| task8_vuln_udm.md | UDM | `IsValidSupi` mancante in handler selezionati (GetTraceData, GetUeContextInSmfData), validazione inconsistente | base+sol+full+full_sol | ❌ |
| task9_vuln_cross.md | Cross-NF | Analisi cross-NF (PCF/AMF/UDM/UDR): CORS, regex `\|.+` UDR, missing return AMF, IsValidSupi UDM | base+sol | ✅ |

### Anomalie / Note

- **task6 è unico in tutti i branch:** unisce due vulnerabilità distinte nello stesso task (regex + missing return) invece di separarle
- **task6/7/8 hanno 4 varianti** (base/sol/full/full_sol) — tutti gli altri solo 2. Sviluppo più lungo con versioni extended
- **task9 cross-NF** è l'unico task che aggrega tutti e 4 i NF security in un unico esercizio comparativo — non presente nella maggior parte degli altri branch
- La numerazione è lineare (1–9) senza salti
