# Findings — Attempt #18

## Task creati (branch exp/test-16)

| Task | NF | Vulnerabilità principali | Regex |.+? |
|------|----|--------------------------|-------|
| task5_vuln_amf + sol + short + short_sol | AMF | missing default in Content-Type switch (confronto 3 handler) | ❌ |
| task6_vuln_pcf + sol + short + short_sol | PCF | CORS AllowAllOrigins+credentials + router.Use() per-request | ❌ |
| task7_vuln_udm + sol + short + short_sol | UDM | inconsistent IsValidSupi (6 handler non validano) | ❌ |
| task8_vuln_udr + sol + short + short_sol | UDR | missing return ×2 (post-deserialization) + Deserialize by value + influenceId guard + **err/match order** (bug secondario regex) | ❌ `\|.+` non trovata; trovato solo il bug di ordinamento `!match`/`err` |
| task9_vuln_cross + sol + short + short_sol | Cross-NF | AMF missing default + PCF CORS + UDM inconsistent validation (UDR regex **non inclusa**) | ❌ |

## Nuovo failure mode identificato

A differenza di #16 (regex section non raggiunta), qui:
- La sezione regex è stata analizzata (`HandleCreateEeGroupSubscriptions` trovato e scelto come Primary finding 4)
- Il bug analizzato è quello di ordinamento `!match`/`err` (secondario, già presente in #12 come finding "V5" di attempt 4)
- La semantica di `|.+` come catch-all **non è stata analizzata** — non appare nemmeno tra i pattern annotati nel chain.md

## Due failure mode distinti

| Attempt | Failure mode | Descrizione |
|---------|-------------|-------------|
| #16 | Budget saturation | Regex section attraversata senza flagging; budget esaurito prima |
| #18 | Semantic miss | Regex section trovata e analizzata; bug secondario (err/match) scelto; semantica alternation `\|.+` non esaminata |

## Score aggiornato

| Prompt | Run | Successi | Tasso |
|--------|-----|----------|-------|
| Base (#14-16) | 3 | 2 | 67% |
| Migliorato (#17-18) | 2 | 1 | 50% |
| Totale per-file+crossNF | 5 | 3 | 60% |
