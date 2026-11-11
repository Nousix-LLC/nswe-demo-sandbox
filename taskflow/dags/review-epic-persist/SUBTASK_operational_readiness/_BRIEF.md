# Task: Operational readiness — PR #113

## Task Specification

**Slug**: SUBTASK_operational_readiness
**Task Kind**: standard
**Status**: Pending

### Objective

Judge whether the provisioned store would be safe and available in the running system, traced against the
operational-readiness design of record.

### Context

Part of the PR #113 review DAG (see `../_GLOBAL.md`). You MAY inspect live cluster state read-only (via the
sandbox's SSH `kubectl` form; those are host facts, never surfaced on GitHub). Read-only on the repo; write a
findings document only.

## Inputs

| Input | Source | Purpose |
|---|---|---|
| Subtree hub | `../_GLOBAL.md` | Pinned commit, target, constraints |
| Contract | `../contracts/finding_schema.md`, `../contracts/_MANIFEST.yaml` | Findings format + rubric |
| PR #113 diff @ `09fa453` | `gh pr diff 113` / `git` (read-only) | Manifests, probes, CronJob, image wiring |
| Design | `design/operational-readiness.md`, `design/release-bar.md` | The ops bar to trace to |
| Live cluster (optional, read-only) | SSH `kubectl --context k3d-nswe -n chirp…` per `CLAUDE.md` | Confirm live state vs manifests; never surfaced on GitHub |

## The bar (what blocks)

An operational gap that would make the store **unsafe or unavailable** in the running system is a finding.
Examine at least:

- Provisioning soundness: single-primary StatefulSet + per-ordinal PVC + headless Service; volume headroom
  and the documented growth assumption.
- Readiness gating on `/readyz` / store health (does traffic get gated until the store is actually ready?).
- The reclaim CronJob (schedule, scope, failure behavior).
- The **digest-pin follow-up** the PR names as the one step to activate the durable image — is that framing
  accurate, and is the `image` check skipping consistent with it?

## Output

`SUBTASK_operational_readiness/outputs/findings.md`, conforming to `../contracts/finding_schema.md` (prefix
`OPS`).

## Success criteria

- [ ] Provisioning, readiness gating, reclaim job, and digest-pin follow-up assessed and traced to
  `design/operational-readiness.md`.
- [ ] "What I checked" / "what I found clean" both specific.
- [ ] Findings pinned (to the diff; cluster observations referenced without host detail), severities +
  `blocks_landing` honest, each with "what would satisfy me"; sub-verdict.

## Constraints

Read-only on the repo; no GitHub writes. Cluster inspection is read-only and its host/address/SSH detail
MUST NOT appear in the findings or anywhere repo-reader-facing. No DAG internals. Plain voice.
