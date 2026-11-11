# Task: Measure the live product at c805525 against every BAR-*

## Task Specification
**Slug**: SUBTASK_live_measurement
**Task Kind**: standard
**Depends on**: none
**Status**: Pending

### Objective
Exercise the **deployed chirp product at commit `c805525`** as a user would, and inspect the repository at that
commit, to judge **every `BAR-*`** in the release bar as `met | partial | missing | not_applicable`, each with a
**recorded observation** — what was done and what was seen — so the gate measures the product rather than assuming
its state.

### Context
Part of `SUBTASK_synthesis` (the DAG's verification gate + fold; see `../_GLOBAL.md` and `../contracts/_MANIFEST.yaml`).
This is the **empirical** half of the gate. It runs in parallel with the internal-consistency sibling
(`SUBTASK_identity_traceability`) and is joined by `SUBTASK_fold`. The headline known fact to confirm, not assume:
the product at `c805525` uses an **in-memory store** that loses all accounts, chirps, follows, and likes on restart —
the release's named blocker — so the whole durable-persistence band of the bar turns on one observable fact.

**Dependencies**: none within this subtree. Inputs below are COMPLETED sibling tasks; read their outputs directly.
**Dependents**: `SUBTASK_fold`.

### Distinct concerns in this task (name-level — evaluate your own scope and decompose if warranted)
The bar is **278 `BAR-*` across five areas** verified by four methods — `manual_user_check` (exercise the running
product), `automated_test` (a repo test asserts it), `inspection` (read a declared property from config/manifest/code),
`operational_check` (observe a running-service property such as survival across restart). Judge your own
atomic-vs-decompose evaluation honestly against the real shape of the work — e.g. the natural cuts are by **area**
(Product 35, Domain 60, Experience 94, Identity 40, Operational 49) and/or by **verification method** (the live
user-journey sweep vs. the repository-inspection sweep vs. the restart/operational checks). Many criteria collapse
onto shared observable facts (the in-memory store resolves the whole persistence band together; the absent
release-layer account-lifecycle surfaces resolve together), but confirming each still requires a real observation,
not a confabulated one.

### How the live product is reached (environment facts — keep OUT of any GitHub/verdict content)
The deployment is reached per the project `CLAUDE.md` host notes (the cluster runs on a build server reached over
SSH; the app is served by the k3d load balancer; ArgoCD app `chirp`, Synced+Healthy at `c805525`, `/healthz`→200).
Use those facts only to run checks. If the live deployment is genuinely unreachable from this environment, fall back
to repository inspection at `c805525` for every criterion that a code/config artifact can settle, and record each
remaining `operational_check`/`manual_user_check` as `missing`/`partial` with the reason it could not be observed —
do not invent an observation.

### Inputs
| Input | Source | Purpose |
|-------|--------|---------|
| Subtree hub | `../_GLOBAL.md` | Shared context, constraints |
| Inherited + sub contract | `../../contracts/`, `../contracts/_MANIFEST.yaml` | `live_status` vocab; your owned per-`BAR-*` verdict table |
| Release bar | `../../SUBTASK_release_bar/outputs/release-bar.md` | The 278 `BAR-*`, each with its statement and verification method |
| Design PR record | `../../SUBTASK_design_pr/outputs/design-pr.md` | The repo `design/` map and branch, for context |
| Repository @ `c805525` | cloned under `../../SUBTASK_design_pr/repo` (or a fresh `gh repo clone Nousix-LLC/nswe-demo` into this workspace) | Inspect code/config/manifests + run/read tests for `inspection` / `automated_test` criteria |
| Live deployment | ArgoCD app `chirp` @ `c805525` (reached per the project `CLAUDE.md`) | Exercise the product read-only for `manual_user_check` / `operational_check` criteria |

### Methodology
Apply the principal-product-designer persona and the relayed **Release Definition** guidance (**ReleaseBar** — measure
the product criterion by criterion as someone who was not in the design room). The `design` methodology loader is
unavailable run-wide (`agent_domain_unset`); record the limitation and proceed. Match each `BAR-*`'s stated
`verification_method` to how you observe it; where a method cannot be run in this environment, say so and judge
conservatively rather than optimistically.

### Output
- `outputs/live-measurement.md` — one verdict row per `BAR-*` (all 278): `bar_id`, `live_status`
  ∈ {`met`, `partial`, `missing`, `not_applicable`}, and a concise **observation** grounding the verdict (what was
  exercised or inspected, and what was seen — e.g. "posted, restarted the serving process, chirp gone → missing";
  "no recovery route exists in the SPA or API at `c805525` → missing"). Keyed by `bar_id` so the fold joins it into
  the matrix mechanically. A short preamble records how the live product was reached (or why it could not be) — kept
  out of anything repository-bound.

### Success criteria
- [ ] Every `BAR-*` in the release bar (all 278) has exactly one `live_status` and a recorded observation.
- [ ] Each observation is grounded in an actual exercise of the live product or an actual repository artifact — no
      assumed or confabulated results; unobservable criteria are judged conservatively with the reason stated.
- [ ] Verdicts use the inherited `live_status` vocabulary and reference `BAR-*` ids verbatim.
- [ ] The measurement is read-only on the live product (no product code; no mutation beyond a throwaway test
      account's own normal actions) and touches only the project's own repo/cluster/namespace.

### Constraints
- Read-only on the live product; no product code.
- Environment/host facts for reaching the deployment MUST NOT appear in anything that could reach GitHub or the
  verdict — reference the product only by repository identity and commit SHA there.
