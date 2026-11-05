# Drawio Reconstruction: Rebuilding a Reference Figure as an Editable Diagram

> Provenance: workflow and Fidelity Contract adapted from
> HKUSTDial/Supervisor-Skills, `skills/drawio-reconstruction/`. The
> skill directory carries its own MIT License (Copyright (c) 2026
> VCG-Bench Authors), distinct from the source repository root's
> CC BY-NC-SA 4.0; the five helper scripts are imported in
> `../scripts/` under that MIT license. This reference restates the
> protocol in CCFA structure.

Use this workflow when a figure exists only as a raster or PDF image
(a paper figure, a slide screenshot) and must be rebuilt as an
editable `.drawio` diagram that still looks like the reference.

## Fidelity Contract

- **Visual fidelity to the reference is the primary goal**;
  editability is secondary. A reconstruction that is easy to edit but
  visibly different has failed.
- A generic icon, a default curve, a default font size, or a plain
  panel background is a **defect** whenever the reference has a
  specific style for that element.
- Script checks prove only technical validity (well-formed XML,
  resolvable references, exportability). **Completion requires a
  visual comparison against the reference at full size** — no batch
  is done on script output alone.
- Work only on the named targets. Never silently "repair" or restyle
  neighbouring diagrams while reconstructing one.
- Distinguish layout-only refinement (spacing, alignment — allowed)
  from content compression (dropping or merging elements — needs the
  owner's permission).

## Workflow

1. **Manifest first.** For a batch, run
   `../scripts/batch_manifest.py --write` to fix the target list and
   the per-image output names before drawing anything:
   `<stem>.drawio`, `<stem>.png` (preview), `<stem>.audit.md`
   (per-target notes).
2. **Reconstruct per target**, using `../scripts/crop_assist.py` to
   inspect reference regions at full resolution instead of guessing
   from a downscaled whole.
3. **Technical gate.** Run `../scripts/check_drawio.py` on each
   `.drawio` (XML structure and style sanity) and export previews
   with `../scripts/export_drawio.py`.
4. **Batch verification.** Run `../scripts/batch_verify.py` to confirm
   every manifest target has its three outputs and passes the
   technical gate.
5. **Visual gate (mandatory).** Compare every preview against its
   reference side by side at full size; log discrepancies in the
   target's `.audit.md` and iterate the diagram — not the reference —
   until the audit is clean. A target with no visual comparison is
   unfinished regardless of script results.
