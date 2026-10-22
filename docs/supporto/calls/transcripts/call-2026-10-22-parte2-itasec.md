# Trascrizione audio grezza — call 2026-10-22, parte 2: articolo ITASEC e risultati SAST

> Trascrizione automatica non editata (materiale-fonte), con il rumore dello speech-to-text.
> Riguarda questo esperimento: articolo ITASEC come estensione del paper IEEE ICAI TEMS 2026,
> braccio a 3 tool SAST, run e repetition nei report, architettura e pipeline da descrivere.
> La parte 1 della stessa call (sommario della tesi) è in `call-2026-10-22-parte1-sommario-tesi.md`.

---

E qui adesso io poi tra cinque minuti vi lascio come dicevo, c'è da da capire, ma articolo per Itasec Allora guarda, mo mi metto a scrivere ho fatto un po' la struttura e c'ho un po' di dubbi da da chiedere a Nico.

Allora ho coinvolto anche il buon Lorenzo che è tornato ieri si sta guardando un po' lui diciamo gli output però ci guardiamo un po' insieme infatti poi Nico dopo ti devo sequestrare un attimo ok perché allora cioè nel senso abbiamo capito che i stati sono un po' meglio perché pure le iterazioni cioè dicono più cose, però ma un attimo ci deve una mano solo per capire cosa ha il confronto tra i risultati vecchi e quelli nuovi, perché se impazziamo al processo auto da capo. Ci devi un po' far capire, cioè nel senso te l'ho scritto pure in chat ci serve un attimo se ci link precisi cioè da dove abbiamo preso i risultati del vecchio paper e magari così c'è guardiamo una Una dall'altra e cerchiamo di fare differenze che il primo risultato sarà qui se poi analizziamo nel detta ok su questo due domande allora intanto mi sembra che tutti vi ha invitato anche Mario e Raffaele sul documento di Francesco, perché daremo una mano.

Solo che Francesco ci deve dare un attimo sulle tempistiche nel senso nei momenti in cui metti una cosa grezza la discutiamo. Seconda cosa, allora no nel senso te lo chiedevo Francesco perché si potrebbe mettere anche in presentazione a sottomesso a Però considera che appunto Nicolò il 29 consegna il sommario per il 30 noi dobbiamo finire però nel momento in cui decidiamo di farlo con tutte le cose 200 cose abbiamo da fare, sappiamo se Nicolò mette dentro o meno.

No, allora guarda, diciamoci un po' cioè mi ero un attimo un po' fermato perché volevo dei primi risultati, perché sennò alla fine diciamo diventa veramente fuffa.

Invece fatto i risultati ce li siamo un po' guardati e sono interessanti, quindi un articolo si può fare.

Che sonovamente la la copia di quell'altro invece adesso c'è qualcosa in più c'è diciamo il dubbio che c'avevo all'inizio era se citare quell'altro articolo e dire che questa è un estensione oppure inglobarlo e farlo diventare diciamo una sorta di di estensione non come dire, cioè nel senso senza girarlo, quindi riprendere un po' i pezzi direi di citarlo sicuramente perché l'unica cosa se lo citi non può prendere i pezzi cioè è ridicolo far presentare due cose che sono uguali no uguali no però nel senso cioè nel senso far capire che questa è un po' un'estensione di quello Nel momento in cui si fa una valutazione adesso giusto per anche per Mario e Raffaele al volo, quello che hanno fatto Francesco con Mariano è prendere altri sistemi statici, altri due.

Confrontarli tra loro, confrontare il tipo di evidenze che davano sempre su quelle quattro network function.

Fare un bel minestrone tutto insieme, passarla a Nicolò che ha fatto fare un altro giro al sistema.

Tirando fuori e adesso vediamo cosa ha tirato fuori non l'ho visto, però tirando fuori qualcosa è stato verificato qualcosa no cioè di quello che avevamo diciamo di ground truth E non trovando mi sembra nuove vulnerabilità.

Esatto al momento, cioè dobbiamo un po' accertare questo quindi il filo logico potrebbe essere che questo articolo È un'estensione di quello precedente, perché introduce altri SAT prima li confronta fra loro e poi li va a mettere insieme.

Su questo io avevo un'unica domanda che almeno per logica a me sarebbe stato venuto spontaneo anche fare una specie di ablash test, ovvero noi abbiamo suona Cube singolo.

E adesso mettiamo tutti e tre e abbiamo un risultato sarebbe stato bello, ma probabilmente non si riesce a fare vedere anche gli altri singolarmente o gli altri accoppiati tra loro, però aumenta il nome di esperimenti da fare che però sarebbe questo facciamolo questo facciamolo in un journalentiamo mettiamo un paio di altre tesi a livello sperimentale ipotesi a livello sperimentale e poi le validiamo quello che stai dicendo tu è molto più interessante.

Allora, quindi qui in questo articolo si parte dall'articolo di Tripla e si affronta il problema prima di confrontare le vari di analisi statica e poi vedere se insieme con le Contribuiscono a migliorare o meno l'identificazione di vulnerabilità, sperando poi che Francesco Lorenzo mugnando un po' fra le varie segnalazioni, magari esce poi qualcos'altro.

Sì, infatti questo vogliamo vedere anche perché diciamo come dicevo l'altra volta, ci aspettiamo cambiando i tool in realtà non è che fanno le stesse cose questi tool sono tre approcci diversi disastro.

Sono proprio tre approcci diversi, noi c'eravamo su S al fiume è quello più famoso che in realtà è più debole.

Invece quello che abbiamo visto è che quello là conL è quello un po' più interessante, perché fa l'analisi non solo del simpact dello sta Quindi praticamente partendo da un punto Val il codice un po' alla volta diciamo gli i quindi si disegna il graffo.

Ma fanno cose un po' più interessante, cioè nel senso valuta anche gli input e la propagazione di quest'input all'interno del codice. Sta cosa ha generato un paio di warning, diciamo di s che sono simpatici perché ti dicono guarda in questo il tuo codice, cioè quello là il file che noi abbiamo segnalato su dietro Ci stanno praticamente danno in input dei dati che non sono sanitizzati e questi dati vanno in un altro file ti puntava addirittura un secondo file ci diceva guarda se sti dati non vengono sanitizzati qua in questo secondo file possono creare dei problemi perché vengono utilizzati senza senza essere sanitizzati dopo.

