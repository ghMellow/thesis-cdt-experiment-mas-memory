## Branch: failed/recreate-biased
**Data analisi:** 2026-06-25
**Task totali:** 10 (solo file base)

### Catalog

| Task file | NF | Topic/Vuln | Varianti | Regex `\|.+`? |
|-----------|----|-----------|---------|----|
| task1_math_int.md | Math | Calcolo connessioni 5G — aritmetica intera (settori A/B/C) | base+sol | ❌ |
| task2_math_real.md | Math | Calcolo media e deviazione standard campionaria throughput antenna | base+sol | ❌ |
| task3_anomaly.md | Anomaly | Classificazione stato nodo 5G (NORMAL / MINOR_ANOMALY / CRITICAL_ANOMALY) da metriche RF | base+sol | ❌ |
| task4_rootcause.md | RootCause | Root cause analysis degradazione SINR/HARQ post firmware update | base+sol | ❌ |
| task5_vuln_pcf.md | PCF | CORS misconfiguration (`AllowAllOrigins: true` + `AllowCredentials: true`) in handler OAM `/am-policy/:supi` | base+sol | ❌ |
| task6_vuln_udr_return.md | UDR | Missing `return` dopo `c.String(404)` — esecuzione prosegue nonostante 404 (logic flow bypass) | base+sol | ❌ |
| task7_vuln_udr_regex.md | UDR | Regex catch-all `\|.+` in ueId validation (CVE GHSA-6gxq-gpr8-xgjp) + NoSQL injection via ueId non sanificato in filtro MongoDB | base+sol | ✅ |
| task8_vuln_amf.md | AMF | Type mismatch nel contesto SBI: `c.Set(IN_PB_DETAILS_CTX_STR, problemDetail)` passa struct invece di string (causa panic/nil nel middleware) | base+sol | ❌ |
| task9_vuln_udr_nosql.md | UDR | NoSQL injection — parametri query (`influenceIds`, `dnns`, `supis`, `snssais`) inseriti direttamente in filtro MongoDB `bson.M{"$in": ...}` senza validazione | base+sol | ❌ |
| task10_vuln_udm_validator.md | UDM | Missing input validation — `HandleGetSmfSelectData`, `HandleGetSupi`, `HandleGetNssai`, `HandleGetSmData` passano `supi` raw senza `IsValidSupi()` | base+sol | ❌ |

### Anomalie / Note

- **10 task** (il massimo tra tutti i branch), con **3 task sull'UDR** (task6/task7/task9) — inflazione su un singolo NF
- **task7 e task9 sovrapposti:** entrambi UDR + MongoDB; task7 ha la regex come gate bypassabile verso MongoDB, task9 mostra lo stesso vettore su parametri query diversi
- **task8 AMF** è l'unica occorrenza del type-mismatch `c.Set` tra tutti i branch — vulnerabilità non presente altrove
- **Nessuna variante extra** (solo base+sol per tutti)
- Origine: questo branch aveva ANALISI_VULNERABILITA.md nel contesto fin dal messaggio 0 → trascrizione, non scoperta
