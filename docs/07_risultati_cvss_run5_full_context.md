# Esperimento 2b — Run 5: contesto pieno (varianti `_full`) — il rubric accuracy crolla su 2 task su 4

> Documento di condivisione per il team. Prima run con **contesto pieno**: invece degli estratti curati, task6/7/8 usano il file sorgente completo (`_full`); task5 era già di fatto full (l'estratto copre l'intero file PCF); task9 resta parziale per costruzione (confronto cross-NF su estratti di 4 file). Obiettivo: verificare se dare più contesto migliora la review — risultato **negativo e specifico**: il Blocco A crolla su task6/7, resta identico su task8/9. 30 run totali (5 task × 1A/1B × 3 rep).

**Data run:** 2026-07-11 · **Autore:** Nicolò (con supporto AI) · **Run precedente:** [run 4](06_risultati_cvss_run4.md) (stessi task su estratto, 30 run) · **Nota sui dati:** `results/<task>/<exp>/agent/` contiene *solo* questa run — le cartelle `agent_8m` e `agent_run4` (run precedenti, stessi task5/task9 senza variante `_full`) sono state escluse dall'analisi qui sotto, anche se compaiono nei report aggregati generati da `main.py` (che scansiona tutte le cartelle-ruolo).

---

## 0. Cosa cambia rispetto alla run 4

