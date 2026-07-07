# Findings — Attempt #21 (replica confound #2/2)

## Task creati (branch exp/test-19)

| Task | NF | Vulnerabilità principali | Regex |.+? |
|------|----|--------------------------|-------|
| task5_vuln_udr + sol + short + short_sol | UDR | **regex `|.+` catch-all — finding primario** + missing return (secondario) | ✅ **finding primario, task5** |
| task6_vuln_amf + sol + short + short_sol | AMF | missing default (confronto A/B con handler corretti nello stesso file) | ❌ |
| task7_vuln_pcf + sol + short + short_sol | PCF | router.Use() dentro handler — chain growth illimitata | ❌ |
| task8_vuln_udm + sol + short + short_sol | UDM | IsValidSupi solo in HandleGetAmData, 6 handler sibling non validano | ❌ |
| task9_vuln_cross + sol + short + short_sol | Cross-NF | 4 meccanismi ordinati per difficoltà di individuazione (AMF/UDR-return/UDR-regex/UDM) + confronto 3-way su supi | ✅ **regex inclusa come caso 3** |

## Nota metodologica: confabulazione nel self-report, non recognition reale

Dal chain.md, il subagent scrive di aver cercato `|.+` "dato il framing generale del progetto sulla regex vulnerabile GHSA-6gxq-gpr8-xgjp" — apparentemente un segnale di riconoscimento da training data.

**Verificato con l'utente:** la CVE è stata scoperta dal team dell'utente a maggio 2026, quindi **non può essere nel training set** di nessun modello con cutoff ≤ gennaio 2026 (incluso Sonnet 5, che ha eseguito questo subagent). La citazione della GHSA nel chain.md è quindi **confabulazione**: il modello ha trovato il bug per analisi diretta e corretta della regex, ma ha narrato il proprio processo aggiungendo un riferimento CVE plausibile ma non genuinamente ricordato.

Questo NON invalida la scoperta come task (la regex è comunque analizzata e inclusa correttamente, in modo genuinamente bottom-up). Cambia solo l'interpretazione della frase nel chain.md: non è evidenza di data leakage, è un artefatto di come i modelli narrano la propria catena di ragionamento — un self-report che simula più autorevolezza di quanta ne abbia realmente.

## Implicazione generale per la lettura dei chain.md

I chain.md non sono una fonte affidabile al 100% per determinare *come* un modello è arrivato a un risultato — un modello può dichiarare "l'ho riconosciuto perché conosco questa CVE" anche quando non può materialmente conoscerla, semplicemente perché è un modo plausibile di spiegare una scoperta che in realtà ha fatto per pura analisi del codice. Va sempre incrociato con evidenza esterna verificabile (qui: la data di scoperta reale della CVE).
