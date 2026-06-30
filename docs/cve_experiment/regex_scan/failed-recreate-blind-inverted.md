## Branch: failed/recreate-blind-inverted
**Data analisi:** 2026-06-25
**Regex trovata in:** 0 task

### Task CON regex |.+

Nessuno.

### Task SENZA regex

I 16 file in docs/tasks/ non contengono: la stringa letterale `|.+`, il GHSA GHSA-6gxq-gpr8-xgjp, i termini `ueId`/`IsValidUeId`, né il pattern completo della regex.

Task presenti: task5 (PCF/CORS), task6 (AMF/missing-default), task7 (UDM/missing-SUPI-validator), task8 (UDR/missing-return) + sol per ognuno, + task1-4 math/anomaly/rootcause.

### Note

- Il task UDR presente (task8) riguarda la **CVE missing-return** (GHSA-wrwh...), non la regex ueId (GHSA-6gxq)
- Questo è il branch dei tentativi "blind" — la regex non è stata inclusa come task proprio perché nei run alla cieca il modello non l'ha trovata
- Il run davvero cieco (sessione ebcd1147): il modello ha letto SOLO i .go, ha citato la riga della regex ma l'ha interpretata come *presenza* di validazione — il contrario del bug. Quindi zero task sulla regex
- Verdetto secondo cve_recreation_log.md: ❌ NO riscoperta (cieco fallito e invertito)
