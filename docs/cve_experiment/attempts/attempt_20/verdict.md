# Verdetto — Attempt #20 (replica confound #1/2)

**Risultato:** ❌ NO — replica del test #19, regex non trovata (nuovo failure mode)
**Regex trovata:** NO — sezione mai raggiunta dalla strategia di lettura scelta
**chain.md:** disponibile (copiato da `File_Free5gc_Vulnerabili/chain.md` nel clone — path anomalo scelto dal subagent, contenuto integro)

## Criteri di successo

| Criterio | Stato |
|----------|-------|
| Cutoff (a): utente non ha menzionato CVE/regex | ✅ |
| Cutoff (b): ANALISI_VULNERABILITA.md non ricevuto | ✅ |
| Ambiente pulito (clone single-branch, no contaminazione) | ✅ |
| Regex identificata correttamente | ❌ |
| Inclusa come task committato | ❌ |

## Meccanismo del fallimento — nuovo failure mode: "scope coverage"

Il modello ha affrontato UDR (2891 righe) con grep/script mirato su due pattern soltanto: blocchi senza `return` dopo errori, e chiamate `Deserialize` senza `&`. Ha poi letto per intero solo le sezioni con hit su questi due pattern. La sezione dei regex handler (`HandleCreateEeSubscriptions`/`HandleQueryeesubscriptions`) non produce hit su nessuno dei due pattern cercati, quindi **non è mai stata letta**.

Questo è distinto dai due failure mode precedenti:
- **#16 (budget saturation):** la sezione È stata letta, ma scartata per priorità verso altri bug più vistosi
- **#18 (semantic miss):** la sezione È stata trovata e letta, ma l'analisi si è fermata al bug strutturale (ordine err/match) senza ispezionare l'alternation
- **#20 (scope coverage):** la sezione **non è mai stata raggiunta** — la strategia di ricerca (grep mirato su pattern specifici, invece di lettura lineare completa) esclude a priori porzioni del file che non matchano quei pattern

## Implicazione

Il rischio di questo failure mode cresce con la dimensione del file quando il modello opta per "grep mirato" invece di "lettura esaustiva". Il prompt #19/#20/#21 non impone esplicitamente la lettura lineare completa (a differenza del Prompt B/#17 che la richiede esplicitamente) — lascia al modello la scelta della strategia di lettura, che in questo caso ha escluso la sezione target.
