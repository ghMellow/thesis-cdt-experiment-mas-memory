# 10 — Esperimento: rubrica GT-free (doc 05) nel banco di prova del doc 08

> Documento operativo (2026-07-16). Via libera del gruppo ricevuto (solo da riportare, non da discutere). Prototipa la rubrica del doc 05 — matrice workflow esperto × classi CWE di alto livello — e la confronta con la baseline misurata nel doc 09. Stesso stile del doc 08: loop agentico con tabella *Stato*, ripresa possibile da sessione futura. Zero run nuove degli agenti: tutto offline sui materiali esistenti.

## 1. Domanda sperimentale

Il doc 09 ha stabilito la baseline: giudice + rubrica GT-derivata → **CGP = +0.948**, 0/15 C2 promossi, accordo 1.00 con M1-strict sul plateau 0.45–0.65. La domanda di questo esperimento: **quanto di quella qualità sopravvive togliendo la GT dalla rubrica?**

- **CGP(GT-free) vs +0.948** — il prezzo del distacco dalla GT, misurato (l'analogo del flip NR→RC del paper doc 06, con M1 come arbitro al posto degli umani).
- **Flip rate sui 15 report reali**: quanti verdetti cambiano ri-giudicando gli stessi report con la rubrica GT-free; accordo con M1-strict a confronto con quello della rubrica GT-derivata.

**Attesa dichiarata (da doc 06/07):** il CGP *deve* scendere — C2 è costruito per essere plausibile, e un auditor GT-free non sa quale vulnerabilità c'è davvero. Il criterio di successo non è CGP≈0.95 ma: (a) CGP nettamente > 0 con C2 sotto soglia in maggioranza; (b) accordo con M1-strict sui report reali non troppo degradato. Se invece CGP ≈ 0 (C2 promossi come C1), la rubrica v1 non basta e va rivista.

## 2. La rubrica v1 (da doc 05 §3)

Task-independent (una sola per tutto il dominio — risolve anche doc 01 §3.7), salvata verbatim in `gtfree/rubric_v1.json`. Quattro criteri, di cui **tre giudicati dall'LLM** (total_max giudice = 7) e **uno deterministico** calcolato dallo script (0–2), per un totale combinato su 9:

| Criterio | Chi lo valuta | Max |
|---|---|---|
| `weakness_classification` — ogni finding dichiara una classe di debolezza di alto livello plausibile per l'evidenza citata (vocabolario: ~10 classi stile pillar CWE-1000, elencate nella rubrica) | LLM | 3 |
| `evidence_class_coherence` — il codice/snippet citato mostra la firma tipica della classe dichiarata (regex→validazione input, risposta-senza-return→controllo di flusso, header/policy→access control…) | LLM | 2 |
| `class_severity_coherence` — l'impatto descritto e il vettore CVSS sono compatibili con la classe dichiarata | LLM | 2 |
| `coverage` — funzioni esposte del file toccate dall'analisi / funzioni esposte totali | **script (deterministico, stile SGV G2)** | 2 |

Regole anti-leakage rispettate: le classi sono di livello alto (coprono qualunque codebase — nessuna informazione sul nostro dataset), nessun nome di vulnerabilità/funzione specifica, la specificità 5G entra solo come contesto di dominio già presente nel prompt del giudice.

**Coverage deterministico**: funzioni estratte dal codice Go nel task (`func (recv) Nome(` / `func Nome(`, **tutte, anche non esportate** — `setCorsHeader` di task5 è non esportata); citate = presenti nel testo del report o nei `function` dei finding CVSS. Ratio = citate / min(n_funzioni, **6**): il denominatore è cappato perché sui file `_full` (~100 funzioni) il rapporto assoluto renderebbe il punteggio pieno irraggiungibile a qualunque report onesto. Punteggio: ratio ≥ 2/3 → 2, ≥ 1/3 → 1, altrimenti 0 (formula dichiarata, discutibile, ma fissa; verificata a secco sui report reali: cov=2 su task6–9, cov=1 su task5 che cita la sola funzione vulnerabile su 3).

**Estrazione probabilistica (pilota doc 03, surrogato cloud)**: K=3 campioni per report a T=0.3, si riporta media e range. I logprob veri restano solo-locale (doc 03 §3) → rimandati; il K-sampling è il metodo principale del paper doc 02 comunque.

## 3. Esecuzione

Script `scripts/judge_calibration/run_gtfree_rubric.py`, riusa `run_judge_textual`/`build_judge_prompt` con la rubrica caricata da file invece che dal `_sol.md`:

1. **Set C1/C2** (10 report × K=3 = 30 chiamate): CGP GT-free, confronto per task con doc 09 §3.
2. **Set report reali** (15 final_answer × K=3 = 45 chiamate): score GT-free vs GT-derivato, flip rate a t=0.65 e 0.7, accordo con M1-strict (sui 12 con M1 definito).
3. Risultati in `11_risultati_rubrica_gtfree.md` + aggiornamento README/status/DEVLOG. Giudice: quello di sistema (`config.MODELS["judge"]`).

## 4. Stato

| # | Passo | Stato | Esito / note |
|---|-------|-------|--------------|
| 0 | File di impostazione | ✅ 2026-07-16 | questo documento |
| 1 | Rubrica v1 salvata verbatim (`gtfree/rubric_v1.json`) | ✅ 2026-07-16 | 3 criteri LLM (classification 0–3, evidence 0–2, severity 0–2), vocabolario ~10 classi alto livello |
| 2 | Script `run_gtfree_rubric.py` (incl. coverage deterministico) | ✅ 2026-07-16 | coverage verificato a secco; due fix: funzioni anche non esportate, denominatore cappato a 6 |
| 3 | Run set C1/C2 → CGP GT-free | ✅ 2026-07-16 | **CGP = +0.437** (baseline +0.948): C1 sempre 1.00, ma **2/5 C2 promossi** (task7 a pieni voti — claim di *assenza* non verificabile; task6 0.78). Respinti i C2 con firma sintattica verificabile (task8 CORS → 0.11) |
| 4 | Run set report reali → flip rate + accordo M1-strict | ✅ 2026-07-16 | **Saturazione**: tutti 7.0/7 su ogni criterio LLM. Flip 3/15 a t=0.65 (tutti task6, direzione sbagliata); accordo M1-strict **9/12** vs 12/12 della baseline. La v1 misura la qualità formale (satura), non la completezza |
| 5 | Doc 11 risultati + README/status/DEVLOG | ✅ 2026-07-16 | verdetto: **v1 non passa il test di ammissione**; 3 meccanismi di rottura identificati e direzioni v2 nel doc 11 §3 |

**Ripresa in sessione futura**: leggere questo file + doc 09 (baseline) + doc 05 §3; proseguire dal primo passo ☐.
