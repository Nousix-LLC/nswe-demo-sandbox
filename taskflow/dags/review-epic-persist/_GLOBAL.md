# Review DAG — PR #113 "Durable PostgreSQL persistence for chirp"

## Project Context

**Status**: Active

### Objective

Render the authoritative human-landing verdict — **APPROVE** or **REQUEST-CHANGES** — on
`Nousix-LLC/nswe-demo#113`, held issue-by-issue to the acceptance criteria of #65/#66/#67 and traced to the
product's design of record. The review reads and judges; it does **not** modify the repository, push, merge,
or fix anything. The verdict is folded into this DAG's root `SYNTHESIS.md`; the overseer gates on that folded
record.

### The target (pinned)

| Field | Value |
|---|---|
| PR | `Nousix-LLC/nswe-demo#113` |
| Title | Durable PostgreSQL persistence for chirp: provision, wire, and prove durability |
| Head branch → base | `work/epic-persist` → `main` |
| **Pinned head commit** | **`09fa453c3c40e39a9b4647e0de6e00dcf50ecb21`** |
| Author | `mattsmcknight` (owner-authored; NOT produced by a code DAG) |
| Size | +11,851 / −77 across 28 files |
| State | OPEN, not draft; `MERGEABLE`, mergeStateStatus `UNSTABLE` |
| Closes | #65, #66, #67 (children of epic #56); #64 stays open |

**Every finding across the whole subtree pins its location to commit
`09fa453c3c40e39a9b4647e0de6e00dcf50ecb21`** so inline comments and the verdict all reference one commit.

### What it closes — the acceptance criteria to hold it to

Read each issue on GitHub and trace the change against its own acceptance criteria:

- **#65** — domain invariants, derived counts (follower/following/like counts), and opaque monotonic ids
  hold in the durable store **under concurrency**. Must be *proved*, not asserted.
- **#66** — durable storage plugs into the **`ChirpRepository` seam** soundly: full capability set behind the
  existing seam, single-writer safety, schema versioned and applied by a migration runner. No capability
  dropped or weakened.
- **#67** — retention/capacity commitments honoured (documented lifetimes for transient state, the reclaim
  job, no-automatic-expiry for user content, fail-closed on a non-durable write) and durability proven by a
  **repeatable, stranger-runnable drill** (restart, redeploy, reschedule).
- **#64 stays open by the PR's own account** — store, wiring, and drill delivered, but the *running system*
  becomes durable only after merge plus a follow-up digest-pin. Confirm the framing is accurate; note, do not
  close, #64. Do not file it as backlog.

### The design of record (read on `main`)

- `design/domain-application-design.md` — carries the durable-persistence requirement.
- `design/release-bar.md` — the release bar (`BAR-*` / `REQ-*`).
- `design/operational-readiness.md` — provisioning / ops half of this change.

A change that passes its tests but misses a `BAR-*` the design requires is a finding.

### The machine signal

This PR is owner-authored, so there is **no code-DAG `SYNTHESIS.md`** for it. The machine signal is the live
CI rollup on PR #113: `clippy` PASS, `fmt` PASS, `test` PASS, `wasm` PASS, `image` skipping, **`doc` FAILING**
→ merge state `UNSTABLE`. `doc` is a required check: **the PR is not clean to land while it fails.** Even an
otherwise-clean review APPROVE must state landing is gated on `doc` going green and the PR being mergeable and
clean.

---

## Constraints (bind every task in this subtree)

- Repo scope: `Nousix-LLC/nswe-demo` only. **Read-only on the code** — review, do not modify, push, merge, or
  fix. The ONLY GitHub writes in this whole subtree are performed by `SUBTASK_synthesis`: posting the review
  (comment + inline comments) and filing backlog issues. Concern spokes perform **no** GitHub writes.
- **No host/system details anywhere on GitHub.** No server addresses, SSH key paths, usernames, host
  filesystem paths, cluster/Tailscale addresses, or taskflow/DAG internals in any posted review, comment,
  filed issue, or in `SYNTHESIS.md` content intended for repo readers. Point at repo files/lines and design
  paths only.
- **No attribution trailers** on anything posted to GitHub (no "Generated with…", no "Co-Authored-By").
- Live cluster state may be inspected read-only for the operational-readiness concern via the sandbox's SSH
  form (host facts only; never surfaced on GitHub).
