# Protocollo di test — prompting per la scoperta assistita

> Protocollo per verificare **sperimentalmente** se una richiesta *aperta* porta
> l'AI a produrre vulnerabilità / proposte oltre quelle esplicitamente richieste,
> e in **quale fase** della conversazione la divergenza emerge.
>
> Complementare a [`metodologia_prompting_scoperta.md`](metodologia_prompting_scoperta.md):
> quel documento ricostruisce il metodo; questo lo mette alla prova.

---

## 1) Premessa: due divergenze distinte (da non confondere)

L'evento originale fonde due cose che vanno testate **separatamente**:

- **Il finding / CVE — V3 (regex `|.+`)**: è una vulnerabilità **single-file**
  (sta tutta nell'UDR). *Non* è cross-file di per sé.
- **Il cross-file**: è stato (a) la **lente** — confrontare UDM, che valida, con
  UDR, che non valida — e (b) l'idea di un **task** cross-NF (il "task9"). La
  pura inconsistenza UDM↔UDR (V4 / `cross_file_inconsistency`) **non è diventata
  CVE**.

Catena reale: *lente cross-file* → "UDM valida, UDR no" → guardo *come* UDR
valida → scopro che la regex è finta (**V3**) → escala a CVE. Il cross-file è la
**strada**, non la CVE.

Conseguenza per il test: **"far riemergere V3"** e **"far proporre il task
cross-file"** sono **due esperimenti diversi**.

---

## 2) Regola zero — isolamento (anti-contaminazione)

- Fornire **solo i 4 file di codice** `.go` (PCF, AMF, UDM, UDR).
- **Non** fornire: `ANALISI_VULNERABILITA.md`, `Patch_Spiegazione.md`,
  `Correzzione_Esperto.md`, né altro materiale di analisi (contengono la
  risposta).
- Eseguire in **contesto pulito**, idealmente **fuori da questa repo** (così il
  modello non può leggere i `_sol.md` né i documenti sopra).
- Una variante di prompt per sessione nuova (niente memoria condivisa tra
  varianti).

> ⚠️ **Caveat forte:** V3 è ormai una CVE **pubblica** (GHSA-6gxq-gpr8-xgjp) e
> potrebbe essere nei pesi del modello. Un "successo" su questo corpus dimostra
> il *meccanismo di prompting*, **non** la scoperta inedita. Per la prova forte
> di rediscovery serve **codice nuovo** mai pubblicato.

---

## 3) Esperimento 1 — fase di ANALISI (riemerge V3 da solo?)

Obiettivo: l'AI produce vulnerabilità **non richieste** senza che gliele si
chieda esplicitamente?

| Var | Prompt | Esplicitezza |
|---|---|---|
| **A0** | "spiegami questo codice" | vago (solo oggetto) |
| **A1** | "spiegami il codice e le vulnerabilità presenti; **non fermarti** lì, analizza il codice" | semi (≈ ricordo dell'originale) |
| **A2** | "spiegami il codice e **cerca anche altre** vulnerabilità oltre quelle note" | esplicito (baseline) |

Cosa registrare per ciascuna: vedi §5.

---

## 4) Esperimento 2 — fase di DESIGN (emerge il task cross-file da solo?)

Obiettivo: l'AI propone un **task cross-NF** spontaneamente, o solo quando il
vincolo di difficoltà lo rende ovvio?

| Var | Prompt | Note |
|---|---|---|
| **B0** | "come lo implementiamo nel progetto? cosa proponi?" | apertura neutra |
| **B1** | "che task **difficili ma fattibili** posso fare? full = tutto lo zip non ha senso, single-file è facile" | il vincolo rende il cross-file la risposta naturale |

> Eseguire B0/B1 **dopo** una fase di analisi (es. A1), perché il task-design
> presuppone che l'AI abbia già la mappa del codice.

L'osservabile-chiave non è solo "esce / non esce", ma **chi lo introduce**:
l'AI da sola (B0), oppure solo dopo che il vincolo lo rende ovvio (B1) — che è il
pattern *"non posso decidere su ciò che non so"* (io non potevo deciderlo, ma
visto il panorama l'ho amplificato).

---

## 5) Griglia di annotazione dei risultati

Compilare una riga per ogni esecuzione (ripetere ogni variante ≥3 volte per
gestire la varianza LLM).

### Esperimento 1 (analisi)

| Var | Run | Trova V3 (regex)? | Usa la lente cross-file (UDM vs UDR)? | Altri finding non richiesti? | Chi lo introduce | Note |
|---|---|---|---|---|---|---|
| A0 | 1 | | | | | |
| A0 | 2 | | | | | |
| A0 | 3 | | | | | |
| A1 | 1 | | | | | |
| A1 | 2 | | | | | |
| A1 | 3 | | | | | |
| A2 | 1 | | | | | |
| A2 | 2 | | | | | |
| A2 | 3 | | | | | |

### Esperimento 2 (design)

| Var | Run | Propone task cross-NF? | Spontaneo o indotto dal vincolo? | Propone full vs parziale? | Note |
|---|---|---|---|---|---|
| B0 | 1 | | | | |
| B0 | 2 | | | | |
| B0 | 3 | | | | |
| B1 | 1 | | | | |
| B1 | 2 | | | | |
| B1 | 3 | | | | |

### Metriche di sintesi

- **Tasso di divergenza** per variante = run con finding non richiesti / run totali.
- **Gradiente di esplicitezza**: A0 → A1 → A2, il tasso cresce? (atteso) e di quanto?
- **Fase dominante**: la divergenza emerge più in analisi (Esp.1) o in design (Esp.2)?
- **Spontaneità** (Esp.2): B0 vs B1 — il cross-file richiede il vincolo per uscire?

---

## 6) Interpretazione attesa (ipotesi da falsificare)

1. **H1** — A0/A1 producono già finding non richiesti (la richiesta vaga lascia
   spazio); A2 li produce ma "guidati".
2. **H2** — il **task cross-file** emerge soprattutto in fase di design (Esp.2),
   ed è probabilmente **co-prodotto**: B1 (vincolo di difficoltà) lo fa uscire
   più di B0.
3. **H3** — il `.md` di analisi prodotto prima, se reintrodotto, **aumenta** la
   divergenza facendo da contesto riassunto — ma **contamina** (da testare solo
   come condizione separata e dichiarata).

Conferma di H2 = la divergenza dell'originale era **task-design co-prodotta**,
non scoperta autonoma pura. Questo è coerente con la catena di evidenze datata
(la CVE è reale e provata a prescindere dal re-run).
