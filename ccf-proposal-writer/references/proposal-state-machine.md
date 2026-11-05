# Proposal State Machine: Foundation Files, Section Contracts, Modes

> Provenance: protocol adapted from Yuan1z0825/nature-skills,
> `skills/nature-proposal-writer/` (repository Apache License 2.0; the
> source skill's frontmatter additionally declares MIT). The state
> machine, foundation files, and section-contract discipline are
> carried over and reworded into CCFA conventions; the source's
> external expert-pool machinery and DOCX export script are not
> imported — expert roles are CCFA review roles, and export stays with
> the host's document tooling.

## Foundation files (evidence before prose)

Drafting starts only after these exist in the task directory:

| File | Content |
| --- | --- |
| `00_scope.md` | The writing task boundary: deliverable, funder/programme, deadline, page budget, what is explicitly out of scope |
| `01_research_canon.md` | Hard facts and constraints: verified preliminary results, team capabilities, facilities, prior funding, fixed assumptions |
| `02_evidence_table.md` | Claim → evidence map: every claim the proposal wants to make, the evidence that supports it, and its strength |
| `03_argument_map.md` | Argument architecture: problem, gap, approach, why this team, why now — before any section text |
| `04_section_contracts.md` | One contract per section (below) |
| `05_style_guide.md` | Terminology, funder-specific phrasing, banned expressions |
| `state.json` | Machine state: mode, round, per-dimension scores, open technical debts |

A fact that is not in the canon does not enter the draft. A claim that
is not in the evidence table does not enter the draft. When either is
missing, the correct move is to record the gap in `state.json` as a
technical debt and ask or search — never to write plausible filler.

## Section contracts

Each section contract states:

- **Purpose** — what this section must achieve for the reviewer.
- **Allowed claims** — claims this section may assert, each traceable
  to the evidence table.
- **Forbidden claims** — claims this section must not assert (usually
  because the evidence is thinner than the wording would suggest).
- **Inputs** — canon entries, evidence rows, figures, or prior
  sections this section may draw on.
- **Validation** — the check that proves the section kept its contract
  (every claim cited? methods reproducible? numbering continuous?).

## Modes

- **compose** (topic or rough idea → proposal): build scope and canon,
  build the evidence table, build the argument map, write section
  contracts, then draft section by section, running the QA gates per
  section before assembling the whole.
- **revise** (existing text): diagnose against the existing contracts
  (rebuild minimal contracts when absent), classify findings by
  severity, revise only what the findings require, re-run the affected
  gates.
- **hybrid** (existing draft + extension): revise-mode diagnosis first,
  then compose-mode foundation work for the new parts only; the phase
  boundary between existing and new scope is locked in `00_scope.md`
  before writing.

## Scope before completeness

For phased work (one chapter now, the rest later), lock the phase
boundary in `00_scope.md` and draft only inside it. Material that
belongs to a later phase is recorded as a debt, not drafted early;
scope creep mid-draft is how proposals end up promising a programme
while evidencing a project.
