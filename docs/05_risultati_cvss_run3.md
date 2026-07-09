# Esperimento 2b — Run 3: REPETITIONS=3, stesso hint di contesto NF

> Documento di condivisione per il team. Stesso setup della [run 2](04_risultati_cvss_run2.md) (task5–9, 1A/1B, expert/beginner, `gemma4:31b-cloud`, hint di contesto NF attivo), con un'unica differenza: **3 ripetizioni per combinazione invece di 1** (60 run totali invece di 20). Obiettivo: capire se gli effetti osservati in run 2 (F8–F11) erano reali o rumore a singolo campione — punto esplicitamente lasciato aperto in run 2 §4 e nella lista "da chiudere col team".

**Data run:** 2026-07-09 · **Autore:** Nicolò (con supporto AI) · **Run precedenti:** [run 1](02_risultati_cvss_run1.md) (senza hint, 1 rep, archiviata in `results/_baseline_run1_no_context_hint_20260709/`), [run 2](04_risultati_cvss_run2.md) (con hint, 1 rep, archiviata in `results/_run2_hint_1rep_20260709/`)

---

## 0. Cosa cambia rispetto alla run 2

**Un solo parametro:** `--repetitions 3` invece di `--repetitions 1`. Prompt, hint di contesto NF, modelli, task, GT — tutto identico alla run 2. `TEMPERATURE=0.3` invariata: è proprio perché non è zero che le 3 ripetizioni danno 3 campioni realmente diversi dello stesso prompt, non 3 copie identiche (vedi [01_proposta_rubrica_cvss.md §8](01_proposta_rubrica_cvss.md#8-discussione-post-condivisione-2026-07-09--esiti-col-team) per la discussione con Andrea su questo punto).

Questa run **chiude il punto "REPETITIONS=3"** della lista aperta in [01_proposta_rubrica_cvss.md](01_proposta_rubrica_cvss.md) e in run 2 §4 — dopo questa run sappiamo quali effetti di run 2 erano reali.

---

## 1. Risultati d'insieme — per blocco e per ruolo

### Blocco A — rubrica testuale (60 run: 5 task × 2 esperimenti × 2 ruoli × 3 rep)

| | correct | avg score normalizzato | wrong |
|---|---|---|---|
| **Tutti** | 59/60 (98.3%) | 0.941 | task7_vuln_amf / 1B **expert** / rep 3 |
| **expert** | 29/30 | 0.941 | task7_vuln_amf / 1B / rep3 |
| **beginner** | 30/30 | 0.941 | — |
| **1A** | 30/30 | 0.945 | — |
| **1B** | 29/30 | 0.937 | task7_vuln_amf / 1B expert / rep3 |

**Osservazione che chiude il dubbio di Andrea (19/20 = "poca differenza tra i ruoli").** Con più campioni la distribuzione dei ruoli si ribalta: qui è l'**expert** a sbagliare (in run 1 e run 2, entrambe a 1 rep, era sempre il beginner). Stesso task (task7), stesso esperimento (1B), stesso normalized_score medio complessivo (0.941 per entrambi i ruoli). **Conclusione: non c'è un effetto di ruolo — c'è un unico punto fragile del sistema (task7 in setup 1B), e quale ruolo ci cade sopra è determinato dal rumore di campionamento (T=0.3), non da una differenza sistematica expert/beginner.** Con 1 sola ripetizione questo non era distinguibile da un vero effetto di ruolo; con 3 lo è.

### Blocco B — CVSS (48 finding abbinati a una CVE su 48 possibili; task9 sempre `null`, F4 di run 1)

| | n | impatto (VC/VI/VA) | exploitability | banda vs pubblicato | banda vs base B |
|---|---|---|---|---|---|
| **Run 3 (hint, 3 rep)** | 48 | 0.77 / 3 (σ=0.55) | 4.02 / 5 | 1.23 / 3 | 0.75 / 3 |
| Run 2 (hint, 1 rep) | 15 | 0.93 / 3 | 4.00 / 5 | 1.53 / 3 | 0.73 / 3 |
| Run 1 (no hint, 1 rep) | 16 | 1.00 / 3 | 4.75 / 5 | 1.62 / 3 | 1.56 / 3 |
| Run 3 — expert | 24 | 0.71 / 3 | 4.00 / 5 | 1.12 / 3 | — |
| Run 3 — beginner | 24 | 0.83 / 3 | 4.04 / 5 | 1.33 / 3 | — |

**Con più campioni il quadro si conferma e si aggrava, non si smentisce**: l'impatto scende ulteriormente (0.77/3, era 0.93 a 1 rep). Non è un caso sfortunato della run 2 — con 3× i dati la media scende ancora. **F8 di run 2 (l'hint minimo non corregge il bias di confidenzialità) è confermato, non era rumore.**

---

## 2. Per-task: cosa era rumore e cosa no (il punto centrale di questa run)

| Task | GT score (tipo) | Impatto | Banda vs pubblicato | Banda vs base B | σ score stimato | Verdetto |
|---|---|---|---|---|---|---|
| task5 (CVE-41135, DoS puro VA:H) | 8.7 (B) | 1.08/3 | **0.08/3** | 0.08/3 | 1.11 | Peggio di quanto sembrasse |
| task6 (CVE-40246, VC:H/VI:H/VA:H) | 8.7 (B) | 0.67/3 | 1.33/3 | 1.33/3 | 0.64 | F3/F11 confermato, ferro |
| task7 (CVE-41136, VI:L) | 5.5 (BT) | 1.00/3 | **2.33/3** | 1.42/3 | 1.16 | F10 confermato reale |
| task8 (CVE-42459, VC:H) | 7.7 (BT) | 0.33/3 | 1.17/3 | 0.17/3 | 0.50 | F9 confermato reale |

**task5 — non solo "non migliorato", instabile.** In run 2 (1 rep) sembrava un fallimento uniforme e prevedibile (tutte e 4 le combinazioni su `VC:L`/`VC:H`, banda 0). Con 3 rep si vede che gli score oscillano parecchio (3.1–7.1, σ=1.11) pur restando quasi sempre lontani dal published (8.7) — la banda media crolla a 0.08/3. L'hint non stabilizza nulla su questo task, anzi il modello sembra più incerto, non più accurato.

**task6 — F3/F11 è un comportamento di ferro, non rumore.** Su **tutti e 12 i run** (3 rep × 4 combinazioni) il matching abbina *esattamente* `CVE-2026-40246` e mai le altre due (`40247`, `40248`). Zero varianza sul pattern di aggregazione — il modello descrive sempre il "return mancante" come un solo finding collettivo, indipendentemente da ruolo, esperimento o campionamento. Prima di questa run era plausibile pensare che fosse un caso della singola ripetizione; ora è chiaro che è **strutturale**: il modello non enumera gli handler singolarmente, punto.

**task7 — il segnale positivo di run 2 (F10) è confermato reale.** Banda media vs pubblicato sale a 2.33/3 (era 1.53 nell'aggregato di run 2, e il singolo campione di run 1 era andato malissimo con 1B expert a banda 0). Con 3 rep, la maggioranza degli score resta vicina al published (5.5), con un solo outlier basso (2.3) — proprio nel run che la rubrica ha segnato `wrong` (task7/1B/expert/rep3): quando l'agente sbaglia la review testuale, sbaglia anche la stima CVSS nello stesso tentativo. Comprensibile: stessa generazione, stesso errore di comprensione del codice si propaga a entrambi i blocchi anche se sono valutati separatamente.

**task8 — F9 è confermato reale, e peggio di quanto sembrasse.** Banda vs base B crolla a 0.17/3 (quasi il minimo). Gli score restano quasi sempre intorno a 5.1 (bassa varianza, σ=0.50) mentre il published è 7.7 — non è rumore, è un **bias sistematico verso il basso**, coerente con l'ipotesi F9: l'hint "OAuth2/TLS attivi di default" sembra convincere il modello che la severità reale sia più bassa di quella che è, per un bug che in realtà bypassa comunque la validazione applicativa (SUPI).

---

## 3. Findings (continuano la numerazione di [run 2](04_risultati_cvss_run2.md))

**F12 — Il presunto effetto di ruolo su task7 non esiste: è rumore di campionamento su un punto fragile del sistema.** Chiude direttamente il dubbio di Andrea sulla run 1. Con 1 rep sembrava sempre il beginner a fallire; con 3 rep fallisce l'expert. Stesso task, stesso setup (1B), stesso normalized_score medio tra ruoli (0.941 = 0.941). Non riportare più "il beginner è più debole su task7" — è falso, ed era un artefatto della singola ripetizione.

**F13 — F8 di run 2 confermato: l'hint minimo non corregge il bias di confidenzialità, ed è ancora più marcato con più campioni.** Impatto medio 0.77/3 su 48 osservazioni (era 0.93/3 su 15). Il worst case è task5 (banda 0.08/3): il DoS puro resta quasi sempre letto come problema di confidenzialità nonostante l'hint lo scoraggi esplicitamente.

**F14 — F3/F11 (matching aggregato task6) è un comportamento strutturale, zero varianza su 12 run.** Il modello non abbina mai più di 1 CVE su 3 nel task6, in nessuna delle 12 combinazioni provate. Non serve più verificarlo con altre ripetizioni: è stabile e va trattato come limite noto del sistema, non come rumore da mediare via.

**F15 — F10 (miglioramento su task7) e F9 (peggioramento su task8) sono entrambi confermati reali, in direzioni opposte.** Stesso hint, stesso tipo di CVE (score BT, metriche threat E incluse), effetti opposti: task7 migliora nettamente (banda 2.33/3), task8 peggiora nettamente (banda 0.17/3). Questo esclude una spiegazione "l'hint aiuta sempre" o "l'hint confonde sempre" — l'effetto è **specifico alla CVE**, non generico. Rende ancora più fragile l'idea di un hint unico e generico per tutti i task; motiva l'idea (già in `03_discussione_post_01_02.md`, proposta Mariano/Andrea) di contesto più ricco e specifico per NF, non una frase valida per tutte.

**F16 — Un errore di rubrica si accompagna a una stima CVSS peggiore nello stesso tentativo (task7/1B/expert/rep3).** L'unico caso `wrong` di questa run ha anche lo score CVSS più lontano dal published (2.3 vs 5.5) tra tutti i 12 campioni di task7. Coerente col fatto che è la stessa generazione a produrre sia la review testuale sia la stima CVSS: un fraintendimento del codice si propaga a entrambi i blocchi anche se vengono poi valutati da meccanismi indipendenti (giudice LLM vs script).

---

## 4. Che cosa dire al team

Il punto "REPETITIONS=3 per chiudere la questione" è ora **chiuso con una risposta netta**: non era rumore. Con 3× i dati, i findings di run 2 non si diluiscono — si confermano (F8/F13, F9/F15-task8) o si rafforzano (F3/F14, quasi deterministico), tranne uno che si **capovolge** (il presunto effetto di ruolo su task7, F12): quello sì era rumore puro a 1 rep, ed è la controprova diretta che l'obiezione di Andrea su REPETITIONS era fondata.

Messaggio di sintesi per il team: l'hint minimo di Lorenzo non risolve il problema generale di F2 (impatto sbagliato), ma **non è neutro** — aiuta chiaramente su una CVE (task7) e danneggia chiaramente un'altra (task8). Questo sposta la discussione: non è più "l'hint funziona o non funziona", ma "un hint di contesto generico ha effetti opposti su CVE diverse, quindi serve un contesto più specifico per NF/endpoint" — esattamente la direzione già proposta da Mariano/Andrea (passare tutto free5GC) o un'alternativa intermedia (hint specifico per task, non uno unico per tutti i task vuln).

**Prossimo passo:** decidere se investire nella variante costosa (tutto free5GC come contesto) o testare prima hint differenziati per task/NF, mantenendo REPETITIONS=3 come standard d'ora in poi per ogni nuova variante — il costo (3× le chiamate) è ormai giustificato dal fatto che a 1 rep si sarebbero tratte conclusioni sbagliate su F12.

---

## 5. Come riprodurre

```bash
poetry run python main.py \
  --task task5_vuln_pcf --task task6_vuln_udr --task task7_vuln_amf \
  --task task8_vuln_udm --task task9_vuln_cross \
  --repetitions 3 --task-timeout 240
```

`CVSS_CONTEXT_HINT_ENABLED = True` in `config.py` (invariato dalla run 2). I risultati grezzi di run 2 (1 rep, stesso hint) sono archiviati in `results/_run2_hint_1rep_20260709/`; quelli di run 1 (senza hint) in `results/_baseline_run1_no_context_hint_20260709/` — stessa struttura `results/<task>/<exp>/<role>/`.
