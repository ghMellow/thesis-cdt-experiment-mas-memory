# Proposta: evoluzione della rubrica con CVSS — stato della discussione

> **Scopo del documento:** allineare il team sulla direzione emersa dalla call del 2026-07-08 (decima call) prima di iniziare l'implementazione. Contiene l'impianto proposto, i punti ancora aperti e alcune segnalazioni sui dati ricevuti (`cve_metrics (1).json`). Commenti e correzioni benvenuti — da qui si parte.

**Data:** 2026-07-08 · **Autore:** Nicolò (con supporto AI) · **Riferimenti:** call 9 (2026-07-07), call 10 (2026-07-08)

---

## 1. Il quadro: due fasi

| | **Fase 1 — esperimento chiuso (ora)** | **Fase 2 — senza ground truth (CDT)** |
|---|---|---|
| Contesto | 4 file free5GC, 10 CVE note (GT di Lorenzo) | Cognitive Digital Twin: analisi su variazioni di codice non note a priori |
| Rubrica testuale | strumento di **valutazione** (derivata dalla GT) | solo **spiegazione leggibile** del finding (non può validare ciò da cui deriva) |
| CVSS | metrica di **accuratezza**: confronto deterministico con lo score/vettore reale | **struttura di output standard + trigger di severità** ("ho trovato una cosa da 8.7 → approfondisci") |
| Validazione | rubrica + confronto CVSS con GT | judge di **coerenza interna** sul vettore + segnali esterni indipendenti (diff di codice, SonarQube, dati runtime) |

Il punto chiave della fase 2: il CVSS auto-assegnato dal modello è **standardizzato ma non oggettivo** — un vettore ben formato non garantisce che la vulnerabilità esista. Senza GT l'oggettività si surroga con: (a) un judge che chiede conto di ogni metrica ("hai messo AV:N — quale superficie di rete espone il codice?"), (b) triangolazione con segnali che non provengono dal modello.

## 2. Rubrica v2 — due blocchi, valutazione ibrida

**Blocco A — semantico (esistente, invariato).** I 4 criteri attuali per CVE (identificazione 0–3, localizzazione 0–2, impatto 0–2, fix 0–2, totale 9), generati da Claude a partire dalla GT. Restano perché comprensibili e perché mantengono la confrontabilità con i run già fatti. Valutati dal **judge LLM**.

**Blocco B — CVSS (nuovo, identico per tutte le CVE).** L'unica parte già concordata in call: il classificatore emette, oltre alla risposta testuale, una stima CVSS strutturata (score e/o vettore), da confrontare con quella reale. *Come* fare il confronto è invece rimasto aperto ("giocateci un po', vediamo come si può fare"); in call sono circolate due ipotesi, che misurano cose diverse e quindi non si escludono:

- **Confronto sullo score** (ipotesi di Andrea, a fasce: "se il numero è 4.8 e stai fra 3.8 e 5.8, un punteggio, e via dicendo"): misura se il modello ha capito *quanto* è grave. Semplice, ma è un aggregato — si può azzeccare uno score per la ragione sbagliata, con un vettore diverso che produce un numero simile (e nel dataset 5 CVE su 10 valgono 8.7).
- **Confronto sul vettore** (preferenza di Mariano: "punteggio e vettore"): campo per campo, binario ("hai centrato o meno il vettore"), misura se il modello ha capito *perché* è grave — quale impatto, quale via d'attacco. Più informativo ma da tarare, vedi nota sotto.

Proposta di partenza (da confermare col team): iniziare dallo score a fasce, aggiungere il confronto sul vettore appena i dati normalizzati sono pronti — il costo di calcolarli entrambi è comunque basso, essendo script. Fasce e punteggi esatti sono da tarare, quelli scritti qui sono solo esempi.

