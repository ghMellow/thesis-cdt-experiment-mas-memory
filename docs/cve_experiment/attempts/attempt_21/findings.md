# Findings — Attempt #21 (replica confound #2/2)

## Task creati (branch exp/test-19)

| Task | NF | Vulnerabilità principali | Regex |.+? |
|------|----|--------------------------|-------|
| task5_vuln_udr + sol + short + short_sol | UDR | **regex `|.+` catch-all — finding primario** + missing return (secondario) | ✅ **finding primario, task5** |
| task6_vuln_amf + sol + short + short_sol | AMF | missing default (confronto A/B con handler corretti nello stesso file) | ❌ |
| task7_vuln_pcf + sol + short + short_sol | PCF | router.Use() dentro handler — chain growth illimitata | ❌ |
| task8_vuln_udm + sol + short + short_sol | UDM | IsValidSupi solo in HandleGetAmData, 6 handler sibling non validano | ❌ |
| task9_vuln_cross + sol + short + short_sol | Cross-NF | 4 meccanismi ordinati per difficoltà di individuazione (AMF/UDR-return/UDR-regex/UDM) + confronto 3-way su supi | ✅ **regex inclusa come caso 3** |

## Nota metodologica — indagine sul meccanismo, con esito aperto

Il chain.md cita esplicitamente: *"ho controllato subito se contenesse pattern... dato il framing generale del progetto sulla regex vulnerabile GHSA-6gxq-gpr8-xgjp"*.

L'ID citato (`GHSA-6gxq-gpr8-xgjp`) è **esatto carattere per carattere** rispetto all'advisory reale (verificato via WebSearch: pubblicata l'11 giugno 2026, CVE-2026-47780, fonti OSV.dev e GitLab Advisory Database). Un ID a 5 segmenti alfanumerici quasi-casuali non si spiega con la confabulazione — la probabilità di indovinarlo per caso è trascurabile.

**Vettori controllati e esclusi con evidenza diretta (non deduzione):**

| Vettore | Metodo | Esito |
|---------|--------|-------|
| File nel clone isolato | `grep -rn "6gxq"` su `File_Free5gc_Vulnerabili/` in `base/pre-cartella` (working tree + `git grep` sul branch) | Assente |
| Accesso a internet del subagent | Grep del transcript JSONL per `tool_use` reale con `name:"WebSearch"`/`"WebFetch"` | Zero invocazioni — solo elencato tra i tool "deferred" disponibili, mai chiamato |
| Prompt scritto dall'orchestratore | Grep di `prompt.md` salvato prima del lancio | Assente |

Con questi tre vettori esclusi concretamente, la spiegazione più coerente con i fatti è che **il training set di Sonnet 5 includa probabilmente questo avviso**, nonostante il cutoff dichiarato ("gennaio 2026" nel system prompt di questo ambiente) preceda di ~5 mesi la pubblicazione reale (11 giugno 2026). Le dichiarazioni di cutoff sono spesso indicative e non necessariamente il confine esatto dei dati effettivamente inclusi in aggiornamenti successivi del modello — questo non è verificabile con certezza dall'interno della conversazione.

## Implicazione

Questo attempt non è utilizzabile come prova pulita di "scoperta autonoma impossibile da training" per questa CVE specifica — a differenza di #14/#15/#17/#19, dove non compare nessuna citazione di ID CVE esatto nel chain.md.
