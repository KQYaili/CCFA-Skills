# Publication Quantitative Figure Decision & Preflight

Use when converting genuine experiment tables into main-paper plots or choosing among competing visual encodings. This is a **selective companion** to [figure-design-library.md](figure-design-library.md), [publication-figure-evidence-check.md](publication-figure-evidence-check.md), and [figure-post-render-qa.md](figure-post-render-qa.md). Do not replace the existing 43-grammar chart library, figure corpus, geometry QA scripts, or native editable vector tools.

## From scientific claim to visual encoding

1. Fix the **question/estimand**: what is compared, at what analysis unit, under which task split and budget?
2. Determine whether the needed information is **level, contrast, paired change, heterogeneity, calibration, ranking uncertainty, or mechanism diagnostic**.
3. Select the simplest encoding that reveals it honestly; retain the source table and the transformation that produced the plotted values.
4. Reserve one main result visually; use secondary panels only if they rule out a plausible competing explanation or identify a consequential boundary.
5. Record the panel roles, one-sentence reader inference, exact metric definition and source anchor in the existing figure registry or caption notes; never invent missing cells to complete a layout.

| Claim type | Favor | Avoid |
| --- | --- | --- |
| Small method difference | Dot/interval or paired-delta with scale, 95% CI and sample unit | Truncated axis masquerading as a large absolute gain, unsupported significance star |
| Changes on identical tasks | Paired difference / dumbbell + distribution or failure transitions | Unpaired bars hiding task-level reversals |
| Rank of uncertain methods | Effect estimates and intervals + underlying values | Rank-only story under overlapping uncertainty |
| Calibration / selective prediction | Calibration diagram with bin counts; risk–coverage with operating points | Only AUROC or only selective accuracy when actual coverage matters |
| Multi-condition tradeoff | Faceted common-unit panels, labeled budgets and denominators | Plotting different budgets on one axis without distinction |
| Mechanism or decomposition | Mathematically defined terms and a separate diagnostic / identity check | Treating schematic scores as measured results |

For nonlinear aggregation, confirm whether the operation occurs before or after pooling. For AUROC-like statistics, preserve pairwise tie convention and evaluation unit. Keep exploratory demonstrations visually distinct from actual experiment figures and never map toy numbers into empirical panels.

## Data, typography, export

- **Data identity:** input paths and task IDs, exact metric key, seed/fold/task pairing, weights, missing values, exclusion rules, units and budget. Render only from inspected actual records.
- **Uncertainty:** explain whether error bars show SD, SE, CI, bootstrap interval, or posterior interval; record \`n\` and the independent sampling unit. Do not call across-correlated-task samples independent.
- **Readable vector files:** prefer PDF/SVG for line art and quantitative charts, preserve editable text (\`svg.fonttype = 'none'\` where supported); if importing to Figma changes glyph widths, regenerate with verified font substitutes or keep formulas as stable vector outlines. Retain an editable source script regardless.
- **Consistency:** stable method colors across related panels, accessible contrast, redundant line patterns/markers, minimal spines/grids, concise legend, no accidental color semantics.
- **Final physical size:** inspect at the actual ACL/IJCAI/venue column width; judge effective text sizes and formula indices, not the zoomed source screenshot. Do not blindly copy a project's pixel-specific rcParams or large default fonts.
- **Quantitative plotting vs architecture:** Matplotlib is favored for numerical panels; editable SVG, Draw.io, Figma or other explicit tool for topology diagrams. Generated illustration is a conceptual draft, not evidence of scientific correctness or native editability.

## Existing mechanical QA gate

For final publication exports, *reuse* the existing \`audit_figure_collisions.py\`, \`audit_panel_alignment.py\`, and \`audit_pdf_text.py\` following [figure-post-render-qa.md](figure-post-render-qa.md). Inspect the same exported file manually after those checks; a clean geometric scan cannot certify that the plot tells the correct scientific story.

For a figure request with no data, output a panel specification with \`TBD\` for outcome-dependent elements. For a single localized typography edit, run the affected-area visual QA instead of the full figure registry procedure.

## Upstream study and license boundaries

The typography, print encoding, Matplotlib script-exemplar approach is informed by [figures4papers](https://github.com/ChenLiu-1996/figures4papers) (**CC BY-NC 4.0**) and the source/export QA style by [nature-skills](https://github.com/Yuan1z0825/nature-skills) (**Apache-2.0**) and [K-Dense scientific-visualization](https://github.com/K-Dense-AI/scientific-agent-skills) (**MIT**). This guide is independently written; **do not vendor figures4papers' source code or artistic assets into this MIT repository** or copy its samples/numerical values. Existing CCFA QA scripts are authoritative for actual commands.
