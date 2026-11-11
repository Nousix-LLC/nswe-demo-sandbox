# Review DAG: review-ferric-async-forms-r3

## Project Context

**Status**: Active

### Objective

Full code review of PR #193 (`work/ferric-async-forms-r2`) after ferric-async-forms-r3 remediation of three blockers from review-ferric-async-forms-r2. Verify B1, B2, B3 are resolved, all acceptance criteria for issue #130 are met, and produce a verdict (APPROVE or REQUEST-CHANGES) with a posted review on PR #193.

### Scope

**In Scope:**
- B1 (REQ-ASYNC-001, 003, 005, 016): `create_resource` reactive constructor with generation counter
- B2 (REQ-ASYNC-023): `EventHandler` enum redesign, `prevent_default`/`stop_propagation` path, `vdom.rs` isolation from `web_sys`
- B3 (REQ-ASYNC-042): `Bind<T>::on_input_event_handler()` WASM correctness
- Code quality and design across changed files (`async_resource.rs`, `vdom.rs`, `form.rs`, `dom.rs`)
- Test coverage depth: generation counter tests, WASM tests, prevent_default verification
- Concurrency and async hazards in `spawn_local` / reactive effect composition
- Rust language idiom (closure.forget(), direct signal field access in tests)
- API and contract stability for the public `EventHandler` type
- Security: no HTML injection gap, no secrets/infrastructure data committed

**Out of Scope:**
- Non-blockers previously filed as issues #196–#201 (do not re-raise)
- The escalation comment from overseer I220 (obsoleted by this re-review)
- Concerns outside the three remediation commits

### Key Reference Data

**Repository**: Nousix-LLC/nswe-demo  
**Branch**: `work/ferric-async-forms-r2`  
**PR**: #193 — Ferric async resources, expanded events, and form binding  
**Head SHA**: `838239e11f131484d4db617fb25dc6e5ea435be1`  
**Issue**: #130 (async resources, expanded events, form binding epic)

**Remediation commits:**

| Commit | Message | Concern |
|--------|---------|---------|
| `9fedad9` | feat(ferric): add create_resource reactive async constructor | B1 / REQ-ASYNC-001, 003, 005 |
| `9557f0c` | feat(ferric): redesign EventHandler as enum for event-carrying closures | B2 / REQ-ASYNC-023 |
| `838239e` | B3 (REQ-ASYNC-042): add Bind::on_input_event_handler() + WASM test | B3 / REQ-ASYNC-042 |

**CI run**: https://github.com/Nousix-LLC/nswe-demo/actions/runs/42126720006  
All 6 jobs (`fmt`, `clippy`, `doc`, `test`, `wasm`, `image`) concluded `success`.

**Code DAG synthesis (prior step):** `taskflow/dags/ferric-async-forms-r3/SYNTHESIS.md`

---

### Acceptance Criteria

**Async resources (REQ-ASYNC-001 through REQ-ASYNC-016)**
- REQ-ASYNC-001: `create_resource(source, fetcher)` two-argument reactive constructor; fires immediately; source closure reads signals; fetcher returns a Future
- REQ-ASYNC-003: Changing a signal read by `source` resets to `Loading` and re-triggers fetcher with new source value
- REQ-ASYNC-005: Reactive re-fetch on each distinct new source value; in-flight futures from stale source values are discarded
- REQ-ASYNC-016: Generation counter: stale future's result is silently dropped; only latest generation's result applied

**Expanded event handling (REQ-ASYNC-023)**
- REQ-ASYNC-023: `EventHandler` supports event-carrying variant; closure receives raw DOM event as `&dyn Any`; can downcast to `web_sys::Event` and call `prevent_default()`/`stop_propagation()`; `vdom.rs` does NOT import `web_sys`; backward compatibility with zero-argument handlers preserved

**Form binding (REQ-ASYNC-042)**
- REQ-ASYNC-042: `Bind<T>::on_input_event_handler()` returns `EventHandler::WithEvent`; reads `HtmlInputElement::value()`; writes to field signal on each `input` event; `wasm-bindgen-test` covers this path end-to-end

---

## Constraints

