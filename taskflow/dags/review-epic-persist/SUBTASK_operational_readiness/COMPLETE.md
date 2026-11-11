# COMPLETE — SUBTASK_operational_readiness — PR #113 @ 09fa453

## What was done

Judged whether the store PR #113 provisions would be **safe and available in the running system**,
traced against `design/operational-readiness.md` (`REQ-OPS-*`) and ADR-0001. Examined the four
surfaces the brief named and produced one `outputs/findings.md` conforming to
`../contracts/finding_schema.md` (prefix `OPS`).

## Output

- `SUBTASK_operational_readiness/outputs/findings.md` — "What I checked" / "What I found clean" /
  four findings (OPS-01..OPS-04) / concern sub-verdict. All locations pin to `09fa453`.

## Sub-verdict

**NON-BLOCKING-ONLY.** No operational-readiness finding makes the store unsafe or unavailable on the
deployment target this PR ships for. The store is pod-independent and single-writer-safe, readiness
gates traffic on store health, the reclaim CronJob deletes exactly the transient tables it should
(SQL verified against migration 0002 and `sweep_expired_transient_state`), and capacity fails safe.

## Findings summary

| ID | Severity | Blocks | Area |
|----|----------|--------|------|
| OPS-01 | major | false | Default `local-path` storage is node-local; REQ-OPS-004 (cross-node reschedule) only partially met — disclosed, tied to #64 |
| OPS-02 | major | false | Reclaim CronJob restates the sweep's delete SQL (second source of truth; drift risk on schema growth) |
| OPS-03 | minor | false | A failing/skipped sweep is not observable (storage-leak-only; alerting deferred to observability) |
| OPS-04 | major | false | Activation is a manual un-gated digest pin (plus the out-of-band Secret); the PR body's "visibly not-ready rather than silently serving" overstates the post-merge state given `maxUnavailable: 0` |

## Notes for synthesis

- Supports **ID-64-OPEN**: this concern confirms #64's open framing is accurate — the running system
  becomes durable only after merge plus the digest pin *and* the out-of-band credential Secret. #64
  should not be closed by this PR.
- No blocker from this concern; the sub-verdict does not gate landing on its own. The required
  `doc`-check / mergeable-and-clean gating is the CI-doc-diagnosis concern's and the synthesis gate's
  to carry.
- An in-cluster plaintext DB connection (`PGSSLMODE: disable`) was observed in the CronJob and the
  credential model; it is a trust-boundary matter left to the security concern, not raised here.
- `findings.md` and this record carry no host/cluster/SSH/credential or taskflow-internal detail;
  all citations are repo-relative paths, lines, issues, and design refs.
