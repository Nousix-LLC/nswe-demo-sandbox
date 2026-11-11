# SYNTHESIS — ferric-ssr-r1 SSR + Hydration

**Synthesis date**: 2026-11-04  
**Synthesized by**: ferric-ssr-r1-synthesis (this task)  
**Branch assembled**: `work/ferric-ssr-r1`

---

## Summary

The synthesis gate merged two of the three planned spoke branches and ran all seven identity
assertions. Two assertions **failed** because the client-hydrate spoke (`ferric-ssr-r1-client-hydrate`)
never ran: `work/ferric-ssr-r1-client` does not exist. As directed by the brief, the GitHub PR
was **not created** pending resolution of the failures.

---

## Spoke Assembly Status

| Spoke | Branch | Status | Merged |
|---|---|---|---|
| `ferric-ssr-r1-server-render` | `work/ferric-ssr-r1-server` | COMPLETE | ✅ commit `3e6a362` |
| `ferric-ssr-r1-client-hydrate` | `work/ferric-ssr-r1-client` | **NEVER RAN** | ❌ branch does not exist |
| `ferric-ssr-r1-axum-integration` | `work/ferric-ssr-r1-axum` | COMPLETE | ✅ commit `4f870d1` |

The two available spoke branches were merged cleanly — disjoint file ownership held, no
conflicts. The client-hydrate branch was never created; `crates/ferric/src/hydrate.rs`
remains the skeleton stub (`todo!()`) authored by the skeleton task.

---

## Identity Assertions

| Assertion | Command / Criterion | Result | Evidence |
|---|---|---|---|
| `native-compile` | `cargo check --lib -p ferric` | ✅ **PASS** | Exit 0; 0 errors |
| `wasm-compile` | `cargo check --target wasm32-unknown-unknown -p ferric` | ✅ **PASS** | Exit 0; 2 warnings (stub unused vars) |
| `native-tests-pass` | `cargo test -p ferric` | ✅ **PASS** | 56 unit tests + 7 doc tests; 0 failed |
| `chirp-server-compile` | `cargo build -p chirp-server` | ✅ **PASS** | Exit 0 |
| `frozen-prelude-unchanged` | git diff on 4 frozen files | ✅ **PASS** | Empty diff; no frozen file modified |
| `marker-format-agreement` | grep `<!--$t-->` in ssr.rs AND hydrate.rs | ❌ **FAIL** | `<!--$t-->` present in `ssr.rs` (line 28); absent from `hydrate.rs` (stub contains only doc comment reference) |
| `issues-closed` | PR body must include closes syntax + BAR-005 sentence | ❌ **NOT APPLICABLE** | PR not created due to assertion failures above |

### marker-format-agreement Detail

The literal `<!--$t-->` appears in `crates/ferric/src/ssr.rs` as the constant definition:
```
pub const TEXT_OPEN_MARKER: &str = "<!--$t-->";
```

It does NOT appear in `crates/ferric/src/hydrate.rs`. The skeleton stub references the
constant by NAME in a doc comment (`crate::ssr::TEXT_OPEN_MARKER`) but contains no actual
code that parses or matches the marker string. The hydration implementation — which would
import and use `TEXT_OPEN_MARKER` during the DOM walk — was never written.

---

## Issue Requirements Assessment

### #223 (BAR-003): Server-side HTML rendering and per-request scope isolation

**STATUS: MET**

Evidence:
- `render_to_string` fully implemented in `crates/ferric/src/ssr.rs` (commit `215dc9d`)
- `TEXT_OPEN_MARKER` / `TEXT_CLOSE_MARKER` wrap every `VNode::Text`
- HTML escaping covers all five injection characters (`< > & " '`)
- Per-request `ReactiveScope` created and disposed each call (isolation verified by test)
- 14 SSR unit tests all passing
- `cargo check --lib -p ferric` exits zero; no `web_sys` or `wasm_bindgen` imported on native target
- Requirements addressed: REQ-SSR-001, REQ-SSR-002, REQ-SSR-003, REQ-SSR-010, REQ-SSR-012

### #224 (BAR-004): Client hydration without re-render

**STATUS: NOT MET**

