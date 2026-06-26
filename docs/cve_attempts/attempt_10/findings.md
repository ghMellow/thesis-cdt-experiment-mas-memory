# Attempt #10 — Findings

## Task creati (exp/test-8, commit 23635b0 + 0fbc92c)

| Task | NF | Vulnerabilità | Regex |.+? |
|------|----|----|--------|
| task5_vuln_amf | AMF | HTTPUEContextTransfer switch senza default | ❌ |
| task6_vuln_pcf | PCF | CORS AllowAllOrigins+AllowCredentials + router.Use() in handler | ❌ |
| task7_vuln_udr | UDR | **Regex `\|.+` bypass** (GHSA-6gxq-gpr8-xgjp) | ✅ **SÌ — task primario** |

## Regex |.+ trovata?

**SÌ — task7_vuln_udr, task primario dedicato.**

## Meccanismo (dalla chain.md)

**Diverso da attempt 9**: l'agente ha letto i .go in ordine (AMF → PCF → UDM → UDR) PRIMA di Patch_Spiegazione.md.

Citazione dalla chain:
> *"L'ultimo branch `|.+` è immediatamente riconoscibile come il CVE GHSA-6gxq-gpr8-xgjp."*

Questo è **training data pattern recognition**: il modello ha memorizzato la CVE free5GC (pubblica su GitHub Advisory Database) e la riconosce nel codice al primo sguardo. Non è una discovery guidata da Patch_Spiegazione.md come in attempt 9.

## Due meccanismi ora documentati

| Attempt | Ordine lettura | Meccanismo | Regex in task? |
|---------|---------------|------------|----------------|
| 9 | Patch_Spiegazione.md PRIMA | Focus su UDR → regex trovata "di passaggio" | secondario in task6 |
| 10 | .go PRIMA → Patch_Spiegazione.md dopo | Training data recognition immediata | task primario task7 |

## Implicazione per la ricerca

La "singolarità" originale potrebbe essere stato uno dei due meccanismi (o entrambi). Il modello Claude ha GHSA-6gxq-gpr8-xgjp nel training data — riconosce il pattern `|.+` in questo specifico file free5GC senza bisogno di guida.
