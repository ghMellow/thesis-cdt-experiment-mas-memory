per ogni tematica troverai prima una breve rielaborazione che dà il contesto della conversazione, seguita dai messaggi testuali integrali (parola per parola, senza alcun taglio o abbreviazione) scambiati dagli esperti di sicurezza e dai membri del team.

1. Valutazione dell'impatto delle vulnerabilità e fornitura del contesto all'LLM
Contesto: Il gruppo discute se le informazioni passate al modello (solo 4 file) siano sufficienti per fargli valutare correttamente l'impatto di una vulnerabilità. Gli esperti di cyber security concordano sulla necessità di fornire all'LLM una visione di insieme più ampia, suggerendo di passargli l'intero codice e di specificare nel prompt dettagli di sicurezza intrinseci del sistema (come OAuth e TLS).

Andrea Bernardini, 9 lug, 14:20
"Ultimo dubbio per quanto riguarda il discorso della valutazione dell'impatto, ma riferito più che altro agli esperti di cyber @Francesco D'Alterio @Lorenzo Cannella @Mariano Forte . Per stimare l'impatto correttamente normalmente un valutatore umano valuta la vulnerabilità riscontrata in un file all'interno di un contesto più complesso, sapendo anche il ruolo svolto da quel file NF nel contesto più generale. In questo caso noi gli stiamo passando solo 4 file o gli stiamo dando spunti che gli facciano capire che si tratta di elementi di free5Gc e che lui potrebbe andare a documentarsi al riguardo ? Potrebbe aver senso ritestare questa valutazione passandogli eventualmente tutto free5Gc."

Mariano Forte, 9 lug, 15:22
"Si in teoria per stimare l’impatto bisognerebbe fargli capire la rilevanza e l’importanza di tutte le NF quindi sì potrebbe aver senso dargli direttamente tutto free5GC"

Lorenzo Cannella, 9 lug, 15:31
"concordo"

Lorenzo Cannella, 9 lug, 15:33
"suggerisco di inserire nel prompt che il sistema è una rete core 5g che ha di per sè Oauth e TLS sempre attivi, potrebbe aiutarlo nel ragionamento dell'impatto"

2. Efficacia di SonarQube (SAST) vs LLM per l'identificazione delle vulnerabilità
Contesto: Analizzando i risultati di SonarQube (tool di analisi statica), emerge che su 54 alert quasi nessuno rappresenta una vera vulnerabilità (nessuna CVE). Gli esperti commentano i limiti del tool, considerandolo più utile per i programmatori che per gli analisti di sicurezza, e ipotizzano che i modelli LLM lo supereranno, pur riconoscendo la complessità del linguaggio GO.

Andrea Bernardini, lun 16:15
"Se si, su 54 ipotesi di vulnerabilità di SonarQube solo 4 corrispondono a vulnerabilità. Già solo questo motiverebbe l'utilizzo di un sistema di pulizia intelligente dei risultati per evitare di costringere i valutatori umani a fare tutte queste verifiche inutili.
Unico dubbio che non capisco è che c'è per i 4 un riferimento alla weakness CWE e non ad una CVE effettiva.
Se fosse una CVE allora si potrebbe creare una matrice di confusione e poi confrontare i risultati con quelli del sistema LLM"

Lorenzo Cannella, lun 16:22
"allora andre, ground_truth_NF sono i code smell di SQ su tutte le NF di free5gc quindi per ora non consideriamolo
ground_truth_vuln_files.json sono i code smell di SQ dei file dove sono le vulnerabilità, prendi quelli. csv e json hanno gli stessi dati, quello invece excel sono i dati ma analizzati a posteriori e purtroppo sonarqube pensa di aver riconosciuto vulnerabilità ma in realtà non trova praticamente nulla, neanche una CVE
da solo degli hint molto banali più forse da programmatore che da security analist"

Andrea Bernardini, lun 16:50
"La domanda a questo punto è. Che valore aggiunto porta un tool come questo ad un framework di LLM ? Sono numeri veramente bassi
Sarà interessante replicare una tabella come questa per il sistema LLM e poi per l'unione SAST+LLM"

Lorenzo Cannella, lun 16:55
"sono d'accordo, ma infatti uno spunto per l'articolo potrebbe essere anche quello di dire che l'analisi statica del codice verrà pensionata dagli LLM. A difesa di sonarqube però sono sicuro che GO non sia proprio un linguaggio semplice da analizzare per lui, forse su C avrebbe inciso di più (tipo con OPEN5GS che è l'altra core)
non lo so, sono supposizioni"

