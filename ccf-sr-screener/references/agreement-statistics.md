# Agreement Statistics: Observed Agreement, Cohen's Kappa, PABAK

> Original CCFA reference, written for ccf-sr-screener. Definitions
> follow the standard sources (Cohen 1960; Byrt, Bishop & Carlin 1993
> for PABAK) and are stated here in summary form.

## The three numbers

For two screeners over `n` records both actually rated, with the 2×2
table

|  | B include | B exclude |
| --- | --- | --- |
| **A include** | a | b |
| **A exclude** | c | d |

- **Observed agreement** `Po = (a + d) / n` — the raw share of records
  where the screeners agree.
- **Cohen's kappa** `κ = (Po − Pe) / (1 − Pe)`, where `Pe` is the
  agreement expected from the two screeners' marginal include/exclude
  rates. Kappa corrects for chance agreement.
- **PABAK** (prevalence- and bias-adjusted kappa) `= 2·Po − 1` —
  kappa recomputed as if both decisions were equally prevalent and
  neither screener were biased toward one decision.

`scripts/screening_agreement.py` computes all three from two decision
CSVs (`record_id,decision` with decisions `include` / `exclude` /
`pending`) and lists every disagreement for adjudication.

## Why kappa alone misleads in screening

Screening corpora are dominated by exclusions — 90–98% exclusion at
title/abstract is normal. At such prevalence, `Pe` is large, so kappa
collapses toward zero even when the screeners agree on almost every
record (the kappa prevalence paradox): a stage can show 97% observed
agreement and a kappa that reads as "fair". Reporting kappa alone
therefore punishes exactly the stages that are working. PABAK removes
the prevalence and bias terms so the number tracks the screeners'
actual consistency; observed agreement anchors both. **Report all
three, always, with the 2×2 counts** — any single one of them, quoted
alone, can be made to say whatever the reader wants.

## Reading rules

- High observed agreement + low kappa + high PABAK: prevalence effect;
  the screeners are consistent, the corpus is skewed. Proceed, and
  say so in the methods text.
- Low observed agreement: the criteria wording is ambiguous regardless
  of what kappa says. Repair the protocol and re-pilot; do not "fix"
  agreement by instructing screeners to converge.
- A large `b` vs `c` asymmetry (one screener systematically more
  inclusive): a bias signal — check whether the two roles are applying
  different implicit thresholds, and record the finding in the
  adjudication log.
- Records rated by only one screener, or left `pending`, are excluded
  from the statistics and reported as their own counts. They are
  never folded into the table as implicit agreements or exclusions.
