# Call 2 — Security Review 5G (§8.11 + snapshot 2026-05-09)

Questa sessione è partita da una chat nel gruppo (Andrea Bernardini) sull'idea di testare LLM locali su CVE reali in codice Go free5GC.
Il sistema è stato esteso con i task security (task5–9) in vista della prossima call, in cui emergeranno i dubbi operativi (sezione "Domande aperte" in fondo).
Per lo stato corrente e i puntatori agli altri documenti vedi [status.md](../status.md).

---

## 8.11 Estensione a security code review su codice 5G reale

- **Dubbio (call, 2026-05-09)**: Andrea Bernardini chiede se il judge LLM puo' trovare vulnerabilita' reali in codice Go di NF free5GC — CVE gia' noti da analisi statica (Francesco). Il modello testato da Andrea con qwen2.5-coder:7b ha dato solo risposte generiche.
- **Situazione attuale**: aggiunti 4 task textual (`task5_vuln_pcf`, `task6_vuln_udr`, `task7_vuln_amf`, `task8_vuln_udm`) che forniscono codice Go di PCF/UDR/AMF/UDM e chiedono all'agente una security review cieca (senza GT). Ground truth = 9 CVE reali (GHSA) da `File_Free5gc_Vulnerabili/Patch_Spiegazione.md`. Analisi manuale in `File_Free5gc_Vulnerabili/ANALISI_VULNERABILITA.md` ha identificato 8 vulnerabilita' (V1-V8), 3 delle quali extra rispetto ai CVE ufficiali. Rubrica del judge valuta: identificazione classe vulnerabilita', localizzazione nel codice, impatto nel contesto 5G, proposta fix.
- **Proposte future**: confronto qwen2.5-coder vs modello general (setup 1A/1B); false positive rate come metrica aggiuntiva; baseline con strumento di analisi statica (gosec); esperimento con snippet vs file intero per misurare impatto context window.

> ✅ **Implementato:** creati task5–task9 (4 single-file + 1 cross-file) + varianti full-file per task6/7/8. Override modello per-task via `TASK_MODEL_OVERRIDES["beginner_1B"]["vuln"]`. Vedi dettagli nella sezione snapshot sotto.

---

## Snapshot sistema — 2026-05-09

### Task security review disponibili

| ID | Contenuto | Dimensione |
| --- | --- | --- |
| `task5_vuln_pcf` | PCF `setCorsHeader` — CORS AllowAllOrigins+AllowCredentials | 65 righe Go |
| `task6_vuln_udr` | UDR excerpt — missing return + regex `\|.+` | ~250 righe |
| `task6_vuln_udr_full` | UDR `api_datarepository.go` completo | 2891 righe |
| `task7_vuln_amf` | AMF excerpt — missing default + c.Set struct | ~120 righe |
| `task7_vuln_amf_full` | AMF `api_communication.go` completo | 501 righe |
| `task8_vuln_udm` | UDM excerpt — handler con/senza IsValidSupi | ~150 righe |
| `task8_vuln_udm_full` | UDM `api_subscriberdatamanagement.go` completo | 858 righe |
| `task9_vuln_cross` | Estratti da tutti e 4 i file — inconsistenze sistemiche cross-NF | multi-file |

### Ground truth security review (CVE reali)

Le vulnerabilità target dei task5–task9 sono CVE reali free5GC documentati in `File_Free5gc_Vulnerabili/Patch_Spiegazione.md`:

| NF | CVE / GHSA | Pattern |
| --- | --- | --- |
| PCF | GHSA-98cp-84m9-q3qp | CORS: AllowAllOrigins + AllowCredentials |
| UDR | GHSA-wrwh, g9cw, x5r2, jgq2, gx38, jwch (×6) | Missing `return` dopo risposta 404 |
| AMF | GHSA-r99v-75p9-xqm5 | Missing `default` nel Content-Type switch |
| UDM | GHSA-585v-hcgf-jhfr | Missing `validator.IsValidSupi()` in handler multipli |

Ulteriori vulnerabilità identificate con analisi manuale (non nei CVE ufficiali): regex inefficace UDR (`|.+`), c.Set struct leak AMF, NoSQL surface UDR query params → documentate in `File_Free5gc_Vulnerabili/ANALISI_VULNERABILITA.md`.

### Rubrica judge (comune a tutti i task security)

Tutte le rubriche security usano `total_max=9` e `TEXTUAL_PASS_RATIO=0.7` (score minimo correct = 6.3/9).
Le categorie variano per task ma la struttura è uniforme:

- identificazione vulnerabilità specifica (3–4 punti)
- localizzazione / secondo finding (2–3 punti)
- impatto nel contesto 5G (2 punti)

### Override modello per-task

`beginner_1B` usa `qwen2.5-coder:1.5b-base` per tutti i task il cui `task_id` contiene `"vuln"`.
Task3/task4 continuano a usare `deepseek-r1:latest` (default `beginner_1B`).

