# Dev Log — Multi-Agent Experiment 5G

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