Quindi, in realtà , cioè nel senso questo è un livello di astrazione un po' più alto rispetto a quello che facevi di profondità più alto rispetto a quello che faceva.

Quindi diciamo questo ci vogliamo analizzare con calma, perché forse riusciamo cioè abbiamo il sospetto che forse riusciamo a trovare una delle merabilità della trown trop che ha più o meno questa che in realtà su Arcube non aveva per niente trovato questo sarebbe un risultato oggi e domani tanto tornato dal Giappone Lorenzo non deve dormire, quindi agli occhi e via io lascio Forse l'unica cosa che può essere ancora utile, cioè dall'altra volta praticamente poi lanciando le analisi il modello rispondeva ha risposto molto più velocemente, quindi è probabile che lato o lama con il loro modello stato hanno cambiato qualcosa. Non so se hai queste misure di tempi stanno sempre là dentro se non le trovo Dovrebbero esserci Sna Jason quelli completi Quindi volendo si può approfondi cioè dico sì volendo si può anche riprendere cioè prendere anche i test di nuovo sulle cose che avevamo già fatto, quindi solo con S Cuba e ripartire da lì lì, se Cercare perché mi hai chiesto prima di cercare le cose per fare i confronti con quello vecchio.

Quindi, nel caso si può anche dire ok abbiamo notato che è cambiato ripartiamo e queste sono le nuove con l'estensione.

Aspetta, scusami, perché allora diciamo noi tu dici nel senso di unire un po' gli esperimenti, perché ad esempio.

Noi adesso abbiamo fatto, quindi abbiamo i primi esperimenti della volta scorsa erano quelli della console Cube E abbiamo dato, diciamo, abbiamo trovato dei risultati degli in come come diceva i F E poi abbiamo rifatto totalmente questi tre non ho capito, diciamo in che senso vorresti riprendere quelli vecchi.

No, che tu mi hai detto di riprendere quelli vecchi per fare i confronti con questi nuovi, però dato che è cambiato tutto in realtà io cioè c'ho già.

Le esecuzioni vecchie fatte però col fatto che il modello risponde più più velocemente, quindi nuove.

Ma perché cosa hai cambiato rispetto adesso?

No, no, io io niente lato mio niente lato invece server di Olama probabilmente hanno fatto qualcosa. Risponde più velocemente che poi può essere semplicemente cose di server, non lo so.

Ma non considerato sta girando, cioè il modello non è lo stesso.

Sì, sì, sì teoricamente sì il nome che appare fuori sì. Che poi non so sì non so dietro cosa ma non ci sta tipo qualche info sulla release cioè se 3.33 stato un trattino basso release devo approfondire no, vedi un po' questa è una cosa vedi un po' per capire se è stato aggiornato nel tempo di sicuro ci hanno un tag Perché appunto, sennò cioè si prendono semplicemente i dati nuovi se nel caso ti servono, perché prima mi hai chiesto appunto per fare confronti.

Raga, io non vi voglio tediare perché ora è una cosa abbastanza tecnica se volete Allora facciamo così, raga, allora vi lascio un attimo e vi lascio scollegare anche così mi mi rubo un attimo Nicolò per 10 minuti ediamo un po' le cose un po' più tecniche.

E altra cosa magari diciamo giusto io volevo mostrare un po' l'articolo per capire sta ancora molto in fa lontanissimo, però almeno per capire come muoverci.

Visto che stiamo dicendo che questo citerà l'altro e non sarà una copia con diciamo una gita. Una domanda è proprio diciamo banale, ma hai materiale per scrivere un articolo perché alla fine diciamo stiamo ripetendo l'articolo vecchio a cui aggiungiamo diciamo dei componenti Infatti diciamo questa è un po' la cosa che dicevo volevo dire ad Andrea allora in realtà, cioè secondo me, se vogliamo fare un articolo proprio da zero un materiale, c'è molto poco Io stesso domanda nasce da questo timore.

Secondo me dovremmo inglobare quello vecchio, anche perché lo possiamo fare perché siamo sui è una conferenza abbastanza particolare.

Ma è una diciamo prassi o è una cosa dal punto di vista di regolamento accettata?

E allora guarda, in realtà Itasek è molto una zona grigia nel senso che non è come i regoli, nel senso tipo ti suggerisce anche di sottomettere articoli già pubblicati in altre Quindi, in sostanza, diciamo tutti quelli che vengono che pubblicano a Ida, è un articolo già pubblica da un'altra parte leggermente allungato. E quindi cadrebbe esattamente, cioè il fatto di raggiungere componenti in più e Verificare cosa cambia e usare gran parte dell'altro articolo dienterebbe esattamente questa.

Esatto, cioè se questo era tipo un articolo dei tre vo oppure un giornale dice ora che non ci abbiamo tempo.

Però, dato che Isec è appunto questa zona grigia che è una convention tutta italiana sulla sicurezza che è +1 cosa di press quindi diciamo tecnica ma fino a un certo punto. Secondo me possiamo un po' spingerci sul riprendere a piene mani quell'articolo abbiamo detto loro ti suggeriscono anche dice presenti qualcosa di nuovo oppure fai un vecchio articolo per farlo conoscere.

E questa cosa va dichiarata?

Questa l'ho detto è sempre una zona critica, perché lui c'ha queste due track.

Però diciamo nel senso di si parla appunto extension cose cioè pure la col for paper è molto famosa.

Tant'è vero che ti ho detto le altre le altre volte vedendo pure i lavori di altre persone sono lavori vecchi un po' più allungati, cioè diciamo non è proprio l'estensione più ho ripreso quel lavoro e ci ho fatto un delta vicino, quello che vogliamo fare.

Capito.

Quindi, in sostanza, dobbiamo modificarlo perché non possiamo veramente fare una copia copiarella, però.

Nel senso mi aspetto che sia una sorta di quello però allunga.

