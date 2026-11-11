# Task: durable-persistence design requirement + applicable BAR-*/REQ- + the #64 "stays open" framing

## Task Specification

**Slug**: SUBTASK_design_req_and_64
**Task Kind**: standard
**Status**: Pending

### Objective

Judge whether PR #113 actually satisfies the design's **durable-persistence requirement** and any applicable
`BAR-*` / `REQ-*` from the release bar — and whether the PR's claim that **#64 "stays open"** is an accurate
account of what the change does and does not make durable.

### Context

This is one area spoke of the `SUBTASK_correctness` subtree (see `../_GLOBAL.md` for the pinned target, the
inherited constraints, and the finding taxonomy). Read-only review; you write one findings document only.
Your area is the design-of-record trace plus the #64 framing. A change that passes its tests but misses a
`BAR-*` the design requires is a finding. Where your reading touches the per-criterion areas (#65/#66/#67) or
the root-level operational-readiness concern, record your finding and note the overlap for synthesis.

**Do not close #64 and do not file it as backlog** — your job is only to confirm or dispute that its "stays
open" framing is accurate.

## Inputs

| Input | Source | Purpose |
|---|---|---|
| Subtree hub | `../_GLOBAL.md` | Pinned commit, target, constraints, overlap policy |
| Root hub | `../../_GLOBAL.md` | The review DAG's pinned target and shared constraints |
| Contract | `../contracts/_MANIFEST.yaml`, `../../contracts/finding_schema.md` | The findings format, severity rubric, and your `COR-60 .. COR-79` id range |
| PR #113 diff + description @ `09fa453c3c40e39a9b4647e0de6e00dcf50ecb21` | `gh pr diff 113` / `gh pr view 113` / `git` (read-only) | The change and the PR's own account of #64 |
| Design of record | `design/domain-application-design.md`, `design/release-bar.md` (read on `main`) | Durable-persistence requirement + applicable `BAR-*` / `REQ-*` |
| Issue #64 | `gh issue view 64` on `Nousix-LLC/nswe-demo` | What #64 actually claims is still open |

## The bar (what blocks)

- A `BAR-*` / `REQ-*` or the durable-persistence requirement that the design requires and the change does not
  deliver (even if tests pass) is a **blocking** finding.
- If the PR's "#64 stays open" framing is **inaccurate** — e.g. the running system is already durable (so #64
  should not stay open), or the PR actually leaves more undone than it admits — that is a finding against the
  framing, pinned to the PR description / the relevant code and the design.
- If the framing is **accurate** (store, wiring, and drill delivered; the running system becomes durable only
  after merge plus the follow-up digest-pin), say so explicitly in "what I found clean" and confirm #64 is
  correctly left open — without closing it or filing it as backlog.

## Output

`SUBTASK_design_req_and_64/outputs/findings.md`, conforming to `../../contracts/finding_schema.md`, finding
ids in range `COR-60 .. COR-79`.

## Success criteria

- [ ] The durable-persistence requirement and each applicable `BAR-*` / `REQ-*` traced, with "what I checked"
  enumerated.
- [ ] The #64 framing explicitly judged accurate or inaccurate, with the evidence; #64 NOT closed, NOT filed
  as backlog.
- [ ] "What I found clean" states specifically what was examined and judged sound.
- [ ] Every finding pinned to `09fa453…` or explicitly design-level/whole-PR with rationale; severity +
  `blocks_landing` set honestly; each with a concrete "what would satisfy me"; `confidence` set verified vs
  suspected.
- [ ] An area sub-verdict (CLEAN / NON-BLOCKING-ONLY / HAS-BLOCKERS).

## Constraints

Read-only on the repo; no GitHub writes (do not comment on, close, or re-label #64). No
host/cluster/SSH/credential details or DAG internals in the findings. Plain voice.
