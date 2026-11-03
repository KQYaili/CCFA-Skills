# Selective Research-Skill Adoption (CCFA)

This note records an **incremental** review of projects mentioned in a community list, inspected 2026-11-03. A GitHub star count, toolkit breadth, or package title is not evidence of correctness. The source list is descriptive, not a dependency manifest or an automatic installation instruction.

| External source (inspected revision prefix) | Reusable idea | Decision / CCFA destination |
| --- | --- | --- |
| [PaperSpine](https://github.com/WUBING2023/PaperSpine) (`42312b8d9c76`, MIT) | Motivation aligned with contribution/evidence at writing-unit granularity | **Adapt**: `ccf-paper-writer/references/argument-spine-audit.md`; no upstream matrix or UI copied |
| [Supervisor Skills](https://github.com/HKUSTDial/Supervisor-Skills) (`a20d76ef3979`, mixed CC BY 4.0 / skill-specific licenses) | Scientific argument checks and figure narrative roles | **Adapt principles only**: writer and visual preflight; no original text/assets copied |
| [Research Paper Writing Skills](https://github.com/Master-cai/Research-Paper-Writing-Skills) (`77e7c2c1ba06`, MIT) | Reviewer-style structural self-check | **Adapt**: selective reverse outlining; retain current CCFA writing owner |
| [ARIS](https://github.com/wanshuiyin/Auto-claude-code-research-in-sleep) (`2927b40b2ea3`, MIT) | Results-to-claim verdicts and retention of negative evidence | **Adapt**: `ccf-common/references/claim-promotion-gate.md`; reject external runtime/reviewer bridge and duplicate research wiki |
| [Claude Scholar](https://github.com/Galaxy-Dawn/claude-scholar) (`d394fb599ed9`, MIT) | Evidence records, claim-strength promotion, source-location handoff | **Adapt**: claim gate using existing CCFA notes, not additional mandatory databases |
| [Nature Skills](https://github.com/Yuan1z0825/nature-skills) (`69817e4dad8b`, Apache-2.0) | Multi-panel evidence roles and final-PDF legibility checks | **Adapt**: `ccf-visual-composer/references/publication-figure-evidence-check.md`; no external images, fonts, plotting scripts, or OpenRouter calls |
| [AI Research SKILLs](https://github.com/Orchestra-Research/AI-Research-SKILLs) (`773a52944ba4`, MIT) | Artifact-level epistemic critique and backend-specific research tools | **Conceptual cross-check** for claim promotion; do not import 98 tool-specific Skills or stale backend instructions |
| [Scientific Agent Skills](https://github.com/K-Dense-AI/scientific-agent-skills) (`a25cf9ec00e2`, MIT) | Specialized scientific database and Python workflows | **Defer**: most are domain/dependency specific; use when a concrete dataset/API task demands one |
| [Academic Research Skills](https://github.com/Imbad0202/academic-research-skills) (`2e02041a3b82`, CC BY-NC 4.0) | Socratic plans and multi-stage integrity gates | **No code/text import** due restrictive license and overlap with CCFA routing/review |

## Integration Rules

- Keep CCFA's 18 runtime Skills and original owner routing unchanged. Add focused references to the existing authoring, evidence, and visual owners; preserve Humanization → Common preflights.
- These new references are **opt-in by task type**, not globally mandatory checklists. A short question, formatting fix or single plot must not trigger an extra report, a reviewer call, experimental execution, or a new file.
- Retain existing `ccfa.yaml`, manuscript Figure Registry and handoff documents as source of truth. The borrowed **ideas** are rewritten into a small compatible procedure; no third-party scripts, original templates, source text, badges, images or model/API credentials were copied.
- The scope of QA is transparent: reading reference procedures is not executing original upstream tools, and deterministic source/path checks do not verify scientific truth.
- Later additions require a specific missing function, an identified source and license review, a nonduplicating owner, and a tested accept/reject condition before integration.
