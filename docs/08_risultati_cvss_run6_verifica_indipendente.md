# Esperimento 2b — Run 6: verifica indipendente su contesto pieno — F17/F18/F21 si confermano su dati freschi

> Documento di condivisione per il team. Prima run con `run_id` reale (non "legacy"): `20260712T142416Z`. Stesso setup di [run 5](07_risultati_cvss_run5_full_context.md) (task5, task6/7/8 `_full`, task9), lanciata da zero dopo aver ripulito `results/` — serve da **verifica indipendente**: gli stessi pattern osservati nella run precedente si confermano su un campione fresco, non erano un caso isolato di quella singola run.

**Data run:** 2026-07-12 · **Autore:** Nicolò (con supporto AI) · **Run precedente:** [run 5](07_risultati_cvss_run5_full_context.md) (stesso setup, `results/` poi svuotata su richiesta) · **run_id:** `20260712T142416Z` (verificabile con `poetry run python -m utils.evaluation_utils --list-runs`)

---

## 0. Cosa cambia rispetto alla run 5

Nulla nel setup — stessi task, stesso prompt, stesso hint, stessa matematica ufficiale. L'unica differenza è che i dati sono stati rigenerati da zero (run precedente cancellata su richiesta esplicita) e questa volta il `run_id` è reale fin dall'inizio, non retroattivo.

⚠️ **Stesso caveat delle run 4/5, confermato anche qui**: `agent_1A`, `agent_1B` e `judge` risolvono tutti a `gemma4:31b-cloud` (verificato nei JSON). **1A e 1B non sono due condizioni sperimentali diverse in questa run — sono lo stesso identico setup**, quindi ogni differenza tra le loro colonne è puro rumore di campionamento (T=0.3), non un effetto di modello.

---

## 1. Risultati d'insieme

### Blocco A — rubrica testuale

| task | 1A correct/3 | 1A avg norm | 1B correct/3 | 1B avg norm |
|---|---|---|---|---|
| task5_vuln_pcf | 3/3 | 1.000 | 3/3 | 1.000 |
| **task6_vuln_udr_full** | **0/3** | 0.481 | **0/3** | 0.444 |
| task7_vuln_amf_full | 2/3 | 0.889 | 1/3 | 0.778 |
| task8_vuln_udm_full | 3/3 | 0.778 | 3/3 | 0.778 |
| task9_vuln_cross | 3/3 | 1.000 | 3/3 | 1.000 |
| **Totale** | **11/15 (73.3%)** | | **10/15 (66.7%)** | |

**Il crollo di task6_full si conferma esattamente** (F21): 0/6 su due run indipendenti ora, sempre 3 tentativi esauriti. task8_full e task9 restano stabili al 100%/78%. **task7_full è l'unico task dove 1A e 1B differiscono (2/3 vs 1/3)** — ma essendo 1A e 1B lo stesso modello, questo *non* è un effetto sperimentale: è la stessa variabilità di campionamento già documentata per questo task (F12, run 3).

### Blocco B — CVSS, matematica ufficiale (23 finding abbinati su questa run)

| task | n | coerenza Δ | Δ vettore vs B | banda vettore vs B (0–3) | dist. impatto |
|---|---|---|---|---|---|
| task5 | 6 | 1.25 | 2.80 | 0.34 | 0.55 |
| **task6_full** | 5 | 1.36 | 0.42 | **2.60** | 0.26 |
| task7_full | 6 | 1.55 | 1.30 | 1.67 | 0.42 |
| **task8_full** | 6 | 0.90 | **3.50** | **0.00** | 0.36 |
| task9 | 0 | n/a | n/a | n/a | n/a (14 unmatched, come sempre — F4) |
| **Media pesata** | **23** | **1.24** | **2.08** | **1.09** | **0.41** |

Aggregati calcolati a mano da questo run (`agent`/`20260712T142416Z`); i numeri per-esperimento (1A/1B separati) sono nei rispettivi `results/evaluation/result_<task>_<exp>.md`.

---

## 2. Risposta diretta alle tre domande

**Ci sono differenze 1A vs 1B, visto che modelli e prompt sono identici?** Sì (73.3% vs 66.7%), interamente concentrate su task7_full, e **non sono un effetto reale**: 1A e 1B usano lo stesso identico modello per agente e giudice in questa run (verificato nei JSON: `gemma4:31b-cloud` ovunque). La differenza è temperatura > 0 su un task già noto per essere il punto fragile del sistema (F12/F21) — è la controprova che, quando davvero non c'è nessuna variabile a differenziare 1A da 1B, il gap osservato è proprio la misura del rumore di campionamento puro su quel task. Per un confronto 1A/1B che misuri qualcosa di reale serve differenziare i modelli in `config.MODELS` prima della prossima run (punto aperto ripetuto da run 4).

**Quanto distano i vettori predetti da quelli ufficiali, e in che direzione?** Il Δ riportato sopra è un valore assoluto — dice quanto ma non se il modello è più prudente o più allarmista della realtà. Con il segno (`computed − GT base pura`; negativo = sottostima, positivo = sovrastima):

