# Task: Synthesis gate — merge concern-7 and concern-8 findings into the spoke's findings.md

## Task Specification

**Slug**: SUBTASK_findings_synthesis
**Task Kind**: synthesis
**Status**: Pending

### Objective

Act as the **verification gate** for the scope-&-verification spoke: evaluate the sub-contract
identities (SV1–SV6) over the two partial findings, then **merge** them into the ONE
`findings_schema.md`-conformant `findings.md` this spoke owes its parent DAG — and write the fold
record that resumes the suspended parent spoke. This is a gate, **not** a prose summary: it asserts
coverage/partition/schema and either passes or schedules remediation.

### Context

This is the synthesis/integration task of the scope-&-verification sub-decomposition (see
`../_GLOBAL.md` and `../contracts/`). It runs after both analysis children complete and reads their
real outputs.

**Dependencies**: `SUBTASK_verification_depth`, `SUBTASK_scope_conformance`.
**Dependents**: resumes the parent spoke `SUBTASK_scope_verification` via the fold.

### What this gate does (approach, not a runbook)

Run the four-check model over the two partial findings and the sub-contract:

1. **Coverage / partition**: assert SV1 (concern 7 and concern 8 each have exactly one disposition),
   SV2 (all nine acceptance criteria called), SV3 (complete touched-file set judged, handoff-vs-breach
   explicit), SV4 (every finding ID matches `SCOPE-V<n>`/`SCOPE-S<n>`, no collision).
2. **Schema conformance**: assert SV5 — the merged document matches `../../contracts/findings_schema.md`
   exactly (header, per-concern disposition blocks for concerns 7 and 8, the
   Finding ID | Concern | Severity | Location | Evidence | Remediation table); every `block`/`major`
   carries location + evidence + remediation.
3. **Severity discipline**: assert SV6 / inherited I4 — downgrade any `block`/`major` that is merely a
   hardening wish; a failing identity is REPORTED, never silently plugged.
4. **Merge**: compose the two partial findings into the single `findings.md`, preserving each child's
   finding IDs and dispositions, with a combined header per the schema (both concerns owned,
   diff reviewed = PR #22 head `bc0c3c0d6380c9edd1b9433addc7fdcbffb55751`).

If an identity FAILS and cannot be satisfied from the partial findings (e.g. a criterion was never
called, or a finding-ID collision), schedule remediation as a decomposed fix-task via
`engine_amend_plan { add_task }` (Inject) rather than silently plugging — then re-verify. You decide
depth and whether remediation is warranted.

### Input Specification

| Input | Source | Purpose |
|---|---|---|
| Subtree hub | `../_GLOBAL.md` | Subtree objective, identities, output location |
| Sub-contract | `../contracts/_MANIFEST.yaml` | Identities SV1–SV6; the `SCOPE-V`/`SCOPE-S` partition |
| Inherited schema | `../../contracts/findings_schema.md` | The exact `findings.md` shape to emit |
| Verification findings | `../SUBTASK_verification_depth/verification_findings.md` | Concern 7 partial findings |
| Scope findings | `../SUBTASK_scope_conformance/scope_findings.md` | Concern 8 partial findings |

### Output Specification

| Attribute | Value |
|---|---|
| Merged deliverable | `findings.md` at the **parent spoke workspace** (`/home/user/nousix-runtime/nswe-demo/taskflow/dags/review-containerize/SUBTASK_scope_verification/findings.md`) — the ONE findings document, in `findings_schema.md` shape |
| Fold record | `SYNTHESIS.md` at the same fold location (`.../SUBTASK_scope_verification/SYNTHESIS.md`) — the synthesis terminal record consumed by `engine_resume_suspended` to fold the parent `SUSPENDED → COMPLETED` |

Terminate with `engine_report_status { status: "completed", outputs: [".../SUBTASK_scope_verification/findings.md"], artifact_path: ".../SUBTASK_scope_verification/SYNTHESIS.md" }`, then call
`engine_resume_suspended { target_task_id: <parent spoke>, synthesized_task_id: <this task>, seam_path: ".../SUBTASK_scope_verification/SYNTHESIS.md" }`.

### Success Criteria

- [ ] SV1–SV6 each evaluated with an explicit PASS/FAIL (a failing identity reported, never plugged).
- [ ] The merged `findings.md` conforms exactly to `../../contracts/findings_schema.md`, covering
      concerns 7 and 8 with their dispositions and a unified, collision-free findings table.
- [ ] `SYNTHESIS.md` written at the fold location; the parent spoke resumed via the fold.
- [ ] Read-only honored; no rebuild; no GitHub write (the posted review is the grandparent gate's job).

## Suggested Methodology Files

This child is a **SYNTHESIS task → author/run it as a verification gate** (deployment obligation). Load
on demand via `engine_load_methodology { name: "<bundle_id>" }`:

- `synthesis/Synthesis_Overview_Methodology.md` — the anchor; the four-check gate model and the
  structured `SYNTHESIS.md` schema. Load first, always.
- `synthesis/Synthesis_Contract_Verification_Methodology.md` — assert the sub-contract identities
  (SV1–SV6) and the inherited schema conformance over the combined outputs.
- `synthesis/Synthesis_Duplication_Detection_Methodology.md` — detect a defect double-filed across the
  two children (a concern-7 evidence gap vs. a concern-8 scope note on the same line).
- `synthesis/Synthesis_Remediation_Methodology.md` — if an identity fails, schedule remediation as a
  decomposed fix-task (Inject) and re-verify, rather than plugging.

The gate posture is mandatory; which sibling check files you load and how deeply you run each check is
your judgment. Load `Synthesis_Overview` first, then the others your reading of the two partial findings
reveals you need.

## Inherited Constraints

- **Read-only** (I5): rely on the machine gate and the two partial findings; no rebuild; no GitHub write.
- **No silent plugs**: a failing identity is reported or remediated via amendment, never quietly fixed.
- **Severity discipline** (I4 / SV6): downgrade any `block`/`major` that is merely a hardening wish.
- Conform to the inherited `findings_schema.md`; do not redefine it.

## Out-of-Scope Methodologies

- `decomposition/` content is decomposer-side only — a synthesis gate never loads it.
- The per-artifact deep analyses (build, security, operability, Rust) are the grandparent DAG's other
  spokes; this gate integrates only concerns 7 and 8 into this spoke's findings.
- Rendering the overall PR verdict and posting the review belong to the grandparent
  `SUBTASK_verdict_synthesis`, not here.