Più alto altro, quello che volevo modificare era un po' anche la descrizione dell'architettura, perché c'avevo un po' di dubbi per Diego.

E forse può essere l'occasione buona per descriverla un po' meglio, perché secondo me qua siamo stati comunque abbastanza sintetici. Magari c'è una cosa che possiamo fare è dare un po' più spazio all'implementazione nel senso come sono stati costruiti modelli e che qua personalmente leggendomi gli articoli mi sono segnato un paio di dubbi che non tornavo un po' di cose.

Da da lettore esterno, quindi diciamo possiamo un po' estendere questo su questo infatti diciamo forse una mano che potete dare voi ragazzi se volete partecipare. Sta parte di diciamo il ration dell'architettura architection perché al momento ho creato la sezione però la deadline giovedì prossimo giovedì prossimo di estensione non ce ne sono estensione senti, visto che tu sei il padrone dell'overleaf attaccare le parti in cui hai bisogno di supporto magari chi se ne prende in carico ci aggiunge diciamo suo.

Ok, allora in sostanza giusto per scorrerlo così poi ti faccio freccia grazie a Dio allora prendete la struttura Posso lavorarci solamente martedì 27 dalle dalle due alle 4, quindi mi prendo prendo in carico la parte dell'architettura devi inserire nell'over aggiunto il l'ho passato a Ad Andrea ci sei c'hai il penning by adesso vado a vedere subito.

Allora, come si chiama la cosa?

Momento TBD è Static Analsis sezione architettura.

Ah sì sì, no la sezione te la dico io System architection la quarta.

C'hai proprio un file dedicato.

Ok. Questo tempte c'ha il file separando nel capito.

Guarda in sostanza, alla fine l'archivio, cioè per mo la struttura che ho buttato giù è molto simile a quella là che già c'è. In sostanza abbiamo il related work che stavo scrivendo che un po' riprende quello là che già avevamo gli avevamo aggiunto solo un po' la parte disast.

Contribution gli ho aggiunto praticamente sono quelli ripresi ma non po' limati però gli ho aggiunto uno nuovo.

Che praticamente il fatto del multim metogiy, quindi se praticamente noi incorporiamo tre metodologie disastre diverse Diciamo questa è un po' la no di questa cosa la system architecture che è la stessa, cioè nel senso l'abbiamo allungato un po' poi vabbè, la parte dei dischi con la discussione questa un po' adesso mi metto a scrivere un po' questo Ma quindi è proprio l'articolo è quello di Ica esatto Sì, no esatto diciamo abbiamo preso partiamo da questo come idea, quello vecchio di Ica è lunga Call for paper, aspetta volevo un attimo vedere quant'era la dimensione massima ma era tipo un numero abbastanza grande.

No, il numero di Perché alla fine, cioè sono sono un po' più informativi che Ah, 16 pagine, però una colonna +4 di appendice, quindi siamo proprio morbidi. Quello di invece quanto Doppia colonna.

Quindi 10 12.

Come vi dicevo in realtà loro chiedono original un publishid contribution, però come dicevo alla fine le barriere all'ingresso sono molto morbide.

Quindi possiamo un po' usare su una sortaorta di paper già fatto più.

Più nostra estensione.

O addirittura, ad esempio, come dicevo, vi dicevo, puoi anche pubblicare un paper già fatto che lo mettono nei loro Le loro pros.

Quindi in teoria proprio alle brutte potremmo anche richiedere il rati di questo paper così com'è, però in realtà una soluzione un po' un po' così perché sta su un'altra track.

Non so se non va nei prosieding, ah no publish work Però diciamo, non non so perché non passanno i posti profili adesso no questo cosa significasse ai livelli sul passare dei post pro che sono stati già pubblicati provano a pubblicarli dei loro profili fanno un culo così.

A livello proprio di editoria.

No, questo sì è chiaro no dico non so però loro come cioè il senso del del mandaregli un paper già fatto, cioè nel senso loro se comunque come lo espongono verso l'esterno, mi ricordo.

Sempre su Seur, se non sbaglio, loro hanno tipo.

Una sorta di track di proseeding di una conferenza diciamo è come se loro facessero pubblicità a questi articoli. Citano gli articoli sono passati in conferenza.

Sì, Diciamo se non sbaglio, alle brutte c'è solo sta cosa se non sbaglio per la vecchia convenzione cioè la vecchia edizione. Li hanno messi da qualche parte. Giovedì è il giorno di consegna hai detto giusto?

30 spostato è la prima 29 e poi fatto un'estensione di un giorno è stata fantastica Che nella mail era 29 Senti, invece altra domanda Provate a chiedere esplicitamente supporto.

Sul sulle sezioni che pensi di non riuscire a curare, perché poi diciamo ti stai concentrando su questi altri sistemi da sperimentare ovviamente sono quelli su cui avrai il focus.

Quindi diciamo l'architettura prova a guardarla Mario io e Nicolò che cosa potremmo Quali parti potranno provare a popolare?

Io penso che la pipeline possa essere interessante per Nicolò che c'era sotto Sott'occhio tutto il tempo e quindi quella.

Sì, infatti raga, a me più altro serve la parte di capitolo quattro, perché secondo me è quello che possiamo estendere meglio.

Perché poi il resto lo use case su questo magari scoccia anche un po' Nico, però mi dà una mano a Lorenzo che c' lavorato scorsa e sui risultati quella la scrivo. Le altre parti No, perché le altre parti sì alla fine se vedete l'intro del work e sono più o meno le stessealtra volta allungate.

Contribution è questo prezzo come un altro, cioè nel senso lasciamo nel momento così gli altri sono sistema architecture cos'è su questo ci possiamo scrivere.

Questo magari più altro raffo, adesso buttiamo giù una bozza pure su questo se ci dà una mano più altro racconta la c'è un po' a forma anche di mare e te Va bene, mi tighi te quando posso darci un?

Sì, sì, sì, perché oggi sto a scrivere appena ci abbiamo qualcosa, allora dacci una mano a un po' rileggere 5 Adesso ci mettiamo su sti due che buttate giù una do una mano Ok, allora muovita.

