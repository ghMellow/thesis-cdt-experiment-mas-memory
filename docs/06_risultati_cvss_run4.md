# Esperimento 2b — Run 4: agente unico, matematica ufficiale CVSS 4.0, prompt a 11 metriche

> Documento di condivisione per il team. Prima run dopo le due semplificazioni decise in call 11 (2026-07-10): **agente unico** (ruoli expert/beginner rimossi) e **valutazione CVSS con la matematica ufficiale FIRST 4.0** al posto del confronto binario per lettera. In più, il prompt ora chiede il **vettore base completo a 11 metriche** (aggiunte SC/SI/SA). 30 run totali (5 task × 1A/1B × 3 rep).

**Data run:** 2026-07-10 · **Autore:** Nicolò (con supporto AI) · **Run precedenti:** [run 3](05_risultati_cvss_run3.md) (60 run, expert/beginner, prompt a 8 metriche) · La run agente-unico con il prompt a 8 metriche (stessa giornata, pre-estensione) è conservata in `results/<task>/<exp>/agent_8m/` e usata qui come confronto diretto.

---

## 0. Cosa cambia rispetto alla run 3

1. **Agente unico** (`SYSTEM_PROMPTS["agent"]`, prompt neutro): 30 run invece di 60. Coerente con F12 di run 3 (l'effetto di ruolo non esisteva).
2. **Valutazione con la matematica ufficiale** (`utils/cvss_eval.py` + libreria `cvss` di RedHat, port Python diretto della reference implementation FIRST [cvss-v4-calculator](https://github.com/FIRSTdotorg/cvss-v4-calculator): stessa lookup table a 270 macrovettori, stessa interpolazione `severity_distance`/`mean_distance` — validato: i 10 vettori GT ricalcolati coincidono tutti con gli score NVD/CNA). Nuovi assi per ogni finding abbinato:
   - `computed_score_B` — lo score che il vettore stimato *vale davvero*;
   - `score_coherence_delta` — |score dichiarato − score del proprio vettore| (i due output dell'agente sono generati indipendentemente);
   - `computed_delta_vs_B` — distanza del vettore dalla GT espressa in punti CVSS;
   - distanze ordinali di severità per campo (exploitability / impatto / subsequent, 0–1).
   La rivalutazione è **retroattiva** (`python -m utils.cvss_eval`): anche run 1–3 e `agent_8m` hanno i nuovi campi — ogni confronto con run precedenti citato in questo documento usa quindi la **stessa** matematica ufficiale, mai il vecchio criterio.
3. **Prompt a 11 metriche**: il blocco CVSS chiede anche SC/SI/SA (impatto sui sistemi a valle).
4. ⚠️ **Caveat setup**: in questa run `agent_1A`, `agent_1B` e `judge` puntano tutti a `gemma4:31b-cloud` — 1A e 1B sono quindi lo **stesso setup** sotto due etichette (di fatto 6 campioni per task, non 2 condizioni). Da differenziare in config alla prossima run se si vuole tornare al confronto "stesso modello vs modelli diversi".

---

## 1. Risultati d'insieme

### Blocco A — rubrica testuale (30 run)

| correct | avg score normalizzato | wrong |
|---|---|---|
| 29/30 (96.7%) | 0.941 | task7_vuln_amf / 1A / rep 1 (3 tentativi) |

L'unico wrong è su task7, il punto fragile già noto del sistema (F12): la ripetizione che ci cade sopra cambia a ogni campionamento.

### Blocco B — CVSS con la matematica ufficiale (24 finding abbinati su 24 possibili; task9 sempre `null`, F4)

| n | coerenza Δ (dich.↔vettore) | Δ vettore vs B (punti CVSS) | banda score *ricalcolato* vs B | banda score *dichiarato* vs B (diagnostica) | dist. impatto (0–1) | dist. exploitability (0–1) | SC/SI/SA emesse |
|---|---|---|---|---|---|---|---|
| 24 | 1.35 (σ 1.12) | 1.72 | **1.42 / 3** | 0.54 / 3 | 0.53 | 0.10 | 24/24 |

**La lettura centrale: lo score ricalcolato dal vettore è molto più vicino alla GT dello score dichiarato** (banda 1.42/3 contro 0.54/3). Il vettore è l'output affidabile; il numero dichiarato no (→ F17). Per questo, da questa run in poi, **lo score dichiarato è declassato a diagnostica di coerenza interna**: nei report le sue colonne sono marcate come non-ufficiali, e le metriche di riferimento sono quelle ricalcolate dal vettore.

---

## 2. Per-task: cosa dice la matematica ufficiale che prima non si vedeva

| Task | GT B | dichiarato (avg) | ricalcolato dal vettore (avg) | coerenza Δ | Δ vettore vs B | banda ricalc. vs B |
|---|---|---|---|---|---|---|
| task5 (CVE-41135, DoS puro VA:H) | 8.7 | 5.0 | 6.6 | 1.62 | 2.07 | 1.17/3 |
| task6 (CVE-40246, VC/VI/VA:H) | 8.7 | 6.5 | 7.9 | 1.33 | 0.82 | **2.33/3** |
| task7 (CVE-41136, VI:L) | 6.9 (pubbl. BT 5.5) | 3.9 | 5.9 | 2.00 | 1.13 | 1.67/3 |
| task8 (CVE-42459, VC:H) | 8.7 (pubbl. BT 7.7) | 5.4 | 5.8 | **0.45** | **2.87** | 0.50/3 |

**Il pattern generale (21 finding su 24): il modello dichiara meno di quanto il suo vettore valga.** Scarto medio dichiarato−ricalcolato = **−1.35** (nella run 8m: −0.94, 23/24). Non è rumore simmetrico, è un bias sistematico di prudenza sul numero. E siccome la GT sta *sopra*, il vettore ricalcolato è quasi sempre la stima migliore.

**task6 — il vettore è quasi giusto.** Δ 0.82 punti dalla GT, banda ricalcolata 2.33/3 (nella run 8m addirittura score ricalcolato medio 8.7 = esatto). Con la valutazione vecchia (banda sul dichiarato: 0.83/3) questo task sembrava mediocre — era un artefatto dello score dichiarato basso, il vettore era buono. Resta invariato il limite di matching F14: sempre 1 CVE abbinata su 3 (12 `missed_cves` su 12 run, zero varianza — strutturale).

**task8 — F9 ora è localizzato con precisione: il bias sta nel vettore, non nel numero.** Coerenza quasi perfetta (0.45: il modello dichiara esattamente ciò che il suo vettore vale, ~5.1–5.8) ma Δ vettore vs B = 2.87, il peggiore. Il modello costruisce *proprio un vettore da 5* (VC sottostimato), non sbaglia la conversione. Qualsiasi correzione deve agire sulla stima dell'impatto, non sullo scoring.

**task7 — il caso opposto: qui il problema era la conversione.** Coerenza peggiore del lotto (2.00: dichiara 3.9 per vettori che valgono 5.9) e il vettore ricalcolato è vicino sia al published BT (5.5) sia decentemente al B (6.9). Il "task fragile" del Blocco A ha anche gli score dichiarati più scollegati dal proprio vettore.

**task5 — resta il caso peggiore sul contenuto del vettore** dopo task8 (Δ 2.07 vs B): il DoS puro continua a essere letto con impatto confidenzialità (F13), e ora si vede che il danno è ripartito tra vettore sbagliato *e* numero dichiarato ancora più basso del vettore.

---

## 3. Findings (continuano la numerazione di [run 3](05_risultati_cvss_run3.md))

**F17 — Lo score dichiarato è sistematicamente più basso di quanto vale il vettore che lo accompagna; lo score ricalcolato è la stima migliore.** Scarto medio −1.35 (21/24 casi in questa run; il pattern si osserva identico anche rivalutando la run gemella pre-estensione con la stessa matematica: −0.94, 23/24 — quindi precede il cambio di prompt). Banda vs B: 1.42/3 col ricalcolato contro 0.54/3 col dichiarato. **Decisione conseguente: lo score dichiarato è declassato a diagnostica di coerenza interna** — si continua a chiederlo (costa zero e F17 è un finding in sé), ma nei report le sue colonne sono esplicitamente marcate come non-ufficiali; ranking per triage (caso d'uso Lorenzo) e metriche di confronto usano solo `computed_score_B`.

**F18 — F9 (task8 sottostimato) è un bias nel *vettore*, non nello scoring.** Coerenza interna quasi perfetta (0.45) ma vettore a 2.87 punti dalla GT: il modello "crede" davvero a una severità 5 e costruisce il vettore di conseguenza. L'hint di contesto non c'entra con la conversione — è la percezione dell'impatto VC a monte che va corretta (contesto più specifico per NF, direzione Mariano/Andrea).

**F19 — L'estensione del prompt a 11 metriche è neutra sulla qualità: il modello emetteva già SC/SI/SA spontaneamente in tutti i 24 finding abbinati anche col prompt a 8** (verificato sulla run gemella `agent_8m`, rivalutata con la stessa matematica ufficiale). Il valore dell'estensione è di *formato* (vettore completo garantito per costruzione → score ufficiale calcolabile senza padding), non di accuratezza. Unica differenza osservata: più finding totali (52 vs 44) e più unmatched (28 vs 20) — direzione "più verboso", entro il rumore.

**F20 — L'agente unico non perde nulla rispetto al setup a due ruoli.** Avg normalizzato 0.941 (identico al valore storico con expert+beginner), unico wrong sul solito task7, stessi pattern CVSS per task. La semplificazione di call 11 ha dimezzato le chiamate a parità di qualità.

---

## 4. Che cosa dire al team

**Lo score ora ha senso** — era il punto sollevato in call 11 ("adesso tira fuori le lettere però non c'è un punteggio calcolato sulle lettere"): il vettore stimato viene ripassato nell'algoritmo ufficiale FIRST e produce uno score confrontabile e riproducibile. La scoperta principale è che **il vettore era già più bravo del numero**: il modello quantifica meglio di quanto dichiari, e la valutazione vecchia (bande sul dichiarato) sottostimava sistematicamente la qualità delle stime.

Per il **flusso pratico** (esperimento 3, SonarQube+LLM): la lista ordinabile per il triage va costruita su `computed_score_B`. Il campo è già in ogni JSON, insieme al dichiarato — nessun dato perso.

**Punti ancora aperti:**
1. **B vs BT** come riferimento principale nell'articolo (task7: il ricalcolato è più vicino al published BT che al B — il confronto giusto dipende da questa scelta);
2. calibrazione bande (ora applicate anche alle Δ ricalcolate);
3. matching multi-CVE task6 (F14, strutturale);
4. interpolazione FIRST vettore↔vettore (materiale Mariano) — oggi la distanza usa i due score ricalcolati;
5. differenziare davvero 1A/1B in config: in questa run erano lo stesso setup (caveat §0.4);
6. CVE-2026-47780 (la regex `|.+` scoperta dal team) ha `task_id: null` nel dataset: la regex vulnerabile non sta nei 4 file usati dai task, quindi non è valutabile da nessuna run — decidere se resta fuori perimetro o se merita un task dedicato.

**Prossima run pianificata:** solo varianti a contesto pieno — task5 (già full di fatto: l'estratto copre il file), task6/7/8 in variante `_full`, task9 (parziale per costruzione, cross-NF). Per task6 la GT si allarga da 3 a 6 CVE: le 3 fuori estratto (`in_task_excerpt: false`) entrano nella valutazione solo con la variante full.

---

## 5. Come riprodurre

```bash
poetry run python main.py --experiment all \
  --task task5_vuln_pcf --task task6_vuln_udr --task task7_vuln_amf \
  --task task8_vuln_udm --task task9_vuln_cross
```

Prompt a 11 metriche in `utils/cvss_utils.py` (`CVSS_PROMPT_BLOCK`), hint di contesto NF invariato (`CVSS_CONTEXT_HINT_ENABLED = True`). La rivalutazione con la matematica ufficiale si riapplica a qualsiasi risultato salvato con `poetry run python -m utils.cvss_eval` (nessuna run da rilanciare). La run gemella col prompt a 8 metriche è in `results/<task>/<exp>/agent_8m/`; run 1–3 nelle cartelle archiviate indicate in [05_risultati_cvss_run3.md §5](05_risultati_cvss_run3.md#5-come-riprodurre).
