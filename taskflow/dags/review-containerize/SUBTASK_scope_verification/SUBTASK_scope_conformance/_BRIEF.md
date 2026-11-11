# Task: Scope conformance — does PR #22's diff stay within work-item #12's scope

## Task Specification

**Slug**: SUBTASK_scope_conformance
**Task Kind**: standard
**Status**: Pending

### Objective

Confirm PR #22's diff stays inside work-item #12's scope (containerization only) and emit
`scope_findings.md` conforming to the inherited findings schema — enumerating the exact touched-file
set and judging each path in/out of scope, with the Dockerfile-handoff-vs-breach distinction explicit.

### Context

This is concern 8 of the scope-&-verification spoke (see `../_GLOBAL.md` and `../contracts/`). It is
one of two parallel analysis children; its output is merged by `SUBTASK_findings_synthesis` into the
single `findings.md` the spoke owes.

**Dependencies**: none. **Dependents**: `SUBTASK_findings_synthesis`.

### Concern owned

- **Concern 8 — scope conformance**: containerization only. The diff MUST NOT author CI workflows /
  GHCR push (that is `#11 ci-actions`'s `.github/`), k8s/ArgoCD manifests (`#13 deploy-argocd`), or
  perform any live registry/cluster deploy. Confirm the diff stays in #12's scope — the `Dockerfile`
  being the artifact #11's image-build job later consumes is a **declared, honest hand-off, not a
  scope breach**; distinguish the two explicitly.

### Input Specification

| Input | Source | Purpose |
|---|---|---|
| Subtree hub | `../_GLOBAL.md` | Subtree objective, posture, read-only constraint |
| Grandparent hub | `../../_GLOBAL.md` | PR coordinates; adjacent work-items #11 (`.github/`) and #13 (k8s/ArgoCD) |
| Inherited schema | `../../contracts/findings_schema.md` | The `findings.md` shape + severity rubric to conform to |
| Sub-contract | `../contracts/_MANIFEST.yaml` | Your `SCOPE-S*` finding-ID prefix; identity SV3 |
| PR file list | `gh pr view 22 --repo Nousix-LLC/nswe-demo --json files` (read-only) | The authoritative touched-file set |
| The diff | `gh pr diff 22 --repo Nousix-LLC/nswe-demo` (read-only) | Confirm what each touched file actually contains |

### Approach (not a runbook)

Enumerate the files PR #22 touches and confirm none fall under `.github/` (CI), k8s/ArgoCD manifest
paths, or live-deploy actions; judge each touched path in/out of work-item #12's scope. Make the
`Dockerfile`-as-handoff distinction explicit: a Dockerfile that #11's image-build job later consumes
is a declared boundary, not an incursion into #11. Honor the severity discipline: a real out-of-scope
file is `major`/`block`; a posture preference about where a boundary "should" sit is `minor`/`nit`.
Record findings with location + evidence + (block/major) remediation. You decide depth and any further
breakdown.

### Output Specification

| Attribute | Value |
|---|---|
| Filename | `scope_findings.md` |
| Location | this workspace (`SUBTASK_scope_conformance/`) |
| Shape | the per-concern disposition block for concern 8 + an enumerated touched-file table + a findings table in `../../contracts/findings_schema.md` shape, using the `SCOPE-S` prefix |

### Success Criteria

- [ ] Concern 8 carries an explicit disposition (PASS | PASS-WITH-NOTES | FAIL).
- [ ] The complete PR #22 touched-file set is enumerated and each path judged in/out of #12 scope
      (identity SV3), with the handoff-vs-breach distinction made explicit.
- [ ] Every `block`/`major` has location + evidence + remediation; finding IDs use `SCOPE-S<n>`.
- [ ] Read-only honored; no GitHub write.

## Suggested Methodology Files

Domain Mapping row matched (verbatim): **"Code review | Code Review | Core, Testing"** — the
change-boundary / scope-conformance lens. Load on demand via `engine_load_methodology { name: "<bundle_id>" }`:

- `code-review/CodeReview_Process_Methodology.md` — scope-conformance and change-boundary discipline:
  judging whether a diff stays within its declared responsibility and distinguishing a declared
  hand-off from scope creep.

The above is a suggestion based on the task type. Load it as a starting point but you are the final
judge of what your work requires — load fewer if clearly inapplicable, more if the diff reveals
additional methodology surface.

## Inherited Constraints

- **Read-only** (I5): diff access via authenticated read-only `gh` (account `mattsmcknight`); no
  edit/stage/commit/push/merge; no GitHub write.
- **Severity discipline** (I4 / SV6): only a real out-of-scope file is `major`/`block`; a boundary
  posture preference is `minor`/`nit`.
- The `Dockerfile`-as-handoff-to-#11 is a declared boundary, NOT a breach — do not file it as an
  out-of-scope finding; state the distinction explicitly.
- Conform to the inherited `findings_schema.md`; do not redefine it. Use the `SCOPE-S` finding-ID prefix.

## Out-of-Scope Methodologies

- Verification/evidence-adequacy (concern 7) belongs to the sibling `SUBTASK_verification_depth` — do
  not assess the acceptance-criteria evidence here; cross-reference by note if needed, do not re-file.
- The per-artifact deep analyses (build, security, operability, Rust) are owned by the four sibling
  spokes of the grandparent DAG; here you judge the scope *boundary* only.
- `decomposition/` and `synthesis/` bundles are not for this analysis child.
