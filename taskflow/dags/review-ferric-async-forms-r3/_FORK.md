owner_id: overseer/I281
owning_thread: overseer/I281
thread_type: dag
launch_agent: swe-reviewer
observation_seam: taskflow/dags/review-ferric-async-forms-r3/SYNTHESIS.md
reap_policy: retain
disposition: retain
goal: "Review PR #193 (ferric async resources, expanded events, form binding) after ferric-async-forms-r3 remediation: verify B1 (reactive Resource/create_resource), B2 (EventHandler enum / prevent_default), B3 (Bind DOM→signal wiring) are resolved and all acceptance criteria met"

---

# Review DAG: review-ferric-async-forms-r3

**Goal**: Full code review of PR #193 (`work/ferric-async-forms-r2`) after ferric-async-forms-r3 remediation of the three blockers from review-ferric-async-forms-r2.

**Repository**: Nousix-LLC/nswe-demo  
**Branch**: `work/ferric-async-forms-r2`  
**PR**: #193 — Ferric async resources, expanded events, and form binding  
**Issues**: #130 (async resources, expanded events, form binding epic)

---

## Prior Review Context

**review-ferric-async-forms-r2** returned **REQUEST-CHANGES** with three blockers:

- **B1 — REQ-ASYNC-001, 003, 005**: `Resource` was fire-once with no reactive re-fetch. When the source signal changed, the resource did not reset to Loading and did not re-trigger the fetcher. The two-argument `create_resource(source, fetcher)` constructor was absent.
- **B2 — REQ-ASYNC-023**: No path existed for a handler to call `prevent_default()` or `stop_propagation()`. `EventHandler` was a plain `Rc<dyn Fn()>` type alias — no event argument could be threaded through.
- **B3 — REQ-ASYNC-042**: `Bind<T>` DOM→signal direction was broken in WASM. The `on_input` binding did not read the input element's current value and write it back to the field signal on user input.

## What ferric-async-forms-r3 Delivered (PASS — 6 CI checks green, head `838239e`)

| Commit | Message | Concern |
|--------|---------|---------|
| `9fedad9` | feat(ferric): add create_resource reactive async constructor | B1 / REQ-ASYNC-001, 003, 005 |
| `9557f0c` | feat(ferric): redesign EventHandler as enum for event-carrying closures | B2 / REQ-ASYNC-023 |
| `838239e` | B3 (REQ-ASYNC-042): add Bind::on_input_event_handler() + WASM test | B3 / REQ-ASYNC-042 |

CI run: https://github.com/Nousix-LLC/nswe-demo/actions/runs/42126720006  
All 6 jobs (`fmt`, `clippy`, `doc`, `test`, `wasm`, `image`) concluded `success`.

---

## Acceptance Criteria

Review against all in-scope requirements for issue #130:

**Async resources (REQ-ASYNC-001 through REQ-ASYNC-016)**
- REQ-ASYNC-001: `create_resource(source, fetcher)` — two-argument reactive constructor; `source` is a closure reading signals; `fetcher` takes a source value and returns a Future; the resource fires immediately on construction
- REQ-ASYNC-003: Changing a signal read by `source` resets the resource to `Loading` and re-triggers the fetcher with the new source value
- REQ-ASYNC-005: Reactive re-fetch: the resource re-fetches on each distinct new source value; in-flight futures from stale source values are discarded
- REQ-ASYNC-016: Generation counter: a stale future's result (from a superseded source value) is silently dropped; only the latest generation's result is applied

**Expanded event handling (REQ-ASYNC-023)**
- REQ-ASYNC-023: `EventHandler` supports event-carrying variant; a handler closure can receive the raw DOM event as a platform-independent reference, downcast it to `web_sys::Event`, and call `prevent_default()` or `stop_propagation()`; `vdom.rs` does not import `web_sys`; backward compatibility with zero-argument handlers is preserved

