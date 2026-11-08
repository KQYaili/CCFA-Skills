# Publication Figure: Panel Evidence And Export Preflight

Use **in addition to**, not instead of, [render-qa.md](render-qa.md) and the [visual contract](visual-contract.md) for substantive multi-panel publication figures or a final-size submission export. A single exploratory chart or one-line SVG fix only needs the existing affected-area QA.

## One Scientific Question, Distinct Panel Jobs

State the question the combined figure must answer. For each panel, name its **inferential role** and evidence source: primary comparison, diagnostic mechanism, paired heterogeneity, ablation, robustness, uncertainty, counterexample, or representative case. A panel without a distinct role may be removed or moved to supplementary material; a missing but decision-critical comparison is a scientific issue for the experiment owner, not a decorative layout vacancy.

Plan the reading order so the main result is visible before interpretation and caveats. Share axes, palettes and legends only when the variables, units, splits and encodings are genuinely compatible. A beautiful aligned grid cannot turn unlike protocols into comparable data. Keep legitimate negative findings and missing/zero distinctions visible.

The default **one principal method architecture figure per manuscript** still applies: do not add a second architecture or motivation diagram just to complete a figure category. Publication-ready architecture topology remains gated on method freeze; generated images do not establish a valid scientific graph.

## Cross-Figure Presentation Consistency

For a paper-wide visual pass, use M07/M10/M13 and X01/X02 of the [shared manuscript audit](../../ccf-common/references/manuscript-audit-standard.md). Compare open/closed axis spines, grid presence and weight, typography, color/line/marker identities, legend semantics, and panel-letter placement across **comparable** figures; deliberate exceptions need a reason. Verify color-vision-deficiency and grayscale legibility. Every used error band, n, statistical marker, highlighted value and unit is explained in the relevant caption/figure; percentage and percentage-point scales must not silently switch. Reconcile the actual rendered panel and cited source data rather than declaring a consistent theme from plotting code alone.

## Final-Size Evidence And Geometry Check

Inspect the real generated output at the intended journal template's **physical width**, using the requested single/double-column or custom width rather than an arbitrary pixel preview.

1. **Data fidelity:** Recompute or reconcile the highlighted values, axes, units, sample identities, confidence intervals, annotation rules, legend mappings and declared metric direction from the source. Check the Figure Registry's current `protocol_id` and any presentation amendments after `verified`.
2. **Panel semantics:** Verify that the caption's (a)/(b)/(c) explanation matches the rendered panel, panel order, range/normalization and role. Distinguish a qualitative example from quantitative evidence.
3. **Visual legibility:** Inspect text/math glyphs, panel letters, ticks, error-bar caps, connectors, black-and-white discriminability and line thickness **at target size**. Check data rectangles and shared scales for alignment; do not simply compare outer image boxes.
4. **Export integrity:** Inspect the exported PDF/SVG and, where needed, the compiled manuscript page for text overlap, clipping, missing CJK/math glyphs, font substitution, negative-space or hidden objects. PDF text extraction or geometric collision heuristics are useful **diagnostics**, not proof that all text is visible or no collision exists.
5. **Genuine editability:** For a requested editable SVG/PPTX, inspect native text, plot marks, shapes and connectors. A whole-page bitmap inside an SVG is not an editable reconstruction. Small photographs, microscopy plates or illustrative raster assets may remain separate raster objects if described honestly.

When the project's existing renderer or audit helpers support automatic checks, use them and record their actual coverage. Do not invent pass results or claim that all glyph overlaps, semantic mistakes or hidden pixels were automatically ruled out. When a tool is unavailable, inspect the output manually and identify only decision-relevant residual uncertainty.

## Repair And Delivery

Fix data and encoding at their source, not by hand-editing a flattened preview. Preserve stable `fig:*` labels, caption references, verified comparison sets and manuscript-local registry state. A post-freeze scientific change follows the protocol amendment rule; a post-freeze presentation-grammar change follows its recorded, reviewed amendment path. Cosmetic corrections require affected export checks but no new scientific protocol.

Deliver the canonical editable source plus requested SVG/PDF/PPTX or raster exports, not a new QA workbook. A concise handoff can state: inspected artifact and width, data/protocol version, visual issues fixed, actual tool/manual checks, and remaining blocker. The existing [render QA policy](render-qa.md) owns the general workflow.

## Adaptation note

Synthesizes publication-sized figure checks and panel evidence sequencing from [Nature Skills](https://github.com/Yuan1z0825/nature-skills) and scientific figure review considerations from [Supervisor-Skills](https://github.com/HKUSTDial/Supervisor-Skills). It does not import image-generation connectors, Python/R exclusivity gates, upstream assets, or venue-specific claims of official compliance.