- **Plain voice.** All prose that ships (the review, inline comments, filed issues, `SYNTHESIS.md`) is held to
  the plain-voice bar: no "honest"/"genuine"/"real" moral adjectives glued to things that cannot hold them,
  no narrated candor, no template filler, no inflated adjectives (seamless/robust/comprehensive/leverage). Run
  the avoid-ai-writing finishing pass before posting.

---

## Task Structure

### Overview

```
_GLOBAL.md (this hub)
├── contracts/
│   ├── _MANIFEST.yaml          (taxonomy: finding schema, severity rubric, ownership, identities)
│   └── finding_schema.md       (the per-concern findings-doc structure every spoke emits)
├── SUBTASK_correctness/_BRIEF.md
├── SUBTASK_durability_proof/_BRIEF.md
├── SUBTASK_code_quality/_BRIEF.md
├── SUBTASK_architecture_contract/_BRIEF.md
├── SUBTASK_security/_BRIEF.md
├── SUBTASK_operational_readiness/_BRIEF.md
├── SUBTASK_ci_doc_diagnosis/_BRIEF.md
└── SUBTASK_synthesis/_BRIEF.md (Task Kind: synthesis — the gate)
```

Each concern spoke reads PR #113 at the pinned commit through ONE concern lens and writes one
`outputs/findings.md` conforming to the contract. The synthesis task depends on all seven, folds them into one
verdict, authors the root `SYNTHESIS.md`, posts the review on the PR, and files non-blocking findings as
backlog issues.

### Task Summary

| Task id | Depends on | Description | Output |
|---------|------------|-------------|--------|
| `SUBTASK_correctness` | none | Does the change actually deliver #65/#66/#67 + the durable-persistence requirement — invariants, derived counts, opaque-id monotonicity, concurrency/single-writer, migration/versioning, fail-closed-on-non-durable-write, seam fidelity | `SUBTASK_correctness/outputs/findings.md` |
| `SUBTASK_durability_proof` | none | Do the tests + drill prove each criterion and the failure paths (restart/redeploy/reschedule; concurrency; non-durable write); real surviving-state assertions vs vacuous; stranger-runnable drill; `postgres` feature gating | `SUBTASK_durability_proof/outputs/findings.md` |
| `SUBTASK_code_quality` | none | Code quality, design, and Rust idiom across the store backend, the `ChirpRepository` seam, and the wiring: responsibilities/coupling, abstraction boundaries, duplication, naming, error handling, ownership/borrowing, async, feature-gating hygiene | `SUBTASK_code_quality/outputs/findings.md` |
| `SUBTASK_architecture_contract` | none | Seam contract stability (`ChirpRepository`) + deployment-contract coherence (manifests, ArgoCD AppProject, probes → `/readyz`); additive AppProject changes (StatefulSet, PVC, CronJob) correct and minimal | `SUBTASK_architecture_contract/outputs/findings.md` |
| `SUBTASK_security` | none | Credential handling for `CHIRP_DATABASE_URL`, SQL/injection & input handling at the store boundary, migration safety, Pod Security `restricted` admission, dependency/feature pull-ins | `SUBTASK_security/outputs/findings.md` |
| `SUBTASK_operational_readiness` | none | Provisioning soundness (single-primary StatefulSet + per-ordinal PVC + headless Service; volume headroom), readiness gating on `/readyz`/store health, reclaim CronJob, digest-pin follow-up; traced to `design/operational-readiness.md` | `SUBTASK_operational_readiness/outputs/findings.md` |
| `SUBTASK_ci_doc_diagnosis` | none | Diagnose the failing required `doc` CI job on PR #113 (read the job log), name the change that greens it, record as a blocker to landing | `SUBTASK_ci_doc_diagnosis/outputs/findings.md` |
| `SUBTASK_synthesis` | `SUBTASK_correctness`, `SUBTASK_durability_proof`, `SUBTASK_code_quality`, `SUBTASK_architecture_contract`, `SUBTASK_security`, `SUBTASK_operational_readiness`, `SUBTASK_ci_doc_diagnosis` | Fold all findings into ONE APPROVE/REQUEST-CHANGES verdict; author root `SYNTHESIS.md`; post the review on PR #113 (comment + inline); file non-blocking findings as backlog issues | `SYNTHESIS.md` |

### Dependency Graph

```
SUBTASK_correctness            ──┐
SUBTASK_durability_proof       ──┤
SUBTASK_code_quality           ──┤
SUBTASK_architecture_contract  ──├── SUBTASK_synthesis
SUBTASK_security               ──┤
SUBTASK_operational_readiness  ──┤
SUBTASK_ci_doc_diagnosis       ──┘
```

