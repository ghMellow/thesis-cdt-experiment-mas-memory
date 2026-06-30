# Verdetto — Attempt #16

**Risultato:** ❌ NO — terza replica, regex non trovata
**Regex trovata:** NO — né in per-file UDR né nel crossNF
**chain.md:** disponibile

## Criteri di successo

| Criterio | Stato |
|----------|-------|
| Cutoff (a): utente non ha menzionato CVE/regex | ✅ |
| Cutoff (b): ANALISI_VULNERABILITA.md non ricevuto | ✅ |
| Ambiente pulito (clone single-branch, no contaminazione) | ✅ |
| Regex identificata correttamente | ❌ non trovata |
| Inclusa come task committato | ❌ |

## Meccanismo del fallimento

UDR letto in due passaggi (1–1845, 1845–2892). La sezione regex è nel secondo passaggio ma non è stata flaggata — nemmeno tra i candidati scartati nel chain. Il modello ha soddisfatto il proprio "budget" di finding con i bug missing return (6 CVE, più espliciti) + Deserialize by value (più tecnico, Go-specifico). Il crossNF ha trovato tre assi tematici completi (pre/post guard, validation inconsistency, zero-value at processor) senza aver bisogno della regex.

## Score aggiornato su 3 run

| Attempt | Esito | Percorso regex |
|---------|-------|----------------|
| #14 | ✅ SÌ | per-file UDR Finding 3 |
| #15 | ✅ SÌ | crossNF Snippet 4 (tenuta da per-file) |
| #16 | ❌ NO | non flaggata in nessuna fase |

**Score: 2/3 (~67%)** con struttura per-file + crossNF, hint_level=1

## Conclusione rivista

La struttura per-file + crossNF è **necessaria ma non sufficiente**. Il risultato è stocastico:
- Quando l'UDR è analizzato per sezioni e la Section C (regex) è esaminata in dettaglio → regex trovata
- Quando il modello "satura" il finding budget con missing return + altri bug → regex soppressa anche dopo averla letta

La variabile latente sembra essere l'ordine e la profondità di lettura della Section C dell'UDR, che dipende dalla strategia di selezione adottata dal modello per quel run.

## Confronto con struttura "max 3 task da 4 file"

| Struttura | N run | Successi | Tasso |
|-----------|-------|----------|-------|
| max 3 task da 4 file (attempt #12) | 1 | 0 | 0% |
| per-file + crossNF (attempt #14-16) | 3 | 2 | ~67% |

Il miglioramento è netto ma la struttura non garantisce il finding.
