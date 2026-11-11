# Task: Review — verification depth & scope conformance (PR #22)

## Task Specification

**Slug**: SUBTASK_scope_verification
**Task Kind**: standard
**Status**: Pending

### Objective

Render the two cross-cutting review judgments — does the machine gate's evidence actually
**demonstrate the acceptance criteria**, and does the diff **stay within work-item #12's scope** —
and emit `findings.md` per the contract.

### Context

Part of the review-containerize DAG (see `../_GLOBAL.md` and `../contracts/`). One of five parallel
analysis spokes; findings feed `SUBTASK_verdict_synthesis`. These two concerns are cross-cutting
(they range over the whole diff), which is why they are a dedicated spoke rather than folded into a
single-artifact analysis.

**Dependencies**: none. **Dependents**: `SUBTASK_verdict_synthesis`.

### Concerns owned (cover each explicitly)

- **Concern 7 — testing / verification depth**: whether the machine gate's build+run evidence (in
  `containerize/SYNTHESIS.md`) actually demonstrates each work-item #12 acceptance criterion, and
  whether anything material is left **unverified** (e.g. a claimed behavior with no corresponding
  evidence, a criterion asserted but not exercised). You assess the *adequacy of the evidence*, not
  re-run the build.
- **Concern 8 — scope conformance**: containerization only. The diff MUST NOT author CI
  workflows / GHCR push (that is `#11 ci-actions`'s `.github/`), k8s/ArgoCD manifests (`#13`), or
  perform any live registry/cluster deploy. Confirm the diff stays in #12's scope — the `Dockerfile`
  being the artifact #11's image-build job later consumes is a **declared, honest hand-off, not a
  scope breach**; distinguish the two.

### Input Specification

| Input | Source | Purpose |
|---|---|---|
| Hub | `../_GLOBAL.md` | Shared context, PR coordinates, read-only constraint |
| Contract | `../contracts/_MANIFEST.yaml`, `../contracts/findings_schema.md` | Ownership + `findings.md` shape + severity rubric |
| Machine gate | `/home/user/nousix-runtime/nswe-demo/taskflow/dags/containerize/SYNTHESIS.md` | The build/run evidence + the nine acceptance criteria whose demonstration you assess |
| The diff (file list + content) | `gh pr diff 22 --repo Nousix-LLC/nswe-demo`; `gh pr view 22 --json files` | Confirm which paths the PR touches (scope) (read-only) |

### Process (approach, not a runbook)

For concern 7: walk each of the nine acceptance criteria in the machine gate and judge whether the
recorded evidence genuinely demonstrates it, flagging any criterion that is asserted but not evidenced,
or evidenced weakly. For concern 8: enumerate the files the PR touches and confirm none fall under
`.github/` (CI), k8s/ArgoCD manifest paths, or live-deploy actions; confirm the `Dockerfile`-as-handoff
is a declared boundary, not an incursion. Record findings with location + evidence + (block/major)
remediation, honoring the severity discipline. You decide depth and any further breakdown.

### Output Specification

| Attribute | Value |
|---|---|
| Filename | `findings.md` |
| Location | this workspace (`SUBTASK_scope_verification/`) |
| Shape | exactly `../contracts/findings_schema.md` |

### Success Criteria

- [ ] Concern 7 and concern 8 each carry an explicit disposition.
- [ ] Concern 7: each of the nine acceptance criteria is called "evidenced" / "weakly evidenced" / "unverified" with the specific evidence cited.
- [ ] Concern 8: the exact touched-file set is enumerated and judged in/out of #12's scope, with the handoff-vs-breach distinction made explicit.
- [ ] Every block/major has location + evidence + remediation; read-only honored; no rebuild.

## Suggested Methodology Files

Domain Mapping rows matched (verbatim): **"Code review | Code Review | Core, Testing"** and
**"Writing tests | Testing | Core"** (the verification-adequacy lens). Load on demand via
`engine_load_methodology { name: "<bundle_id>" }`:

- `testing/Testing_Strategy_Methodology.md` — what "adequate verification" means; mapping evidence to criteria (concern 7).
- `testing/Testing_Integration_Testing_Methodology.md` — judging whether the build-and-run evidence exercises the real acceptance paths.
- `code-review/CodeReview_Process_Methodology.md` — scope-conformance and change-boundary discipline (concern 8).

Flagged by task type; load as a starting point, you are the final judge — fewer if inapplicable, more if the diff reveals it.

## Inherited Constraints

- **Read-only** (I5); do not rebuild; only the synthesis gate posts to GitHub.
- Rely on the machine gate for build/test FACTS; your job is to judge whether those facts SUFFICE to demonstrate the criteria, and whether the diff stays in scope.
- Severity discipline (I4): "more tests would be nice" is minor; a criterion that is genuinely unverified or a real out-of-scope file is major/block as warranted.
- Adjacent items for the scope boundary: `#11 ci-actions` (`.github/`), `#13 deploy-argocd` (k8s/ArgoCD). PR #22 head `bc0c3c0d...`; repo `Nousix-LLC/nswe-demo`.

## Out-of-Scope Methodologies

- The per-artifact deep analyses (build, security, operability, Rust) → owned by the other four spokes; here you assess verification *adequacy* and scope *boundary*, not re-adjudicate their domains.
- `decomposition/` and `synthesis/` bundles are not for this analysis spoke.
