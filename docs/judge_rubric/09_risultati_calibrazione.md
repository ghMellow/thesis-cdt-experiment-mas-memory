# 09 — Risultati: calibrazione del giudice (passi 1 e 1-bis)

> Risultati dell'esperimento impostato nel doc 08, eseguito il 2026-07-16 sui dati della run SGV-fixed del 2026-07-14 (task5–9, config 1A, 3 ripetizioni). Nessuna run nuova degli agenti: analisi dei `results/` esistenti + chiamate standalone al giudice via Ollama Cloud. Dati grezzi in `results/evaluation/judge_calibration/` (non tracciato). **Limite dichiarato**: N piccolo (12–15 ripetizioni, 5 task) — pilota, non conclusivo.

## 1. Passo 1a — Calibrazione soglia (zero chiamate LLM)

**Scoperta preliminare**: task9_vuln_cross ha `n_target_cves = 0` nel dataset CVE normalizzato → M1 lì è **indefinito** (né TP né FP), escluso dalla calibrazione. Da sistemare se si vuole includere il task cross-file nelle metriche deterministiche. Restano 12 ripetizioni (4 task).

Due definizioni di riferimento deterministico:

- **M1@any** = almeno una CVE target trovata → positivo su **12/12**: l'agente trova sempre almeno una CVE. Nessuna classe negativa → curva degenere, non usabile da sola.
- **M1-strict** = *tutte* le CVE target trovate → positivo su 9/12 (task6 ne manca 4 su 6 in tutte le rep).

| confronto | accordo a t=0.7 (attuale) | accordo massimo | plateau ottimale |
|---|---|---|---|
| vs M1@any | 0.50 (0 FP, 6 FF) | 0.92 | 0.05–0.40 |
| vs **M1-strict** | 0.75 (0 FP, 3 FF) | **1.00** | **0.45–0.65** |

**Letture:**

1. Il giudice attuale è **severo, non generoso**: zero false pass a qualunque soglia. Il rischio di generosità del doc 06 non si manifesta *con la rubrica GT-derivata* — coerente col paper, dove è la presenza della reference a tenere il giudice onesto.
2. Il `normalized_score` della rubrica traccia **M1-strict quasi perfettamente**: la rubrica misura la *copertura completa* della GT, non la detection di almeno una vulnerabilità. Le due metriche rispondono a domande diverse — da scegliere consapevolmente quale interessa.
3. La soglia 0.7 è **troppo alta di un soffio**: boccia sistematicamente task8 (0.67 in tutte e 3 le rep, con *tutte* le CVE trovate — il punto perso è su un criterio qualitativo). **Raccomandazione: 0.65** (bordo del plateau; il centro 0.55 è più robusto ma meno conservativo). Con 0.65 l'accordo con M1-strict è 12/12.
4. `config.TEXTUAL_PASS_RATIO` **non è stato cambiato**: la scelta 0.65 vs 0.55 e M1-strict vs M1@any come riferimento è una decisione di gruppo.

## 2. Passo 1b — Giudice ≠ agente (15 chiamate)

Ri-giudizio dei 15 `final_answer` con **gpt-oss:20b** (hosted): famiglia del tutto diversa da gemma, taglia paragonabile (20b vs 31b). Stessa rubrica, stesso prompt, stessa temperatura.

- Delta medio (gpt-oss − gemma): **+0.074** — il giudice esterno è *leggermente più generoso*, non più severo.
- Verdetti flippati: **2/15 a t=0.7, 1/15 a t=0.65**.
- Ordinamento per task identico: task6 basso (0.33–0.56), task8 intermedio, task5/7/9 pieni.

**Lettura**: nessun segnale forte di **self-enhancement bias** del giudice gemma su questi dati — se il bias di famiglia dominasse, gemma avrebbe dovuto sovra-premiare i report del proprio agente rispetto a un giudice terzo, e accade il contrario (gemma è il più severo dei due). Con la rubrica GT-derivata il giudizio è robusto al cambio di famiglia. Da rifare come confronto quando ci sarà la rubrica GT-free: è lì che il paper (doc 06, Appendix A.4) osserva il bias di famiglia all'opera.

## 3. Passo 1-bis — Test di ammissione C1/C2 (30 chiamate)

Protocollo del doc 07 §3 (trasposto da arXiv:2607.12885): per ogni task, un report **C1** (coerente con la GT ma riscritto) e un report **C2** (plausibile ma sbagliato: vulnerabilità trapiantata da un altro task su funzioni realmente presenti nel file, così un verificatore sintattico non lo fermerebbe). Materiali verbatim in `calibration_c1c2/` (con la nota sul caso task9, dove la rotazione letterale avrebbe prodotto un C2 vero). Giudice di sistema gemma4:31b-cloud, K=3 per report.

| task | C1 medio | C2 medio | CGP |
|---|---|---|---|
| task5_vuln_pcf | 1.00 | 0.00 | +1.00 |
| task6_vuln_udr_full | 1.00 | 0.04 | +0.96 |
| task7_vuln_amf_full | 1.00 | 0.00 | +1.00 |
| task8_vuln_udm_full | 1.00 | 0.00 | +1.00 |
| task9_vuln_cross | 1.00 | 0.22 | +0.78 |
| **complessivo** | **1.000** | **0.052** | **+0.948** |

- C2 promossi (falsi positivi del giudice): **0/15** sia a t=0.7 sia a t=0.65. C1 bocciati: 0/15.
- Varianza tra le K=3 ripetizioni quasi nulla (range massimo 0.11) — il giudizio è stabile.
- task9 C2 = 0.22: credito parziale atteso — il report cita la classe giusta (CORS, che in task9 esiste davvero) in posizione sbagliata; la rubrica lo penalizza correttamente ma non a zero.

**Lettura**: il giudice attuale **supera il test di ammissione** con margine enorme. Confronto col paper: Gemma3-27B *reference-free* accettava il 66% delle risposte sbagliate nel dominio ostico; il nostro Gemma *con rubrica GT-derivata* ne accetta lo 0%. È la conferma sperimentale, sul nostro dominio, della tesi del paper: **è la reference (qui: la rubrica GT-derivata) a tenere il giudice calibrato**. Il valore operativo di questo numero è come **baseline**: quando si proverà la rubrica GT-free (doc 05), lo stesso identico test — stessi 10 report, stesso K — misurerà quanto CGP si degrada, e quella differenza sarà *il prezzo misurato dell'uscita dalla GT* (la quantità che il doc 04 §1 chiedeva di misurare, R4).

## 4. Sintesi per la discussione di gruppo

1. **Soglia**: portare `TEXTUAL_PASS_RATIO` a **0.65** (o 0.55): a 0.7 si boccia un task con copertura CVE completa. Decidere anche il riferimento dichiarato della rubrica: copertura completa (M1-strict) o detection (M1@any).
2. **task9 senza CVE target**: aggiungere il mapping delle CVE al task cross-file nel dataset normalizzato, o dichiararlo fuori dalle metriche deterministiche.
3. **Il giudice attuale è affidabile** (CGP +0.948, robusto cross-family, zero false pass): la debolezza del sistema oggi non è il giudizio ma la sua **dipendenza dalla GT** — confermato che il lavoro va investito sulla rubrica GT-free (docs 04/05), con questo test come metro.
4. **Asset riusabili**: `scripts/judge_calibration/` (3 script) e `calibration_c1c2/` (10 report) sono il banco di prova permanente per qualunque rubrica candidata.
