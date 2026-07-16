# 03 — Discussione: LLM-as-a-Verifier come strada per il nostro giudice

> Documento di discussione (2026-07-16). Analizza il paper riportato nel doc 02 (Kwok et al., arXiv:2607.05391) e valuta se e come le sue idee possono migliorare il giudice a rubrica descritto nel doc 01. Contiene la valutazione di Claude — da discutere, nulla è deciso.

## 1. Cosa dice il paper, in tre righe

Un giudice LLM standard fa emettere al modello *un token* di punteggio discreto e prende il più probabile: collassa la distribuzione e produce valutazioni grossolane (tie rate 27% su Terminal-Bench). LLM-as-a-Verifier calcola invece il **valore atteso sulla distribuzione dei logit dei token di punteggio** → score continui, zero tie, e tre assi di scaling indipendenti: **granularità** della scala (G, fino a 20 livelli), **ripetizione** delle valutazioni (K, riduce la varianza come 1/K), **decomposizione in criteri** (C, riduce il bias del criterio monolitico). Il tutto training-free e cross-dominio.

## 2. Mappa sul nostro sistema: cosa abbiamo già, cosa no

| Asse del paper | Da noi oggi | Distanza |
|---|---|---|
| Criteria decomposition (C) | ✅ già presente: la rubrica è per-criterio (3 dimensioni in task7), aggregata per somma | Vicina — ma i nostri criteri sono GT-derivati, i loro sono generici per-dominio (Specification / Output / Errors) |
| Repeated evaluation (K) | ❌ un solo giudizio per attempt | Banale da implementare: K chiamate al giudice, media — costa K× in token (misurabile con M5) |
| Score granularity (G) + expectation sui logit | ❌ score interi 0–2/0–4, argmax implicito | Richiede accesso ai **logprobs** dei token di punteggio |
| Pairwise + tournament (PPT) | ❌ giudichiamo in assoluto contro soglia, non selezioniamo tra N candidati | Cambio di paradigma — vedi §4 |

Punto notevole: la nostra rubrica fa già la cosa che il paper chiama criteria decomposition, quindi il salto concettuale non è "aggiungere struttura" ma **cambiare come si estrae il punteggio** (distribuzione invece di argmax) e **quanto si campiona** (K>1).

## 3. Fattibilità tecnica nel nostro stack

- **Logprobs.** Il metodo pieno richiede i logprob dei token di punteggio. Da verificare cosa espone la versione di Ollama in uso (endpoint nativo e OpenAI-compatible) sia in locale sia su Ollama Cloud — su cloud già oggi perdiamo `prompt_eval_count`/`eval_count` (vedi nota M5 in `status.md`), quindi l'accesso ai logprob non è scontato.
- **Workaround senza logprobs.** L'appendice B.6 del paper offre una via a due stadi per modelli chiusi; e in ogni caso i due assi K (ripetizione) e C (già nostro) non richiedono logprob. Un surrogato povero ma onesto della distribuzione: K giudizi a T>0 e media dei punteggi — è già "expectation via sampling", con convergenza più lenta.
- **Scala 1–20 con token-lettera.** Il trucco della scala a lettere (per estrarre un solo token di score) è a costo zero e applicabile anche senza logprob per ridurre i tie della scala 0–4.

## 4. Dove il paper NON risponde al nostro problema

Due disallineamenti da tenere presenti, per non comprare il paper "a scatola chiusa":

1. **Selezione vs accettazione.** Il paper seleziona il migliore tra N traiettorie (best-of-N, pairwise): non ha bisogno di uno zero assoluto. Noi decidiamo *accetta/rifiuta un singolo report* contro una soglia: il punteggio continuo aiuta (verdetti più stabili vicino alla soglia), ma la calibrazione della soglia resta un problema nostro, non risolto dal paper. Uso alternativo coerente col paper: generare N report per task (abbiamo già REPETITIONS=3) e usare il verifier per *scegliere* quello da mandare alla misura — best-of-N sul nostro pipeline, con l'oracle gap misurabile perché abbiamo M1–M3.
2. **I criteri restano da scrivere.** Il paper assume criteri dati (e ammette in Appendix A che la decomposizione è hand-designed). Non ci dice come costruire una rubrica **senza ground truth** — che è il nostro limite di fondo (doc 01 §4). Però la sua decomposizione Specification/Output/Errors è *GT-free per costruzione*: valuta proprietà del processo e del report, non la corrispondenza con una soluzione nota. Questo è il suggerimento più utile del paper per noi, più ancora dei logprob.

## 5. Valutazione di Claude

**Sì, è una strada, ed è migliore dell'idea "rubrica = workflow dell'esperto di sicurezza" come asse portante** (discussa nel doc 04 §2 — le due cose però possono convergere). Ragioni:

- Attacca esattamente due delle debolezze empiriche del doc 01: verdetti non riproducibili (K>1 + score continuo ⇒ varianza controllata e misurabile) e granularità grossolana (tie e cliff-effect alla soglia 0.7).
- È **incrementale**: si può adottare a strati senza rifare il giudice — (a) K ripetizioni + media, (b) scala 1–20, (c) expectation sui logprob se Ollama li espone, (d) best-of-N. Ogni strato è un esperimento con metrica di confronto già pronta (accordo verdict-rubrica ↔ M1 deterministico).
- È coerente con la linea del relatore: non reintroduce leakage (il verifier valuta, non suggerisce; il feedback in-loop resta all'SGV), e rende il giudizio *più* riproducibile e ispezionabile, non meno — con K fissato e seed/temperatura documentati, il punteggio atteso è un numero stabile.
- Attenzione all'onestà sperimentale: il paper usa Gemini 2.5 Flash come verifier; noi useremmo gemma piccoli. I guadagni di granularità presuppongono che il modello *abbia* una credenza interna più fine della scala — su un giudice al limite di capacità (doc 01 §3.6) l'effetto potrebbe essere molto ridotto. Da misurare, non da assumere.

**Rischio principale**: costo. K=8–16 moltiplica le chiamate del giudice; con M5 in mano possiamo però quantificare il trade-off accuratezza/costo esattamente come fa il paper (Fig. 4), che è un risultato presentabile in tesi di per sé.

**Proposta operativa minima** (se il gruppo è d'accordo): un esperimento pilota su task7/8 — giudice attuale vs (K=5, scala 1–20, media) sugli stessi report già salvati in `results/` (il giudizio è rieseguibile offline sui report esistenti, come il recompute CVSS), confrontando la stabilità del verdict e l'accordo con M1. Zero modifiche al loop: solo rivalutazione.

## 6. Collegamento con la liberazione dalla ground truth

Il paper da solo non ci svincola dalla GT, ma indica la composizione che può farlo:

```
criteri GT-free (Specification / Groundedness / Error-awareness / Severity plausibility)
        × estrazione probabilistica dello score (G, K)
        = giudice riproducibile che misura la QUALITÀ del report, non l'aderenza alla soluzione
```

dove la groundedness è già garantita a monte dall'SGV (G2/G3) e quindi non spreca capacità del giudice. Le opzioni concrete per i criteri GT-free sono nel doc 04.