Mariano Forte, lun 16:56
"Sono d’accordo"

3. Stima dei vettori CVSS 4.0, Confidenzialità, Integrità e definizione dei Prompt
Contesto: Lorenzo Cannella analizza le risposte del modello riguardo i punteggi CVSS. Sottolinea che alcuni errori (es. confondere integrità con confidenzialità o assegnare "low" invece di "high") sono trascurabili a fini pratici, purché la vulnerabilità venga effettivamente trovata. Suggerisce inoltre di inserire nel prompt le definizioni esatte delle metriche per aiutare il modello.

Lorenzo Cannella, mar 10:26
"Buongiorno a tutti, come primo step ho analizzato la stima dei CVSS degli LLM, ho notato che in primis nell'esperimento dell'UDR viene riportata solo la CVE-2026-40249, mancano le altre 6"

Lorenzo Cannella, mar 10:33
"poi considerazione mia, in quelle in cui azzecca il valore (esempio confidenzialità) e al posto di dare valore high lo dà low io la darei per buona perchè a parer mio in molti casi rimane arbitrario. Per quelle per cui al posto di confidenzialità mette integrità vorrei sapere se magari è possibile avere un output del suo ragionamento nei casi in cui sbaglia. Attualmente nella CVE-2026-41135 sulla PCF e CVE-2026-41136 su AMF (mancano quelle dell'UDR). Altra considerazione, alla fine poco importa secondo me nei fini pratici se sbaglia integrity con confidenzialità o analoghe tanto ai fini pratici a noi interessa che trovi la vulnerabilità, la CVSS ci dà solo un ordine di priorità ma alla fine la cosa migliore sarà sempre quella di analizzarle tutte, ad ogni modo con l'output del ragionamento magari potremmo capire perchè sbaglia e correggerlo"

Lorenzo Cannella, mar 10:33 (Messaggio successivo allegato al file)
"Sto mettendo i miei appunti qui, ho cambiato il CVSS della nostra cve perchè era troppo basso, ti consiglio di riprenderli tutti perchè forse in un altro dell'UDR c'era un errore. Ora sono tutti corretti e ricontrollati"

Lorenzo Cannella, mer 09:56
"Buongiorno, il prompt mi sembra scritto molto bene, non se sia meglio dare una definizione di C,I e A quando le metti qui:

VC / VI / VA Confidentiality / Integrity / Availability impact on the
vulnerable system: H (High), L (Low), N (None)

Tipo confidenzialità se è possibile accedere a dati sensibili
Integrità se tali dati possono essere compromessi

è un'ipotesi poi non lo so se funziona

Inoltre analizzando le CVE che trova nell'UDR nei dettagli si vede chiaramente che fa un mappazzone e ci inserisce tutte le vulnerabilità insieme, poco male. Ora però mi concentro sulla parte di findings e non sulla validazione, alla fine le vulnerabilità sembra riconoscerle, poi fa un pò di confusione su punteggi e cve ma nel concreto funziona e questo è più importante. Controllo i findings e vediamo se ha trovato qualcosa di interessante da aggiungere al lavoro. Ti aggiorno appena riesco"

4. Identificazione di nuove vulnerabilità (Zero-Day/Findings)
Contesto: Il team ha utilizzato il framework per identificare nuove vulnerabilità non ancora note. Lorenzo comunica l'esito della sua analisi manuale sui "findings" (le anomalie trovate) prodotti dal modello, riportando la scoperta di 10 nuove potenziali vulnerabilità.

Lorenzo Cannella, 48 min
"Buon pomeriggio a tutti, vi condivido tutti gli aggiornamenti sui findings: CVE_CVSS.docx
Vi spoilero che sono state identificate 10 nuove vulnerabilità, ho aperto i report e vi ho taggati a tutti. Vi sottolineo che molte di queste sono vulnerabilità con un impatto molto basso ma che ho comunque segnalato, ora bisogna aspettare e vedere quante di queste ci verranno accettate come CVE ma ad ogni modo è un ottimo risultato. Nel documento trovate tutte le mie considerazioni di cui poi parleremo assieme anche riguardo alla validazione (dovrei aver capito perché sbaglia a identificare gli impatti). Attualmente non potete vedere i link di github che ho messo perchè sono privati ma vi arriverà l'email una volta che verranno accettati."