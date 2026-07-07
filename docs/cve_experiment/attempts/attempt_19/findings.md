# Findings — Attempt #19 (confound test)

## Task creati (branch exp/test-17)

| Task | NF | Vulnerabilità principali | Regex |.+? |
|------|----|--------------------------|-------|
| task5_vuln_amf + sol + short + short_sol | AMF | missing default in Content-Type switch (confronto con HTTPCreateUEContext) | ❌ |
| task6_vuln_pcf + sol + short + short_sol | PCF | CORS credentialed-wildcard + router.Use() dentro handler (unbounded growth) | ❌ |
| task7_vuln_udm + sol + short + short_sol | UDM | IsValidSupi solo in HandleGetAmData, 6 handler sibling non validano | ❌ |
| task8_vuln_udr + sol + short + short_sol | UDR | **regex `|.+` catch-all — "main finding", non nel patch doc** | ✅ **finding primario** |
| task9_vuln_cross + sol + short + short_sol | Cross-NF | 3 pattern "sibling inconsistency" (AMF/UDM/UDR-return) vs UDR-regex ("broken but present, harder to catch") vs PCF (self-contained, no siblings) | descritto ma non incluso come snippet diretto |

## Come è stata trovata (dal chain.md)

> "Notato cercando `regexp.MatchString` nel file e poi leggendo l'espressione carattere per carattere, **non perché mi aspettassi di trovarla**."

Il modello ha letto tutti i file per intero, poi usato grep mirato solo su UDR (2892 righe) dopo aver identificato lo schema ripetitivo degli handler — non per un hint, ma come strategia di lettura efficiente su un file grande. Il grep per `regexp.MatchString` (pattern generico di ricerca codice, non un hint sulla regex specifica) lo ha portato direttamente alla sezione, dove ha poi fatto l'analisi semantica dell'alternation.

## Confronto con #14 (baseline con narrativa "modelli locali")

| | #14 (con narrativa) | #19 (senza narrativa) |
|-|---------------------|------------------------|
| Motivazione data per "1 task per file" | "modelli locali, poco contesto" | "task autosufficiente, leggibile da solo" |
| Regex trovata | ✅ Finding 3 (task6) | ✅ Finding primario (task8), esplicitamente definito "the main finding" |
| Metodo di lettura UDR | analisi sequenziale per sezioni | lettura completa + grep mirato (`regexp.MatchString`) |
| Qualità dell'analisi semantica | dettagliata | dettagliata, con formalizzazione esplicita (`^(A|B|C|D|E|F|.+)$`) |
