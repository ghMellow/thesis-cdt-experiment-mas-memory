# Dev Log — Multi-Agent Experiment 5G

I mesi chiusi stanno in `devlog/AAAA-MM.md` (indice: `grep '^## ' DEVLOG.md devlog/*.md`).

---

## 2026-10-29 — CLAUDE.md a livelli (skill ottimizza-contesto)  [sessione: 1ff07bd9-327a-4499-863f-a01a08a9a439]

**Intent:** «ottimizza contesto».
**Divergenze:** la radice era già piccola (64 righe, 4,8 KB): il costo vero era il «Bootstrap di sessione», che imponeva di leggere `docs/status.md` (22 KB, ~7k token) a ogni avvio. Nei transcript: letto in 1 sessione su 15, `call_2`/`call_3` in 0.
**Decisioni:** «si» all'intera proposta, compreso `docs/artefatti/CLAUDE.md` **versionato** (non era una scelta esplicita fra le due opzioni: si è preso il default proposto).
**Esito/Problemi:**
- Il Bootstrap è stato sostituito da §0 «Contesto a necessità», scritto per condizione. Mappa accorciata (l'elenco completo resta in `docs/README.md`), Workflow accorpato alla Regola fondamentale.
- Radice da 64 righe / 4,8 KB a 55 righe / 4,2 KB, meno della stima di 3,5 KB perché la tabella §0 pesa. Nuovo `docs/artefatti/CLAUDE.md` (7 righe); regola dei tag `results-*` aggiunta anche alla skill `results-publish`.
- Fatti superati corretti: «2 math, 2 textual» → 12 task. Per la roadmap ora si rimanda anche alle trascrizioni di ottobre. Non toccato: lo snapshot di `status.md` è fermo al 2026-07-10.
- Ancora da verificare in una sessione nuova: carico della radice leggera, caricamento automatico di `docs/artefatti/CLAUDE.md`, letture innescate dal §0.

---

## 2026-10-29 — Riordino del progetto e archivio mensile del DEVLOG  [sessione: b24cebac-2a02-4431-a589-e88400857da4]

**Intent:** «il progetto è ben organizzato o ci sono file e altro rimasti non catalogati come abbiamo detto nelle skill?», poi «1 e 2» (le correzioni senza rischio e l'archivio del DEVLOG).
**Divergenze:** trovato e corretto un link rotto in `docs/README.md` (`team_update` puntava alla radice di `docs/` invece che a `cve_experiment/`). `results/logs/` messo in `.gitignore` invece che committato: sono output di terminale, non parte degli snapshot `results-*`.
**Decisioni:** accettati i punti 1 (correzioni senza rischio) e 2 (archivio DEVLOG). Restano da decidere: uv o Poetry (ci sono tutti e due i lock, `.venv` è di uv), cancellare lo zip `Analisi_Statica-…` dopo il confronto con `docs/sast_tools/analisi_statica_v4.2.1/`, creare `research/` (paper rielaborati in `docs/judge_rubric/`, `docs/chat_exports/`), dove mettere `ground_truth_vuln_files.xlsx` e `File_Free5gc_Vulnerabili/`, la rinomina dei file datati in `docs/`.
- Punto 3 («sistema»), scelte dell'utente: **zip tenuto** (verificato identico byte per byte a `docs/sast_tools/analisi_statica_v4.2.1/`, 24 file); **Poetry** (cancellato `uv.lock`; `poetry run` verificato sulla `.venv` esistente, `poetry check --lock` ok); **niente `research/`** per ora; **rinomina solo di `team_update_CVE-…`** (doppio spazio → `_`, link aggiornati in `docs/README.md` e `docs/cve_experiment/README.md`), date nei nomi di `docs/` lasciate.
- Non chiesti, decisi: `File_Free5gc_Vulnerabili/` e `ground_truth_vuln_files.xlsx` restano dove sono (percorso letto da `config.py`, 73 rimandi; `cve_metrics (1).json` è il file grezzo ricevuto, citato con quel nome in `docs/tasks_provenance.md`).
**Esito/Problemi:**
- `.notes/INDEX.md`: aggiunte le 7 note mancanti e la cartella `report/figura-architettura/` (versione standalone della figura, non un doppione); cancellati i file intermedi di LaTeX.
- `docs/README.md`: aggiunti `sast_tools/`, `graph.png`, `index.md`, `chat_exports/`. `pyproject.toml`: `readme = "readme.md"` (il file in git è minuscolo).
- DEVLOG: da 1524 righe / 246 KB a ~300 righe / 39 KB; mesi 2026-05…2026-08 in `devlog/`. 134 entry prima e dopo, contenuto confrontato con diff sul backup.

---

## 2026-10-28 — Push di dev, PDF in .notes/, controllo dei link condivisi  [sessione: ef61eec8-7f03-41bf-86b1-aa7f016ee8ac]

**Intent:** «c'è altra roba da pushare, o comunque ci sono dei file da riorganizzare es i due pdf da mettere dentro le cose non tracciate nostre direi»; poi «se i link che avevamo dato non sono taggati allora tagga così rimangono nel tempo».
**Divergenze:** i PDF sono stati rinominati con la data (`.notes/paper/2026-10-16-icai-tems-2026.pdf`, `2026-10-28-bozza-itasec.pdf`) e aggiunti a `.notes/INDEX.md`.
**Decisioni:** «si» alla proposta → pushati i 5 commit di documentazione e committati i report `_n3`, i findings e `semantic_cache.json` (`627cb34`); `results/logs/` resta fuori da git.
**Esito/Problemi:** i link mandati a Francesco e Lorenzo (`.notes/report/2026-10-22-provenienza-numeri-paper-icai.md`) puntano già ai tag `results-2026-07-14`, `-07-23c`, `-10-18`, che sono sul remote, e i file citati ci sono: nessun tag nuovo. I due artifact claude.ai del 22/10 erano già stati cancellati.

---

## 2026-10-28 — Sezione IV resa generica rispetto al resto della bozza  [sessione: 736f85c6-b1ad-47d6-a15f-1c26a2ca5a50]

**Intent:** «salvare il lavoro fatto ora su git e poi di generalizzare la nostra parte»; sul 9/9 CVE: «non importa per ora va bene così».
**Decisioni:** le incongruenze aggiustate a mano nelle sezioni degli altri si portano dietro; si tocca solo la sez. IV; il 9/9 non si segnala per ora.
**Esito/Problemi:**
- Testo (`.notes/report/2026-10-27-sezione-architettura.tex`): «gosec, Semgrep and CodeQL» → «the Multi-SAST suite of Section 5.2» (poi senza rimando: «introduced in this work»); tolti estratti e commit range (file sempre interi nelle prove); tolta la variante con codice collegato; tolto il confronto primo attempt / risposta finale, che nessuna tabella riporta.
- Trovata e corretta: «Processing is organised in three phases.» era finita dentro un commento `% NOTE` e mancava dal PDF; il rimando a `subsec:repetitions` (numero sbagliato) → «see *Independent runs* below».
- Figura: «SonarQube alone, or the Multi-SAST suite», ricompilata, PNG rigenerati.

## 2026-10-28 — Valutazione della bozza ITASEC rispetto alla sezione 4  [sessione: 736f85c6-b1ad-47d6-a15f-1c26a2ca5a50]

**Intent:** «rispetto il resto del paper siamo totalmente scollegati o lavoriamo al nostro obiettivo ci sono parti che andrebbero scritte in altre zone, ecc fai una valutazione» (bozza `TBD__Static_Analysis_Guided_Agentic_LLMs_.pdf`).
**Esito/Problemi:**
- La sezione 4 è allineata con il codice e con le RQ; le sezioni 1, 5 e 6 descrivono un sistema e dei numeri diversi: «9/9 CVE con Multi-SAST» non ha riscontro nelle corse (UDR 3 SAST: 3/6 distinte sul dataset corretto, 5/6 su quello non corretto; 40245 mai trovata); terzo tool chiamato SonarQube invece di gosec; righe Multi-SAST di AMF/PCF senza corse; variante con codice collegato assente dalla valutazione.
- Promesse della sez. 4 mai usate nella 6: primo attempt contro risposta finale, detection per run (hit rate), valore di R.
- Fonte dei numeri: `.notes/report/2026-10-22-mega-confronto.md`, `docs/sgv_protocol/14_braccio_sast_multitool.md`. Valutazione completa data in chat, non salvata in un file.

## 2026-10-28 — Figura: suggerimenti di un collaboratore  [sessione: 723f5456-66ef-4869-983e-5720df5869e3]

**Intent:** suggerimenti incollati dall'utente (testi delle caselle più uniformi, via le scritte «code»/«LLM», contorni più spessi, colori LLM/codice ben diversi, «tipo blu e arancione»); «magari abbiamo già sistemato qualcosa o comunque c'è un sottotesto da applicare alla nostra nuova versione?».
**Divergenze:**
- Non applicati, perché contraddicono il codice: SAST «SonarQube, Semgrep, CodeQL» (i 3 tool sono gosec + Semgrep + CodeQL, `utils/sast_unified_to_hint.py`); CVSS reporting instructions nella casella Task (sono un blocco aggiunto dal prompt builder, non stanno nel task); «prompt creation and verification» (il prompt builder non verifica niente).
- CVSS scorer: «score assignment» → «score recomputation from the agent's vector» (il punteggio si ricalcola dal vettore dell'agente, non si assegna).
- Freccia del confine GT da ruggine a nera (si confondeva con l'arancione); retry dell'SSV in arancione come la casella; didascalia con i colori; copia per Overleaf rigenerata dallo standalone con i `\definecolor` elencati in testa.
**Esito/Problemi:** applicati gli altri suggerimenti; figura ricompilata e controllata anche in scala di grigi (blu scuro contro arancio chiaro, più angoli tondi/vivi).
**Decisioni:** l'utente: «noarqube ok era del vecchio ma lo inserirei comunque no? per dire tutti i sast provati» → SonarQube inserito come **alternativa** («SonarQube, or gosec + Semgrep + CodeQL»), nella casella e nel testo, perché il sistema riceve o l'uno o i tre insieme, mai tutti e quattro. Poi l'utente: «nella nuova versione si fa il confronto con i risultati della vecchia» → la riga SonarQube è nel paper, il dubbio sollevato non si pone.

## 2026-10-28 — Sezione IV: revisione dell'inglese e dei termini interni  [sessione: 723f5456-66ef-4869-983e-5720df5869e3]

**Intent:** «analizzare il testo da un punto di vista di esperto di lingua inglese […] se usiamo termini interni del progetto al posto di usare parole con significato anche per chi vede per la prima volta».
**Divergenze:** proposte in tre gruppi (1 termini, 2 inglese, 3 spostare il paragrafo delle unità dopo le fasi). Trovata un'imprecisione mia di prima: «each task covers one file» è falso per i task non `_full` (estratti) e per task9 (quattro file).
**Decisioni:**
- «procedi con le correzioni 1 e 2» → applicate: *execution* → *run* (paragrafo *Independent runs*), Judge presentato come *LLM-as-a-judge*, SSV definito come *grounding check*, verdetto *accepted*/*rejected*, FIRST spiegato, `handler_functions` tradotto, tolta la frase sul file dei risultati, *linked-code variant* riscritto, più le correzioni d'inglese.
- Il gruppo 3 non è stato chiesto: il paragrafo delle unità resta prima delle fasi.
- Fatto anche senza richiesta esplicita, per coerenza: nella figura «(correct, or budget spent)» → «(accepted, …)», ricompilata.
**Esito/Problemi:** compila senza errori; `Section~\ref{subsec:repetitions}` stampa il numero di «Execution Pipeline» (la label sta in un `\paragraph`). Aggiunta al `CLAUDE.md` globale la sezione «Lessico — plain language», anche per la chat.

## 2026-10-28 — Sezione IV: repetition, attempt e perché i retry  [sessione: 723f5456-66ef-4869-983e-5720df5869e3]

**Intent:** passaggio «The same matching is applied to the report of the first attempt […] it cannot alter this matching» non chiaro; l'utente: «non è chiaro il motivo per cui abbiamo i retry e come li usiamo anche final answer», e ricorda un problema dei report «riguardo proprio a come contiamo le rep» da sistemare dopo la consegna.
**Divergenze:** «it cannot alter this matching» era falso (il Judge decide quale report arriva al matcher); proposte, oltre alla riscrittura del passaggio, le due unità execution/attempt in apertura, il perché del loop, una riga in *Repetitions*.
**Decisioni:** «si» → applicati tutti e 4 i punti a `.notes/report/2026-10-27-sezione-architettura.tex` (compila, nessun riferimento indefinito) e aggiunta la voce «dopo la consegna» nel piano `.notes/piani/2026-10-22-piano-call-itasec.md`.
**Esito/Problemi:** il problema dei report era scritto solo nella trascrizione della call del 27 (righe 252-258): i report mostrano `rep` e `attempts` in sezioni sparse, senza spiegare la differenza.

## 2026-10-28 — Sezione IV e figura: Task e Go source sono un input solo  [sessione: 723f5456-66ef-4869-983e-5720df5869e3]

**Intent:** dubbio dell'utente su «takes the task and the Go source» («è una variabile o un file preso due volte?»), poi «si e a sto punto anche img è corretta o va sistemata?».
**Esito/Problemi:**
- Nel codice il sorgente sta dentro il task: nei task fissi è il blocco ```go del `.md`; in `--source-dir` il task si costruisce da un file. Anche «file, project or commit diff» era impreciso: un task = un file, un progetto diventa N task e `--changed-since` sceglie solo quali file analizzare, sempre dati per intero.
- Testo: due input invece di tre, frase su un task = un file, «the source code» tolto dal prompt builder.
- Figura (`figura-architettura/system-architecture.tex` e copia `2026-10-27-figura-architettura.tex`): box Go source unito a Task, prompt builder «task + SAST alerts»; ricompilata, PNG rigenerati.

## 2026-10-27 — Sezione IV (System Architecture) riscritta per ITASEC  [sessione: 718d2b3b-d8ef-4d93-9632-277b1f6d9649]

**Intent:** «devo fare il punto 4 […] prendere il paper vecchio e limare correggere le imprecisioni», sul testo della sezione IV del paper ICAI TEMS.
**Divergenze:**
- Corrette sul codice nove affermazioni del testo vecchio: feedback semantico dopo il judge (il retry è neutro); «k=3 retries» (sono 3 attempt); «admitted only if it clears both checks» (l'ultimo report si salva comunque); il judge «never sees the raw source» (lo riceve); SSV su «every referenced symbol» (solo il campo `function`); «external coordinator» (sono gli archi del grafo); il judge che «gonfia» i finding per gli esperti; lista SAST solo SonarQube; «line parameter» (è la riga `snippet`).
- Aggiunti un paragrafo sulle repetition e il CVSS scorer; fasi rinominate come nella figura (Generation / In-loop checks / Post-loop scoring); banda della figura rinominata «POST-LOOP SCORING».
**Esito/Problemi:** `.notes/report/2026-10-27-sezione-architettura.tex`, compilata con la figura su un banco locale. Aperte, come `% NOTE` nel file: quale rubrica descrive il paper (quella del task nomina la debolezza attesa, quindi «no GT» va attenuato) e il valore di R nelle tabelle.

---

## 2026-10-27 — Documentazione HTML in docs/artefatti/  [sessione: 7fcc1247-9695-444a-91bb-5aa71aa99400]

**Intent:** «avevamo iniziato a scrivere la documentazione del progetto, continua e finiscila». Ripreso il lavoro interrotto il 22/10 (sessione 74810fbc): «no gli artefatti dicevo pagine html locali nel progetto pushate come fatto per il progetto phytwin». I due artifact claude.ai erano stati cancellati quel giorno: l'entry del 22/10 che li dà pubblicati non vale più.
**Divergenze:**
- `docs/documentazione_sistema.html` divisa in 10 pagine (`01_sistema` … `10_glossario`) con l'impianto di PhyTwin (menu, tema, mermaid in `vendor/`); stile e runtime dei diagrammi in file unici (`stile.css`, `diagrammi.js`) invece che ricopiati in ogni pagina come in PhyTwin; accento blu per distinguerla. Vecchia pagina rimossa.
- Aggiunta nella pagina dei report la vista `--max-repetitions` (codice del 27/10, ancora non committato) e riallineati i `file:riga` di `utils/evaluation_utils.py`, spostati di 22–57 righe; tolti i rimandi in avanti.
- Confronto: invece dello script usa e getta del 22/10, `utils/md_to_artefatto.py` + `--html` in `utils/generate_mega_comparison.py` → `docs/artefatti/11_confronto.html` generata (test in `tests/test_md_to_artefatto.py`). Rigenerato: numeri identici al 22/10, cambiata solo «Come si rigenera» (tolto il percorso assoluto).
**Esito/Problemi:**
- Schermate Chrome headless di 01, 04, 05, 11: diagrammi disegnati; all'inizio i due larghi uscivano a destra (mancava `max-width` sull'SVG), corretto. Link interni e ancore controllati da script: 0 rotti. `unittest`: 17 test OK.
- `11_confronto.html` contiene la serie SonarQube `rerun2610` che il 16/10 si era deciso di non pubblicare (repo pubblico).

**Decisioni:** «pusha questi artefatti la doc va bene» → pushate le pagine del sistema; il confronto escluso (ambiguo rispetto alla decisione del 16/10): fuori dal menu e in `.gitignore`, resta in locale. Pushate anche la vista `--max-repetitions` e i test del 27/10, che la pagina dei report descrive. Poi: «sono i file che fanno da source del progetto come claude md e devlog e altri indici di cartella da non pushare» → `CLAUDE.md`, `DEVLOG.md`, `docs/README.md`, `docs/status.md` aggiornati solo in locale.

**Problema:** `git push origin dev` ha pubblicato anche sei commit del 22/10 rimasti solo in locale (`295cbc1`…`ed0379a`), non controllati prima del push. Fra questi `bd11758` porta su GitHub la corsa SonarQube `1A_sast_hint_full_rerun2610` (raw JSON di UDR e UDM, report, file di dettaglio), che il 16/10 si era deciso di non pubblicare, e `48c1d73`/`ed0379a` toccano `DEVLOG.md`. Prima del push su `origin/dev` non c'era nessun file `sast_hint_full_rerun2610`. Rimedio (riscrivere la storia e fare force-push) in attesa di decisione dell'utente.

**Decisione (poi):** «massi pubblica tutto poi l'importante è saper condividere correttamente il materiale quando è necessario» → niente force-push; la decisione del 16/10 su SonarQube `rerun2610` è superata, pubblicato anche `11_confronto.html` (tolto da `.gitignore`, rimesso nel menu).
- Convenzioni in `docs/artefatti/DESIGN.md`; indice in `docs/README.md` e riga in `CLAUDE.md`.

---

## 2026-10-27 — Figura System Architecture rifatta per ITASEC  [sessione: 718d2b3b-d8ef-4d93-9632-277b1f6d9649]

**Intent:** «nella trascrizione c'è da migliorare il grafico per la prossima paper […] dammi il nuovo (vedi se creare un latex locale di test e poi io lo incollo)», a partire dalla figura TikZ di Andrea.
**Divergenze:**
- Il punteggio CVSS sta nella fascia dopo il loop, non fra verifier e judge come nello schema della nota del 27 (§3): nel codice il punteggio si ricalcola dal vettore con la libreria `cvss` solo in `save_result`, mentre l'SSV controlla soltanto che il vettore sia valido.
- In più rispetto alle critiche: un solo budget di 3 attempt per i due retry, retry dell'SSV con i difetti formali, retry del judge senza feedback, uscita «last attempt's report», cioè come si comporta il codice e non come lo descrive il paper di ICAI TEMS.
- Didascalia riscritta; serve `shapes.geometric` in `\usetikzlibrary`.
**Esito/Problemi:** `.notes/report/2026-10-27-figura-architettura.tex` (+ `.png`), compilata con pdflatex su un banco locale. La TikZ incollata nel template Overleaf non si vedeva: consegnata anche come PDF vettoriale autonomo (`.notes/report/figura-architettura/system-architecture.pdf`) da inserire con `\includegraphics`.
**Decisioni:** l'utente chiede se il punteggio ricalcolato con la libreria vada nel grafico → aggiunto il blocco «CVSS scorer» dopo il loop e **prima** del confine GT, perché il ricalcolo non usa la GT: serve al confronto con il CVSS pubblicato, alla coerenza fra punteggio dichiarato e vettore, e a ordinare i finding non abbinati per gli esperti (`utils/cvss_eval.py`). Resta aperto: sui task statici la rubrica del judge nomina la debolezza attesa, quindi la scritta «no GT» sulla fascia dei controlli vale solo se il paper descrive la rubrica generica.

---

## 2026-10-27 — Allineamento della documentazione rimandato  [sessione: 3ed4d8a2-f42e-4cd6-a4d6-bb10c6973133]

**Intent:** «quel progetto l'ho un po lasciato da parte andrebbero rivisti e allineati o fatta una linea e partire congruenti sulle cose fatte», poi «altrimenti lasciamolo come lavoro futuro da fare in quel progetto».
**Decisioni:** non serve al sommario della tesi, quindi è lavoro futuro dopo la consegna del 29/10.
**Esito/Problemi:** piano in `.notes/piani/2026-10-27-allineamento-docs.md`. Emerso scrivendo il sommario: il doc 15 della rubrica dice che la GT-free non è usata in nessun run, ma la v2 è cablata nella modalità generica (`config.DYNAMIC_RUBRIC_PATH`, `main.py:172`).

---

## 2026-10-27 — Trascrizione della call del 27 divisa per tema  [sessione: f3a382e1-3eea-44a2-9bf7-eb4180145291]

**Intent:** «la seguente trascrizione tocca più temi insieme crea n trascrizioni che separano questi momenti […] poi posiziona le trascrizioni nelle cartelle dei progetti corretti e crea anche un documento in cui estrai le informazioni rilevanti».
**Divergenze:** due documenti di estrazione invece di uno, uno per progetto accanto alla sua trascrizione; le righe sulla trasferta a Pisa spostate nella parte 2; futuro/incarico lasciati nella parte 1 (tesi).
**Decisioni:** prima la sezione System Architecture del paper (testo vecchio ripreso e sistemato, figura rifatta), poi la presentazione; il riassunto della tesi lo controlla Nicolò a parte.
**Esito/Problemi:** `docs/supporto/calls/transcripts/call-2026-10-27-itasec-presentazione.md` + `.notes/call/2026-10-27-punti-dalla-call.md` (nuova cartella `call/`); parte 1 (tesi) nel repo PhyTwin. Data del 27 dedotta dalla registrazione («Tesi_call_24 (papers)», salvata il 27 alle 10:55).

---

## 2026-10-27 — Report «3 tool + file» a 3 repetition  [sessione: f9a8ba38-796f-4ffa-85ac-8d58eb7d44b7]

**Intent:** «di cui ci interessa solo quelli 3 tool + file / riesci a sistemare il problema e rendere i confronti a 3 rep?», riferito ai report consegnati `results-2026-07-14` (UDR `1A`) e `results-2026-10-18` (UDM `1A_sast3tool_linked_full`).
**Divergenze:**
- L'AI ha scelto una vista accanto al report completo (`result_<task>_<id>_n3.md`, opzione `--max-repetitions` in `utils/evaluation_utils.py`) invece di riscrivere i report a 10: quelli restano validi per D1.
- I file di dettaglio della vista hanno nome proprio (`…_n3_…`), perché le lettere `group` cambiano quando le repetition sono 3.
- Il confronto fra corse vecchie e nuove si fa con `generate_detection_table`, leggendo dal tag, perché `1A` su disco è la corsa rifatta il 14/07 (con SGV) e non quella del 13/07 che è stata consegnata.
**Esito/Problemi:**
- Generati `result_task6_vuln_udr_full_1A_sast3tool_linked_full_n3.md` e `result_task8_…_n3.md`. Sul dataset non corretto TP/FP/FN di UDR (7/11/11) coincidono con quelli calcolati da `generate_detection_table`.
- UDR a n=3, dataset corretto: il vecchio trova 1/6 CVE distinte (P 0.133), «3 tool + file» 3/6 (P 0.278). UDM: tutti e due 1/1, ma P scende da 0.250 a 0.107 (FP 9 → 25).
- Il controllo semantico ha chiamato il judge su UDR: le 3 repetition sono una combinazione nuova, quindi `semantic_cache.json` è cambiato.
- I report per corsa contano ancora i match spuri 40249/40343 (problema C1 aperto): per l'articolo valgono i numeri sul dataset corretto.

---

## 2026-10-22 — Pubblicazione delle pagine come artifact  [sessione: 74810fbc-7fbe-445d-9bef-258557bddc81]

**Intent:** «pubblica gli artefatti così sono visionabili» (prima: «no sempre nella repo», detto della pagina HTML).
**Divergenze:**
- L'AI ha scelto di pubblicare due pagine: la documentazione del sistema e il mega confronto. Le altre note (provenienza, legenda, tempi) non sono pubblicate.
- Nel mega confronto ha aggiunto un riquadro «In breve» con le conclusioni dell'agente `mega-confronto`.
- In `docs/documentazione_sistema.html` la classe `mermaid` diventa `mmd`, perché il visualizzatore degli artifact disegna da solo i blocchi `mermaid` e la pagina li ridisegnerebbe.
**Esito/Problemi:**
- Documentazione del sistema: https://claude.ai/artifact/LwVCJiX7aphULHm2gfa4om
- Confronto detection: https://claude.ai/artifact/549xEnLnGqdfcFPQRi46KM. È generato dal markdown con uno script usa e getta nello scratchpad (`md2page.py`): se il confronto si rigenera, la pagina va ripubblicata.
- Tutte e due sono private: vanno condivise dal menu Share. Il rendering dei diagrammi sul visualizzatore non è stato verificato.

---

## 2026-10-22 — Repetition UDM, serie di luglio, deduplica e mega confronto  [sessione: 74810fbc-7fbe-445d-9bef-258557bddc81]

**Intent:** «1. si 2. a 3. se pensi che a basti altrimenti anche il modello / fai tutto e rendi tutto poi in un mega confronto così prendiamo quello che vogliamo».
**Decisioni:**
- Lanciare le 28 repetition UDM della serie del 16/10, in sequenza (P1 di B2).
- La serie di luglio su UDM resta a 3 repetition, dichiarate (opzione a); niente serie ibrida.
- Deduplica degli unmatched: prima per sola funzione, in modo deterministico; il check LLM solo se questo non basta (libertà lasciata all'AI).
- Alla fine un confronto unico di tutte le varianti, da cui scegliere.
- Richiesta durante il lavoro: «lancia un agente in parallelo che usi la skill per creare la documentazione [...] fatto come html». L'AI la interpreta come la documentazione dell'intero sistema (architettura, pipeline, SAST, valutazione), salvata in `docs/documentazione_sistema.html`.
**Esito/Problemi:**
- Corse UDM lanciate in background.
- Subagent `dedup-rule`, `mega-confronto` e `doc-html` in parallelo.
- Corse UDM finite: tutti e 4 gli experiment-id della serie del 16/10 sono a 10 repetition (rep 4-10 con run_id `20261022T1114..–1118..Z`), in ~5 min, senza 429 né errori (log in `results/logs/d1_*udm.log`). La serie di luglio è segnata a 3 ripetizioni nel report.
- **dedup-rule** (subagent): vista dei distinti con gli unmatched per funzione normalizzata, ignorando il vettore. Su 4 report gli unmatched sono 65 con la regola vecchia, 28 con questa, 18 nel riferimento fatto a mano. Lo scarto resta perché lo stesso bug compare su più handler. (b) non è stato implementato: agirebbe solo sui 4 casi in difetto, il passo estratto a volte è quello sbagliato, e servirebbero 128 chiamate nuove. Per i casi in eccesso servirebbe (c), che è da decidere.
- **mega-confronto** (subagent): `utils/generate_mega_comparison.py` produce `.notes/report/2026-10-22-mega-confronto.md`. `generate_detection_table.py --paper-icai` rifà TP e FN della Tab. III in 8 righe su 8; le tabelle dei doc 13 e 14 escono identiche. Risultato principale: nella serie di ottobre SonarQube non batte il no hint su UDR (2/6 contro 3/6 CVE), mentre 3 SAST + linked arriva a 9/10 rep e P 0.36. Divergenze: la serie UDM di ottobre mette insieme le rep 1-3 del 16/10 e le 4-10 del 22/10; Tab. V e Candidates non ci sono.
- **Orchestratore:**
  - `python -m utils.evaluation_utils` senza filtro rigenerava solo gli id `1A`/`1B`, al contrario di quanto dice il commento. Corretto: rigenera tutti gli id salvati tranne i `dyn_*`. 25 report, 0 chiamate LLM, `semantic_cache.json` identico per md5. Compaiono report nuovi per gli experiment-id `*_excerpt`, `1A_sast_hint` e `*_rerun2610`.
  - Aggiunto ⚠️ sul retry per SGV in `architecture.md`; corretta la riga sui distinti in `status.md`.
- **doc-html** (subagent): `docs/documentazione_sistema.html` con `/crea-documentazione`; 5 diagrammi mermaid verificati con Chrome headless, tema chiaro e scuro, larghezza 390px non verificata; riga in `docs/README.md`. Nuove incoerenze trovate:
  - G4 non valida SC/SI/SA;
  - «DR» del paper (Cand/(TP+FP)) non è la «detection rate» dei report;
  - CVE-2026-47780 non è mai candidata (handler null), quindi un finding sulla regex conta FP;
  - nella modalità generica gosec/Semgrep ricevono la nota SonarQube (`utils/dynamic_task.py:240`);
  - `comparison.md` non si rigenera con experiment-id personalizzati.
  Tutte non corrette.
- Orchestratore: in `docs/pipeline_esecuzione.md` corretti i riferimenti a `config.py`, che erano spostati di +1 (`REPETITIONS` = 10), e il calcolo del verdetto, che usa il `total_score` del judge.

---

## 2026-10-22 — Decisioni D1/D2 e avvio degli agenti  [sessione: 74810fbc-7fbe-445d-9bef-258557bddc81]

**Intent:** «D1 10 / D2 non lo so preventivamente prendile tutte e due / le altre ok / io ti direi di fare da orchestratore lancia gli agenti assegnandoli il lavoro in parallelo».
**Decisioni:**
- D1: 10 repetition fisse per tutti i task (non le 5 proposte in call).
- D2: la tabella dell'articolo si fa su tutte e due le serie, luglio e `rerun2610`; la scelta si fa dopo, sui numeri.
- Il resto del piano è accettato così com'è.
**Divergenze:**
- A4, B1 e B3 vanno a un solo agente, perché toccano lo stesso file (`utils/evaluation_utils.py`).
- B2 si ferma all'inventario e alla stima del costo: le corse mancanti (rep 4-10) si lanciano solo dopo l'ok, perché consumano credito Ollama.
- C1 resta in coda finché non si chiudono A2, A5 e B2.
**Esito A3** (subagent `A3-modello-tempi`): misurato che le corse di ottobre sono 7-10 volte più veloci su UDR (latenza del primo tentativo da 65 a 8 s), a parità di prompt, lunghezza dell'output e client. Che il modello sia cambiato non si può dimostrare: abbiamo solo il tag, senza digest. Già dentro luglio la velocità varia di circa 6 volte. Nota: `.notes/analisi/2026-10-22-modello-ollama-tempi.md`.
- Divergenze dell'agente: usa i caratteri al secondo perché i `tokens` sono `null` in tutti i JSON (probabile lettura di `prompt_eval_count` su una risposta `ChatOpenAI`, `agents/agent_runner.py:51-52`, non verificato); come riferimento UDM senza hint di luglio usa `1A` del 14/07; propone, senza implementarle, la lettura corretta dei token e un'impronta del modello in ogni JSON.
**Esito A5** (subagent `A5-legenda`), in `.notes/report/2026-10-22-legenda-tabella-multitool.md`:
- TP = match per nome di funzione con `handler_functions` della GT (`utils/cvss_eval.py:156-176`), non passa dal judge.
- «10» = repetition con almeno una CVE; per linked UDR sul dataset corretto vale 9/10, non 10/10.
- «56» non è nella tabella 3tool: si chiede a Lorenzo.
- Difetto principale: i report per corsa contano ancora i match spuri 40249/40343, la tabella del doc 14 no, quindi i numeri divergono. Il punto è riportato in C1.
**Esito A1** (subagent `A1-doc-pipeline`): `docs/pipeline_esecuzione.md` (+ riga in `docs/README.md`) e il testo per Overleaf `.notes/report/2026-10-22-execution-pipeline-overleaf.tex` (compila con IEEEtran).
- Incoerenze fra il paper IEEE e il codice:
  - retry al massimo 2, non 3 (`MAX_RETRIES` conta gli attempt);
  - quando gli attempt finiscono si salva e si valuta comunque l'ultimo report (10 repetition su 96 con l'SGV ancora fallito);
  - il judge vede il sorgente;
  - sui task statici la rubrica è quella del `_sol.md` e nomina la debolezza;
  - il prompt di retry non contiene il feedback del judge;
  - G2 controlla solo il campo `function`.
- Divergenze dell'agente: non corregge `architecture.md`/`codemap/` (manca `check_sgv`, righe vecchie) e lo segnala soltanto; nel `.tex` descrive il comportamento del codice e lascia commenti `% NOTE`; l'esempio della pagina è costruito, non preso da una corsa vera; il rendering dei diagrammi mermaid non è verificato.
**Esito B2** (subagent `B2-inventario`): `utils/repetition_inventory.py` e `.notes/analisi/2026-10-22-inventario-repetition-d1.md`. Niente lanciato.
- UDR è già a 10 in tutte e due le serie.
- Alla serie del 16/10 mancano 28 rep su UDM (~6 min).
- La serie di luglio su UDM non si può completare nelle condizioni di luglio: il servizio è cambiato; il prompt di `1A` del 14/07 è cambiato per il commit `0fb13b5`; per PCF è cambiata una nota nel task.
- Divergenze dell'agente: token stimati come caratteri/4; i comandi P2/P3 sono lasciati commentati; consiglia di lanciare in sequenza.
**Esito A2** (subagent `A2-provenienza`): `.notes/report/2026-10-22-provenienza-numeri-paper-icai.md`. TP e FN della Tab. III tornano in 8 celle su 8, con una combinazione di corse non dichiarata da nessuna parte:
- il no hint viene dal tag `results-2026-07-14`, run `20260713T174027Z`, quindi senza SGV;
- UDR SAST usa 10 repetition, contro le 3 del no hint;
- in tutti e due i bracci c'è la correzione 40249/40343.
Scarti segnalati: FP deduplicati a mano (2 celle su 8 si ricostruiscono); Cand. UDR 5 contro 4 dello script; Tab. V no-hint 62% non si riproduce (54.2%); colonna CWE della Tab. II; CVSS di 47780 6.9 contro 4.9/7.1 nella GT.
- Divergenze dell'agente: script di ricalcolo nello scratchpad, non versionati; non aggiorna il doc 13 né lo script.
**Esito A4+B1+B3** (subagent `report-code`), in `utils/evaluation_utils.py`, test `tests/test_report_findings.py` (11/11, ricontrollati dall'orchestratore):
- A4: il dettaglio di un finding mostra solo il passo del reasoning che nomina la funzione; il resto sta in `<details>`. Test rosso prima (5 su 5), verde dopo.
- B1: l'intestazione dà gli intervalli di repetition per ogni run e un avviso ⚠️ se le repetition non sono 10.
- B3: vista «Distinct findings» costruita riusando `group` e il collegamento unmatched→CVE; per gli unmatched il conteggio è solo un limite superiore.
- Rigenerati i report UDR e UDM `1A_sast_hint_full`, usando solo la cache (md5 di `semantic_cache.json` invariato).
- Divergenze dell'agente: `config.REPETITIONS` passa da 3 a 10 e diventa la costante unica, anche come default di `main.py`; crea `tests/`, che prima non esisteva; aggiorna `architecture.md`, `status.md` e `codemap/05`; non tocca il manifest del codemap.

---

## 2026-10-22 — Call ITASEC: trascrizione divisa e piano d'azione  [sessione: 74810fbc-7fbe-445d-9bef-258557bddc81]

**Intent:** «la seguente trascrizione è divisa in due parti, separale [...] e poi la seconda parte che è di questo progetto crea un file con le cose discusse-da fare migliorie e formalizzare spiegare le cose [...] ma per ora delinea solo il piano d'azione e dividendolo in ciò che si può fare in parallelo e prevedendo un campo per poi farsi segnare quale agente si è incaricato di farlo».
**Divergenze:**
- La divisione è a «E qui adesso io poi tra cinque minuti vi lascio…»: prima c'è il sommario e il titolo della tesi CDT, dopo ITASEC. Tutte e due le parti stanno in `docs/supporto/calls/transcripts/`, anche la parte 1, che è di un altro progetto.
- Il piano (`.notes/piani/2026-10-22-piano-call-itasec.md`) aggiunge due decisioni da prendere prima di agire, non chieste: D1 = numero fisso di repetition, con tre opzioni; D2 = quali corse vanno nella tabella dell'articolo.
**Esito/Problemi:**
- Prima della call è stato chiarito nel codice: run = un lancio di `main.py` (`run_id`); `--repetitions N` = totale da raggiungere per ogni task ed experiment-id, e le repetition già salvate si saltano. Per questo UDR `1A_sast_hint_full` ha 3 run e 10 repetition.
- Il piano non è ancora eseguito.

---

## 2026-10-22 — Verifica push e corsa SonarQube del 16/10  [sessione: bb9f90ac-ea8d-4f3f-9f7e-30a529a4bdf7]

**Intent:** «ci sono cose da pushare?», poi «ma questi file servono per chi deve fare i confronti leggere i report?».
**Divergenze:** l'AI propone di pubblicare la corsa `1A_sast_hint_full_rerun2610` (SonarQube, 16/10) aggiungendola al doc 14, senza aver riletto la decisione del 16/10 che la tiene locale finché il team non decide. L'utente risponde «ok procedi».
**Esito/Problemi:**
- `dev` = `origin/dev`, nessun commit in sospeso; `main` indietro di 10+ commit rispetto a `dev`.
- Modifiche a doc 14, `status.md` e `generate_multitool_table.py` fatte, poi annullate prima del commit dopo aver riletto il DEVLOG; salvate come patch nello scratchpad della sessione. Righe esistenti delle tabelle invariate dopo la rigenerazione.
- Dato emerso (non pubblicato): con lo stesso prompt di luglio (`prompt_user` identico byte per byte), su UDR n=10 SonarQube oggi ha TP 4, prec. 0.065, 4/10 ripetizioni con almeno una CVE (senza SAST: 7, 0.101, 3/10). È l'unica corsa che trova la 40245 (2/10).
- `consistency.md` e `semantic_cache.json` contengono anche la corsa SonarQube: non committati.
- `poetry install --no-root` per sincronizzare il `.venv` (mancava `cvss`).

---

## 2026-10-16 — ITASEC 2027: braccio SAST a 3 tool, convertitore e corse  [sessione: a08af94f-f3ef-4807-becf-b09009bbcaf0]

**Intent:** l'utente passa il paper inviato (`IEEE_ICAI_TEMS_2026_...pdf`, radice del repo) e dice: «per le altre cose non mi hanno risposto quindi direi che possiamo partire».
**Decisioni:**
- Niente codice del file collegato nel prompt: l'utente accetta la proposta della entry precedente («ok ok ci sta»). Gli smell indiretti hanno solo l'aggancio alla riga di origine e il punto d'arrivo nel messaggio.
- Il team non ha risposto su indiretti e AMF/PCF: si procede con quanto proposto nel messaggio (aggancio all'origine, AMF/PCF non girati).
**Divergenze:**
- L'header del blocco SAST diceva «Most describe code-style issues [...] NOT security vulnerabilities», vero per SonarQube ma falso per questi alert (regole di sicurezza). Reso un pezzo variabile (`{dataset_note}`) letto dal JSON del dataset: vuoto per i 3 tool, testo originale per SonarQube. Il blocco SonarQube resta identico byte per byte (verificato sui 4 task contro `HEAD`). È comunque una differenza di prompt fra i due bracci, da dichiarare nel paper.
- Il convertitore non legge il ridotto del team: riparte dal JSON completo (316), riapplica il filtro e fallisce se la selezione differisce dal ridotto (`--check-reduced`). Esce identica, 16 alert.
- Il doppione gosec G115 (senza `origine_dato`) eredita l'aggancio del gemello CodeQL (L1842).
**Esito/Problemi:**
- Nuovo `utils/sast_unified_to_hint.py`, output `docs/sast_tools/analisi_statica_v4.2.1/hint_alerts_3tool.json` (UDR 12 righe, UDM 4, AMF/PCF 0). `config.SAST_HINT_DATASET_PATH` ora si sovrascrive da env var.
- Righe di origine controllate sui file GT: sono tutte letture di parametri della richiesta (`c.Params.ByName`, `strconv.ParseInt(c.Param("pduSessionId"))`).
- Dal paper: le ripetizioni non sono dichiarate; nel repo il braccio SonarQube è `1A_sast_hint_full` (UDR a 10 rip., prime 3 canoniche; UDM a 3). Corse lanciate con experiment-id `1A_sast3tool_full`, stessi numeri di ripetizioni.
- Il servizio hosted oggi risponde in ~10–30 s a ripetizione (luglio: 4–16 min). Prompt verificato identico a luglio fuori dal blocco SAST, quindi non è input troncato.
- **Divergenza:** visto il cambio di servizio, l'AI ha rifatto lo stesso giorno anche la corsa senza SAST (`1A_no_hint_full_rerun2610`) e quella SonarQube, senza chiedere: era il «baseline opzionale» proposto prima, e il costo era sceso da ~1 h a pochi minuti. Il primo lancio non è partito per un errore nel ciclo zsh (`set -- $t` non spezza le parole), rilanciato con comandi espliciti.
- Esito (tabelle e lettura in `docs/sgv_protocol/14_braccio_sast_multitool.md`): su UDR a 10 rip. i 3 tool trovano almeno una CVE in 7/10 ripetizioni contro 3/10 senza SAST, precisione 0.200 contro 0.101, stesse CVE distinte. UDM: CVE trovata ovunque, FP distinti 11 → 8 con gli alert.
- **Decisione del team (Francesco):** sugli smell indiretti chiede l'opposto della proposta: «aggiungiamo alla fine del file la porzione dei file collegati, poi mettiamo qualche frase di spiegazione»; AMF/PCF: «ci bastano i vecchi risultati». L'utente accetta di farlo come variante in più, tenendo la corsa senza codice collegato («si»).
- Variante con codice collegato: `--with-linked-code` nel convertitore porta le ~11 righe di `contesto` del report attorno a ogni destinazione (6 snippet, deduplicati), accodate dopo gli alert con una frase che le dichiara contesto e chiede di riportare i finding sul file in revisione (**divergenza**: la frase è dell'AI). Gli snippet sono blocchi ```go, quindi SGV li conta come codice mostrato. Experiment-id `1A_sast3tool_linked_full`. Blocchi SonarQube e 3 tool riverificati identici.
- Esito variante con codice collegato: su UDR 9/10 ripetizioni con almeno una CVE, precisione pooled 0.364 (3 tool senza codice 0.200, senza SAST 0.101); CVE distinte sempre 3/6; nessun finding sulle funzioni degli snippet. UDM invariato.
- Nuovo `utils/generate_multitool_table.py`; aggiornati `status.md`, `architecture.md`, `docs/README.md`. Nessun commit né tag `results-*` (`results/` non si committa senza richiesta).
- **Decisione sulla presentazione:** l'utente propone «dato che ormai l'altro documento lo hanno pubblicato per non mettere dubbi lascerei stare i risultati che abbiamo ottenuto oggi, usiamo quelli del paper e mostriamo le cose nuove solo». L'AI obietta che 3 tool di oggi contro baseline di luglio dà un guadagno falso (senza SAST: 1/6 a luglio, 3/6 oggi = 3 tool) e propone: 3 tool (con e senza codice collegato) confrontati solo col senza SAST dello stesso giorno, SonarQube citato come lavoro precedente senza confronto diretto. L'utente accetta («dammi il msg»).
- **Decisione sulla pubblicazione** (repo pubblica, push con tag per condividere col team): l'utente sceglie di pubblicare solo il nuovo. La corsa SonarQube del 2026-10-16 e il confronto con la Tabella III restano in locale finché il team non decide; doc 14 e `utils/generate_multitool_table.py` riscritti sulle sole tre corse dello stesso giorno. Aggiunto `.notes/` a `.gitignore`.

---

## 2026-10-16 — ITASEC 2027: ricezione analisi statica a 3 tool, stima del rerun  [sessione: 74f260f4-fd3f-4a58-b470-5dede5ce5136]

**Intent:** il team (Francesco, Mariano, Andrea) vuole ripresentare il paper SAST+LLM a ITASEC 2027 (scadenza 30 ottobre) con gli smell di gosec, Semgrep e CodeQL al posto dei soli SonarQube. Richiesta dell'utente: «capisci dove spostarla [...] prima di partire col lavoro vero cercherei di capire se dobbiamo allineare qualcosa, poi dare le stime».
**Esito/Problemi:**
- Zip estratta in `docs/sast_tools/analisi_statica_v4.2.1/` (accanto al vecchio dataset SonarQube). La zip resta nella radice, ignorata da git.
- Il JSON unificato contiene **316** segnalazioni (non 326) e **solo gosec/Semgrep/CodeQL**: SonarQube è escluso perché per Go non ha regole di sicurezza (RELAZIONE §3). Nel messaggio al team si parlava di «3 tool più SonarQube».
- La versione ridotta ha 16 smell (UDR 5 nel file + 6 indiretti più il doppione gosec, UDM 2+2, AMF/PCF 0). Le 7 righe nel file corrispondono **riga per riga** ai nostri file GT: la scansione v4.2.1 è sulla stessa versione dei task.
- Gli smell «indiretti» stanno in file che l'agente non vede; il loro `origine_dato` invece è una riga del file GT. È la decisione di metodo da prendere prima di lanciare.
- Tempi misurati sulla corsa vecchia (`task6_vuln_udr_full`, 1A_sast_hint_full): circa 16 minuti per 3 ripetizioni.
- Dei 16 smell ridotti, 15 sono di CodeQL e 1 di gosec (indiretto); Semgrep non ne ha nessuno sui file GT.

**Divergenze:** l'AI aveva scritto che SonarQube era stato «sostituito». L'utente corregge: è assente perché è già stato usato nel paper precedente.
**Decisioni:**
- AMF/PCF (0 smell): l'utente propone di non farli girare, per i tempi stretti. L'AI è d'accordo.
- Task e ripetizioni: si chiede al team il paper finale inviato, invece di ricostruirli dall'Overleaf.
- Braccio unico con gli alert dei tre tool insieme: **accettato**.
- Smell indiretti agganciati alla riga di `origine_dato` nel file GT, con il punto d'arrivo nel messaggio: **accettato**. L'utente chiede se dare all'agente anche il codice collegato: l'AI consiglia di no, perché cambierebbe l'input rispetto al braccio SonarQube. In attesa di conferma.
- Ricontrollo del ridotto: ricostruito dal JSON completo (316) con il filtro «file GT oppure `origine_dato` nel file GT», esce identico (15 CodeQL più il doppione gosec senza `origine_dato`).

---
