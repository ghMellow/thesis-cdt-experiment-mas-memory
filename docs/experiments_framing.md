# Framing Experiment Plan — Expert vs Beginner Anomaly

---

## Protocollo di esecuzione (leggi prima di tutto)

Questo file è una **coda di esperimenti**. Ogni sessione con un LLM segue questo protocollo:

1. **Leggi questo file dall'inizio.**
2. **Trova il primo esperimento con `[ ] pending`** — quello è il prossimo da eseguire.
3. **Segui le istruzioni dell'esperimento:** branch suggerito, modifiche a `config.py` o `agents/prompts.py`, comando CLI.
4. **Esegui e attendi il completamento.**
5. **Aggiorna il campo `Risultato:`** con i dati chiave (accuracy per ruolo, norm score, note anomalie).
6. **Marca l'esperimento come completato:** cambia `[ ] pending` in `[x] done`.
7. **Salva il file.** La prossima sessione ripartirà dall'esperimento successivo ancora `[ ] pending`.

### Struttura di ogni esperimento

Ogni esperimento ha questi campi:

- **Setup:** cosa cambia rispetto alla baseline 1A
- **Predizione:** cosa ci si aspetta e perché
- **Modello / config.py:** parametri da impostare
- **Task:** quali task eseguire (primari o completo)
- **Branch suggerito:** branch git da usare per questa fase
- **Esperimento id:** cartella in `results/` dove salvare i file
- **CLI:** comando esatto da eseguire
- **Status:** `[ ] pending` → `[x] done`
- **Risultato:** da compilare dopo l'esecuzione

### Cosa fare prima di ogni esperimento

1. Controlla di essere sul branch giusto (`git branch`).
2. Verifica che `config.py` abbia i valori corretti per l'esperimento.
3. Verifica che non esistano già file in `results/<experiment_id>/` da run precedenti con config diversa — se sì, eliminarli prima di rieseguire.

---

**Motivazione:** su task7_vuln_amf con gemma4:e4b (4B), beginner batte expert (3/3 vs 2/3).
L'ipotesi del context window è stata falsificata (differenza 21 chars / ~8 token).
La causa più probabile: il framing "senior expert" induce analisi verbose sui bug facilmente visibili,
impedendo la scansione sistematica dello switch statement dove si trova il CVE target.

**Domanda centrale:** il paradosso è un problema di **framing** o di **capacità del modello**?

---

## Task scope — quali task eseguire

task5 è già risolto correttamente da entrambi i ruoli → escluso da tutti gli esperimenti.

Per ogni esperimento i task vanno eseguiti nell'ordine seguente (excerpt prima, full dopo):

```text
task6_vuln_udr → task6_vuln_udr_full → task7_vuln_amf → task7_vuln_amf_full → task8_vuln_udm → task8_vuln_udm_full → task9_vuln_cross
```

Ogni esperimento specifica se il task set è **completo** (tutti e 7 sopra) o **primario** (solo task6/7/8/9 excerpt, senza full).

CLI di riferimento per i task completo:

```bash
poetry run python main.py --task task6_vuln_udr --task task6_vuln_udr_full --task task7_vuln_amf --task task7_vuln_amf_full --task task8_vuln_udm --task task8_vuln_udm_full --task task9_vuln_cross
```

CLI per i task primari (excerpt only, più veloce):

```bash
poetry run python main.py --task task6_vuln_udr --task task7_vuln_amf --task task8_vuln_udm --task task9_vuln_cross
```

---

## Ipotesi A — Framing (il system prompt cambia il comportamento, non il modello)

### A1 — Prompt neutro
**Setup:** rimuovere completamente il system prompt (nessun ruolo). In `agents/prompts.py`, impostare `SYSTEM_PROMPTS["expert"] = ""` e `SYSTEM_PROMPTS["beginner"] = ""`.
**Predizione:** se neutro ≥ expert → il framing "senior engineer" è attivamente dannoso su modelli piccoli.
**Modello:** gemma4:e4b (locale, `use_hosted=False` in `config.py`)
**Task:** primari (task6/7/8/9 excerpt) — se A1 mostra effetto rilevante, estendere ai full
**Branch suggerito:** `exp/framing-prompts` (crea da main se non esiste)
**Esperimento id:** `framing_A1`
**CLI:**

