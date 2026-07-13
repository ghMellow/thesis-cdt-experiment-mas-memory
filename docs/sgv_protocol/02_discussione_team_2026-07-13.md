# 02 — Discussione di team (2026-07-13, pomeriggio): reazioni alla proposta SGV

> Segue [00_proposta_relatore.md](00_proposta_relatore.md) (proposta) e [01_discussione_2026-07-13.md](01_discussione_2026-07-13.md) (mappatura sull'architettura). Nicolò condivide la cartella `docs/sgv_protocol/` con il team; seguono i primi commenti.

## Messaggi (verbatim)

**Nicolò**, condividendo la cartella:
> Interessante, mentre mi leggo per bene il doc vi condivido la cartella che ho creato nel progetto dove gli ho fatto comparare-discutere dell'argomento guardando lo stato attuale del progetto. E che altre discussioni valutazioni relative a questo saranno li.
>
> docs/sgv_protocol

**Andrea Bernardini**, 14:57:
> Ok grazie Nicolò ragioniamoci sopra. Vanno bene anche ipotesi operative. L'obiettivo è quello di svincolarsi dalla ground truth in qualche modo elegante e con un po' di novelty

**Raffaele Nicolussi**, 15:16:
> La proposta mi sembra valida ma, se non prendo cantonate (e con me gemini che mi ha aiutato nell'analizzare la proposta di Andrea), potrebbe soffrire "cecità semantica" ovvero l'SGV convalida esclusivamente la groundedness formale per cui pattern di ragionamento completamente allucinati o logicamente fallaci supereranno il filtro purché referenzino simboli esistenti, il che rischia di saturare a vuoto i tentativi di retry (k=3).
>
> Una possibile soluzione potrebbe essere quella di inserire controlli che verifichino il senso logico senza conoscere a priori la soluzione:
>
> 1. **L'input (SAST)**: il coordinatore sa dal report di SonarQube che in quella funzione c'è un rischio legato al CWE-287 (Improper Authentication). Questa è l'etichetta semantica di partenza (Ground Truth parziale del SAST).
> 2. **Il task dell'LLM (Worker)**: l'Agente LLM analizza il codice. Nel suo prompt di sistema gli viene richiesto di produrre l'output in JSON con un campo obbligatorio, ad esempio: `"cwe_id_rilevato": "CWE-XXX"`.
> 3. **La verifica (SGV Deterministico)**: l'LLM restituisce il suo JSON. A questo punto subentra l'SGV (il filtro non-AI), che aggiunge un nuovo controllo deterministico (**G5 — Semantic CWE Match**):
>
> Regola dell'SGV: SE `cwe_id_rilevato` (dell'LLM) NON È COMPATIBILE CON `cwe_sast` (di SonarQube) → SCARTA E CHIEDI RETRY
>
> Esempio pratico: se l'LLM allucina e scrive `"cwe_id_rilevato": "CWE-119"` (Buffer Overflow), lo script Python (SGV) vede che "CWE-119" non c'entra nulla con il "CWE-287" segnalato da SonarQube. Il filtro sintattico boccia il tentativo e rimanda all'LLM il messaggio di errore: *"Il tipo di vulnerabilità rilevata non è coerente con l'anomalia strutturale della funzione. Ritenta."*
>
> Quindi:
> - L'LLM non fa da giudice. L'LLM "Lavoratore" si limita a dichiarare cosa ha trovato.
> - Il sistema mantiene l'assoluta riproducibilità: non c'è una temperatura o un seed stocastico nel controllo, è un banale operatore logico `==` o un controllo in un albero tassonomico.
> - Risolve la cecità semantica: se l'agente spara una vulnerabilità a caso solo per soddisfare il controllo sui nomi delle funzioni (G2 e G3), viene bloccato perché l'etichetta CWE non fa match con il contesto di quel frammento di codice.

**Raffaele Nicolussi**, 15:19 (modificato):
> Ci potrebbero essere altre cose da limare come l'eccessiva rigidità del vincolo di matching deterministico. Il rischio è di penalizzare le detection indirette (ad esempio, logic flaws individuati correttamente in una funzione chiamante o in un'interfaccia correlata anziché nella specifica funzione modificata dalla patch) cosa che potrebbe essere mitigata da metriche di prossimità basate sull'Abstract Syntax Tree (AST).

