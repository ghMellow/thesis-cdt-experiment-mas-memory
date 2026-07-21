# 10 — Dati per il paper: configurazione senza SonarQube (2026-07-20)

> Numeri pronti da incollare in Overleaf per la parte **"Agentic LLMs" (senza SAST)** del paper (sezioni V.C, VI). Fonte: unico run disponibile `20260714T152535Z` (`results/evaluation/comparison.md` + `result_task*_1A.md`). Copre §IV.B **Precision/Recall/F1 (M2)**, **Alerts-per-TP (M3)**, **Computational cost (M5)**, **Exact vector match (S1)**, **Per-metric accuracy (S2)**. Non copre RQ1 (serve M4/SonarQube, vedi doc 08 §3 — rimandato).

## ⚠️ Da chiudere prima di scrivere i numeri in bella

Il run disponibile produce **84 finding non matchati (FP)** in totale, non i "~10 potenziali" che Lorenzo aveva dichiarato venerdì con la versione precedente del sistema. Di questi 84, **21 sono su task9** (0 CVE target mappate in quel task — ogni finding è per costruzione unmatched, non è rumore comparabile agli altri task). Restano **63 FP sui task5–8**. Prima di scrivere "il sistema trova tutte le CVE note + ne dà N potenziali" nel paper, va riconciliato questo numero con quanto dichiarato da Lorenzo (task aperto, non bloccante per compilare le tabelle sotto).

---

## Tabella 1 — Detection & workload per network function (M2, M3)

Riga per NF (`final answer`, cioè la risposta dopo i retry — quella da riportare). task9 escluso dal pooled per assenza di CVE target mappate (nota a piè tabella).

```latex
\begin{table}[t]
\centering
\caption{Detection performance and analyst workload of the unguided agentic LLM (no SAST guidance), pooled over 3 repetitions per network function.}
\label{tab:detection-no-sast}
\begin{tabular}{lrrrrrrr}
\toprule
NF & TP & FP & FN & Prec. & Rec. & F1 & Alerts/TP \\
\midrule
PCF & 3  & 0  & 0  & 100.0\% & 100.0\% & 100.0\% & 1.0 \\
UDR & 6  & 13 & 12 & 31.6\%  & 33.3\%  & 32.4\%  & 3.2 \\
AMF & 3  & 16 & 0  & 15.8\%  & 100.0\% & 27.3\%  & 6.3 \\
UDM & 3  & 34 & 0  & 8.1\%   & 100.0\% & 15.0\%  & 12.3 \\
\midrule
Pooled$^{*}$ & 15 & 63 & 12 & 19.2\% & 55.6\% & 28.6\% & 5.2 \\
\bottomrule
\end{tabular}
\\[2pt]
\footnotesize{$^{*}$Excludes the cross-NF task (0 mapped target CVEs; all 21 of its findings are unmatched by construction, not comparable noise). Including it: TP 15, FP 84, precision 15.2\%, alerts/TP 6.6 (see \texttt{comparison.md}).}
\end{table}
```

Note per il testo:
- **PCF è il caso ideale**: coverage e precision al 100%, alerts/TP = 1.0.
- **UDR è il buco di completezza**: detection rate 100% ma coverage 33% — trova sempre qualcosa, mai tutto (4 CVE su 6 mai trovate in nessuna delle 3 ripetizioni, vedi CVE×repetition matrix in `comparison.md`).
- **AMF/UDM sono il caso "trova ma annega nel rumore"**: recall 100%, precision bassa. Su UDM, 15 dei 34 unmatched condividono l'handler della CVE-2026-42459 già matchata (probabili duplicati, non 34 candidate distinte — colonna `group` nel report per-task).

## Tabella 2 — Severity: exact match e baseline (S1, S3)

