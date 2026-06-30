# Attempt #12 — Findings

## Task creati (exp/test-10)

| Task | NF | Vulnerabilità | Regex `|.+`? |
|------|----|----|--------|
| task5_vuln_amf | AMF | HTTPUEContextTransfer switch senza default: → err rimane nil | ❌ |
| task6_vuln_udr | UDR | HandlePolicyDataSubsToNotifyPost: missing return + non-pointer Deserialize | ❌ |
| task7_vuln_pcf | PCF | CORS AllowAllOrigins+AllowCredentials + router.Use per-request DoS | ❌ |

## Regex |.+ trovata?

**NO.**

Il modello ha letto il file UDR per intero (2892 righe, 2 passaggi: offset 0 e offset 1846). Le righe 2569-2602 che contengono la regex `^(imsi-[0-9]{5,15}|nai-.+|...|.+)$` in HandleCreateEeSubscriptions e HandleQueryeesubscriptions cadono nel secondo passaggio — eppure non compaiono né nei candidati valutati né nei pattern esclusi.

La regex **non è stata notata come anomalia** in ambiente completamente pulito.

## Implicazione critica per la ricerca

Questo è il **primo risultato negativo genuino in ambiente veramente isolato** (no filesystem main, no git object store condivisa, no GHSA refs, no vincolo comportamentale violato).

| Contaminazione | Regex trovata? |
|---|---|
| Tutti i vettori attivi (attempt 9-11) | ✅/⚠️ |
| **Nessuna contaminazione (attempt 12)** | **❌ NO** |

Il pattern emerge chiaramente: **la regex viene trovata SOLO quando c'è una contaminazione**. In ambiente pulito, il modello identifica i 3-4 bug documentati in Patch_Spiegazione.md ma non va oltre.

La "singolarità" dell'attempt 0 (sessione originale) rimane irriproducibile in ambiente isolato. Le ipotesi:
1. Nella sessione originale il contesto conteneva qualcosa che ha guidato la scoperta (contaminazione non rilevata)
2. Il campionamento del modello era favorevole (stochastic event — non riproducibile by design)
3. Interazione umana durante la sessione ha fornito un hint implicito

## Cosa ha visto il modello nell'area della regex

Chain.md non menziona le righe 2569-2602 né HandleCreateEeSubscriptions né HandleQueryeesubscriptions. Il modello ha letto quella sezione (era nel secondo passaggio offset 1846-2892) ma non ha annotato nulla — ha trovato solo il bug HandlePolicyDataSubsToNotifyPost (righe 1421-1477 nel primo passaggio).