Allora, quindi esiste marchitection.

Al momento qua.

Ti segno qua, ma estrema sicurezza stiamo parlando che questo è un follow-up del static analisy Guy agenti che l'M vulnerabili di Discovery in F 5G giusto?

Esatto.

Nico, se c'hai un attimo, buttagli un'occhiata pure tu alla fine, ok?

Sì, sulla parte dell'architettura no?

Sì,mente ok.

Invece noi abbiamo detto un 56 ce ne occupiamo di Beh, a questo punto dico potrebbero diventare tre citazioni degli articoli.

Quindi piatti pronto a modificare l'appstrat Almeno in la puoi mettere come sottomesso anche per una terza conferenza in attesa di bla Ok, allora noi siamo ancora.

Noi siamo a posto, no?

Sì, sì, sì, no su questo siamo a posto.

Ho detto se lasciatemi solo un po' la carta aperta che voglio chiedere un po' di infamico sui risultati.

Andrea Va bene, allora appena c'ho qualche hit possiamo spostarci su un'altra che ti voglio chiedere una cosa?

Sì, ti do un url qui in chat così poi loro se vogliono si collegano e fanno.

Meet boombing entrano ci prendono male parole e poi scappano se no ci spostiamo io e Nico, no tranquilli restate qua noi ci Ci vediamo ciao ciao ciao ciao Guarda Nico ho detto mi serve più alto una mano per capire perché mi sono un po' confrontato con Lorenzo, poi magari lo segnalo lo sentiamo un attimo nei prossimi giorni quando ci sta.

Allora guarda, ci abbiamo i dubbi sono un po' questi cioè nel senso quello che vogliamo fare adesso. È un po' capire un po' che sta a parte i risultati, quindi il confronto tre punti.

Uno è il confronto con con la quindi diciamo quanto ci hanno trovato.

Due un po' le performance operative, come ti dicevo, perché sono uniche cose che possiamo fare quindi nel senso quante volte la trova se trova qualche novità cioè se trovo qualcosa di utile, quante volte lo trova ad esempio se bastano più repedition o di meno.

E a sto punto anche i tempi operativi che poteva essere uti cosa un attimo se c'hai cerca un po' di capire se magari ma non so che sistema stai usando, però non ho capito cosa stai girando.

E su sui loro server praticamente perché sto usando Gemma 31 B. E praticamente ho fatto loro e ti permettono di crearti la tua con col profilo hai dei crediti che si resettano mensilmente, tipo settimanalmente mensilmente.

E quindi praticamente semplicemente ho la piki che mi se salvo nel codice e poi fa le richieste lì.

Ho capito quindi sì ottengo un Jason io cerco di salvare il più possibile, però Tipo i ragionamenti poi ragionamento è una cosa che non non ti non ti danno.

Il thinking d'interno sì infatti io li faccio sempre gli chiedo sempre il ragionamento poi nell'output.

Che non è come il thinking, ma è una versione diciamo elaborata Di di spiegazione, quindi qualcosa ecco si riesce poi sempre a prendere dall'output.

Ok, però sta cosa se c'è veramente tre secondi pure per la tesi ti può servire, cioè nel senso cerca di capire se loro hanno cambiato una versione sì, questo sì sì devo approfondire un attimo Vedi un po' sicuramente qualche log loro che dicono cioè nel senso in che momento fanno l'app delle versioni con le performance con le cose così pure questo io con il tre nella p altra cosa stavo un po' a vedere a parte che la volta scorsa non l'ho seguito veramente poco quindi ho un bel po' di dubbi allora praticamente abbiamo più altro ci siamo presi. Non lo so Mario ci siamo presi quello là che i due file con con l'estensione, quella che avevi chiamato tu praticamente con i file aggiunti. File collegato e qual era la differenza tra tre tool e tre tool più file collegati perché tu qua spieghi un attimo tu perché ho finito ho capito male Sì, no era semplice semplicemente l'ultimo c'era uno dei tre tool che agganciava anche il pezzo di codice dell'altro file.

Ah e nella prima run che appunto io ero partito subito appena dato il materiale.

E aveva escluso quei pezzi di codice, perché essendo legati a un altro file. Per il fatto che appunto lui non ha il contesto del l'altro file perché non ce l'ha l'altro file quando fa il ragionamento.

Allora li aveva esclusi poi dopo che appunto in chat ne abbiamo parlato e tutto glieli ho fatti aggiungere, mettendo nel prompt che appunto è un contesto di un altro file, ma che non hai accesso a quel file.

Quindi sì, diciamo la parte più completa è quella lì con i file collegati, sì.

Ok, quindi anche questo può essere diciamo la sorta possiamo raccontarla se ci sono delle differenze.

E tu Giulia avevi già trovato delle differenze tra tra questo e questo quindi tra tra i tool e tre tool lo fai Ma io l'unica cosa che ho guardato è la tabellina sotto quella dove ti ho mandato la foto foto se scendi.

Cioè, non non non ho approfondito più di tanto come sono fermato a fare e fornire, anche perché l'altra volta è stato più o meno quello il flusso di lavoro nel senso che ho fatto le cose. Me le ho passate e poi in realtà l'altro problema è che poi quando hanno fatto il paper io non c'ero.

E quindi non non so bene poi cosa hanno fatto se hanno toccato poi dei dati e roba come li hanno sistemate.

Quindi, in realtà su quello sono un attimo.

Però detto questo, allora a leggere.

Sì, aumentava solo la precisione, diciamo perché appunto c'è la prima run che è la prima riga che è quella solo che gli passa i file.

E il modello sa che appunto è un agente che deve trovare le vulnerabilità e quindi ricerca così. Invece poi c'è quella con i tre tool, ma senza il pezzo attaccato e poi invece quella con i tre tool è con il file col contesto, cioè.

Sa che un altro file appunto non ha l'altro file, ma sa che quel codice che gli arriva anche dell'altro file.

Sì, aumenta la precisione nel senso che c'è meno rumore.

