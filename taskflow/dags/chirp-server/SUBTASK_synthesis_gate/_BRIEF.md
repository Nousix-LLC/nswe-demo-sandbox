# Task: Synthesis verification gate for `chirp-server` (push + PR + verdict)

## Task Specification

**Slug**: SUBTASK_synthesis_gate
**Task Kind**: synthesis
**Status**: Pending

### Objective

Act as the **verification gate** for the chirp-server subtree: run the authoritative build/test/fmt/clippy and
the four-check model over the combined output of the three implementation spokes, then — only if the work holds
up — push `work/chirp-server` and open the PR into `main`, and record a PASS/FAIL verdict with evidence at the
hub's `SYNTHESIS.md` (the fold location / observation seam). This is **not a prose summary**; it is a gate that
either asserts coverage (PASS) or schedules remediation (FAIL).

### Context

This is the terminal gate of the chirp-server pipeline (work-item #8). The three implementation spokes have
committed the full crate (repository layer → API layer → integration tests + docs) into the shared clone. You
verify the assembled result mechanically against the contract's assertion set, then handle delivery. The subtree
hub `_GLOBAL.md` and `contracts/_MANIFEST.yaml` bind you — the contract's `identities` are your assertion set.

**Dependencies**: `SUBTASK_scaffold_and_repository`, `SUBTASK_api_layer`, `SUBTASK_integration_tests_and_docs`.
**Dependents**: none — your `SYNTHESIS.md` is the fold record the parent resolves on.

---

## Input Specification

| Input | Source | Purpose |
|-------|--------|---------|
| Subtree hub | `../_GLOBAL.md` | Shared context, success criteria, identities |
| Contract | `../contracts/_MANIFEST.yaml` | The gate `identities` (assertion set) + ownership + error-mapping to verify against |
| Spoke handoffs | `../SUBTASK_scaffold_and_repository/IMPLEMENTATION_NOTES.md`, `../SUBTASK_api_layer/API_NOTES.md`, `../SUBTASK_integration_tests_and_docs/TEST_NOTES.md` | What each spoke claims it produced — verify against the real clone |
| Committed code | the shared clone at the contract's `clone_path` | The real assembled crate to build/test/review and deliver |

---

## Process / Approach — this is a verification GATE

Run the gate, do not summarize. Concretely, this task is a four-check gate over the combined output plus delivery:

1. **Build/test/fmt/clippy** — run each command in the contract's `identities` from the clone:
   `cargo build --workspace`, `cargo test` (unit + integration, no DB running), `cargo fmt --check`,
   `cargo clippy --all-targets -- -D warnings`. Capture real output as evidence.
2. **Contract check** — confirm all wire types come from `chirp-types` (no DTO re-declared in `chirp-server`), and
   errors surface as `ApiError`/`ErrorCode` per the error-mapping table.
3. **Wiring check** — confirm every in-scope endpoint is routed + reachable and handlers call through
   `ChirpRepository` (no bypass); no detached dead code; static serving + SPA fallback + `/healthz` present.
4. **Duplication / review check** — scan for duplicated shared logic across the spokes and give the combined diff a
   synthesis-level code review against the acceptance criteria.

**Decision.** If every check passes: push `work/chirp-server` and open the PR into `main`
(`gh pr create`, title per the contract, body summarizing design + test results and ending `Closes #8`), then
write `SYNTHESIS.md` = **PASS** with the PR URL. If any check FAILS: do **not** green-wash and do **not** open a
passing PR on broken work — record a **FAIL** verdict with evidence, and schedule remediation as decomposed
fix-task(s) (`engine_amend_plan { add_task }`, Inject) targeting the specific failure, followed by a re-verification.
A clean FAIL with evidence beats a false PASS.

### Methodology

Read `synthesis/Synthesis_Overview_Methodology.md` first (always), then load the sibling check/remediation files
your reading of the subtree reveals you need. You are the final judge of coverage depth.

---

## Output Specification

### Primary Output (fold record)

| Attribute | Value |
|-----------|-------|
| Filename | `SYNTHESIS.md` |
| Location | the **hub workspace** (`../SYNTHESIS.md`, i.e. `/home/user/nousix-runtime/nswe-demo/taskflow/dags/chirp-server/SYNTHESIS.md`) — the fold location / observation seam |

Must contain: a **build verdict**, a **test verdict** (incl. API integration tests), **fmt/clippy** results, the
four-check results, a **diff manifest** (files added/changed), the **PR URL**, and an overall **PASS/FAIL** — with
the PR URL and verdict prominent so the overseer can gate without re-running the build.

---

## Success Criteria

This gate is complete when:

- [ ] All contract `identities` were evaluated with real command output captured as evidence (no assertion skipped, no silent plug).
- [ ] The four checks (build/test/fmt/clippy; contract; wiring; duplication/review) were run and their results recorded.
- [ ] On PASS: branch pushed, PR into `main` opened with body ending `Closes #8`, PR URL recorded.
- [ ] On FAIL: a clean FAIL verdict with evidence, and remediation scheduled as decomposed fix-task(s) + re-verification (no false PASS).
- [ ] `SYNTHESIS.md` written at the hub (fold location) with build/test/fmt/clippy verdicts, four-check results, diff manifest, PR URL, and PASS/FAIL prominent.

---

## Suggested Methodology Files

Matched Domain-Mapping row: **Synthesizing / verifying a hub-and-spoke decomposition → primary `synthesis`;
supporting `code-review`, `code-quality`**; plus **`testing`** to judge the integration suite's adequacy.

- `synthesis` — `synthesis/Synthesis_Overview_Methodology.md` (anchor — always; the four-check model + the structured `SYNTHESIS.md` schema + the PASS/FAIL gate decision), `synthesis/Synthesis_Contract_Verification_Methodology.md` (assert the contract identities), `synthesis/Synthesis_Wiring_Verification_Methodology.md` (no detached dead code; endpoints wired; repository used), `synthesis/Synthesis_Duplication_Detection_Methodology.md` (duplicated shared logic across spokes), `synthesis/Synthesis_Code_Review_Methodology.md` (review the combined diff), `synthesis/Synthesis_Remediation_Methodology.md` (remediation-as-decomposition on FAIL).
- `code-review` — `code-review/CodeReview_Checklist_Methodology.md` for the combined-diff review.
- `operations` — `operations/GitWorkflow_PR_Lifecycle_Methodology.md` for the push + `gh pr create` flow (load if you need the mechanics).

These are the parent's flagged methodologies; the gate posture (four-check + remediation) is mandatory, but how deeply
you run each check is your judgment — load fewer if a check is clearly inapplicable, more if the subtree reveals it.

## Inherited Constraints

- Run the authoritative checks from the ONE shared clone at the contract's `clone_path` — do NOT re-clone or reuse another process's clone.
- Report honestly: a clean FAIL with evidence beats a green-washed PASS. Do not modify the spokes' code to force a pass; schedule remediation instead.
- Never commit to / force-push `main`; the only write to `main` is via the PR. No commit-attribution trailers.
- `Closes #8` must end the PR body; PR title per the contract's `conventions.pr.title`.

## Out-of-Scope Methodologies

- Decomposition methodologies are decomposer-side only: a synthesis gate never loads `decomposition/` content — you are the reassembly, not the split (remediation, if needed, is a targeted Inject, not a re-plan of the whole subtree).
- Do NOT author new feature code yourself; if the work is incomplete, that is a FAIL + remediation, not a fix-in-the-gate.
