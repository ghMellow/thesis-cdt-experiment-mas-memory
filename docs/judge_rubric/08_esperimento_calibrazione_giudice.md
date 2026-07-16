# 08 — Esperimento: calibrazione del giudice (passi 1 e 1-bis)

> Documento operativo (2026-07-16). Impostazione + checklist eseguibile dei primi due passi della sequenza proposta nel doc 04 §6, come emendata dal doc 07 (passo 1-bis). Pensato come **loop agentico**: l'orchestratore (Claude, sessione corrente o futura) esegue i passi in ordine, aggiorna la sezione *Stato* dopo ogni passo, e può delegare a subagent i passi marcati come delegabili. Se la sessione si interrompe, si riparte da qui: la sezione *Stato* dice esattamente dove si era rimasti.

## 1. Scopo

Due domande, entrambe rispondibili **senza nuove run degli agenti** (si lavora sui report già salvati in `results/`):

1. **Passo 1a — Calibrazione soglia**: la soglia `TEXTUAL_PASS_RATIO = 0.7` è arbitraria (config.py:50). Qual è la soglia che massimizza l'accordo tra il verdetto della rubrica e il match deterministico M1 (CVE trovata sì/no)? → toglie l'arbitrarietà, requisito di qualunque rubrica futura (doc 04 §5).
2. **Passo 1b — Giudice ≠ agente**: quanto cambiano score e verdetti se il giudizio lo dà un modello di famiglia diversa dall'agente? → misura del self-enhancement bias (doc 01 §3.4), meccanismo 1B già in `config.py`.
3. **Passo 1-bis — Test di ammissione C1/C2** (dal doc 07 §3, trasposto da arXiv:2607.12885): il giudice attuale promuove un report coerente con la GT (C1) e boccia un report plausibile ma sbagliato (C2)? Il **Calibration Gap** `CGP = score(C1) − score(C2)` è il test di ammissione prima di qualunque migrazione GT-free.

## 2. Chiarimento "offline"

"Offline" = **fuori dal loop degli agenti** (script che rilegge `results/` e, dove serve, richiama il giudice con chiamate standalone). NON significa senza modelli hostati: i passi 1b e 1-bis usano i modelli Ollama (cloud o locale) esattamente come `run_judge_textual`, solo fuori dal loop. Il passo 1a non fa **alcuna** chiamata LLM.

## 3. Dati disponibili (verificato 2026-07-16)

- `results/task{5..9}_*/1A/agent/hosted_gemma4_31b_cloud.json` — 5 task × 3 ripetizioni = **15 ripetizioni giudicate** (run SGV-fixed del 2026-07-14).
- Per ogni attempt in `repetitions[].history[]`: `judge_score` con i 4 criteri (`vulnerability_identified_score` 0–3, `location_precision_score` 0–2, `impact_assessment_score` 0–2, `fix_quality_score` 0–2), `total_score`, `normalized_score`, `feedback`; più `sgv_eval` e `verdict`.
- Per ogni ripetizione: `cvss_eval.matched[]` / `missed_cves[]` → il segnale deterministico "CVE trovata" usato come M1.
- Rubrica per-task nel secondo blocco JSON dei `_sol.md`; prompt del giudice in `build_judge_prompt` (`utils/experiment_utils.py`); giudice in `agents/judge_agent.py`.

**Limite dichiarato**: N=15 è piccolo. I risultati sono indicativi, non conclusivi — vanno presentati come pilota. Se nel frattempo arrivano run nuove (altri task/config), gli script devono raccoglierle automaticamente (glob su `results/*/**/agent/*.json`).

## 4. Disegno degli esperimenti

### Passo 1a — Calibrazione soglia (zero chiamate LLM)

