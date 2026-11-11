# Correctness concern subtree — PR #113 (#65/#66/#67 + durable-persistence requirement)

## Project Context

**Status**: Active

### Objective

Judge whether PR `Nousix-LLC/nswe-demo#113` at commit `09fa453c3c40e39a9b4647e0de6e00dcf50ecb21`
actually delivers the behavior that acceptance criteria **#65**, **#66**, **#67** and the design's
**durable-persistence requirement** specify — behavior, not assertion. This subtree is the decomposition of
the `SUBTASK_correctness` concern of the PR #113 review DAG. It produces ONE consolidated
`SUBTASK_correctness/outputs/findings.md` (prefix `COR`) conforming to the inherited finding schema, folded
from four per-area reviews plus a synthesis gate.

This subtree reads and judges. It does **not** modify the repository, push, merge, fix, or perform any GitHub
write. Every finding pins its location to commit `09fa453c3c40e39a9b4647e0de6e00dcf50ecb21`.

### Why this concern decomposed

The `SUBTASK_correctness` brief enumerates four distinct requirement areas and instructs the agent to "treat
them as the distinct areas they are when you size your own work." Each area is a separate acceptance criterion
or design requirement, each with its own "proved, not asserted" bar, traced against different parts of an
+11,851/−77 / 28-file change. The scope trigger and the Distinct Concerns Test fire by that enumeration; a
single invocation tracing all four against the full diff, three issues, and three design docs would exceed the
atomic envelope. The areas overlap on the same durable-store code — that overlap is recorded by each spoke and
de-duplicated at synthesis, not used as grounds to keep the work whole.

### Inherited target (pinned) — from the root hub

| Field | Value |
|---|---|
| PR | `Nousix-LLC/nswe-demo#113` |
| Pinned head commit | `09fa453c3c40e39a9b4647e0de6e00dcf50ecb21` |
| Head → base | `work/epic-persist` → `main` |
| Closes | #65, #66, #67 (children of epic #56); #64 stays open by the PR's own account |

### The acceptance criteria / requirement areas (one per spoke)

- **#65** — domain invariants, derived counts (follower/following/like counts), and opaque monotonic ids hold
  in the durable store **under concurrency**. Must be *proved*, not asserted.
- **#66** — durable storage plugs into the **`ChirpRepository` seam** soundly: full capability set behind the
  existing seam, single-writer safety, schema versioned and applied by a migration runner; no capability
  dropped or weakened. (Behavioral correctness here; contract-stability *shape* is owned by the root-level
  `SUBTASK_architecture_contract` — record overlaps, let synthesis de-dup.)
- **#67** — retention/capacity commitments honoured (documented lifetimes for transient state, the reclaim
  job, no-automatic-expiry for user content) and the **fail-closed-on-non-durable-write** rule. (Proof-depth
  of the durability *drill* is owned by the root-level `SUBTASK_durability_proof` — this spoke judges the
  retention/fail-closed *behavior*, records overlaps, lets synthesis de-dup.)
