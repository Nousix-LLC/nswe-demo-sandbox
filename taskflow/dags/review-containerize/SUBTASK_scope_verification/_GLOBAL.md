# _GLOBAL.md — SUBTASK_scope_verification (subtree hub)

Hub document for the sub-decomposition of the **scope & verification** spoke of the
review-containerize DAG (PR #22 / work-item #12). This subtree splits the two distinct
cross-cutting concerns this spoke owns into two parallel analysis children plus a synthesis
gate that folds them into the ONE `findings.md` this spoke owes to its parent DAG.

## Project Context

**Status**: Active

### Objective

Render the two cross-cutting review judgments the parent assigned to `SUBTASK_scope_verification`
and emit a single `findings.md` conforming to the inherited `../contracts/findings_schema.md`:

- **Concern 7 — verification / evidence adequacy**: does the machine gate's build+run evidence (in
  `taskflow/dags/containerize/SYNTHESIS.md`) actually demonstrate each of work-item #12's nine
  acceptance criteria, and is anything material left unverified?
- **Concern 8 — scope conformance**: does PR #22's diff stay inside #12's scope (containerization
  only — no `.github/` CI, no k8s/ArgoCD manifests, no live deploy), with the `Dockerfile`-as-handoff
  to #11 recognized as a declared boundary rather than a scope breach?

### Why this spoke decomposed

The parent brief enumerates **two distinct concerns** (7 and 8) with **distinct primary inputs**
(the machine-gate evidence record vs. the PR file manifest) and **distinct methodology lenses**
(the testing/verification-adequacy bundle vs. the code-review/change-boundary bundle). That is a
fired Scope-Based trigger (enumerated concerns + multiple methodologies) and a passed Distinct
Concerns Test — the two judgments could be rendered by two different reviewers in parallel. Per
Trigger Precedence the single declared output does not override the fired scope trigger, so this
spoke is decomposed into two parallel analysis children and one synthesis gate.

### Scope

**In scope**: judgment over PR #22's diff for concerns 7 and 8, folded into one schema-conformant
`findings.md`.

**Out of scope**: the per-artifact deep analyses (build, security, operability, Rust) owned by the
four sibling spokes; editing/fixing the PR; re-running the container build; posting to GitHub (the
grandparent verdict-synthesis gate alone posts the review).

### Success Criteria

- [ ] Concern 7 and concern 8 each carry an explicit per-concern disposition.
- [ ] Concern 7: each of the nine acceptance criteria is individually called `evidenced` /
      `weakly evidenced` / `unverified` with the specific machine-gate evidence cited.
- [ ] Concern 8: the exact touched-file set is enumerated and judged in/out of #12's scope, with the
      handoff-vs-breach distinction made explicit.
- [ ] The merged `findings.md` conforms exactly to `../contracts/findings_schema.md`; every
      `block`/`major` carries location + evidence + remediation; read-only honored; no rebuild.
- [ ] No finding-ID collision across the two spokes (the `SCOPE-V*` / `SCOPE-S*` partition holds).

## Constraints and Requirements

