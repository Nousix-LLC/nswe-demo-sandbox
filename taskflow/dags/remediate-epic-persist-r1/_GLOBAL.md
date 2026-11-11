# _GLOBAL.md — Remediate PR #113 doc blocker (round 1)

## Project Context

**Status**: Active

### Objective

Make `Nousix-LLC/nswe-demo` PR #113 ("Durable PostgreSQL persistence for chirp", `work/epic-persist` → `main`,
epic #56 / issues #65, #66, #67) landable by turning the red **required `doc` CI check** green under
`RUSTDOCFLAGS: -D warnings`, and by clearing the connected doc-link / feature-gating hazards grouped in issue
**#118** — **without re-architecting the durable store** (the implementation was found sound on review). The only
source changes permitted are to doc comments, intra-doc links, and doc feature-gate attributes.

### Scope

**In scope:**
- The landing blocker **CI-01**: the public→private intra-doc link on `export_user_data` at
  `crates/chirp-server/src/repository/in_memory.rs` (~line 787) linking `` [`ExportDocument`](super::export::ExportDocument) ``
  into the `pub(crate)` item in the private `export` module, which `rustdoc::private_intra_doc_links` turns into a
  hard error under `-D warnings`.
- The **#118** connected hazards: the ungated→gated doc reference at
  `crates/chirp-server/src/repository/export.rs` (~line 7) into the `postgres`-feature-gated module; and the stale
  "scaffold stub"/"placeholder" rustdoc plus internal build-breakdown vocabulary in the persistence layer's public
  doc comments.
- Verification that `cargo doc --workspace --no-deps --locked` is green under `-D warnings` on a **fresh** run
  (rustdoc reports only the first failing crate, so the fix must be re-verified end-to-end), and that the
  previously-green checks (`clippy`, `fmt`, `test`, `wasm`) stay green.
- Delivery: commit to `work/epic-persist` to update PR #113 in place; author the PR-reader-facing narrative.

**Out of scope:**
- Any change to the durable store's logic, schema, migrations, `ChirpRepository` seam, fail-closed behavior,
  retention/transient lifetimes, or wiring. Touch source **only** where a doc comment / intra-doc link / doc
  feature-gate attribute must change.
- Merging the PR, pushing to `main`, force-pushing, or rewriting merged history. The DAG never merges its own PR.
- Opening a second PR — unless the branch state makes updating #113 impossible, in which case exactly one PR into
  `main` closing #65, #66, #67 (one `Closes #N` per issue, plain text).

### Success Criteria

- [ ] CI-01 resolved: the `in_memory.rs` public→private link is dropped or reworked; rustdoc no longer errors on it.
- [ ] #118 resolved: `export.rs` reference is gating-correct; persistence-layer public docs are accurate (no
      implemented-as-stub/placeholder descriptions, no internal build vocabulary); all public→private /
      ungated→gated intra-doc links in the changed crate resolve.
- [ ] `cargo doc --workspace --no-deps --locked` is green under `-D warnings` on a fresh run.
- [ ] No durability regression: `clippy`, `fmt`, `test`, `wasm` remain green; the only behavioral change is to docs.
- [ ] PR #113 updated in place on `work/epic-persist`, mergeable and clean; reader-facing description present.
- [ ] Root `SYNTHESIS.md` verdict accounts for CI-01 (fixed, with verification) and each #118 item (fixed, or not
      and why), and confirms no durability regression.

---

## Constraints and Requirements

- **Documentation and doc-feature-gating only.** Do not modify store logic, schema, migrations, or wiring.
- **Branch `work/epic-persist`.** Never force-push `main`; never rewrite merged history. The DAG never merges.
- **No attribution trailers** on commits.
- **Output hygiene (hard).** Nothing posted to GitHub (commits, PR body, comments) carries host/absolute paths,
  cluster/SSH/credential details, or taskflow/agent/run identifiers. Name everything by repository identity:
  `owner/repo`, issue/PR numbers, commit SHAs, repo-relative paths.

---

## Input Specifications

| Source | Identity | Purpose |
|--------|----------|---------|
| Branch under remediation | `Nousix-LLC/nswe-demo` `work/epic-persist`, PR #113, head `09fa453c3c40e39a9b4647e0de6e00dcf50ecb21` | The prior diff being corrected |
| Review verdict | The posted REQUEST-CHANGES review on PR #113 and its CI-01 finding | Names the blocker and the two further `doc` hazards |
| Issue #118 | "stale scaffold documentation & feature-gating hygiene" | Groups the connected hazards + their acceptance criteria |
| Durability bars | Acceptance criteria of #65/#66/#67; the persistence design epic #56 traces to | The non-regression bar |

---

## Methodology

Methodology selection belongs to each child at its own dispatch; no bundle is named here. The work is a surgical,
documentation-only remediation of a Rust workspace crate (`chirp-server`), verified by `cargo doc` under
`-D warnings` and the existing CI check suite.

---

## Task Structure

### Overview

```
_GLOBAL.md (this hub)
├── contracts/
│   ├── _MANIFEST.yaml              (kind, ownership, identities)
│   └── inventory.schema.yaml       (the correction-record schema assess→apply share)
├── SUBTASK_assess/_BRIEF.md        (diagnose: enumerate every hazard → INVENTORY.md)
├── SUBTASK_apply_fixes/_BRIEF.md   (remediate: edit docs per inventory + commit)
├── SUBTASK_verify_deliver/_BRIEF.md(verify green + no regression; push to update PR #113)
└── SUBTASK_synthesis/_BRIEF.md     (fold: root SYNTHESIS.md verdict)
```

