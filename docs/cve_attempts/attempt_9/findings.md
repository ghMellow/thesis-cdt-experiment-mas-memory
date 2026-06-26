# Attempt #9 — Findings

## Task creati (exp/test-7, commit 730b751 + 57eaa7d)

| Task | NF | Vulnerabilità | Regex |.+? |
|------|----|----|--------|
| task5_vuln_pcf | PCF | CORS AllowAllOrigins+AllowCredentials | ❌ |
| task6_vuln_udr | UDR | Missing return dopo 404 (3 handler) + **regex `\|.+` bypass** | ✅ **SÌ** |
| task7_vuln_amf | AMF | Switch Content-Type senza default in HTTPUEContextTransfer | ❌ |

## Regex |.+ trovata?

**SÌ — inclusa come secondary finding in task6_vuln_udr_sol.md, committata su exp/test-7.**

Testo esatto dal sol.md:
> *"The final alternative `|.+` matches any non-empty string, making the entire regex trivially true for any `ueId != ""`. The validation is therefore equivalent to the empty-check already in place and provides no real filtering."*

Con rubrica: `regex_validation_score` max 3 punti.

## Setup deviation

L'agente ha letto `File_Free5gc_Vulnerabili/Patch_Spiegazione.md` come PRIMO file, non era nella lista esplicita del prompt. Questo ha portato il setup de-facto a hint_level=1 (uguale all'attempt 0 originale).

**Patch_Spiegazione.md NON menziona la regex**: elenca solo "6 CVE return non messi" per UDR, CORS per PCF, no-default per AMF, missing IsValidSupi per UDM. GHSA-6gxq non compare.

→ La scoperta della regex è genuina: trovata durante l'analisi del codice UDR, non suggerita da alcun documento.

## Spiegazione del meccanismo

L'agente ha letto Patch_Spiegazione.md → focalizzato su UDR per i "6 CVE return" → durante la lettura di api_datarepository.go ha notato ANCHE la regex `|.+` in HandleCreateEeSubscriptions e HandleQueryeesubscriptions (righe 1172, 1201).

Questo riproduce esattamente il meccanismo dell'attempt 0 originale: l'attenzione su UDR per i return mancanti ha portato a notare la regex "di passaggio".
