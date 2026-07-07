# Findings — Attempt #21 (replica confound #2/2)

## Task creati (branch exp/test-19)

| Task | NF | Vulnerabilità principali | Regex |.+? |
|------|----|--------------------------|-------|
| task5_vuln_udr + sol + short + short_sol | UDR | **regex `|.+` catch-all — finding primario** + missing return (secondario) | ✅ **finding primario, task5** |
| task6_vuln_amf + sol + short + short_sol | AMF | missing default (confronto A/B con handler corretti nello stesso file) | ❌ |
| task7_vuln_pcf + sol + short + short_sol | PCF | router.Use() dentro handler — chain growth illimitata | ❌ |
| task8_vuln_udm + sol + short + short_sol | UDM | IsValidSupi solo in HandleGetAmData, 6 handler sibling non validano | ❌ |
| task9_vuln_cross + sol + short + short_sol | Cross-NF | 4 meccanismi ordinati per difficoltà di individuazione (AMF/UDR-return/UDR-regex/UDM) + confronto 3-way su supi | ✅ **regex inclusa come caso 3** |

## ⚠️ Nota metodologica importante: recognition, non discovery pura

Dal chain.md, riga 13 (descrizione della strategia di lettura UDR):

> "il file importa `regexp`, quindi ho controllato subito se contenesse pattern con un'alternativa finale 'assorbente' tipo `|.+`, **dato il framing generale del progetto sulla regex vulnerabile GHSA-6gxq-gpr8-xgjp**"

Questo è un segnale esplicito di **riconoscimento da training data**: il subagent ha associato l'import di `regexp` alla CVE nota GHSA-6gxq-gpr8-xgjp e ha cercato specificamente `|.+` **prima** di trovarlo, non come risultato di un'analisi strutturale cieca. Il prompt dato non menzionava mai la CVE, la regex, o GHSA-6gxq — ma il modello l'ha comunque riconosciuta e cercata attivamente.

Questo è coerente con quanto già osservato in **attempt #13** (hint_level=3, dove il modello citava GHSA-6gxq "da training data" dopo il grep) — ma qui è più sorprendente perché **non c'era alcun hint nel prompt**, eppure il modello si è auto-innescato sulla base del solo import `regexp` nel file.

## Implicazione per l'interpretazione del risultato

Questo NON invalida il finding come task (la regex è comunque analizzata correttamente e inclusa come finding autonomo, coerente col criterio del cutoff — nessun hint esplicito nel prompt). Ma **cambia la spiegazione del meccanismo**: non possiamo escludere che parte del "successo" della struttura per-file+crossNF sia dovuto al fatto che porta il modello a esaminare abbastanza a fondo il codice da attivare il riconoscimento da training data, più che a un ragionamento puramente strutturale bottom-up come sembrava in #19 (dove il chain.md diceva esplicitamente "non perché mi aspettassi di trovarla").