```bash
poetry run python main.py --experiment 1A --experiment-id framing_A1 --role all --task task6_vuln_udr --task task7_vuln_amf --task task8_vuln_udm --task task9_vuln_cross --repetitions 3
```

**Status:** `[x] done`
**Risultato:** task7 discriminante: expert 66.7% (=1A), beginner 33.3% (era 100% in 1A). Rimuovere il framing penalizza il beginner di -66.7pp su task7 — il framing "junior technician" era attivamente utile. Task6/8/9: 100% entrambi, invariati. Conclusione: il paradosso è causato dal framing beginner (aiuta), non da un danno del framing expert. Pre-requisito A2: ripristinare i prompt originali in `agents/prompts.py` (vedi F16 in findings.md).

### A2 — Expert con vincolo di stile
**Setup:** aggiungere in coda al system prompt expert in `agents/prompts.py`: *"List each finding as a single bullet point. One sentence per finding. No elaboration."* Il resto del prompt expert rimane invariato.
**Predizione:** se questo recupera l'accuracy → il problema è la verbosità indotta dal framing, non la conoscenza tecnica.
**Modello:** gemma4:e4b (locale, `use_hosted=False`)
**Task:** primari (task6/7/8/9 excerpt)
**Branch suggerito:** `exp/framing-prompts` (stesso di A1)
**Esperimento id:** `framing_A2`
**CLI:**

```bash
poetry run python main.py --experiment 1A --experiment-id framing_A2 --role expert --task task6_vuln_udr --task task7_vuln_amf --task task8_vuln_udm --task task9_vuln_cross --repetitions 3
```

**Status:** `[x] done`
**Risultato:** task7 expert 33.3% (scende da 66.7% in 1A — peggiora). Task6/8/9: 100%, invariati. Il vincolo "one bullet, no elaboration" non recupera l'accuracy — la abbassa. La predizione era sbagliata: la verbosità non è il problema, è parte del processo di reasoning. Vedi F17 in findings.md.

### A3 — Beginner + expert knowledge injected
**Setup:** aggiungere in coda al system prompt beginner in `agents/prompts.py`: *"When reviewing code, scan switch statements and check for missing default cases."* Il resto del prompt beginner rimane invariato.
**Predizione:** se il beginner mantiene 3/3 → il framing non aggiunge nulla su modelli piccoli; se scende → la semplicità del framing era intenzionalmente utile.
**Modello:** gemma4:e4b (locale, `use_hosted=False`)
**Task:** primari (task6/7/8/9 excerpt)
**Branch suggerito:** `exp/framing-prompts` (stesso di A1/A2)
**Esperimento id:** `framing_A3`
**CLI:**

```bash
poetry run python main.py --experiment 1A --experiment-id framing_A3 --role beginner --task task6_vuln_udr --task task7_vuln_amf --task task8_vuln_udm --task task9_vuln_cross --repetitions 3
```

**Status:** `[x] done`
**Risultato:** task7 beginner 66.7% — scende da 100% in 1A ma superiore al 33.3% di A1. L'hint switch non replica il framing originale. Task6/8/9: 100% invariati (task6 norm=1.000, massimo visto). Conclusione: il framing beginner ha un effetto comportamentale ampio che non si riduce a una singola istruzione tecnica. Vedi F18 in findings.md.

---

## Ipotesi B — Capacità del modello (il framing complesso non è sostenibile da modelli piccoli)

### B1 — Scaling su ruolo expert

**Setup:** eseguire solo role=expert con modelli crescenti. e4b è già eseguito in 1A (baseline). Eseguire e2b e poi cloud.

- B1_e2b: in `config.py` impostare `expert_1A local = gemma4:e2b`, `use_hosted=False`
- B1_cloud: in `config.py` impostare `use_hosted=True` per expert_1A e scegliere il modello cloud disponibile

