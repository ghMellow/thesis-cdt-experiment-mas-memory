## Branch: failed/recreate-blind-inverted
**Data analisi:** 2026-06-25
**Task totali:** 8 (solo file base)

### Catalog

| Task file | NF | Topic/Vuln | Varianti | Regex `\|.+`? |
|-----------|----|-----------|---------|----|
| task1_math_int.md | Math | Aritmetica intera: conteggio connessioni 5G (3 settori) | base+sol | ❌ |
| task2_math_real.md | Math | Statistica: media aritmetica e deviazione standard campionaria su throughput 5G | base+sol | ❌ |
| task3_anomaly.md | Anomaly | Classificazione anomalia nodo 5G (RSRP, packet loss, throughput, temp, handover) | base+sol | ❌ |
| task4_rootcause.md | RootCause | Root cause analysis: degradazione SINR post-firmware update, HARQ retransmission spike | base+sol | ❌ |
| task5_vuln_pcf.md | PCF | CORS misconfiguration: `AllowAllOrigins=true` + `AllowCredentials=true` (free5gc PCF SBI) | base+sol | ❌ |
| task6_vuln_amf.md | AMF | Content-Type split senza bounds check (`strings.Split(contentType, ";")[0]`): potenziale panic/DoS | base+sol | ❌ |
| task7_vuln_udm.md | UDM | SUPI validation: analisi handler `Nudm_SubscriberDataManagement` — verifica completezza validazione su tutti i path | base+sol | ❌ |
| task8_vuln_udr.md | UDR | Missing `return` dopo `c.String(404)` nella guard `influenceId != "subs-to-notify"`: esecuzione continua oltre il check | base+sol | ❌ |

### Anomalie / Note

- **AMF vulnerability diversa da tutti gli altri branch:** qui è Content-Type split panic (`strings.Split[0]`), altrove è missing default in switch (main), type mismatch c.Set (biased), info disclosure (exp/test-1), o assente (exp/test-2)
- **Nessuna regex |.+** — l'unico run davvero cieco (sessione ebcd1147) ha letto il codice ma ha interpretato la regex come validazione corretta (invertita)
- Solo variante base+sol, nessun _full
