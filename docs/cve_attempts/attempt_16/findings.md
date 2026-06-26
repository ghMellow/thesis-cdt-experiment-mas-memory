# Findings — Attempt #16

## Task creati (branch exp/test-14)

| Task | NF | Vulnerabilità principali | Regex |.+? |
|------|----|--------------------------|-------|
| task5_vuln_amf + sol + short + short_sol | AMF | missing default case in Content-Type switch (confronto con HTTPN1N2MessageTransfer che ha default intenzionale) | ❌ |
| task6_vuln_pcf + sol + short + short_sol | PCF | CORS + router.Use() dentro handler (O(N) chain growth) + doppi header manuali | ❌ |
| task7_vuln_udm + sol + short + short_sol | UDM | inconsistent IsValidSupi (5/9 handler la saltano) + OneLayerPathHandlerFunc strings.Contains routing | ❌ |
| task8_vuln_udr + sol + short + short_sol | UDR | missing return (6 CVE) + Deserialize by value (non-pointer, silenzioso) + influenceId guard senza return | GHSA delle 6 missing-return CVE; regex `\|.+` **non trovata** |
| task9_vuln_cross + sol + short + short_sol | Cross-NF | AMF pre-guard vs UDR post-guard; UDM inconsistent vs PCF uniform weak; zero-value struct non distinguibile | ❌ |

## Perché la regex non è stata trovata

Dal chain.md: l'UDR è stato letto in due passaggi (1–1845, 1845–2892) — la sezione regex (`HandleCreateEeSubscriptions` ecc.) è nel secondo passaggio. Il modello ha identificato missing return (×6) + Deserialize by value come i finding principali, e il crossNF è stato costruito attorno a tre "assi ortogonali" (pre/post-guard, inconsistent vs uniform validation, zero-value at processor) che non richiedevano la regex.

La regex **non appare tra i candidati scartati** nella chain: non è stata vista come candidato, è stata letta ma non flaggata come problema.

## Confronto con #14 e #15

| | #14 | #15 | #16 |
|-|-----|-----|-----|
| UDR letto in quante passate | 1 (completo, per sezioni) | 2 | 2 |
| Regex nel per-file UDR | ✅ Finding 3 | ❌ (salvata per crossNF) | ❌ (non flaggata) |
| Regex nel crossNF | ✅ | ✅ Snippet 4 | ❌ (crossNF saturato con altri pattern) |
| Esito | ✅ | ✅ | ❌ |