```python
# config.py
TASK_MODEL_OVERRIDES = {
    "beginner_1B": {
        "vuln": "qwen2.5-coder:1.5b-base",
    },
}
```

### Nota context window

`qwen2.5-coder:1.5b-base` ha context window di 32K token (confermato da specifiche ufficiali). Il crash su task5 (806 token in input, ben sotto il limite) non era quindi un problema di context window ma di **capacità**: con 1.54B parametri il modello non riesce a produrre output strutturato in modo stabile dopo più tentativi falliti. Fix implementato: passaggio a template Markdown con parsing dedicato e fallback JSON per garantire output strutturato invece di crash.

---

## Analisi risultati preliminari (2026-05-09, task5 + task6)

### Task 5 (PCF CORS, 65 righe) — risolto da tutti

| exp | role | model | avg norm |
| --- | --- | --- | --- |
| 1A | expert | gemma4:e2b | 0.93 |
| 1A | beginner | gemma4:e2b | 0.93 |
| 1B | expert | gemma4:e2b | 0.96 |
| 1B | beginner | deepseek-r1 | 1.00 |

File piccolo, pattern CORS noto nelle training data. Nessun modello ha difficoltà.

### Task 6 (UDR excerpt, ~250 righe) — 0/12 correct, fallimento sistematico

| exp | role | model | avg norm |
| --- | --- | --- | --- |
| 1A | expert | gemma4:e2b | 0.33 |
| 1A | beginner | gemma4:e2b | 0.48 |
| 1B | expert | gemma4:e2b | 0.00 |
| 1B | beginner | deepseek-r1 | 0.11 |

**`missing_return_score = 0` in tutte le 24 ripetizioni.** Il finding primario (6 GHSA, CVE ufficiali) non viene identificato da nessun modello. Il finding secondario (regex `|.+`) viene trovato parzialmente da gemma4:e2b in 1A ma non in 1B.

Interpretazione: il pattern `c.String(404) senza return` richiede di sapere che Gin non ferma Go dopo aver scritto la risposta — conoscenza framework-specifica non comune nelle training data di security review generica. Non è un pattern OWASP, non assomiglia a SQL injection o XSS.

**Anomalia 1A vs 1B su gemma4:e2b**: stesso modello, stesso task, risultati diversi (1A: 0/4/5, 1B: 0/0/0). Probabile effetto dell'ordine di esecuzione e dello stato KV-cache di Ollama, non della capacità del modello.

**Attenzione sui dati 1B beginner**: i risultati in `results/1B/beginner/task5*` e `task6*` usano `deepseek-r1:latest`, non `qwen2.5-coder:1.5b-base`. Sono file di una run precedente alla TASK_MODEL_OVERRIDES — lo skip automatico li ha preservati quando qwen è crashato. Per dati puliti con qwen bisogna eliminare quei file e rieseguire.

---

## Decisioni e domande aperte (in vista della call di mercoledì 2026-05-13)

### 8.12 Prompt engineering vs modelli più grandi su task security

- **Situazione (2026-05-09)**: task6 fallisce su tutti i modelli testati. Il finding mancante richiede conoscenza specifica di Gin (framework HTTP Go). I prompt attuali sono profili 5G generici, non security analyst.
- **Opzione A — prompt engineering**: aggiungere contesto sul framework Gin nei system prompt o nel task. Rischio: introduce bias (stai dicendo al modello dove guardare), invalidando la misura di capacità raw.
- **Opzione B — modelli più grandi**: testare gemma4:e4b (già in uso come judge, 4B) o qwen2.5-coder:7b (già usato da Andrea, ha trovato risposte generiche) come agent su task6. Misura se il bottleneck è la capacità di ragionamento sul framework, non la comprensione sintattica.
- **Decisione**: procedere con **opzione B** — confronto modelli, prompt invariato. Il prompt è difficile da ottimizzare senza introdurre bias; la variabile controllata deve essere il modello. Aggiungere `gemma4:e4b` e/o `qwen2.5-coder:7b` al mapping in `config.py` e rieseguire task6 (e idealmente task7–task8 per confronto).
- **Proposte future**: gerarchia di capacità da misurare: 1.5B → 2B → 4B → 7B su task6; curva di scaling come risultato.

### Domande ancora aperte per la call

- **Soglia TEXTUAL_PASS_RATIO = 0.7**: con rubrica a 9 punti il minimo per "correct" è 6.3/9. Per task di security review con finding primario da 4 punti mai trovato, la soglia è forse troppo bassa (tutti falliscono ampiamente, la soglia non è il problema).
- **False positive rate**: non ancora tracciato. task9 (cross-file) penalizza implicitamente risposte vuote ma non conta finding inventati.
- **Dati 1B beginner**: eliminare i vecchi file deepseek e rieseguire con qwen (dopo aver verificato che il fallback JSON funziona) oppure cambiare il mapping e usare un modello più grande anche per beginner_1B?
