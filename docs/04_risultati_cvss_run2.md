# Esperimento 2b — Run 2: hint di contesto NF (Lorenzo) su impatto CVSS

> Documento di condivisione per il team. Stesso setup della [run 1](02_risultati_cvss_run1.md) (task5–9, 1A/1B, expert/beginner, `gemma4:31b-cloud`), con un'unica differenza: il prompt ora include un paragrafo di contesto di sistema (proposta di Lorenzo Cannella, [discussione post-01/02](03_discussione_post_01_02.md)) prima del blocco istruzioni CVSS. Obiettivo: capire se F2 (impatto sbagliato sistematicamente, default a confidenzialità) dipende dalla mancanza di contesto sul ruolo della NF nel sistema più ampio.

**Data run:** 2026-07-09 · **Autore:** Nicolò (con supporto AI) · **Baseline di confronto:** run 1, archiviata in `results/_baseline_run1_no_context_hint_20260709/`

---

## 0. Cosa cambia rispetto alla run 1

Un solo paragrafo aggiunto in [`utils/cvss_utils.py`](../utils/cvss_utils.py) (`NF_CONTEXT_HINT`), iniettato subito prima del blocco istruzioni CVSS, gate da `config.CVSS_CONTEXT_HINT_ENABLED`:

> *"the code under review is a Network Function (NF) inside a 5G core network (free5GC architecture). In a standard 5G core deployment, the Service-Based Interface (SBI) between NFs runs behind mutual TLS and OAuth2 authorization by default. Use this when judging the impact... do not assume a bug automatically exposes data — consider what is actually reachable or corrupted given this baseline."*

