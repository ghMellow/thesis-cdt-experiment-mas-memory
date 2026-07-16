# Materiali di calibrazione C1/C2

Materiali per il **Passo 1-bis** (test di ammissione C1/C2) descritto in
`docs/judge_rubric/08_esperimento_calibrazione_giudice.md` §4. Ogni task ha un report C1
(corretto, riscritto senza copiare GT/rubrica) e un report C2 (plausibile ma sbagliato, vulnerabilità
trapiantata da un altro task) — salvati verbatim prima di essere passati al giudice, come richiesto
dal protocollo.

## Tabella task → vulnerabilità

| Task | Vuln vera (C1) | Vuln trapiantata in C2 (da dove) | Funzioni reali usate in C2 |
|---|---|---|---|
| task5_vuln_pcf | CORS: `AllowAllOrigins` + `AllowCredentials` in `setCorsHeader` | Missing-return dopo 404 + regex `\|.+` inefficace (da task6/UDR) | `HTTPOAMGetAmPolicy`, `setCorsHeader` |
| task6_vuln_udr_full | Missing `return` dopo 404 (3 handler subs-to-notify) + regex `\|.+` inefficace | Missing `default` in switch Content-Type + struct passato a `c.Set` invece di stringa (da task7/AMF) | `HandleAmfContext3gpp`, `HandleCreateAmfContext3gpp`, `HandleAmfContextNon3gpp`, `HandleCreateAmfContextNon3gpp` |
| task7_vuln_amf_full | Missing `default` in `HTTPUEContextTransfer` + struct passato a `c.Set` in 5 handler | Validazione SUPI mancante (da task8/UDM), trapiantata su `ueContextId` | `HTTPCreateUEContext`, `HTTPEBIAssignment`, `HTTPReleaseUEContext`, `HTTPAMFStatusChangeSubscribeModify` (contrasto) |
| task8_vuln_udm_full | Validazione SUPI mancante in 6 handler (`HandleGetSmfSelectData` e altri) | CORS `AllowAllOrigins`+`AllowCredentials` (da task5/PCF) | `getSubscriberDataManagementRoutes` |
| task9_vuln_cross | Inconsistenza cross-file validazione UDM/UDR + 5 finding per-file (CORS PCF, default AMF, c.Set AMF, missing-return UDR, regex UDR) | CORS `AllowAllOrigins`+`AllowCredentials` (da task5/PCF), attribuito però ad AMF/UDR invece che a PCF per non sovrapporsi ai finding veri | `HTTPAMFStatusChangeSubscribeModify`, `HandleCreateEeSubscriptions`, `HandleGetAmData` (contrasto) |

**Nota sulla rotazione task9**: la rotazione originale (task9→usa la vuln di task5) avrebbe fatto
coincidere il C2 con un finding vero di task9 stesso, dato che il file 1 di task9 è proprio il PCF con
lo stesso bug CORS. Per preservare l'intento del test (C2 non deve mai contenere una vulnerabilità
vera del task corrente), la vulnerabilità CORS è stata trapiantata su funzioni reali di AMF/UDR
citate nello scenario di task9, non su `setCorsHeader`/PCF.

## Formato

Ogni file: `{"answer": "...", "reasoning": "...", "confidence": 0.0-1.0}`, stesso formato di
`repetitions[].final_answer` nei risultati salvati (es. `results/task5_vuln_pcf/1A/agent/hosted_gemma4_31b_cloud.json`).

- Data: 2026-07-16
- Generato da subagent (sonnet), verificato dall'orchestratore
