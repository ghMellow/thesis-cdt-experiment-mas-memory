# Template — documento di risultati per una run

> Non è un report di run: è lo **scheletro** da copiare per scrivere il prossimo `docs/0N_risultati_*.md` (finora 02→07). Nato dal problema del doc 07: due domande dell'utente ("questi numeri si evincono dal doc?" / "la gestione dei risultati è un po' problematica") hanno mostrato che (a) affermazioni puntuali finivano nel testo senza modo di riverificarle, (b) capire quali dati appartenessero a quale run richiedeva script ad hoc. Con `run_id` (vedi `architecture.md` §7) il punto (b) è ormai automatico; questo template codifica cosa aggiungere di *proprio* oltre a `results/evaluation/*.md`, che ora si genera da solo.

---

## Cosa fa GIÀ `results/evaluation/*.md` — non ripeterlo qui

Prima di scrivere il doc, apri i report rilevanti (`result_<task>_<exp>.md`, `comparison.md`) e guarda cosa contengono già:

- blocco `> **Run(s) in this report:**` — provenienza (ruolo + run_id) dei dati aggregati
- Summary: total/correct/wrong/retried/inconsistent
- Anomalies: wrong verdicts, retry triggered, inconsistenze di reasoning (con classificazione LLM vera-inconsistenza vs parafrasi)
- Scores by role: accuracy, confidence, brier score, avg_attempts, avg_textual_norm/avg_math_delta
- CVSS estimate: tabella diagnostica (score dichiarato), tabella "Official CVSS 4.0 math" (score ricalcolato — quella che conta), vector detail per-CVE, **Unmatched findings rankati per triage**
- comparison.md: accuracy 1A vs 1B per ruolo

**Il doc di run non deve copiare queste tabelle.** Deve rispondere a una domanda che le tabelle da sole non rispondono: *cosa significa, perché, e cosa cambia rispetto a prima.*

---

## Prima di scrivere: identifica la run

```bash
poetry run python -m utils.evaluation_utils --list-runs
```

Annota il/i `run_id` esatti che il doc descrive (o l'intervallo di `earliest`, se sono risultati "legacy" pre-`run_id`). Se serve isolare solo quella run nei calcoli, usa:

```bash
poetry run python -m utils.evaluation_utils --run-id <id>
```

Questo rigenera i report *scoped* a quella run soltanto — è la sostituzione diretta dello script ad hoc scritto a mano per il doc 07.

---

## Scheletro (sezioni — ometti quelle senza contenuto)

```markdown
# Esperimento 2b — Run N: <una riga sul cambiamento testato>

> Una frase su cosa cambia rispetto alla run precedente e perché la si è lanciata (quale dubbio/proposta la motiva — cita la call o il messaggio utente se pertinente).

**Data run:** · **Autore:** · **Run precedente:** [link] · **run_id:** <valore da --list-runs, o "legacy">

---

## 0. Cosa cambia rispetto alla run precedente
Elenco puntuale: task/prompt/modelli/valutazione toccati. Se un parametro NON cambia ma potrebbe sembrare rilevante, dillo esplicitamente (es. "agente e giudice restano lo stesso modello" — un caveat, non un'ovvietà).

## 1. Risultati d'insieme
Tabelle **compatte**, aggregate al livello che il lettore userà per orientarsi (per-task va bene, per-attempt no — quello sta già nel JSON/nel report evaluation). Ogni numero riportato qui deve essere ottenibile da un comando o da un file citato, non da un calcolo mentale non tracciato.

## 2. Per-task (o per-condizione): cosa dice il dato che l'aggregato nasconde
Qui vive il valore aggiunto vero: legare un numero a un **meccanismo** ("perché succede", non solo "quanto"). Se l'affermazione è puntuale (es. "sub-score X è 0.0 in tutti i tentativi"), scrivi anche *come l'hai verificato* — anche solo un percorso di campo JSON, non serve lo script intero.

## 3. Findings (continua la numerazione dalla run precedente)
Una entry per scoperta, non per tabella. Formato: **Fnn — affermazione in una riga.** poi 2-4 frasi con l'evidenza e, se c'è, l'implicazione operativa (per il codice, per l'articolo, per l'esperimento 3).

## 4. Che cosa dire al team
La sintesi orientata alla decisione: cosa è confermato, cosa è cambiato rispetto all'aspettativa, quali cautele (dimensione campione, confound non isolati). Punti aperti come lista puntata, non prosa.

## 5. Come riprodurre
Comando `main.py` esatto. Se la run richiede uno stato particolare (cartelle spostate, config diversa dal default), dillo qui — è la sezione che rende il documento eseguibile da chiunque, non solo leggibile.
```

---

## Checklist prima di pubblicare/committare

- [ ] Ogni numero puntuale (non aggregato) ha un modo dichiarato di essere riverificato (percorso JSON, comando, o riferimento al report evaluation)
- [ ] Il `run_id`/intervallo di questa run è scritto in testa — se i dati sono "legacy" (pre-`run_id`), dillo esplicitamente
- [ ] Nessuna tabella duplicata da `results/evaluation/*.md` — solo interpretazione o dati che quei report non calcolano (es. confronto tra run diverse, causalità ipotizzata)
- [ ] I findings continuano la numerazione della run precedente, non ripartono da F1
- [ ] Le cautele/limiti del campione sono dichiarati, non solo le conclusioni positive
- [ ] `docs/README.md` e `docs/status.md` aggiornati con il puntatore al nuovo doc
