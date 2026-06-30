# CVE Branch Scan — Index
> Regex target: `|.+` (GHSA-6gxq-gpr8-xgjp) nella validazione `ueId` dell'UDR in free5GC
> Aggiornato: 2026-06-25

| Branch | Task con regex | Task totali | Ultima analisi | Note brevi |
|--------|---------------|-------------|----------------|------------|
| `main` | task6 (×4 varianti), task9 (×2 varianti) | 24 | 2026-06-25 | hint esplicito in task6; solo codice in task9 |
| `failed/recreate-biased` | task7_vuln_udr_regex (×2) | 20 | 2026-06-25 | task dedicato, ma da ANALISI (trascrizione) |
| `failed/recreate-blind-inverted` | ❌ nessuno | 16 | 2026-06-25 | UDR coperto solo per missing-return |
| `exp/test-1` | ❌ nessuno | 24 | 2026-06-25 | task8 UDR usa solo check `ueId == ""` |
| `exp/test-2` | ❌ nessuno | 16 | 2026-06-25 | task8 cross-NF vicino ma non cita regex |
| `base/pre-cartella` | ❌ nessuno | 8 | 2026-06-25 | baseline ante-cartella, solo math+anomaly |

## Riepilogo

- **Branch con regex:** 2/6 (`main`, `failed/recreate-biased`)
- **Origine della regex nei task:** sempre da `ANALISI_VULNERABILITA.md` passata al modello, mai da riscoperta autonoma (vedere [cve_recreation_log.md](../cve_recreation_log.md))
- **Branch senza task security UDR:** `base/pre-cartella` (pre-integrazione)
- **File di dettaglio:** uno per branch in questa directory
