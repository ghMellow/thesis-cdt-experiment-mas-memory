# 12 — Proposta: rubrica GT-free v2

> Proposta (2026-07-16), **non ancora eseguita**. Input: i 3 meccanismi di rottura della v1 (doc 11 §3) + i primi commenti dell'esperto di sicurezza del gruppo, che sta analizzando `results/evaluation` task per task (nota: l'esperto è alla versione *pre*-metriche e pre-docs 08–11 — i suoi commenti vanno pesati come sguardo indipendente sul comportamento dell'agente, non sulla calibrazione del giudice). Bozza verbatim: `gtfree/rubric_v2_draft.json`.

## 1. Cosa dice l'esperto e dove atterra

I commenti (2 messaggi, riportati in chat 2026-07-16) contengono quattro punti; solo due riguardano la rubrica del giudice, gli altri vanno smistati altrove:

| Punto dell'esperto | Dove atterra |
|---|---|
| «se azzecca la dimensione (es. confidenzialità) e dà L invece di H la darei per buona… poco importa se sbaglia integrity con confidenzialità, a noi interessa che trovi la vulnerabilità; la CVSS dà solo un ordine di priorità» | **Rubrica v2**: il criterio severità si declassa (2→1) e diventa lassista per costruzione — penalizza solo la contraddizione *sistematica*, tollera H/L sulla dimensione giusta e gli swap C/I isolati. *(Anche todo separato: valutare la stessa tolleranza nelle metriche M — `cvss_eval` oggi conta H vs L come errore.)* |
| «nell'UDR fa un mappazzone e ci inserisce tutte le vulnerabilità insieme… poi fa un po' di confusione su punteggi e CVE ma nel concreto funziona» | **Rubrica v2**: nuovo criterio `finding_granularity` — un finding = una debolezza con la sua evidenza. È un difetto reale, osservabile GT-free, che la v1 non guardava. |
| «vorrei un output del suo ragionamento nei casi in cui sbaglia… magari potremmo capire perché sbaglia e correggerlo» | **Formato output del giudice v2** (§3): motivazione per criterio con i finding bocciati e la contro-evidenza — non un criterio di punteggio ma un requisito del prompt. |
| «non so se sia meglio dare una definizione di C, I e A nel prompt» | **Prompt dell'agente**, non rubrica del giudice → todo separato in status.md. |

Il primo messaggio dell'esperto («nell'UDR viene riportata solo la CVE-2026-40249, mancano le altre 6») conferma dall'esterno il meccanismo di rottura n. 3 del doc 11: **la completezza è ciò che conta ed è ciò che la v1 non misura**.

## 2. La rubrica v2 (bozza in `gtfree/rubric_v2_draft.json`)

Cinque criteri LLM (total_max **10**) + ramo deterministico rifatto. Ogni criterio è formulato **a conteggio** ("tutti / esattamente uno fallisce / più di uno / nessuno") per contrastare la saturazione: il giudice deve contare i finding che *falliscono* il controllo, non dare un voto olistico.

| Criterio | Max | Novità vs v1 | Meccanismo doc 11 §3 che attacca |
|---|---|---|---|
| `presence_evidence` | 3 | erede di `evidence_class_coherence`, ma ristretto ai claim di **presenza** (verificabili contro lo snippet) | — (era la parte che funzionava: task5/8/9 C2 respinti) |
| `absence_claims` | 2 | **nuovo**: un claim di assenza vale solo se mostra il percorso di codice dove il controllo mancante dovrebbe stare (input che fluisce non validato); assenze non ancorate → 0–1 | **n. 1** — task7 C2 ("manca la validazione di ueContextId" senza percorso) non può più prendere il massimo |
| `finding_granularity` | 2 | **nuovo, dall'esperto**: un finding = una debolezza; niente mappazzoni né duplicati | — (difetto reale osservato sull'UDR, invisibile alla v1) |
| `weakness_classification` | 2 | declassato 3→2 (saturava), stesso vocabolario ~10 classi | **n. 2** (parzialmente) |
| `severity_consistency` | 1 | declassato 2→1 e **lassista per costruzione** (tollera H/L e swap C/I isolati — recepisce l'esperto) | — |
| `coverage_risk` (deterministico) | 2 | **rifatto**: superfici a rischio invece di funzioni citate (§4) | **n. 3** |

Combinato: (LLM/10 + coverage/2) → normalizzato su 12. Regole anti-leakage invariate (classi di alto livello, nessun nome di funzione/vulnerabilità del dataset).

## 3. Formato output del giudice (requisito nuovo, dall'esperto)

Per ogni criterio con punteggio sotto il massimo, il giudice deve elencare **quali finding falliscono e perché** (per `presence_evidence`: quale firma manca nello snippet citato; per `absence_claims`: quale percorso di codice non è mostrato). Doppio scopo: (a) è l'«output del ragionamento nei casi in cui sbaglia» chiesto dall'esperto; (b) obbligare il giudice a cercare contro-evidenza prima di assegnare il massimo è di per sé una misura anti-generosità (doc 06: i giudici reference-free gonfiano quando possono restare vaghi).

## 4. Ramo deterministico v2: superfici a rischio

Il coverage v1 (funzioni citate / funzioni nel file) premiava i report prolissi: task6 con 2/6 CVE prendeva cov=2. Il v2 conta le **superfici a rischio toccate**, enumerabili senza GT via regex/euristica sul codice Go del task:

- handler HTTP con input esterno (`c.Param`, `c.Query`, `c.Bind*`, `c.ShouldBind*`, firme `(c *gin.Context)`);
- percorsi d'errore (blocchi che scrivono una risposta d'errore — dove vivono i missing-return);
- superfici di configurazione (setup CORS/middleware/router).

