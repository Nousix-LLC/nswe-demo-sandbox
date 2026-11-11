# SUSPENSION — SUBTASK_release_and_distribution (NeedsDecompose)

**Task**: `SUBTASK_release_and_distribution` (concern 7 of the Ferric 1.0 framework design).
**Terminal state**: SUSPENDED · `decompose_evaluation = NeedsDecompose`.
**Resumption condition**: all child tasks below reach terminal lifecycle state; the synthesis child folds this
task `SUSPENDED → COMPLETED` via `engine_resume_suspended`, with `release-and-distribution.md` as the output.

## Why decomposed

The brief names three distinct concerns — crates.io **publishing** readiness + multi-crate release, the
**semver** contract + **changelog** practice, and the 1.0 **versioning & compatibility** policy. Applied at the
evaluation point against this actual brief:

- **Scope / Distinct-Concerns Test** — *fires*: three separable work items a build/release engineer, an
  API-stability lead, and a platform-stability lead could each own in parallel. The enumerated-concerns rule
  fires the scope trigger by the enumeration alone.
- **Single-Responsibility Test** — *fires*: three different kinds of analysis over different subject matter
  (crates.io mechanics; change classification + communication; stability promises).
- **Output Size** — *fires* (weakest): one consolidated doc estimated >400 lines.
- **Token** — clears.

Per Trigger Precedence the scope/concern signals win; the "one release engineer holds it whole" instinct carries
no weight at the evaluation point. Verdict: NeedsDecompose.

## Subtree materialized

Hub `_GLOBAL.md` and sub-contract `contracts/_MANIFEST.yaml` (partitions the `REQ-REL-*` number space so the
registers never collide) authored at this workspace. Children added via `engine_amend_plan { add_task }`:

| Child (task id) | Group | Owns | Output |
|---|---|---|---|
| `SUBTASK_publishing` | 0 | `REQ-REL-001..019` | `SUBTASK_publishing/publishing.md` |
| `SUBTASK_semver_changelog` | 0 | `REQ-REL-020..039` | `SUBTASK_semver_changelog/semver-changelog.md` |
| `SUBTASK_versioning_compat` | 0 | `REQ-REL-040..059` | `SUBTASK_versioning_compat/versioning-compat.md` |
| `SUBTASK_rel_synthesis` | 1 (deps: the three spokes) | merged register | `release-and-distribution.md` + `SYNTHESIS.md` |

The synthesis gate merges the three partials into the parent's declared output `release-and-distribution.md`,
asserts the merge identities J1–J7 (disjoint ranges, schema conformance, framework-appropriate verification,
all-concerns-covered, the MSRV + frozen-`prelude` 1.0 promise, peers named, placed-once in repo shape), and
folds this task to COMPLETED.

## Grounding carried into the subtree (baseline `276138f`)

- Virtual workspace, all Ferric crates `version.workspace = true` (0.1.0, edition 2021, MSRV 1.82); lints
  already enforce `missing_docs`.
- No `license`/`license-file` in any manifest and no top-level `LICENSE` (crates.io requires one) — the headline
  publishing gap. No `CHANGELOG.md`. No `keywords`/`categories`.
- `ferric-router` → `ferric` is a `{ path }` dependency with no version (blocks `cargo publish`).
- Frozen public surfaces are the `prelude` modules of `ferric`, `ferric-router`, `ferric-http` (enumerated in
  `_GLOBAL.md`).

## Note on methodology surface

The methodology loader was unavailable in this runtime (`agent_domain_unset`); the decomposition and briefs were
authored from release-engineering expertise directly, as the parent hub permits ("each child selects and loads
its own methodologies"). Each spoke brief directs the assigned agent to load its own release/semver methodology
if available.
