# 00 — Matching CVE↔handler quando una CVE copre più funzioni (caso UDM) [sessione: 2026-08-02]

> Cartella nuova, aperta su richiesta dell'utente per tracciare l'evoluzione di questo tema nel tempo. Stato ad oggi: **discussione chiusa per ora** (decisione: lasciare il codice invariato), riaperta solo se il team decide diversamente o se emergono altri task multi-handler.
>
> Versione discorsiva, pensata per farsi un'idea della discussione e del perché della conclusione senza dover ricostruire i dettagli tecnici: [01_discussione_narrativa_2026-08-02.md](01_discussione_narrativa_2026-08-02.md).

## Il meccanismo di matching (invariato, non in discussione)

Il matching finding↔CVE è deterministico, per nome di funzione (`utils/cvss_eval.py:156-175`, `_match_finding`): substring match tra il campo `function` dichiarato dall'agente e la lista `handler_functions` della CVE candidata nella ground truth. Nessuna interpretazione semantica avviene a runtime — l'unica "intelligenza" nel capire che due funzioni condividono la stessa vulnerabilità è già stata messa a mano nella GT, in anticipo, tramite quella lista.

## Il problema misurato

`CVE-2026-42459` (UDM) è mappata su **6 handler gemelli** (`HandleGetSmfSelectData`, `HandleGetNssai`, `HandleGetSmData`, `HandleGetTraceData`, `HandleGetUeContextInSmfData`, `HandleGetSupi` — stesso bug, `validator.IsValidSupi()` mancante, copiato-incollato). Il loop di valutazione (`utils/cvss_eval.py:294-309`) consuma l'intera CVE al primo finding che nomina uno qualsiasi di questi handler; i finding successivi sugli altri 5 handler, per costruzione della lista sopra corretti, non trovano più candidati liberi e finiscono in `unmatched` → contati come FP.

Impatto misurato riusando i run esistenti (nessun nuovo run necessario): **15 dei 34 FP di UDM `_full`** (e tutti i 15 FP di UDM excerpt) sono questo artefatto, non rumore reale. Zero effetto su AMF/UDR/PCF (nessuna altra CVE nel dataset condivide handler tra loro).

## Le due opzioni valutate (non implementate)

**Opzione A — slot per handler.** Ogni CVE con N handler diventa N candidati consumabili indipendenti. TP passa da "CVE trovata sì/no" a "quante istanze note ho trovato" (UDM: TP 3→18, entrambe le condizioni). Ridefinisce TP/recall — tocca tutte le tabelle già pubblicate nel doc `sgv_protocol/11`.

**Opzione B — bucket "duplicato".** I finding sugli handler gemelli di una CVE già matchata non contano né come TP né come FP, escono solo dal denominatore FP (UDM: FP 34→19, TP invariato a 3). Non tocca nessuna definizione né numero già pubblicato.

**Perché la scelta non è urgente**: nessuna delle due cambia la conclusione sostanziale del test hint/no-hint su UDM (identica in entrambi i casi, con o senza fix — vedi `sgv_protocol/11_sast_hint_noise_test_2026-07-21.md`). Cambia solo quanto "rumoroso" appare il sistema in assoluto sui file `_full`.

## La provenienza di `handler_functions` (perché non c'è un'"intenzione originale" da rispettare)

Verificato confrontando i dati ricevuti in fase 2 (`File_Free5gc_Vulnerabili/cve_metrics (1).json`, campi: solo `id`/`url`/`network_function`/`root_cause`/`cvss`) con la versione normalizzata (`cve_metrics_normalized.json`): il campo `handler_functions` **non esiste nel dato grezzo ricevuto**, per nessuna CVE. È stato aggiunto interamente da Claude.

Per CVE-2026-42459 nello specifico, i 6 handler comparivano già nella rubrica `docs/tasks/task8_vuln_udm_sol.md`, scritta da Claude il 2026-06-15 (sessione `32b9e5ff`) leggendo il codice sorgente UDM — **prima** della query alla GitHub Advisory API del 2026-07-08 citata in `_meta.nota_matching` del normalizzato. Non è quindi accertato se i 6 handler vengano da una verifica indipendente sull'advisory ufficiale `GHSA-585v-hcgf-jhfr` o siano stati semplicemente riportati dalla rubrica già esistente. Dettaglio in `cve_metrics_normalized.json` → `_meta.nota_provenienza_handler_functions`.

Conseguenza pratica: la scelta A vs B non è "rispettare vs tradire l'intenzione del relatore" — è una decisione di design nostra su un artefatto che abbiamo costruito noi, quindi si può decidere con calma.

## Decisione (2026-08-02)

Lasciare il matching invariato. Motivi: (1) non cambia la conclusione già riportata su UDM; (2) non c'è un vincolo esterno da rispettare; (3) la roadmap verso una rubrica GT-free sposta comunque il peso della valutazione sul giudice qualitativo (che già gestisce la sfumatura "quante istanze trovate" via soglia di rubrica, es. "almeno 3 su 6" in `task8_vuln_udm_sol.md`), rendendo il matching deterministico meno centrale in futuro.

Voce di tracking aperta in `docs/status.md` (checklist principale). Se il team la riprende, i numeri e le due opzioni sono già pronti qui sopra — non serve ririfare l'analisi.

## Riferimenti

- Codice: `utils/cvss_eval.py:140-175` (candidati e matching), `utils/cvss_eval.py:274-345` (loop di valutazione), `utils/evaluation_utils.py` (definizioni TP/FP/matched/unmatched nei report)
- Dati: `File_Free5gc_Vulnerabili/cve_metrics_normalized.json` (`_meta.nota_matching`, `_meta.nota_provenienza_handler_functions`), `File_Free5gc_Vulnerabili/cve_metrics (1).json` (dato grezzo fase 2, confrontato)
- Task: `docs/tasks/task8_vuln_udm_sol.md` (rubrica con soglia "almeno 3 su 6")
- Esperimento collegato: `docs/sgv_protocol/11_sast_hint_noise_test_2026-07-21.md` (dove l'artefatto è stato notato per la prima volta durante il conteggio dei FP)
- Apertura originale del tema (mai chiusa fino ad oggi): `DEVLOG.md`, entry con "aperture per il gruppo: (1) contare i finding sugli handler gemelli come duplicati o come match multipli della stessa CVE"