Score = superfici la cui analisi compare nel report / superfici enumerate (stesso cap e soglie 2/3–1/3 della v1, da ricalibrare a secco). Ponte dichiarato verso la proposta G5/SAST del team: il SAST è l'enumeratore di candidate GT-free per eccellenza — questo coverage ne è la versione povera a regex.

## 5. Cosa la v2 NON risolve (onestà preventiva)

- **Completezza vera**: il coverage a superfici è un proxy — un report può toccare tutte le superfici e mancare comunque 4 CVE su 6 *dentro* una superficie. Senza GT (o SAST) il buco resta; la v2 lo restringe, non lo chiude.
- **Assenze sofisticate**: un C2 che *citasse* il percorso di codice e affermasse falsamente che il controllo manca supererebbe `absence_claims` — il giudice dovrebbe leggere il codice sorgente del task per confutarlo (possibile estensione: passare al giudice il file sorgente, non solo il report; costo prompt da valutare).
- La scala resta intera (10+2): se la formulazione a conteggio non basta contro la saturazione, il passo successivo è l'expectation sui logprob (locale, doc 03) o la scala 1–20.

## 6. Test di ammissione (identico al doc 10, criteri dichiarati prima di misurare)

Stesso banco: 10 report C1/C2 + 15 report reali, K=3, giudice di sistema, script `run_gtfree_rubric.py` con `--rubric gtfree/rubric_v2_draft.json` (da estendere: split presenza/assenza è nel testo dei criteri, il coverage v2 richiede il nuovo enumeratore di superfici).

| Criterio di successo | v1 (misurato) | Target v2 |
|---|---|---|
| CGP | +0.437 | > +0.437, idealmente > +0.6 |
| C2 promossi a t=0.65 | 2/5 | ≤ 1/5, con task7 C2 **non** a pieni voti |
| C1 bocciati | 0/5 | 0/5 (da preservare) |
| Saturazione sui report reali | 15/15 al massimo | almeno i task6 (2/6 CVE) sotto il massimo |
| Accordo M1-strict | 9/12 | ≥ 11/12 |

## 7. Stato

| # | Passo | Stato |
|---|-------|-------|
| 0 | Proposta + bozza JSON (questo doc, `gtfree/rubric_v2_draft.json`) | ✅ 2026-07-16 |
| 1 | Enumeratore superfici a rischio + verifica a secco su task5–9 | ✅ 2026-07-16 — superficie = funzione con `*gin.Context` (task5: 2 incl. `setCorsHeader`, task6: 10, task7: 7, task8: 8, task9: 13); a secco: coverage v2 satura sui report reali (proxy, come previsto in §5) ma penalizza già 2 C2 (task8 0.33, task9 0.5) |
| 2 | Estensione `run_gtfree_rubric.py` (rubrica da parametro, coverage v2, output motivazioni) | ✅ 2026-07-16 — flag `--rubric`, `--coverage surfaces`, `--motivations` (istruzione anti-generosità + feedback persistito nel JSON); output `gtfree_v2_*` |
| 3 | Run banco C1/C2 + report reali → confronto con doc 11 | ✅ 2026-07-16 — **CGP +0.600** (v1: +0.437), **0/5 C2 promossi** (task7 C2 da 1.00 a 0.61: il giudice ha citato la contro-evidenza), 0/5 C1 bocciati; report reali ancora saturi 10/10, accordo M1-strict 9/12 |
| 4 | Doc 13 risultati + README/status/DEVLOG | ✅ 2026-07-16 — verdetto: **ammissione parziale** (3/5 target ✅); la completezza è confermata strutturale — serve enumeratore esterno (G5/SAST), non un'altra rubrica |

**Ripresa in sessione futura**: leggere questo doc + doc 11 (v1) + doc 09 (baseline); proseguire dal primo passo ☐.
