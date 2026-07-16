---
name: aggiorna-modelli-ollama
description: >
  Skill per aggiornare un documento Markdown che elenca i modelli hostati
  su Ollama (variante :cloud), verificandone la disponibilità gratuita,
  il livello di Usage (rate-limit) e le eventuali deprecazioni/sostituzioni.
  Usa ricerca web + lettura di pagine ufficiali Ollama, non solo dati locali.
triggers:
  - "aggiorna file modelli ollama"
  - "verifica modelli ollama gratuiti"
  - "controlla usage modelli ollama"
  - "trova nuovi modelli cloud ollama"
---

# Skill: Aggiornamento elenco modelli cloud Ollama

## Obiettivo
Mantenere aggiornato un file Markdown (es. `Modelli_hostati_su_ollama.md`) che
elenca i modelli `:cloud` disponibili su Ollama, il loro stato di disponibilità
gratuita, il livello di Usage, e le sostituzioni in caso di ritiro.

## Perché è necessario un LLM (non solo uno script)
Ollama non fornisce un'API pubblica strutturata con stato "gratuito",
"usage tier" e "motivo ritiro/sostituto" in un unico endpoint. Queste
informazioni vivono in testo libero su:
- pagina di ricerca `https://ollama.com/search?c=cloud` (richiede JS/SSR, spesso non fetchabile direttamente)
- pagine singolo modello `https://ollama.com/library/<nome>`
- documentazione `https://docs.ollama.com/cloud` (sezione Retirements)
- blog ufficiale `https://ollama.com/blog` e changelog GitHub

Interpretare "questo modello è stato ritirato, il sostituto è X" richiede
ragionamento semantico su fonti eterogenee: è un compito da LLM+ricerca web,
non da parsing deterministico.

## Cosa può invece essere scriptato (supporto opzionale)
- Scraping dell'elenco nomi modelli/tag via HTML o API terze (es. ollamadb.dev,
  ollama-models-api) per ottenere una lista grezza da confrontare.
- Diff automatico tra la lista precedente (dal file .md esistente) e la nuova
  lista grezza, per segnalare all'LLM solo le voci cambiate.
- Questi script NON determinano da soli "gratuito sì/no", "Usage tier" o
  "sostituto consigliato": servono solo a restringere il perimetro di ricerca.

## Procedura step-by-step

1. **Leggi il file esistente**
   Estrai la lista attuale di modelli (nome, tag, categoria Usage, link).

2. **Ricerca web per aggiornamenti**
   Esegui query mirate:
   - "ollama cloud models list [mese] [anno]"
   - "ollama docs.ollama.com/cloud retirements"
   - "ollama blog nuovi modelli cloud"
   Obiettivo: individuare (a) modelli ritirati, (b) modelli nuovi, (c) cambi di Usage tier.

3. **Fetch pagine ufficiali**
   Recupera il contenuto di:
   - `https://docs.ollama.com/cloud` (sezione retirements/sostituzioni)
   - `https://ollama.com/blog/cloud-models`
   - pagine singolo modello per confermare tag `:cloud`, contesto, licenza, parametri

4. **Verifica ogni modello della lista originale**
   Per ciascuna voce: è ancora nella libreria ufficiale? Ha tag `:cloud`?
   È stato deprecato? Se sì, qual è il sostituto indicato da Ollama stesso?

5. **Cerca modelli nuovi non presenti nel file**
   Confronta la lista aggiornata con quella originale; aggiungi solo modelli
   con tag `:cloud` ufficiale confermato (scarta mirror community non ufficiali,
   es. repository utente tipo `nomeutente/modello-cloud`).

6. **Aggiorna il documento Markdown**
   Mantieni la struttura esistente (tabelle per categoria Usage), aggiungi
   sezione "Modelli ritirati" con sostituti, aggiorna frontmatter con data.

7. **Scrivi output**
   Salva il file aggiornato mantenendo lo stesso nome, pronto per il download.

## Note importanti
- "Usabile gratuitamente" per i modelli cloud Ollama significa nessun costo
  per token; il livello di Usage indica solo il rate-limit applicato, non un prezzo.
- Non aggiungere mai modelli senza tag `:cloud` ufficiale confermato nella
  libreria principale, anche se esistono varianti locali o mirror community.
- Citare sempre la fonte (pagina ufficiale o blog) per ogni ritiro/sostituzione riportata.