Senti, qual è la differenza sei questa qua 56 sono quella della dell'inizio 10 non mi Sì, perché sono dovrebbero essere devo controllare, però dovrebbero essere i Cioè, su su come conta lui i true positive forse negative Prova a chiederglielo un attimo, perché non mi ricordo più.

Senti, facciamo una cosa se c'hai veramente altri 10 minuti, io mo vedo se ci sta pure Lorenzo se è finito. Magari lo aggiungiamo un attimo ci almeno così ti abbiamo le palle una a volte per bene.

Sì, sì, no, no va bene almeno così poi sappiamo che Sì, anche perché in realtà caso vuole che oggi pomeriggio parto. E torno lunedì vado a Barcellona con mio fratello.

Sparisco e riappaio poi lunedì tanto cos'era il venerdì lide no hai detto giovedì.

Torno lunedì, sì sì.

Quindi, poi, nel caso, appunto Ok, si ha detto che se sta Ti mando allora ti mando un attimo il link così.

Ah 10 sono le corse sì, perché ho fatto 10 run per con almeno due quindi ha fatto sto check su sto parametro, quindi tre su 6 3 maggiore di uno quindi ha segnato la corsa penso che abbia fatto una cosa del genere. Cibo che c'era ha detto sì tutte e tre e l'hanno trovata in tutte e tre le cose Sì, corse con almeno una C 50 robe La versione è 421 5G Penso di sì, non lo so perché.

Tutti sti dettagli non li controllo in realtà, quindi cado un po' Sì, il mio problema è che sono abituato a fare le cose, cioè ti può prendere e fare le cose non sono abituato molto poi a razionalizzare tutto.

No, devi tenere una sorta di diario che impazzisce E lo sto notando adesso se se decidi di fare il dottorato ci sono passato a volte almeno 20% del tempo 30 lo passi solo da ordinariamente Ha detto ci raggiunge tra poco. Senti allora no tornando un attimo a noi che più altro ho detto cioè cominciamo a fare Lorenzo sta un po' più avanti. Giustamente io mi ho un po' di dubbi proprio pesanti.

Allora più altro il fatto è che allora una domanda che ti volevo fare perché tre ripetizione e un altro 10. Sull'DR ne fatte 10 sul DM3 Non lo so io ti devi essere costante se fai un'analisi cioè devi decidere un parametro è quello Sto cercando adesso di riprendere in mano un discorso perché Dai che se se lo piena tre articoli, mannaggia.

Cioè, dov'è che dice dov'era la roba?

Hai detto che in alcuni casi fa No, il fatto delle delle retitions cioè tu praticamente su questo qua hai fatto tre repetitions che è il cacchio.

L'UDMUDM sono tre repetitions mentre invece l'UDR Ciao, buongiorno.

Oh ciao Lollo.

C'è qui Nico, quindi riempiamolo di domande tartassiamolo prima che scappa.

No, non ho grandi domande, però se più altro Eh no, ragioniamoci un po' a così stiamo che pure ha detto a me mancano i pezzi lo dobbiamo scrivere. Innanzitutto, adesso stavo vedendo perché uno c'ha 10 ripetizioni soltanto tre.

E questo come l'altra volta immagino sia stato un caso.

Se sto controllando, perché i report Non li tocco la da veramente troppo, allora.

Allora questo Che quella sezione delle ripetizioni era era qualcosa legato.

Perché non è la stessa, non sono le stesse cose, vero?

Cioè c'è diverso.

No, perché secondo me era una roba che faceva perché appunto lui fa più run.

Nelle più run ogni volta prima matcha quelli che che trova nella ground truth e poi dopo.

Tutti gli altri li segna come nuovi findings e però faceva una parte di semantica che provava comunque ad associarli a renderli uguali, quindi capire un attimo però non so se è quello.

Più che altro lì c'è il controllo delle ripetition è un parametro che tu gli metti lo decide lui io immagino le repetition siano le varie runner repetition su due cose diverse.

Il numero di run è fisso perché magari lo scegli tu le repetition sono quante volte lui ti segegue di nuovo questo flusso.

Sì, sì, se sono le run esatto sì quante volte lo segue me lo sto immaginare come le run sono tutte le volte che tu gli dai di nuovo l'input e lì si fa tutta dal giro Le ripetitition quando una volta l'LLM agent fa praticamente questo cerchio e vedrai Sì, sì, il numero standard è tre.

Nel senso che appunto fa tre corse.

Sì, diciamo che ogni volta che c'è un numero maggiore, è vero, questo era già successo l'altra volta ogni volta che c'è un numero maggiore di corse è perché in quel.

Per quel file lì. Non è schiacciante il numero di di findings che trova, quindi magari in una run c'è un numero di findings in più in un altro o in meno.

E allora, per cercare di tirar fuori una consistenza maggiore fa più run e quindi lo alza poi a 10.

E però questa cosa c'è nel senso che questa non è una cosa che forzi tu, cioè nel senso che dici io gli faccio una run.

È una run è tutta un insieme di iterazione, cioè nel senso è tutto il flusso da qui a qui.

Così me lo immagino, nel senso io faccio un'ora la vita degli output e lui internamente fa delle rip nel senso fa sto loop n volte magari n massimo gli settato tutto da qualche parte no che se sei palla lo fa 1000 volte magari N5 E poi le magari io la stessa cosa gli dico però tutta la catena sto giochetto che hai fatto da tasca giù fammelo No, però aspetta tu adesso intendevi dei dei ritra interni lì nel Sytac structure perché No, no partiamo da che non mi è chiaro me il concetto a differenza tra run e Repetition.

Cioè, nel senso quando lui negli altri dice ho fatto 10 repetition in sostanza lui che ha fatto a livello proprio di flusso.

La ripetiti da quello che mi ricordavo io poi correggimi se sbaglio Nicolò era soltanto il fatto che tu per una questione pure deterministica dell'LM gliela ripassavi più volte, cioè Gli input che riceve che l'input diciamo della della cosa dell'analisi statica del codice io ripassavi più volte all'M producendo più output e quindi più rap.

