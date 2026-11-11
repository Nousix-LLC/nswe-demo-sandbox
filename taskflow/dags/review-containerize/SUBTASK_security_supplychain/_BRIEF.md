# Task: Review — container security posture & supply-chain / dependency trust boundary (PR #22)

## Task Specification

**Slug**: SUBTASK_security_supplychain
**Task Kind**: standard
**Status**: Pending

### Objective

Render a security reviewer's judgment over PR #22's **container security posture** and its
**supply-chain / dependency trust boundary**, and emit `findings.md` per the contract.

### Context

Part of the review-containerize DAG (see `../_GLOBAL.md` and `../contracts/`). One of five parallel
analysis spokes; findings feed `SUBTASK_verdict_synthesis`.

**Dependencies**: none. **Dependents**: `SUBTASK_verdict_synthesis`.

### Concerns owned (cover each explicitly)

- **Concern 3 — container security posture**: non-root (`USER 65532`, non-zero uid, PID-1 as the
  server via exec-form `ENTRYPOINT`); no secrets baked into any layer or `ARG`/`COPY`; least-privilege
  friendliness (`--read-only` / `--cap-drop=ALL` / `no-new-privileges`); SPA bundle read-only.
- **Concern 3 — supply-chain / dependency trust boundary**: this diff pulls base images and installs a
  CLI from crates.io — assess the trust boundary: `@sha256` digest pinning of both base images,
  `--locked` cargo builds, and provenance of `wasm-bindgen-cli` (crates.io vs a prebuilt binary).
- **Concern 2 (secret/credential-leakage face ONLY)**: whether any secret/credential leaks into a
  runtime (or builder) layer. **The layer-composition + size face of concern 2 is OWNED BY
  `SUBTASK_dockerfile_build`** — adjudicate only leakage here; cross-reference by note if needed.

### Input Specification

| Input | Source | Purpose |
|---|---|---|
| Hub | `../_GLOBAL.md` | Shared context, PR coordinates, read-only constraint |
| Contract | `../contracts/_MANIFEST.yaml`, `../contracts/findings_schema.md` | Ownership + `findings.md` shape + severity rubric |
| Machine gate | `/home/user/nousix-runtime/nswe-demo/taskflow/dags/containerize/SYNTHESIS.md` | Authoritative build/run facts (e.g. live PID-1 uid, digests) — rely on it |
| The diff | `gh pr diff 22 --repo Nousix-LLC/nswe-demo`; blobs via `gh api .../contents/<path>?ref=bc0c3c0d...` | `Dockerfile`, `.dockerignore`, and any config under review (read-only) |

### Process (approach, not a runbook)

Read the `Dockerfile` and related files from the diff at head `bc0c3c0d`. Judge the runtime security
posture and the supply-chain trust boundary against secure-coding and dependency-security methodology;
verify the non-root/exec-form/digest-pinning/`--locked` claims against the actual file content and the
machine gate. Distinguish a concrete landable defect (e.g. a baked secret, a mutable SPA path, a
genuinely unpinned/untrusted dependency) from a hardening wish (e.g. "could also add seccomp") —
per the severity discipline the latter is minor/nit, not block/major. Record each finding with
location + evidence + (block/major) remediation. You decide depth and any further breakdown.

### Output Specification

| Attribute | Value |
|---|---|
| Filename | `findings.md` |
| Location | this workspace (`SUBTASK_security_supplychain/`) |
| Shape | exactly `../contracts/findings_schema.md` |

### Success Criteria

- [ ] Concern 3 (posture) and concern 3 (supply-chain) and the concern-2 leakage face each carry an explicit disposition.
- [ ] Non-root / exec-form / digest-pinning / `--locked` / provenance claims checked against the actual diff.
- [ ] Hardening wishes correctly ranked minor/nit, not block/major (I4).
- [ ] Every block/major has a concrete location + remediation; read-only honored.

## Suggested Methodology Files

Domain Mapping rows matched (verbatim): **"Container deployment / production ops | Containerization | Operations, Security"**
and **"Security review | Security | Code Review"**. Load on demand via `engine_load_methodology { name: "<bundle_id>" }`:

- `security/Security_Secure_Coding_Methodology.md` — least-privilege, non-root, attack-surface reasoning for the posture concern.
- `security/Security_Dependency_Security_Methodology.md` — the supply-chain / dependency trust boundary (digest pinning, `--locked`, provenance).
- `security/BestPractices_Configuration_Management_Methodology.md` — secret handling / no-credentials-in-layers.
- `containerization/Containerization_Runtime_Methodology.md` — distroless runtime hardening posture (the container-specific angle).
- `code-review/CodeReview_Checklist_Methodology.md` — systematic, severity-calibrated review.

Flagged by task type; load as a starting point, you are the final judge — fewer if inapplicable, more if the diff reveals it.

## Inherited Constraints

- **Read-only** (I5); do not rebuild; only the synthesis gate posts to GitHub.
- Severity discipline (I4): a security *wish* is not a block/major.
- PR #22 head `bc0c3c0d6380c9edd1b9433addc7fdcbffb55751`; repo `Nousix-LLC/nswe-demo`; distroless runtime is `gcr.io/distroless/cc-debian12:nonroot`, builder `rust:1.88-slim-bookworm`.

## Out-of-Scope Methodologies

- Image layer-composition/size and build reproducibility mechanics → owned by `SUBTASK_dockerfile_build`.
- SIGTERM/Rust-code correctness → owned by `SUBTASK_rustcode_sigterm`.
- `decomposition/` and `synthesis/` bundles are not for this analysis spoke.
