# docs/ — mappa della documentazione

Punto di ingresso unico. La documentazione è divisa in **tre aree**: sistema (come funziona il progetto), esperimento CVE (la "singolarità"), e materiale di supporto.

---

## 🧭 Sistema multi-agent

Come è fatto e come gira il progetto di sperimentazione.

| Documento | Contenuto |
|-----------|-----------|
| [status.md](status.md) | Stato attuale: modelli, task, CLI, checklist funzionalità |
| [architecture.md](architecture.md) | Mappa codice, flusso LangGraph, valutazione, report — riferimento stabile |
| [findings.md](findings.md) | Registro empirico: osservazioni che hanno causato correzioni al codice/metodo |
| [risultati_template.md](risultati_template.md) | **Template** da copiare per il prossimo doc `0N_risultati_*.md`: cosa NON ripetere (già in `results/evaluation/*.md`), scheletro, checklist |
| [experiments_framing.md](experiments_framing.md) | Coda di esperimenti framing (expert vs beginner) |
| [changelog.md](changelog.md) | Storico modifiche |
| [tasks/](tasks/) | I task di code review usati dagli agenti |

## 🔬 Esperimento CVE — "la singolarità"

Riproduzione della scoperta spontanea della regex `|.+` (GHSA-6gxq-gpr8-xgjp) in free5GC.

