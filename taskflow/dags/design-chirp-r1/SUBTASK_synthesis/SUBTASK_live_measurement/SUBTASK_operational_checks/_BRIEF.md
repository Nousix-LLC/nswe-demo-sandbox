# Task: Measure every operational_check BAR-* by observing running-service properties at c805525

## Task Specification
**Slug**: SUBTASK_operational_checks
**Task Kind**: standard
**Depends on**: none
**Status**: Pending

### Objective
Observe the running-service properties of the chirp deployment at commit `c805525`, and judge **every `BAR-*` whose
declared `verification_method` is `operational_check`** (68 criteria) as `met | partial | missing |
not_applicable`, each with a recorded observation — the running-service property observed and what was seen.

### Context
Part of `SUBTASK_live_measurement` (see `../_GLOBAL.md` and `../contracts/_MANIFEST.yaml`). This is the operational
partition: the `BAR-*` settled by observing a property of the running service rather than exercising a user journey,
running a test, or reading a static artifact — among them data **surviving a restart/redeploy** (the headline
`c805525` blocker: the in-memory store loses every account, chirp, follow, and like on restart), durable acknowledged
writes, authoritative state held in a store separate from the serving process, a readiness signal that reflects the
store, backup-and-restore, limit and quota enforcement (oversized bodies, unbounded list reads), and the
observability/incident/status operational surface. The other partitions are owned by siblings; measure only the
`operational_check` `BAR-*`, and every one of them.

The whole durable-persistence band turns on one observable fact — whether state survives a restart of the serving
process — so establishing that fact once settles many criteria together; confirm it by observation (post something,
cause/observe a restart or redeploy of the serving process within the project's own namespace, check whether it
survives) rather than assuming it, and record the single observation each dependent verdict rests on. These are
several distinct operational properties (durability, backup/restore, limits, readiness/liveness, observability,
incident/status); weigh them honestly in your own atomic-vs-decompose evaluation against the real shape of the work.

**Dependencies**: none. **Dependents**: `SUBTASK_measurement_fold`.

### Inputs
| Input | Source | Purpose |
|-------|--------|---------|
| Subtree hub | `../_GLOBAL.md` | Shared context, constraints, hygiene |
| Sub-contract | `../contracts/_MANIFEST.yaml` | Your owned partition (`operational_check`), the verdict-row schema, the `live_status` vocab |
| id/traceability schema | `../../../contracts/id_and_traceability_schema.yaml` | `live_status` + `verification_method` vocab (authoritative) |
| Release bar | `../../../SUBTASK_release_bar/outputs/release-bar.md` | The 278 `BAR-*`; filter to those tagged `operational_check` |
| Design PR record | `../../../SUBTASK_design_pr/outputs/design-pr.md` | Repo layout and branch context |
| Live deployment | ArgoCD app `chirp` @ `c805525` (reached per the project `CLAUDE.md` host notes) | Observe running-service properties read-only, within the project's own namespace |
| Repository @ `c805525` | `../../../SUBTASK_design_pr/repo` (or a fresh `gh repo clone Nousix-LLC/nswe-demo`, checked out at `c805525`) | Confirm the store/backup/limit/readiness design where a code/manifest artifact settles whether a running-service property can exist at all |

### How the live product is reached (environment facts — keep OUT of the output)
Reach the deployment per the project `CLAUDE.md` host notes, and act only within the project's own
namespace/application — observe read-only; do not disrupt or reconfigure the cluster beyond observing a
restart/redeploy of the project's own serving process. Those host facts are for running checks only and MUST NOT
appear in the output. If the deployment is genuinely unreachable from this environment, settle from the
store/backup/limit/readiness design at `c805525` whatever a code/manifest artifact can (e.g. an in-memory store in the
source is itself grounds for a `missing` restart-survival verdict), and record each remaining property that truly
needs a running observation as `missing`/`partial` with the reason — do not invent an observation.

### Methodology
Apply the principal-product-designer persona and the relayed **ReleaseBar** guidance. Match each `operational_check`
`BAR-*` to the running-service property it names and ground the verdict in an observation of the running service (or,
where unreachable, in the manifest/source property that determines whether the running behavior can hold), judging
conservatively. Record the shared observation (such as the restart-survival result) that a band of criteria rests on,
so each dependent verdict is traceable to a real observation rather than a repeated assumption.

### Output
- `outputs/operational-measurement.md` — a verdict table conforming to `verdict_row_schema` in the sub-contract: one
  row per `operational_check` `BAR-*` (`bar_id`, `live_status`, `observation`). A short access-note header records only
  *that* the running service was observed (or why not), by repository/commit identity — no host detail. Keyed by
  `bar_id`.

### Success criteria
- [ ] Every `BAR-*` tagged `operational_check` in the release bar has exactly one `live_status` and a grounded
      observation; none omitted, none of another method included.
- [ ] Each observation is grounded in an actual observation of the running service (or the determining manifest/source
      property at `c805525` where the service was unreachable) — never assumed or confabulated; unobservable criteria
      judged conservatively with the reason stated.
- [ ] `live_status` values from the inherited vocab; `bar_id`s verbatim.
- [ ] Read-only observation within the project's own namespace/application only; no host/system/taskflow detail in the
      output.

### Constraints
- Read-only on the live product and cluster; no product code; touch only the project's own namespace/application.
- Reference the product only by repository identity and commit SHA in the output.
