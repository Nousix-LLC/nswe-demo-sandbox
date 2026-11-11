# Task: Measure safety, trust & support surfaces (manual_user_check) against the live product at c805525

## Task Specification
**Slug**: SUBTASK_safety_trust_support
**Task Kind**: standard
**Depends on**: none
**Status**: Pending

### Objective
Exercise the product's safety, trust, and support surfaces at commit `c805525` as a user, and judge each of the 8
`manual_user_check` `BAR-*` assigned to this cluster `met | partial | missing | not_applicable`, each with a recorded
observation of what was exercised and seen.

### Context
Part of `SUBTASK_live_journeys` (see `../_GLOBAL.md` and `../contracts/_MANIFEST.yaml`). This cluster covers the
distinct safety/trust surfaces — among them: **reporting** a chirp and an account (with acknowledgement, pointing at a
rule); the **rules / terms** screen; **help & support** reachable signed-out and signed-in; the provisioned,
least-privilege **operator/support surface** (assist recovery, remove a chirp, action an abusive account); and the
**status / degraded** surface a person sees when the product is unavailable or degraded. Weigh these honestly in your
own atomic-vs-decompose evaluation against the real shape and size of the work.

A fact to confirm by observation, not assume: the product at `c805525` uses an in-memory store and **most of this
cluster — reporting, rules, help, operator surface, status notice — may be entirely absent** in the SPA/API at
`c805525`. The operator surface in particular is a provisioned least-privilege path that a user cannot reach; confirm
its presence or absence from the SPA/API source at `c805525` where a code artifact can settle it. Where a surface does
not exist, that is a grounded `missing`; do not presume.

**Dependencies**: none. **Dependents**: `SUBTASK_journeys_fold`.

### Owned criteria (measure every one; measure no other)
BAR-023, BAR-025, BAR-256, BAR-257, BAR-258, BAR-334, BAR-482, BAR-485.

### Inputs
| Input | Source | Purpose |
|-------|--------|---------|
| Subtree hub | `../_GLOBAL.md` | Shared context, constraints, hygiene |
| Sub-contract | `../contracts/_MANIFEST.yaml` | Your owned cluster, the verdict-row schema, the `live_status` vocab, totality identity |
| id/traceability schema | `../../../../contracts/id_and_traceability_schema.yaml` | `live_status` + `verification_method` vocab (authoritative) |
| Release bar | `../../../../SUBTASK_release_bar/outputs/release-bar.md` | The full statement of each owned `BAR-*` |
| Design PR record | `../../../../SUBTASK_design_pr/outputs/design-pr.md` | PR #, branch, repo `design/` map, for context |
| Live deployment | ArgoCD app `chirp` @ `c805525` (reached per the project `CLAUDE.md` host notes) | Exercise the product read-only |
| Repository @ `c805525` | `../../../../SUBTASK_design_pr/repo` (or a fresh `gh repo clone Nousix-LLC/nswe-demo`, checked out at `c805525`) | Confirm presence/absence of a surface in the SPA/API source where the running UI is ambiguous |

### How the live product is reached (environment facts — keep OUT of the output)
Reach the deployment per the project `CLAUDE.md` host notes. Use those facts only to run checks; they MUST NOT appear
in the output. If the deployment is genuinely unreachable, confirm presence/absence from the SPA/API source at
`c805525` where a code artifact can settle it, and record each criterion that truly needs a running session as
`missing`/`partial` with the reason — do not invent an observation.

### Methodology
Apply the principal-product-designer persona and the relayed ReleaseBar guidance: measure criterion by criterion as
someone who was not in the design room. Use a single throwaway test account for anything needing a signed-in user;
stay read-only beyond that account's own normal actions. Judge conservatively where a surface cannot be reached. The
Phase-B `design` loader is unavailable run-wide (`agent_domain_unset`); record the limitation and proceed.

### Output
- `outputs/safety-trust-support-measurement.md` — a verdict table conforming to the inherited `verdict_row_schema`
  (columns `bar_id, live_status, observation`): one row per owned `BAR-*`, keyed by `bar_id`. A short access-note
  header records only *that* the live product was reached (or why not), by repository/commit identity — no host detail.

### Success criteria
- [ ] Every owned `BAR-*` has exactly one `live_status` and a grounded observation; none omitted; no `BAR-*` outside
      this cluster included.
- [ ] Each observation is grounded in an actual exercise of the live product (or an actual `c805525` source artifact
      where the running product was unreachable or ambiguous) — never assumed or confabulated.
- [ ] `live_status` values are from the inherited vocab; `bar_id`s are verbatim.
- [ ] Read-only on the live product; output touches only `Nousix-LLC/nswe-demo` and the project's own deployment; no
      host/system/taskflow detail in the output.

### Constraints
- Read-only on the live product; no product code.
- Environment/host facts for reaching the deployment MUST NOT appear in the output — reference the product only by
  repository identity and commit SHA.