1. **Task**: `task6_vuln_udr_full`, `task7_vuln_amf_full`, `task8_vuln_udm_full` al posto delle varianti excerpt; `task5_vuln_pcf` e `task9_vuln_cross` invariati (nessuna variante full disponibile/sensata per loro — vedi intro).
2. **GT più ampia per task6**: le CVE candidate passano da 3 a **6** (le 3 escluse dall'estratto — `in_task_excerpt: false` — ora rientrano: CVE-40245, 40249, 40343).
3. **Setup invariato**: agente/giudice/prompt/hint/rivalutazione ufficiale identici a run 4. Stesso caveat di run 4 §0.4: `agent_1A`, `agent_1B` e `judge` sono tutti `gemma4:31b-cloud`.

---

## 1. Risultati d'insieme

### Blocco A — rubrica testuale (30 run)

| task | correct/6 | avg norm | dettaglio |
|---|---|---|---|
| task5_vuln_pcf | 6/6 | 0.944 | invariato rispetto a run 4 |
| **task6_vuln_udr_full** | **0/6** | **0.481** | tutti wrong, 3 tentativi esauriti in ogni run |
| **task7_vuln_amf_full** | **0/6** | **0.519** | tutti wrong, 3 tentativi esauriti in ogni run |
| task8_vuln_udm_full | 6/6 | 0.778 | invariato rispetto a run 4 |
| task9_vuln_cross | 6/6 | 1.000 | invariato (task non toccato da questa run) |
| **Totale** | **18/30 (60%)** | **0.745** | contro 29/30 (96.7%) di run 4 |

**Non è "il contesto pieno fa sempre peggio": è specifico a 2 rubriche su 4.** task8_full (858 righe) e task5 (già full) restano a punteggio pieno; task9 non tocca il contesto. Solo task6_full (2937 righe) e task7_full (545 righe — non enorme) collassano, e lo fanno **in modo deterministico**, non rumoroso: su task6_full il sub-score `missing_return_score` è **0.0 in tutti e 6 i tentativi** (12 chiamate contando i 2 retry ciascuno), mai un'eccezione.

### Blocco B — CVSS (19 finding abbinati su 8 CVE candidate possibili — 6 per task6 + 1 per task7 + 1 per task8; task5/9 come in run 4)

| n matched | coerenza Δ | Δ vettore vs B | banda ricalc. vs B | banda dichiarato vs B (diagn.) | dist. impatto | unmatched totali | missed CVEs |
|---|---|---|---|---|---|---|---|
| 19 | 1.21 (σ 0.87) | 2.24 | 1.00/3 | 0.89/3 | 0.46 | **83** | 35 |

Il pattern F17 (dichiarato < ricalcolato) si conferma: 16/19 casi, scarto medio **−1.21**. Ma il dato che salta all'occhio è **unmatched**: 83 su 30 run, quasi il triplo dei 28 di run 4 a parità di ripetizioni — il modello riporta molti più candidati per file, la maggior parte senza CVE corrispondente (mai penalizzati, ma segnale di maggiore "rumore" col contesto pieno).

---

## 2. Per-task: cosa succede col contesto pieno

**task6_vuln_udr_full — il caso peggiore, e istruttivo.** Su tutti i 6 tentativi il giudice assegna `missing_return_score: 0.0` — il modello non identifica mai il bug specifico della rubrica (return mancante dopo `c.String(404,...)` in 3 handler). Trova sempre la vulnerabilità regex (`regex_validation_score: 3.0`, perfetto) e un impatto generico (1–2/3), ma il bug di controllo di flusso — quello che richiede di seguire riga per riga cosa succede *dopo* la risposta di errore in decine di handler — si perde. Coerente col Blocco B: delle 6 CVE candidate (erano 3 in run 4), **solo una viene mai abbinata** (CVE-40249, e solo in 4 run su 6) — le altre 5, incluse le 3 nuove disponibili con la variante full, non vengono mai matchate. Il contesto pieno non ha "recuperato" le CVE storicamente fuori estratto: ha *peggiorato* anche il matching sulle CVE che prima funzionavano sempre (F14, run 3: 12/12 match su CVE-40246 con l'estratto; qui 4/6 su una CVE diversa).

**task7_vuln_amf_full — stesso pattern, file non enorme (545 righe).** Il giudice segnala sistematicamente due mancanze specifiche: lo `switch` su Content-Type senza `default` case, e l'uso inconsistente di `c.Set(...)` tra handler diversi. Sono bug che richiedono di **confrontare più handler tra loro** nello stesso file — con l'estratto (282 righe, presumibilmente già ritagliato sugli handler rilevanti) il confronto era più diretto; nel file intero, con più handler "distraenti", il confronto si perde. Il caso peggiore è 1B/rep2: normalized 0.0, punteggio nullo su tutte e 3 le categorie.

**task8_vuln_udm_full — nessun cambiamento.** Stesso punteggio di run 4 (0.778), stessa CVE unica abbinata in tutti i 6 run, coerenza interna simile (0.65 vs 0.45), bias di sottostima dell'impatto confermato (Δ vettore vs B 3.47, il peggiore di questa run — F18 si conferma anche col contesto pieno). La singola CVE di questo task ha un solo handler_function target diretto, quindi non c'è "confronto tra handler" da perdere.

**task5_vuln_pcf e task9_vuln_cross — nessun cambiamento**, come atteso (non toccati dal cambio di contesto).

---

## 3. Findings (continuano la numerazione di [run 4](06_risultati_cvss_run4.md))

**F21 — Il contesto pieno non è un miglioramento generico: peggiora drasticamente il Blocco A su rubriche che richiedono analisi di controllo di flusso o confronto cross-handler, non lo tocca su rubriche con un bersaglio singolo.** task6/7_full crollano a 0/6 (missing_return_score sempre 0.0, non un caso isolato); task8_full e task9 restano identici. La differenza non è la dimensione del file (task7_full è più piccolo di task8_full) ma la **forma della rubrica**: bug che richiedono di seguire il flusso attraverso più handler si diluiscono quando il modello deve scansionare l'intero file invece di un estratto già mirato. **Implicazione diretta per l'esperimento 3 (SonarQube+LLM):** se l'idea è dare più contesto via analisi statica, questo risultato suggerisce che il contesto va reso *mirato* (segnalare dove guardare), non semplicemente *più ampio* (dare tutto il file).

**F22 — Il matching CVSS su task6 peggiora invece di migliorare, nonostante 6 CVE candidate invece di 3.** Con l'estratto (run 1–4) il modello abbinava sempre la stessa CVE in ogni run (F14, comportamento di ferro). Con il file intero abbina una CVE diversa (CVE-40249, una di quelle prima escluse) solo in 4 run su 6, e non ne trova mai altre. Il contesto pieno non "sblocca" le CVE storicamente irraggiungibili — le rende semplicemente più difficili da trovare tutte, perché il bug alla base (missing return) smette di essere identificato affidabilmente (conseguenza diretta di F21).

**F23 — F9/F18 (task8, impatto sottostimato) è indifferente al contesto: stesso bias, stessa entità.** Δ vettore vs B 3.47 (era 2.87 sull'estratto) — leggermente peggiore, non migliore. Conferma che il problema è nella percezione dell'impatto (VC), non nella quantità di codice disponibile: dare più contesto non corregge un bias di interpretazione della severità.

**F24 — Col contesto pieno il modello diventa più verboso, non più preciso: quasi 3× i finding senza CVE corrispondente.** 83 unmatched su 30 run (run 4: 28 su 30 run). Mai penalizzato per design, ma è un segnale di "rumore" in aumento — più segnalazioni generiche, non necessariamente più CVE reali intercettate. Coerente con l'intuizione di Andrea in call 11: più contesto senza guida rischia di aumentare il carico di validazione umana invece di ridurlo.

---

## 4. Che cosa dire al team

**Il contesto pieno, testato nella sua forma più semplice (tutto il file, nessuna guida su dove guardare), non ha funzionato — anzi ha rotto due task su quattro.** Non è un fallimento generico dell'idea "più contesto aiuta": è la controprova diretta che serve un contesto *mirato*, non solo *ampio* — esattamente la direzione dell'esperimento 3 (SonarQube segnala dove guardare, l'LLM guarda lì). Se SonarQube indica la riga/handler sospetto invece di lasciare che il modello scansioni tutto da solo, il problema di F21 (diluizione dell'attenzione su bug di controllo di flusso) potrebbe non presentarsi.

Nota di cautela: il crollo è "solo" 2 task su 4, e uno di questi (task6) ha il file più grande in assoluto (2937 righe, ~9× l'estratto) — non si può escludere un effetto combinato dimensione+forma-del-bug con questi soli 4 campioni per task. Prima di trarre conclusioni definitive per l'articolo servirebbero più task con rubriche "cross-handler" per isolare la variabile.

**Punti aperti** (ripresi da run 4, nessuno risolto da questa run):
1. B vs BT come riferimento principale;
2. calibrazione bande;
3. matching multi-CVE (F14/F22: ora anche instabile col contesto pieno);
4. interpolazione FIRST vettore↔vettore (materiale Mariano);
5. differenziare 1A/1B in config (ancora stesso modello ovunque);
6. CVE-2026-47780 fuori perimetro (nessun task associato).

**Nuovo, dalla run 4**: score dichiarato ormai trattato come diagnostica (F17); questa run lo conferma (16/19, scarto −1.21).

---

## 5. Come riprodurre

```bash
poetry run python main.py --experiment all \
  --task task5_vuln_pcf --task task6_vuln_udr_full --task task7_vuln_amf_full \
  --task task8_vuln_udm_full --task task9_vuln_cross
```

Stesso prompt a 11 metriche e hint NF di run 4. Per isolare i dati di *questa* run nei report — dato che `_write_evaluation_reports` aggrega tutte le cartelle-ruolo di un task — filtrare sulla cartella `agent/` escludendo `agent_8m/` e `agent_run4/` (presenti solo su task5/task9, che non hanno variante `_full` dedicata).
