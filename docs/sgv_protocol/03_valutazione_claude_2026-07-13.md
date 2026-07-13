# 03 — Valutazione (2026-07-13): reazioni del team e problema aperto

> Segue [02_discussione_team_2026-07-13.md](02_discussione_team_2026-07-13.md). Richiesta di Nicolò: "valutazione sui messaggi? e cosa intendi? [...] il problema aperto cos'è?"

## Sulla "cecità semantica" (Raffaele)

Il punto è corretto e serio, e coincide con il rischio "gaming formale" già segnalato in [01_discussione_2026-07-13.md](01_discussione_2026-07-13.md#3-rischidomande-aperte-prima-di-implementare) (punto 1). G1–G4 verificano solo che i simboli/snippet citati esistano, non che il ragionamento abbia senso: un agente può soddisfare il filtro citando una funzione reale con motivazioni allucinate. In quel caso i k=3 retry si sprecano su un finding formalmente valido ma sostanzialmente vuoto — l'obiettivo del retry (dare all'agente la possibilità di correggersi) fallisce silenziosamente, senza che nulla nel sistema se ne accorga prima del Judge a valle.

## Su G5 — Semantic CWE Match (Raffaele)

Proposta ingegnosa ma con una tensione da esplicitare al team, non solo da implementare:

- La CWE segnalata dal SAST su quella funzione **è essa stessa informazione semantica sulla natura della vulnerabilità** — lo stesso Raffaele la chiama "ground truth parziale del SAST". Va quindi deciso esplicitamente se, ai fini del paper, la definizione di "ground truth da cui l'esperimento si vuole svincolare" include o esclude segnali di tool esterni come il SAST. Questo è rilevante rispetto all'obiettivo dichiarato da Andrea: *"svincolarsi dalla ground truth in qualche modo elegante e con un po' di novelty"*.
- **Tensione concreta con una metrica già definita nella proposta**: M4 (Delta SAST, §5.1 di `00_proposta_relatore.md`) misura quante vulnerabilità vere l'agente trova che il SAST *non* trova. Se G5 obbliga l'agente ad allinearsi alla CWE del SAST per superare il filtro, si rischia di sopprimere sistematicamente proprio i finding indipendenti dal SAST che M4 vuole catturare: un finding reale ma con CWE diversa da quella segnalata da SonarQube verrebbe scartato da G5 prima ancora di arrivare al Judge. Questa è una seconda ragione (oltre a quella già data da Andrea) per tenere G5 fuori dal primo esperimento.

## Sulla rigidità del matching esatto / proposta AST (Raffaele)

Punto valido ma di portata diversa e maggiore rispetto agli altri: non riguarda solo il filtro in-loop (G2), riguarda **la definizione stessa di ground truth** (§2 della proposta: `f ∈ V` per uguaglianza esatta di nome qualificato). Sostituirla con una metrica di prossimità AST ridefinirebbe cosa conta come "match" anche per le metriche M1/M2 a valle, non solo per il retry — tocca la validità della misurazione, non solo l'eleganza del filtro. Andrea non l'ha ancora commentato: merita una discussione a parte, esplicita, prima di deciderla insieme al resto.

## Il problema aperto

Andrea ha indicato una sequenza: si parte da un flusso che esclude il SAST (**esperimento 1**: solo G1–G4 su LLM puro); il suggerimento SAST (e quindi presumibilmente G5) entra "al terzo esperimento" (**esperimento 3**). Non ha specificato cosa occupi l'**esperimento 2**. Possibilità aperte, nessuna confermata:

- una via di mezzo con qualche mitigazione minima alla cecità semantica ma ancora senza SAST;
- semplicemente una tappa di consolidamento/ripetizione dell'esperimento 1 su altri task;
- oppure la numerazione "primo/terzo" era solo colloquiale e il piano reale è binario (solo-LLM vs con-SAST), senza un vero step intermedio.

Prima di disegnare qualunque cosa oltre l'esperimento 1 (G1–G4 puro), va chiesto esplicitamente ad Andrea/Raffaele cosa riempie questo slot — altrimenti si rischia di costruire una tappa intermedia che nessuno ha davvero richiesto.
