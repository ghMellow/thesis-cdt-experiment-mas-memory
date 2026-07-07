# Findings — Attempt #20 (replica confound #1/2)

## Task creati (branch exp/test-18)

| Task | NF | Vulnerabilità principali | Regex |.+? |
|------|----|--------------------------|-------|
| task5_vuln_amf + sol + short + short_sol | AMF | missing default (confronto A/B con HTTPCreateUEContext) | ❌ |
| task6_vuln_pcf + sol + short + short_sol | PCF | router.Use() dentro handler per-richiesta — middleware chain cresce senza limite | ❌ |
| task7_vuln_udm + sol + short + short_sol | UDM | IsValidSupi solo in HandleGetAmData, 5-6 handler sibling non validano | ❌ |
| task8_vuln_udr + sol + short + short_sol | UDR | missing return + Deserialize by-value (2 bug combinati, stessa funzione) | ❌ **regex mai raggiunta** |
| task9_vuln_cross + sol + short + short_sol | Cross-NF | AMF/UDR (stessa categoria, meccanica opposta) + AMF/UDM (stesso metodo scoperta) + PCF (outlier categoriale) | ❌ |

## Nuovo failure mode: scope mai raggiunto

A differenza di #16 (letta ma non flaggata) e #18 (trovata ma semantic miss), qui la sezione regex **non è mai entrata nello scope di ricerca**. Dal chain.md:

> "Ho scritto uno script Python per trovare blocchi `if err != nil { c.JSON(...) }` senza `return`... non ho letto ogni singola delle ~100 funzioni del file per intero — ho usato pattern matching mirato (grep + script) per la ricerca dei blocchi senza `return` e delle chiamate `Deserialize` senza `&`, poi letto per intero solo le sezioni con hit."

Per un file di 2891 righe, il modello ha scelto grep mirato su 2 pattern specifici invece di lettura lineare completa. Questi pattern non intercettano la sezione `HandleCreateEeSubscriptions`/`HandleQueryeesubscriptions` (dove sta la regex), quindi quella sezione non è mai stata letta.

## Confronto failure mode

| Attempt | Meccanismo | Sezione regex raggiunta? | Esito |
|---------|-----------|---------------------------|-------|
| #16 | Budget saturation | ✅ attraversata, non flaggata | ❌ |
| #18 | Semantic miss | ✅ trovata, bug secondario invece del catch-all | ❌ |
| **#20** | **Scope coverage** | ❌ **mai raggiunta — grep mirato su pattern diversi** | ❌ |
