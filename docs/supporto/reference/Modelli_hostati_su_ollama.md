---
title: "Cloud models"
source: "https://ollama.com/search?c=cloud"
author:
published:
description: "Cloud models on Ollama - aggiornato al 16 luglio 2026."
tags:
  - "clippings"
updated: "2026-07-16"
---

# Modelli Cloud Ollama: stato di disponibilità gratuita

> Nota: tutti i modelli "cloud" di Ollama restano **utilizzabili gratuitamente tramite API key** (nessun costo per token). Il livello di "Usage" (Low/Medium/High/Extra High) indica solo il grado di rate-limiting applicato, non un costo. Ollama però **ritira periodicamente** i modelli più vecchi: il 15 luglio 2026 è stata effettuata una tornata massiccia di deprecazioni.

## ✅ Modelli ancora attivi e gratuiti

| Modello | Link | Note |
|---|---|---|
| deepseek-v4-pro:cloud | [Link](https://ollama.com/library/deepseek-v4-pro) | Attivo |
| deepseek-v4-flash:cloud | [Link](https://ollama.com/library/deepseek-v4-flash) | Attivo, sostituto di deepseek-v3.1 e v3.2 |
| kimi-k2.6:cloud | [Link](https://ollama.com/library/kimi-k2.6) | Attivo |
| kimi-k2.5:cloud | [Link](https://ollama.com/library/kimi-k2.5) | Attivo |
| kimi-k2.7-code:cloud | [Link](https://ollama.com/library/kimi-k2.7-code) | Nuovo, non presente nella lista precedente |
| glm-5.1:cloud | [Link](https://ollama.com/library/glm-5.1) | Attivo |
| glm-5.2:cloud | [Link](https://ollama.com/library/glm-5.2) | Nuovo, sostituto di glm-4.7 e glm-5 |
| mistral-large-3:675b-cloud | [Link](https://ollama.com/library/mistral-large-3) | Attivo, sostituto consigliato per devstral-2:123b |
| qwen3.5:cloud | [Link](https://ollama.com/library/qwen3.5) | Attivo (qwen3.5:397b è il sostituto di qwen3-coder-next e qwen3-coder:480b) |
| minimax-m2.7:cloud | [Link](https://ollama.com/library/minimax-m2.7) | Attivo |
| minimax-m2.5:cloud | [Link](https://ollama.com/library/minimax-m2.5) | Attivo |
| minimax-m3:cloud | [Link](https://ollama.com/library/minimax-m3) | Nuovo, sostituto di minimax-m2, minimax-m2.1 e gemini-3-flash-preview |
| nemotron-3-super:cloud | [Link](https://ollama.com/library/nemotron-3-super) | Attivo |
| nemotron-3-ultra:cloud | [Link](https://ollama.com/library/nemotron-3-ultra) | Nuovo |
| nemotron-3-nano:30b-cloud | [Link](https://ollama.com/library/nemotron-3-nano) | Attivo |
| gemma4:31b-cloud | [Link](https://ollama.com/library/gemma4) | Attivo, sostituto di gemma3:4b/12b/27b |
| gpt-oss:20b-cloud | [Link](https://ollama.com/library/gpt-oss) | Attivo |
| gpt-oss:120b-cloud | [Link](https://ollama.com/library/gpt-oss) | Attivo |

## ❌ Modelli ritirati il 15 luglio 2026

| Modello ritirato | Sostituto consigliato |
|---|---|
| deepseek-v3.1:671b | deepseek-v4-flash |
| deepseek-v3.2 | deepseek-v4-flash |
| devstral-2:123b | mistral-large-3:675b |
| devstral-small-2:24b | — |
| ministral-3:14b | — |
| ministral-3:3b | — |
| ministral-3:8b | — |
| gemini-3-flash-preview | minimax-m3 |
| gemma3:12b | gemma4:31b |
| gemma3:27b | gemma4:31b |
| gemma3:4b | gemma4:31b |
| glm-4.7 | glm-5.2 |
| glm-5 | glm-5.2 |
| minimax-m2.1 | minimax-m3 |
| qwen3-coder-next | qwen3.5:397b |
| qwen3-coder:480b | qwen3.5:397b |

## ❌ Modelli ritirati in precedenza (giugno 2026)

| Modello ritirato | Data ritiro | Sostituto consigliato |
|---|---|---|
| rnj-1:8b | 30 giugno 2026 | — |
| kimi-k2-thinking | 16 giugno 2026 | kimi-k2.6 |
| kimi-k2:1t | 16 giugno 2026 | kimi-k2.6 |
| minimax-m2 | 16 giugno 2026 | minimax-m3 |
| glm-4.6 | 16 giugno 2026 | glm-5.1 |
| qwen3-next:80b | 16 giugno 2026 | qwen3.5 |
| qwen3-vl:235b | 16 giugno 2026 | qwen3.5 |
| qwen3-vl:235b-instruct | 16 giugno 2026 | qwen3.5 |
| cogito-2.1:671b | 16 giugno 2026 | deepseek-v4-flash |

## Come funziona il ritiro dei modelli

Ollama comunica in anticipo (email e sito) le deprecazioni dei modelli cloud, mentre i modelli locali non sono mai affetti da questi ritiri. Il ritiro non riguarda il costo (resta gratuito), ma la disponibilità: i tool che puntano a un modello ritirato smettono di funzionare e vanno aggiornati verso il modello sostitutivo indicato.

## Come restare aggiornati

Per un elenco sempre corrente, la pagina ufficiale da consultare è `https://ollama.com/search?c=cloud`, mentre lo stato dei ritiri (passati e futuri) è documentato su `https://docs.ollama.com/cloud`.
