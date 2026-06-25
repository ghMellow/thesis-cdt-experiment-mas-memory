## Branch: main
**Data analisi:** 2026-06-25
**Regex trovata in:** 6 file (2 task distinti + varianti full/sol)

### Task CON regex |.+

- **task6_vuln_udr.md** — codice embedded (righe 165, 172, 194, 201) + **hint esplicito** al tester: *"Does a catch-all branch like `|.+` undermine the entire regex logic?"*
- **task6_vuln_udr_full.md** — versione full con codice sorgente completo; regex alle righe 2580, 2587, 2612, 2619
- **task6_vuln_udr_sol.md** — soluzione: cita `|.+` come vulnerabilità esplicita, spiega che equivale a non-empty check, propone fix (rimuovere il branch). Rubrica include criteri su `|.+`
- **task6_vuln_udr_full_sol.md** — identico a task6_vuln_udr_sol.md con codice completo
- **task9_vuln_cross.md** — regex nel codice embedded (riga 215); task cross-NF (PCF/AMF/UDM/UDR). Nessun hint esplicito sulla regex
- **task9_vuln_cross_sol.md** — tabella riassuntiva che cita `|.+` come finding UDR in `HandleCreateEeSubscriptions` e `HandleQueryeesubscriptions`

### Task SENZA regex

task5_vuln_pcf.md, task5_vuln_pcf_sol.md, task7_vuln_amf.md, task7_vuln_amf_full.md, task7_vuln_amf_full_sol.md, task7_vuln_amf_sol.md, task8_vuln_udm.md, task8_vuln_udm_full.md, task8_vuln_udm_full_sol.md, task8_vuln_udm_sol.md, task1_math_int.md, task1_math_int_sol.md, task2_math_real.md, task2_math_real_sol.md, task3_anomaly.md, task3_anomaly_sol.md, task4_rootcause.md, task4_rootcause_sol.md

### Note

- La forma canonica è sempre: `^(imsi-[0-9]{5,15}|nai-.+|msisdn-[0-9]{5,15}|extid-[^@]+@[^@]+|gci-.+|gli-.+|.+)$`
- task6 ha un hint esplicito guidato che punta il dito sul catch-all branch → task progettato per far trovare questa vulnerabilità
- task9 include la regex nel codice ma senza hint esplicito → finding atteso ma non telegrafato
- Nessun riferimento al CVE ID GHSA-6gxq-gpr8-xgjp nei file task (quello è in docs/)
- Origine: la regex nei task di main deriva dall'ANALISI_VULNERABILITA.md passata al modello nella sessione originale (persa), non da una riscoperta autonoma