| task | Δ con segno per rep | media | lettura |
|---|---|---|---|
| task5 | −3.4, −1.6, −1.6, −3.4, −3.4, −3.4 | **−2.80** | sottostima **sistematica**: mai una ripetizione va nella direzione opposta |
| task6_full | 0.0, +0.2, −1.6, +0.3, +0.2 | −0.18 | oscilla intorno allo zero, **nessun bias direzionale** — è dispersione, non errore sistematico |
| task7_full | −1.6, +1.4, −1.6, −1.6, +1.4, +0.2 | −0.30 | segno che **cambia da una ripetizione all'altra** — stessa lettura di task6 |
| task8_full | −3.6, −3.6, −3.4, −3.6, −3.4, −3.4 | **−3.50** | sottostima **sistematica**, la più marcata |

**Distinzione importante**: task5/task8 hanno un vero **bias direzionale riproducibile** (ogni singola ripetizione sottostima, mai il contrario — coerente con F18, lettura conservativa dell'impatto). task6/task7 invece non hanno una direzione dominante: l'errore è **varianza**, il modello sovrastima tanto quanto sottostima a seconda della ripetizione. Le implicazioni sono diverse: su task5/8 va corretto un bias specifico (probabilmente nella percezione dell'impatto); su task6/7 va ridotta la variabilità della stima, non una direzione sbagliata.

**Cosa ricaviamo di nuovo?** Vedi findings sotto — la sintesi è che **questa run non aggiunge un fenomeno nuovo, conferma che quelli di run 4/5 sono reali e riproducibili**, non artefatti di un singolo campionamento.

---

## 3. Findings (continuano la numerazione di [run 5](07_risultati_cvss_run5_full_context.md))

**F25 — F17 (score dichiarato sistematicamente sotto il vettore) si conferma su un campione completamente indipendente.** 20/23 finding con declared < computed, scarto medio −1.20 (era −1.35 in run 4, −1.21 in run 5, ora −1.20). Tre run indipendenti convergono sullo stesso numero: non è rumore, è un bias strutturale del modello nel dichiarare lo score.

**F26 — Il collo di bottiglia di task6_full resta il matching, non il vettore (F22 riconfermato).** Solo 2/18 (1A) e 3/18 (1B) possibili abbinamenti CVE riusciti, ma quando l'abbinamento avviene lo score ricalcolato è quasi esatto (Δ 0.42 medio, banda 2.60/3 — la migliore di tutto il dataset). Il problema non è la qualità della stima quando il modello identifica il bug giusto — è che lo identifica raramente.

**F27 — Il bias di sottostima dell'impatto su task8 (F9/F18) è ora confermato su due run full-context indipendenti con lo stesso valore (Δ ~3.5, banda 0/3).** Coerenza interna alta in entrambe le run (0.90 qui, 0.45–0.65 in run 4/5) — il modello è internamente consistente ma il vettore che costruisce è sbagliato sull'impatto di confidenzialità, in modo riproducibile.

**F29 — Non tutti i task sbagliano nello stesso modo: task5/task8 hanno un bias direzionale (sempre sottostima, mai il contrario), task6/task7 hanno solo dispersione (il segno cambia ripetizione per ripetizione, media vicina a zero).** Verificato sul Δ con segno per rep (§2): task5 (−3.4,−1.6,−1.6,−3.4,−3.4,−3.4) e task8 (−3.6,−3.6,−3.4,−3.6,−3.4,−3.4) non hanno mai un segno positivo; task6 (0.0,+0.2,−1.6,+0.3,+0.2) e task7 (−1.6,+1.4,−1.6,−1.6,+1.4,+0.2) oscillano. **Implicazione:** correggere task5/8 richiede un intervento mirato sul bias di percezione dell'impatto (prompt/contesto); correggere task6/7 richiederebbe invece ridurre la variabilità della stima (es. più campioni, temperatura più bassa), non una direzione sbagliata da correggere.

**F28 — Con 1A e 1B a modello identico, il gap di accuratezza osservato (73.3% vs 66.7%, tutto su task7) è la misura diretta del rumore di campionamento puro su un task fragile.** Nessuna variabile sperimentale separa 1A da 1B in questa run — è la controprova più pulita finora che le fluttuazioni 1A/1B a questo campione (n=3 per cella) non vanno lette come effetti se non si è certi che i due bracci usino modelli diversi.

---

## 4. Che cosa dire al team

**I findings di run 4/5 non erano rumore di una singola run: si riproducono identici su un campione fresco e indipendente.** In particolare F17 (il vettore batte il numero dichiarato) e il bias di task8 (impatto sottostimato) sono ormai osservazioni **stabili e riproducibili**, non artefatti di campionamento — un argomento più solido per l'articolo rispetto a un singolo risultato.

**Punto pratico da chiudere prima della prossima run:** differenziare davvero `agent_1A`/`agent_1B`/`judge` in `config.py` — finché restano tutti sullo stesso modello, 1A vs 1B non misura nulla di significativo (F28).

**Punti aperti** (invariati da run 5): B vs BT come riferimento; calibrazione bande; matching multi-CVE task6 (ora ancora più debole, F26); interpolazione FIRST vettore↔vettore; CVE-2026-47780 fuori perimetro.

---

## 5. Come riprodurre

```bash
poetry run python main.py --experiment all \
  --task task5_vuln_pcf --task task6_vuln_udr_full --task task7_vuln_amf_full \
  --task task8_vuln_udm_full --task task9_vuln_cross
```

Questa run ha `run_id=20260712T142416Z` — per isolarla esplicitamente in futuro (anche se al momento è l'unica presente):

```bash
poetry run python -m utils.evaluation_utils --run-id 20260712T142416Z
```