- **durable-persistence design requirement + #64** — the design's durable-persistence requirement and any
  applicable `BAR-*` / `REQ-*` traced against the change; and whether the PR's "#64 stays open" framing is
  accurate (confirm or dispute; **do not close #64, do not file it as backlog**).

## Constraints (bind every task in this subtree)

- Repo scope: `Nousix-LLC/nswe-demo` only. **Read-only on the code and on GitHub** — review, do not modify,
  push, merge, or fix. **No GitHub writes from any task in this subtree** (the only GitHub writes in the whole
  review DAG belong to the root `SUBTASK_synthesis`).
- **No host/system details anywhere in a findings doc** that will be surfaced to repo readers: no server
  addresses, SSH key paths, usernames, host filesystem paths, cluster/Tailscale addresses, or taskflow/DAG
  internals. Point at repo files/lines, issues, and design paths only.
- **Plain voice.** All prose is held to the plain-voice / avoid-ai-writing bar: no "honest"/"genuine"/"real"
  moral adjectives glued to things that cannot hold them, no narrated candor, no template filler, no inflated
  seamless/robust/comprehensive/leverage. Judge by cluster and density; run the finishing pass before writing
  the output.
- Every finding pins to commit `09fa453c3c40e39a9b4647e0de6e00dcf50ecb21` (repo file + line range), OR is an
  explicit whole-PR / design-level finding with its rationale stated.
- Severity is honest: `blocker` ⟺ `blocks_landing: true`; a blocker is never downgraded to backlog and a
  preference is never inflated to a blocker. "I would have done it differently" is not a finding on its own.

## Task Structure

### Overview

```
SUBTASK_correctness/
├── _GLOBAL.md (this hub)
├── contracts/
│   └── _MANIFEST.yaml                         (sub-contract: extends the root finding taxonomy — COR id ranges, ownership, identities)
├── SUBTASK_ac65_invariants/_BRIEF.md          (#65 — invariants, derived counts, opaque-id monotonicity, under concurrency)
├── SUBTASK_ac66_seam_migration/_BRIEF.md      (#66 — seam fidelity, single-writer safety, migration/versioning)
├── SUBTASK_ac67_retention_failclosed/_BRIEF.md (#67 — retention/capacity + fail-closed-on-non-durable-write)
├── SUBTASK_design_req_and_64/_BRIEF.md        (durable-persistence design requirement + BAR-*/REQ-* + #64 framing)
└── SUBTASK_synthesis/_BRIEF.md                (Task Kind: synthesis — fold the four areas into outputs/findings.md)
```

### Task Summary

| Task id | Depends on | Description | Output |
|---------|------------|-------------|--------|
| `SUBTASK_ac65_invariants` | none | #65: domain invariants, derived counts, opaque-id monotonicity hold in the durable store under concurrency — proved, not asserted | `SUBTASK_ac65_invariants/outputs/findings.md` |
| `SUBTASK_ac66_seam_migration` | none | #66: full capability set behind the `ChirpRepository` seam, single-writer safety, schema versioned + applied by a migration runner; no capability dropped/weakened | `SUBTASK_ac66_seam_migration/outputs/findings.md` |
| `SUBTASK_ac67_retention_failclosed` | none | #67: retention/capacity commitments (lifetimes, reclaim job, no-auto-expiry for user content) + fail-closed-on-non-durable-write | `SUBTASK_ac67_retention_failclosed/outputs/findings.md` |
| `SUBTASK_design_req_and_64` | none | Durable-persistence design requirement + applicable BAR-*/REQ- traced; #64 "stays open" framing confirmed or disputed (not closed, not backlog) | `SUBTASK_design_req_and_64/outputs/findings.md` |
| `SUBTASK_synthesis` | `SUBTASK_ac65_invariants`, `SUBTASK_ac66_seam_migration`, `SUBTASK_ac67_retention_failclosed`, `SUBTASK_design_req_and_64` | Fold the four per-area findings into ONE `outputs/findings.md` conforming to `finding_schema.md`; de-duplicate overlaps; render the concern sub-verdict | `SUBTASK_correctness/outputs/findings.md` (+ `SUBTASK_correctness/SYNTHESIS.md` fold record) |

### Dependency Graph

```
SUBTASK_ac65_invariants            ──┐
SUBTASK_ac66_seam_migration        ──┤
SUBTASK_ac67_retention_failclosed  ──├── SUBTASK_synthesis
SUBTASK_design_req_and_64          ──┘
```

## Contract

**Contract location**: `contracts/` (read-only for every descendant)
**Contract kind**: `taxonomy` (sub-contract extending the root review DAG's finding taxonomy)

### Inherited Contracts

| Ancestor contract | Path | What it binds here |
|---|---|---|
| Finding schema | `../contracts/finding_schema.md` | The per-concern `findings.md` document structure, the per-finding field set, the severity rubric, the `file:line @ 09fa453` citation format, the `COR` prefix, and the concern sub-verdict vocabulary. Every spoke here composes against this; this sub-contract MUST NOT override it. |
| Review taxonomy manifest | `../contracts/_MANIFEST.yaml` | Pinned commit, severity rubric, and the cross-cutting review identities (ID-SCHEMA, ID-PIN, ID-SEVERITY, ID-ACTIONABLE, ID-64-OPEN, ID-NO-HOST, ID-PLAIN-VOICE). |

### Structural Declarations

Each area spoke emits one `outputs/findings.md` conforming to the inherited `finding_schema.md`, covering its
one area. The synthesis gate consolidates the four into a single `SUBTASK_correctness/outputs/findings.md`
(same schema, one "What I checked" / "What I found clean" / "Findings" / "Concern sub-verdict" document that
covers all four areas). Finding-ID ranges are partitioned so the consolidated document has no `COR-NN`
collision.

### Ownership

| Artifact | Owning subtask | Finding-ID range |
|---|---|---|
| `SUBTASK_ac65_invariants/outputs/findings.md` | `SUBTASK_ac65_invariants` | `COR-01` … `COR-19` |
| `SUBTASK_ac66_seam_migration/outputs/findings.md` | `SUBTASK_ac66_seam_migration` | `COR-20` … `COR-39` |
| `SUBTASK_ac67_retention_failclosed/outputs/findings.md` | `SUBTASK_ac67_retention_failclosed` | `COR-40` … `COR-59` |
| `SUBTASK_design_req_and_64/outputs/findings.md` | `SUBTASK_design_req_and_64` | `COR-60` … `COR-79` |
| `SUBTASK_correctness/outputs/findings.md`, `SUBTASK_correctness/SYNTHESIS.md` | `SUBTASK_synthesis` | — (consolidation; preserves each area's IDs) |

### Identities (evaluated by the synthesis gate; no silent plugs)

- [ ] Each of #65, #66, #67 and the durable-persistence requirement is traced by exactly one spoke, which
  states BOTH "what I checked" and "what I found clean" for its area.
- [ ] Every finding conforms to `finding_schema.md`: pinned to `09fa453…` (or explicit whole-PR/design-level
  with rationale), carries a severity and an explicit `blocks_landing` boolean, and names a concrete "what
  would satisfy me".
- [ ] `COR-NN` ids are unique across the consolidated document (the per-spoke ranges above do not collide).
- [ ] Overlaps with the root-level `SUBTASK_architecture_contract` (seam shape) and `SUBTASK_durability_proof`
  (drill/test depth) are recorded as findings where they bear on correctness and left for the root synthesis
  to de-duplicate — not dropped, not reconciled here beyond noting the overlap.
- [ ] #64 is noted (its open framing confirmed or disputed) but NOT closed and NOT filed as backlog.
- [ ] The consolidated concern sub-verdict is `HAS-BLOCKERS` iff any area carries a `blocks_landing: true`
  finding; `NON-BLOCKING-ONLY` iff findings exist but none block; `CLEAN` iff no findings.
- [ ] No findings-doc content carries host paths, cluster/SSH/credential details, or DAG internals; all prose
  passes the plain-voice bar.

### Derived Artifacts

None auto-generated. The synthesis task consumes the four area `findings.md` files directly.

### Thin-Seam Note

The seam is thin and inherited: the four spokes already share the root's finding taxonomy, so this
sub-contract adds only (a) the `COR-NN` id-range partition that keeps the consolidated document collision-free
and (b) the consolidation identities the synthesis gate asserts. Small is correct here; absent would defer the
id-collision and sub-verdict-aggregation questions to synthesis.

## Output Specifications

| Deliverable | Format | Location | Description |
|---|---|---|---|
| Per-area findings | Markdown | `SUBTASK_<area>/outputs/findings.md` | One per area spoke, conforming to `finding_schema.md` |
| Consolidated concern findings | Markdown | `SUBTASK_correctness/outputs/findings.md` | The single deliverable the root DAG consumes: all four areas, what-checked / what-clean / findings / concern sub-verdict |
| Fold record | Markdown | `SUBTASK_correctness/SYNTHESIS.md` | The synthesis task's terminal + fold record |
