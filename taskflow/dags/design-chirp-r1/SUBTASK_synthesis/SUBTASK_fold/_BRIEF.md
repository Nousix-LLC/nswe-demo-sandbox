# Task: Fold the gate — join, verdict, remediation, and resolve the DAG root

## Task Specification
**Slug**: SUBTASK_fold
**Task Kind**: synthesis
**Depends on**: SUBTASK_identity_traceability, SUBTASK_live_measurement
**Status**: Pending

### Objective
Integrate the two analytical halves of the gate into the **DAG's root verdict** and resolve the decomposition:
join the live measurement into the traceability matrix, confirm every gap maps to a filed issue, author
**`design-chirp-r1/SYNTHESIS.md`** (the DAG's observation seam and fold record), remediate any **fixable**
design/backlog gap by decomposing a remediation subtree, and **fold** so the DAG root `design-chirp-r1` reaches
COMPLETED with that verdict as its seam.

### Context
Part of `SUBTASK_synthesis` (see `../_GLOBAL.md`, `../contracts/_MANIFEST.yaml`, and the inherited `../../contracts/`).
`SUBTASK_synthesis` is this DAG's designated **root-synthesis child**: the DAG root `design-chirp-r1` is SUSPENDED
(`NeedsDecompose`) awaiting a `SYNTHESIS.md` at its own workspace root that states the bar, indexes the issues by
epic, and gives the measured live-product standing (see the root's `SUSPENSION.md` and the `_FORK.md`
`observation_seam`, which is `design-chirp-r1/SYNTHESIS.md`). Because `SUBTASK_synthesis` itself decomposed, that
root fold falls to this node. The established in-DAG fold pattern is the sibling `SUBTASK_release_bar` /
`SUBTASK_bar_synthesis`: the nested synthesis authors the fold record at the fold location and resumes the suspended
ancestor via `engine_resume_suspended`.

**Dependencies**: `SUBTASK_identity_traceability` and `SUBTASK_live_measurement` are COMPLETED when this runs; read
their outputs directly.
**Dependents**: the DAG root `design-chirp-r1` (and, through it, the overseer that forked this DAG).

### Distinct concerns in this task (name-level — evaluate your own scope and decompose if warranted)
- **The join + gap confirmation** — derive each matrix row's `live_status` from its `bar_ids` per the sub-contract's
  `join_rule`; confirm `GAP_MAPPED` (every `missing`/`partial` `BAR-*` maps to ≥1 filed issue/epic) and that the eight
  inherited identities hold.
- **The verdict** — author `design-chirp-r1/SYNTHESIS.md`: the release bar (what releasable means), the filed issues
  indexed by epic, and the measured standing (met/partial/missing/not_applicable per the areas, each gap mapped to its
  covering epic/issue), with the headline `c805525` findings (e.g. the in-memory-store persistence blocker) stated
  plainly.
- **Remediation (conditional)** — if a **fixable** design/backlog gap is found (e.g. a `missing`/`partial` `BAR-*`
  with no covering issue, an uncovered gating `REQ-*`, an identity `FAIL`), remediate by **decomposing a remediation
  subtree** (author its hub + child briefs and materialize children) rather than failing the DAG or papering over it.
  If no fixable gap is found, record that and proceed to the fold.
- **The fold** — resolve the suspended ancestors so the DAG root `design-chirp-r1` reaches COMPLETED with
  `design-chirp-r1/SYNTHESIS.md` as its fold seam.

### Inputs
| Input | Source | Purpose |
|-------|--------|---------|
| Subtree hub + sub-contract | `../_GLOBAL.md`, `../contracts/_MANIFEST.yaml` | The join seam, column ownership, the gate identities |
| Inherited contract | `../../contracts/` | The eight identities; id/traceability schema; design-artifact map |
| Identity + matrix skeleton | `SUBTASK_identity_traceability/outputs/identity-and-traceability.md` | The eight verdicts + the matrix (all columns but `live_status`) |
| Live measurement | `SUBTASK_live_measurement/outputs/live-measurement.md` | Per-`BAR-*` `live_status` + observations to join |
| Release bar | `../../SUBTASK_release_bar/outputs/release-bar.md` | The bar to restate in the verdict |
| Backlog + trace map | `../../SUBTASK_delivery_backlog/outputs/backlog.md` | Issues/epics to index by epic and map gaps to |
| Root records | the DAG root `design-chirp-r1` workspace `SUSPENSION.md` and `_FORK.md` | The fold target, the observation seam, the expected verdict shape |

### Methodology
Apply the principal-product-designer persona and the relayed **Release Definition** guidance
(**CompletenessAndGapReview**, **ReleaseBar**); reach the software-domain **synthesis-gate** and
**remediation-decomposition** practice by prose. The `design` methodology loader is unavailable run-wide
(`agent_domain_unset`); record the limitation and proceed, as the siblings did. The fold is a verification gate, not
a prose summary: assert, measure, map every gap — no silent plug, no quiet pass.

### Output
- **`design-chirp-r1/SYNTHESIS.md`** — authored at the DAG root workspace (the fold location / `_FORK.md`
  observation seam). It is the DAG's verdict and fold record: the release bar; the filed issues indexed by epic; the
  measured live-product standing against the bar (met/partial/missing/not_applicable, each gap mapped to its covering
  epic/issue); and a note that any fixable gap has been remediated by a materialized subtree (or that none was found).
- Fold: resolve the suspended ancestors — flip `SUBTASK_synthesis` and then the DAG root `design-chirp-r1`
  SUSPENDED → COMPLETED with `design-chirp-r1/SYNTHESIS.md` as the seam — via `engine_resume_suspended`, per the
  kernel fold contract and the established sibling pattern. (Resolve the exact resume chain at runtime from the kernel
  contract and the ancestor records; the required end state is: the verdict exists at the observation seam and the
  DAG root is COMPLETED with it as seam.)

### Success criteria
- [ ] Every matrix row carries a joined `live_status` per the `join_rule`; the join is mechanical, not guessed.
- [ ] `GAP_MAPPED` holds — every `missing`/`partial` `BAR-*` maps to ≥1 filed issue/epic — and the eight inherited
      identities' verdicts are carried into the verdict; any `FAIL` is either remediated or reported, never plugged.
- [ ] `design-chirp-r1/SYNTHESIS.md` states the bar, indexes issues by epic, and gives the measured standing with
      each gap mapped to its covering epic/issue.
- [ ] Any fixable gap found is remediated by a decomposed remediation subtree, not by failing or papering over.
- [ ] The DAG root `design-chirp-r1` reaches COMPLETED with `design-chirp-r1/SYNTHESIS.md` as its fold seam.
- [ ] `design-chirp-r1/SYNTHESIS.md` carries no host/system/taskflow detail and no attribution trailer — repository
      identity only (`Nousix-LLC/nswe-demo`, commit SHA, repo-relative paths, `REQ-*`/`BAR-*`/`EPIC-*`/issue #).

### Constraints
- The verdict is the DAG's observation seam and is read by the overseer; keep it hygienic (no host/cluster address,
  no filesystem/taskflow path, no agent/DAG/run id, no `SYNTHESIS.md`/`SUSPENSION.md` location, no attribution).
- Do not edit completed sibling outputs; reconcile by remediation subtree, not in place.
- No product code.
