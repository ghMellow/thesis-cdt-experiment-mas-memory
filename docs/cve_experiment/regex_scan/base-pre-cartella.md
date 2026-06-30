## Branch: base/pre-cartella
**Data analisi:** 2026-06-25
**Regex trovata in:** 0 task

### Task CON regex |.+

Nessuno.

### Task SENZA regex

8 file totali in docs/tasks/:
- task1_math_int.md / task1_math_int_sol.md
- task2_math_real.md / task2_math_real_sol.md
- task3_anomaly.md / task3_anomaly_sol.md — classificazione anomalia 5G (KPI radio)
- task4_rootcause.md / task4_rootcause_sol.md — root cause analysis (regressione post-firmware)

### Note

- Branch baseline ante-integrazione della cartella File_Free5gc_Vulnerabili/
- Nessun task security esiste: i task 3-4 riguardano 5G ma trattano KPI radio e analisi firmware, non validazione identificatori UE né componenti del core network
- La CVE GHSA-6gxq-gpr8-xgjp non era ancora stata introdotta/documentata in questo branch
- Utile come punto di partenza per test blind (commit 2438b71 secondo cve_recreation_log.md §6)