- Review text posted to PR #193 must name files/lines by repository-relative paths only; no internal host paths, taskflow paths, or infrastructure addresses
- Non-blockers #196–#201 are filed; do not re-raise them as blockers; if remediation introduced new non-blockers, file them as NEW issues and list in synthesis
- Verdict must be `APPROVE` or `REQUEST-CHANGES` with explicit justification

---

## Subtree Methodology Posture

**Dominant task type:** Ferric PR review (Rust library)  
**Primary bundles:** Code Review, Rust  
**Supporting bundles:** Framework Design (for API/contract stability concerns)

**Cross-cutting bindings across all spokes:**
- `code-review/CodeReview_Checklist_Methodology.md` — the review checklist applies to every concern area
- `code-review/CodeReview_Process_Methodology.md` — review process applies to every spoke
- `rust/Rust_Async_Tokio_Methodology.md` — `spawn_local`, reactive effects, closure captures
- `rust/Rust_Testing_Methodology.md` — test adequacy standards

---

## Task Structure

```
review-ferric-async-forms-r3/
├── _GLOBAL.md                                        (this document)
├── contracts/
│   └── _MANIFEST.yaml                                (findings schema + ownership)
├── SUBTASK_correctness_concurrency/
│   └── _BRIEF.md
├── SUBTASK_quality_tests_idiom/
│   └── _BRIEF.md
├── SUBTASK_security/
│   └── _BRIEF.md
└── SUBTASK_synthesis/
    └── _BRIEF.md
```

### Task Summary

| Task id | Depends on | Description | Output |
|---------|------------|-------------|--------|
| `SUBTASK_correctness_concurrency` | none | Verify B1/B2/B3 correctness + concurrency/async hazards (concerns 1 & 4) | `SUBTASK_correctness_concurrency/findings.md` |
| `SUBTASK_quality_tests_idiom` | none | Code quality/design + test coverage depth + Rust idiom + API stability (concerns 2, 3, 6, 7) | `SUBTASK_quality_tests_idiom/findings.md` |
| `SUBTASK_security` | none | Security pass (concern 5) | `SUBTASK_security/findings.md` |
| `SUBTASK_synthesis` | `SUBTASK_correctness_concurrency`, `SUBTASK_quality_tests_idiom`, `SUBTASK_security` | Synthesis/verification gate: compile verdict, write SYNTHESIS.md, post review to PR #193 | `SYNTHESIS.md` (at this directory) |

### Dependency Graph

```
SUBTASK_correctness_concurrency ──┐
                                   │
SUBTASK_quality_tests_idiom    ──┼── SUBTASK_synthesis
                                   │
SUBTASK_security               ──┘
```

---

## Contract

**Contract location:** `contracts/` (read-only for descendants)  
**Contract kind:** `yaml_schema`

See `contracts/_MANIFEST.yaml` for findings structure, ownership, and identities each spoke must produce.

### Structural Declarations

Each spoke MUST produce a `findings.md` file at its own workspace root following the findings schema:
- One or more entries, each with: severity (`blocker`/`non-blocker`/`clean`), requirement ID (if applicable), location (file:line), description, and disposition
- A section "What was checked and found sound" naming what the spoke examined and found no issues with

### Ownership

| Artifact | Owning subtask |
|----------|---------------|
| `SUBTASK_correctness_concurrency/findings.md` | `SUBTASK_correctness_concurrency` |
| `SUBTASK_quality_tests_idiom/findings.md` | `SUBTASK_quality_tests_idiom` |
| `SUBTASK_security/findings.md` | `SUBTASK_security` |
| `SYNTHESIS.md` | `SUBTASK_synthesis` |

### Identities

- [ ] Every requirement in scope (REQ-ASYNC-001, 003, 005, 016, 023, 042) must appear in at least one spoke's findings (either as verified clean or as a finding)
- [ ] Synthesis verdict must be supported by all three spoke findings
- [ ] Any blocker must name its requirement ID and location

---

## Output Specifications

| Deliverable | Format | Location | Description |
|-------------|--------|----------|-------------|
| `SYNTHESIS.md` | Markdown | `review-ferric-async-forms-r3/SYNTHESIS.md` | Verdict, findings, CI confirmation, PR posting confirmation |
