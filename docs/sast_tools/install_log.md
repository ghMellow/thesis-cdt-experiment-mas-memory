# SAST tools — install log (gosec / semgrep)

> Ledger per la skill `sast-tools-lifecycle`. Non cancellare: resta lo storico anche dopo la rimozione.

## Stato: NON ANCORA INSTALLATO

Motivo previsto: check offline di copertura sulle 9 CVE target (`File_Free5gc_Vulnerabili/cve_metrics_normalized.json`), come alternativa a SonarQube — vedi `docs/status.md` §todo "Rivalutare l'enumeratore di completezza".

Verificato 2026-07-21: nessuna delle formule necessarie è presente sul sistema (`go`, `python@3.14`, `gosec`, `semgrep` assenti da `brew list --formula`) — installazione futura sarebbe interamente rimovibile senza impatto su altri progetti/tool esistenti.

Stima pre-installazione (da verificare con misura reale all'install): ~1-1.3 GB totali, dominati da `go` (~500-600 MB) e dalle dipendenze di `semgrep` (`python@3.14` + 11 altre formule, ~300-500 MB).

---

<!-- Alla prima installazione, la skill aggiunge qui una entry con:
data, formule installate (dirette vs transitive), peso per formula (du -sh reale),
comando di rimozione esatto, stato ATTIVO. -->
