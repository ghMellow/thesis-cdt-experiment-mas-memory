# 01 — Fattibilità pratica: cosa servirebbe per implementarlo, e inghippi [sessione: 2026-08-04]

> Segue [00_call15_notazione_semantica_esplicita_2026-07-29.md](00_call15_notazione_semantica_esplicita_2026-07-29.md). Analisi di fattibilità, non implementazione: nessun codice toccato da questo documento.

## I passi pratici, in ordine

1. **Costruire l'ontologia** (lavoro di dominio, non di codice): nodi/concetti (es. `Vulnerability`, `HandlerFunction`, `CWEClass`, `ImpactType`, `NetworkFunction`, `CVSSMetric`), relazioni tipizzate (`exposes`, `requiresPrivilege`, `impacts`, `conflictsWith`), vincoli (es. "una CWE-89 non può avere `VC:N/VI:N/VA:N`"). Lavoro assegnato a Mario+Francesco in call 15, non ancora consegnato.
2. **Scegliere la rappresentazione e il motore di query**: OWL/RDF + SPARQL (`owlready2`, `rdflib`) è lo standard accademico ma pesante da integrare in una pipeline Python già interamente custom; l'alternativa più leggera — un grafo Python (dict di nodi/archi) con un piccolo motore di regole — è più coerente con lo stile del resto del codice (`utils/sgv.py`, `utils/cvss_eval.py` sono entrambi Python puro, zero dipendenze da librerie di grafo/ontologia).
3. **Il problema centrale, non banale: il grounding.** L'output dell'agente è testo libero + un vettore CVSS + un nome funzione + uno snippet — non è già nella forma "nodo ontologico". Serve un passo che mappi quell'output su concetti/relazioni dell'ontologia prima di poter verificare un vincolo. Due strade, entrambe con un costo:
   - **Mapping deterministico** (regex/keyword su CWE dichiarata, network function del task, campi del vettore CVSS): stesso spirito di G2/G3, ma più fragile perché il numero di concetti da riconoscere è molto più grande del semplice "esiste questo nome di funzione".
   - **Mapping via LLM**: reintroduce esattamente lo strato implicito che il controllo dovrebbe eliminare — lo stesso compromesso già rifiutato per G3 in ADR-2 (`docs/codemap/mappa_sistema.md`).
4. **Decidere dove si aggancia nel grafo LangGraph**: come nodo nel retry loop (tipo `check_sgv`, con feedback e re-tentativo) o come blocco di sola annotazione a valle (come il ramo B CVSS, che non tocca mai `verdict` — ADR-5). La seconda opzione è molto più sicura da aggiungere: non rischia di introdurre falsi retry su un controllo ancora non calibrato.
5. **Calibrare i vincoli su un banco di prova**, non fidarsi della prima stesura: serve un piccolo set di casi "coerente" vs "incoerente" noto a mano, sul modello del test di ammissione C1/C2 già usato per calibrare il giudice rubrica (`docs/judge_rubric/08_esperimento_calibrazione_giudice.md`). Senza questo passo non c'è modo di sapere se l'ontologia è troppo permissiva (non rifiuta mai nulla) o troppo rigida (rifiuta anche findings corretti).

## È fattibile?

**La parte infrastrutturale sì, in tempi brevi** (giorni): un nuovo modulo `utils/ontology_check.py` con la stessa forma di `utils/sgv.py` — grafo statico caricato da un file JSON/YAML, funzione di verifica che ritorna pass/fail + feedback — è un pattern già collaudato nel repo, non richiede nuove dipendenze pesanti se si evita OWL/SPARQL.

**La parte di contenuto (l'ontologia stessa e il mapping) è il rischio reale**, ed è quella che non dipende da noi: richiede lavoro di dominio esterno (Mario/Francesco), non ha ancora una prima bozza, e il mapping output-modello→ontologia è strutturalmente il punto debole (vedi punto 3 sopra).

## Inghippi principali

- **Circolarità con la ground truth.** Se l'ontologia viene costruita guardando le stesse CVE/CWE del dataset di test (com'è già successo per la rubrica del ramo A, che parte dalla GT — vedi `docs/judge_rubric/01_stato_attuale_giudice_rubrica.md`), il controllo rischia di validare solo cose già note, non di aggiungere potere di detection reale. La "CWE 5G" come tassonomia formale non esiste comunque (nota già in `docs/judge_rubric/05_rubrica_esperto_cwe_5g.md`): quello che si userebbe come riferimento (FiGHT/SCAS, CWE generiche) è un proxy, non uno standard di dominio pronto.
- **Reintroduzione dello strato implicito.** Se il mapping o l'interrogazione dell'ontologia passano per un LLM (come discusso in call 15 stessa: "un LLM che prende in input questo e ci rifà direttamente la risposta... in maniera molto più comprensibile"), il vantaggio di "deterministico e ispezionabile" si perde nello stesso punto in cui si voleva guadagnarlo.
- **Campione piccolo per validare l'aggiunta.** Il dataset ha ~10 CVE su 9 task; anche con calibrazione C1/C2-style, il numero di casi per stimare se il nuovo controllo migliora qualcosa resta piccolo (stesso limite già discusso per il CI95 a n=3 ripetizioni, ADR-10).
- **Owner esterno, non nel loop di sviluppo del codice.** Il lavoro di dominio dipende da Mario, che non ha visibilità diretta sul resto della pipeline — rischio di derive tra cosa l'ontologia rappresenta e cosa il codice può effettivamente verificare, se non c'è un giro di revisione stretto (com'è già previsto: "la rivediamo insieme" in call 15).
- **Rischio di ridondanza.** Se i vincoli finiscono per ricodificare quello che G2/G3/G4 già verificano (esistenza simbolo, groundedness snippet, validità vettore), il nuovo livello non aggiunge segnale — va progettato esplicitamente per catturare *relazioni* (es. "questa combinazione di CWE e impatto è implausibile") non fatti già coperti.

## Raccomandazione (non decisione — resta da portare al gruppo)

Partire piccolo e fuori dal retry loop: un numero ridotto di vincoli manuali (5-10, non un'ontologia OWL completa), verificati come blocco di annotazione a valle (come il ramo B), calibrati su un mini banco di prova prima di considerare l'aggancio al retry. Solo se il controllo dimostra di catturare incoerenze reali sui dati esistenti ha senso investire nel mapping più ricco e nell'integrazione nel loop.

## Riferimenti

- Codice come precedente di pattern: `utils/sgv.py` (gate deterministico in-loop), `utils/cvss_eval.py` (blocco di annotazione a valle, mai tocca `verdict` — ADR-5 in `codemap/mappa_sistema.md`)
- Calibrazione: `docs/judge_rubric/08_esperimento_calibrazione_giudice.md`, `09_risultati_calibrazione.md` (banco di prova C1/C2)
- Circolarità GT↔rubrica: `docs/judge_rubric/01_stato_attuale_giudice_rubrica.md`, `15_stato_attuale_gtfree.md`
- "CWE 5G" non standard: `docs/judge_rubric/05_rubrica_esperto_cwe_5g.md`
- Precedente di rifiuto di un fallback LLM per motivi analoghi: ADR-2 in `codemap/mappa_sistema.md`