**Form binding (REQ-ASYNC-042)**
- REQ-ASYNC-042: `Bind<T>` DOM→signal direction works in WASM; `on_input_event_handler()` returns an event handler that reads the `HtmlInputElement`'s current value and writes it back to the bound signal on each `input` event; a `wasm-bindgen-test` covers this path end-to-end

---

## Review Scope and Concerns

This is a full review of the change. Apply all standard concerns:

1. **Correctness**: Does each of REQ-ASYNC-001, 003, 005, 016, 023, 042 work as specified? Focus especially on the three former blockers. Verify edge cases: concurrent in-flight futures for rapid source changes (REQ-ASYNC-016 generation counter), event downcasting safety (panics vs. graceful no-op on unexpected event type), and signal write ordering in `on_input_event_handler`. Verify backward compatibility: zero-argument `EventHandler` callers must compile unchanged.

2. **Code quality and design**: Responsibilities and coupling across `async_resource.rs`, `vdom.rs`, `form.rs`, `dom.rs`. Is the `EventHandler` enum variant scheme a sound abstraction boundary — does `vdom.rs` correctly stay free of `web_sys`? Is the generation counter in `create_resource` straightforward and free of race conditions in a single-threaded WASM executor (`spawn_local`)?

3. **Test coverage and depth**: Do the tests in `async_resource.rs` exercise the generation counter and reactive re-fetch scenarios as stated? Does the `wasm-bindgen-test` for REQ-ASYNC-042 (`on_input_event_handler_updates_signal_from_dom_value`) attach a real DOM element, dispatch a real event, and assert signal state — or is it vacuous? Does the `event_carrying_handler_can_call_prevent_default` test in `dom.rs` actually verify `prevent_default()` took effect?

4. **Concurrency and async hazards**: `create_resource` uses `spawn_local` inside a reactive effect; verify no double-borrow or dropped references in the closure captures. Verify the generation counter approach is sound for the `'static` closure constraints.

5. **Security**: No new HTML injection or escaping gap. No host path, internal address, or infrastructure detail committed into the repository.

6. **Language idiom (Rust)**: `closure.forget()` in the WASM test (`form.rs` L519) — is this acceptable or should it be commented? `resource.signal.set(...)` direct field access in native tests (`async_resource.rs`) — is a test helper warranted? No unnecessary `unsafe`.

7. **API and contract stability**: `EventHandler` is a public type. The enum redesign must preserve the existing public API surface for callers passing `impl Fn()` to `VElement::on_event()`. Verify the wrapper in `vdom.rs` makes this transparent.

---

## Prior Non-Blockers

Non-blockers from review-ferric-async-forms-r2 were filed as issues #196–#201 and are on the board as separate backlog items. Do not re-raise them as blockers in this review. If the remediation introduced new non-blockers, file them as new issues and list them in the synthesis.

---

## Declared Output

A `SYNTHESIS.md` at the DAG root with:
- Verdict: `APPROVE` or `REQUEST-CHANGES`
- If `APPROVE`: confirmation that B1, B2, and B3 are resolved, all in-scope requirements satisfied, CI green, and PR #193 is ready to land
- If `REQUEST-CHANGES`: each remaining blocker named against its requirement ID; severity and whether it blocks stated for every finding; non-blockers filed as issues and listed

Post the review findings to PR #193 as a GitHub review comment (or a review if the platform permits). The posted review must be readable as the repository's own: findings name files and lines by repository-relative paths; nothing names internal host paths, taskflow internals, or infrastructure addresses.

---

## Notes

- The escalation comment on PR #193 (from overseer I220, https://github.com/Nousix-LLC/nswe-demo/pull/193#issuecomment-6624409600) is obsoleted by this re-review — do not reference or re-raise it
- ferric-async-forms-r3's code DAG synthesis is at `taskflow/dags/ferric-async-forms-r3/SYNTHESIS.md`
- Non-blockers previously filed (#196–#201) are on the board as backlog issues; do not re-open or re-file them
