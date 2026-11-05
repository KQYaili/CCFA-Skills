# Structured Draft Schema (Condensed)

> Provenance: condensed from Yuan1z0825/nature-skills,
> `skills/nature-paper-to-patent/references/draft-schema.md`
> (Apache License 2.0), aligned to the exact checks implemented by
> `../scripts/validate_patent_draft.py` — when this summary and the
> validator disagree, the validator wins.

The draft package is one JSON object. The validator requires these
top-level keys; a missing key is an ERROR (`MISSING_KEY`):

| Key | Content |
| --- | --- |
| `title` | Application title |
| `metadata` | Bookkeeping (jurisdiction, source document, draft status) |
| `source_analysis` | Source profile, including `formula_count_in_source` and `contains_core_formulas` |
| `source_map` | Source blocks: `id` (`P/E/F/C` + ≥3 digits), `locator` |
| `terminology_ledger` | One row per object: `canonical_zh` (non-empty, unique), `forbidden_aliases` |
| `formula_inventory` | Per source equation: `source_id`, `disposition` (kept / simplified / dropped, with reason) |
| `figure_inventory` | Per source figure: `source_id`, `disposition` |
| `evidence_ledger` | Per claim feature: `id`, `support_status` ∈ {explicit, inherent, needs-confirmation, unsupported}, `source_ids` (required for explicit/inherent) |
| `claims` | Ordered claims: `number` (continuous from 1), `text` (no `[TO CONFIRM]` markers) |
| `claim_feature_map` | Per claim: `claim_number`, `feature`, `evidence_ids` — every claim must be mapped, every mapped feature must cite ledger IDs |
| `figures` | Draft figures: `number` (continuous), `nodes` (unique IDs, `label`), `edges` (`from`/`to`), `source_ids`; the terminal node of a flow figure must name a concrete output, not 技术结果/处理结果/最终结果 |
| `abstract_figure_number` | Must point at an existing figure number |
| `specification` | `technical_field`, `background`, `invention_content` {`problem`, `solution`, `beneficial_effects`}, `figure_descriptions`, `embodiments`, and `equations` (array) |
| `abstract` | Specification abstract (validator warns beyond ~300 characters) |
| `quality_assessment` | `status` (`review-draft` or `incomplete-draft`) and `scores` |

Specification `equations` entries carry `number` (continuous),
`latex` (convertible LaTeX source), `source_ids`, `symbols`
(structured definitions), and `technical_role`.

## Quality thresholds

Scores are integers 1–5, each with an `evidence` note. Delivery
thresholds enforced by the validator: `evidence_support` ≥ 4,
`claim_architecture` ≥ 4, `terminology_consistency` ≥ 4,
`enablement_detail` ≥ 3, `technical_effect_reasoning` ≥ 3; when the
source contains core formulas, `formula_coverage` ≥ 4; when figures
exist, `figure_alignment` ≥ 4. Below any threshold the validator
raises an ERROR and the package must be delivered labelled an
incomplete draft.