Cosa che all'inizio facevamo a tre poi tu per alcuni hai fatta a 10 perché come dicevi tu, magari ti dava più finding diverso e quindi per una questione pure di omogeneità di coerenza lamentavi a 10, ma io comunque l'ho analizzati, cioè alla fine sono sempre quelle, quindi diciamo che siano tre o 10 a volte non è che sia cambiato chissà quanto che più che altro loro bisogna capire un po', cioè nel senso noi qua ci abbiamo dei risultati ok praticamente gli abbiamo detto un po' a parte i falsi positivi e le cose negative l'unica cosa che possiamo fare anche perché cioè ad occhio mi sembra che più grandi stra Allora, io l'ho finito analizzare ci dovrebbero essere due finding nuove sull'UDM e due funding 9 sull'DR Ok, già questo è ottimo però le devo controllare per capire se sono vulnerabilità a bere, perché poi effettivamente, cioè a volte ci sono insomma i Ma tu come le confrontate, cioè confrontati rispetto ai vecchi?

Allora io ho preso nella prima analisi che ho finito ho preso tutte le cose che già avevamo trovato sia dei miei CVE, cioè sia le CV vecchie che usavamo come ground Tue, sia le CVE nuove cioè CV ancora non proprio però comunque unerabilità trovate. E queste le ho scartate, cioè le ho le ho prese ho scritto questa l'avevamo già trovate, quindi. Cioè lo vedi tutto nel file nuovo che ti ho mandato CV nuovisec e poi ce ne stanno di tutte quelle là che già avevamo visto ce ne sono quattro nuove che nessuno aveva mai visto mai provato.

Però, ovviamente, non so ancora se sono vulnerabilità potrebbero essere stronzate, capito allucinazioni cose quattro intendi solo adesso di queste run nuove Isec per capirci di Isec sono solo quattro quelle finding nuove della roba che avevamo portato cioè perché la PC FMF l'abbiamo scattate non ho capito bene perché però perché non ha trovato nulla immagino eh no perché sono chi quella ok invece delDR eDM ce ne sono due nuove a testa ora le stavo cercando di finire per capire se sono veramente vulnerabilità le stavo testando sul Free file No più altro giusto per capirci un attimo perché poi ti ho detto dopo dobbiamo un attimo raccontare. Tu adesso gli hai dato come outp, cioè gli l' output questo qua di Nico e confrontato con immagino concde con qualcuno di questi gli ha dato in input, però l'altro input che gli dà cioè nel senso verifica se sono se ci sono dei dei punti uguali con con che fatto a mano l'ho fatto Io ho preso innanzitutto le rap e ho eliminato i doppioni i duplicati perché ovviamente dava sempre duplicato.

Quindi poi della della parte dell'UDM prendo della parte delle Alla fine ho trovato una 2, 5 findings nel DM cosa ti lascio lo schermo secondo Ah comunque la versione 421 te l'ho scritto.

Ok, vabbè sulla 422 Allora questa parte qua delle run repetition è un po'' incasinata perché era.

Sì, era tutto nato con la questione di quello di dire io lancio una run in questa run vado a ripetere la la stessa esecuzione con un numero fisso di tre volte, appunto per vedere se le cose combaciano.

E poi c'era appunto la la roba, come hai detto prima di se voglio approfondire invece maggiormente . Un caso specifico di un file, posso alzare il numero di ripetizioni nei report, però cosa succede che durante le run può accadere che come mi è accaduto in realtà che molto spesso magari o lama si blocca oppure il mio PC si interrompe, cioè possono succedere dei casi per cui la l'esecuzione non va completa.

E qui si interrompe e quindi anche per riprendere il flusso.

Poi riparte e diciamo che nel questa cosa qua mi è servita a me per semplificarmi la vita lato codice nel far funzionare il codice.

Però, al lato invece di report, poi queste cose vengono riportate in maniera un po' ambigua nel senso che ti riporta il numero di ram il numero di .

Di ripetizioni un po'' così dovrei un attimo formalizzare meglio come escono i compiti a casa esatto Perché pure per la tesi, capì nel senso ti faranno sicuramente domande sul tuo agente, cioè nel senso quante volte fate delle violazioni, qual è il patto che segue sicuro se pure io a mostrare architettura come quella dell' dell'articolo, penso che è una cosa del genere gli dovrei mostrare.

Quindi dicono sì, ok, però come raccontami sto patto traversa, cioè che fa nel senso sì ok però quante ripetizioni hanno fatto.

Perché cosa che triggera Ste ripetizioni, cioè perché sì, abbiamo capito che deve fare il ramblick Lubrick e già però nel senso gli devi un attimo raccontare un po' più nei dettagli e questa è un po' la cosa infatti mi ero segnato parentesi sull'articolo Cioè, nel senso un po'' per capirmi nel senso è un po'' fumosa sta cosa pure qua, cioè nel senso va un attimo spiegata quali sono un po' i casi che triggano bene non retrai.

Cioè, oltre a dice sì ok non si confronta con la ground root se invece non non gli è piaciuto per dei KPI ok.

Sì va bene, però nel senso va un attimo contestualizzato a me che nel senso che non ha mai visto cioè per me praticamente.

Arriva sto verifi me lo retrai però diciamo perché così ha deci deciso è un po' spiegata così invece un attimo capito quante retrai fa cioè se c'è un limite a sto retri Ste cose qua.

Quindi sì, nel senso studiato era un attimo meglio che poi questo ci serve anche per scrivere l'architettura dovrei dare una mano a Mario De Zos.

Sì Sì, più che altro perché appunto questo era nato come esperimento buttato lì, no?

E poi dopo ha preso effettivamente valore, quindi ci sono è sempre così sono Cioè adesso sul CDT sono partito un po' più pronto infatti sto provando a fare già la documentazione e tutto questo l'avevo poi proprio dimenticato.

Quindi adesso magari provo a Sì, solo che io c'ho solo 12 minuti alla tesi, quindi non so cioè io boh Sono cucinato, cioè gli devo dire le cose in maniera super generica veloce e poi sì, dipende poi le domande che mi fanno.

Ma guarda in realtà 10 minuti poi capirai che sono sufficiente non gli devi raccontare tutto, però gli devi mostrare delle immagini e gliele devi commentare.

