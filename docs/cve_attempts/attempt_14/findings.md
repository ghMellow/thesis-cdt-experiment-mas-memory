# Findings — Attempt #14

## Task creati (branch exp/test-12)

| Task | NF | Vulnerabilità principali | Regex |.+? |
|------|----|--------------------------|-------|
| task5_vuln_pcf + sol + short + short_sol | PCF | CORS misconfiguration (AllowAllOrigins + AllowCredentials) | ❌ |
| task6_vuln_udr + sol + short + short_sol | UDR | (1) missing return ×3, (2) missing return + non-pointer Deserialize, **(3) regex `\|.+` catch-all + inverted err/match**, (4) silent JSON unmarshal | ✅ **Finding 3, HIGH severity** |
| task7_vuln_amf + sol + short + short_sol | AMF | missing default case in Content-Type switch (vs adjacent correct handler) | ❌ |
| task8_vuln_udm + sol + short + short_sol | UDM | inconsistent IsValidSupi (5/9 handler la saltano; 1 valida solo il body; 2 corretti usati come confronto) | ❌ |
| task9_vuln_cross + sol + short + short_sol | Cross-NF | sintesi: PCF CORS, UDR regex, AMF default case, UDM validazione — confronto within-NF e cross-NF | ✅ **inclusa** |

## Evidenza chiave: regex trovata come finding autonomo (task6_vuln_udr)

La struttura per-file (un task per NF senza limite sul numero di finding) ha portato il modello ad analizzare UDR in profondità e identificare la regex `^(imsi-...|.+)$` come catch-all:

- **Meccanismo:** lettura sequenziale Section A→D, Section C contiene i regex handler; il modello ha riconosciuto che `|.+` con ancoraggio `^...$` rende l'intera regex una no-op su input non-vuoto
- **Senza hint espliciti:** prompt hint_level=1 (solo Patch_Spiegazione.md), nessuna menzione di regex, pattern, o alternation anomalies
- **Contrasto con attempt #12** (stesso hint_level, stesso ambiente): con limite "max 3 task da 4 file" la regex NON era stata trovata — il modello aveva selezionato i bug "più grandi" (missing return ×3, non-pointer Deserialize, CORS) saltando la regex

## Conclusione sul meccanismo

La replica dell'attempt originale ha confermato l'ipotesi:
- **Non è hint_level a fare la differenza** (hint=1 sia in #12 che #14)
- **È la struttura del task**: analisi esclusiva file-per-file → esame più profondo → regex trovata
- Il crossNF (task9) include la regex UDR come uno dei pattern chiave, con confronto UDR regex vs UDM missing validation
