# Task: Review — Dockerfile build correctness, reproducibility & runtime image composition (PR #22)

## Task Specification

**Slug**: SUBTASK_dockerfile_build
**Task Kind**: standard
**Status**: Pending

### Objective

Render a reviewer's judgment over PR #22's **build and image-composition** story: whether the
multi-stage `Dockerfile` is correct and reproducible, and whether the runtime image carries only what
it must at a reasonable size — and emit `findings.md` per the contract.

### Context

Part of the review-containerize DAG (see `../_GLOBAL.md` and `../contracts/`). This is one of five
parallel analysis spokes; its findings feed `SUBTASK_verdict_synthesis`.

**Dependencies**: none. **Dependents**: `SUBTASK_verdict_synthesis`.

### Concerns owned (cover each explicitly)

- **Concern 1 — Dockerfile build correctness & reproducibility**: multi-stage correctness; the builder
  actually produces BOTH the release `chirp-server` AND the `wasm-bindgen --target web` SPA bundle;
  `--locked` throughout; base images pinned by tag **and** `@sha256` digest; the `wasm-bindgen-cli`
  version matches the `wasm-bindgen` crate in `Cargo.lock`; the builder-Rust-1.88-vs-workspace-MSRV-1.82
  bump is sound and justified; `.dockerignore` trims the context without excluding anything the build needs.
- **Concern 2 (layer composition + size face)**: the distroless runtime carries only what it must
  (server binary, probe, SPA bundle); no toolchain/source leakage into runtime layers; the glibc ABI
  match (bookworm builder ↔ `cc-debian12` runtime) is correct; size (41.7 MB) is reasonable and the
  reported breakdown holds. **The secret/credential-leakage face of concern 2 is OWNED BY
  `SUBTASK_security_supplychain` — do not re-file it here; cross-reference by note if relevant.**
- **Concern 6 (Dockerfile/shell idiom slice only)**: clarity, maintainability, and idiom of the
  Dockerfile and any shell in it.

### Input Specification

| Input | Source | Purpose |
|---|---|---|
| Hub | `../_GLOBAL.md` | Shared context, PR coordinates, read-only constraint |
| Contract | `../contracts/_MANIFEST.yaml`, `../contracts/findings_schema.md` | Ownership + the exact `findings.md` shape + severity rubric |
| Machine gate | `/home/user/nousix-runtime/nswe-demo/taskflow/dags/containerize/SYNTHESIS.md` | Authoritative build/run facts — rely on it, do not rebuild |
| The diff | `gh pr diff 22 --repo Nousix-LLC/nswe-demo`; file blobs via `gh api .../contents/<path>?ref=bc0c3c0d...` | The `Dockerfile` and `.dockerignore` under review (read-only) |

### Process (approach, not a runbook)

Read the `Dockerfile` and `.dockerignore` from the diff at head `bc0c3c0d`. Evaluate build correctness
and reproducibility against the machine-gate evidence and the acceptance criteria; confirm digest
pinning and `--locked` claims against the actual file content rather than the summary. Apply the
containerization build methodology for what "correct and reproducible" means. Record each finding with
a concrete location + evidence + (for block/major) remediation, honoring the severity discipline
(a block/major is a concrete landable defect, not a hardening wish). You decide depth and whether this
is one coherent analysis or needs further breakdown.

### Output Specification

| Attribute | Value |
|---|---|
| Filename | `findings.md` |
| Location | this workspace (`SUBTASK_dockerfile_build/`) |
| Shape | exactly `../contracts/findings_schema.md` (header, per-concern disposition, findings table) |

### Success Criteria

- [ ] Concerns 1, 2 (layer/size face), and the Dockerfile/shell slice of 6 each carry an explicit disposition.
- [ ] Every finding has a concrete location + evidence; every block/major has remediation.
- [ ] Reproducibility/`--locked`/digest claims checked against the actual diff, not just the gate summary.
- [ ] Read-only honored; no rebuild performed.

## Suggested Methodology Files

Domain Mapping row matched (verbatim): **"Docker setup / Dockerfile authoring | Containerization | Operations"**;
plus **"Code review | Code Review | Core, Testing"** (this is a review). Load bundles on demand via
`engine_load_methodology { name: "<bundle_id>" }`:

- `containerization/Containerization_Docker_Build_Methodology.md` — multi-stage build correctness, build-context hygiene, reproducibility/pinning: the core of concern 1.
- `containerization/Containerization_Runtime_Methodology.md` — runtime-layer minimality and what a distroless image should carry: the layer-composition face of concern 2.
- `code-review/CodeReview_Checklist_Methodology.md` — keeps the review systematic and severity-calibrated.
- `core/BestPractices_Coding_Standards_Methodology.md` — baseline for the Dockerfile/shell idiom slice of concern 6.

The above are flagged by task type; load these as a starting point but you are the final judge — load
fewer if clearly inapplicable, more if your reading of the diff reveals methodology surface not anticipated here.

## Inherited Constraints

- **Read-only** (contract I5): no edit/commit/push/merge; only the synthesis gate posts to GitHub.
- **Do not rebuild** to reconfirm the green machine gate; judge the diff.
- Severity discipline (I4): block/major = concrete landable defect only.
- PR #22 head is `bc0c3c0d6380c9edd1b9433addc7fdcbffb55751`; repo `Nousix-LLC/nswe-demo`.

## Out-of-Scope Methodologies

- Secret/credential leakage, supply-chain trust, non-root posture → owned by `SUBTASK_security_supplychain`; do not load the Security bundle to re-adjudicate them here.
- `decomposition/` and `synthesis/` bundles are decomposer/gate-side; not for this analysis spoke.