**Andrea Bernardini**, 15:26:
> Si ci sono molti scenari. L'unica osservazione è che partirei da un flusso che esclude il discorso SAST così possiamo testare anche il contesto solo framework LLM. Il suggerimento del SAST che si integra nel prompt arriva al terzo esperimento

## Sintesi dei punti nuovi rispetto a 00/01

1. **Obiettivo esplicito (Andrea)**: svincolarsi dalla ground truth "in modo elegante e con un po' di novelty" — le ipotesi operative sono benvenute, non solo la teoria.
2. **Debolezza nuova identificata (Raffaele): "cecità semantica" dell'SGV.** G1–G4 verificano solo la fondatezza formale (simboli esistenti, snippet reali), non la plausibilità logica del ragionamento — un finding allucinato ma formalmente valido supera il filtro e può saturare a vuoto i k=3 tentativi di retry. Coerente con il rischio "gaming formale" già annotato in [01_discussione_2026-07-13.md](01_discussione_2026-07-13.md#3-rischidomande-aperte-prima-di-implementare) punto 1, ma qui arriva con una proposta concreta di mitigazione.
3. **Proposta G5 — Semantic CWE Match (Raffaele)**: usa la CWE segnalata dal SAST (es. SonarQube) come "ground truth parziale" nota a priori al coordinatore (non alla soluzione specifica, solo alla categoria di vulnerabilità), e verifica deterministicamente (confronto/tassonomia CWE, non LLM) che la CWE dichiarata dall'agente sia compatibile con quella del SAST. Resta un controllo `==`/albero tassonomico, quindi preserva riproducibilità e assenza di temperatura/seed nel gate.
4. **Rischio collaterale segnalato dallo stesso Raffaele**: eccessiva rigidità del matching deterministico — penalizzerebbe detection indirette (logic flaw trovato nella funzione chiamante o in un'interfaccia correlata, non nella funzione esatta modificata dalla patch). Mitigazione proposta: metriche di prossimità basate su AST (distanza strutturale invece di uguaglianza esatta sul nome di funzione).
5. **Decisione di sequenza (Andrea, 15:26)** — **presa**: il primo esperimento del protocollo SGV esclude il SAST. Si parte da un flusso "solo framework LLM" (G1–G4, senza G5/CWE-match); l'integrazione del suggerimento SAST nel prompt (e quindi G5) arriva solo al terzo esperimento della sequenza.

## Implicazioni per l'implementazione (non ancora fatta)

- L'ordine di rollout ora ha una sequenza esplicita: **(1) SGV puro G1–G4 solo-LLM → (2) [da definire, presumibilmente variante intermedia] → (3) G5 con input SAST/CWE nel prompt.** Va chiarito con Andrea/Raffaele cosa occupa lo step (2), non ancora specificato nei messaggi.
- G5, quando introdotto, richiede una tassonomia di compatibilità CWE (non solo uguaglianza esatta: CWE correlate/genitore-figlio vanno probabilmente considerate compatibili — da definire prima di implementare, altrimenti si reintroduce rigidità eccessiva sul lato semantico analoga a quella già notata sul matching per nome di funzione).
- La proposta AST-based di Raffaele (prossimità strutturale invece di match esatto sul nome) tocca sia G2 (esistenza simboli) sia la relazione di match §2 della proposta originale (oggi: uguaglianza esatta case-insensitive su f ∈ V) — impatta la definizione di ground truth stessa, quindi va discussa con più attenzione prima di sciogliere il nodo, essendo un cambio della metrica di detection (M1/M2), non solo del filtro in-loop.
