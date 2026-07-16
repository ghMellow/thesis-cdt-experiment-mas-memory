# 05 — Discussione: rubrica "esperto di sicurezza" × CWE MITRE (con declinazione 5G)

> Documento di discussione (2026-07-16). Sviluppa l'idea nata in coda alla dodicesima call (vedi `00_call12_2026-07-14.md` §2–3): impostare la rubrica simulando il metodo di lavoro di un esperto di sicurezza, ancorandola alle CWE del MITRE — eventualmente quelle rilevanti per il 5G. Nel doc 04 le due idee erano state pesate *separatamente* (opzione A ridimensionata, opzione C complementare); qui si valuta la loro **combinazione**, che è più forte di ciascuna delle due da sola. Valutazione di Claude — da discutere.

## 1. Perché la combinazione cambia il giudizio dato nel doc 04

Le obiezioni alle due idee prese singolarmente erano speculari:

- L'opzione A (workflow esperto) da sola è **struttura senza vocabolario**: "hai tracciato il flusso dati?" è una domanda che il giudice può riempire di apparenza, e per valutarla davvero dovrebbe rifare l'analisi.
- L'opzione C (CWE) da sola è **vocabolario senza struttura**: una lista di classi non dice al giudice *cosa controllare* di un report, e scegliere quali classi mettere in rubrica rischiava di reintrodurre la GT.

Ma è esattamente così che lavora un esperto vero: **un metodo sistematico che percorre superfici e flussi usando una tassonomia di debolezze note come checklist mentale** (Top 25, OWASP, esperienza codificata). Il workflow è il *come*, le CWE sono il *cosa*. Combinate, ciascuna tappa il buco dell'altra:

| Asse | Contributo | Buco che tappa |
|---|---|---|
| Workflow esperto | Struttura dei criteri: quali domande fare al report, in che ordine | Le CWE da sole non dicono cosa verificare |
| CWE | Ancoraggio semantico pubblico, stabile, GT-free per costruzione | Il workflow da solo è valutabile solo "a impressione" |

## 2. Il dubbio di fondo: ha senso un giudice-esperto che valuta il lavoro di un agente?

Il dubbio (sollevato dall'utente ed emerso identico in call: "bisogna capire dove entra") è legittimo, e la risposta dipende da **quale mestiere** si assegna al giudice:

- **Giudice-analista** (rifà l'analisi da esperto e confronta): non ha senso. Se il giudice sapesse fare l'analisi meglio dell'agente, useremmo lui come agente; ed è la configurazione dove pesano di più capacità limitata, contaminazione e leakage.
- **Giudice-auditor** (verifica il *report* contro la checklist dell'esperto): ha senso, e c'è una ragione teorica — il **generator-verifier gap**: verificare un'argomentazione è sistematicamente più facile che produrla (è l'assunto su cui poggia tutta la letteratura dei verifier, incluso il paper del doc 02). L'auditor non deve trovare la vulnerabilità: deve controllare che il finding dichiari una classe di debolezza plausibile, che l'evidenza citata sia *compatibile con la firma di quella classe* (un ReDoS deve citare una regex; un CORS misconfigurato deve citare una policy), e che l'analisi abbia coperto le superfici del file.

Quindi: l'idea "come lavora l'esperto" **non va data al giudice come identità** ("sei un esperto, rifai l'analisi") ma **come checklist di audit** sul lavoro altrui. È la differenza tra chiedere a un revisore di riscrivere il paper e chiedergli di controllare che i claim siano supportati.

C'è anche un secondo ingresso possibile, da non confondere col primo: il workflow esperto come guida **dell'agente** (nel prompt di generazione). Legittimo, ma è un esperimento sul generatore, non sul giudice — e va tenuto separato, altrimenti non si capisce quale dei due interventi produce l'effetto.

## 3. Bozza concreta: rubrica a matrice workflow × CWE

Istanziazione dell'opzione B del doc 04 con questo materiale (criteri GT-free, punteggio estratto col metodo probabilistico del doc 03):

| Criterio (fase del workflow) | Domanda di audit al report | Ancoraggio CWE |
|---|---|---|
| **Coverage delle superfici** | L'analisi ha toccato gli entry point del file (handler HTTP, parser, percorsi d'errore)? | — (calcolabile *deterministicamente*, vedi sotto) |
| **Classificazione della debolezza** | Ogni finding dichiara una classe CWE plausibile per l'evidenza citata? | classi di alto livello (input validation, error handling, authz, esposizione dati, DoS) |
| **Coerenza evidenza↔classe** | Lo snippet citato mostra la firma tipica della classe dichiarata? | firme per classe (regex→ReDoS, switch senza default→unexpected state, header→CORS/authz) |
| **Coerenza classe↔severità** | Il vettore CVSS è compatibile con la classe (un DoS puro con VC:H è incoerente)? | mapping CWE→pattern d'impatto tipico |

Due note che rendono la cosa più solida di come suona:

- **Il criterio di coverage non serve nemmeno l'LLM.** L'elenco degli handler/funzioni del file è già estratto dall'SGV (G2 conosce i simboli dell'estratto): `funzioni toccate dai finding / funzioni esposte nel file` è un rapporto **deterministico**, in pieno stile SGV. Il pezzo più "gameable" del workflow esperto (la sistematicità) esce così dal giudizio LLM. Risolve anche l'obiezione form-over-substance del doc 04 §2.
- **La coerenza classe↔severità collega due output che già esistono** (finding testuale e vettore CVSS) senza toccare la GT: è il criterio *Internal consistency* del doc 04 reso operativo dal vocabolario CWE.

