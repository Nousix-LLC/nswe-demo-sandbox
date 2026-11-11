# Task: Verification depth — evidence adequacy for work-item #12's acceptance criteria (PR #22)

## Task Specification

**Slug**: SUBTASK_verification_depth
**Task Kind**: standard
**Status**: Pending

### Objective

Judge whether the machine gate's recorded build+run evidence actually **demonstrates** each of
work-item #12's **nine acceptance criteria**, and flag anything material left **unverified** — then
emit `verification_findings.md` conforming to the inherited findings schema.

### Context

This is concern 7 of the scope-&-verification spoke (see `../_GLOBAL.md` and `../contracts/`). It is
one of two parallel analysis children; its output is merged by `SUBTASK_findings_synthesis` into the
single `findings.md` the spoke owes. You assess the **adequacy of the evidence**, not re-run the build.

**Dependencies**: none. **Dependents**: `SUBTASK_findings_synthesis`.

### Concern owned

- **Concern 7 — testing / verification depth**: whether the machine gate's build+run evidence (in
  `taskflow/dags/containerize/SYNTHESIS.md`) genuinely demonstrates each work-item #12 acceptance
  criterion, and whether anything material is left unverified (a claimed behavior with no corresponding
  evidence, or a criterion asserted but not exercised). This is an evidence-to-criterion mapping
  judgment, not a rebuild.

### Input Specification

| Input | Source | Purpose |
|---|---|---|
| Subtree hub | `../_GLOBAL.md` | Subtree objective, posture, read-only constraint |
| Grandparent hub | `../../_GLOBAL.md` | PR coordinates, the machine-gate-is-input rule |
| Inherited schema | `../../contracts/findings_schema.md` | The `findings.md` shape + severity rubric to conform to |
| Sub-contract | `../contracts/_MANIFEST.yaml` | Your `SCOPE-V*` finding-ID prefix; identity SV2 |
| Machine gate | `/home/user/nousix-runtime/nswe-demo/taskflow/dags/containerize/SYNTHESIS.md` | The build/run evidence AND the nine acceptance criteria whose demonstration you assess |
| The diff (for cross-check) | `gh pr diff 22 --repo Nousix-LLC/nswe-demo` (read-only) | Confirm a claimed behavior corresponds to something actually in the diff |

### Approach (not a runbook)

Walk each of the nine acceptance criteria in the machine gate and judge whether the recorded evidence
genuinely demonstrates it. Call each criterion exactly one of `evidenced` / `weakly evidenced` /
`unverified`, citing the specific evidence (or its absence). Flag any criterion asserted but not
exercised. Honor the severity discipline: a genuinely unverified criterion is `major`/`block`; "more
tests would be nice" is `minor`/`nit`. Record findings with location + evidence + (block/major)
remediation. You decide depth and any further breakdown.

### Output Specification

| Attribute | Value |
|---|---|
| Filename | `verification_findings.md` |
| Location | this workspace (`SUBTASK_verification_depth/`) |
| Shape | the per-concern disposition block for concern 7 + a findings table in `../../contracts/findings_schema.md` shape, using the `SCOPE-V` prefix |

### Success Criteria

- [ ] Concern 7 carries an explicit disposition (PASS | PASS-WITH-NOTES | FAIL).
- [ ] Each of the nine acceptance criteria is individually called evidenced / weakly evidenced /
      unverified, with the specific machine-gate evidence cited (identity SV2).
- [ ] Every `block`/`major` has location + evidence + remediation; finding IDs use `SCOPE-V<n>`.
- [ ] Read-only honored; no rebuild; no GitHub write.

## Suggested Methodology Files

Domain Mapping row matched (verbatim): **"Writing tests | Testing | Core"** — the verification-adequacy
lens. Load on demand via `engine_load_methodology { name: "<bundle_id>" }`:

- `testing/Testing_Strategy_Methodology.md` — what "adequate verification" means; mapping evidence to
  criteria; risk-based judgement of what MUST be exercised vs. what is advisory.
- `testing/Testing_Integration_Testing_Methodology.md` — judging whether build-and-run evidence
  exercises the real acceptance paths (the `/healthz`, SPA fallback, `/pkg/*.wasm`, `POST /api/users`,
  SIGTERM-exit behaviors) rather than merely asserting them.

The above are suggestions based on the task type. Load these as a starting point but you are the final
judge of what your work requires — load fewer if some are clearly inapplicable, more if your own reading
of the machine gate reveals additional methodology surface.

## Inherited Constraints

- **Read-only** (I5): rely on `taskflow/dags/containerize/SYNTHESIS.md` for build/test FACTS; do NOT
  rebuild; do NOT post to GitHub.
- **Severity discipline** (I4 / SV6): only a genuinely unverified criterion or a false claimed behavior
  is `major`/`block`; a testing hardening wish is `minor`/`nit`.
- Conform to the inherited `findings_schema.md`; do not redefine it. Use the `SCOPE-V` finding-ID prefix.

## Out-of-Scope Methodologies

- Scope-boundary / change-boundary review (concern 8) belongs to the sibling `SUBTASK_scope_conformance`
  — do not file scope-conformance findings here.
- The per-artifact deep analyses (build, security, operability, Rust) are owned by the four sibling
  spokes of the grandparent DAG; here you judge verification *adequacy*, not re-adjudicate their domains.
- `decomposition/` and `synthesis/` bundles are not for this analysis child.
