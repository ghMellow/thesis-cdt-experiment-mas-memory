---
name: feedback-poetry
description: Il progetto usa Poetry — tutti i comandi Python vanno prefissati con poetry run
metadata:
  type: feedback
---

Usare sempre `poetry run python main.py ...` invece di `python main.py ...`.

**Why:** il progetto gestisce le dipendenze con Poetry e l'ambiente virtuale è attivato tramite `poetry run`.

**How to apply:** ogni volta che fornisco un comando CLI per eseguire script Python in questo progetto.