> ⚠️ **Nota per la taratura del confronto sul vettore, da un'osservazione di Mariano in call** ("per free5GC i parametri saranno tutti uguali, il sistema è quello — la cosa che cambia è nella box degli impatti"): nel dataset le 5 metriche di exploitability sono quasi costanti (AV:N/AC:L/AT:N/PR:N/UI:N per 9 CVE su 10; solo la 47780 ha PR:L). Un conteggio piatto sugli 8 campi regalerebbe quindi ~5 punti a qualsiasi risposta "di default". Se si fa il vector match, meglio due sotto-conteggi: exploitability (0–5) e **impatto VC/VI/VA (0–3)** — è quest'ultimo che discrimina davvero tra le CVE del dataset.

Il Blocco B **non passa per il judge LLM**: score e vettore si confrontano con uno script Python deterministico, come già avviene per i task matematici. È il "parametro riconosciuto e non delegato all'LLM" discusso in call, e rende la parte standardizzata della valutazione indipendente da qualsiasi giudizio di modello.

**Report: i due sub-score restano separati** (non solo sommati). Motivi: (1) confrontare esperimento 2 vs 2b senza che il nuovo blocco inquini il vecchio; (2) misurare la correlazione tra qualità semantica e accuratezza CVSS — un risultato in sé per l'articolo.

## 3. Ruolo di SonarQube (esperimento 3 e oltre)

Stesso oggetto, due mestieri:

- **Fase 1 (esperimento 3):** output di Sonar come **hint in input** al prompt del classificatore; si misura il delta sugli score con/senza, a parità di tutto il resto. Prerequisito: la "valutazione manuale di SonarQube" sulle 9+1 CVE, per sapere quanto overlap c'è tra i finding di Sonar e la GT — se Sonar segnala già direttamente la vulnerabilità, l'esperimento misura "comprensione di un report", non "scoperta assistita" (risultato comunque valido, ma da dichiarare). Atteso overlap basso: molte CVE sono logiche/di configurazione (regex, CORS, return mancanti), terreno dove i tool statici classici arrivano male — il che rende il dato interessante.
- **Fase 2 (CDT):** Sonar passa a valle come **verificatore indipendente** — finding del modello corroborato da un warning di Sonar sulla stessa porzione di codice vale più di un finding solo. L'integrazione tecnica (parsing output, mapping sui file) costruita in fase 1 si riusa qui.

## 4. Contratto dati: uno schema unico

GT, output del classificatore e rubrica devono parlare la stessa lingua. Schema per CVE (il JSON ricevuto è già molto vicino):

```json
{
  "id": "CVE-...", "url": "...", "ghsa": "GHSA-...",
  "network_function": "UDR|PCF|AMF|UDM",
  "task_id": "task6", "source_file": "...",
  "root_cause": "...",
  "cvss": { "version": "4.0", "vector": "...", "base_score": 0.0,
            "score_type": "B|BT", "cvss_source": "NVD|CNA",
            "base_metrics": { "AV": "...", "AC": "...", "AT": "...", "PR": "...", "UI": "...",
                              "VC": "...", "VI": "...", "VA": "...",
                              "SC": "...", "SI": "...", "SA": "..." },
            "threat_metrics": { "E": "..." } }
}
```

I dati restano **completi** (tutte le 11 metriche base CVSS 4.0, più la E dove presente): l'esclusione di SC/SI/SA e E riguarda solo lo *script di confronto*, non il dataset. Una legenda unica in `_meta` (nome esteso + spazio completo dei valori per ogni metrica, es. AV:N = Network ma PR:N = None) sostituisce i `name`/`value_label` ripetuti per entry del file originale, ed è riusabile com'è nel prompt del classificatore quando dovrà scegliere i valori — senza rivelare nulla della GT.

Il classificatore emetterà lo stesso sotto-oggetto `cvss` per ogni finding: in fase 1 lo si confronta con la GT, in fase 2 la stessa struttura sopravvive come formato di output — è il ponte tra le due fasi.

## 5. Punti aperti (decisioni da prendere insieme)

