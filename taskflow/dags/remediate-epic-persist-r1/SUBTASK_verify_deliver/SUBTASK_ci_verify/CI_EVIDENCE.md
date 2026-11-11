# CI Evidence — PR #113 (`Nousix-LLC/nswe-demo`)

**Repository**: `Nousix-LLC/nswe-demo`
**PR**: #113 — "Durable PostgreSQL persistence for chirp: provision, wire, and prove durability"
**Branch**: `work/epic-persist`
**Observation timestamp**: 2026-10-29

---

## Summary Table — Required Checks

| Check  | Observed Status | Notes |
|--------|-----------------|-------|
| `doc`  | **FAILED**      | Intra-doc link error (see detail below) |
| `clippy` | PASSED        | — |
| `fmt`  | PASSED          | — |
| `test` | PASSED          | — |
| `wasm` | PASSED          | — |

---

## Observed CI Run

**Run**: `38616250978`
**Run URL**: https://github.com/Nousix-LLC/nswe-demo/actions/runs/38616250978
**Triggered**: 2026-10-14T18:34:05Z (via `pull_request` event)
**Head commit of PR at observation**: `09fa453c3c40e39a9b4647e0de6e00dcf50ecb21`
**CI merge-ref commit**: `3888f22ec207e38af49510222baaacc7bff97faf`
**Run outcome**: FAILURE (exit code 101 on `doc` job)

This is the **only** CI run recorded for `work/epic-persist`. No subsequent run exists as of the observation timestamp.

---

## `doc` Check — FAILED

**Job ID**: 116031969925
**Job URL**: https://github.com/Nousix-LLC/nswe-demo/actions/runs/38616250978/job/116031969925
**Environment**: `RUSTDOCFLAGS=-D warnings`, `cargo doc --workspace --no-deps --locked`

**Failure**:
```
error: public documentation for `export_user_data` links to private item `super::export::ExportDocument`
   --> crates/chirp-server/src/repository/in_memory.rs:787:58
    |
787 |     /// serialized through the shared [`ExportDocument`](super::export::ExportDocument) so the two
    |                                                          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ this item is private
    |
    = note: this link will resolve properly if you pass `--document-private-items`
    = note: `-D rustdoc::private-intra-doc-links` implied by `-D warnings`
    = help: to override `-D warnings` add `#[allow(rustdoc::private_intra_doc_links)]`

error: could not document `chirp-server`
```

**Affected crate**: `chirp-server`
**Affected file**: `crates/chirp-server/src/repository/in_memory.rs`, line 787

---

## Commit `e63e607` — Not Found

The brief specified commit `e63e607` as the verifying commit containing doc corrections (addressing CI-01 public→private intra-doc link). **That SHA does not exist in the repository** (`git`/GitHub API returns HTTP 422: "No commit found for SHA: e63e607"). The doc fix has not been pushed to `work/epic-persist`.

The public→private intra-doc link error in `in_memory.rs:787` (CI-01) is **still present** on the current head `09fa453c3c40e39a9b4647e0de6e00dcf50ecb21`, as evidenced by the CI failure.

---

## Other Required Checks — All PASSED on Run 38616250978

| Check   | Job ID          | Duration | Result  |
|---------|-----------------|----------|---------|
| `clippy` | 116031969600  | 45 s     | PASSED  |
| `fmt`   | 116031969720    | 13 s     | PASSED  |
| `test`  | 116031969402    | 31 s     | PASSED  |
| `wasm`  | 116031970091    | 29 s     | PASSED  |

(`image` job was SKIPPED — not a required check.)

---

## Durability Assessment

- **`doc` check**: FAILED — the intra-doc link fix commit `e63e607` was never pushed; CI-01 remains unresolved.
- **`clippy`, `fmt`, `test`, `wasm`**: No durability regression — all four passed on the only existing run.
- **Net result**: PR #113 does not have a green `doc` check. The branch needs the doc correction commit pushed and CI re-triggered to confirm end-to-end resolution.
