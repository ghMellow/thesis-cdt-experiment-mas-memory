# 07 — Discussione: "LLM Judges Can Be Too Generous" e cosa ci porta in casa

> Documento di discussione (2026-07-16). Analizza il paper riportato nel doc 06 (Kranti & Vajjala, arXiv:2607.12885, luglio 2026) — trovato durante le verifiche web del 2026-07-16 e inizialmente citato nel doc 04 §1 solo a livello di abstract; qui la lettura integrale. Valutazione di Claude — da discutere.

## 1. Cosa dice il paper, in tre righe

I giudici LLM in setting **reference-free** (senza ground truth nel prompt) gonfiano sistematicamente la correctness: aggiungere la reference al prompt ribalta i verdetti fino all'**85%** dei casi, e i verdetti *con* reference sono quelli che concordano con gli annotatori umani (alignment da 0.33–0.74 in NR a 0.85–0.96 con reference). Il paper propone una pipeline in due stadi per decidere se un giudice è affidabile in reference-free: **calibration** (sa distinguere risposte giuste da sbagliate?) e **sensitivity** (quanto cambia verdetto quando gli mostri la reference?).

## 2. Perché ci riguarda più della media

Tre coincidenze non casuali con il nostro setup:

1. **Uno dei giudici testati è Gemma3-27B** — la famiglia dei nostri modelli. Nel dominio "difficile" del paper (telugu, MATA) il suo tasso di accettazione di risposte *sbagliate* (C2) arriva a **0.66**: due volte su tre promuove una risposta errata, contro 0.01–0.07 in inglese. La generosità non è uniforme: esplode dove il giudice è al limite di competenza.
2. **Il proxy "lingua low-resource" siamo noi.** Il paper mostra che il problema è marginale dove il giudice è competente (inglese) e massimo dove non lo è. Il nostro dominio — security review di Go su un core 5G, con giudici gemma piccoli — è l'analogo di dominio del telugu: è esattamente il regime dove il doc 01 §3.6 colloca il nostro giudice ("vicino al limite di capacità").
3. **La nostra roadmap va verso il reference-free.** Tutta la cartella (opzione B, doc 05) propone di togliere la GT dal giudizio. Questo paper misura il prezzo di quel passaggio: senza contromisure, la rubric accuracy GT-free sarà *strutturalmente più alta* di quella attuale — non perché i report migliorano, ma perché il giudice diventa più generoso. Se non lo mettiamo in conto, leggeremmo il confronto vecchia/nuova rubrica al contrario.

Due findings secondari ma rilevanti per noi: i flip avvengono già in **Reference-Visible** (la reference nel prompt cambia il verdetto anche senza chiedere il confronto esplicito — il grosso del segnale è la *presenza*, non l'istruzione); e l'analisi qualitativa documenta *self-family bias* (il giudice Gemini che ignora la GT pur di promuovere una risposta della sua famiglia) — il rischio del nostro setup 1A, stavolta osservato e non solo teorizzato.

## 3. Il regalo metodologico: la calibrazione è trasponibile da noi quasi gratis

Il contributo più utile non è il finding (che rafforza quello che già scrivevamo) ma il **protocollo**, che è un blueprint dichiarato e si traspone direttamente perché noi la GT *ce l'abbiamo* (task5–9):

- **Calibration (C1/C2) per il nostro giudice.** C1: si dà al giudice+rubrica un report *coerente con la GT* (i finding veri, riformulati). C2: un report plausibile ma *sbagliato* (es. i finding di un altro task, trapiantati — l'analogo della loro scelta di pescare risposte errate dalla stessa categoria). La differenza C1−C2 (loro la chiamano CGP) misura se il giudice distingue davvero — **prima** di fidarci di lui in regime GT-free. Costo: qualche decina di chiamate offline, zero modifiche al loop.
- **Sensitivity (NR vs reference) sui report già salvati.** Il nostro analogo naturale: stesso report giudicato con la rubrica GT-derivata attuale (≈ il loro RC) e con una rubrica GT-free candidata (≈ il loro NR). Il **flip rate** tra i due è la misura diretta della generosità che il passaggio a GT-free introduce — e siccome abbiamo M1–M3, possiamo anche dire *quale* dei due verdetti aveva ragione, cosa che il paper può fare solo con annotatori umani.

Questo dà forma precisa alla "misura della generosità" che il caveat del doc 04 §1 chiedeva genericamente: non solo accordo con M1 a valle, ma un test di ammissione del giudice (CGP) prima ancora di cambiargli la rubrica.

## 4. Disanalogie da dichiarare (per non comprare troppo)

- **Verdetto binario su QA aperta vs rubrica per-criterio su report strutturati.** Il loro giudice decide CORRECT/INCORRECT su una risposta breve; il nostro somma sub-score su criteri. La decomposizione potrebbe attenuare la generosità (ogni criterio ancora il giudizio) o solo distribuirla — non lo sappiamo, ed è un motivo in più per fare la calibrazione, non per saltarla.
- **La loro "reference" è la risposta d'oro nel prompt; la nostra GT entra per via indiretta** (rubrica GT-derivata). Il nostro RC-analogo è quindi più debole del loro: se anche così osserviamo flip alti verso la rubrica GT-free, l'effetto reale è probabilmente maggiore.
- Il multilinguismo, asse centrale del paper, per noi è solo l'analogia di §2.2 — non trasferiamo i numeri, trasferiamo il meccanismo.

## 5. Posizione e aggancio alla sequenza

Il paper **non è un argomento contro la direzione GT-free** — è il manuale di sicurezza per percorrerla. Conclusione operativa: al passo (1) della sequenza del doc 04 §6 (calibrazione soglia + giudice ≠ agente) va affiancato un **passo (1-bis): calibrazione C1/C2 del giudice** sui task con GT, e ogni confronto futuro "rubrica attuale vs rubrica GT-free" va letto insieme al flip rate, non solo all'accuracy. Rafforza anche la scelta del doc 05 di tenere il coverage *fuori* dal giudizio LLM: ogni criterio calcolato deterministicamente è un criterio che non può essere gonfiato dalla generosità.

Va infine citato in tesi accanto a VulTrial (leniency del critico LLM in ambito vulnerability, doc 01 §2): stesso fenomeno, misurato lì nel dominio e qui nel meccanismo (presenza/assenza della reference).