### Il livello giusto della tassonomia (il punto critico anti-leakage)

Il rischio segnalato nel doc 04 §4 resta: se il sottoinsieme di CWE in rubrica viene curato *guardando le nostre 10 CVE* (ReDoS, CORS, missing default, input validation…), la GT rientra dalla finestra. Mitigazione per costruzione: usare un **livello alto della gerarchia** (i pillar/class di CWE-1000 sono ~10 categorie: improper input validation, improper access control, improper error handling, resource consumption, ecc.) oppure un riferimento pubblico e indipendente dal dataset come la **CWE Top 25**. A quel livello ogni codebase reale è coperta, quindi non c'è informazione sul *nostro* dataset dentro la rubrica — e la scelta è difendibile in un articolo con una riga.

## 4. E la declinazione 5G? (onestà sui riferimenti)

Qui serve precisione, perché in call il punto è rimasto vago ("c'erano delle [CWE] del 5G in particolare"):

- **Non esiste una vista CWE ufficiale per il 5G.** *(Verificato 2026-07-16 su cwe.mitre.org, CWE v4.20)*: le viste sono generali (Software Development CWE-699, Research Concepts CWE-1000, Hardware CWE-1194, Top 25 2025) più viste per linguaggio, standard di coding, OWASP, mobile *applications* (app-level, non reti mobili) e AI/ML — nessuna vista o categoria telco/5G.
- Quello che esiste per il dominio: **MITRE FiGHT™** (framework di minacce per 5G, ma è ATT&CK-like — tattiche/tecniche d'attacco, non classi di debolezza del codice) e le **3GPP SCAS** (Security Assurance Specifications, requisiti di sicurezza per NF con test case). Utili come *contesto* e per i related work, ma non sostituiscono le CWE come vocabolario di code review.
- La via pragmatica: rubrica ancorata alle classi CWE generali (§3), più un **contesto di dominio nel prompt del giudice** ("il file è una network function di un core 5G: le superfici tipiche sono SBI/HTTP, N1/N2, dati subscriber") — che è l'evoluzione naturale dell'hint di contesto NF già testato in run 2. La specificità 5G entra come contesto, non come tassonomia: meno elegante ma onesta, e non richiede di inventare una "CWE 5G" che non c'è.

## 5. Validazione e rischi

**Validazione (R4 + controprova della call 12):** sui task con GT si misura l'accordo del giudice-auditor con M1–M3, e in più la **accuratezza di classificazione CWE sui TP** diventa una metrica downstream nuova, gemella delle S (le nostre CVE hanno CWE assegnate negli advisory GHSA — la GT resta a valle, mai nel giudizio). La controprova decisiva è quella proposta dal relatore: file mai visto, stesso giro, verifica a mano — una rubrica davvero GT-free deve funzionare identica.

**Rischi da dichiarare:**

1. *Capacità di classificazione del giudice.* La call 12 lo ha già osservato ("ci ha dato quattro weakness, non quella [attesa]"): classificare per CWE è un giudizio semantico non banale per modelli piccoli. La letteratura lo quantifica ed è dura: sul benchmark CWE-Trace (834 sample kernel Linux, 74 CWE) la Top-1 accuracy di classificazione CWE esatta resta **sotto l'1.3%**; e su 66k CVE un TF-IDF tradizionale batte gli LLM in classificazione (74% vs 59% direct prompting — "On Using LLMs for Vulnerability Classification", LAMPS 2025). Questo è l'argomento empirico decisivo per la mitigazione già proposta: livello alto della tassonomia (~10 classi invece di 900 cambia radicalmente il compito) + estrazione probabilistica (doc 03) che misura l'incertezza invece di nasconderla.
2. *Il limite ammesso in call resta:* con questo approccio non si scoprono classi di debolezza nuove — accettabile perché l'obiettivo è trovare *vulnerabilità* nuove dentro classi note.
3. *Doppio uso da non mescolare:* se il vocabolario CWE finisce sia nel prompt dell'agente sia nella rubrica del giudice, l'accordo agente–giudice si gonfia per costruzione. Sceglierne uno per volta, o dichiarare l'accoppiamento.

## 6. Sintesi della posizione

L'idea della call 12 non è un'alternativa in più da mettere in fila alle altre: **è il modo concreto di riempire l'opzione B del doc 04**. Il workflow esperto fornisce le righe della rubrica, le CWE di alto livello il vocabolario, l'SGV il pezzo deterministico (coverage), il metodo del doc 02/03 l'estrazione del punteggio. Il giudice che ne esce non "fa l'esperto" — fa l'**auditor di un report scritto da qualcuno che doveva fare l'esperto**, che è l'unico ruolo in cui un modello della stessa taglia dell'agente ha un vantaggio strutturale (verificare < generare). La specificità 5G entra come contesto di dominio nel prompt, non come tassonomia inesistente.

Aggiornamento della sequenza proposta (doc 04 §6): i passi (1) calibrazione soglia e (2) pilota probabilistico restano invariati; il passo (3) "rubrica per-dominio" ha ora una forma concreta — la matrice del §3 — e un test di accettazione preciso: la controprova sul file mai visto.