Questo alla fine farai 12 minuti fa nel senso appunto, dato che mi mostri le immagini, cioè nel senso devi essere loro ti fanno le domande su questo tu gli mostri una roba del genere ti ho detto che domande più o meno ti fanno devi essere pupare se no ci cazzo questa è l'unica cosa a cui devi stare attento. Perché se gli mostri un'immagine a tuo un grafico operativo come questo loro non ti stanno a sentire guardano questo e dicono ah ok fa delle mi spieghi meglio qual è la sintasse perché le fa quante ripetizioni ti ha dato.

Hai fatto delle iterazioni come si è comportato il sistema cioè allora queste sonopiscono il 20% di quello più alto le immagini. Quindi sta attenta alle immagini che metti anzi questa qua perciò gli sta a fare la testa così perché questa la dobbiamo sistemare secondo me è qualcosa che non va.

Quindi c'è due tre punti che non so chiare sistemiamola bene e poi due la schiatti nella tesi così come sta Vabbè dai Lollo, scusami ti ho un attimo.

No, se avete appunto dei feedback così adesso poi ci ragiono un attimo perché devo riprendere in mano il progetto in realtà.

Il 4 dicembre è la proclamazione, quindi in realtà la discussione è a fine novembre.

Ah, sono preparate.

Sì, sì, sì, sì, perché al poli siamo talmente tanti lì Vabbè, ti stai tranquillo ma guarda i suggerimenti sono sempre gli stessi dell'altra volta cioè la cosa che forse più cambierei è il fatto che nelle rap ci siano sempre duplicati, forse fare tipo una cosa in più in cui Poi un'altra cosa che tipo c'è ancora è che quando poi clicchi su The Tales mi pare insa, sì secondo quando si giù the tailatto tipo che ne so, c'è match atfdings e tu clicchi to the tails e poi sotto ti dà il il reasoning.

Ti dà una serie di poi di vulnerabilità che sono miste invece non mi mi dovrebbe da solo una sola di quelle là che poi cioè quella che ho cliccato mi dovrebbe dare invece me le da tutte è un'altra cosa sicuramente però vabbè poi è forse giusto più per una cosa No, se ci sono migliorie, ditevele pure perché alla fine l'avete usato più voi come output, quindi.

Prevalentemente queste due a me poi se ne vengono a vedere sì ho detto fix sta cosa delle rap Sì, da formalizzarla meglio anche nei report.

Sì, mi da mettere fissa forse cinque magari.

L'importante è che la rendi esplicable, cioè se uno dice, ma perché tre rap perché così È meglio un perché ho deciso così che è un perché non lo so hai deciso cinque direi che cinque sono sufficienti anche per una questione statistica di performance ok allora guarda, ti stavo ti stavo chiedendo quindi praticamente LOL giusto per allinearci sulle cose fatte, quindi allora ti sei un attimo confrontate con le vulnerabilità, quelle là totali, quindi sia la ground frutto sia quelle nuove trovate con la Sì, allora aspetta preferiamo sulla base innanzitutto di tutte quelle là dell'output dita secca chiamiamolo così che Nicolò ha chiamato St tre tool Rketfull per UDM e per UDR quello che avete mandato su Gmail, ok?

Quello muovi bene come si chiama allora UDR tre tool più file collegati UDM tre tool più file collegati io quei due l'ho preso.

Perfetto. Di questi nell'UDM filtrando ha trovato in totale una 2 3 4 e 5 finding.

Di queste cinque una era la CVE della Grand Tru.

Due sono nuove, ma le devo vedere, quindi non non vedo Dio più di questo per ora.

Sono sicuramente nuove, però devo capire se sono delle abilità affettive.

Poi una di quelle che abbiamo trovato e quindi che ancora c'è nell'articolo che è ancora non ha CVE.

E l'altra pure era un'altra di quelle nuove. Cioè quindi vecchie che da da questo dal nostro punto di vista attuale vecchie e solo due sono nuove per l'UDR sono invece una 7 finds di cui cinque sono vecchi.

Molte erano delle CV proprio quelle della Grand True e due sono due dei findings che devo un attimo vedere voi questi.

Ma potete vedere due sono uguali, proprio Loggjection c'era pure qua. Che vince una pure l'altra Quindi magari sono cazzate probabili. Questo è interessante, ma secondo me non è applicabile praticamente. Non si sa per quale motivo passa da 64 32 senza controllare. Sì, lo stavo vedendo E pure questa interessante sta qua.

Sempre quelle cose di validation del su in realtà questa è molto simile a una che già avevamo trovato, però sono andato a vedere un po' nel dettaglio in realtà è un po' diverso vabbè. Possiamo considerare diversa. Non è non è è un punto diverso.

Quindi vabbè, mo vi faccio sapere. Dobbiamo capire sta cosa dell'articolo che cazzo raccontare e allora stavamo a vedere il fatto.

Questa non so se l'avrei fatto tu Andrea fatto dei falsi positivi, Ste cose qua al momento abbiamo il vecchio articolo c'aveva una.

Una stima dei falsi positivi l'ho fatta io ok, ottimo e allora dobbiamo una cosa del genere così almeno la confrontiamo con i risultati e dire ok gigendo tre st si riducono aumentano i falsi positivi o queste cose qua.

Scusami, nel nel coso di Idasek c'è nel nel parlato di quello che si scriveva nell'articolo. Farà si userà come base il vecchio articolo o quello non viene proprio preso in considerazione e si riparte da zero questo non ho capito. Questo ne abbiamo parlato prima in realtà nel senso io personalmente vorrei proprio considerare quell'articolo, diciamo nel senso magari lo citiamo pure. Però lo riprendi, cioè è come se ne facessimo tipo una sorta di versione estesa di quello là quindi ho dei falsi positivi ti devo prendere quelli vecchi e ti devo dire più due o devo fare proprio più o devo scrivere soltanto due falsi No, no, dobbiamo confrontiamolo con quello che abbiamo capito.

Nel senso che diciamo gli facciamo il confronto, cioè nel senso noi.