### Task Summary

| Task id | Depends on | Description | Output |
|---------|------------|-------------|--------|
| `SUBTASK_assess` | none | Survey `work/epic-persist` at the pinned head; enumerate every doc-link hazard (public→private, ungated→gated) and every stale/inaccurate persistence-layer doc comment + internal build vocabulary in the `chirp-server` crate; produce the precise correction inventory (file, anchor, hazard kind, current text, exact rework, acceptance criterion served) | `SUBTASK_assess/INVENTORY.md` |
| `SUBTASK_apply_fixes` | `SUBTASK_assess` | Apply the inventory's corrections to the doc comments / intra-doc links / doc feature-gate attributes in the changed crate, touching source only where a doc comment/link/gate must change, and commit to `work/epic-persist` | `SUBTASK_apply_fixes/CHANGESET.md` (+ committed source edits) |
| `SUBTASK_verify_deliver` | `SUBTASK_apply_fixes` | Confirm `cargo doc --workspace --no-deps --locked` is green under `-D warnings` on a fresh run and that `clippy`/`fmt`/`test`/`wasm` stay green (no durability regression); push to update PR #113 in place; author the reader-facing PR description/commit narrative | `SUBTASK_verify_deliver/VERIFICATION.md` (+ updated PR #113) |
| `SUBTASK_synthesis` | `SUBTASK_assess`, `SUBTASK_apply_fixes`, `SUBTASK_verify_deliver` | Verify the parts composed and fold the verdict: account for CI-01 (fixed, with verification) and each #118 item (fixed, or not and why), confirm no durability regression | `SYNTHESIS.md` (at this root — the fold location) |

### Dependency Graph

```
SUBTASK_assess ── SUBTASK_apply_fixes ── SUBTASK_verify_deliver ──┐
     └────────────────────┴───────────────────────┴── SUBTASK_synthesis
```

---

## Contract

**Contract location**: `contracts/` (read-only for every descendant)
**Contract kind**: `yaml_schema`

### Inherited Contracts

None — this is the root decomposition.

### Structural Declarations

| Artifact | Kind | Declares |
|---|---|---|
| `contracts/inventory.schema.yaml` | `yaml_schema` | The schema of each correction record in `INVENTORY.md`: `id`, `file` (repo-relative), `anchor` (symbol / approx line), `hazard_kind` ∈ {`public_to_private_link`, `ungated_to_gated_link`, `stale_scaffold_doc`, `internal_vocab`}, `current`, `rework`, `criterion` ∈ {`CI-01`, `#118`}. This is the seam `assess` produces and `apply_fixes` consumes. |

### Ownership

| Artifact | Owning subtask |
|---|---|
| `SUBTASK_assess/INVENTORY.md` | `SUBTASK_assess` |
| Source doc-comment/link/gate edits on `work/epic-persist` + `SUBTASK_apply_fixes/CHANGESET.md` | `SUBTASK_apply_fixes` |
| `SUBTASK_verify_deliver/VERIFICATION.md` + the push updating PR #113 + the PR description | `SUBTASK_verify_deliver` |
| `SYNTHESIS.md` (root) | `SUBTASK_synthesis` |

### Identities

Invariants the synthesis task evaluates as assertions (no silent plugs):

- [ ] **Coverage.** Every hazard enumerated in `INVENTORY.md` (every CI-01 and #118 finding) has exactly one
      corresponding applied fix recorded in `CHANGESET.md`.
- [ ] **Scope.** The only source changes are to doc comments, intra-doc links, and doc feature-gate
      (`#[cfg(...)]` / `#[cfg_attr(..., doc = ...)]` / `#[doc(cfg(...))]`) attributes — no change to store logic,
      schema, migrations, the `ChirpRepository` seam, or wiring.
- [ ] **Blocker cleared.** `cargo doc --workspace --no-deps --locked` under `-D warnings` is green on a **fresh**
      run (re-verified after the fix, not inferred from clearing the first error), recorded in `VERIFICATION.md`.
- [ ] **No regression.** `clippy`, `fmt`, `test`, `wasm` remain green, recorded in `VERIFICATION.md`.
- [ ] **Output hygiene.** Nothing committed or posted to GitHub carries host/cluster/SSH/credential/taskflow
      details; everything is named by repository identity.

### Derived Artifacts

None auto-generated; `INVENTORY.md` is the hand-authored seam delivered (by dependency) into `apply_fixes`.

### Thin-Seam Note

The seam here is genuinely thin: a one-file correction inventory plus the ownership and identities above. That is a
complete contract for a surgical, single-crate documentation remediation.

---

## Output Specifications

| Deliverable | Location | Description |
|-------------|----------|-------------|
| Correction inventory | `SUBTASK_assess/INVENTORY.md` | Precise, per-hazard corrections (contract schema) |
| Changeset record | `SUBTASK_apply_fixes/CHANGESET.md` | What was edited and the commit SHA(s) on `work/epic-persist` |
| Verification record | `SUBTASK_verify_deliver/VERIFICATION.md` | Evidence `doc` is green under `-D warnings` + other checks green |
| Updated PR #113 | `Nousix-LLC/nswe-demo` PR #113 | Commits on `work/epic-persist`; reader-facing description |
| Root verdict | `SYNTHESIS.md` | The folded remediation verdict (the overseer's observation seam) |
