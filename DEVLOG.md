# Dev Log — Multi-Agent Experiment 5G

---

## 2026-06-25 — Attempt #6 e #7: bug strutturale filesystem + prima scoperta autonoma della regex  [sessione: a4261493]

**Intent:** "procedi" — continuare la ricreazione CVE con la skill /cve-attempt.

**Esito/Problemi:**
- **Attempt #6 (exp/test-4, hint=0, student, all_go):** ❌ contaminato. Bug strutturale scoperto: dopo `git checkout main`, le directory non tracciate (docs/cve_attempts/, ANALISI_VULNERABILITA.md) restano su disco. Il subagent ha letto ANALISI V3 e da lì ha trovato la regex — non dal codice.
- **Attempt #7 (exp/test-5, hint=0, student, all_go, con checkout fix):** ⚠️ PARZIALE — **prima volta che la regex `|.+` viene trovata per analisi autonoma del codice, senza ANALISI**. Ma il subagent ha letto `docs/cve_attempts/log.md` (rimasto untracked su disco) e si è auto-censurato: "già oggetto degli attempt 1-6, non includo per evitare ridondanza".
- **Fix definitivo identificato:** `Agent(isolation="worktree")` — crea un worktree git isolato che contiene solo i file tracciati del branch, eliminando l'accesso a tutte le directory untracked. Skill aggiornata.

**Decisioni:**
- Attempt 7 classificato ⚠️ PARZIALE, non ✅ SÌ: la scoperta era genuina ma la task creation è stata soppressa per meta-conoscenza.
- Prossimo attempt userà `isolation="worktree"` per ambiente completamente pulito.

**Lesson learned:** il filesystem locale è un vettore di contaminazione bidirezionale — non solo ANALISI entra, ma anche il log degli attempt stessi diventa visibile. Il worktree isolation è l'unico fix robusto.

---

## 2026-06-23 — Documentazione tentativi di ricreazione CVE (multi-branch)  [sessione: 9c7c92ef]

**Intent:** "adesso bisogna documentare il tutto […] segna i casi fallimentari e quelli […] buon fine […] vai a leggerti le chat (usa la skill) […] riportare anche i prompt usati […] highlight riassuntivo" + "conviene dividere il lavoro?" (concessione su struttura e divisione).

**Divergenze/Decisioni:** nuovo `docs/cve_recreation_log.md` scritto su `main`; estrazione catene di prompt **delegata a 4 subagent Sonnet 4.6 in background** (uno per branch-lineage) per non saturare la finestra Opus — autorizzato dall'utente. I subagent localizzano la sessione via `grep` dei nomi-task distintivi nei `.jsonl`.

**Esito:** creato `docs/cve_recreation_log.md` (criterio di successo, highlight + matrice di copertura, §4 catene di prompt per branch, §5 lessons). Verdetti: `test_fallimentare` RIUSCITO (regex standalone `task7_udr_regex`) → rivalutato valido; `test-reproducibility` PARZIALE (regex esclusa per fedeltà a `Patch_Spiegazione.md`); `main`/exp RIUSCITO (cross + full). Origine = commit perso `bbbbd6a`.

**Lesson learned:** la sessione originale è irrecuperabile (backup transcript partito dopo) → il log è reverse-engineering di `bbbbd6a`. Le estensioni di valore (task cross-NF, varianti `_full`, scoperta della regex poi GHSA-6gxq) furono **iniziative autonome del modello** abilitate da prompt a bassa costrizione — il fenomeno stesso che si vuole riprodurre.

**Correzione (stessa sessione):** l'utente ha precisato il criterio vero = il **cutoff** (riscoperta spontanea *prima* che l'obiettivo sia rivelato o che venga passata l'ANALISI). Rianalizzato con 2 subagent: **nessun tentativo ha riscoperto la regex** prima del cutoff. `test_fallimentare` aveva l'ANALISI (V3) nel contesto dal msg 0 → trascrizione, non scoperta; `test-reproducibility` nell'unico run cieco (`ebcd1147`) ha letto la regex ma l'ha **invertita** (presa per validazione corretta). Verdetto corretto: `test_fallimentare` NON è "RIUSCITO" — *esistenza del task ≠ riscoperta*. L'unica riscoperta genuina resta l'originale persa. Doc `cve_recreation_log.md` riscritto di conseguenza.

