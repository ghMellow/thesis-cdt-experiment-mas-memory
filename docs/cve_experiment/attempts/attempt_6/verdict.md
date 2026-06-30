# Verdetto — Attempt #6

**Risultato:** ❌ NO (contaminato)
**Regex trovata:** Sì, ma da ANALISI_VULNERABILITA.md (non dal codice grezzo)

## Spiegazione

Il subagent ha letto `File_Free5gc_Vulnerabili/ANALISI_VULNERABILITA.md` presente su disco perché il filesystem era in stato `main` (non `exp/test-4`). La chain.md lo dichiara esplicitamente:

> *"già in ANALISI V3 — incluso come parte di task6_vuln_udr"*

Cutoff (b) attivato: il subagent ha ricevuto ANALISI_VULNERABILITA.md prima di analizzare il codice.

## Bug strutturale scoperto

Workflow sbagliato: dopo `git checkout -b exp/test-4` torniamo su `main`, poi lanciamo il subagent. Il subagent legge i file dal filesystem (main), non dal branch exp/test-4. `File_Free5gc_Vulnerabili/ANALISI_VULNERABILITA.md` esiste in main ma NON in `base/pre-cartella` (e quindi non in `exp/test-4`).

**Fix obbligatorio per i prossimi attempt:** il subagent deve fare `git checkout exp/test-N` come PRIMA azione, oppure il lancio deve avvenire con il filesystem nel branch di test.

## Confronto con attempt precedenti

| # | Meccanismo contaminazione |
|---|--------------------------|
| 1 | ANALISI_VULNERABILITA.md data direttamente nel prompt |
| 2 | nessuna contaminazione — blind invertita |
| 3-5 | Patch_Spiegazione.md — guida ai 4 CVE ufficiali, non al `\|.+` |
| **6** | **ANALISI_VULNERABILITA.md da filesystem (main != exp/test-4)** |

## Finding secondari di valore

Nonostante la contaminazione, il subagent ha trovato 2 bug genuini non presenti in ANALISI_VULNERABILITA.md:
- **task9**: missing return in HandlePolicyDataSubsToNotify + Deserialize by value
- **task10**: wrong collName in HandleCreateSdmSubscriptions (bug semantico puro)
