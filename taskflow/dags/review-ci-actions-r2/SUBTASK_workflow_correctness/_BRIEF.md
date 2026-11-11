# Task: Review CI workflow correctness & reproducibility (PR #21, concerns 1+2)

## Task Specification

**Slug**: SUBTASK_workflow_correctness
**Task Kind**: standard
**Status**: Pending

### Objective

Review `.github/workflows/ci.yml` (new, ~194 lines) at PR head `c8123376` and judge two concerns —
**CI workflow correctness** and **reproducibility / pinning** — emitting findings in the frozen
findings schema. You are a reviewer: read-only, push nothing, change nothing.

### Context

Part of the review DAG for PR #21 (see `../_GLOBAL.md`). The code DAG already folded
**machine-PASS** at head (fmt/clippy/test/doc/wasm/actionlint green); rely on that — do not re-run
the full build. You MAY spot-check (`actionlint`, YAML validity, reading `ci.yml`) to substantiate
findings.

**Dependencies**: none. **Dependents**: `SUBTASK_synthesis`.

## What to evaluate (name distinct sub-concerns; judge each block/major/minor/nit)

**Concern 1 — CI workflow correctness:**
- Do the five PR/push jobs (`fmt`, `clippy`, `test`, `wasm`, `doc`) actually run the stated commands
  (`cargo fmt --check`, `cargo clippy -D warnings`, `cargo test`, WASM frontend build, doc build)?
- Are triggers correct (PR + push to `main`)?
- Do job names stay stable enough to serve as required checks?
- Is the matrix/caching sound, and is `--locked` used consistently?

**Concern 2 — reproducibility / pinning:**
- Toolchain pin (`dtolnay/rust-toolchain@1.97`), `wasm-bindgen-cli` pinned to the locked `0.2.129`,
  `--locked` cargo, `Swatinem/rust-cache@v2` cache-key correctness (keys on `Cargo.lock` + rustc).
- Flag any drift risk (version float, cache poisoning / stale-cache correctness, lockfile skew).

(Workflow **security / least-privilege / supply-chain** — `permissions`, token scoping, action
tag-vs-SHA pinning — is a *different spoke* (`SUBTASK_supply_chain_security`); do not re-adjudicate
it here. Note a cross-reference if correctness and security interact, but leave the security verdict
to that spoke.)

## Input Specification

| Input | Source | Purpose |
|-------|--------|---------|
| Shared facts & evidence-access commands | `../_GLOBAL.md` | Repo, PR, head SHA, machine-gate posture, `gh` access patterns |
| Findings schema (frozen) | `../contracts/findings_schema.md` | Record shape + severity enum you MUST emit in |
| Ownership (your id prefix `WF-`) | `../contracts/_MANIFEST.yaml` | Your output path and finding-id prefix |
| `ci.yml` at head | `gh api repos/Nousix-LLC/nswe-demo/contents/.github/workflows/ci.yml?ref=c8123376 -q .content \| base64 -d` | The workflow under review |
| PR diff / metadata | `gh pr diff 21 --repo Nousix-LLC/nswe-demo`, `gh pr view 21 ...` | Confirm job names, triggers, file set |

## Output Specification

| Attribute | Value |
|-----------|-------|
| Filename | `findings.md` (in this workspace) |
| Format | Per `../contracts/findings_schema.md` (header stating head `c8123376`; findings table with `WF-` ids; concern-coverage note for concerns 1 & 2; roll-up counts) |

## Success Criteria

- [ ] `ci.yml` read at head `c8123376`; concerns 1 and 2 both covered with a coverage note each.
- [ ] Every finding conforms to the schema (id `WF-n`, severity in enum, location `ci.yml:line`/job, rationale; `required_change` on every block/major).
- [ ] Drift/caching risks evaluated explicitly (even if the conclusion is "sound").
- [ ] `findings.md` states the PR head reviewed and a block/major/minor/nit roll-up ("no findings" stated explicitly if clean).

## Suggested Methodology Files

Parent's Domain-Mapping reading: closest rows are **"Code review"** (primary: Code Review;
supporting: Core, Testing) and **"CI/CD setup"** (primary: Operations; supporting: Security). For a
*review of a CI workflow* the parent flags:

- `code-review/CodeReview_Checklist_Methodology.md` — systematic review coverage so no job/trigger/cache aspect is missed.
- `code-review/CodeReview_Feedback_Guidelines_Methodology.md` — severity calibration and actionable required-change wording.
- `operations/DevTools_CICD_Methodology.md` — what a correct CI pipeline must do; required-check stability; cache correctness.
- `operations/DevTools_Build_Systems_Methodology.md` — build/caching determinism and reproducibility judgment.

Load via `engine_load_methodology { name: "code-review" }` and `{ name: "operations" }`, then
reference the files above. **These are suggestions, not an exclusive list** — load fewer if clearly
inapplicable; load more if your reading of `ci.yml` reveals additional methodology surface.

## Inherited Constraints

- **Read-only review (P1): touch no code, push nothing.** No `gh pr merge`, no `gh pr review --approve`, no branch writes. `gh` read/GET and local `actionlint`/YAML checks only.
- **Rely on machine-PASS**; do not re-run fmt/clippy/test/wasm. Spot-checks substantiate, they do not re-litigate the machine gate.
- **Emit in the frozen findings schema** (`../contracts/findings_schema.md`); do not invent your own format. Request an additive amendment if the schema is inadequate.
- Severity semantics are the contract's: `block`/`major` force REQUEST-CHANGES; `minor`/`nit` are advisory.

## Out-of-Scope Methodologies

- Decomposition (`decomposition/`) and Synthesis (`synthesis/`) bundles are decomposer/gate-side — not for this spoke.
- Workflow security/supply-chain methodology belongs to `SUBTASK_supply_chain_security`; container/image methodology belongs to `SUBTASK_image_job`.
