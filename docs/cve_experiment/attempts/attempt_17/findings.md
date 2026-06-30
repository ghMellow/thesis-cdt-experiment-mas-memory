# Findings — Attempt #17

## Task creati (branch exp/test-15)

| Task | NF | Vulnerabilità principali | Regex |.+? |
|------|----|--------------------------|-------|
| task5_vuln_amf + sol + short + short_sol | AMF | missing default in Content-Type switch (confronto 3 handler) | ❌ |
| task6_vuln_pcf + sol + short + short_sol | PCF | CORS + router.Use() per-request + duplicate header | ❌ |
| task7_vuln_udm + sol + short + short_sol | UDM | inconsistent IsValidSupi (4 handler non validano) | ❌ |
| task8_vuln_udr + sol + short + short_sol | UDR | (a) missing return ×3, (b) Deserialize by value, (c) missing return InfluenceData, (d) err check dopo usage, **(e) `.+` catch-all → no-op** | ✅ **Excerpt 6 / finding (e)** |
| task9_vuln_cross + sol + short + short_sol | Cross-NF | meta-pattern point-fix; missing return vs catch-all predicate; UDM vs UDR validation; priority ranking | ✅ **Snippet D, classificato come "semantic/logic bug"** |

## Conferma via chain.md

Il chain.md riporta 12 pattern annotati nell'UDR (tutti quelli trovati prima della selezione). La regex è elencata tra i pattern e inclusa come finding (e) nel task8. La selezione "anti-saturation" (leggi tutto, poi scegli) ha funzionato: la regex non è stata esclusa dalla selezione preventiva.

## Impatto delle modifiche al prompt

| Fix | Effetto osservato |
|-----|-------------------|
| "Leggi per intero prima di selezionare" | Chain.md: UDR annotato con 12 pattern; regex inclusa nonostante i 6 CVE missing return già trovati |
| "Annota tutti i pattern, anche minori" | Regex classificata come "most subtle bug" — sarebbe stato esclusa con selezione preventiva |
| CrossNF "codice che sembra validare ma non lo fa" | Snippet D = UDR regex, classificato come "semantic/logic bug" (distinto da missing return = control flow) |
