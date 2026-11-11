# COMPLETE — SUBTASK_design_req_and_64

## What was done

Reviewed, read-only, whether PR #113 @ `09fa453` satisfies the design's durable-persistence requirement and
the applicable `BAR-*` / `REQ-*`, and whether the PR's "#64 stays open" framing is an accurate account of what
the change does and does not make durable. No repository or GitHub writes; #64 neither closed nor filed as
backlog.

## Evidence traced

- `design/domain-application-design.md` §3 `persistence_requirement` — REQ-DOM-012, REQ-DOM-013, REQ-DOM-014.
- `design/release-bar.md` §E — BAR-019 (`operational_check`, `usable_early`) and its reference set
  (REQ-PROD-026, REQ-DOM-012/013, REQ-OPS-001/002/003/004/006/007); BAR-020/021/022 cross-checked for the
  closes/open split.
- `design/operational-readiness.md` §`durable_data` — REQ-OPS-001..007 acceptance criteria and verification
  methods.
- Issue #64 and epic #56 (`Nousix-LLC/nswe-demo`).
- PR #113 description and `deploy/chirp/10-deployment.yaml` @ 09fa453 (placeholder image digest,
  `CHIRP_DATABASE_URL` injection, `/readyz` readiness gating).

## Result

- **#64 framing: ACCURATE.** BAR-019 and its reference set are verified against the running deployment; the
  change delivers the store, seam wiring, and drill, but the running system becomes durable only after merge
  plus the follow-up digest-pin (and the out-of-band Secret). #64 is confirmed correctly open.
- **One finding, COR-60 (minor, non-blocking):** the PR's "what remains / one follow-up" wording understates
  the activation sequence (merge/reconcile → Secret present → digest-pin, with a deliberate not-ready window
  between merge and the digest-pin). Reinforces #64-open; does not dispute it.
- **Overlaps recorded** for the per-criterion areas (#65/#66/#67) and the root operational-readiness,
  architecture-contract, durability-proof, and CI-doc concerns, left for synthesis to de-duplicate.
- **Area sub-verdict: NON-BLOCKING-ONLY.**

## Output

- `SUBTASK_design_req_and_64/outputs/findings.md` — conforms to `../../contracts/finding_schema.md`; finding
  id COR-60 within the assigned `COR-60 .. COR-79` range.