- **Read-only (identity I5)**: no edit/stage/commit/push/rebase/relock/merge; `main` and
  `work/containerize` untouched. No GitHub writes from this subtree at all (the posted review is the
  grandparent synthesis gate's job alone).
- **Rely on the machine gate** at `taskflow/dags/containerize/SYNTHESIS.md` for build/test FACTS; the
  work is to JUDGE whether those facts SUFFICE to demonstrate the criteria and whether the diff stays
  in scope — never to rebuild.
- **Severity discipline (identity I4)**: "more tests would be nice" / a hardening wish is `minor`/`nit`;
  only a genuinely unverified criterion or a real out-of-scope file is `major`/`block`.
- **Repo scope**: `Nousix-LLC/nswe-demo` only; diff access via authenticated read-only `gh`
  (account `mattsmcknight`). PR #22 head `bc0c3c0d6380c9edd1b9433addc7fdcbffb55751`.

## Subtree Methodology Posture

- **Dominant task type**: code review / verification. The subtree splits across two Domain-Mapping
  rows: **"Writing tests | Testing | Core"** (the verification-adequacy lens, concern 7) and
  **"Code review | Code Review | Core, Testing"** (the scope-boundary lens, concern 8).
- **Primary bundles** descendants should assume in scope: `testing` (concern 7), `code-review`
  (concern 8); the synthesis child additionally assumes `synthesis`.
- **Cross-cutting binding**: every child composes against the inherited `../contracts/findings_schema.md`
  shape and the sub-contract's `SCOPE-V*`/`SCOPE-S*` finding-ID partition. These bind the whole subtree.
- Suggestion, not prescription: each descendant is the final judge of what it loads.

## Subtree-Wide Constraints

- Inherited from the grandparent hub (`../../_GLOBAL.md`) and the grandparent contract
  (`../../contracts/`): read-only (I5); rely on the machine gate (no rebuild); severity discipline (I4);
  one finding per defect per owner (I2 seam); concern→owner partition.
- The `findings_schema.md` column set and severity rubric are inherited verbatim and MUST NOT be
  redefined — descendants compose against them.

## Task Structure

### Overview

```
_GLOBAL.md (this hub)
├── contracts/
│   └── _MANIFEST.yaml                         (taxonomy sub-contract: SCOPE-ID partition + merge identities)
├── SUBTASK_verification_depth/_BRIEF.md        (concern 7 — nine-criteria evidence adequacy)
├── SUBTASK_scope_conformance/_BRIEF.md         (concern 8 — touched-file scope boundary)
└── SUBTASK_findings_synthesis/_BRIEF.md        (synthesis gate — folds into findings.md)
```

### Task Summary

| Task id | Depends on | Description | Output |
|---------|------------|-------------|--------|
| `SUBTASK_verification_depth` | none | Concern 7: walk the nine work-item #12 acceptance criteria against the machine-gate evidence; call each evidenced / weakly evidenced / unverified | `SUBTASK_verification_depth/verification_findings.md` |
| `SUBTASK_scope_conformance` | none | Concern 8: enumerate PR #22's touched files; judge each in/out of #12 scope; make the Dockerfile-handoff-vs-breach distinction explicit | `SUBTASK_scope_conformance/scope_findings.md` |
| `SUBTASK_findings_synthesis` | `SUBTASK_verification_depth`, `SUBTASK_scope_conformance` | Synthesis/verification GATE: evaluate the sub-contract identities over the two partial findings, merge them into the ONE schema-conformant `findings.md`, write the fold record | `findings.md` (at this spoke's workspace) + `SYNTHESIS.md` (fold record) |

### Dependency Graph

```
SUBTASK_verification_depth ──┐
                             ├── SUBTASK_findings_synthesis
SUBTASK_scope_conformance  ──┘
```

## Contract

**Contract location**: `contracts/` (read-only for every descendant).
**Contract kind**: `taxonomy` — extends (never overrides) the inherited `../contracts/findings_schema.md`.

### Inherited Contracts

| Ancestor contract | Path | What it binds here |
|---|---|---|
| Review findings schema | `../contracts/findings_schema.md` | The exact `findings.md` shape every output conforms to (per-concern disposition block + Finding ID/Concern/Severity/Location/Evidence/Remediation table + severity rubric). |
| Review manifest | `../contracts/_MANIFEST.yaml` | `SCOPE` finding-ID prefix for this spoke; concern 7+8 ownership; identities I1–I6; severity taxonomy `[block, major, minor, nit]`. |

### Structural Declarations

| Artifact | Kind | Declares |
|---|---|---|
| `contracts/_MANIFEST.yaml` | taxonomy | The `SCOPE-V*` (verification) / `SCOPE-S*` (scope) finding-ID partition of the inherited `SCOPE` namespace, per-concern ownership across the two spokes, and the merge identities the synthesis gate asserts. |

### Ownership

| Concern / artifact | Owning child |
|---|---|
| Concern 7 disposition + nine-criteria evidence-adequacy table | `SUBTASK_verification_depth` |
| Concern 8 disposition + touched-file scope table | `SUBTASK_scope_conformance` |
| Merged `findings.md` + fold `SYNTHESIS.md` | `SUBTASK_findings_synthesis` |

### Identities (evaluated at the synthesis gate; never silently plugged)

- [ ] **SV1 coverage** — concern 7 and concern 8 each carry exactly one explicit disposition.
- [ ] **SV2 nine-criteria completeness** — all nine acceptance criteria appear in the verification
      output, each with an evidenced / weakly evidenced / unverified call and cited evidence.
- [ ] **SV3 file-set completeness** — the scope output enumerates the complete PR #22 touched-file set
      and judges each in/out of #12 scope, with the Dockerfile-handoff-vs-breach distinction explicit.
- [ ] **SV4 ID partition** — every finding ID matches `SCOPE-V<n>` or `SCOPE-S<n>`; no collision.
- [ ] **SV5 schema conformance** — the merged `findings.md` matches `../contracts/findings_schema.md`
      exactly; every `block`/`major` has location + evidence + remediation.
- [ ] **SV6 severity discipline** — no `block`/`major` that is merely a hardening wish (downgrade to
      minor/nit per I4).

### Derived Artifacts

None mechanical — this is a review taxonomy. The synthesis child IS the integration step that merges
the partial findings and evaluates SV1–SV6.

## Output Specifications

| Deliverable | Format | Location | Description |
|---|---|---|---|
| Verification partial findings | Markdown | `SUBTASK_verification_depth/verification_findings.md` | Concern 7 disposition + nine-criteria table + `SCOPE-V*` findings |
| Scope partial findings | Markdown | `SUBTASK_scope_conformance/scope_findings.md` | Concern 8 disposition + touched-file table + `SCOPE-S*` findings |
| Merged spoke findings | Markdown | `findings.md` (this spoke's workspace) | The ONE `findings_schema.md`-conformant findings document this spoke owes its parent DAG |
