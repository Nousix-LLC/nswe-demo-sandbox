# _GLOBAL.md — Review DAG hub: ci-actions PR #21 (issue #11), re-fork r2

## Project Context

**Status**: Active (decomposed into 4 review spokes + 1 synthesis gate)

### Objective

Produce an **authoritative landing verdict** (`APPROVE` or `REQUEST-CHANGES`) on **PR #21 —
"CI: GitHub Actions for the Rust/WASM workspace (#11)"** in `Nousix-LLC/nswe-demo`, reviewed at
head **`c8123376`** (`c8123376ca1794c0b0466f41a1204bf3c3301b16`). The verdict is the body of a
root `SYNTHESIS.md` at this DAG's workspace root — the overseer gates on that body.

This is a **review**, not an authoring task. No spoke may push to the branch, merge, rewrite the
PR, or touch repository code. Spokes produce findings; the synthesis gate renders the verdict;
the overseer lands.

### Why this is a re-fork (r2)

The first review DAG (`review-ci-actions`) was lost to a whole-OS reconstruction before producing
a root `SYNTHESIS.md` verdict. There is **no verdict on record** for PR #21; nothing was landed on
its strength. `main` is unchanged at `61f924a`. This DAG re-does the review from the current head.

### Scope

**In scope** — six concerns from the root `_BRIEF.md`, partitioned across spokes (see Task
Structure). Each finding is judged `block` / `major` / `minor` / `nit`.

**Out of scope** — re-running the full build (the code DAG already folded **machine-PASS**:
fmt/clippy/test/doc/wasm/actionlint green at head — rely on it); posting a GitHub review
(self-review is platform-blocked and non-authoritative); any write to the repo or branch.

### Success Criteria

