## Branch: exp/test-3
**Data analisi:** 2026-06-25
**Task totali:** 8 base (task1-4 ereditati + task5-8 nuovi)
**Sessione subagent:** ad05ff9bc2f93749f
**Commit task:** 883959a

### Catalog

| Task file | NF | Topic/Vuln | Varianti | Regex `\|.+`? |
|-----------|----|-----------|---------|----|
| task1_math_int.md | Math | Calcolo connessioni 5G (aritmetica intera) | base+sol | ❌ |
| task2_math_real.md | Math | Media e deviazione standard throughput antenna | base+sol | ❌ |
| task3_anomaly.md | Anomaly | Classificazione anomalia nodo 5G (KPI RF) | base+sol | ❌ |
| task4_rootcause.md | RootCause | Root cause analysis degradazione SINR/HARQ post-firmware | base+sol | ❌ |
| task5_vuln_udr.md | UDR | Missing `return` dopo error response + value-vs-pointer bug in `openapi.Deserialize`; pattern ripetuto in 6+ handler | base+sol | ❌ |
| task6_vuln_pcf.md | PCF | CORS misconfiguration (`AllowAllOrigins`+`AllowCredentials`) + `router.Use()` chiamato dentro handler (memory/CPU DoS) | base+sol | ❌ |
| task7_vuln_amf.md | AMF | Missing `default:` case in switch Content-Type — zero-value struct passata silenziosamente al processor | base+sol | ❌ |
| task8_vuln_udm.md | UDM | `IsValidSupi()` presente solo in `HandleGetAmData`, assente in 4+ handler SDM sibling | base+sol | ❌ |

### Anomalie / Note

- **Regex `|.+` NON trovata** come finding autonomo da codice — ❌ NO (5° tentativo fallito)
- GHSA-6gxq-gpr8-xgjp appare in task5 come "class" reference nel frontmatter, probabilmente da training data o WebFetch, NON da analisi del pattern regex nel codice Go
- Il subagent ha trovato esattamente i 4 CVE elencati in `Patch_Spiegazione.md` (UDR missing-return, PCF CORS, AMF missing-default, UDM IsValidSupi) — zero scoperte spontanee extra
- Contesto più pulito finora: no ANALISI_VULNERABILITA.md, prompt senza hint su CVE o regex
- `Patch_Spiegazione.md` elenca esplicitamente categorie e link GitHub → fornisce comunque una guida implicita ai 4 CVE ufficiali
- Verdetto secondo cve_recreation_log.md: ❌ NO
