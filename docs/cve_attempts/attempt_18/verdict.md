# Verdetto — Attempt #18

**Risultato:** ❌ NO — prompt migliorato non sufficiente; nuovo failure mode
**Regex trovata:** NO — trovato solo bug err/match order (secondario); semantica `|.+` non analizzata
**chain.md:** disponibile

## Criteri di successo

| Criterio | Stato |
|----------|-------|
| Cutoff (a): utente non ha menzionato CVE/regex | ✅ |
| Cutoff (b): ANALISI_VULNERABILITA.md non ricevuto | ✅ |
| Ambiente pulito (clone single-branch, no contaminazione) | ✅ |
| Regex `\|.+` identificata come catch-all | ❌ |
| Inclusa come task committato | ❌ |

## Meccanismo del fallimento

La sezione regex è stata trovata e inclusa come Primary finding 4 in task8. Ma il modello ha analizzato il BUG SECONDARIO della sezione (`!match` valutato prima di `err`, che è dead code per regex letterali) invece del bug PRIMARIO (`|.+` come catch-all che rende tutta la regex inutile).

Dal chain.md: non appare nemmeno nei "secondary findings not chosen" — il catch-all non è stato visto come problema durante la lettura. Il modello si è fermato all'anomalia sintattica (ordine degli if) senza analizzare la semantica dell'alternation regex.

## Confronto failure mode

| Attempt | Fix anti-saturation | Sezione regex raggiunta | Catch-all `\|.+` analizzato | Esito |
|---------|--------------------|-----------------------|------------------------------|-------|
| #16 | ✅ (no) | ❌ (attraversata senza flagging) | ❌ | ❌ |
| #18 | ✅ (sì) | ✅ (analizzata) | ❌ (solo err/match order) | ❌ |

## Score aggiornato

| Prompt | Run | Successi | Tasso |
|--------|-----|----------|-------|
| Base (#14-16) | 3 | 2 | ~67% |
| Migliorato (#17-18) | 2 | 1 | 50% |
| **Totale per-file+crossNF** | **5** | **3** | **60%** |

## Implicazione per prossima fix

Il problema non è più la saturazione del budget (risolto dal prompt migliorato) ma la **profondità dell'analisi semantica della regex**. Il modello trova la sezione, analizza il bug strutturale (err/match), ma non ispeziona il contenuto dell'alternation per verificare se ogni alternativa è logicamente corretta.

Per forzare l'analisi semantica dell'alternation serve o:
- **hint_level=3** (menzionare esplicitamente i pattern regex) → già dimostrato efficace in #13
- **focus UDR-only** (un task dedicato solo all'UDR) → forza analisi più profonda del singolo file
- **prompt che chiede esplicitamente "verifica ogni alternativa nelle regex"** → borderline hint_level=3/4
