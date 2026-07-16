# 13 — Risultati: rubrica GT-free v2 nel banco di prova

> Risultati dell'esperimento del doc 12 (2026-07-16). Rubrica v2 = `gtfree/rubric_v2_draft.json` (5 criteri LLM a conteggio, max 10) + coverage su superfici a rischio (0–2), giudice di sistema gemma4:31b-cloud, K=3, `--motivations` attivo. Dati grezzi: `results/evaluation/judge_calibration/gtfree_v2_*.{md,json}`.

## 1. Il banco C1/C2: da +0.437 a +0.600, zero C2 promossi

| | GT-derivata (doc 09) | GT-free v1 (doc 11) | **GT-free v2** |
|---|---|---|---|
| C1 medio | 1.000 | 1.000 | 0.983 |
| C2 medio | 0.052 | 0.563 | **0.383** |
| CGP | +0.948 | +0.437 | **+0.600** |
| C2 promossi a t=0.65 | 0/5 | 2/5 | **0/5** |
| C1 bocciati | 0/5 | 0/5 | 0/5 |

I due C2 che la v1 promuoveva sono rientrati, ed entrambi per il meccanismo previsto:

| task | C2 | v1 | **v2** | perché |
|---|---|---|---|---|
| task5 | missing-return + regex | 0.44 | 0.50 | respinto (era già respinto) |
| task6 | switch/`c.Set` | 0.78 | **0.33** | criteri a conteggio: l'evidenza generica non regge più |
| task7 | SUPI validation mancante | **1.00** | **0.61** | `absence_claims`: il giudice ha cercato la contro-evidenza e l'ha trovata — «`ueContextId` non è mai nemmeno estratto dal contesto Gin; il percorso descritto non esiste nello snippet» (feedback persistito nel JSON) |
| task8 | CORS | 0.11 | 0.33 | respinto |
| task9 | CORS su funzioni sbagliate | 0.48 | **0.14** | respinto più nettamente (coverage superfici 0.5 + conteggio) |

Il requisito di motivazione (doc 12 §3) ha fatto esattamente il suo lavoro anti-generosità: per abbassare `absence_claims` il giudice deve citare il percorso di codice mancante, e sul task7 C2 lo ha fatto con precisione chirurgica. È anche l'«output del ragionamento nei casi in cui sbaglia» chiesto dall'esperto — ora persistito per ogni giudizio sotto il massimo.

## 2. Sui report reali: la saturazione resta — ed è la conferma del buco strutturale

Tutti i 15 report reali: **10/10 su ogni criterio LLM, in tutte le K=3 ripetizioni** (varianza zero). Flip vs GT-derivata 3/15 a t=0.65 (sempre i task6, sempre nella direzione sbagliata); accordo M1-strict **9/12**, identico alla v1.

Non è un incidente: è la previsione del doc 12 §5 realizzata. I criteri v2 misurano se i claim del report reggono il confronto con il codice citato — e i report reali dell'agente *reggono quel confronto*, anche quando trovano 2 CVE su 6: ciò che affermano è vero, è ciò che *non affermano* che li rende incompleti. Il coverage a superfici non lo cattura (i report di task6 toccano tutte le superfici, mancano 4 CVE *dentro* le superfici toccate — verificato a secco nel doc 12 Stato #1). **Nessuna rubrica sull'argomentazione può misurare la completezza: serve un enumeratore esterno di candidate** — il G5/SAST del team, o la GT stessa.

## 3. Verdetto contro i target dichiarati (doc 12 §6)

| Criterio di successo | Target v2 | Misurato | |
|---|---|---|---|
| CGP | > +0.437, idealmente > +0.6 | **+0.600** | ✅ |
| C2 promossi a t=0.65 | ≤ 1/5, task7 non a pieni voti | **0/5**, task7 a 0.61 | ✅ |
| C1 bocciati | 0/5 | 0/5 (C1 medio 0.983) | ✅ |
| Saturazione report reali | almeno i task6 sotto il massimo | tutti 10/10 | ❌ |
| Accordo M1-strict | ≥ 11/12 | 9/12 | ❌ |

**Ammissione parziale**: la v2 chiude i meccanismi di rottura 1 e 2 del doc 11 §3 *sul banco C1/C2* (claim di assenza ora falsificabili, conteggio che discrimina i report falsi), ma il meccanismo 3 — la completezza — è confermato **strutturale**: i due target falliti sono entrambi lo stesso fallimento, e nessuna variante di rubrica lo può chiudere. Il divario residuo CGP (+0.948 vs +0.600) e l'accordo 9/12 sono il prezzo *incomprimibile* del GT-free a livello di rubrica.

## 4. Cosa significa per il gruppo

1. **Come detector di report falsi ben scritti** la v2 è utilizzabile: zero falsi positivi e zero falsi negativi sul banco C1/C2, con motivazioni verificabili.
2. **Come sostituto del giudice GT-derivato nel loop** non lo è (né può diventarlo per raffinamento della rubrica): sui report *sinceri ma incompleti* serve la GT o un suo surrogato. La divisione dei compiti naturale: rubrica v2 = qualità/veridicità dell'argomentazione; enumeratore esterno (G5/SAST) = completezza.
3. La scala CGP ora ha tre punti fermi riproducibili: **+0.948** (GT-derivata) / **+0.600** (v2, meglio del pavimento v1 +0.437) / il gap residuo ≈ 0.35 è la quota "completezza" non recuperabile senza enumeratore.
