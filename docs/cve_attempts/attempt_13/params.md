# Attempt #13 — Parametri

| Parametro | Valore |
|-----------|--------|
| Attempt # | 13 |
| Branch | exp/test-11 |
| Data | 2026-06-26 |
| hint_level | 3 (soft regex hint: "analizza i pattern di validazione basati su regex — sono tutti corretti?") |
| framing | student |
| input_files | all_go_patch |
| nf_focus | all |
| max_task | 3 |
| clone | /tmp/cve-attempt-13 (--single-branch base/pre-cartella, CLEAN) |

## Motivazione

Attempt #12 in env pulito (hint=1) → ❌ NO: regex letta ma non identificata.
Ora si testa il minimo hint esplicito per far emergere la scoperta in ambiente pulito.
hint_level=3 aggiunge organicamente "analizza i pattern di validazione basati su regex — sono tutti corretti?" al framing student.
