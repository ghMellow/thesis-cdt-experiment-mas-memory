# Framing Experiment Plan — Expert vs Beginner Anomaly

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
python main.py --task task6_vuln_udr task6_vuln_udr_full task7_vuln_amf task7_vuln_amf_full task8_vuln_udm task8_vuln_udm_full task9_vuln_cross
```

CLI per i task primari (excerpt only, più veloce):

```bash
python main.py --task task6_vuln_udr task7_vuln_amf task8_vuln_udm task9_vuln_cross
```

---

## Ipotesi A — Framing (il system prompt cambia il comportamento, non il modello)

### A1 — Prompt neutro
**Setup:** rimuovere completamente il system prompt (nessun ruolo).
**Predizione:** se neutro ≥ expert → il framing "senior engineer" è attivamente dannoso su modelli piccoli.
**Modello:** gemma4:e4b (locale, use_hosted=False)
**Task:** primari (task6/7/8/9 excerpt) — se A1 mostra effetto rilevante, estendere ai full
**Esperimento id:** `framing_A1` (--experiment 1A --role all)
**Status:** `[ ] pending`
**Risultato:** —

### A2 — Expert con vincolo di stile
**Setup:** aggiungere al system prompt expert: *"List each finding as a single bullet point. One sentence per finding. No elaboration."*
**Predizione:** se questo recupera l'accuracy → il problema è la verbosità indotta dal framing, non la conoscenza tecnica.
**Modello:** gemma4:e4b (locale, use_hosted=False)
**Task:** primari (task6/7/8/9 excerpt)
**Esperimento id:** `framing_A2` (--experiment 1A --role expert)
**Status:** `[ ] pending`
**Risultato:** —

### A3 — Beginner + expert knowledge injected
**Setup:** aggiungere al system prompt beginner una frase tecnica aggiuntiva, es. *"When reviewing code, scan switch statements and check for missing default cases."*
**Predizione:** se il beginner mantiene 3/3 → il framing non aggiunge nulla su modelli piccoli; se scende → la semplicità del framing era intenzionalmente utile.
**Modello:** gemma4:e4b (locale, use_hosted=False)
**Task:** primari (task6/7/8/9 excerpt)
**Esperimento id:** `framing_A3` (--experiment 1A --role beginner)
**Status:** `[ ] pending`
**Risultato:** —

---

## Ipotesi B — Capacità del modello (il framing complesso non è sostenibile da modelli piccoli)

### B1 — Scaling su ruolo expert

**Setup:** eseguire solo expert con modelli crescenti: e2b → e4b (già eseguito in 1A) → cloud.
**Predizione:** se il paradosso sparisce con modelli più grandi → la capacità compensa il framing.
**Modello:** gemma4:e2b poi gemma4:e4b poi [cloud TBD]
**Task:** primari (task6/7/8/9 excerpt) — solo role=expert
**Esperimento id:** `framing_B1_e2b`, `framing_B1_cloud`
**Status:** `[ ] pending` (B1_cloud dipende da accesso modelli cloud)
**Risultato:** —

### B2 — Setup asimmetrico (1B): expert=grande, beginner=piccolo

**Setup:** expert su modello cloud grande, beginner su gemma3:4b-cloud.
**Predizione:** se expert batte beginner → era capacità. Se ancora non batte → è framing.
**config.py:** expert_1B hosted=gemma4:31b-cloud · beginner_1B hosted=gemma3:4b-cloud · use_hosted=True
**Task:** completo (task6/7/8/9 excerpt + full)
**Esperimento id:** `1B` (setup standard, già configurato in config.py)
**Status:** `[ ] pending`
**Risultato:** —

### B3 — Setup asimmetrico inverso: expert=e4b, beginner=e2b

**Setup:** expert su e4b, beginner su e2b (modello più piccolo).
**Predizione:** se expert batte beginner → su modelli molto piccoli il framing esperto aiuta.
**config.py:** expert_1A local=gemma4:e4b · beginner_1A local=gemma4:e2b · use_hosted=False
**Task:** primari (task6/7/8/9 excerpt)
**Esperimento id:** `framing_B3` (--experiment 1A --role all)
**Status:** `[ ] pending`
**Risultato:** —

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

## Note metodologiche

- Tutti gli esperimenti usano 3 ripetizioni per consistenza con le run esistenti.
- Temperature fissa a 0.3 (stesso valore delle run 1A) per isolare la variabile framing.
- I risultati vanno salvati in `results/` con experiment_id dedicato (es. `framing_A1`, `framing_A2`) per non mescolarli con 1A/1B.
- Il template risposta ora è `Reasoning → Answer → Confidence` dopo il fix §6.5 — da usare in tutti i nuovi esperimenti.
