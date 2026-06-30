## Branch: exp/test-1
**Data analisi:** 2026-06-25
**Regex trovata in:** 0 task

### Task CON regex |.+

Nessuno.

### Task SENZA regex

Tutti e 24 i file (task1–task9, varianti long/short/sol). Task UDR: `task8_vuln_udr_long.md` e `task8_vuln_udr_short.md`.

### Note

- I task UDR (task8 long/short) includono codice Go che importa `"regexp"` e usa `:ueId` come path parameter, ma il codice presentato fa solo check primitivo `if ueId == ""` — non c'è validazione con regex né la regex vulnerabile `|.+`
- I finding documentati in task8 sol riguardano: missing return dopo error response, `Deserialize` chiamato senza puntatore, `json.Unmarshal` error silentemente ignorato
- task7 (UDM) copre la mancanza di `IsValidSupi()` — analoga ma distinta (SUPI su UDM, non ueId su UDR)
- La CVE GHSA-6gxq-gpr8-xgjp non è esplicitamente menzionata in nessun task del branch