Tutto il resto — task, rubrica, GT, flusso di valutazione a due blocchi — è **identico alla run 1** (vedi [risultati_cvss_run1.md §1](02_risultati_cvss_run1.md#1-setup-della-fase-di-test) per il dettaglio del flusso). Questa è la variante "economica" discussa col team, testata prima di investire nel passare l'intero free5GC come contesto (proposta di Andrea/Mariano).

> ⚠️ **Limite di questa run: 1 sola ripetizione per combinazione**, come la run 1. I confronti sotto sono indicativi, non statisticamente solidi — è lo stesso limite già segnalato per la run 1, e resta il motivo principale per chiudere col team il punto REPETITIONS=3.

---

## 1. Risultati d'insieme — per blocco **e per ruolo**

> Nota: questa run divide esplicitamente i dati per ruolo (expert/beginner) e per esperimento (1A/1B) fin dal primo sguardo — nella run 1 la mancata suddivisione ha generato l'ambiguità sollevata da Andrea Bernardini ("19/20 è l'unione di beginner ed expert?"). Non è il focus di questa run (che è il Blocco B), ma evita di riproporre la stessa domanda.

### Blocco A — rubrica testuale

| | correct | avg score normalizzato | wrong |
|---|---|---|---|
| **Tutti (20 run)** | 19/20 (95%) | 0.939 | task7_vuln_amf / 1B beginner |
| **expert** | 10/10 | 0.956 | — |
| **beginner** | 9/10 | 0.922 | task7_vuln_amf / 1B |
| **1A** | 10/10 | 0.956 | — |
| **1B** | 9/10 | 0.922 | task7_vuln_amf / 1B beginner |

Identico alla run 1 in ogni dettaglio, incluso l'unico caso `wrong`. Atteso: il Blocco A non riceve mai la stima CVSS né l'hint di contesto CVSS-specifico è nella sezione di prompt che il giudice vede diversamente — la rubrica valuta la review testuale, il cui contenuto non è cambiato. **Conferma l'indipendenza dei due blocchi**, coerente col disegno sperimentale.

### Blocco B — CVSS (solo finding abbinati a una CVE, n=15/16 possibili — task9 sempre `null`, vedi F4 in run 1)

| | n | impatto (VC/VI/VA) | exploitability | banda vs pubblicato | banda vs base B |
|---|---|---|---|---|---|
| **Run 2 (con hint), tutti** | 15 | **0.93 / 3** | 4.00 / 5 | 1.53 / 3 | 0.73 / 3 |
| **Run 1 (senza hint), tutti** | 16 | 1.00 / 3 | 4.75 / 5 | 1.62 / 3 | 1.56 / 3 |
| Run 2 — expert | 7 | 1.00 / 3 | 4.00 / 5 | 1.57 / 3 | — |
| Run 2 — beginner | 8 | 0.88 / 3 | 4.00 / 5 | 1.50 / 3 | — |

**Il messaggio in una riga: l'hint minimo non ha migliorato l'impatto, e su alcune metriche è leggermente peggiorato.** Nessuna delle due dimensioni CVSS beneficia chiaramente del paragrafo di contesto aggiunto — vedi §3 per il dettaglio per-task, che spiega da dove viene il calo.

---

## 2. Confronto diretto run 1 → run 2, per CVE

Stessa CVE, stessa combinazione (task/esperimento/ruolo), unica variabile = presenza dell'hint. `banda` = punti secondo `CVSS_SCORE_BANDS` (±0.5→3, ±1.5→2, ±3.0→1, altrimenti 0), vs score pubblicato.

| Task | Combo | Score run1 → run2 | Banda run1 → run2 | Vettore impatto run2 |
|---|---|---|---|---|
| task5 (CVE-41135, GT VA:H puro, 8.7) | 1A expert | 5.1 → 5.3 | 0 → 0 | `VC:L/VI:N/VA:N` |
| | 1A beginner | 5.1 → 5.3 | 0 → 0 | `VC:L/VI:N/VA:N` |
| | 1B expert | 6.8 → 5.3 | **1 → 0** | `VC:L/VI:N/VA:N` |
| | 1B beginner | 5.3 → 5.1 | 0 → 0 | `VC:L/VI:N/VA:N` |
| task6 (CVE-40246, GT VC:H/VI:H/VA:H, 8.7) | 1A expert | 9.3 → — | 2 → **nessun match (0/3 CVE)** | — |
| | 1A beginner | 9.3 → 7.7 | 2 → 2 | `VC:H/VI:H/VA:H` |
| | 1B expert | 9.3 → 7.7 | 2 → 2 | `VC:H/VI:H/VA:H` |
| | 1B beginner | 9.3 → 7.1 | 2 → **1** | `VC:H/VI:H/VA:H` |
| task7 (CVE-41136, GT VI:L, 5.5 BT) | 1A expert | 5.1 → 5.3 | 3 → 3 | `VC:N/VI:N/VA:H` |
| | 1A beginner | 5.3 → 5.3 | 3 → 3 | `VC:N/VI:N/VA:H` |
| | 1B expert | 8.7 → 5.3 | **0 → 3** | `VC:N/VI:N/VA:H` |
| | 1B beginner | 5.1 → 5.3 | 3 → 3 | `VC:N/VI:N/VA:H` |
| task8 (CVE-42459, GT VC:H, 7.7 BT) | 1A expert | 8.7 → 6.7 | 2 → 2 | `VC:H/VI:H/VA:L` |
| | 1A beginner | 8.7 → 5.1 | 2 → **1** | `VC:L/VI:L/VA:L` |
| | 1B expert | 8.4 → 5.1 | 2 → **1** | `VC:L/VI:N/VA:L` |
| | 1B beginner | 8.7 → 6.2 | 2 → 2 | `VC:H/VI:L/VA:L` |

Letture per task:

- **task5 — nessun miglioramento.** L'hint dice esplicitamente "non dare per scontato che un bug esponga dati automaticamente", eppure tutte e 4 le combinazioni restano su `VC:L`/`VC:H` invece di riconoscere il DoS puro (`VA:H`, `VC:N`). Un caso, 1B expert, addirittura **peggiora** (perdeva 1 punto di banda che prima aveva). L'hint non ha smosso il pattern.
- **task6 — comportamento di matching invariato (F3 di run 1), non toccato dall'hint.** Resta al massimo 1 CVE abbinata su 3 per combinazione — un caso (1A expert) ora ne abbina addirittura 0/3. Confermato: F3 è un comportamento di aggregazione dei finding, indipendente dal contesto di sistema.
- **task7 — unico segnale positivo, ma va letto con cautela.** In run 1 il caso 1B expert era un outlier isolato (score 8.7, vettore quasi opposto alla GT); in run 2 tutte e 4 le combinazioni convergono sullo stesso vettore e la stessa banda massima. Potrebbe indicare che l'hint riduce la varianza di ragionamento su questo task specifico — ma con **1 sola ripetizione per combinazione non possiamo distinguere "l'hint ha aiutato" da "questa volta è girata bene"**. Va riverificato con REPETITIONS≥3.
- **task8 — peggioramento netto.** La banda media scende da 2.0 a 1.5: gli score stimati si abbassano (da ~8.5 a 5–6) allontanandosi dal 7.7 di GT. Ipotesi: l'hint, enfatizzando "OAuth2/TLS attivi di default", può aver spinto il modello a **sottostimare la gravità** di un bypass di validazione (SUPI) che aggira comunque l'autenticazione applicativa — un effetto collaterale opposto a quello cercato.

---

## 3. Findings (continuano la numerazione di [risultati_cvss_run1.md](02_risultati_cvss_run1.md))

**F7 — Il Blocco A è insensibile all'hint CVSS, come atteso.** Rubrica invariata in ogni singolo verdetto rispetto alla run 1 (19/20, stesso unico wrong). Conferma diretta che i due blocchi restano indipendenti anche quando si modifica il prompt CVSS-specifico.

**F8 — L'hint minimo non corregge il bias verso la confidenzialità (F2 di run 1 non risolto).** Impatto medio 0.93/3 (era 1.00/3): nessun miglioramento, leggero peggioramento. Il caso più chiaro è task5, dove l'hint dice esplicitamente di non assumere esposizione dati automatica, eppure il modello continua a stimare `VC:L`/`VC:H` invece del DoS puro della GT. Una frase di contesto di sistema non basta a spostare quello che sembra un prior strutturale del modello (associare "vulnerabilità" a "esposizione dati") più che una lacuna informativa colmabile con un hint testuale.

**F9 — task8 peggiora, possibile effetto collaterale dell'hint (da verificare).** La banda media scende da 2.0 a 1.5; gli score si abbassano proprio sul task dove GT è high-severity (7.7). Ipotesi da testare: enfatizzare "OAuth2/TLS di default" può portare il modello a sottostimare bug che bypassano comunque l'autenticazione applicativa (validazione SUPI). Se confermato con più ripetizioni, sarebbe un argomento contro l'hint generico "il sistema è sicuro di base" e a favore di un hint più specifico per NF/endpoint.

**F10 — task7 mostra meno varianza tra le combinazioni (positivo, ma n=1 non basta).** Le 4 combinazioni convergono sullo stesso vettore/score in run 2, mentre in run 1 un caso divergeva nettamente. Segnale interessante ma non conclusivo — richiede repliche per non confondere riduzione di varianza con rumore favorevole di una singola esecuzione.

**F11 — Il comportamento di aggregazione dei finding (F3, task6) è indipendente dal contesto di sistema.** L'hint non cambia il fatto che i modelli riportino il pattern "return mancante" come un solo finding invece di 3 handler separati — anzi in un caso il matching per-funzione fallisce completamente (0/3). Conferma che F3 è un limite del modo in cui il modello enumera i finding, non della mancanza di contesto NF.

---

## 4. Che cosa dire al team

L'esperimento economico proposto da Lorenzo è stato provato **e, su questo singolo campione, non ha risolto il problema di F2** — anzi in 2 task su 4 (task5, task8) il risultato è invariato o peggiore, in 1 (task7) è migliorato ma non è distinguibile dal rumore, in 1 (task6, F3) non è pertinente. Questo è un dato onesto da riportare, non un fallimento dell'esperimento: **restringe le ipotesi**. Se un singolo paragrafo di contesto di sistema non sposta l'ago, il problema di F2 sembra meno "manca un'informazione" e più "il modello ha un'associazione di default vulnerabilità→confidenzialità" che serve più contesto (o un prompt più mirato per singola metrica di impatto) per essere corretta.

Prossimo passo naturale, coerente con quanto discusso: o (a) la variante costosa di Andrea/Mariano — passare tutto free5GC come contesto — o (b) prima ancora, ripetere questa stessa run con REPETITIONS=3 per capire se F9/F10 sono effetti reali o rumore a n=1, prima di investire nel refactor più grosso.

---

## 5. Come riprodurre

```bash
# CVSS_CONTEXT_HINT_ENABLED = True in config.py (default dopo questa run)
poetry run python main.py \
  --task task5_vuln_pcf --task task6_vuln_udr --task task7_vuln_amf \
  --task task8_vuln_udm --task task9_vuln_cross \
  --repetitions 1 --task-timeout 240
```

Per riprodurre la run 1 (senza hint): impostare `CVSS_CONTEXT_HINT_ENABLED = False` in `config.py`. I risultati grezzi della run 1 sono archiviati in `results/_baseline_run1_no_context_hint_20260709/` (stessa struttura di `results/<task>/<exp>/<role>/`).
