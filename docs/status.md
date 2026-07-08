# Stato del sistema — Multi-Agent Experiment 5G

> 🧭 Per la **mappa completa della documentazione** vedi [README.md](README.md). Questo file è lo **stato/snapshot del sistema**.

## Dove trovare i dettagli

| Documento | Contenuto |
| --- | --- |
| [architecture.md](architecture.md) | §1–7 + §9: mappa codice, flusso, valutazione, report — **riferimento stabile** |
| [supporto/calls/call_1.md](supporto/calls/call_1.md) | Call iniziali: judge, soglie, rubrica, retry, confidence, token, consistenza, modelli, lingua (§8.1–8.10) |
| [supporto/calls/call_2.md](supporto/calls/call_2.md) | Call 2026-05-09: security review 5G, task5–9, snapshot sistema (§8.11 + §10) |
| [supporto/calls/call_3.md](supporto/calls/call_3.md) | Call 2026-05-13: presentazione risultati, dubbi metodologici, roadmap 19 maggio |
| [findings.md](findings.md) | Registro empirico: osservazioni che hanno causato correzioni al codice o alla metodologia |
| [cve_experiment/](cve_experiment/README.md) | Esperimento "singolarità": un LLM riscopre da solo la CVE `\|.+`? Presentazione, guida pratica, log #0–#18 |

---

## Stato attuale (snapshot 2026-06-09)

> Questo snapshot copre il **workstream framing** (esperimenti A/B/C). Il workstream **esperimento CVE** (riproduzione scoperta `|.+`) procede in parallelo ed è tracciato separatamente in [cve_experiment/](cve_experiment/README.md) — ultimo aggiornamento #18 (2026-06-30).

Sistema operativo. 12 task disponibili, framework LangGraph con retry/judge/token tracking/semantic consistency.

**Serie framing completata (A1–A3, B1–B3):** il paradosso beginner>expert su task7 è completamente spiegato — effetto framing × capacità confinato alla finestra e4b. Vedi `docs/findings.md` F16–F22 e `docs/experiments_framing.md`. **Prossimo:** C1 — temperature sweep T∈{0.1, 0.7} su task7/8.

### Modelli (`config.py`)

| Chiave | Local | Hosted | use_hosted |
| --- | --- | --- | --- |
| `expert_1A` | gemma4:e4b | gemma3:12b-cloud | True |
| `beginner_1A` | gemma4:e4b | gemma3:12b-cloud | True |
| `expert_1B` | gemma4:e4b | gemma4:31b-cloud | True |
| `beginner_1B` | gemma4:e4b | gemma3:4b-cloud | True |
| `judge` | gemma4:e4b | nemotron-3-super:cloud | True |
| `semantic_check` | gemma4:e2b | gemma3:4b-cloud | True |

Vedi header di `config.py` per la quick-reference dei setup framing (A1/A2/B1/B2/B3).

### Task disponibili

| ID | Tipo | beginner_1B model |
| --- | --- | --- |
| `task1_math_int`, `task2_math_real` | math | deepseek-r1:latest |
| `task3_anomaly`, `task4_rootcause` | textual 5G | deepseek-r1:latest |
| `task5_vuln_pcf` | security review PCF | qwen2.5-coder:1.5b-base |
| `task6_vuln_udr` | security review UDR excerpt | qwen2.5-coder:1.5b-base |
| `task6_vuln_udr_full` | security review UDR file completo (2891 righe) | qwen2.5-coder:1.5b-base |
| `task7_vuln_amf` | security review AMF excerpt | qwen2.5-coder:1.5b-base |
| `task7_vuln_amf_full` | security review AMF file completo (501 righe) | qwen2.5-coder:1.5b-base |
| `task8_vuln_udm` | security review UDM excerpt | qwen2.5-coder:1.5b-base |
| `task8_vuln_udm_full` | security review UDM file completo (858 righe) | qwen2.5-coder:1.5b-base |
| `task9_vuln_cross` | security review cross-NF | qwen2.5-coder:1.5b-base |

### Funzionalità implementate / aperte

- [x] Judge con rubrica dinamica per-task (`_build_judge_prompt`)
- [x] Brier score per calibrazione confidence
- [x] Semantic consistency check a due fasi (string equality → LLM)
- [x] Token tracking agent + judge per ripetizione
- [x] Context window logging all'avvio via Ollama `/api/show`
- [x] Task security review task5–task9 (CVE reali free5GC)
- [x] Retry neutro con risposta precedente (senza feedback judge)
- [x] Output Markdown per agent/judge (template Answer/Reasoning/Confidence + parsing)
- [x] Prompt completo salvato per ogni run (`history[n].prompt_system` + `prompt_user`)
- [x] Score intermedi per-attempt in `history[n].judge_score` + `verdict`
- [x] Framing experiments A1–A3: effetto framing beginner isolato e spiegato (F16–F18)
- [x] Framing experiments B1–B3: paradosso confermato come framing × capacità — scala e2b→e4b→31b (F19–F22)
- [x] Accesso modelli cloud (gemma4:31b, gemma3:12b via Ollama Cloud — usati in B1_cloud/B2)
- [ ] **C1 — Temperature sweep** T∈{0.1, 0.7} su task7/8 expert e4b (prossimo esperimento)
- [ ] Retry con feedback del judge reiniettato
- [ ] Rieseguire task6 blind (senza special attention) — baseline pulita
- [ ] False positive rate tracking / task "controllo negativo"
- [ ] Preparare estratti per validazione esperti 5G (task5, task7, task8)
- [ ] Convertire output JSON in report Markdown strutturato per l'AI
- [ ] Profiling sistematico VRAM/latency per modello

