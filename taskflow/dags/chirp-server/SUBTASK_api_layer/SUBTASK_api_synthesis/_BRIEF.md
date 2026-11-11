# Task: API-layer verification gate + handoff (synthesis/fold)

## Task Specification

**Slug**: SUBTASK_api_synthesis
**Task Kind**: synthesis
**Status**: Pending

### Objective

Act as the **verification gate** for the chirp-server API-layer subtree: assert that the combined
output of the three implementation spokes satisfies the sub-contract's identities, then author the
`API_NOTES.md` handoff and fold the result into the suspended parent (`SUBTASK_api_layer`). This is a
gate, **not a prose summary** — it either asserts coverage (PASS) or schedules remediation fix-tasks
(FAIL); it does not green-wash.

### Context

This task is the synthesis hub of the subtree (see `../_GLOBAL.md`). Its three sibling spokes
(`SUBTASK_transport_foundations`, `SUBTASK_handlers`, `SUBTASK_router_and_bootstrap`) have committed
the error `IntoResponse` + `AppState` + auth extractor, the full handler surface, and
`build_router` + static/SPA + `/healthz` + tracing + `main.rs` into the shared clone on
`work/chirp-server`. You verify the assembled layer against `../contracts/_MANIFEST.yaml §identities`
and the parent `../../contracts/_MANIFEST.yaml §error_mapping`.

**Scope boundary**: this gate verifies the **API layer** (build + wiring + contract + error mapping +
clippy/fmt for `-p chirp-server`). It does NOT run the full-workspace `cargo test`, author the
integration suite or `README.md`, or open the PR — those belong to the parent's
`../../SUBTASK_integration_tests_and_docs` and `../../SUBTASK_synthesis_gate`. Stay in the API-layer lane.

**Dependencies**: `SUBTASK_transport_foundations`, `SUBTASK_handlers`, `SUBTASK_router_and_bootstrap`.
**Dependents**: folds into the suspended parent `SUBTASK_api_layer` (see Fold wiring below).

---

## Input Specification

| Input | Source | Purpose |
|-------|--------|---------|
| Subtree hub | `../_GLOBAL.md` | Subtree objective, success criteria, output locations |
| Sub-contract | `../contracts/_MANIFEST.yaml` | `identities`, `endpoint_surface`, `ownership`, the symbol seam to assert |
| Parent contract | `../../contracts/_MANIFEST.yaml` | Authoritative `error_mapping` + `repository_seam` to check handlers against |
| Spoke handoffs | `../SUBTASK_transport_foundations/FOUNDATIONS_NOTES.md`, `../SUBTASK_handlers/HANDLERS_NOTES.md`, `../SUBTASK_router_and_bootstrap/BOOTSTRAP_NOTES.md` | What each spoke claims it produced — route table, exposed symbols, serving wiring |
| Committed code | the shared clone at the contract's `clone_path` | The real combined output to verify + build |

---

## Process / Approach

Run the **four-check model** over the combined api-layer output (see the Synthesis methodology):

1. **Contract** — every `endpoint_surface` op is routed; `ServerError → ErrorCode → HTTP status`
   matches the parent `error_mapping` for every variant (validation `details` populated).
2. **Wiring** — every handler is mounted in `build_router` and reachable; handlers delegate through
   `ChirpRepository` (no persistence bypass); `build_router` is re-exported from `lib.rs`; no detached
   dead code.
3. **Dedup / contract-purity** — no DTO/trait/error re-declared in `chirp-server`; all wire types come
   from `chirp-types`; the trait/error come from the predecessor's modules.
4. **Review** — a focused code review of the combined transport layer (layering, clarity, error paths).

