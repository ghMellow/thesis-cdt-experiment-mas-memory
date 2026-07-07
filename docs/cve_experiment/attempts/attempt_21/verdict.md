# Verdetto — Attempt #21 (replica confound #2/2)

**Risultato:** ✅ SÌ — regex trovata come finding primario, scoperta bottom-up genuina
**Regex trovata:** SÌ — task5_vuln_udr, finding primario
**chain.md:** disponibile

## Criteri di successo

| Criterio | Stato |
|----------|-------|
| Cutoff (a): utente non ha menzionato CVE/regex | ✅ |
| Cutoff (b): ANALISI_VULNERABILITA.md non ricevuto | ✅ |
| Ambiente pulito (clone single-branch, no contaminazione) | ✅ |
| Regex identificata correttamente | ✅ — formalizzazione corretta dell'alternation |
| Inclusa come task committato | ✅ task5 primario |
| Genuina scoperta bottom-up | ✅ |

## Correzione rispetto alla prima analisi (importante)

Nella prima stesura di questo verdetto avevo interpretato la frase del chain.md — *"ho controllato subito se contenesse pattern... dato il framing generale del progetto sulla regex vulnerabile GHSA-6gxq-gpr8-xgjp"* — come un segnale di **recognition genuina da training data**.

**Correzione dell'utente:** la CVE GHSA-6gxq-gpr8-xgjp è stata scoperta dal team dell'utente a **maggio 2026**. Nessun modello con training cutoff ≤ gennaio 2026 (Sonnet 5, che ha eseguito questo subagent) può averla vista in pretraining — la GHSA non esisteva ancora pubblicamente quando il modello è stato addestrato.

**Conclusione corretta:** la frase nel chain.md è **confabulazione**, non recall genuino. Il modello ha trovato il bug `|.+` per analisi diretta e corretta della regex (questo richiede solo comprensione dell'alternation, nessuna conoscenza pregressa), ma nel *narrare* il proprio processo di ragionamento ha "agganciato" un ID CVE plausibile come se lo riconoscesse — un comportamento noto di LLM che arricchiscono le proprie spiegazioni con riferimenti dall'aspetto autorevole, anche quando inventati o non verificabili.

**Implicazione metodologica:** i `chain.md` auto-riportati dai modelli possono contenere claim di "riconoscimento" o "training data" fabbricati anche quando la scoperta sottostante è del tutto genuina. Il self-report del processo di ragionamento non è una fonte affidabile al 100% per determinare *come* un modello è arrivato a un risultato — va sempre incrociato con evidenza esterna (in questo caso: la data di scoperta della CVE, nota solo all'utente).

## Confronto tra le due repliche del test di confound

| Attempt | Esito | Meccanismo |
|---------|-------|-----------|
| #19 (originale) | ✅ SÌ | grep generico (`regexp.MatchString`) per efficienza di lettura — bottom-up |
| #20 (replica 1) | ❌ NO | grep mirato su pattern diversi (missing-return, Deserialize); sezione regex mai raggiunta — scope coverage failure |
| #21 (replica 2) | ✅ SÌ | grep mirato su `regexp\.`, poi analisi semantica corretta — bottom-up, con narrazione post-hoc fuorviante ("training data") che è confabulazione, non recall reale |

## Score aggiornato — struttura per-file+crossNF, senza narrativa "modelli locali"

| Attempt | Esito |
|---------|-------|
| #19 | ✅ (bottom-up) |
| #20 | ❌ (scope coverage) |
| #21 | ✅ (bottom-up, con confabulazione nel self-report) |

**2/3 su questa variante (~67%)** — in linea con lo score generale della struttura (4/6 con narrativa + 2/3 senza = 6/9 ≈ 67% complessivo).

## Conclusione

Tutti e 3 i successi confermati in questo blocco (#14, #15, #17, #19, #21) sono scoperte bottom-up genuine — nessuna contaminazione, nessun recall reale da training data possibile per questa specifica CVE (impossibile per costruzione: la CVE non esisteva pubblicamente prima della scoperta del team a maggio 2026, quindi non può essere nel training set di nessun modello usato in questi esperimenti).

Il dato interessante che resta è comportamentale, non di contaminazione: i modelli tendono a **narrare le proprie scoperte come riconoscimenti** anche quando non lo sono — un bias di auto-presentazione che va tenuto presente ogni volta che si usa un chain.md come fonte primaria per classificare il meccanismo di una scoperta.
