# Research Figure Lifecycle: Incremental Results, Deferred Method Diagrams

This adaptation provides an evidence-first figure lifecycle for iterative research projects — any project where experiments, manuscript text, and figures evolve at different speeds. Apply it to coordinated experiments, multi-figure manuscripts, and project-level drafting. For a one-off plot or an explicit early diagram request, complete that request without imposing a project registry. Current user instructions and existing project paths take precedence.

## Scheduling Contract

| Lane | Begin | Update trigger | Publication gate |
| --- | --- | --- | --- |
| Quantitative figures | During experiment design; start rendering as soon as real measurements are available | A new protocol-compatible, checked result batch or an explicit request | Validated inputs, units, aggregation, uncertainty, provenance, scientific and visual QA |
| Manuscript and figure placements | During outline/method drafting, before final figures exist | Any changed method definition, experiment protocol, figure result, or section structure | All used figures resolve; descriptions and claims match final evidence; no draft markers |
| Architecture and process diagrams | Preserve a structural specification during research; normally defer publication-quality rendering | Method topology is frozen and source descriptions/code agree | Scientific graph and training/inference distinctions checked against final mechanism and editable source |

Do **not** force a polished architecture or workflow diagram during early design merely because the paper contains a reserved figure slot. A preliminary debugging sketch may be produced when requested, but label it exploratory; do not pass it off as the final paper figure. For authoritative paper method diagrams, prefer a verified node/edge specification and semantically editable SVG/draw.io/PPTX objects over a single uneditable raster; an image-generated concept may be used for visual exploration, not as the source of computational truth. Existing approved visual style or a direct user request can override the rendering-route default.

## Authoritative Figure Identity

For iterative manuscripts, keep one registry per manuscript at its established location, or by default `<manuscript-root>/figures/figure-registry.json`. When one repository contains multiple papers, keep their registries separate even if they reuse labels such as `fig:method-overview`; never merge them into a flat project-wide label namespace. The registry is a small coordination index, **not** an additional copy of measurements, plotting specifications, or `ccfa.yaml`. Maintain stable `fig:*` keys and corresponding LaTeX labels across sections, tables, plots, captions, and appendices. Reuse a registry if one already exists and preserve unrelated entries.

Suggested fields per figure:

- `id`: stable LaTeX key, e.g. `fig:main-results` or `fig:method-overview`.
- `kind`: `quantitative`, `architecture`, `workflow`, or `other`.
- `status`: `reserved`, `exploratory`, `verified`, or `final`.
- `section`: intended manuscript section; `purpose`: the scientific question the figure answers.
- `evidence_paths`: relative paths to actual inputs, code/specifications, or source artifacts; empty while reserved.
- `protocol_id`: nonempty for validated quantitative evidence; include split/seed/aggregation identity in the referenced protocol, not in this index.
- `method_frozen`: true when the method graph/procedure is frozen and inspected, especially for method diagrams.
- `in_manuscript`: whether the figure is expected in the submitted document.

These fields are an index; `verified` is an assertion requiring independent evidence checks, not proof just because the JSON says so. Do not silently promote status on file creation, a successful command, or a visually pleasing preview. Use the bundled `ccf-common/scripts/check_figure_registry.py` for structural/LaTeX checks where the registry is used. See `examples/figure-registry.example.json` for a safe starter; replace its generic entries with the actual paper plan rather than copying them into every project.

## Quantitative Figure Loop (during experiments)

1. Attach each chart to a specific comparison, observation unit, metric direction, sample identities, dataset/split, aggregation order, and reproducible input path. When a result batch arrives, inspect its run success, configuration, evaluation identity, and whether it is comparable before updating the chart. Failed or incompatible runs remain diagnostic evidence, not bars in a reported comparison.
2. Keep a stable authoring script/specification and explicit input bindings. Freeze the scientific comparison definitions — observation unit, metric direction, aggregation rule and uncertainty meaning — when evidence becomes publication-bound; changes to those definitions require a disclosed protocol version and recomputation where applicable. Chart grammar, palette, layout and other presentation choices may still improve as real data arrives, provided axes and transformations remain honest and the affected exports are rechecked. Update only affected panels from genuine recorded measurements, retain raw observations, and keep seeds, error bars, sample counts, and missing values explicit. Do not silently pool unlike protocols or fill missing metrics.
3. Distinguish exploratory from publication-bound outputs. Exploratory figures may be regenerated on every checked batch and are useful for scientific decisions. Promote to `verified` only after the scientific comparison and normalization/aggregation definitions are checked; `final` additionally requires caption, final-size design and PDF/SVG/render QA. Reusing the plotting script is preferred to recreating the figure from scratch.
4. When a figure changes, hand the changed claims and identifiers to the paper writer; update only dependent text and captions, including unfavorable outcomes. Do not infer a win from a visual trend without the specified comparison.

