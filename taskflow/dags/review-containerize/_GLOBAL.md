# _GLOBAL.md — review-containerize (subtree hub)

Hub document for the review DAG that renders an authoritative APPROVE / REQUEST-CHANGES verdict on
**PR #22** (work-item **#12 `containerize`**). This is the narrative/strategic context every spoke
reads at boot. The machine-readable DAG is the **Task Summary** table below; the shared structural
seam is the **Contract** (`contracts/`).

## Project Context

**Status**: Active

### Objective

Review — not fix — PR #22 and produce ONE authoritative verdict. The work is split into five parallel
analysis spokes (one per coherent concern-domain) plus a synthesis gate that integrates the spoke
findings, maps them to the work-item's acceptance criteria, renders the single verdict, writes the
root `SYNTHESIS.md`, and posts the review to PR #22.

### What is under review

- **PR #22** — `work/containerize` → `main`, **Closes #12**, head `bc0c3c0d6380c9edd1b9433addc7fdcbffb55751`,
  base `main` (`7a81849` after #10 landed; PR OPEN/MERGEABLE/CLEAN). Review the diff of
  `work/containerize` against its merge base, **read-only**.
- **Work-item #12 `containerize`** (EPIC #3 devops, M3): a multi-stage container image for the chirp
  app that builds the release server **and** the wasm SPA bundle, runs non-root from a minimal
  runtime, health-checks `/healthz`, is configurable + documented, reproducible, reasonably small.
- **Deliverables in the diff**: `Dockerfile` (builder `rust:1.88-slim-bookworm` → runtime
  `gcr.io/distroless/cc-debian12:nonroot`), `.dockerignore`, `deploy/docker/healthcheck.rs` (std-only
  `/healthz` probe), `deploy/README.md`, a "Running chirp in a container" section in `README.md`, and
  a minimal `crates/chirp-server/src/main.rs` SIGTERM change (unix-gated).

### The code DAG's machine verdict (INPUT — do not re-run)

The code DAG `containerize` folded **PASS**. Its record is at
`/home/user/nousix-runtime/nswe-demo/taskflow/dags/containerize/SYNTHESIS.md` and is a **required
input for every spoke**. It records the build+run evidence (image `chirp:local` 41.7 MB,
`linux/amd64`, `USER 65532:65532` distroless; base images pinned by tag + `@sha256` digest; all cargo
builds `--locked`; `/healthz`→200, SPA + client-route fallback + `/pkg/*.wasm` (`application/wasm`) +
`POST /api/users`→201 all served; `HEALTHCHECK` healthy; `docker stop` SIGTERM exits 0; `cargo
fmt`/`clippy -D warnings`/`test` 20-passed clean after the SIGTERM change) and the nine acceptance
criteria. **Rely on this machine gate for build/test facts; do not rebuild to reconfirm a green gate.**
The spokes' job is JUDGMENT over the diff, not re-execution.

### How to access the change (read-only)

The local checkout directory is NOT a git repo; use authenticated `gh` (account `mattsmcknight`,
`repo` scope) against `Nousix-LLC/nswe-demo`:
- `gh pr view 22 --repo Nousix-LLC/nswe-demo` — PR metadata.
- `gh pr diff 22 --repo Nousix-LLC/nswe-demo` — the full diff.
- `gh api repos/Nousix-LLC/nswe-demo/contents/<path>?ref=bc0c3c0d...` — a specific file blob at head.
Read-only only. No clone-and-mutate, no push, no checkout that writes to a tracked branch.

### Scope

**In scope**: judgment over PR #22's diff against the eight concerns, mapped to the acceptance
criteria, yielding one verdict + severity-tagged findings.

**Out of scope**: editing/fixing the PR; re-running the container build; reviewing #11 (`.github/`
CI/GHCR), #13 (k8s/ArgoCD), or any live deploy — except to CONFIRM this diff did not stray into them
(that confirmation is itself concern #8).

### Success Criteria

- [ ] All 8 brief concerns covered exactly once across the spokes (contract identity I1).
- [ ] Root `SYNTHESIS.md` carries ONE APPROVE / REQUEST-CHANGES verdict (identity I3).
- [ ] Explicit per-acceptance-criterion pass/fail for all nine criteria (identity I6).
- [ ] Severity-tagged findings (block/major/minor/nit) with location + evidence + remediation for each block/major (identity I4).
- [ ] A review posted to PR #22 (or a review comment if a formal self-approval is blocked).
- [ ] Read-only honored throughout (identity I5).

## Constraints and Requirements

- **Read-only** (identity I5): no edit/stage/commit/push/rebase/relock/merge; `main` and
  `work/containerize` untouched. The only GitHub write is the synthesis gate's single posted review on PR #22.
- **Rely on the machine gate** for build/test facts; do not rebuild.
- **Repo scope**: `Nousix-LLC/nswe-demo` only.
- **One verdict**: rendered solely in the root `SYNTHESIS.md`; the gh review state is secondary to it.

## Methodology

Each spoke selects its own methodology from the bundle IDs its `_BRIEF.md` names (the code-review
bundle is the spine for every spoke; each adds what its concern-domain warrants). Bundle IDs are
loaded on demand by the executing spoke via `engine_load_methodology { name: "<bundle_id>" }`.

## Task Structure

### Overview

```
_GLOBAL.md (this hub)
├── contracts/
│   ├── _MANIFEST.yaml          (concern->spoke ownership, identities, severity taxonomy)
│   └── findings_schema.md      (the shared findings shape every spoke conforms to)
├── SUBTASK_dockerfile_build/_BRIEF.md       (concerns 1,2 + Dockerfile/shell idiom slice of 6)
├── SUBTASK_security_supplychain/_BRIEF.md   (concern 3 + secret-leakage slice of 2)
├── SUBTASK_operability_docs/_BRIEF.md       (concern 4 + docs slice of 6)
├── SUBTASK_rustcode_sigterm/_BRIEF.md       (concern 5 + Rust/probe idiom slice of 6)
├── SUBTASK_scope_verification/_BRIEF.md     (concerns 7,8)
└── SUBTASK_verdict_synthesis/_BRIEF.md      (synthesis gate — renders the verdict, posts the review)
```

### Task Summary

| Task id | Depends on | Description | Output |
|---------|------------|-------------|--------|
| `SUBTASK_dockerfile_build` | none | Concern 1 (build correctness & reproducibility) + concern 2 (runtime image layer composition & size) + Dockerfile/shell idiom slice of concern 6 | `SUBTASK_dockerfile_build/findings.md` |
| `SUBTASK_security_supplychain` | none | Concern 3 (container security posture + supply-chain / dependency trust boundary) + the secret/credential-leakage face of concern 2 | `SUBTASK_security_supplychain/findings.md` |
| `SUBTASK_operability_docs` | none | Concern 4 (operability: HEALTHCHECK, one-knob port, config, logging, out-of-box) + documentation clarity/accuracy slice of concern 6 | `SUBTASK_operability_docs/findings.md` |
| `SUBTASK_rustcode_sigterm` | none | Concern 5 (SIGTERM handling in `main.rs`: correctness, unix-gating, no regression, scope fit) + Rust/probe idiom slice of concern 6 | `SUBTASK_rustcode_sigterm/findings.md` |
| `SUBTASK_scope_verification` | none | Concern 7 (verification depth — does the machine-gate evidence demonstrate the acceptance criteria) + concern 8 (scope conformance) | `SUBTASK_scope_verification/findings.md` |
| `SUBTASK_verdict_synthesis` | `SUBTASK_dockerfile_build`, `SUBTASK_security_supplychain`, `SUBTASK_operability_docs`, `SUBTASK_rustcode_sigterm`, `SUBTASK_scope_verification` | Synthesis/verification GATE: evaluate contract identities I1–I6 over the spoke findings, map to the nine acceptance criteria, render the single APPROVE/REQUEST-CHANGES verdict, write root `SYNTHESIS.md`, post the review on PR #22 | `SYNTHESIS.md` (at DAG root) + posted PR #22 review |

### Dependency Graph

```
SUBTASK_dockerfile_build     ──┐
SUBTASK_security_supplychain ──┤
SUBTASK_operability_docs     ──┼── SUBTASK_verdict_synthesis
SUBTASK_rustcode_sigterm     ──┤
SUBTASK_scope_verification   ──┘
```

## Contract

**Contract location**: `contracts/` (read-only for every descendant).
**Contract kind**: `taxonomy` — finding categories + severity rubric + per-concern ownership partition + verdict rule.

### Structural Declarations

| Artifact | Kind | Declares |
|---|---|---|
| `contracts/findings_schema.md` | taxonomy | The shape of each spoke's `findings.md`: per-concern disposition + the findings table (Finding ID / Concern / Severity / Location / Evidence / Remediation) + the severity rubric. |
| `contracts/_MANIFEST.yaml` | manifest | concern→spoke ownership (every concern owned once), finding-ID prefixes, and identities I1–I6. |

### Ownership

| Concern | Owning spoke |
|---|---|
| 1 Dockerfile build correctness & reproducibility | `SUBTASK_dockerfile_build` |
| 2 Runtime image hygiene & size (layer composition + size) | `SUBTASK_dockerfile_build` |
| 2 secret/credential leakage (security face) | `SUBTASK_security_supplychain` |
| 3 Container security posture + supply-chain | `SUBTASK_security_supplychain` |
| 4 Operability | `SUBTASK_operability_docs` |
| 5 SIGTERM `main.rs` correctness | `SUBTASK_rustcode_sigterm` |
| 6 code quality & idiom | partitioned by artifact: Dockerfile/shell→build; Rust(SIGTERM+probe)→rustcode; docs→operability |
| 7 verification depth | `SUBTASK_scope_verification` |
| 8 scope conformance | `SUBTASK_scope_verification` |
| verdict integration | `SUBTASK_verdict_synthesis` |

### Identities (evaluated at the synthesis gate; never silently plugged)

- [ ] **I1 coverage** — every concern 1..8 addressed exactly once with an explicit disposition.
- [ ] **I2 concern-6 / concern-2 seam** — idiom partitioned by artifact; concern-2 layer-vs-leakage seam respected; no defect double-filed.
- [ ] **I3 verdict rule** — REQUEST-CHANGES iff ≥1 open `block`; APPROVE requires an explicit call on every open `major`; exactly one verdict.
- [ ] **I4 severity discipline** — no `block`/`major` that is merely a hardening wish; downgrade such to minor/nit.
- [ ] **I5 read-only** — nothing edited/committed/pushed/merged; only write is the posted PR review.
- [ ] **I6 acceptance-criteria map** — explicit pass/fail per the nine work-item acceptance criteria.

### Derived Artifacts

None mechanical — this is a review taxonomy. The synthesis gate IS the integration step that
evaluates the identities above.

## Output Specifications

| Deliverable | Format | Location | Description |
|---|---|---|---|
| Per-spoke findings | Markdown | `SUBTASK_*/findings.md` | Concern dispositions + severity-tagged findings per `findings_schema.md` |
| Root verdict | Markdown | `SYNTHESIS.md` (DAG root) | The ONE APPROVE/REQUEST-CHANGES verdict, acceptance-criteria map, consolidated findings |
| Posted review | gh review / comment | PR #22 | The verdict + key findings posted on `Nousix-LLC/nswe-demo#22` |
