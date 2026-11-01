# Evidence Gates for Iterative ML Research

Use this **selectively** when an ML study's mechanism, evaluation, statistical claim, compute comparison, or experiment handoff depends on the issue described below. This is a shared reference, not an always-on checklist or a new stage that delays one-off writing, figure edits, idea reviews, or unrelated experiments. Current user instructions, the actual research protocol, source evidence, and host permissions take precedence. Do not start GPU jobs or create new records merely to satisfy this guide.

## 1. Algebraic and Gradient Pre-Audit

For a newly proposed training signal, reconstruct its actual path from per-sample reward through grouping, centering/normalization, clipping, weighting, reduction, optimizer membership, and parameter update. Identify which quantities are constant within the normalization group and which vary among completions. Before a costly authorized training run, use a small controlled probe to distinguish an inactive mechanism from an ineffective but implemented mechanism.

For example, if a positive prompt-constant weight \(a_q\) multiplies each completion reward \(c_{qg}\) **before** within-group normalization, the resulting advantage can be

\[
\widehat A_{qg}=\frac{a_q(c_{qg}-\bar c_q)}{a_q s_q+\varepsilon}
=\frac{c_{qg}-\bar c_q}{s_q+\varepsilon/a_q}.
\]

For \(\varepsilon=0\) and \(s_q>0\), the factor cancels exactly; for a fixed nonzero \(\varepsilon\), this is **not an exact invariance**, and zero-variance groups, clipping, sign, implementation details, and numerical precision must be inspected. Do not conclude that a mechanism reached the gradient merely because its reward changed. If a different location for weighting is proposed, verify its real computation/gradient path and scientific meaning; do not silently change the method. An FP32 analytic or finite-difference gradient check and BF16 comparison may be useful, with tolerance justified by scale and operation rather than a universal hard-coded threshold.

For selection, voting, retrieval, or routing mechanisms, align the proposed training target and manipulation check with the actual deployment readout and distinguish generation from selection using a shared candidate archive when it answers the causal question.

## 2. Experiment Identity, Metrics, and Inference

When a study uses preregistration or a held-out confirmatory comparison, preserve the frozen primary outcomes, analysis unit, exclusion rules, selection policy, contrast family, dataset/split, and seed identity. Keep development/calibration, model selection, and final held-out evaluation separated at the level the study requires; amendments are explicit and do not rewrite past tests into untouched evidence. Exploratory and diagnostic work remains permitted and clearly named; do not impose a mandatory M0-M5 ladder on unrelated tasks.

Check whether a reported metric applies a nonlinear operation **before or after** pooling. In particular,
\(\operatorname{mean}_k |e_k|\) and \(|\operatorname{mean}_k e_k|\) measure different things. Preserve signed fold-level observations, evaluate the declared endpoint at its correct unit, and label legitimate alternative aggregates separately. An exact zero, missing result, aborted run, conditional denominator, and not-applicable cell must remain distinguishable. For selective systems, separately identify **coverage**, **accuracy conditional on selection**, **unconditional net utility**, and **measured end-to-end latency/FLOPs** when those are relevant.

Use paired analyses only when observations are actually matched (by task, run, or seed, not merely equal array length). Report effect sizes and uncertainty appropriate to the design; paired task bootstrap can be suitable for task-level comparisons, while hierarchical dependence may require resampling at another unit. For a predefined family of significance tests, apply a justified multiple-comparison procedure such as Holm-Bonferroni and state its family. Do **not** require p-values, 8-12 seeds, Holm correction, or a specific confidence interval for every descriptive chart, theoretical paper, or small diagnostic. No invented significance or fabricated intervals.

## 3. Strong, Fair Discriminating Controls

Match the baseline to the causal claim and resources. When claiming benefits from multiple models/agents, inspect a fair single-model repeated-sampling comparison at comparable call/token/compute budgets; when claiming diversity benefits, consider a strongest-member homogeneous team. When claiming peer-content influence rather than re-prompting, consider a shared generation archive and unrelated-peer/placebo or solo-revision control. A genuine negative finding is evidence, not an invitation to remove a strong baseline. These controls are conditional on the question and resources, not mandatory additions to every experiment.

## 4. Decision-Oriented Literature Triage

For research literature lists, optionally label sources: **精读** (read specific decisive sections now), **补充** (essential direct precedent or missing comparator), **备选** (useful later context), or **剔除** (not relevant). State which next experiment, mechanism assumption, or manuscript claim a paper might change. Give a source/version and inspected passage for consequential claims; title-only screening remains visibly unverified. Merge duplicate preprint and venue versions where they are the same work, while preserving real version differences. Do not force the four labels on a user-requested citation format or one-paper factual lookup.

## 5. Writing, Review, and Negative Findings

When scientifically suitable, lead a paper with the concrete decision/question and a supported claim rather than process narration. A null or negative baseline can be a rigorous diagnostic result; describe what was tested, which alternative explanation remains, and what (if anything) a proposed repair changes. Do not force every paper into a "diagnostic audit + repair" story, pretend that the repair worked, or require a statistically unsupported positive takeaway. Check that the abstract, tables, plots, captions, and conclusions share the same protocol and outcome identity. Keep the project's existing figure lifecycle: quantitative figures may evolve with checked results, manuscript slots are reserved early, and final architecture figures wait for method freeze.

## 6. Run Completion, Archives, and Handoffs

Treat the actual worker/job state, exit status, saved measurements, and provider session state as separate observations. A checkpoint filename, file mtime, terminal disconnect, quota balance, or token expiry alone does not prove successful training or released compute. Preserve the existing authoritative handoff record where present; do not impose a new docs/HANDOFF.md file or cloud backend on every project.

Keep credentials and OAuth/rclone/SSH configuration out of repositories. When large checkpoint artifacts are stored externally, retain verified pointers and checksums through the project's existing archive process; a declared pointer without a successful upload/readback is not proof of persistence. Confirm session/cost release using available provider evidence when a cloud run is being closed, and report an unavailable check as unverified rather than claiming zero billing.

## Ownership and Completion

- Idea optimizer: mathematical mechanism and discriminating prediction; no required GPU experiment for concept-only work.
- Research engineer: inspected executable path, numerical/gradient diagnostic, and real run evidence.
- Experiment designer: comparison contract, metric/aggregation meanings, paired units, and interpretation of observed results.
- Integrity auditor/paper reviewer: only relevant claim, normalization, denominator, inferential, or evidence conflicts.
- Literature searcher and paper writer: decision-relevant sources and evidence-matched language.
- Orchestrator: milestone, frozen protocol where actually applicable, receipts, budget, and safe recovery.

Apply the **smallest check that can change the decision**. An actual adverse result completes an honest test; a missing result or failed run remains distinct. This reference augments, but does not replace, the existing family preflights, artifact contracts, or Figure Registry checks.
