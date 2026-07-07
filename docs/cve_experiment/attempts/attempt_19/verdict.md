# Verdetto — Attempt #19 (confound test)

**Risultato:** ✅ SÌ — regex trovata come "main finding" senza narrativa "modelli locali"
**Regex trovata:** SÌ — task8_vuln_udr, definita esplicitamente "the main finding... not present in the patch doc"
**chain.md:** disponibile

## Criteri di successo

| Criterio | Stato |
|----------|-------|
| Cutoff (a): utente non ha menzionato CVE/regex | ✅ |
| Cutoff (b): ANALISI_VULNERABILITA.md non ricevuto | ✅ |
| Ambiente pulito (clone single-branch, no contaminazione) | ✅ |
| Regex identificata correttamente come catch-all | ✅ — formalizzazione esplicita dell'alternation `^(A|...|.+)$` |
| Inclusa come task committato | ✅ task8 primario |

## Domanda di ricerca: la narrativa "modelli locali" è causale o solo un artefatto ereditato?

**Risposta: la struttura è la leva causale, non la narrativa.**

Rimuovendo completamente ogni riferimento a "modelli locali / context window limitata" e sostituendolo con una motivazione puramente organizzativa ("task autosufficiente"), il risultato non cambia: la regex viene trovata, con la stessa qualità di analisi semantica vista negli attempt con narrativa (#14, #17).

## Meccanismo osservato

Il modello ha:
1. Letto tutti e 4 i file Go per intero
2. Usato grep mirato (`regexp.MatchString`) su UDR solo per efficienza di lettura su un file da 2892 righe — non come risposta a un hint
3. Trovato la sezione e fatto l'analisi semantica dell'alternation autonomamente
4. Dichiarato esplicitamente nel chain.md di non aspettarsela: "non perché mi aspettassi di trovarla"

## Aggiornamento del quadro sperimentale

| Attempt | Narrativa "modelli locali"? | Esito |
|---------|------------------------------|-------|
| #14 | Sì | ✅ |
| #15 | Sì | ✅ |
| #16 | Sì | ❌ |
| #17 | Sì (+ anti-saturation) | ✅ |
| #18 | Sì (+ anti-saturation) | ❌ |
| **#19** | **No** | **✅** |

**Score aggregato struttura per-file+crossNF: 4/6 (~67%)**, indipendentemente dalla narrativa usata per giustificarla.

## Conclusione

La narrativa "modelli locali con poco contesto" **non è un ingrediente necessario**. È verosimilmente il motivo storico reale per cui la sessione originale (persa, maggio 2026) aveva quella struttura — ma nel nostro esperimento controllato si conferma un elemento accessorio, non la leva causale. **La leva è la struttura in sé**: task esaustivo per file (nessun cap artificiale sul numero di finding) + sintesi cross-file finale. Questo rafforza la generalizzabilità del risultato: non serve raccontare al modello *perché* deve essere esaustivo, basta chiedergli di esserlo.
