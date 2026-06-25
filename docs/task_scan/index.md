# Task Branch Map — Index
> Aggiornato: 2026-06-25

## Matrice cross-branch

| Topic/Vuln | base/pre-cartella | main | failed/recreate-biased | failed/recreate-blind-inverted | exp/test-1 | exp/test-2 |
|---|---|---|---|---|---|---|
| **Math integer** | task1 | task1 | task1 | task1 | task1 | task1 |
| **Math real/stats** | task2 | task2 | task2 | task2 | task2 | task2 |
| **Anomaly detection** | task3 | task3 | task3 | task3 | task3 | task3 |
| **Root cause analysis** | task4 | task4 | task4 | task4 | task4 | task4 |
| **PCF CORS** | ❌ | task5 | task5 | task5 | task5 | task7 |
| **AMF missing default/switch** | ❌ | task7 | ❌ | ❌ | ❌ | ❌ |
| **AMF Content-Type panic** | ❌ | ❌ | ❌ | task6 | ❌ | ❌ |
| **AMF type mismatch c.Set** | ❌ | ❌ | task8 | ❌ | ❌ | ❌ |
| **AMF info disclosure** | ❌ | ❌ | ❌ | ❌ | task6(s/l) | ❌ |
| **UDR missing return** | ❌ | task6* | task6 | task8 | task8(s/l) | task5 |
| **UDR logic bug (Deserialize)** | ❌ | ❌ | ❌ | ❌ | task8(s/l)* | task6 |
| **UDR regex `\|.+` (GHSA-6gxq)** | ❌ | **task6+task9** | **task7** | ❌ | ❌ | ❌ |
| **UDR NoSQL injection** | ❌ | ❌ | task9 | ❌ | ❌ | ❌ |
| **UDM IsValidSupi missing** | ❌ | task8 | task10 | task7 | task7(s/l) | task8(cross)* |
| **Cross-NF synthesis** | ❌ | task9 | ❌ | ❌ | task9 | task8* |
| **PCF memory leak router.Use** | ❌ | ❌ | ❌ | ❌ | ❌ | task7* |

*note: task6 di main combina regex+missing_return nello stesso task; task8 di exp/test-1 combina missing_return+Deserialize; task8 di exp/test-2 è cross-NF UDM→UDR; task7 di exp/test-2 combina CORS+memory_leak

## Anomalie evidenziate

1. **Regex `|.+` solo in main e failed/recreate-biased** — in main è scoperta spontanea (sessione persa); in biased è trascrizione da ANALISI passata al modello. Nei 4 branch rimanenti mai presente.

2. **La vulnerabilità AMF è la più volatile:** ogni branch la identifica diversa (missing default / Content-Type panic / type mismatch c.Set / info disclosure / assente). Nessuna consistenza tra run.

3. **exp/test-2 non ha nessun task AMF** — unico branch security senza questa NF. Al suo posto: 2 task UDR + 1 PCF + 1 cross-NF.

4. **failed/recreate-biased ha 10 task** (max tra tutti) con 3 task sull'UDR — conseguenza del bias da ANALISI che conteneva già molte vuln UDR.

5. **exp/test-1 usa varianti short/long** invece di base/full — struttura diversa da tutti gli altri.

6. **task4 (rootcause)** in tutti i branch = degradazione SINR/HARQ — l'unico task identico in contenuto tra tutti i branch security.

7. **PCF CORS** è consistente in tutti i branch security (solo numerazione varia: task5 ovunque tranne exp/test-2 dove è task7).

## File di dettaglio

- [base/pre-cartella](base-pre-cartella.md)
- [main](main.md)
- [failed/recreate-biased](failed-recreate-biased.md)
- [failed/recreate-blind-inverted](failed-recreate-blind-inverted.md)
- [exp/test-1](exp-test-1.md)
- [exp/test-2](exp-test-2.md)