- [ ] All six concerns covered across the four spokes; each finding carries severity + file:line + rationale.
- [ ] Acceptance-criteria mapping (issue #11) rendered pass/fail per criterion at the gate.
- [ ] Root `SYNTHESIS.md` carries an explicit `APPROVE` / `REQUEST-CHANGES` verdict, confirms head `c8123376`, and reports block/major/minor/nit counts.
- [ ] Verdict rule honored: `APPROVE` iff 0 block AND 0 major; otherwise `REQUEST-CHANGES` with the specific changes required.

---

## Shared Review Facts (constant across the subtree)

| Fact | Value |
|------|-------|
| Repo | `Nousix-LLC/nswe-demo` |
| PR | #21 — "CI: GitHub Actions for the Rust/WASM workspace (#11)" |
| PR head reviewed | `c8123376` (`c8123376ca1794c0b0466f41a1204bf3c3301b16`) |
| Base | `main` at `61f924a` |
| PR state at dispatch | OPEN / MERGEABLE / CLEAN |
| Diff size | 22 files, +286 / −92 |
| Machine gate | already folded **machine-PASS** at head (do not re-run the full build; spot-checks allowed) |
| #12 containerize | **merged to `main` (`61f924a`)** — a real `./Dockerfile` now exists on `main` |
| Issue #11 acceptance | `ci.yml` runs on PR + push to `main`: `cargo fmt --check`, `cargo clippy -D warnings`, `cargo test`, build WASM frontend, and (on `main`) build+push chirp-server image to GHCR; cache cargo/target; required-check friendly; delivered as a PR into `main` |

### Evidence access (every spoke; read-only)

`gh` is authenticated (account `mattsmcknight`, scopes incl. `repo`, `workflow`) and PR #21 is
reachable. This workspace is **not** a local checkout; gather evidence via `gh` (read-only — no
`gh pr merge`, no `gh pr review --approve`, no push):

- PR diff: `gh pr diff 21 --repo Nousix-LLC/nswe-demo`
- PR metadata / files / checks: `gh pr view 21 --repo Nousix-LLC/nswe-demo --json ...`
- File at the PR head: `gh api repos/Nousix-LLC/nswe-demo/contents/.github/workflows/ci.yml?ref=c8123376 -q .content | base64 -d`
- File on `main`: `gh api repos/Nousix-LLC/nswe-demo/contents/Dockerfile?ref=61f924a -q .content | base64 -d`
- Issue #11: `gh issue view 11 --repo Nousix-LLC/nswe-demo`
- Optional spot-checks: `actionlint` on the fetched `ci.yml`, YAML validity — substantiate findings, do not re-run CI.

---

## Methodology

Each spoke selects and loads its own methodology bundles (IDs suggested in each `_BRIEF.md`). This
is a review engagement; the dominant task type is **code review**, specialized per concern
(CI/workflow, supply-chain security, container/image, doc-only change verification) and closed by a
**synthesis verification gate**.

---

## Task Structure

### Overview

```
_GLOBAL.md (this hub)
├── contracts/
│   ├── _MANIFEST.yaml              (taxonomy kind; per-spoke ownership; identities)
│   └── findings_schema.md          (severity enum + finding-record schema + verdict rule)
├── SUBTASK_workflow_correctness/_BRIEF.md   (concerns 1+2)
├── SUBTASK_supply_chain_security/_BRIEF.md  (concern 3)
├── SUBTASK_image_job/_BRIEF.md              (concern 4 — most important newly-relevant)
├── SUBTASK_folded_minors/_BRIEF.md          (concern 5)
└── SUBTASK_synthesis/_BRIEF.md              (concern 6 + fold → root SYNTHESIS.md verdict)
```

### Task Summary

| Task id | Depends on | Description | Output |
|---------|------------|-------------|--------|
| `SUBTASK_workflow_correctness` | none | Concerns 1+2: CI workflow correctness (jobs, triggers, required-check-stable names, matrix/caching, `--locked`) and reproducibility/pinning (`dtolnay/rust-toolchain@1.97`, `wasm-bindgen-cli` 0.2.129, `Swatinem/rust-cache@v2` key correctness, drift risk). | `SUBTASK_workflow_correctness/findings.md` |
| `SUBTASK_supply_chain_security` | none | Concern 3: workflow security / least-privilege / supply-chain — top-level `permissions: contents: read`, `image` job `packages: write` scoping, `GITHUB_TOKEN`-only secrets, third-party actions pinned by tag vs commit SHA (supply-chain exposure; tracked as issue #24). | `SUBTASK_supply_chain_security/findings.md` |
| `SUBTASK_image_job` | none | Concern 4: the `image` job now that #12's `./Dockerfile` exists on `main` — build context, image name/tag, GHCR auth via `GITHUB_TOKEN`, digest/push correctness, and whether the "skip when Dockerfile missing" logic is now dead or could misfire. Call out any block/major explicitly. | `SUBTASK_image_job/findings.md` |
| `SUBTASK_folded_minors` | none | Concern 5: folded #8-review minors — confirm the ~79 rustdoc intra-doc-link fixes are doc/comment-only (no runtime behavior change), verify the chirp-server README validation-error correction (422→400 / `VALIDATION_ERROR`) is accurate, judge whether folding these into a CI PR is acceptable scope. | `SUBTASK_folded_minors/findings.md` |
| `SUBTASK_synthesis` | `SUBTASK_workflow_correctness`, `SUBTASK_supply_chain_security`, `SUBTASK_image_job`, `SUBTASK_folded_minors` | Concern 6 + fold: verification gate — assert every spoke emitted conformant findings, de-duplicate overlapping findings, map every issue-#11 acceptance criterion to evidence (pass/fail), aggregate block/major/minor/nit counts, apply the verdict rule, and author the root `SYNTHESIS.md`. | `../review-ci-actions-r2/SYNTHESIS.md` (DAG root; the overseer's observation seam) |

### Dependency Graph

```
SUBTASK_workflow_correctness  ──┐
SUBTASK_supply_chain_security ──┤
SUBTASK_image_job             ──┼──▶ SUBTASK_synthesis ──▶ SYNTHESIS.md (verdict)
SUBTASK_folded_minors         ──┘
```

---

## Contract

**Contract location**: `contracts/` (read-only for every descendant)
**Contract kind**: `taxonomy`

### Why a contract here

The four spokes are parts of ONE review; their findings must recompose into one verdict. The seam
is the **findings format + severity taxonomy**: unless every spoke emits findings in an identical
record shape with an identical severity vocabulary, the synthesis gate cannot mechanically
aggregate block/major/minor/nit counts or apply the verdict rule. This seam's shape is *forced* by
the root `_BRIEF.md` output spec (stable) and is membership-checkable (assertable) → **frozen** as a
`taxonomy` contract. The seam is cheap to declare now and unbounded to reconcile later.

### Structural Declarations

| Artifact | Kind | Declares |
|---|---|---|
| `contracts/findings_schema.md` | taxonomy | Severity enum (`block`/`major`/`minor`/`nit`), the per-finding record fields, the finding-id prefix per spoke, and the verdict rule the gate asserts. |
| `contracts/_MANIFEST.yaml` | taxonomy manifest | Kind, per-spoke ownership of findings files + id-prefix, synthesis ownership of `SYNTHESIS.md`, and the cross-output identities. |

### Ownership

| Artifact | Owning subtask |
|---|---|
| `SUBTASK_workflow_correctness/findings.md` (id prefix `WF-`) | `SUBTASK_workflow_correctness` |
| `SUBTASK_supply_chain_security/findings.md` (id prefix `SEC-`) | `SUBTASK_supply_chain_security` |
| `SUBTASK_image_job/findings.md` (id prefix `IMG-`) | `SUBTASK_image_job` |
| `SUBTASK_folded_minors/findings.md` (id prefix `DOC-`) | `SUBTASK_folded_minors` |
| `SYNTHESIS.md` (DAG root) | `SUBTASK_synthesis` |

### Identities (asserted by the synthesis gate; no silent plugs)

- [ ] Every spoke produced its `findings.md` and it conforms to `contracts/findings_schema.md`.
- [ ] Every finding's `severity` ∈ {`block`, `major`, `minor`, `nit`}; every finding carries a location and a rationale; every `block`/`major` carries a `required_change`.
- [ ] Every spoke reviewed PR head `c8123376` (stated in its findings file).
- [ ] Verdict rule holds: `APPROVE` iff aggregate `block` count == 0 AND aggregate `major` count == 0; otherwise `REQUEST-CHANGES`.
- [ ] Every issue-#11 acceptance criterion maps to pass/fail evidence drawn from the spoke findings; no criterion unaddressed.
- [ ] Each of the six brief concerns is covered by exactly one spoke's scope (no concern dropped, none double-owned).

### Derived Artifacts

None generated automatically (thin taxonomy seam). The synthesis gate consumes the four real
findings files directly (serialized dependency), using `findings_schema.md` as the conformance
reference.

### Suggestion, not prescription

Each spoke's `_BRIEF.md` names suggested methodology bundles; spokes retain final judgment over what
they load. The contract (findings schema + severity taxonomy) is **binding** — it is the seam, not a
suggestion.