**Predizione:** se il paradosso sparisce con modelli più grandi → la capacità compensa il framing.
**Branch suggerito:** `exp/framing-models`
**Esperimento id:** `framing_B1_e2b` (poi `framing_B1_cloud`)
**CLI:**

```bash
poetry run python main.py --experiment 1A --experiment-id framing_B1_e2b --role expert --task task6_vuln_udr --task task7_vuln_amf --task task8_vuln_udm --task task9_vuln_cross --repetitions 3
```

**Status:** `[x] done` (B1_e2b + B1_cloud)
**Risultato (B1_e2b):** task7 expert (e2b) 0.0% — identico al beginner e2b in B3. Task8 0.0% (norm=0.593 vs beginner 0.408 — framing expert dà più copertura parziale ma sotto soglia). Task6/9 100%. Conclusione: l'advantage di expert su B3 task7 (33.3% vs 0%) era interamente effetto del modello (e4b > e2b), non del framing. Su e2b né il framing expert né il beginner funzionano sui task difficili. Vedi F20 in findings.md.
**Risultato (B1_cloud):** task7 expert (31b) **100%** — il paradosso scompare. Tutti e 4 i task al 100% con zero retry, Brier≈0. Norm: task6=1.000, task7=0.926, task8=0.852, task9=1.000. Scaling completo: e2b=0% → e4b=66.7% → 31b=100% su task7 expert. Vedi F21 in findings.md.

### B2 — Setup asimmetrico (1B): expert=grande, beginner=piccolo

**Setup:** expert su modello cloud grande, beginner su gemma3:4b-cloud. Prerequisito: accesso a modelli cloud.
**config.py:** `expert_1B hosted=gemma4:31b-cloud` · `beginner_1B hosted=gemma3:4b-cloud` · `use_hosted=True`
**Predizione:** se expert batte beginner → era capacità. Se ancora non batte → è framing.
**Branch suggerito:** `exp/framing-models` (stesso di B1)
**Esperimento id:** `framing_B2`
**CLI:**

```bash
poetry run python main.py --experiment 1B --experiment-id framing_B2 --role all --task task6_vuln_udr --task task6_vuln_udr_full --task task7_vuln_amf --task task7_vuln_amf_full --task task8_vuln_udm --task task8_vuln_udm_full --task task9_vuln_cross --repetitions 3
```

**Status:** `[ ] pending` (dipende da accesso modelli cloud)
**Risultato:** —

### B3 — Setup asimmetrico inverso: expert=e4b, beginner=e2b

**Setup:** expert su e4b, beginner su e2b. In `config.py`: `expert_1A local=gemma4:e4b` · `beginner_1A local=gemma4:e2b` · `use_hosted=False`.
**Predizione:** se expert batte beginner → su modelli molto piccoli il framing esperto aiuta.
**Branch suggerito:** `exp/framing-models` (stesso di B1/B2)
**Esperimento id:** `framing_B3`
**CLI:**

```bash
poetry run python main.py --experiment 1A --experiment-id framing_B3 --role all --task task6_vuln_udr --task task7_vuln_amf --task task8_vuln_udm --task task9_vuln_cross --repetitions 3
```

**Status:** `[x] done`
**Risultato:** task7 — il paradosso si inverte: expert (e4b) 33.3% > beginner (e2b) 0.0%. In 1A era beginner 100% > expert 66.7%. Task8 — expert 100% vs beginner 0.0% (in 1A entrambi a 77.8% norm). Task6/9 invariati al 100%. Il beginner su e2b esaurisce MAX_RETRIES su task7 e task8 (avg_attempts=3.00, Brier=1.000). Conclusione: il paradosso è framing × capacità — il vantaggio del framing beginner richiede capacità sufficiente. Vedi F19 in findings.md.

---

## Tabella comparativa setup

