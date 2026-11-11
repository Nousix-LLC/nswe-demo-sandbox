# SYNTHESIS.md — PR #113 doc-blocker remediation (round 1)

**Repository**: `Nousix-LLC/nswe-demo`
**PR**: #113 — "Durable PostgreSQL persistence for chirp"
**Branch**: `work/epic-persist`
**Synthesized**: 2026-10-29

---

## Overall Verdict: FAIL

The remediation diagnosed and applied all named corrections to the `chirp-server` doc comments,
intra-doc links, and internal vocabulary. The correction coverage is complete and the scope is clean.
However, the critical contract identity `blocker_cleared` — confirmed-green `cargo doc` under
`RUSTDOCFLAGS=-D warnings` on a fresh run after the fix — is **not satisfied** by the evidence in
`SUBTASK_verify_deliver/VERIFICATION.md`. No CI run recording a green `doc` result on the corrected
commit is present in `CI_EVIDENCE.md`.

---

## CI-01 — public→private intra-doc link (`in_memory.rs`)

**Criterion**: CI-01 resolved; `export_user_data` public→private link dropped.

**Disposition**:
- `SUBTASK_assess/INVENTORY.md` record CI-01 correctly identifies the link
  `` [`ExportDocument`](super::export::ExportDocument) `` in `fn export_user_data` at
  `crates/chirp-server/src/repository/in_memory.rs` (~L787) as the `public_to_private_link` hazard.
- `SUBTASK_apply_fixes/CHANGESET.md` confirms the fix was applied in commit `e63e607`: the
  intra-doc link was replaced with the plain code span `` `ExportDocument` ``.
- `SUBTASK_verify_deliver/VERIFICATION.md` records that commit `e63e607` was not found in the
  repository (GitHub API returned HTTP 422). The only observed CI run (`38616250978`) was against
  the prior head `09fa453c3c40e39a9b4647e0de6e00dcf50ecb21`, on which the `doc` check **FAILED**
  with the CI-01 error. A push of commit `db1a5d6` is noted in `PR_UPDATE.md`, and the PR
  description claims all five checks are green — but this is not corroborated by `CI_EVIDENCE.md`.

**CI-01**: fix applied in changeset; green `doc` run on the corrected commit **unconfirmed**.

---

## #118 Items

### H-02 — ungated→gated intra-doc link (`export.rs`)

INVENTORY.md H-02 identifies `` [`PostgresRepository`](crate::repository::postgres::PostgresRepository) ``
in the `export.rs` module doc (~L7) as an `ungated_to_gated_link` that fires once CI-01 is cleared.
CHANGESET.md confirms the fix: replaced with the plain code span `` `PostgresRepository` ``.
Same CI caveat as CI-01 — fix applied; green `doc` run unconfirmed by `CI_EVIDENCE.md`.

### H-03 through H-14 — stale scaffold docs and internal vocabulary

All nine remaining inventory items were applied per CHANGESET.md:

| id | file (repo-relative) | fix summary |
|----|----------------------|-------------|
| H-03 | `crates/chirp-server/src/repository/postgres.rs` | Scaffold label removed from module title |
| H-04 | `crates/chirp-server/src/repository/postgres.rs` | "# Scaffold boundary" section replaced with "# Implementation" |
| H-05 | `crates/chirp-server/src/repository/postgres.rs` | "Unlike the other scaffold methods this is not a stub" prefix removed from `store_health` |
| H-06 | `crates/chirp-server/src/repository/in_memory.rs` | "not a placeholder that masks unimplemented behaviour" clause removed from `store_health` |
| H-07 | `crates/chirp-server/src/repository/in_memory.rs` | Hypothetical SQLite sentence updated to describe `PostgresRepository` under `postgres` feature |
| H-08 | `crates/chirp-server/src/repository/mod.rs` | Hypothetical SQLite sentence replaced with factual two-backing description |
| H-09 / H-14 | `crates/chirp-server/src/repository/mod.rs` | "Release-bar additions" paragraph replaced (single combined edit per INVENTORY.md note); `EPIC-PERSIST` label removed |
| H-10 | `crates/chirp-server/src/lib.rs` | Layering diagram updated to show both `InMemoryRepository` and `PostgresRepository`; prose updated |
| H-11 | `crates/chirp-server/src/error.rs` | "# Ownership of the error seam" corrected; false "HTTP-free" / no-`IntoResponse` claim removed |
| H-12 | `crates/chirp-server/src/repository/postgres.rs` | Internal build-stage vocabulary removed from `DEFAULT_MAX_CONNECTIONS` doc |
| H-13 | `crates/chirp-server/src/repository/postgres.rs` | `SUBTASK_mapping_validation` and `SUBTASK_durable_impl` identifiers removed from `pub mod mapping` doc |

**H-03 through H-14**: all fixes applied per changeset. These items are #118 accuracy hazards (none
break `cargo doc` directly). Their fix state is verifiable in the committed diff on `work/epic-persist`.

---

## Contract Identity Assertions

### coverage
**Assertion**: Every hazard enumerated in INVENTORY.md has exactly one corresponding applied fix in CHANGESET.md.