---

## 2026-06-09 — Framing experiment series completata: paradosso beginner>expert risolto

**Done:**
- Serie A (A1/A2/A3): isolato l'effetto framing — il vantaggio del beginner su task7 è causato dal framing "junior technician", non da un danno del framing expert
- Serie B (B1_e2b / B1_cloud / B2 / B3): confermato che il paradosso è framing × capacità — esiste solo nella finestra e4b; sparisce con e2b (collasso totale) e con 31b (expert raggiunge 100%)
- Curva scaling expert su task7: e2b=0% → e4b=66.7% → 31b=100%
- Accesso Ollama Cloud ottenuto e usato (gemma4:31b-cloud in B1_cloud/B2)
- Aggiornati status.md (snapshot → 2026-06-09) e call_3.md §7 roadmap

**Problemi:**
- gemma3:4b-cloud restituisce 500 su payload tecnici lunghi (~11KB+) → workaround: usato gemma3:12b-cloud in B2 per il beginner, che introduce una variabile confondente (architettura gemma3 vs gemma4)
- B2 beginner (12b) peggiore del beginner e4b locale su task7 (33.3% vs 100%) — effetto architettura non eliminabile con workaround

**Lesson learned:**
- Il framing agisce come "stile cognitivo implicito": non è riducibile a una singola istruzione (A3: hint switch dà 66.7%, non 100%) né a verbosità (A2: il vincolo peggiora l'accuracy)
- Il paradosso beginner>expert non è un risultato stabile — dipende dalla finestra di capacità del modello; va presentato come effetto framing × capacità, non come proprietà assoluta del sistema
- **Prossimo:** C1 — temperature sweep T∈{0.1, 0.7} su task7/8 expert e4b; vedi `docs/experiments_framing.md` §C1

---

## 2026-05-14 — Fix template risposta + tracciamento prompt e score intermedi

**Done:**
- Invertito ordine campi in tutti i 12 task: `Reasoning → Answer → Confidence` (fix chain-of-thought prima del commit)
- Aggiunto `prompt_system` e `prompt_user` in ogni `history[n]` — debugging non più cieco
- Aggiunto `judge_score` (breakdown per criterio) e `verdict` per ogni attempt in `history[n]`
- Aggiunto `temperature` e `judge_model` in `run_config`
- Analizzati reasoning task7 expert rep3: 3 retry quasi identici, `missing_default_score=0` sempre — retry neutro non rompe convergenza su T=0.3
- Falsificata ipotesi context window su task7: differenza expert/beginner = 21 chars / ~8 token

**Problemi:**
- Il bug `Answer prima di Reasoning` era silenzioso: il modello calcolava correttamente nel reasoning ma committava l'ipotesi iniziale nel campo Answer

**Lesson learned:**
- Con modelli che fanno chain-of-thought, il campo risposta deve venire DOPO il reasoning nel template — altrimenti il modello committa prima di ragionare
- Il retry senza feedback direzionale è utile solo per varianza stocastica; su T=0.3 il modello converge strutturalmente sullo stesso errore

---

## 2026-05-09 — Security review tasks + framework consolidato

**Done:**
- Task5–9 operativi (CVE reali free5GC: PCF, UDR, AMF, UDM, cross-NF)
- Timeout moltiplicatore per task `*_full` (×2 = 1200s, configurabile)
- Rubrica dinamica per-task (`_build_judge_prompt`), Brier score, semantic consistency, token tracking
- Output da JSON a Markdown — eliminati crash di parsing su modelli piccoli
- Prompt tradotti in inglese, temperatura 0.0→0.3, `OLLAMA_NUM_PREDICT` 256→1024

**Problemi:**
- task6_vuln_udr_full: timeout colpisce il judge (non l'agent) al terzo retry — contesto crescente supera il limite
- task6_vuln_udr con prompt generico: `missing_return_score=0` sistematico → aggiunto "special attention" (metodologicamente discutibile, vedi F10)
- File results/1B/beginner/task5*/task6* usano deepseek invece di qwen — skip automatico li ha preservati (F8)

**Lesson learned:**
- Il prompt del task deve essere specifico quanto la rubrica — se la rubrica valuta 3 criteri tecnici precisi, il prompt non può essere generico
- Il timeout uniforme agent/judge non regge i task full-file: separare i due timeout