Run the authoritative commands from `../contracts/_MANIFEST.yaml §identities`:
`cargo build -p chirp-server`, `cargo clippy -p chirp-server --all-targets -- -D warnings`,
`cargo fmt -p chirp-server --check`. (Full `cargo test` + the four-check over the WHOLE crate is the
parent gate's job; here, confirm the API layer builds and wires.)

**On FAIL**, do not patch silently and do not green-wash: schedule remediation as decomposed fix-tasks
via `engine_amend_plan { add_task }` (Inject) targeting the specific gap, then record FAIL with the
scheduled remediation. **On PASS**, author the handoff and fold.

### Methodology

This task is a verification gate. Load `synthesis/Synthesis_Overview_Methodology.md` first (always),
then the sibling check files your reading of the subtree calls for. You are the final judge of
coverage depth.

---

## Output Specification

### Primary outputs (at the PARENT `SUBTASK_api_layer/` workspace — the fold location)

| Deliverable | Location | Description |
|-------------|----------|-------------|
| `API_NOTES.md` | `../API_NOTES.md` (i.e. `SUBTASK_api_layer/API_NOTES.md`) | The API-layer handoff `../../SUBTASK_integration_tests_and_docs` reads: the route table (method + path + request DTO + response DTO + status), the `AppState` design, the error→HTTP mapping as implemented, how static serving + SPA fallback are wired (+ placeholder dir), how to run the server, and the local `cargo build -p chirp-server` status. |
| `SYNTHESIS.md` | `../SYNTHESIS.md` (i.e. `SUBTASK_api_layer/SYNTHESIS.md`) | The fold record + verdict: four-check results, the identity assertions with evidence, build/clippy/fmt results, PASS/FAIL, and any scheduled remediation. |

### Fold wiring (how this task resolves the parent)

1. Author `../SYNTHESIS.md` and `../API_NOTES.md` via `engine_write`.
2. Terminal `engine_report_status { status: "completed", outputs: ["<abs>/SUBTASK_api_layer/API_NOTES.md", "<abs>/SUBTASK_api_layer/SYNTHESIS.md"], artifact_path: "<abs>/SUBTASK_api_layer/SYNTHESIS.md" }`.
3. `engine_resume_suspended { target_task_id: "SUBTASK_api_layer", synthesized_task_id: "SUBTASK_api_synthesis", seam_path: "<abs>/SUBTASK_api_layer/SYNTHESIS.md" }` — flips the parent `SUSPENDED → COMPLETED`, unblocking `../../SUBTASK_integration_tests_and_docs`.

(`<abs>` = `/home/user/nousix-runtime/nswe-demo/taskflow/dags/chirp-server`.)

---

## Success Criteria

- [ ] All four checks (contract, wiring, dedup, review) run over the combined output; each identity in `../contracts/_MANIFEST.yaml` evaluated as an assertion with recorded evidence.
- [ ] `cargo build -p chirp-server`, `cargo clippy -p chirp-server --all-targets -- -D warnings`, `cargo fmt -p chirp-server --check` run; results recorded.
- [ ] A PASS/FAIL verdict recorded in `../SYNTHESIS.md`; on FAIL, remediation scheduled as fix-tasks (no silent plug, no green-wash).
- [ ] `../API_NOTES.md` authored with the full route table + state + error-mapping + serving + run instructions.
- [ ] The parent `SUBTASK_api_layer` folded `SUSPENDED → COMPLETED` via `engine_resume_suspended`.

---

## Suggested Methodology Files

Matched Domain-Mapping row: **Synthesizing/verifying a hub-and-spoke decomposition → primary
`synthesis`; supporting `code-review`.** Load via `engine_load_methodology { name: "<bundle_id>" }`.

- `synthesis` — `synthesis/Synthesis_Overview_Methodology.md` (anchor — always first; the four-check
  gate model + `SYNTHESIS.md` schema), `synthesis/Synthesis_Contract_Verification_Methodology.md`
  (endpoint/error-mapping coverage against the contract), `synthesis/Synthesis_Wiring_Verification_Methodology.md`
  (every handler mounted + reachable, no dead code), `synthesis/Synthesis_Duplication_Detection_Methodology.md`
  (no re-declared DTO/trait), `synthesis/Synthesis_Code_Review_Methodology.md` (review of the combined
  layer), `synthesis/Synthesis_Remediation_Methodology.md` (remediation-as-decomposition on FAIL).
- `code-review` — `code-review/CodeReview_Checklist_Methodology.md`, `code-review/CodeReview_Process_Methodology.md`.

Load `Synthesis_Overview_Methodology.md` first; load the sibling check/remediation files your reading
of the subtree reveals it needs. You are the final judge of coverage depth. (A synthesis gate never
loads `decomposition/` content — synthesis is the reassembly, not the split.)

## Inherited Constraints

- The gate asserts; it does not implement. If a check fails, schedule a fix-task — do not edit the spokes' code yourself.
- `contracts/` is READ-ONLY. All verification happens against the real committed code in the ONE shared clone; never touch `main`; no commit-attribution trailers.
- Stay in the API-layer lane: no full-workspace `cargo test`, no integration suite, no `README.md`, no PR — those are parent-level siblings.

## Out-of-Scope Methodologies

- Do NOT load `decomposition/` methodology — this is the reassembly gate, not a decomposer.
- Do NOT treat this as a prose summary task — the Synthesis bundle's gate posture is mandatory.
