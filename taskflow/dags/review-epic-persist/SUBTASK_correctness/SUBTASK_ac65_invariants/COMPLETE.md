# COMPLETE — SUBTASK_ac65_invariants

## Task
Judge whether PR `Nousix-LLC/nswe-demo#113` @ `09fa453c3c40e39a9b4647e0de6e00dcf50ecb21` makes
acceptance criterion **#65** hold in the durable store — domain invariants, derived counts, opaque
monotonic ids **under concurrency** — and whether that is *proved* by the change or merely asserted.
Read-only review of the #65 area only.

## Output produced
- `SUBTASK_ac65_invariants/outputs/findings.md` — conforms to `../../contracts/finding_schema.md`;
  finding ids `COR-01 .. COR-04` (within the assigned `COR-01 .. COR-19` range). Sections: What I
  checked / What I found clean / Findings / Concern sub-verdict.

## Area sub-verdict: HAS-BLOCKERS
- **COR-01 (blocker, verified)** — #65's durable-store concurrency invariant tests
  (`concurrency_invariants.rs` durable half) execute in no CI gate: the `test` job runs
  `cargo test --workspace` with no `postgres` feature, no Postgres service, and no
  `CHIRP_TEST_DATABASE_URL`, so the durable suite is not compiled there and every durable test skips
  otherwise. #65's "under concurrency" guarantee is asserted, not proved.
- **COR-02 (major, suspected)** — `delete_account` reconcile-then-cascade can drift a surviving
  neighbour's denormalized count against a concurrent edge insert on the victim under READ COMMITTED;
  untested interleaving. Blocker-class if confirmed; reproducer named.
- **COR-03 (major, suspected)** — `bump_follow_counts` locks follower-then-followee, so reciprocal
  concurrent follows deadlock (`40P01`), surfaced as `Internal`; a valid op fails spuriously. Canonical
  lock order would fix it.
- **COR-04 (minor, verified)** — the "ids stable across restart" clause is tested only via a fresh
  connection pool, not an actual restart; the restart proof belongs to the durability drill.

## What was found clean
Id mechanism (durable sequences: monotonic, unique, never-reused, allocated in-transaction); counts
maintained in lockstep with edges inside one transaction with correct idempotent edge ops; handle
uniqueness via the unique index → `Conflict` (no TOCTOU); exactly-once reverse-chronological cursor
paging; domain-boundary validation through `chirp-types` value objects with in-store `CHECK` backstops.

## Overlaps recorded (left for synthesis, not reconciled here)
- COR-01 / COR-04 overlap root `SUBTASK_durability_proof` (general test depth, the drill) and
  `SUBTASK_ci_doc_diagnosis` (CI health).
- COR-03 overlaps `SUBTASK_code_quality` (lock-ordering idiom) and `SUBTASK_architecture_contract`
  (seam concurrency-safety).
- #64 not in this area's scope; not touched, not closed, not filed.

## Constraints honored
Read-only on the repo and GitHub (no writes). Every finding pinned to `09fa453`. No host/cluster/SSH/
credential details or DAG internals in the findings doc. Plain-voice finishing pass run over the
output.

## Note
Phase B methodology loader reported `agent_domain_unset` in this deployment; the methodology surface
was not resolvable via syscall. Review conducted against the self-contained brief and inherited
contracts.