**Audit example — aggregation order is part of the result:** record whether an aggregate error is `mean(abs(fold_error))` or `abs(mean(fold_error))` and preserve the fold-level observations. They are not interchangeable. Likewise, verify that a claimed mechanism survives the pipeline's actual normalization before claiming it changes the optimized signal: a group-constant multiplier, for instance, may be cancelled exactly by group normalization. These are scientific checks, not figure styling choices.

**Audit example — a visualization is not proof of a structural claim:** do not substitute an attractive latent-space or embedding scatter for evidence about geometry, feasibility, or intervention effects. Record the embedding provenance, the objects plotted, the metric, the constraints, the intervention semantics, and the discriminating baseline or counterexample before interpreting the picture.

## Manuscript Placement Before Rendering

The writer owns the prose, while the visual composer owns graphics. As soon as the outline is concrete, assign stable labels and section positions to the planned figures. Introduce **why** the figure will be read, refer to the stable label, and reserve a natural transition to the next scientific question. Explanations of the method and evaluation protocol may be written before results; dependent result interpretation stays blank unless real observations support it. The default `results_pending_draft=off` is unchanged.

For a full LaTeX draft that explicitly needs visible figure placeholders, use a clearly marked, compilable draft block with a stable label, for example:

```latex
% DRAFT FIGURE SLOT: replace before submission; do not interpret missing results.
\begin{figure}[t]
  \centering
  \fbox{\parbox[c][30mm][c]{0.9\linewidth}{\centering DRAFT FIGURE SLOT: method overview}}
  \caption{Draft placement for the method overview; final caption requires source verification.}
  \label{fig:method-overview}
\end{figure}
```

Use `Fig.~\ref{fig:method-overview}` where relevant so the reference survives replacement. If the user wants the entire experimental section empty, do **not** populate it with setup, slots, or prospective prose; retain only the requested section position. If a placeholder figure environment is inappropriate for the current draft, reserve its label and adjacency in the author-owned registry or source comments rather than creating unsupported graphics. Never invent a figure, result, caption assertion, diagram module, or qualitative example to bridge the prose. Do not insert draft placeholders into a submitted file.

## Method Freeze and Final Diagram Gate

For this manuscript workflow, default to **one principal method architecture figure per paper**, with optional (a)/(b)/(c) insets to explain the key mechanism or training/inference paths. A separate flowchart is not required just to complete a template: use prose, equations, pseudocode or an appendix when sufficient. Add another standalone method diagram only when its scientific role is distinct or the user requests it. For a portfolio of three papers, maintain three distinct main diagrams and three manuscript-scoped registries; do not reuse an unverified diagram by relabeling it.

Treat the method as frozen only when the intended computational graph, modules, branches, objectives, supervision, training/inference boundary, and relevant implementation/version are resolved. A git commit alone is not evidence of scientific consistency. Create final architecture/process figures from the approved topology; compare every arrow and label with the actual computation and remove nonexistent modules. If the method changes later, reopen affected diagrams, figure captions, and dependent manuscript passages. Do not force extra retraining solely to finalize artwork.

## Final Integration Check

Before submission, inspect the complete manuscript and figures together:

1. Every referenced `fig:*` label exists, names the same scientific object, and is backed by a final figure; no visible draft placeholders, unresolved source comments, or anticipated result claims remain.
2. Quantitative figures agree with the retained result sources and declared protocol: units, folds, aggregation order, uncertainty, method version, and valid zero/missing distinctions.
3. Architecture/process diagrams agree with the frozen method and its code/equations, including training versus inference; editable outputs are genuinely editable.
4. Figure captions and preceding/following paragraphs accurately explain purpose, evidence, and limitations. Negative or mixed findings are preserved. Check rendered page-size legibility, cross-references, and figure placement.

Run the structural validator against each manuscript registry and its complete TeX source set separately. `--submission` requires at least one `--tex` input for manuscripts containing figures; omitting a TeX file may still hide errors in that omitted file. The structural validator detects schema, labels, and draft markers; it cannot prove scientific correctness. Preserve the independent integrity/review checks already required elsewhere in CCFA.