Tipo l'articolo vecchio, no ti mostro giusto il secondo lo schermo video per farti capire come possiamo agitato che sono poche cose dobbiamo un po' giocare atuzio. Noi abbiamo questo, cioè in sostanza a parte le abbiamo trovate, ma questo se troviamo qualcosa gli aggiungiamo abbiamo questa.

Che è la tabella delle statistiche, quindi falsi negativi, la precisione, il regola e cazzi.

Una cosa che possiamo fare noi adesso abbiamo messo no int e no faremo un'altra cosa e diremo no hit un st tre st quindi aggiungiamo una riga ogni ogni cosa di questo in sostanza due diciamo non cambia un cazzo a questi due vediamo se cambia qualcosa.

Ma quegli acronimi sanno spiegare da qualche parte che nonorta mi ricordo PP che cos'è?

Tr positi ok la faccio io non ti preoccupare.

Grazie.

Almeno così decidiamo un attimo cosa mettere i risultati allora al momento quindi abbiamo se troviamo una pi nuova è ok gli diciamo che abbiamo trovato già dei fans diversi o quella la faccio io vabbè faccio i confronti converti il risultato e la cosa terza parte questa cosa qua della stabile delle statistiche entriamo fuori qualche altro risultato penso basta perché alla fine qua già dentro qua ci mettiamo non solo quante ne abbiamo trovati, ma pure falsi positivi la precision.

Queste poi nel senso una volta ci proprio i dati ce le calcoliamo è già qualcosa in più. Che ti volevo dire.

In realtà Andrea aveva suggerito il fatto di fare gli ablation studies, però questo ride tempo Sono praticamente che tu quando passi da uno stato uno stato in questo caso, siamo passati da un st a tre st in teoria una cosa che ti possono chiedere di sì ok però in realtà ti si salta tutti gli stati intermedi cioè dovresti far vedere il sistema come cambia qui ad un st sono a Cube dovresti fare una run con altro sS, una run conQL una run con l'altro SAS in gretto E poi la run con tutti, così per dire guarda ha senso fare una run con tutti e tre oppure bastava che ne so scegliere meglio il SAS questo dovrebbe essere risultato finale che poi dici. Alla fine gli dovresti far vedere guarda se io che ne so daranno con sono a Cube ottengo risultati sette risultati validi.

La run con quella ne trovo altri due la run con quell'altro ne trovo nessuno se laranno con tutte e tre trova la somma di tutte e tre oppure ne trovo uno in più meno e quindi in teoria poi poi ci ricami su e dici guarda è meglio Dati i risultati è meglio che le fai le run singole è meglio che fai una run tutti insieme guarda non serve un cazzo fare la run tutti e tre insieme capisci Ste cose qua.

Però il problema è che dovremmo fare altre run e mo sinceramente penso che abbiamo il manco tu Nico.

Ma allora, fare le run ripeto, tanto se cioè dipende poi se vi interessano solo i numeri finali da mettere in tabella o.

O se bisogna poi valutare anche le cose che escono, perché i numeri in tabella, penso che il numero il problema è il lavoro che che sta a fare Lorenzo è pure le palle immagino Non lo so allora per me va bene pure così visti i tempi sì si può anche tenere così sì no va bene così voglio dire ma che cazzo Cioè, io assumerei come lavoro anche il background, cioè nel senso è un'estensione e non è che deve essere solo l'estensione in sé la Io infatti voglio, cioè io la mettere così, cioè nel senso Gli segnaliamo questo articolo gli mettiamo pure tra i citati e dicevo guarda, abbiamo lavorato.

Questa è un'estensione una ridizione di quel lavoro mi invento io non hanno qualche cazzata dai non ti preoccupare. Vabbè dai raga allora cose da fare Candi perché cinque forse cambi intende quelli veri Forse quella là che quelle nuove.

Quelle oltre la la gran Ah sì, c'è la nota sotto Ah sì, sono nuovi E nuove?

Vabbè, quindi giusto raga, come stiamo a chiuderci i compiti allora l'architettura, quindi la parte questo articolo.

Allora, Lorenzo, tu tu fai sta cosa di Finings e ce lo guardiamo insieme e sto qua.

Tu Nico ho detto dai una mano alle zosce da parte della dell'architettura, perché ci stanno un po' di cioè leggiti anche il te perché ho detto ci sono un po' di cose che non non mi suonano più altro l'execution Pipeline. Perché questa dobbiamo qua dobbiamo scrivere la cosa tutta fatta bene cioè questo sarebbe proprio il pezzo che tu prendi e metti nella tesi ok Quindi l'architettura tutti i pezzi io adesso mo metto la parte delle use case tranquillo lo racconto la ground rotta e qua Lollo magari ti scoccerà un po' qualche dettaglio l'analisi dei disastro la metto io e poi facciamo l'e valuation pure io mi dai una mano tu Lollo ti chiedono un po' dopo analisi dei risultati e poi li scriviamo bene. E basta, cioè nel senso e basta poi ha detto Raffaele si vede un po' tutta la forma e basta Questo file è condiviso il file l'overf Non mi ricordo la me perché con la mente sì, perché ci sono stati problemi con la med del poli devo vedere un attimo.

Che era era andata giù, aspetta vediamo un attimo Mi sa che anche oggi È una cosa per LOL, tu questi qua i nuovi funding le prodiy avranno tipo nell'LM per vedere se ti dava qualcosa ho detto che ti ha detto qualcosa sto un attimo sicuramente lo sto facendo di chat però per forza ancora non l'ho consultato bene purtroppo c'è la mail ancora giù del politecnico non riesco a non mi arriva nulla vabbè vediamo poi tanto mi mi collegherò poi da lunedì ecco.

Ma sì, ti ho detto i compiti a casa questa cosa dell'architettura Più che altro, se ti serve una mano pure a rivedere il lupo ho detto ma non mi tolano dagli un'occhiata e magari la descriviamo insieme Va bene.

Va bene, allora queste allora ci ci aggiorniamo in chat a stretto ok ok.

Va bene, belli ciao ciao ciao ciao.

Buona giornata.

Ciao buona giornata.
