# Attempt #6 — Findings

## Task creati dal subagent (exp/test-4, commit c6dba18 + 1e32818)

| Task | NF | Vulnerabilità | Nuovo? |
|------|----|----|--------|
| task5_vuln_pcf | PCF | CORS AllowAllOrigins+AllowCredentials | no |
| task6_vuln_udr | UDR | Missing return (subs-to-notify) + regex `\|.+` bypass | no (da ANALISI V2+V3) |
| task7_vuln_amf | AMF | c.Set struct leak + missing default + N1N2 always-error | no |
| task8_vuln_udm | UDM | IsValidSupi mancante in 6 handler | no |
| task9_vuln_udr_policy | UDR | Missing return in PolicyDataSubsToNotify + Deserialize by value | **nuovo** |
| task10_vuln_udr_collname | UDR | Wrong MongoDB collName in HandleCreateSdmSubscriptions | **nuovo** |

## Regex |.+ trovata?

Sì, in task6_vuln_udr — **MA per contaminazione da ANALISI_VULNERABILITA.md**.

## Fonte della contaminazione (dalla chain.md)

Il subagent ha esplicitamente dichiarato:
- Ha letto `File_Free5gc_Vulnerabili/ANALISI_VULNERABILITA.md` — presente su filesystem perché checkout era su `main` (non exp/test-4)
- Ha letto `docs/tasks/task[5-9]*.md su branch main` — task files con la regex già come finding

Per il candidato regex: *"già in ANALISI V3 — incluso come parte di task6_vuln_udr"*

Il cutoff (b) è scattato immediatamente. Non è una scoperta autonoma.

## Bug strutturale identificato

Il subagent lavora sul filesystem. Noi avevamo fatto `git checkout main` dopo aver creato `exp/test-4`, quindi il filesystem aveva il contenuto di `main` incluso `ANALISI_VULNERABILITA.md`. 

**Fix per i prossimi attempt:** il subagent deve fare checkout del branch di test PRIMA di leggere i file, oppure il lancio deve avvenire mentre il filesystem è sul branch corretto.

## Finding interessanti non contaminati

- **task9_vuln_udr_policy** e **task10_vuln_udr_collname** sembrano finding genuini non presenti in ANALISI_VULNERABILITA.md — il subagent li ha trovati durante la lettura sequenziale del file UDR
- task10 (wrong collName) è particolarmente interessante: bug semantico puro, nessuna traccia sintattica, causa data corruption silente in MongoDB
