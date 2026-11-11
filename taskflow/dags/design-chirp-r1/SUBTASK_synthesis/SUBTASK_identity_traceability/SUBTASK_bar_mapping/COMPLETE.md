# COMPLETE — SUBTASK_bar_mapping

## What this task was
Map every release-bar criterion (`BAR-*`) to the requirements (`REQ-*`) it enforces, produce the
inverted `REQ → bar_ids` map the traceability matrix needs, and assert the `BAR_TESTABLE` identity
with recorded evidence. Single source: `design/release-bar.md` (`Nousix-LLC/nswe-demo` @ `c805525`),
read-only. Ownership (per `../contracts/_MANIFEST.yaml`): the `bar_ids` column (as the `REQ → bar_ids`
map) and the `BAR_TESTABLE` identity — and nothing else.

## Decompose evaluation
Atomic. One read→process→write cycle over one source region; the per-`BAR-*` table, its inversion, and
the `BAR_TESTABLE` property-check are facets of one parse, not distinct concerns. Token/scope/
single-responsibility/owl triggers all clear; the only borderline signal was output size (one ~480-line
mechanical table), which Trigger Precedence subordinates for a single-source tabular extraction.

## What was produced
`outputs/bar-mapping.md` — the declared output — containing:
1. **Per-`BAR-*` table** (278 criteria, id order): `bar_id`, `stage`, `verification_method`, referenced
   `REQ-*` (verbatim from each criterion's authoritative `_Enforces …_` clause).
2. **Inverted `REQ → bar_ids` map**: 343 distinct `REQ-*` keys, each with its enforcing `bar_ids`,
   keyed by `req_id` for the synthesis join.
3. **`BAR_TESTABLE` verdict**: **PASS**, with evidence.

## Findings
- **278 `BAR-*` found** (the bar's own area table totals 278; the hub's working estimate of 279 was one
  high — the actual parsed count is 278). Stage split 148 `usable_early` / 130 `releasable`.
- **Per-area stage counts match the bar's own published table exactly** (Product 14/21, Domain 50/10,
  Experience 51/43, Identity 18/22, Ops 15/34) — the cross-check evidence that every criterion was
  captured with the right stage.
- **343 distinct `REQ-*`** are referenced by at least one `BAR-*`.
- **`BAR_TESTABLE` = PASS.** Every one of the 278 criteria names a verification method from the closed
  vocabulary (`manual_user_check`, `automated_test`, `inspection`, `operational_check`) and references
  ≥1 `REQ-*`; 0 offenders, 0 parse problems, 0 out-of-vocabulary stages. A method or stage outside the
  inherited vocabulary would have been reported as a failure, not normalised; none was found.

## How it was verified (reproducible)
Parsed with an authored script (`scripts/parse_bar.py`, `scripts/render_deliverable.py`) over the
`_Enforces …_` clauses; the deliverable was generated to `scripts/bar-mapping.staging.md` and the
named-state output authored via `engine_write`, then confirmed **byte-identical** by `diff`. Row counts
confirmed (278 table / 343 inversion). Hygiene scan confirmed no host/workspace/taskflow path, process
id, or attribution trailer in the deliverable.

## Boundaries honored
Owns only `bar_ids` + `BAR_TESTABLE`; did not assert other identities, build other matrix columns, edit
the completed bar, or touch the live product. The `design` methodology loader was unavailable run-wide
(`agent_domain_unset`); proceeded under the principal-product-designer persona and the relayed
release-definition guidance per the subtree hub, and recorded the limitation in the deliverable.

## Output
- `outputs/bar-mapping.md`
