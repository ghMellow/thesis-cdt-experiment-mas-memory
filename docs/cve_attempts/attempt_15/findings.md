# Findings — Attempt #15

## Task creati (branch exp/test-13)

| Task | NF | Vulnerabilità principali | Regex |.+? |
|------|----|--------------------------|-------|
| task5_vuln_amf + sol + short + short_sol | AMF | missing default case in Content-Type switch (confronto con handler gemello corretto) | ❌ |
| task6_vuln_pcf + sol + short + short_sol | PCF | router.Use() dentro handler (O(N) middleware growth) + CORS AllowAllOrigins+AllowCredentials | ❌ |
| task7_vuln_udm + sol + short + short_sol | UDM | inconsistent IsValidSupi (5 handler la saltano; plmn-id raw string vs JSON struct) | ❌ |
| task8_vuln_udr + sol + short + short_sol | UDR | missing return (DELETE side-effect) + Deserialize by value (non-pointer) | GHSA citata come CVE ref per missing return; regex esplicitamente tenuta per crossNF |
| task9_vuln_cross + sol + short + short_sol | Cross-NF | AMF silent passthrough + UDM inconsistent validation + **UDR regex `\|.+`** + PCF router state | ✅ **Snippet 4, full explanation** |

## Confronto con attempt #14

| | Attempt #14 | Attempt #15 |
|-|-------------|-------------|
| Ordine NF analizzate | PCF→UDR→AMF→UDM | AMF→PCF→UDM→UDR |
| Regex trovata in per-file UDR | ✅ Finding 3 | ❌ (vista ma salvata per crossNF) |
| Regex trovata in crossNF | ✅ inclusa | ✅ Snippet 4 primario |
| Verdetto finale | ✅ SÌ | ✅ SÌ |

## Note sul meccanismo di replicazione

L'agente ha visto la regex nell'UDR (chain.md: "Il regex `|.+` — questo è il bug CVE GHSA-6gxq-gpr8-xgjp nella sua forma originale... Nel task 8 ho lasciato fuori il regex `|.+` — lo uso nel task 9 cross-NF dove ha più valore didattico nel confronto.")

Questo indica due punti di accesso alla regex nella struttura per-file + crossNF:
1. **Accesso 1:** analisi profonda per-file UDR → regex come finding autonomo nel task UDR (attempt #14)
2. **Accesso 2:** crossNF synthesis → regex inclusa come pattern comparativo di maggior valore didattico (attempt #15)

In entrambi i casi la regex finisce committata come task.
