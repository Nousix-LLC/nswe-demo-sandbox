# Task: Review — SIGTERM repo-code change in main.rs & the std-only probe (PR #22)

## Task Specification

**Slug**: SUBTASK_rustcode_sigterm
**Task Kind**: standard
**Status**: Pending

### Objective

Render a Rust reviewer's judgment over the **repo-code change** in this PR — the SIGTERM handling
added to `crates/chirp-server/src/main.rs` and the std-only health probe
`deploy/docker/healthcheck.rs` — and emit `findings.md` per the contract.

### Context

Part of the review-containerize DAG (see `../_GLOBAL.md` and `../contracts/`). One of five parallel
analysis spokes; findings feed `SUBTASK_verdict_synthesis`.

**Dependencies**: none. **Dependents**: `SUBTASK_verdict_synthesis`.

### Concerns owned (cover each explicitly)

- **Concern 5 — SIGTERM handling correctness**: the signal handling is correct and **unix-gated**
  (`#[cfg(unix)]` or equivalent, so non-unix still compiles); it introduces no API / transport /
  behavior change beyond clean shutdown (graceful drain → exit 0 on `docker stop` / Kubernetes stop);
  it does not regress the server; and whether it **belongs in this item's scope** — the brief frames it
  as the minimal change required to run cleanly in a container, so judge whether it is genuinely
  minimal and justified rather than scope creep.
- **Concern 6 (Rust idiom slice)**: idiom, clarity, and maintainability of the SIGTERM change AND of
  the std-only probe `healthcheck.rs` (Rust quality — not the probe's docs, which `operability_docs`
  owns, nor its operational behavior, which `operability_docs` owns).

### Input Specification

| Input | Source | Purpose |
|---|---|---|
| Hub | `../_GLOBAL.md` | Shared context, PR coordinates, read-only constraint |
| Contract | `../contracts/_MANIFEST.yaml`, `../contracts/findings_schema.md` | Ownership + `findings.md` shape + severity rubric |
| Machine gate | `/home/user/nousix-runtime/nswe-demo/taskflow/dags/containerize/SYNTHESIS.md` | Authoritative facts: SIGTERM→exit 0; `cargo fmt`/`clippy -D warnings`/`test` 20-passed clean after the change |
| The diff | `gh pr diff 22 --repo Nousix-LLC/nswe-demo`; blobs via `gh api .../contents/<path>?ref=bc0c3c0d...` | `crates/chirp-server/src/main.rs` change and `deploy/docker/healthcheck.rs` under review (read-only) |

### Process (approach, not a runbook)

Read the `main.rs` SIGTERM diff and the probe source at head `bc0c3c0d`. Judge correctness of the
signal handling (does it actually await SIGTERM alongside SIGINT, drain, and exit 0; is it unix-gated;
does it avoid introducing races or changing the server's observable API/transport). Judge the probe's
Rust quality. Rely on the machine gate for the fact that fmt/clippy/tests are clean — your job is
code-judgment, not re-running the suite. Apply Rust concurrency/error-handling methodology. Record
findings with location + evidence + (block/major) remediation, honoring the severity discipline.
You decide depth and any further breakdown.

### Output Specification

| Attribute | Value |
|---|---|
| Filename | `findings.md` |
| Location | this workspace (`SUBTASK_rustcode_sigterm/`) |
| Shape | exactly `../contracts/findings_schema.md` |

### Success Criteria

- [ ] Concern 5 (correctness, unix-gating, no-regression, scope-fit) and the Rust-idiom slice of concern 6 each carry an explicit disposition.
- [ ] A concrete call on whether the SIGTERM change is correct and minimal (belongs in #12's scope).
- [ ] Every block/major has location + evidence + remediation; read-only honored; no suite re-run needed.

## Suggested Methodology Files

Domain Mapping row matched (verbatim): **"Rust code review | Rust | Code Review, Core"**. Load on demand via
`engine_load_methodology { name: "<bundle_id>" }`:

- `rust/Rust_Concurrency_Methodology.md` — correctness of async signal handling / graceful shutdown (the heart of concern 5).
- `rust/Rust_Async_Tokio_Methodology.md` — if the server uses Tokio, the idiomatic `signal`/`select!` shutdown pattern to check the change against.
- `rust/Rust_Error_Handling_Methodology.md` — error/exit-path idiom in the shutdown and the std-only probe.
- `code-review/CodeReview_Checklist_Methodology.md` + `core/BestPractices_Coding_Standards_Methodology.md` — systematic review and baseline idiom for concern 6.

Flagged by task type; load as a starting point, you are the final judge — fewer if inapplicable, more if the diff reveals it.

## Inherited Constraints

- **Read-only** (I5); do not rebuild or re-run the test suite to reconfirm the green gate; judge the code.
- Severity discipline (I4): a style preference is nit/minor; an actual correctness bug (e.g. a shutdown that can hang or drop in-flight work, or non-unix build breakage) is block/major.
- The change is asserted MINIMAL and unix-gated; verify that assertion against the diff rather than assuming it.
- PR #22 head `bc0c3c0d6380c9edd1b9433addc7fdcbffb55751`; repo `Nousix-LLC/nswe-demo`.

## Out-of-Scope Methodologies

- The probe's operational behavior and its docs → owned by `SUBTASK_operability_docs`.
- Dockerfile build/size and security posture → owned by the respective spokes.
- `decomposition/` and `synthesis/` bundles are not for this analysis spoke.