```latex
\begin{table}[t]
\centering
\caption{Exact CVSS v4.0 vector match on true positives (S1), against a null-model baseline that always predicts the modal target vector (S3).}
\label{tab:s1-s3}
\begin{tabular}{lrrr}
\toprule
NF & n (TP) & S1 exact match & S3 baseline \\
\midrule
PCF & 3  & 0.0\% & 100.0\%$^{*}$ \\
UDR & 6  & 0.0\% & 0.0\% \\
AMF & 3  & 0.0\% & 100.0\%$^{*}$ \\
UDM & 3  & 0.0\% & 100.0\%$^{*}$ \\
\midrule
Pooled & 15 & 0.0\% & 0.0\% \\
\bottomrule
\end{tabular}
\\[2pt]
\footnotesize{$^{*}$Degenerate: single target CVE in scope, so the modal vector is that CVE's own vector by construction — only UDR (6 heterogeneous CVEs) and the pooled row are informative.}
\end{table}
```

## Tabella 3 — Severity: accuratezza per metrica CVSS e distanza ordinale (S2, pooled)

```latex
\begin{table}[t]
\centering
\caption{Per-metric accuracy and average ordinal distance on the CVSS v4.0 base metrics, pooled over all matched findings ($n=15$), against the S3 baseline.}
\label{tab:s2}
\begin{tabular}{lrrr}
\toprule
Metric & Agent acc. & Baseline acc. & Avg. ordinal dist. \\
\midrule
AV & 100.0\% & 100.0\% & 0.00 \\
AC & 100.0\% & 100.0\% & 0.00 \\
AT & 100.0\% & 100.0\% & 0.00 \\
PR & 20.0\%  & 100.0\% & 0.53 \\
UI & 86.7\%  & 100.0\% & 0.07 \\
VC & 66.7\%  & 80.0\%  & 0.20 \\
VI & 46.7\%  & 40.0\%  & 0.27 \\
VA & 60.0\%  & 80.0\%  & 0.33 \\
SC & 73.3\%  & 100.0\% & 0.13 \\
SI & 60.0\%  & 80.0\%  & 0.27 \\
SA & 93.3\%  & 100.0\% & 0.03 \\
\bottomrule
\end{tabular}
\end{table}
```

Nota per il testo: AV/AC/AT perfetti; l'errore si concentra su **PR** (20% vs baseline 100%) — l'agente sovrastima sistematicamente il bisogno di privilegi rispetto a quanto dicono le CVE. Le distanze ordinali restano basse (≤0.33) altrove: sbaglia il valore ma non "esplode" sulla scala di severità.

## Tabella 4 — Costo computazionale (M5, pooled — tutti i task)

```latex
\begin{table}[t]
\centering
\caption{Wall-clock cost per repetition (including every SGV/rubric retry), pooled across all task types ($n=15$).}
\label{tab:cost}
\begin{tabular}{lr}
\toprule
Metric & Value \\
\midrule
Avg. elapsed time (s) & 56.2 \\
Avg. agent tokens (in/out) & n/a$^{*}$ \\
Avg. judge tokens (in/out) & n/a$^{*}$ \\
\bottomrule
\end{tabular}
\\[2pt]
\footnotesize{$^{*}$Token counts unavailable on this hosted backend (Ollama Cloud does not always report \texttt{prompt\_eval\_count}/\texttt{eval\_count}); available on local-model runs.}
\end{table}
```

## Numeri grezzi (per la narrativa dei Risultati, non tabella)

- 9 CVE target totali (5 su task5/7/8, 1 ciascuna; 6 su task6) × 3 ripetizioni = 27 (CVE × rep) attese sui 4 task con GT.
- **TP = 15** → 5 CVE distinte su 9 trovate almeno una volta, e sempre in tutte e 3 le ripetizioni quando trovate (nessuna instabilità di campionamento — vedi CVE×repetition matrix).
- **FN = 12** → le 4 CVE di UDR mai trovate, ×3 ripetizioni. Miss sistematico, non rumore.
- **FP = 84** totali (63 sui 4 task con GT + 21 su task9 senza GT mappata) → tutti da validazione manuale (§2 doc 08: la precision riportata è un *floor*, non un valore assoluto).

## Da NON mettere in questa versione del paper

- RQ1 (SAST-alone) — serve M4, non implementata: task successivo.
- M1 (detection rate/coverage) come tabella a sé — già assorbita nella narrativa sopra, non richiesta da §IV.B.
- Detection delta by retry channel / SGV conformity / consistency — diagnostiche interne, non nel piano tabelle del paper.