---

## Contract

**Contract location**: `contracts/` (read-only for every descendant)
**Contract kind**: `taxonomy` (code-review finding taxonomy + citation format + severity rubric + per-concern
ownership)

### Inherited Contracts

None — this is the root decomposition of the review DAG.

### Structural Declarations

| Artifact | Kind | Declares |
|---|---|---|
| `contracts/finding_schema.md` | taxonomy | The per-concern `findings.md` document structure, the per-finding field set, the severity rubric, the location/citation format (repo-relative path + line range @ pinned commit), and the concern sub-verdict vocabulary that every spoke emits and the synthesis task folds |
| `contracts/_MANIFEST.yaml` | taxonomy | kind, per-task ownership, the cross-cutting identities, and derived artifacts |

### Ownership

| Artifact | Owning subtask |
|---|---|
| `SUBTASK_correctness/outputs/findings.md` | `SUBTASK_correctness` |
| `SUBTASK_durability_proof/outputs/findings.md` | `SUBTASK_durability_proof` |
| `SUBTASK_code_quality/outputs/findings.md` | `SUBTASK_code_quality` |
| `SUBTASK_architecture_contract/outputs/findings.md` | `SUBTASK_architecture_contract` |
| `SUBTASK_security/outputs/findings.md` | `SUBTASK_security` |
| `SUBTASK_operational_readiness/outputs/findings.md` | `SUBTASK_operational_readiness` |
| `SUBTASK_ci_doc_diagnosis/outputs/findings.md` | `SUBTASK_ci_doc_diagnosis` |
| `SYNTHESIS.md`, the posted PR review + inline comments, the filed backlog issues | `SUBTASK_synthesis` |

### Identities (evaluated by the synthesis gate; no silent plugs)

- [ ] Every concern spoke produced a `findings.md` conforming to `finding_schema.md` and listing BOTH what it
  checked and what it found clean.
- [ ] Every finding pins a location to commit `09fa453c3c40e39a9b4647e0de6e00dcf50ecb21` (repo file + line
  range), OR is explicitly a whole-PR / design-level finding with its rationale stated.
- [ ] Every finding carries a severity and an explicit `blocks_landing` boolean; the severity rubric in
  `finding_schema.md` is applied honestly (a blocker is never downgraded to backlog; a preference is never
  inflated to blocker).
- [ ] The failing required `doc` check is represented as a blocker: the verdict MUST state landing is gated on
  `doc` going green and the PR being mergeable and clean, even if every code concern is otherwise clean.
- [ ] The verdict is **REQUEST-CHANGES if any concern carries a `blocks_landing: true` finding**, otherwise
  **APPROVE** with the explicit doc-gate / mergeable-and-clean note.
- [ ] Blocking findings are named in the verdict as what must change before landing; they are **NOT** filed as
  backlog. Non-blocking findings ARE filed as backlog, grouped, de-duplicated against existing issues, each
  linked to PR #113 and to epic #56 / the originating issue.
- [ ] No posted artifact (review, inline comment, filed issue) and no repo-reader-facing `SYNTHESIS.md`
  content contains host paths, cluster/SSH/credential details, or taskflow/DAG internals.
- [ ] All shipped prose passes the plain-voice / avoid-ai-writing bar.

### Derived Artifacts

None auto-generated. The synthesis task consumes the seven `findings.md` files directly.

### Thin-Seam Note

The seam here is the finding taxonomy: without it, seven reviewers would each invent their own findings format
and severity language, and the synthesis task would reconcile them retroactively while rendering a verdict. The
contract fixes that format before any spoke runs.

---

## Output Specifications

| Deliverable | Format | Location | Description |
|---|---|---|---|
| Per-concern findings | Markdown | `SUBTASK_<concern>/outputs/findings.md` | One per spoke, conforming to `finding_schema.md` |
| Root verdict | Markdown | `SYNTHESIS.md` (this workspace root — the fold location / observation seam) | APPROVE/REQUEST-CHANGES, findings grouped per concern with severity + blocks, what-checked/what-clean per concern |
| Posted PR review | GitHub | PR #113 | Comment carrying the verdict + inline/line comments for specific findings |
| Backlog issues | GitHub | repo issues | Non-blocking findings, grouped/de-duplicated, linked to #113 and epic #56 |
