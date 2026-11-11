# Task: Measure the web-delivery & API-as-experienced surface (manual_user_check) against the live product at c805525

## Task Specification
**Slug**: SUBTASK_web_delivery_api
**Task Kind**: standard
**Depends on**: none
**Status**: Pending

### Objective
Exercise the product's web-delivery surface as a user experiences it at commit `c805525`, and judge each of the 10
`manual_user_check` `BAR-*` assigned to this cluster `met | partial | missing | not_applicable`, each with a recorded
observation of what was exercised and seen.

### Context
Part of `SUBTASK_live_journeys` (see `../_GLOBAL.md` and `../contracts/_MANIFEST.yaml`). This cluster covers how the
product is delivered and reached — distinct surfaces among them: **one web address** serving the single-page app with
nothing to install; the **single service** serving the REST API, the SPA, and the health endpoint from one origin;
**SPA routing** (in-app routes load client-side; an unknown path returns the app entry document); the **API path
prefix** on the same origin; the **end-to-end API operations** as reached through the app (create account, profile,
session, post/reply, timeline, follow/unfollow, like/unlike); **timeline pagination** with an opaque cursor and clamped
size; the **bearer-token / public-fields-only** response discipline; **typed errors** with a machine-readable category
the UI branches on; **data presence over a sustained period**; and the **health endpoint** answering with no session.
Several of these are observed through the running app and its network traffic; some can be settled from the SPA/API
source at `c805525`. Weigh these honestly in your own atomic-vs-decompose evaluation against the real shape and size of
the work.

**Dependencies**: none. **Dependents**: `SUBTASK_journeys_fold`.

### Owned criteria (measure every one; measure no other)
BAR-166, BAR-169, BAR-170, BAR-171, BAR-172, BAR-173, BAR-176, BAR-177, BAR-406, BAR-462.

### Inputs
| Input | Source | Purpose |
|-------|--------|---------|
| Subtree hub | `../_GLOBAL.md` | Shared context, constraints, hygiene |
| Sub-contract | `../contracts/_MANIFEST.yaml` | Your owned cluster, the verdict-row schema, the `live_status` vocab, totality identity |
| id/traceability schema | `../../../../contracts/id_and_traceability_schema.yaml` | `live_status` + `verification_method` vocab (authoritative) |
| Release bar | `../../../../SUBTASK_release_bar/outputs/release-bar.md` | The full statement of each owned `BAR-*` |
| Design PR record | `../../../../SUBTASK_design_pr/outputs/design-pr.md` | PR #, branch, repo `design/` map, for context |
| Live deployment | ArgoCD app `chirp` @ `c805525` (reached per the project `CLAUDE.md` host notes) | Exercise the product read-only |
| Repository @ `c805525` | `../../../../SUBTASK_design_pr/repo` (or a fresh `gh repo clone Nousix-LLC/nswe-demo`, checked out at `c805525`) | Confirm presence/absence of a surface in the SPA/API source where the running product is ambiguous |

### How the live product is reached (environment facts — keep OUT of the output)
Reach the deployment per the project `CLAUDE.md` host notes. Use those facts only to run checks; they MUST NOT appear
in the output — reference the product only by repository identity and commit SHA, repo-relative paths, and
`BAR-*`/`REQ-*` ids. Record only *that* the product was reached (or why not), never how. If the deployment is genuinely
unreachable, confirm presence/absence from the SPA/API source at `c805525` where a code artifact can settle it, and
record each criterion that truly needs a running session as `missing`/`partial` with the reason — do not invent an
observation.

### Methodology
Apply the principal-product-designer persona and the relayed ReleaseBar guidance: measure criterion by criterion as
someone who was not in the design room, reaching the product only as a user does (the app, its routes, and the traffic
the app itself makes). Use a single throwaway test account for anything needing a signed-in user; stay read-only beyond
that account's own normal actions. Judge conservatively where a surface cannot be reached. The Phase-B `design` loader
is unavailable run-wide (`agent_domain_unset`); record the limitation and proceed.

### Output
- `outputs/web-delivery-api-measurement.md` — a verdict table conforming to the inherited `verdict_row_schema`
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