- Per ogni ripetizione: `normalized_score` finale + esito M1 binario (`len(cvss_eval.matched) > 0`).
- Sweep della soglia t ∈ {0.05, 0.10, …, 1.0}: verdetto(t) = `normalized_score ≥ t`; accordo(t) = frazione di ripetizioni in cui verdetto(t) == M1.
- Output: tabella accordo per soglia + curva; soglia raccomandata = argmax accordo (in caso di plateau, riportare l'intervallo). Riportare anche accordo a t=0.7 (soglia attuale) e distribuzione dei `normalized_score` (se sono tutti ≈1.0, la curva è degenere e va detto: il giudice attuale non discrimina — risultato interessante di per sé, collegabile alla generosità del doc 06).

### Passo 1b — Giudice ≠ agente (chiamate LLM: ~15–30)

- Ri-giudicare i 15 `final_answer` salvati con un giudice di **famiglia diversa** dall'agente (agente = gemma). Candidati in ordine: modello non-gemma disponibile su Ollama Cloud (verificare a runtime con `ollama ls` / API); fallback `deepseek-r1:7b` locale. **Decisione modello da registrare in Stato.**
- Stessa rubrica, stesso prompt (`build_judge_prompt`), stessa temperatura — cambia solo il modello. 1 chiamata per ripetizione (opzionale ×2 per varianza se il costo lo consente).
- Output: confronto per ripetizione (score gemma vs score altra famiglia), delta medio, verdetti flippati a t=0.7 e alla soglia calibrata in 1a, accordo di ciascun giudice con M1.

### Passo 1-bis — Test di ammissione C1/C2 (chiamate LLM: ~30–60)

Costruzione materiali, **salvati verbatim prima di giudicare** (in `docs/judge_rubric/calibration_c1c2/`):

- **C1** (per ognuno dei 5 task): report coerente con la GT del `_sol.md` — vulnerabilità giusta, funzione giusta, impatto corretto — ma **riscritto** (non copiato dalla soluzione né dalla rubrica, per non testare il string-match).
- **C2** (per ognuno dei 5 task): report plausibile ma sbagliato — finding **trapiantato da un altro task** (stile e formato identici, vulnerabilità che non c'è in quel file), adattando i nomi di funzione a funzioni realmente presenti nel file del task (così SGV G2 non lo fermerebbe: testiamo il giudice, non l'SGV).
- Giudizio con la rubrica per-task attuale, K=3 ripetizioni per report per misurare la varianza. Giudice = quello di sistema (gemma cloud); opzionale ripetere col giudice del passo 1b.
- Output: `score(C1)` e `score(C2)` medi per task, **CGP = C1 − C2**, tasso di promozione di C2 a t=0.7 e alla soglia calibrata. Confronto qualitativo con il paper (Gemma3-27B: C2=0.66 nel dominio ostico).

**Interpretazione attesa**: la rubrica attuale è GT-derivata, quindi C2 *dovrebbe* fallire (la rubrica nomina la vulnerabilità vera). Se C2 passa lo stesso → il giudice ignora la rubrica = problema serio già oggi. Il valore vero del test è come **baseline**: quando arriverà la rubrica GT-free (doc 05), lo stesso identico test misurerà quanto CGP si degrada.

### Passo 2 — Report e chiusura

- Riepilogo risultati in `docs/judge_rubric/09_risultati_calibrazione.md` (numeri, tabelle, letture, limiti N=15).
- Aggiornare `docs/README.md` (righe 08/09), `docs/status.md` se cambia la soglia raccomandata, `DEVLOG.md`.
- **Non committare `results/`** salvo richiesta esplicita (regola di progetto). Gli output degli script vanno in `results/evaluation/judge_calibration/`; i materiali C1/C2 e il doc 09 in `docs/`. *(2026-07-16: su richiesta esplicita dell'utente anche `judge_calibration/` è stato committato, come già fatto per la run SGV-fixed.)*

## 5. Note per l'orchestratore

- **Esecutore**: gli script e l'analisi li fa l'orchestratore direttamente (sono corti e toccano convenzioni di progetto). Delegabile a un subagent (famiglia sonnet, `general-purpose`): la **stesura dei 10 report C1/C2**, che è generazione di testo parallela e ben specificata — nel prompt del subagent includere il `_sol.md` del task, il file di codice, e le regole del §4. La verifica finale dei materiali resta all'orchestratore.
- Script in `scripts/judge_calibration/` (nuova cartella): `calibrate_threshold.py` (1a), `rejudge_cross_family.py` (1b), `run_c1c2.py` (1-bis). Riusare `agents/judge_agent.py` e `build_judge_prompt` — non duplicare la logica del giudice.
- Modelli sempre presi da `config.py` o parametro CLI — mai hardcoded (regola di progetto).
- Il giudice **non riceve mai la ground truth testuale** — vale anche per questi script: solo rubrica.
- Dopo ogni passo: aggiornare la tabella *Stato* qui sotto e il DEVLOG se c'è una decisione/divergenza.

## 6. Stato

| # | Passo | Stato | Esito / note |
|---|-------|-------|--------------|
| 0 | File di impostazione | ✅ 2026-07-16 | questo documento |
| 1a | Script + calibrazione soglia | ✅ 2026-07-16 | 12 rep valide (task9 escluso: `n_target_cves=0`, M1 indefinito). Vs **M1-strict** (tutte le CVE trovate): accordo **1.00** sul plateau **[0.45–0.65]**; la soglia attuale 0.7 boccia task8 (0.67, tutte le CVE trovate) → raccomandata **0.65** (o 0.55 centro-plateau). Vs M1@any il giudice è *severo*, non generoso: 0 false pass, 6 false fail a 0.7 — la rubrica misura la copertura completa, non la detection. Output: `results/evaluation/judge_calibration/threshold_calibration.{md,json}` |
| 1b | Ri-giudizio cross-family | ✅ 2026-07-16 | Modello: **gpt-oss:20b** (hosted; famiglia diversa, taglia paragonabile a gemma4:31b). Delta medio **+0.074** (leggermente più generoso), verdetti flippati **2/15 a t=0.7, 1/15 a t=0.65**; ordinamento per task identico (task6 basso, task5/7/9 alti, task8 intermedio) → nessun segnale forte di self-family bias su questi dati. Output: `results/evaluation/judge_calibration/cross_family_hosted_gpt_oss_20b.{md,json}` |
| 1-bis.1 | Materiali C1/C2 (10 report, salvati verbatim) | ✅ 2026-07-16 | 10 file in `docs/judge_rubric/calibration_c1c2/` (5 task × C1/C2) + README con tabella task→vuln. Rotazione task9 adattata: vuln CORS trapiantata su funzioni AMF/UDR reali invece che su PCF, per non sovrapporsi al finding vero di task9 (il file 1 di task9 è il PCF con lo stesso bug). Stesura delegata a subagent sonnet, verificata dall'orchestratore. |
| 1-bis.2 | Run giudizio C1/C2 + CGP | ✅ 2026-07-16 | Giudice gemma4:31b-cloud, 10 report × K=3 = 30 giudizi. **CGP = +0.948** (C1 medio 1.000, C2 medio 0.052); C2 promossi **0/15** a t=0.7 e a t=0.65; C1 bocciati 0/15. Varianza quasi nulla (range max 0.11). task9 C2 = 0.22 (credito parziale per la classe giusta in posizione sbagliata — atteso). Il giudice con rubrica GT-derivata **supera il test di ammissione**: questa è la baseline per la futura rubrica GT-free. Output: `results/evaluation/judge_calibration/c1c2_hosted_gemma4_31b_cloud.{md,json}` |
| 2 | Doc 09 risultati + README/status/DEVLOG | ✅ 2026-07-16 | vedi `09_risultati_calibrazione.md`; soglia in config **non cambiata** (decisione di gruppo) |

**Ripresa in sessione futura**: leggere questo file + doc 04 §5–6 + doc 07 §3; controllare la tabella Stato; proseguire dal primo passo ☐.