| Setup | Expert | Beginner | Task | Cosa misura |
|---|---|---|---|---|
| 1A (eseguito) | gemma4:e4b | gemma4:e4b | task6–9 excerpt | Puro effetto framing a parità di modello |
| A1 | neutro (no role) | neutro | task6–9 excerpt | Baseline senza framing |
| A2 | e4b + stile vincolato | e4b | task6–9 excerpt | Framing knowledge vs framing verbosità |
| A3 | e4b | e4b + hint tecnico | task6–9 excerpt | Il hint tecnico aiuta o disturba il beginner? |
| B1_e2b | gemma4:e2b | — | task6–9 excerpt | Scaling verso il basso del modello expert |
| B1_cloud | [cloud TBD] | — | task6–9 excerpt | Scaling verso l'alto del modello expert |
| B2 (1B) | gemma4:31b-cloud | gemma3:4b-cloud | task6–9 full | Modello grande compensa il framing? |
| B3 | gemma4:e4b | gemma4:e2b | task6–9 excerpt | Framing expert aiuta su modelli molto piccoli? |

---

## Ordine di esecuzione suggerito

1. **A1** — zero costo locale, risponde direttamente se il framing è la causa
2. **A2** — distingue "conoscenza del ruolo" da "stile di risposta"
3. **A3** — completa il quadro del framing
4. **B3** — test locale asimmetrico inverso senza cloud
5. **B1_e2b** — scaling verso il basso, locale
6. **B2 + B1_cloud** — dopo accesso a modelli cloud (§5.2 di overview_call_3.md)

---

## Finding già acquisiti (baseline)

| Esperimento | Modello | Expert | Beginner | Note |
|---|---|---|---|---|
| 1A — task7 | gemma4:e4b | 2/3 correct | 3/3 correct | `missing_default_score=0` in tutti i retry dell'expert rep3 |
| 1A — task8 | gemma4:e4b | 0.778 norm | 0.778 norm | `spec_reference_score=0` sistematico in entrambi |
| 1A — task9 | gemma4:e4b | 3/3 correct | 3/3 correct | 9/9 ogni run, zero varianza |
| 1A — task1 | gemma3:4b-cloud | 3/3 (con retry) | 3/3 (no retry) | Bug template: answer prima di reasoning → fix applicato |

---

## Ipotesi C — Temperatura (fase separata, dopo A e B)

Gli esperimenti A e B usano temperatura fissa 0.3 per isolare la variabile framing. Solo quando A e B sono completati ha senso variare la temperatura — altrimenti si hanno due variabili cambiate contemporaneamente e il risultato non è interpretabile.

### C1 — Temperature sweep su task7/8

**Prerequisito:** A1–A3 e B3 completati. Almeno una conclusione chiara su framing vs capacità.

**Setup:** eseguire task7_vuln_amf e task8_vuln_udm con T ∈ {0.1, 0.3, default_model, 0.7} — stesso modello (gemma4:e4b), stesso prompt (1A standard).

**Predizione:**

- Se accuracy aumenta con T più alta → T=0.3 era troppo deterministica e forzava convergenza sullo stesso errore (F5 generalizzato oltre il retry).
- Se accuracy è flat → il problema è la capacità o il framing, non la temperatura.

**Cosa misurare:** accuracy per temperatura + varianza tra le 3 ripetizioni (con T alta ci si aspetta più varianza).

**Esperimento id:** `temp_C1_T01`, `temp_C1_T03`, `temp_C1_Tdef`, `temp_C1_T07`

**Status:** `[ ] pending` — dopo completamento A e B

---

## Note metodologiche

- Tutti gli esperimenti A e B usano 3 ripetizioni per consistenza con le run esistenti.
- **Temperatura fissa a 0.3** per tutti gli esperimenti A e B — isola la variabile framing. Non cambiare la temperatura in questa fase.
- Il temperature sweep (C1) è una fase separata, da eseguire solo dopo aver concluso A e B.
- I risultati vanno salvati in `results/` con experiment_id dedicato (es. `framing_A1`, `framing_A2`) per non mescolarli con 1A/1B.
- Il template risposta ora è `Reasoning → Answer → Confidence` dopo il fix §6.5 — da usare in tutti i nuovi esperimenti.
