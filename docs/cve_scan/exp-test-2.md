## Branch: exp/test-2
**Data analisi:** 2026-06-25
**Regex trovata in:** 0 task

### Task CON regex |.+

Nessuno. Ricerca letterale per `|.+`, `gli-.+`, `GHSA-6gxq`, `IsValidUeId` e la stringa completa su tutti i file: zero match.

### Task SENZA regex

Tutti e 16 i file in docs/tasks/:
- task1-4: math + anomaly + rootcause (no security)
- task5_vuln_missing_return.md — missing `return` dopo 404 in Gin (UDR influenceData handlers)
- task6_vuln_logic_bug.md — pointer-vs-value bug in `openapi.Deserialize`
- task7_vuln_cors.md — CORS misconfiguration + DoS via middleware accumulation in PCF
- task8_vuln_cross_nf.md — missing `supi` validation in UDM propagata a UDR (usa `IsValidSupi`, non `IsValidUeId`)

### Note

- task8_vuln_cross_nf è il più vicino per tema: mostra Handler C (UDR `HandleQuerySmfSelectData`) che valida `ueId` solo per stringa vuota — esattamente la debolezza a monte della CVE. Tuttavia non menziona la regex `|.+`, né GHSA, né `IsValidUeId`
- Il contesto della vulnerabilità è implicito nel codice mostrato, non esplicitato come finding
- Numerazione diversa da main: missing return = task5, logic bug = task6, CORS = task7, cross-NF = task8
