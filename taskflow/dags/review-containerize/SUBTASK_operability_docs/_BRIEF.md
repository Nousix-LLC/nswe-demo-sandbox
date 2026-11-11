# Task: Review — operability (healthcheck, config, logging) & documentation accuracy (PR #22)

## Task Specification

**Slug**: SUBTASK_operability_docs
**Task Kind**: standard
**Status**: Pending

### Objective

Render an operator's judgment over PR #22's **operability** and whether its **documentation matches
real behavior**, and emit `findings.md` per the contract.

### Context

Part of the review-containerize DAG (see `../_GLOBAL.md` and `../contracts/`). One of five parallel
analysis spokes; findings feed `SUBTASK_verdict_synthesis`.

**Dependencies**: none. **Dependents**: `SUBTASK_verdict_synthesis`.

### Concerns owned (cover each explicitly)

- **Concern 4 — operability**: the `HEALTHCHECK` genuinely exercises `/healthz`; the standalone probe
  (`deploy/docker/healthcheck.rs`) derives its port from the same `CHIRP_BIND_ADDR` the server reads
  (one knob, not two that can drift); bind addr / static-asset path (`CHIRP_STATIC_DIR`) / log level
  (`RUST_LOG`) are configurable and documented; logs go to stdout/stderr; the image starts and serves
  SPA + API out of the box on the in-memory default (no external DB).
- **Concern 6 (documentation slice)**: clarity and maintainability of `deploy/README.md` and the
  `README.md` "Running chirp in a container" section, AND crucially whether the docs MATCH the real
  behavior of the diff (commands, env vars, ports, defaults). Documentation idiom for the probe's
  behavior-facing text is in scope here; the probe's Rust idiom is owned by `SUBTASK_rustcode_sigterm`.

### Input Specification

| Input | Source | Purpose |
|---|---|---|
| Hub | `../_GLOBAL.md` | Shared context, PR coordinates, read-only constraint |
| Contract | `../contracts/_MANIFEST.yaml`, `../contracts/findings_schema.md` | Ownership + `findings.md` shape + severity rubric |
| Machine gate | `/home/user/nousix-runtime/nswe-demo/taskflow/dags/containerize/SYNTHESIS.md` | Authoritative run facts (healthcheck healthy, config vars, out-of-box serve) — rely on it |
| The diff | `gh pr diff 22 --repo Nousix-LLC/nswe-demo`; blobs via `gh api .../contents/<path>?ref=bc0c3c0d...` | `Dockerfile` (HEALTHCHECK/ENV/ENTRYPOINT), `deploy/README.md`, `README.md`, `deploy/docker/healthcheck.rs` (behavior) under review |

### Process (approach, not a runbook)

Read the operability-facing parts of the diff (the `HEALTHCHECK`/`ENV`/`ENTRYPOINT` in the Dockerfile,
the probe's port-derivation, and both docs). Check that the documented build/run/config/healthcheck
instructions correspond to what the diff actually does and to the machine-gate evidence — a doc that
claims a flag or env var the image does not honor is a concrete landable defect. Apply observability /
documentation methodology. Record each finding with location + evidence + (block/major) remediation,
honoring the severity discipline. You decide depth and any further breakdown.

### Output Specification

| Attribute | Value |
|---|---|
| Filename | `findings.md` |
| Location | this workspace (`SUBTASK_operability_docs/`) |
| Shape | exactly `../contracts/findings_schema.md` |

### Success Criteria

- [ ] Concern 4 and the documentation slice of concern 6 each carry an explicit disposition.
- [ ] Docs-match-behavior checked concretely (every documented command/env/port cross-checked against the diff).
- [ ] One-knob port derivation (probe ↔ server via `CHIRP_BIND_ADDR`) explicitly judged.
- [ ] Every block/major has location + remediation; read-only honored; no rebuild.

## Suggested Methodology Files

Domain Mapping rows matched (verbatim): **"Incident response | Operations | -"** / **"CI/CD setup | Operations | Security"**
(the operability/observability surface) and **"Code review | Code Review | Core, Testing"**. Load on demand via
`engine_load_methodology { name: "<bundle_id>" }`:

- `operations/Observability_Monitoring_Methodology.md` — what a health check must actually prove (liveness vs readiness); the HEALTHCHECK concern.
- `operations/Observability_Logging_Methodology.md` — stdout/stderr logging and log-level configurability.
- `operations/BestPractices_Documentation_Methodology.md` — documentation clarity and the docs-match-behavior slice of concern 6.
- `code-review/CodeReview_Feedback_Guidelines_Methodology.md` — phrasing findings as actionable, severity-calibrated feedback.

Flagged by task type; load as a starting point, you are the final judge — fewer if inapplicable, more if the diff reveals it.

## Inherited Constraints

- **Read-only** (I5); do not rebuild; only the synthesis gate posts to GitHub.
- Severity discipline (I4): a doc *improvement wish* is minor/nit; a doc that is factually WRONG about behavior is a concrete defect (major/block as warranted).
- Config vars of record (from the machine gate): `CHIRP_BIND_ADDR` (`0.0.0.0:8080`), `CHIRP_STATIC_DIR` (`/srv/chirp`), `RUST_LOG`.
- PR #22 head `bc0c3c0d6380c9edd1b9433addc7fdcbffb55751`; repo `Nousix-LLC/nswe-demo`.

## Out-of-Scope Methodologies

- The probe's and SIGTERM's Rust idiom/correctness → owned by `SUBTASK_rustcode_sigterm`.
- Build reproducibility / image size → owned by `SUBTASK_dockerfile_build`.
- Security posture / supply chain → owned by `SUBTASK_security_supplychain`.
- `decomposition/` and `synthesis/` bundles are not for this analysis spoke.
