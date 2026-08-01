# Codemap/narrativa — indice

Questa cartella è lo strato discorsivo sopra `docs/codemap/`: stessa area, stessa profondità tecnica, stessi riferimenti `file:riga`, ma raccontata in prosa continua invece che tabulata. Non è una fonte indipendente — ogni file qui è una riscrittura per leggibilità del corrispondente file tecnico, verificata contro il codice dove serviva chiarezza, mai una nuova analisi da zero. Se un file qui e il suo corrispondente tecnico divergono su un fatto, il tecnico ha la precedenza (è quello ri-derivato direttamente dal codice a ogni `/codemap-refresh`); questo strato può restare indietro di qualche dettaglio minore finché non viene aggiornato a sua volta.

**A cosa serve**: leggerla per possedere davvero la conoscenza del sistema — non solo "cosa fa questa funzione" ma "perché è così, cosa succederebbe a cambiarla, come lo spiegherei/difenderei in una discussione col gruppo". Ogni file include, dove il file tecnico lo permette, una sezione esplicita su cosa dipende da cosa e cosa cambierebbe toccando un punto chiave — pensata per chi deve ragionare su sviluppi futuri, non solo capire lo stato presente.

**A cosa non serve**: non è un sostituto della verifica puntuale. Per citare un fatto con certezza (es. in una review, in un paper) risali sempre al riferimento `file:riga` indicato, o al file tecnico corrispondente.

## File

| File | Corrispondente tecnico | Racconta |
|---|---|---|
| [01_orchestrazione.md](01_orchestrazione.md) | [codemap/01_orchestrazione.md](../01_orchestrazione.md) | Come parte un esperimento da CLI e come è organizzata la configurazione |
| [02_langgraph_state_machine.md](02_langgraph_state_machine.md) | [codemap/02_langgraph_state_machine.md](../02_langgraph_state_machine.md) | Il ciclo di vita di un tentativo: agente → gate SGV → verifica risposta → retry → salvataggio |
| [03_agenti_llm.md](03_agenti_llm.md) | [codemap/03_agenti_llm.md](../03_agenti_llm.md) | Come si parla con l'LLM (agente e giudice), parsing, prompt |
| [04_task_loader.md](04_task_loader.md) | [codemap/04_task_loader.md](../04_task_loader.md) | Come un file task diventa stato del grafo, e come si evita di rieseguire l'esperimento |
| [05_valutazione_metriche.md](05_valutazione_metriche.md) | [codemap/05_valutazione_metriche.md](../05_valutazione_metriche.md) | La pipeline di reporting e il perché di ogni metrica M/S — il file più utile da saper argomentare |
| [06_cvss_scoring.md](06_cvss_scoring.md) | [codemap/06_cvss_scoring.md](../06_cvss_scoring.md) | Come un vettore CVSS testuale diventa un confronto contro la ground truth |
| [07_sgv_gate.md](07_sgv_gate.md) | [codemap/07_sgv_gate.md](../07_sgv_gate.md) | Cosa verifica il gate sintattico G1-G4 e perché, incluso un razionale esplicito da commit su una scelta scartata |
| [08_script_calibrazione.md](08_script_calibrazione.md) | [codemap/08_script_calibrazione.md](../08_script_calibrazione.md) | Cosa fanno i 4 script di calibrazione del giudice e quando useresti uno piuttosto che l'altro |

## Aggiornamento

Mantenuta insieme al livello tecnico dalla skill `/codemap-refresh`: quando un file tecnico viene rigenerato perché il codice sorgente è cambiato, il corrispondente file narrativo va rigenerato a sua volta (stesso comando, la skill lo fa in coppia).
