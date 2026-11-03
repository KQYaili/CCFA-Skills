# Figure Post-Render QA: The Mechanical Export Gate

Use at export time for publication figures, **after** rendering and in
addition to [publication-figure-evidence-check.md](publication-figure-evidence-check.md).
Division of labour: that file owns panel evidence roles and final-size
legibility judgment; this file owns the *mechanical geometry* layer it
deliberately leaves to tooling — collisions, alignment, effective text
sizes — as a hard gate. A figure does not ship with an unresolved FAIL from
this gate.

## Gate 1 — Rendered Collision Audit (blocking)

```bash
python3 scripts/audit_figure_collisions.py <figure.pdf> \
  --json-out <figure.collision-audit.json> [--strict]
```

Reads the final PDF's geometry (PyMuPDF; backend-neutral — Python and R
figures are checked identically). Reliable collisions — text–text overlap,
text crossed by a stroked path, text clipped by the page — are FAIL and
block delivery. Partial overlap of text with a filled shape or raster
image is WARN (in-bar labels, heatmap values, scale bars can be
intentional): every WARN is reviewed at final size and either fixed or
justified in the QA notes. `--strict` promotes WARNs to blocking. The
audit is a deterministic geometry check, not proof that all text is
visible or correctly placed; it complements, never replaces, the final-size
visual inspection.

## Gate 2 — Panel Alignment (1.5 pt, exemptions recorded)

```bash
python3 scripts/audit_panel_alignment.py <figure.alignment-layout.json> \
  --json-out <figure.alignment.json>
```

The plotting script exports a layout manifest of plot-area rectangles
(Matplotlib figures may instead call the script's
`require_matplotlib_panel_alignment(...)` in-process after the final draw).
Comparable row/column edges, panel dimensions, and repeated gutters must
agree within **1.5 pt** at final physical size. Asymmetric hero panels,
insets, and colorbars are excluded or **exempted with a recorded reason** —
never handled by silently widening the tolerance or exempting an entire
row. Every multi-panel figure ships with a fresh alignment JSON.

## Gate 3 — Effective Text-Size Floor

```bash
python3 scripts/audit_pdf_text.py <figure.pdf>
```

Dependency-free scan of the PDF content streams for the *effective* size
of every glyph run (Tf size scaled by text and current transformation
matrices). This catches reduced mathtext super/subscripts and shrunken
annotations that fall below the journal font-size floor even when the
source `fontsize` looks compliant.

## Export Contract (checked with the gates)

- **Raster floor:** raster exports below 300 dpi FAIL; 600 dpi is the
  default target unless the venue specifies otherwise.
- **Display-item budget:** count main-text figures + tables against the
  target venue's declared display-item limit and record the count in the
  QA notes; over-budget is resolved by moving panels to supplementary
  material, not by shrinking type.
- **Source-data bundle:** the export bundle is script + source data + SVG
  + PDF + raster preview + QA notes, delivered together. A panel that
  cannot be traced to its source data fails this contract — consistent
  with the Figure Registry's provenance rules; previews are never
  mislabelled as accepted upload formats.

Record the gate outputs (collision JSON, alignment JSON, text-audit
result, and any WARN justifications or exemptions) in the QA notes that
accompany the figure. Fix failures at the plotting source, never by
hand-editing the rendered output.

> Provenance: scripts adapted from Yuan1z0825/nature-skills (Apache
> License 2.0), `skills/nature-figure/scripts/{audit_figure_collisions.py,
> audit_panel_alignment.py, audit_pdf_text.py}` and the QA contract in
> `skills/nature-figure/references/qa-contract.md`, batch-2 integration
> 2026-11-03. Gate logic unchanged (collision script needs
> `PyMuPDF>=1.24,<2` for PDF input; its geometry core self-tests without
> it). Not imported: the upstream source-level preflight
> (`validate_figure.py` — tied to that skill's Python/R backend workflow;
> its 300/600 dpi rule is carried into the export contract above), the R
> alignment bridge, and all venue-specific Nature Portfolio requirements.