| Documento | A chi serve |
|-----------|-------------|
| **[cve_experiment/README.md](cve_experiment/README.md)** | **Inizia da qui.** Presentazione per chi parte da zero: contesto, problema, test, risultati |
| [cve_experiment/team_update.md](team_update_CVE-2026-47780%20%20GHSA-6gxq-gpr8-xgjp.md) | Aggiornamento di chiusura per il team: findings, problemi, prompt testuali |
| [cve_experiment/hands_on.md](cve_experiment/hands_on.md) | Guida pratica: i prompt che funzionano + come rifare il test |
| [cve_experiment/attempts/log.md](cve_experiment/attempts/log.md) | Log tecnico di tutti i tentativi (#0–#21) — **fonte autoritativa** |
| [cve_experiment/attempts/](cve_experiment/attempts/) | Dettaglio per tentativo: `attempt_<N>/` (params, prompt, chain, findings, verdict) |
| [cve_experiment/history_0-5.md](cve_experiment/history_0-5.md) | Storico narrativo dei primi tentativi (#0–#5) — superato dal log sopra |

**Dati gestiti dalle skill** (non modificare a mano):

| Cartella | Skill che la gestisce |
|----------|-----------------------|
| [cve_experiment/attempts/](cve_experiment/attempts/) | `/cve-attempt` |
| [cve_experiment/regex_scan/](cve_experiment/regex_scan/) | `/cve-branch-scan` (scansione regex nei branch) |
| [cve_experiment/task_map/](cve_experiment/task_map/) | `/task-branch-map` (mappa task cross-branch) |

## 🧪 Protocollo SGV — proposta in discussione

Proposta del relatore (2026-07-13): sostituire il retry guidato da LLM-judge con un verificatore sintattico deterministico (Syntactic Grounding Verifier), per eliminare leakage semantico e non-riproducibilità dal loop in-loop. **G1–G4 implementati** (`utils/sgv.py`, 2026-07-14) — vedi doc 06.

| Documento | Contenuto |
|-----------|-----------|
| [sgv_protocol/00_proposta_relatore.md](sgv_protocol/00_proposta_relatore.md) | Proposta originale del relatore (verbatim): motivazione, protocollo G1–G4, metriche M/S, related work |
| [sgv_protocol/01_discussione_2026-07-13.md](sgv_protocol/01_discussione_2026-07-13.md) | Mappatura sull'architettura attuale — cosa è già allineato, cosa richiede refactor, rischi aperti, prossimi passi |
| [sgv_protocol/02_discussione_team_2026-07-13.md](sgv_protocol/02_discussione_team_2026-07-13.md) | Reazioni del team (Andrea, Raffaele): rischio "cecità semantica" dell'SGV, proposta G5 (Semantic CWE Match via SAST), rigidità del matching e mitigazione AST, decisione di sequenza esperimenti (SAST solo dal terzo) |
| [sgv_protocol/03_valutazione_claude_2026-07-13.md](sgv_protocol/03_valutazione_claude_2026-07-13.md) | Valutazione critica delle reazioni del team — tensione tra G5 e la metrica M4 (Delta SAST), portata della proposta AST sulla definizione di ground truth, problema aperto: cosa occupa il secondo esperimento della sequenza |
| [sgv_protocol/04_call12_2026-07-14.md](sgv_protocol/04_call12_2026-07-14.md) | Dodicesima call: via libera esplicita a implementare l'SGV, precedente deterministico già esistente (`_match_finding`), ipotesi rubrica ancorata a CWE invece che a CVE, sequenza di lavoro (SGV → rubrica → formato output), piano operativo per iniziare l'implementazione |
| [sgv_protocol/05_dove_va_sgv.html](sgv_protocol/05_dove_va_sgv.html) | Presentazione (3 slide): (1) stato attuale del flusso per formato con i controlli deterministici già esistenti; (2) proposta — un solo gate SGV condiviso prima dello split, Ramo A/B separati a valle; (3) **implementazione reale** — G1/G2/G4 sempre attivi, G3 opzionale via `config.SGV_SNIPPET_ENABLED` deciso a monte nel prompt |
| [sgv_protocol/06_implementazione_2026-07-14.md](sgv_protocol/06_implementazione_2026-07-14.md) | **Prima implementazione G1–G4** (`utils/sgv.py`): cosa fa ogni controllo, scelte prese (campo `snippet` opzionale via flag, `_match_finding` non riusata per G2, gate condiviso, retry indipendente dalla rubrica), cosa resta aperto (calibrazione soglia Jaccard, prima run di prova) |

## ⚖️ Giudice a rubrica — discussione in corso

Cartella gemella di `sgv_protocol/` (che copre l'in-loop): qui si discute il **giudizio di accettazione** (giudice LLM + rubrica + soglia) e come svincolarlo dalla ground truth, dato che oggi la rubrica è scritta a partire dalla GT. Nulla è implementato — materiale per la discussione di gruppo.

| Documento | Contenuto |
|-----------|-----------|
| [judge_rubric/00_call10_proposta_rubrica_cvss.md](judge_rubric/00_call10_proposta_rubrica_cvss.md) | Antecedente (verbale decima call, 2026-07-08): rubrica v2 a due blocchi, tabella "Fase 2 senza GT" che apre il tema della cartella; schema dati, matching CVE↔handler, scelta B vs BT tuttora validi |
| [judge_rubric/00_call11_2026-07-10.md](judge_rubric/00_call11_2026-07-10.md) | Antecedente (estratto undicesima call): Lorenzo propone di eliminare il giudice (output = lista CVSS ordinabile), difesa di Andrea, genealogia della rubrica GT-derivata, uscita dalla GT come obiettivo d'articolo, metriche di qualità/costo |
| [judge_rubric/00_call12_2026-07-14.md](judge_rubric/00_call12_2026-07-14.md) | Antecedente (estratto dodicesima call): «un cane che si morde la coda» (circolarità rubrica↔GT), nascita delle idee "rubrica come esperto di sicurezza" e "rubrica ancorata alle CWE", rubrica attuale declassata a strada tentata, controprova su file mai visto |
| [judge_rubric/01_stato_attuale_giudice_rubrica.md](judge_rubric/01_stato_attuale_giudice_rubrica.md) | Stato attuale: come funziona il giudice a rubrica, teoria e paper di riferimento (MT-Bench, G-Eval, Prometheus, RUBRICEVAL), debolezze osservate nel progetto, limite strutturale della rubrica GT-derivata |
| [judge_rubric/02_paper_LLM-as-a-Verifier_2607.05391v2.md](judge_rubric/02_paper_LLM-as-a-Verifier_2607.05391v2.md) | Paper (verbatim, arXiv:2607.05391): score continui via expectation sui logit dei token di punteggio, scaling su granularità/ripetizione/decomposizione dei criteri — proposta futura come alternativa di rubrica |
| [judge_rubric/03_discussione_llm_as_a_verifier.md](judge_rubric/03_discussione_llm_as_a_verifier.md) | Discussione del paper: mappa sul nostro sistema, fattibilità con Ollama/logprobs, cosa NON risolve (soglia, criteri GT-free), valutazione di Claude e proposta di pilota offline |
| [judge_rubric/04_alternative_e_proposte.md](judge_rubric/04_alternative_e_proposte.md) | Alternative a confronto: rubrica "workflow esperto di sicurezza", criteri GT-free di qualità del report (raccomandata), ancoraggio CWE, calibrazione soglia, giudice ≠ agente — con sequenza operativa proposta |
| [judge_rubric/05_rubrica_esperto_cwe_5g.md](judge_rubric/05_rubrica_esperto_cwe_5g.md) | Sviluppo dell'idea di call 12: combinazione workflow esperto × CWE di alto livello — giudice come auditor (non analista), matrice di criteri con coverage deterministico stile SGV, livello della tassonomia anti-leakage, onestà sulla "CWE 5G" (non esiste: FiGHT/SCAS come contesto), validazione con controprova su file mai visto |
| [judge_rubric/06_paper_LLM_Judges_Too_Generous_2607.12885v1.md](judge_rubric/06_paper_LLM_Judges_Too_Generous_2607.12885v1.md) | Paper (verbatim, arXiv:2607.12885): i giudici LLM reference-free gonfiano la correctness (flip fino all'85% aggiungendo la reference); pipeline di calibration (C1/C2) e sensitivity (NR/RV/RC) per validare un giudice prima di usarlo senza GT |
| [judge_rubric/07_discussione_giudici_troppo_generosi.md](judge_rubric/07_discussione_giudici_troppo_generosi.md) | Discussione del paper: perché ci riguarda (giudice Gemma3-27B testato, dominio ostico ≈ il nostro 5G/Go), trasposizione del protocollo C1/C2 come test di ammissione del giudice sui task con GT, flip rate come misura della generosità del passaggio a GT-free, disanalogie dichiarate |
| [judge_rubric/08_esperimento_calibrazione_giudice.md](judge_rubric/08_esperimento_calibrazione_giudice.md) | **Documento operativo** (loop agentico con checklist di stato): calibrazione soglia sui `results/` esistenti, ri-giudizio cross-family, test di ammissione C1/C2 — passi 1 e 1-bis della sequenza del doc 04 §6. **Eseguito 2026-07-16** |
| [judge_rubric/09_risultati_calibrazione.md](judge_rubric/09_risultati_calibrazione.md) | **Risultati** dell'esperimento del doc 08: soglia 0.7 troppo alta (accordo perfetto con M1-strict sul plateau 0.45–0.65), nessun self-enhancement bias rilevato (gpt-oss:20b concorda, +0.074), giudice attuale supera il test di ammissione C1/C2 (**CGP +0.948**, 0 falsi positivi) — baseline per la futura rubrica GT-free; task9 scoperto senza CVE target mappate |
| [judge_rubric/calibration_c1c2/](judge_rubric/calibration_c1c2/) | Materiali verbatim del test C1/C2: 10 report (5 C1 corretti-riscritti, 5 C2 plausibili-ma-sbagliati) — banco di prova riusabile per qualunque rubrica candidata |

## 📎 Supporto

Materiale ausiliario: non necessario per capire lo stato attuale del sistema, ma utile come riferimento/archivio.

| Cartella | Contenuto |
|----------|-----------|
| [supporto/calls/](supporto/calls/) | Verbali storici delle call (call_1, call_2, call_3) |
| [supporto/calls/transcripts/](supporto/calls/transcripts/) | Trascrizioni audio grezze delle call (materiale-fonte dei verbali) |
| [supporto/presentations/](supporto/presentations/) | Speech outline della tesi (`presentation_new.md`) + presentazioni HTML architettura-flusso a livelli: `architettura_flusso_v1_pre_cvss.html` (ruoli expert/beginner, 1A/1B, giudice, retry) e `architettura_flusso_v2_cvss.html` (agente unico, doppio ramo giudice/script CVSS, punti di uscita dati) |
| [supporto/reference/](supporto/reference/) | Materiale esterno (modelli Ollama, paper RUBRICEVAL) |
| [results_reference/](results_reference/) | Schema JSON dei risultati (`schema_math.json`, `schema_textual.json`) e pacchetto di validazione esterna (`validation/`) — spostati fuori da `results/` per non confonderli con gli output delle run |
| [supporto/archive/](supporto/archive/) | Materiale storico grezzo (vecchio stack trace di debug) |

---

> Regola di progetto (vedi [CLAUDE.md](../CLAUDE.md)): repo e documentazione sempre allineati. Dopo ogni modifica al codice, aggiorna il documento di dettaglio corrispondente.
