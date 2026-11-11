# Task: Architecture, layering & frozen-contract conformance review of chirp-server (PR #19)

## Task Specification
**Slug**: SUBTASK_architecture_contract_review
**Task Kind**: standard
**Status**: Pending

### Objective
Review the `chirp-server` feature diff (PR #19, head `714d50f`) through the **single lens of
architecture / layering / frozen-`chirp-types`-contract conformance**, and emit
`findings_architecture_contract.md` conforming to the findings contract. You review; you do NOT
edit, fix, or push.

### Context
Part of the review-chirp-server review DAG (`../_GLOBAL.md`). Sibling spokes own Rust soundness,
test adequacy, and code-review quality. You own the most acceptance criteria (AC1–AC5) plus the F1
reachability/contract-satisfaction questions (F1_1, F1_3). Stay on structure & contract.

**Dependencies**: none. **Dependents**: `SUBTASK_synthesis_verdict`.

## Input Specification
| Input | Source | Purpose |
|-------|--------|---------|
| Hub | `../_GLOBAL.md` | Shared context, input set, discipline |
| Findings contract | `../contracts/findings_schema.md`, `../contracts/_MANIFEST.yaml` | Output shape; owned AC1–AC5, F1_1, F1_3 |
| Root rubric | `../_BRIEF.md` | Full acceptance rubric + the `chirp-types` wire contract detail |
| PR diff | `gh pr diff 19 -R Nousix-LLC/nswe-demo` | The change under review |
| Checkout | `/home/user/nousix-runtime/nswe-demo/taskflow/dags/chirp-server/checkout/crates/chirp-server/src/` | `api/{router,handlers,auth,json,state,mod}.rs`, `error.rs`, `lib.rs`, `main.rs`, `repository/{in_memory,mod}.rs` |
| Contract crate | `.../checkout/crates/chirp-types/` | The frozen wire contract the server MUST compose, never redefine |
| Code DAG verdict | `/home/user/nousix-runtime/nswe-demo/taskflow/dags/chirp-server/SYNTHESIS.md` | Context only (wiring/contract/duplication checks already PASS; re-review for design) |

## Review Concern (one responsibility: architecture & contract conformance)
- **AC1 — Full REST surface**: confirm the 9 `/api/...` routes (create user, login/session, get
  profile, post chirp, home timeline [reverse-chronological, cursor + limit-clamp], follow/unfollow,
  like/unlike) are mounted in ONE composition root (`build_router`), plus `GET /healthz` and a
  static-file service with **SPA fallback** for client-side routes.
- **AC2 — Layering & repo seam**: transport → service → repository separation; persistence behind
  the `ChirpRepository` trait with an **in-memory default** (`Arc<dyn ChirpRepository>`); server
  boots and the whole suite runs with **no database**; SQLite/`sqlx` only a documented optional
  backing, never a test prerequisite. Review in-memory repo **semantics**: timeline ordering/cursor/
  limit-clamp, follow/like idempotency, conflict/duplicate (409) handling.
- **AC3 — Typed error mapping**: `ServerError` → `ApiError`/`ErrorCode` + HTTP status via
  `IntoResponse` is complete and correct for all six rows (400 VALIDATION_ERROR, 401 UNAUTHORIZED,
  403 FORBIDDEN, 404 NOT_FOUND, 409 CONFLICT, 500 INTERNAL). (Rust spoke co-reviews the enum idiom;
  you own mapping *correctness/completeness*.)
- **AC4 — tracing + lib exposure**: structured `tracing`; `lib.rs` exposes router + repository so
  integration tests drive the real app against the in-memory repo.
- **AC5 — No DTO redefinition**: DTOs imported from `chirp-types`, never redefined; wire shape
  honored by composition — base `/api`, **camelCase** JSON, `Authorization: Bearer`, `ErrorCode`
  **SCREAMING_SNAKE_CASE**. Flag any local re-declaration of a contract type as a `block`.
- **F1_1 — fix is live, not dead code**: the three body handlers (`create_user`, `login`,
  `create_chirp`) extract via `ValidatedJson<T>`; the 400 arm is routed; no orphaned items.
- **F1_3 — `details` limitation contract-satisfaction**: `details` carries a single generic
  `FieldError{field:"body", message:<rejection text>}` (field name not structurally recoverable from
  axum `JsonRejection` without `serde_path_to_error`). Assess whether this satisfies the contract's
  "populate details (`Vec<FieldError>`)" requirement; state your reading (satisfies / weakens /
  blocking) with reasoning. **The final acceptable-vs-blocking ruling is the gate's**, but give it
  your contract-conformance analysis to rule on.

A frozen-contract violation (DTO redefinition, wrong wire shape, missing/incorrect status mapping,
a route absent from the surface) is a `block`. Layering impurity that is correct-but-leaky is
`major`/`minor` per impact.

## Methodology (load on demand — IDs only)
### Suggested Methodology Files
Matched rows: **"Code review" → Code Review / Core** and **"Designing systems" → Architecture**.
- `architecture` — primary. Flag `Architecture_API_Design_Methodology.md` (REST surface, wire
  contract), `Architecture_Styles_Methodology.md` / `Architecture_Dependency_Management_Methodology.md`
  (layering, the `Arc<dyn>` seam & dependency direction), `Architecture_Data_Modeling_Methodology.md`
  (repo semantics).
- `code-review` — `CodeReview_Checklist_Methodology.md`, `CodeReview_Process_Methodology.md`.
- `core` — baseline standards.
Load on demand via `engine_load_methodology`. **Suggestions, not exclusive** — you are the final judge.

### Inherited Constraints
- `chirp-types` (#7) is **landed and frozen** — the server composes it and MUST NOT redefine the contract.
- Stack: axum + Tokio; persistence seam `Arc<dyn ChirpRepository>` with in-memory default; no DB in tests.
- Reviewer discipline (P1): read-only; no edits/push/rebase/relock; never touch `main`.
- Do NOT flag the CONFLICTING/DIRTY mergeability (known `Cargo.lock` restale, overseer clears it).

### Out-of-Scope Methodologies
- Testing bundle (that is `SUBTASK_test_adequacy_review`) — you confirm `lib.rs` *exposes* the app for
  tests (AC4), but test coverage adequacy is the test spoke's.

## Output Specification
**Primary output**: `findings_architecture_contract.md` conforming to `../contracts/findings_schema.md`,
with the owned-items verdict ledger covering AC1–AC5, F1_1, F1_3.

## Success Criteria
- [ ] AC1–AC5 each rendered with an explicit verdict + evidence (`file:line` / route / diff ref).
- [ ] In-memory repo semantics (timeline ordering/cursor/clamp, follow/like idempotency, 409) assessed.
- [ ] F1_1 (live/not-dead) and F1_3 (`details` contract-satisfaction analysis) answered.
- [ ] Every finding uses the fixed severity vocabulary and cites evidence; ledger present; file written.
