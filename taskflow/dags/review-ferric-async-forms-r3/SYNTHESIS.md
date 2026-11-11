# SYNTHESIS — review-ferric-async-forms-r3

## Verdict

```
gate:  FAIL
round: 1
```

**PR verdict: REQUEST-CHANGES**

One blocker is open. The generation-counter stale-write guard (REQ-ASYNC-016) is not exercised by any existing test; deleting the guard would leave all tests green. The design is sound; the coverage gap is what blocks.

---

## Checks

| Check       | Result | Mechanical evidence                                                                      | Notes |
|-------------|--------|------------------------------------------------------------------------------------------|-------|
| wiring      | pass   | All three spokes filed `findings.md`; each covered its declared concern area with no detached spoke | No contradiction across spokes |
| contract    | pass   | REQ-ASYNC-001, 003, 005, 016, 023, 042 each appear in at least one spoke; `blocker_has_location` identity satisfied (blocker names REQ-ASYNC-016 + file:line); `synthesis_verdict_supported` identity derivable from spoke files | Full requirements coverage |
| duplication | pass   | REQ-ASYNC-016 appears in two spokes asking different questions (design soundness vs. test coverage); no finding duplicated across spokes | No consolidation needed |
| code-review | fail   | One blocker finding from `SUBTASK_quality_tests_idiom`; 11 non-blockers recorded (see §Findings) | Gate fails on the blocker |

---

## Findings

### Blockers

**[B1]** severity=block  check=code-review  requirement=REQ-ASYNC-016  
location=`crates/ferric/src/async_resource.rs:652`  
statement=Generation-counter stale-write guard never exercised: existing tests cannot detect deletion of the `if gen_check.get() == next_gen` check.  
mechanical=LLM-judged; structural analysis of test execution path confirmed by spoke SUBTASK_quality_tests_idiom.

The native test `create_resource_two_source_changes_stay_loading` (line 655) takes the `#[cfg(not(target_arch = "wasm32"))]` branch, which calls `drop(fut)` — no future is ever spawned and the generation guard never runs. The WASM test `create_resource_refetches_on_source_change` (line 778) covers only sequential refetch (first fetch already `Ready` before the source changes), so the guard is never in the stale-write path. Removing the guard leaves every test green.

Satisfying condition: a WASM test that (1) constructs a fetcher backed by a manually-held Promise resolve handle; (2) triggers the first fetch (gen=1 starts, state is `Loading`); (3) changes the source signal before releasing the first future (gen=2 starts, state remains `Loading`); (4) releases the first future; (5) asserts the signal did *not* become `Ready` with the first result. That test fails if the guard is deleted.

Tracked: #248

---

### Non-blockers (11)

All filed as GitHub issues. No re-filing of #196–#201.

| # | Concern | Location | Issue |
|---|---------|----------|-------|
| NB-1 | `suspense()` colocation undocumented | `async_resource.rs:14` | #254 |
| NB-2 | Sideways `async_resource → vdom` dependency undocumented | structural | #255 |
| NB-3 | Generation counter declaration has no inline comment | `async_resource.rs:217` | #256 |
| NB-4 | `create_resource` missing from `ferric::prelude` | `lib.rs:41` | #257 |
| NB-5 | `Resource::new` / `Resource::new_fallible` missing WASM gate note | `async_resource.rs:112, 133` | #258 |
| NB-6 | `on_input_handler` stale-write precondition not documented at call site | `form.rs:175` | #259 |
| NB-7 | No `VElement::with_handler(kind, EventHandler)` builder method | `vdom.rs:317` | #260 |
| NB-8 | Fail-silent paths of `on_input_event_handler` have no tests | `form.rs:220` | #261 |
| NB-9 | `closure.forget()` in production `set_events()` has no lifecycle comment | `dom.rs:287` | #262 |
| NB-10 | `ResourceState<T>` and `EventHandler` missing `#[non_exhaustive]` | `async_resource.rs:1` | #253 |
| NB-11 | `EventHandler` missing from `ferric::prelude` | `lib.rs:40–41` | #252 |

---

## Spoke summary

### SUBTASK_correctness_concurrency — all clean, no blockers

Covered REQ-ASYNC-001, 003, 005, 016, 023, 042 and an independent concurrency hazard assessment. Verified the generation-counter design is sound (the logic at `async_resource.rs:217–243` correctly discards stale futures in every scenario including non-FIFO network delivery). Verified the WASM execution model eliminates races (`!Send` marker, single-threaded microtask queue, synchronous effect closure). No borrow-safety or use-after-free concerns. All six requirements clean.

### SUBTASK_quality_tests_idiom — one blocker, 11 non-blockers

One blocker on REQ-ASYNC-016: the generation guard's concurrent in-flight scenario is untested (see §Findings). Eleven non-blockers across code quality (colocation doc, sideways-dep doc, inline comments, prelude discoverability, WASM gate notes, stale-write precondition, builder gap), tests (fail-silent paths), idiom (`closure.forget()` comment), and API stability (#[non_exhaustive], prelude completeness). Twenty-three items checked and found clean.

### SUBTASK_security — all clean, no blockers

Covered HTML injection, secrets/infra data, unsafe code, downcast panic surface, and `closure.forget()` scope. Confirmed no `set_inner_html` in the rendering path, no hardcoded credentials, zero `unsafe` blocks added, all production downcasts guarded with `if let`, and the new `forget()` is test-only. Security spoke clean.

---

## CI evidence

All 6 CI jobs (`fmt`, `clippy`, `doc`, `test`, `wasm`, `image`) passed at `838239e`:  
https://github.com/Nousix-LLC/nswe-demo/actions/runs/42126720006

---

## Review posted

Review posted to PR #193 as a comment (GitHub blocks `--request-changes` on self-owned PRs):  
https://github.com/Nousix-LLC/nswe-demo/pull/193#issuecomment-6675723989
