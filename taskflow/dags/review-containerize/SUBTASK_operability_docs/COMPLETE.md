# COMPLETE — SUBTASK_operability_docs

**Task**: Render an operator's judgment over PR #22's operability (concern 4) and the
documentation-match-behavior slice of concern 6; emit `findings.md` in the contract shape.

**Status**: COMPLETED (Atomic).

## What was done

Reviewed, read-only, the operability-facing surface of PR #22 (head `bc0c3c0d…`) — the
`Dockerfile` `HEALTHCHECK`/`ENV`/`ENTRYPOINT`, `deploy/docker/healthcheck.rs` (behavior only),
`deploy/README.md`, and the `README.md` "Running chirp in a container" section — and cross-checked
every documented command / env var / port / default against the diff and the authoritative machine
gate (`taskflow/dags/containerize/SYNTHESIS.md`). The container build was NOT re-run.

## Result (summary)

- **Concern 4 — operability: PASS-WITH-NOTES.** HEALTHCHECK exec-form genuinely exercises `/healthz`;
  one-knob port derivation (probe ↔ server via `CHIRP_BIND_ADDR`) is real and correct; config vars
  externalized + documented; stdout/stderr logging; out-of-box serve on in-memory default. One nit.
- **Concern 6 (docs slice) — docs-match-behavior: PASS-WITH-NOTES.** Both docs are clear and
  **factually match** the diff on every operator-facing command/env/port/default (the `/healthz` JSON
  is byte-identical to the machine gate; HEALTHCHECK params exact). No doc claims a flag the image does
  not honor. Two concrete minor inaccuracies remain.

## Findings emitted (per `contracts/findings_schema.md`)

- `OPS-1` (concern 6, **minor**) — docs say the probe is "compiled with `rustc -O`"; Dockerfile uses
  `rustc -C opt-level=z -C strip=symbols`. Internal build-detail mismatch; fix the prose.
- `OPS-2` (concern 6, **minor**) — `deploy/README.md` defers the image size to the out-of-repo
  `SYNTHESIS.md`; state "≈42 MB" inline so a repo reader sees the documented size.
- `OPS-3` (concern 4, **nit**) — probe hardcodes `127.0.0.1`; correct for the `0.0.0.0` default,
  robustness observation only, no code change warranted.

**No `block`, no `major`** — honoring severity discipline (I4): no operator-facing behavior is
misstated. On the contract's verdict rule (I3), this spoke contributes zero blocking findings.

## Outputs

- `SUBTASK_operability_docs/findings.md` — concern dispositions + severity-tagged findings table.

## Contract compliance

- Shape conforms exactly to `contracts/findings_schema.md`.
- I2 seam honored: Rust idiom → rustcode_sigterm; size/repro → dockerfile_build; security → security_supplychain (cross-referenced, not re-filed).
- I5 read-only honored: no edit/stage/commit/push/merge; nothing posted to GitHub; no rebuild.
- Concern 4 and the concern-6 docs slice each carry an explicit disposition; one-knob derivation explicitly judged; docs-match-behavior checked concretely; every block/major (none) would carry location + remediation.
