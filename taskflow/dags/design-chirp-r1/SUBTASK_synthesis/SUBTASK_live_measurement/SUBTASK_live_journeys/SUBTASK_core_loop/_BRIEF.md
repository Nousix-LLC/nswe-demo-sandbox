# Task: Measure the core value loop (manual_user_check) against the live product at c805525

## Task Specification
**Slug**: SUBTASK_core_loop
**Task Kind**: standard
**Depends on**: none
**Status**: Pending

### Objective
Exercise the product's core value loop at commit `c805525` as a user, and judge each of the 24 `manual_user_check`
`BAR-*` assigned to this cluster `met | partial | missing | not_applicable`, each with a recorded observation of what
was exercised and seen.

### Context
Part of `SUBTASK_live_journeys` (see `../_GLOBAL.md` and `../contracts/_MANIFEST.yaml`). This cluster covers the
product's main loop and the entities behind it — distinct surfaces among them: the **account/profile model** (one
account entity, handle rules, opaque ids, creation time, display-name/bio editing); **composing and posting** a chirp
(length limit, attribution, immutability); **replies** (targeting an existing chirp); **likes** (idempotent toggle,
count); **follows** (one-directional, idempotent, counts, no self-follow); the **home timeline** (own + followed,
newest-first, bounded pages, catch-up); the **compose affordance**; and **public profiles** with follower/following
lists. Weigh these honestly in your own atomic-vs-decompose evaluation against the real shape and size of the work.

**Dependencies**: none. **Dependents**: `SUBTASK_journeys_fold`.

### Owned criteria (measure every one; measure no other)
BAR-100, BAR-101, BAR-102, BAR-104, BAR-105, BAR-106, BAR-107, BAR-108, BAR-109, BAR-110, BAR-111, BAR-117, BAR-163,
BAR-209, BAR-211, BAR-212, BAR-238, BAR-239, BAR-242, BAR-243, BAR-244, BAR-245, BAR-246, BAR-247.

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
- `outputs/core-loop-measurement.md` — a verdict table conforming to the inherited `verdict_row_schema` (columns
  `bar_id, live_status, observation`): one row per owned `BAR-*`, keyed by `bar_id`. A short access-note header records
  only *that* the live product was reached (or why not), by repository/commit identity — no host detail.

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