**Evidence**: INVENTORY.md enumerates 14 records (CI-01, H-02 through H-14). H-09 and H-14 are
explicitly noted as a single combined edit at the same location. CHANGESET.md lists 13 entries
(CI-01, H-02 through H-13, with H-09/H-14 as one combined edit). Every inventory record is
accounted for exactly once; none is missing, none is duplicated.

**Result**: **PASS**

---

### scope_docs_only
**Assertion**: The only source changes are to doc comments, intra-doc links, and doc feature-gate
attributes. No change to store logic, schema, migrations, `ChirpRepository` seam, or wiring.

**Evidence**: CHANGESET.md scope assertion: "The diff is strictly documentation: doc comment text,
intra-doc links, and module doc (`//!`) blocks. No logic, schema, migration, `ChirpRepository`
seam, or wiring was touched."

**Result**: **PASS**

---

### blocker_cleared
**Assertion**: `cargo doc --workspace --no-deps --locked` under `RUSTDOCFLAGS=-D warnings` is green
on a FRESH run (re-verified after the fix, not inferred from clearing the first error).

**Evidence**: VERIFICATION.md records that commit `e63e607` (the correction commit per CHANGESET.md)
was not found in the repository (HTTP 422 from the GitHub API). `CI_EVIDENCE.md` records only CI run
`38616250978` against the prior head `09fa453c3c40e39a9b4647e0de6e00dcf50ecb21`, on which the `doc`
job (`116031969925`) **FAILED** with code 101. `PR_UPDATE.md` notes a push of commit `db1a5d6` and
states the PR description claims all five checks are green, but `CI_EVIDENCE.md` does not record a
CI run on `db1a5d6` or any later commit.

There is a commit SHA discrepancy: CHANGESET.md names `e63e607`; PR_UPDATE.md names `db1a5d6`;
neither appears in `CI_EVIDENCE.md` with a green `doc` result. This requires investigation before
submitting a re-review request.

**Result**: **FAIL** — No fresh green `doc` run recorded in the evidential seam (`CI_EVIDENCE.md`).

---

### no_regression
**Assertion**: `clippy`, `fmt`, `test`, `wasm` remain green.

**Evidence**: VERIFICATION.md records all four checks PASSED on CI run `38616250978`:
- `clippy` (job `116031969600`): PASSED (45 s)
- `fmt` (job `116031969720`): PASSED (13 s)
- `test` (job `116031969402`): PASSED (31 s)
- `wasm` (job `116031970091`): PASSED (29 s)

These results are on the prior head. CHANGESET.md confirms the changeset is documentation-only (doc
comment text, `//!` blocks, intra-doc links). No behavioral code was modified; regression on these
checks from a docs-only diff is not expected. Direct CI evidence for the corrected commit is absent
from `CI_EVIDENCE.md`.

**Result**: **PASS (qualified)** — All four checks passed on the prior head; documentation-only
diff makes regression extremely unlikely, but a CI run on the corrected commit is not recorded.

---

### output_hygiene
**Assertion**: Nothing committed or posted to GitHub carries host/cluster/SSH/credential/taskflow details.

**Evidence**: VERIFICATION.md confirms `PR_UPDATE.md` and the posted PR description are clean — no
host, cluster, SSH, credential, or taskflow identifiers; all references use repository identity
(`Nousix-LLC/nswe-demo`, issue/PR numbers, commit SHAs, repo-relative paths).

**Result**: **PASS**

---

## No Durability Regression

No durability regression is evidenced. The changeset is strictly documentation; logic, schema,
migrations, the `ChirpRepository` seam, and wiring are untouched per CHANGESET.md. `clippy`, `fmt`,
`test`, `wasm` all passed on the prior head (CI run `38616250978`).

---

## PR #113 State

PR #113 (`Nousix-LLC/nswe-demo`, `work/epic-persist` → `main`) was updated in place by
SUBTASK_verify_deliver. State at last observation: **OPEN, MERGEABLE**. The reader-facing PR
description closes #65, #66, and #67 and narrates the durable store delivery and doc corrections.
The description claims all five required checks are green on the branch head; this claim has not
been independently corroborated by `CI_EVIDENCE.md`.

---

## Failure Summary and Recommended Path Forward

**The sole failing identity is `blocker_cleared`.** The root cause is a gap in the verification
chain: the correction commit (either `e63e607` as named in CHANGESET.md or `db1a5d6` as noted in
PR_UPDATE.md) was not confirmed against a fresh CI run before `CI_EVIDENCE.md` was finalized.

Before a re-review request (round 2), the following should be established:

1. **Confirm the current branch head SHA** on `work/epic-persist` and reconcile the discrepancy
   between `e63e607` (CHANGESET.md) and `db1a5d6` (PR_UPDATE.md).
2. **Obtain a fresh CI run** on the confirmed branch head and record the `doc` job result.
3. **If the `doc` check is green** on that run, update the verification record and submit a round-2
   SYNTHESIS with `blocker_cleared: PASS`.
4. **If the `doc` check is still red**, diagnose the remaining error (likely H-02 or an undetected
   hazard) and return to apply-fixes for a further correction.

All other identities (`coverage`, `scope_docs_only`, `no_regression`, `output_hygiene`) are
satisfied. The correction work product is complete and correctly scoped; only the fresh-CI
confirmation step remains.
