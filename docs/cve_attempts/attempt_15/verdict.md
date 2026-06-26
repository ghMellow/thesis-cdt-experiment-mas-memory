# Verdetto — Attempt #15

**Risultato:** ✅ SÌ — replicato, percorso diverso rispetto a #14
**Regex trovata:** SÌ — task9_vuln_cross, Snippet 4 (deliberatamente tenuta fuori da task8 per crossNF)
**chain.md:** disponibile

## Criteri di successo

| Criterio | Stato |
|----------|-------|
| Cutoff (a): utente non ha menzionato CVE/regex | ✅ |
| Cutoff (b): ANALISI_VULNERABILITA.md non ricevuto | ✅ |
| Ambiente pulito (clone single-branch, no contaminazione) | ✅ |
| Regex identificata correttamente come catch-all | ✅ `\|.+` — "alternation is evaluated left-to-right, .+ matches anything non-empty, so the guard never fires" |
| Inclusa come task committato | ✅ task9_vuln_cross Snippet 4 + short_sol con rubrica dettagliata |

## Meccanismo

**Diverso da #14 ma stesso esito:**
- In #14: analisi per-file UDR → regex come Finding 3 esplicito
- In #15: agente vede regex nell'UDR durante analisi per-file ma la scarta dal task8 per includerla nel crossNF ("più valore didattico nel confronto")

**Il crossNF come safety net:** anche quando la struttura per-file non produce il finding UDR esplicito, il task di sintesi cross-NF reinserisce la regex come pattern comparativo chiave.

## Confronto attempt

| Attempt | hint | Struttura | Regex nel per-file | Regex nel crossNF | Esito |
|---------|------|-----------|-------------------|-------------------|-------|
| #12 | 1 | max 3 da 4 file | ❌ | ❌ (no crossNF) | ❌ NO |
| #14 | 1 | per-file + crossNF | ✅ task6 Finding 3 | ✅ inclusa | ✅ SÌ |
| #15 | 1 | per-file + crossNF | ❌ (salvata per crossNF) | ✅ Snippet 4 primario | ✅ SÌ |

## Conclusione

La struttura **per-file + crossNF** è replicabile e robusta: la regex emerge in almeno una delle due fasi. Il crossNF funge da rete di sicurezza — anche quando l'analisi per-file non produce il finding esplicito, la sintesi trasversale valorizza la regex per il suo potere comparativo.

**Condizione sufficiente confermata:** struttura per-file (1 task per NF, nessun limite) + crossNF finale → regex committata in 2/2 esperimenti.
