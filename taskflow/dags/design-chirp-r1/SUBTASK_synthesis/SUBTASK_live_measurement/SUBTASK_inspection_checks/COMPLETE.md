# COMPLETE — SUBTASK_inspection_checks

## What was done

Measured every release-bar criterion whose declared `verification_method` is `inspection` (35 criteria)
against `Nousix-LLC/nswe-demo` at commit `c805525`, by reading the declaring config/manifest/code artifact for
each and judging it `met | partial | missing | not_applicable` with a grounded observation. Read-only
repository inspection; no checkout mutated, no product code written.

## Output

- `outputs/inspection-measurement.md` — a verdict table conforming to `verdict_row_schema` (columns
  `bar_id`, `live_status`, `observation`), one row per `inspection` `BAR-*`, keyed by `bar_id`, preceded by a
  short access note.

## Result (35 criteria, each once)

- met (9): BAR-120, 160, 161, 162, 165, 167, 168, 174, 179 — the four-crate product partition over the
  `ferric` framework layer, the single `chirp-types` wire contract, the one `ChirpRepository` persistence
  seam, server-authoritative counts, env-driven config, and one self-contained serving artifact.
- partial (4): BAR-310 (token hygiene met, transport encryption omitted), BAR-339 (fields minimal, no stated
  mapping), BAR-463 (structured `tracing`, default text format not JSON), BAR-465 (no secrets in logs, but no
  audit trail / admin & recovery surfaces to complete the check).
- missing (22): BAR-021, 024, 175, 203, 275, 293, 294, 302, 311, 326, 331, 332, 408, 412, 421, 423, 424, 425,
  432, 481, 484, 486 — release-stage surfaces and stated/published postures (deletion/rules/export/operator/
  recovery, accessibility statement and records, backup/retention/RPO-RTO/restore, incident/status/availability,
  transport encryption) that are not stated or built at `c805525`.
- not_applicable (0).

## Grounding and scope

Two facts set the backdrop, recorded in the output's access note: the repository's `design/` tree is **empty**
at `c805525` (the refreshed design docs land only via the still-open PR `#122`), so "the product states X"
criteria were measured against the product's own shipped artifacts (code, README, `deploy/`), where those
postures are absent; and authentication at `c805525` is **handle-only** (`LoginRequest` carries just a
`username`; the repository doc states there is "no password/credential step"), with no recovery, deletion,
export, settings, reporting, or operator surface in the router.

Every observation cites the repo-relative artifact at `c805525` it rests on and the property read; `live_status`
values are from the inherited vocab and `bar_id`s are verbatim. The output references the product only by
repository identity, commit SHA, and repo-relative paths — no host/system/taskflow detail.

## Methodology note

The Phase-B `design`-domain methodology loader was unavailable run-wide (`agent_domain_unset`), as recorded in
`../_GLOBAL.md`; this partition was measured applying the principal-product-designer persona and the relayed
Release Definition / ReleaseBar guidance, which were sufficient. Recorded for transparency.