---

## CLI comandi rapidi

```bash
# Run tutti i task security review, 1B, tutti i ruoli
python main.py --experiment 1B --task task5_vuln_pcf task6_vuln_udr task7_vuln_amf task8_vuln_udm task9_vuln_cross

# Includi anche le varianti full-file
python main.py --experiment 1B --task task6_vuln_udr_full task7_vuln_amf_full task8_vuln_udm_full

# Test rapido singolo task
python main.py --task task5_vuln_pcf --repetitions 1 --task-timeout 120

# Export grafo LangGraph
python main.py --export-graph docs/graph.png
```

---

## Presentazione (`docs/presentation.html`)

### Come aggiornare la presentazione

Quando viene chiesto di aggiornare o rigenerare la presentazione, seguire questo ordine:

**1. Leggi prima questi file (in ordine):**

1. `docs/status.md` — stato attuale: modelli, task, checklist
2. `docs/architecture.md` — mappa codice e flusso (slide architettura)
3. `docs/supporto/calls/call_1.md` — sfide e decisioni base (slide sfide aperte)
4. `docs/supporto/calls/call_2.md` — risultati security review, decisioni recenti (slide risultati/prossimi passi)
5. `results/evaluation/scores_1A.md` e `scores_1B.md` — se ci sono risultati da mostrare

**2. Mapping slide → sorgente (struttura attuale come riferimento):**

| Slide | Contenuto | Sorgente |
| --- | --- | --- |
| 01 Titolo | nome progetto, tagline | fisso |
| 02 Cos'è | obiettivo, ruoli, setup, consistenza | `architecture.md` §1 |
| 03 Setup 1A vs 1B | controllo vs confronto | `architecture.md` §2 |
| 04 Ruoli | expert / beginner / JSON output | `architecture.md` §2 |
| 05 Task | math vs textual, SVG | `architecture.md` §2 + task list da questo file |
| 06 Mappa codice | file e responsabilità | `architecture.md` §3 |
| 07 Flusso LangGraph | SVG grafo nodi | `architecture.md` §5 |
| 08 Ripetizioni vs retry | parametri esecuzione | `architecture.md` §5 |
| 09 Judge LLM | input/output, SVG | `architecture.md` §6.2 |
| 10 Output | file risultati, report | `architecture.md` §7 |
| 11 Metriche | accuracy / confidence / consistenza | `architecture.md` §6 |
| 12 Sfide aperte | problemi da risolvere | `supporto/calls/call_1.md` §8.1–8.10 (proposte non ancora implementate) |
| 13 Chiusura | tagline | fisso |

Aggiungere slide nuove (es. risultati security, confronto modelli) dopo la slide 11, prima della chiusura.

**3. Stile da preservare:**

- CSS e variabili `:root` invariate (palette `--gold`, `--accent`, `--bg`)
- Font stack: `Playfair Display` (serif, titoli), `IBM Plex Mono` (codice), `Inter` (corpo)
- Struttura HTML: `<section>` con classi `left-align` o centrata, componenti `.card`, `.mem-card`, `.code-block`, `.callout`
- SVG inline per diagrammi (non immagini esterne)
- Navigation JS invariato (frecce, touch, sidebar, progress bar)
- **Non aggiungere dipendenze esterne** oltre ai Google Fonts già presenti

**4. Quando aggiornare:**

- Quando cambiano i task disponibili → aggiorna slide 05
- Quando cambiano i modelli → aggiorna slide 03 e aggiorna le card
- Quando ci sono risultati da mostrare → aggiungi slide dopo la 11
- Quando cambiano le sfide aperte (nuove implementazioni) → aggiorna slide 12
- Non riscrivere slide già corrette — modificare solo quelle impattate

---

## Regola di aggiornamento

Dopo ogni modifica al codice:

- Aggiorna il file `architecture.md` se cambia la mappa codice, il flusso o la valutazione.
- Aggiungi una nuova sezione `§8.N` in `supporto/calls/call_1.md` o crea `docs/supporto/calls/call_<N>.md` per nuove call.
- Aggiorna questo index (tabelle modelli/task e checklist) se cambia la configurazione.
- Usa `> ✅ **Implementato:**` / `> ⚠️ **Correzione:**` inline nel documento di dettaglio corrispondente.