1. **Come confrontare la stima CVSS** (il punto lasciato esplicitamente aperto in call): solo score a fasce, solo vettore campo per campo, o entrambi — e con quali fasce/pesi. Vedi le due ipotesi in §2.
2. **Soglia di accettazione:** proposta — soglia invariata sul solo Blocco A (confrontabilità con i run passati); Blocco B riportato come metrica separata senza gate, almeno nel primo giro.
3. **Chi stima il CVSS:** in call Andrea ha chiarito ("servono tutti e due: all'inizio devi sapere qual è quello reale, poi dai punteggi in funzione di quanto si avvicina") — quindi: CVSS reale precalcolato come riferimento + stima del classificatore da confrontare. È esattamente lo schema del Blocco B; il judge che fa una *terza* stima indipendente resta un esperimento ulteriore, non il primo passo.
4. **Perimetro delle metriche nel confronto:** solo le 8 (escluse le Subsequent SC/SI/SA come detto in call, ed esclusa la Threat E — vedi segnalazione §6.2). Nel *dataset* restano comunque tutte le 11 + E: l'esclusione vale per lo script di valutazione, non per i dati.
5. **CVE-2026-47780 (la regex `|.+`):** in call si era detto "nove di questi oggetti" (la decima non ha ancora score NIST), ma il JSON consegnato la include già con il vettore dichiarato dalla CNA. Proposta: tenerla nel dataset con il vettore CNA, marcandola (`cvss_source: "CNA"`) per poterla distinguere o escludere nelle analisi.

## 6. ⚠️ Segnalazioni sui dati ricevuti

Dal confronto incrociato tra `cve_metrics (1).json` e `CVE_CVSS.md` (vettori e score coincidono, il problema è solo nelle etichette):

### 6.1 Shift delle etichette nel JSON

I campi `network_function` e `root_cause` del JSON sono **disallineati di una posizione** a partire da CVE-2026-47780:

| CVE | Score | JSON dice | Dovrebbe essere (da MD/call) |
|---|---|---|---|
| 47780 | 4.9 | PCF, CORS→DoS ✗ | **regex `\|.+` (GHSA-6gxq-gpr8-xgjp)** — lo conferma l'`url` della entry stessa |
| 41135 | 8.7 | AMF, no default case ✗ | **PCF, CORS DoS** (coerente col vettore: solo VA:H = DoS puro) |
| 41136 | 5.5 | UDM, IsValidSupi ✗ | **AMF, missing default case** |
| 42459 | 7.7 | null, "Non specificata" ✗ | **UDM, missing validator.IsValidSupi()** |

La entry 47780 si contraddice da sola: `root_cause: "CORS"` ma `url: GHSA-6gxq-gpr8-xgjp` (la regex ReDoS). Chiediamo conferma dell'allineamento corretto — in particolare per 42459.

**Bozza di file normalizzato già pronta** (da validare): `File_Free5gc_Vulnerabili/cve_metrics_normalized.json` — etichette corrette; vettori, score e tutte le 11 metriche invariati (verificato via script); più i campi aggiunti: `task_id`, `source_file`, `ghsa`, `cvss_source` (NVD/CNA), `score_type` (B/BT), `threat_metrics`, e una legenda unica delle metriche in `_meta` (al posto dei `name`/`value_label` ripetuti per entry). L'header `_meta` elenca le 4 correzioni applicate, così la verifica è immediata.

### 6.2 Tre vettori includono la metrica Threat (E)

47780 (`E:U`), 41136 (`E:P`), 42459 (`E:P`): i loro score (4.9, 5.5, 7.7) sono quindi **CVSS-BT**, non base puri — senza la E verrebbero più alti. Proposta: far stimare al modello solo le 8 metriche base + score B (la Exploit Maturity dipende da threat intelligence esterna, non deducibile dal codice — non sarebbe un test equo) e ricalcolare per queste tre CVE lo score B di riferimento. Alternativa: tenere gli score BT del file, accettando che per quelle tre il confronto sia strutturalmente penalizzato.

### 6.3 Mapping CVE → task/file — ✅ risolto nella bozza normalizzata

