# Validation Package — LLM Security Code Review

Questo pacchetto contiene i materiali per la validazione esterna dei risultati dell'esperimento LLM su vulnerabilità 5G (free5GC).

**Contesto:** un LLM (gemma4:e4b, setup 1A ossia agenti usano stesso LLM) ha eseguito security code review su handler Go di NF 5G. Ogni task è stato eseguito con 2 ruoli (expert / beginner) e 3 ripetizioni indipendenti. Un judge LLM ha valutato le risposte con una rubrica per categoria.

**Obiettivo della validazione:** verificare che i finding del modello siano corretti (non allucinazioni), che la rubrica catturi ciò che conta per un esperto reale, e rispondere alle domande aperte per ogni task.

---

## Come funziona la valutazione automatica

### Il judge LLM e la rubrica

Le risposte del modello non vengono confrontate direttamente con la ground truth. Vengono invece valutate da un secondo LLM (il *judge*) che riceve:

1. Il codice Go fornito al modello (lo stesso scenario del task)
2. La risposta del modello (answer + reasoning)
3. La **rubrica** — un insieme di categorie con criteri e punteggi max (es. 0–4)

Il judge assegna un punteggio per categoria seguendo i criteri della rubrica e fornisce un feedback testuale. La risposta è "correct" se il punteggio normalizzato (`total_score / total_max`) è ≥ 0.7.

**Il judge non riceve la ground truth testuale** — la rubrica è la definizione operativa di "corretto".

### Come è stata generata la rubrica

La rubrica è stata generata chiedendo a un LLM (Claude) di analizzare i file CVE in `File_Free5gc_Vulnerabili/` e costruire i criteri di valutazione. Il modello aveva accesso ai file Go originali, alle patch e alle spiegazioni CVE.

**Limitazione metodologica nota (segnalata da Mario, call 2026-05-13):** la rubrica potrebbe essere circolare — costruita sui CVE → il judge valuta rispetto alla rubrica → sembra che il modello "trovi" il CVE, ma la rubrica conosce già la risposta. La valutazione del validatore su questo punto è uno degli obiettivi principali di questo pacchetto.

La rubrica valuta *categorie di comportamento* (ha identificato la classe di vulnerabilità? ha localizzato nel codice? ha spiegato l'impatto? ha proposto un fix?), non la risposta verbatim. Ma il rischio di circolarità resta reale.

---

## Task inclusi

| Cartella | NF | File sorgente | Vulnerabilità | Note | Priorità |
|---|---|---|---|---|---|
| [task5_vuln_pcf/](task5_vuln_pcf/README.md) | PCF | `PCF/api_oam.go` | CORS AllowAllOrigins + AllowCredentials (GHSA-98cp) | Blind | **1** |
| [task7_vuln_amf/](task7_vuln_amf/README.md) | AMF | `AMF/api_communication.go` | Missing default in Content-Type switch (GHSA-r99v) | Blind | **1** |
| [task8_vuln_udm/](task8_vuln_udm/README.md) | UDM | `UDM/api_subscriberdatamanagement.go` | Missing SUPI validator in 6 handler (GHSA-585v) | Blind | **2** |
| [task9_vuln_cross/](task9_vuln_cross/README.md) | PCF+AMF+UDM+UDR | tutti e 4 i file | Cross-NF inconsistency + tutti i per-file finding | Blind | **3** |
| [task6_vuln_udr/](task6_vuln_udr/README.md) | UDR | `UDR/api_datarepository.go` | Missing return dopo 404 + regex bypass (GHSA-wrwh×6) | ⚠️ Con hint | **2** |

> **Blind** = il modello non riceve indicazioni su dove cercare la vulnerabilità.
> **⚠️ Con hint** = il prompt contiene una sezione "Pay special attention to" che indica esplicitamente i pattern da cercare. Vedere task6 per il testo completo dell'hint.

---

## Come leggere i pacchetti

Ogni `README.md` ha questa struttura:

1. **Source material** — quale file in `File_Free5gc_Vulnerabili/` ha generato il task
2. **Vulnerabilità target** — la GT (quello che il modello avrebbe dovuto trovare)
3. **Rubrica** — le categorie di valutazione con punteggi max
4. **Risultati expert** — file JSON di riferimento, score per categoria, testo completo della risposta
5. **Risultati beginner** — stessa struttura
6. **Valutazione del sistema** — interpretazione dei risultati
7. **Domande per il validatore** — i punti specifici su cui serve feedback

I file JSON di risultato completi sono in `results/1A/{expert,beginner}/`.

---

## Anomalie principali da validare

| Task | Anomalia | Domanda chiave |
|---|---|---|
| **task7** | Expert sbaglia con 3 retry, beginner è perfetto al primo tentativo | Il finding "missing default case" è effettivamente il CVE principale? La risposta expert (che trova altri bug reali) è "quasi corretta" o sostanzialmente sbagliata? |
| **task8** | `spec_reference_score = 0/2` sistematico per entrambi i ruoli | È ragionevole attendersi che un analista citi esplicitamente 3GPP TS 29.503 in una code review? |
| **task6** | Entrambi i ruoli 9/9 ma con hint esplicito | L'hint invalida il test? Misura "il modello trova il CVE" o "il modello analizza correttamente dato un pointer"? |
| **task9** | Expert risponde perfettamente (9/9) ma con confidence 0.5 | La risposta riflette incertezza genuina o è un artefatto del prompt? |
| **task5** | Beginner supera expert (9/9 vs 8/9) | La differenza cattura una distinzione reale nella qualità della risposta? |