The `ferric-ssr-r1-client-hydrate` spoke task never ran. No `work/ferric-ssr-r1-client`
branch was created. `crates/ferric/src/hydrate.rs` remains the skeleton stub:
```rust
pub fn hydrate<F>(root: web_sys::Element, f: F)
where F: FnOnce() -> VNode + 'static
{
    todo!("hydrate: implement in ferric-ssr-r1-client-hydrate spoke")
}
```

Unmet requirements: REQ-SSR-004 (zero structural mutations adopt pass), REQ-SSR-005 (event
handler wiring), REQ-SSR-009 (mismatch detection and recovery). These are the core BAR-004
acceptance criteria.

**Blocking gap**: `work/ferric-ssr-r1-client` branch must be created and the client-hydrate
spoke task must run before the synthesis PR can be opened.

### #226 (BAR-006): Hydration mismatch detection and Axum server integration

**STATUS: PARTIALLY MET**

The issue covers two sub-concerns:

1. **Axum server integration** (REQ-SSR-011): **MET**
   - `crates/chirp-server/src/ssr.rs` implemented: `assemble_document` + `ssr_handler`
   - `ferric = { path = "../ferric" }` added to `crates/chirp-server/Cargo.toml`
   - `cargo build -p chirp-server` exits zero
   - Note: PR #227 (open, not merged) addresses this sub-concern independently

2. **Mismatch detection and recovery** (from BAR-004 scope): **NOT MET**
   - Mismatch detection is part of the hydration implementation (#224 / BAR-004)
   - Not present in the stub `hydrate.rs`
   - Requires the client-hydrate spoke to run first

---

## Branch State After Synthesis

```
work/ferric-ssr-r1 (pushed to origin at 4f870d1)
├── 156d9e9  feat(ferric): add ssr + hydrate module skeleton (ferric-ssr-r1)
├── 36b6ea9  feat(chirp-server): wire ferric::render_to_string into Axum handler
├── 215dc9d  feat(ferric/ssr): implement render_to_string (BAR-003, Issue #223)
├── d8d56dc  fix(ferric/ssr): resolve type inference ambiguity in test .into() calls
├── 3e6a362  chore(ferric-ssr-r1): merge server-render spoke (BAR-003, #223)
└── 4f870d1  chore(ferric-ssr-r1): merge axum-integration spoke (REQ-SSR-011, #226)
```

The branch is in a **passing build state** for the work completed:
- 56 ferric unit tests pass
- `cargo build -p chirp-server` exits zero
- All compile checks pass

---

## GitHub PR

**PR was NOT created** because `marker-format-agreement` fails and issue #224 is unaddressed.

Pre-existing related PR: #227 (`work/ferric-ssr-r1-axum` → target, open) — covers axum
integration portion of #226 only. The synthesis gate PR is distinct and cannot be opened
until #224 is resolved.

---

## Known Gaps and Follow-Up Required

1. **Client-hydrate spoke must be executed** (`ferric-ssr-r1-client-hydrate` task):
   - Branch `work/ferric-ssr-r1-client` to be created from current `work/ferric-ssr-r1`
   - Implement `hydrate` per `contracts/ferric_ssr_contract.rs` and the spoke's `_BRIEF.md`
   - After that spoke completes, re-run synthesis: merge `work/ferric-ssr-r1-client` into
     `work/ferric-ssr-r1`, re-run all assertions, create the PR

2. **PR #227** (axum integration) is open but not merged. The final synthesis PR will
   supersede it — recommend closing #227 without merge to avoid duplicate history.

3. **BAR-005 / #225** (state carry + async resource resume): remains out of scope,
   blocked on issue #130. The mandatory follow-up sentence for the future PR is:
   "BAR-005 / #225 (state carry + async resource resume) is a follow-up issue dependent
   on #130 and is NOT part of this goal."

---

## Disposition

| Deliverable | Status |
|---|---|
| `work/ferric-ssr-r1` branch with server + axum merged | ✅ Delivered (pushed to origin) |
| `work/ferric-ssr-r1` branch with ALL three spokes merged | ❌ Blocked (client spoke missing) |
| GitHub PR closing #223, #224, #226 | ❌ Not created — blocked on client-hydrate spoke |
| `SYNTHESIS.md` documenting state | ✅ This file |
