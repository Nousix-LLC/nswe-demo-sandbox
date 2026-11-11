# SYNTHESIS — SUBTASK_correctness — PR #113 @ 09fa453

Fold record for the `SUBTASK_correctness` subtree: how the four per-area reviews were verified against the
subtree contract and consolidated into one concern deliverable, and the fold that resolves the suspended
`SUBTASK_correctness` parent.

## What was folded

| Area (spoke) | Acceptance criterion / requirement | Finding-id range | Area sub-verdict | Findings |
|---|---|---|---|---|
| `SUBTASK_ac65_invariants` | #65 — invariants / counts / opaque-id monotonicity under concurrency | COR-01..19 | HAS-BLOCKERS | COR-01 (blocker), COR-02, COR-03 (major), COR-04 (minor) |
| `SUBTASK_ac66_seam_migration` | #66 — seam fidelity, single-writer, migration/versioning | COR-20..39 | NON-BLOCKING-ONLY | COR-20 (major), COR-21, COR-22, COR-23 (minor) |
| `SUBTASK_ac67_retention_failclosed` | #67 — retention/capacity + fail-closed write | COR-40..59 | NON-BLOCKING-ONLY | COR-40 (major), COR-41 (minor), COR-42, COR-43 (nit), COR-44 (minor) |
| `SUBTASK_design_req_and_64` | durable-persistence requirement + #64 framing | COR-60..79 | NON-BLOCKING-ONLY | COR-60 (minor) |

Consolidated into `SUBTASK_correctness/outputs/findings.md` (14 findings, one blocker). No area was missing or
malformed; nothing was silently plugged.

## Contract identities asserted (no silent plugs)

Against `contracts/_MANIFEST.yaml` plus the inherited root identities:

- **COR-ID-COVERAGE** — PASS. Each of #65, #66, #67 and the durable-persistence requirement is traced by
  exactly one spoke, each stating both "What I checked" and "What I found clean".
- **COR-ID-UNIQUE** — PASS. Every `COR-NN` id is unique in the consolidated document; each spoke stayed inside
  its assigned range (01–19 / 20–39 / 40–59 / 60–79). No collision.
- **COR-ID-PROVED** — PASS (and it is what drives the verdict). #65 distinguishes what the change proves from
  what it merely asserts and makes the unproven under-concurrency guarantee a blocker (COR-01), rather than
  passing it.
- **COR-ID-OVERLAP** — PASS. Overlaps with the architecture/contract-stability and durability-proof concerns
  (and the CI doc-check, operational-readiness, security, and code-quality concerns) are recorded on the
  findings they bear on and left for the root synthesis to de-duplicate — not dropped, not reconciled here.
- **ID-64-OPEN** — PASS. #64 is noted and its open framing confirmed accurate; it is neither closed nor filed
  as backlog.
- **COR-ID-SUBVERDICT** — PASS. One area carries `blocks_landing: true` (COR-01), so the consolidated concern
  sub-verdict is **HAS-BLOCKERS**; the gate did not plug the failing area.
- **ID-SCHEMA / ID-PIN / ID-SEVERITY / ID-ACTIONABLE** — PASS. Every finding conforms to `finding_schema.md`,
  pins to `09fa453` (or is marked whole-PR/design-level with rationale), carries a severity with
  `blocks_landing` matching the `blocker` ⟺ true rule, and names a concrete "what would satisfy me".
- **ID-NO-HOST / ID-PLAIN-VOICE** — PASS. The consolidated deliverable carries no host/SSH/cluster/credential
  details and no DAG internals (sibling task slugs were rephrased to concern subjects); the avoid-ai-writing
  finishing pass was run over the prose before writing.

## De-duplication performed at this gate

- COR-01 (#65) and COR-44 (#67), with #66's proof-in-CI overlap note, were identified as one underlying
  mechanism — the durable test suite is feature-gated (off by default) and skips without
  `CHIRP_TEST_DATABASE_URL`, and CI runs neither — seen from two acceptance-criterion angles. Both numbered
  findings are retained (each is its area's distinct bar and the ids must be preserved); the shared pattern is
  named in the consolidated document so the root synthesis de-duplicates it once against the durability-proof
  and CI concerns rather than counting three independent gaps.
- COR-20's stale seam rustdoc is connected to the failing required `doc` CI check for the root CI doc-check
  concern, without being claimed as a correctness-area blocker.

## Concern sub-verdict

**HAS-BLOCKERS** — COR-01: #65's central guarantee (invariants, derived counts, opaque monotonic ids under
concurrency, proved not asserted) is not proved, because the durable-store concurrency suite executes in no
automated gate. The store implementation is otherwise sound for its acceptance bars; the blocker is a proof gap
in the CI gate, and two suspected #65 concurrency hazards (COR-02, COR-03) would each be blocker-class for #65
if confirmed and are currently uncovered.

## Fold

- Declared output produced: `SUBTASK_correctness/outputs/findings.md`.
- This record (`SUBTASK_correctness/SYNTHESIS.md`) is authored at the fold location — the suspended
  `SUBTASK_correctness` parent's directory — and is the seam the fold consumes to flip
  `SUBTASK_correctness` SUSPENDED → COMPLETED, so the root review DAG can consume the one consolidated
  correctness findings document.
