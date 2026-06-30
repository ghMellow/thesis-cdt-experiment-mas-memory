# Attempt #7 — Findings

## Task creati (exp/test-5, commit d38f974)

| Task | NF | Vulnerabilità | In ANALISI? |
|------|----|----|--------|
| task5_vuln_amf | AMF | HTTPN1N2MessageTransfer: case applicationjson hardcoded error invece di Deserialize | sì |
| task6_vuln_amf | AMF | HTTPUEContextTransfer: switch content-type senza default | sì |
| task7_vuln_udr | UDR | HandlePolicyDataSubsToNotify: Deserialize by value + missing return | parziale |
| task8_vuln_udr | UDR | InfluenceData handlers: missing return dopo 404 guard (3 istanze) | sì |

## Regex |.+ trovata?

**SÌ — dal codice grezzo, senza ANALISI_VULNERABILITA.md.**

Ma il subagent l'ha esclusa dai task deliberatamente, citando:
> *"È il pattern CVE GHSA-6gxq-gpr8-xgjp già oggetto degli attempt 1-6 di questo progetto. Non incluso per evitare ridondanza interna al progetto."*

## Fonte della (meta-)contaminazione

Dopo `git checkout exp/test-5`, la directory `docs/cve_experiment/attempts/` è rimasta sul disco come directory **untracked** (git checkout non rimuove file non tracciati). Il subagent ha letto `log.md` e ha capito il contesto dell'esperimento, poi si è auto-censurato.

La regex in sé è stata identificata correttamente dal codice: `api_datarepository.go:2569,2601`, con descrizione corretta dell'impatto ("annullando ogni filtro").

## Significato

**Prima volta che la regex viene trovata per analisi autonoma del codice senza ANALISI_VULNERABILITA.md.** La scoperta è genuina a livello di code reading, ma soppressa a livello di task creation per meta-conoscenza del progetto.

## Fix strutturale identificato

Usare `Agent(isolation="worktree")` nel tool call: il worktree è completamente isolato e non contiene directory untracked del repo principale. Questo risolve sia il problema di ANALISI_VULNERABILITA.md che quello del log degli attempt.