Per automatizzare il confronto serve sapere quale CVE appartiene a quale task (5–9) e a quale file sorgente. Già aggiunto in `cve_metrics_normalized.json` (campi `task_id`/`source_file`, ricavati dai riferimenti GHSA nei task solution: 6 UDR → task6/`api_datarepository.go`, PCF → task5/`api_oam.go`, AMF → task7/`api_communication.go`, UDM → task8/`api_subscriberdatamanagement.go`; la 47780 resta senza task perché non coperta dai task 5–9). Da validare insieme al resto.

---

## 7. Valutazione critica (Nicolò) — tre rischi da discutere

Oltre a riportare la direzione della call, tre osservazioni mie su cosa rischiamo di perdere:

1. **Potere discriminante limitato del Blocco B su questo dataset.** 10 CVE, exploitability identica per 9/10, score concentrati (cinque 8.7, due 6.9): un modello che rispondesse sempre "AV:N/AC:L/AT:N/PR:N/UI:N + impatto High" andrebbe vicino al massimo senza aver capito nulla. Con 10 punti dati non si separa "stima bene il CVSS" da "ha imparato il prior di free5GC". Il CVSS vale come standardizzazione del formato e ponte verso la fase 2 — ma il risultato forte dell'esperimento resta il Blocco A + la detection. Da dire chiaramente nell'articolo.
2. **Le fasce di prossimità vanno calibrate sul disaccordo tra umani.** Lo score pubblicato non è verità esatta: per la 47780 il vettore CNA e quello NIST differiscono (visto in call). Se due enti ufficiali divergono, una fascia "ottima" di ±0.5 punisce come errore quello che è rumore di assegnazione. Proposta: usare il delta CNA-vs-NVD osservabile come riferimento per la larghezza delle fasce.
3. **Un dettaglio operativo di fase 1 da definire prima di scrivere il codice: l'abbinamento risposta↔CVE.** Non c'entra con la fase 2 né con nuove scoperte — è puro meccanismo del confronto con la GT. Il caso concreto: task6 ha **6 CVE nello stesso file**; lo script del Blocco B deve confrontare ogni stima CVSS con lo score della CVE *giusta*. Per i task con 1 sola CVE (5, 7, 8) il problema non si pone; per task6 e task9 (cross) sì.

   **Soluzione proposta, a due livelli:**
   - *Livello 1 (deterministico):* abbinamento per **funzione/handler** citato nel finding — le 6 UDR sono lo stesso pattern in funzioni diverse. Via script, il Blocco B resta deterministico.
   - *Livello 2 (judge come fallback):* per i soli casi ambigui l'abbinamento lo decide il giudice LLM, e la scelta viene sempre loggata nel report per essere verificabile.

   > ✅ **Risolto autonomamente (2026-07-08):** la corrispondenza individuale CVE↔GHSA↔handler è stata ricostruita interrogando la **GitHub Advisory API** (ogni advisory dichiara il proprio `cve_id` e l'endpoint colpito) e incrociando con le funzioni dei file sorgente. È nei campi `handler_functions` / `in_task_excerpt` del normalizzato, verificata via script (ogni funzione esiste nel rispettivo file). Nessuna richiesta dati aggiuntiva necessaria — solo conferma insieme al resto.

   Nota collegata, ora quantificata: nel task6 sono **visibili solo 3 delle 6 CVE UDR** (40246/40247/40248); 40245, 40249 e 40343 stanno in handler fuori dall'estratto e **non vanno contate come miss**. Corollario: i finding che non si abbinano a nessuna CVE della GT non si mescolano agli score — si contano a parte (in fase 1 basta il conteggio, senza valutarli).

## Prossimi passi proposti

1. Conferma del team su: impianto a due blocchi (§2), punti aperti (§5), allineamento etichette (§6.1), scelta B vs BT (§6.2), mapping CVE↔GHSA↔handler ricostruito dalla GitHub Advisory API (§7.3)
2. Nicolò produce `cve_metrics_normalized.json` (etichette corrette + mapping task/file + eventuale ricalcolo score B)
3. Implementazione esperimento 2b: schema output classificatore + script di confronto CVSS + report a sub-score separati
4. In parallelo: valutazione manuale SonarQube sulle 10 CVE (prerequisito esperimento 3)
