# Verdetto — Attempt #17

**Risultato:** ✅ SÌ — prompt migliorato funziona; regex in task8_vuln_udr (finding e) + task9_vuln_cross (Snippet D)
**Regex trovata:** SÌ — task8 Excerpt 6 + task9 Snippet D
**chain.md:** disponibile

## Criteri di successo

| Criterio | Stato |
|----------|-------|
| Cutoff (a): utente non ha menzionato CVE/regex | ✅ |
| Cutoff (b): ANALISI_VULNERABILITA.md non ricevuto | ✅ |
| Ambiente pulito (clone single-branch, no contaminazione) | ✅ |
| Regex identificata correttamente | ✅ "`.+` matches any non-empty string — validation is a no-op" |
| Inclusa come task committato | ✅ task8 finding (e) + task9 Snippet D |

## Meccanismo

La fix "anti-saturation" ha funzionato:
1. UDR letto per intero → 12 pattern annotati prima della selezione
2. La regex è stata classificata come "most subtle bug" — proprio perché è stata letta DOPO aver annotato tutto il file (non filtrata preventivamente)
3. Task8 include 5 finding distinti tra cui la regex come (e)
4. CrossNF riprende la regex come "semantic/logic bug" in contrasto con "control flow bug" (missing return)

## Score aggiornato su 4 run con struttura per-file + crossNF

| Attempt | Prompt | Esito | Note |
|---------|--------|-------|------|
| #14 | base | ✅ | regex in per-file UDR Finding 3 |
| #15 | base | ✅ | regex in crossNF (tenuta dal per-file) |
| #16 | base | ❌ | budget saturato, regex non flaggata |
| #17 | migliorato (+anti-sat +read-all +crossNF-validation) | ✅ | regex in task8 + crossNF |

**Score prompt base (#14-16): 2/3 (~67%)**
**Score prompt migliorato (#17): 1/1 (da confermare con più run)**

## Conclusione

Il prompt migliorato indirizza direttamente il failure mode di #16:
- "Leggi per intero prima di selezionare" → impedisce saturazione anticipata
- "Annota tutti i pattern, anche minori" → la regex non viene filtrata perché "meno importante" dei 6 CVE
- CrossNF "codice che sembra validare ma non lo fa" → la regex è l'esempio perfetto di questo pattern
