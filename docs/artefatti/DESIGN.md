# Pagine HTML della documentazione — convenzioni

Le pagine di `docs/artefatti/` si aprono da file (`open docs/artefatti/index.html`), senza
server e senza pubblicazione; l'unica risorsa di rete sono i font da Google Fonts, con
ripiego sui font di sistema.

## Struttura

```text
docs/artefatti/
├── DESIGN.md          questo file
├── index.html         rimanda a 01_sistema.html
├── NN_<nome>.html     una pagina per argomento; NN è l'ordine di lettura
├── stile.css          token dei due temi e stili delle pagine (un solo file per tutte)
├── nav.css / nav.js   menu laterale, bottone del tema, precedente/successivo
├── theme.js           applica il tema scelto prima del disegno (nell'<head>)
├── diagrammi.js       disegna i blocchi mermaid nei colori del tema
└── vendor/            mermaid.min.js in locale
```

Ogni pagina carica nell'`<head>` `theme.js`, `stile.css` e `nav.css`, e in fondo
`nav.js`; se ha diagrammi, prima di `nav.js` anche `vendor/mermaid.min.js` e
`diagrammi.js`. **Una pagina nuova** è un file `NN_<nome>.html` più una riga in
`CAPITOLI` dentro `nav.js`: numero del file e posizione nell'elenco devono coincidere. Il
menu mostra sotto la pagina aperta le sue `section[id]` con un `h2`.

`11_confronto.html` è **generata** e resta fuori da git (`.gitignore`), perché contiene corse non destinate al repo pubblico. Non si modifica a mano: si rigenera con
`poetry run python -m utils.generate_mega_comparison --html docs/artefatti/11_confronto.html`
(il markdown passa da `utils/md_to_artefatto.py`, che usa lo stesso scheletro).

## Contenuto

- Si scrive con la skill `/crea-documentazione`: il perché prima del come, un solo esempio
  corrente (UDR, braccio a 3 tool, presentato in `01_sistema.html`), componenti con il nome
  del codice, ogni affermazione con il suo `file:riga`.
- L'esempio sta in `<p class="esempio">` o `<div class="esempio">`: barra ed etichetta
  «Nell'esempio» le mette lo stile.
- Le pagine rimandano solo all'indietro; fa eccezione il rimando a `09_divergenze.html`
  nella panoramica.
- Il testo dell'articolo IEEE ICAI-TEMS che non coincide con il codice sta solo in
  `09_divergenze.html`, mai nel testo delle altre pagine.
- Quando il codice cambia, i `file:riga` invecchiano: si ricontrollano sulle pagine che
  descrivono il file toccato.

## Aspetto

- **Token** in `stile.css` (`--bg --surface --border --text --text-dim --accent
  --accent-soft --accent-text --warn --warn-soft --code-bg`), accento blu (`#2456a6` chiaro,
  `#7ea6ee` scuro). I componenti usano solo i token; il tema scuro ridefinisce i token sotto
  `prefers-color-scheme` (con guardia `:root:not([data-theme="light"])`) e sotto
  `:root[data-theme="dark"]`. Il bottone del tema salva la scelta in `localStorage`
  (`mas-tema`).
- **Font**: IBM Plex Sans per il testo (17px, interlinea 1.6), IBM Plex Mono per codice,
  sopratitoli e intestazioni di tabella.
- **Colonna** `.wrap` di 700px di testo; `.wrap.largo` (1180px) solo per le pagine di
  tabelle come il confronto. Tabelle in `<div class="tab">`, che scorre in orizzontale: la
  pagina non scorre mai.
- **Riquadri**: `dl.breve` per chi è / a cosa serve (solo nella panoramica), `.avviso` per
  ciò che chi legge non deve fraintendere.

## Diagrammi

- Markup: `<figure><pre class="mermaid">…</pre><figcaption>…</figcaption></figure>`, subito
  dopo il paragrafo che descrive lo stesso meccanismo.
- `flowchart LR` per i flussi con archi di ritorno, decisioni come esagoni (`{{"…"}}`),
  etichette di due o tre righe con `<br/>`, ogni arco di un ciclo con il suo limite letto nel
  codice («no, attempts &lt; 3»).
- La figura è larga almeno quanto la colonna e si allarga fino allo spazio libero ai lati;
  oltre, l'SVG si riduce in proporzione (`nav.css`, `stile.css`).
- **Controllo**: una schermata con Chrome headless a 1440px
  (`--headless=new --window-size=1440,2400 --virtual-time-budget=8000 --screenshot=…`), e
  una stretta se il diagramma è largo: nessuna etichetta tagliata. Chrome headless non scende
  sotto i 500px di finestra, quindi una schermata «a 420px» è una pagina da 500 tagliata.
