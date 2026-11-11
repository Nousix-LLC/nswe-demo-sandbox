# SYNTHESIS — SUBTASK_axum_mismatch Fold Record

## Gate Outcome: PASS

## Checks Run

### Check 1 — All criteria present: PASS

Verified that every criterion listed in `../_GLOBAL.md` §Success Criteria has a named verdict in the spoke outputs:

- **REQ-SSR-006**: present in `SUBTASK_mismatch_detect/mismatch_detect_findings.md` (under the label REQ-SSR-009, which the spoke identified as the same criterion and explicitly flagged — see labeling note below)
- **REQ-MIS-001**: present in `SUBTASK_axum_server/axum_server_findings.md`
- **REQ-MIS-002**: present in `SUBTASK_axum_server/axum_server_findings.md`
- **REQ-SSR-007 non-goal confirmation**: present in `SUBTASK_axum_server/axum_server_findings.md`

No criterion is silently omitted.

**Labeling discrepancy (non-blocker, surfaced in findings)**: The brief labels the mismatch-detection criterion REQ-SSR-006; issue #226 and `crates/ferric/src/hydrate.rs:11` use REQ-SSR-009. The spoke correctly adopted the code/issue label (REQ-SSR-009) as authoritative and explicitly flagged the divergence. The review content is complete and correct; the label inconsistency in the review infrastructure is recorded in `axum_mismatch_findings.md` under REQ-SSR-006 §"Label discrepancy."

### Check 2 — Marker format cross-check: PASS

**Client-side format** (from `SUBTASK_mismatch_detect/mismatch_detect_findings.md`):
Text-boundary HTML Comment sentinels. `TEXT_OPEN_MARKER = "<!--$t-->"` (DOM `comment.data()` = `"$t"`); `TEXT_CLOSE_MARKER = "<!--/$t-->"` (DOM `comment.data()` = `"/$t"`). No element-level attributes. Constants defined in `crates/ferric/src/ssr.rs:28–43`, imported by `crates/ferric/src/hydrate.rs:35`.

**Server-side format** (from `SUBTASK_axum_server/axum_server_findings.md`):
Text-boundary HTML Comment sentinels. `TEXT_OPEN_MARKER = "<!--$t-->"` (HTML Comment node, `comment.data()` = `"$t"`); `TEXT_CLOSE_MARKER = "<!--/$t-->"` (HTML Comment node, `comment.data()` = `"/$t"`). No element-level markers. Constants defined once in `crates/ferric/src/ssr.rs:33, 50`, imported by `crates/ferric/src/hydrate.rs:35`.

**Result**: MATCHES. Agreement is by construction: the client imports the same constants from `crate::ssr` that the server uses to serialize (`use crate::ssr::{TEXT_CLOSE_MARKER, TEXT_OPEN_MARKER}` at `hydrate.rs:35`). There are no inline copies and no separate server-side vs client-side schemas. The client cannot diverge from the server's format without changing the same constants that both sides read.

### Check 3 — Evidence standard: PASS

Verified both spoke outputs for host filesystem paths, taskflow paths, and test assertions used as proxies for behavior.

- `mismatch_detect_findings.md`: All evidence citations are `crates/ferric/src/...` paths at named line ranges within `Nousix-LLC/nswe-demo`. No host paths, no taskflow paths. The BLOCKER finding (absence of `wasm-bindgen-test`) cites the absence with file name and line count (`hydrate.rs`, 466 lines, no `#[cfg(test)]` block), not a test assertion as a proxy.
- `axum_server_findings.md`: All evidence citations are `crates/chirp-server/src/...` and `crates/ferric/src/...` paths at named lines within `Nousix-LLC/nswe-demo`. No host paths, no taskflow paths.

Evidence standard satisfied across both spokes.

### Check 4 — Non-goal boundary: PASS

`SUBTASK_axum_server/axum_server_findings.md` contains a dedicated "Non-goal Boundary" section for REQ-SSR-007 / #225 with Status: CONFIRMED NON-GOAL, specific code examined, and evidence at named lines (`crates/chirp-server/src/ssr.rs:138–143`, `:114`, `:160–163`). The confirmation is explicit and grounded in the code. REQ-SSR-007 is not evaluated as deficient anywhere in the spoke output.

## Outputs Produced
- `axum_mismatch_findings.md` — combined findings for SUBTASK_correctness_synthesis
