# Task: Measure every manual_user_check BAR-* by exercising the live product at c805525

## Task Specification
**Slug**: SUBTASK_live_journeys
**Task Kind**: standard
**Depends on**: none
**Status**: Pending

### Objective
Exercise the deployed chirp product at commit `c805525` as a user would, and judge **every `BAR-*` whose declared
`verification_method` is `manual_user_check`** (139 criteria) as `met | partial | missing | not_applicable`, each with
a recorded observation — what was exercised and what was seen.

### Context
Part of `SUBTASK_live_measurement` (see `../_GLOBAL.md` and the sub-contract `../contracts/_MANIFEST.yaml`). This is
the live-user-journey partition of the measurement: the `manual_user_check` criteria, those a person settles by using
the running product. The other partitions (`automated_test`, `inspection`, `operational_check`) are owned by siblings;
measure only the `manual_user_check` `BAR-*`, and measure every one of them.

The `manual_user_check` criteria span the product's whole user surface across all five areas — distinct journeys and
surfaces that a person reaches at different points, among them: first-visit and sign-up; sign-in, sign-out, and
credential recovery; composing and posting; reading the home timeline, replies, likes, and follows; viewing public
profiles; editing profile and settings; the verified-contact, sessions-and-devices, data-export, and account-deletion
surfaces; reporting and the in-product rules; the operator/support surface; empty states, loading states, and error
recovery; the typical-phone (responsive) experience; and the keyboard-and-screen-reader (accessibility) path. These
are genuinely distinct concerns reached through different parts of the product; weigh them honestly in your own
atomic-vs-decompose evaluation against the real shape and size of the work.

A headline fact to confirm by observation, not assume: the product at `c805525` uses an in-memory store that loses all
data on restart — many release-layer account-lifecycle surfaces (recovery, settings, export, deletion, reporting,
operator tools) may be entirely absent in the SPA/API at `c805525`. Where a surface does not exist, that is a grounded
`missing` observation; confirm its absence rather than presuming it.

**Dependencies**: none. **Dependents**: `SUBTASK_measurement_fold`.

### Inputs
| Input | Source | Purpose |
|-------|--------|---------|
| Subtree hub | `../_GLOBAL.md` | Shared context, constraints, hygiene |
| Sub-contract | `../contracts/_MANIFEST.yaml` | Your owned partition (`manual_user_check`), the verdict-row schema, the `live_status` vocab |
| id/traceability schema | `../../../contracts/id_and_traceability_schema.yaml` | `live_status` + `verification_method` vocab (authoritative) |
| Release bar | `../../../SUBTASK_release_bar/outputs/release-bar.md` | The 278 `BAR-*`; filter to those tagged `manual_user_check` |
| Design PR record | `../../../SUBTASK_design_pr/outputs/design-pr.md` | PR #, branch, repo `design/` map, for context |
| Live deployment | ArgoCD app `chirp` @ `c805525` (reached per the project `CLAUDE.md` host notes) | Exercise the product read-only |
| Repository @ `c805525` | `../../../SUBTASK_design_pr/repo` (or a fresh `gh repo clone Nousix-LLC/nswe-demo`, checked out at `c805525`) | Confirm the presence/absence of a user-facing surface in the SPA/API source where the running UI is ambiguous |

### How the live product is reached (environment facts — keep OUT of the output)
Reach the deployment per the project `CLAUDE.md` host notes. Use those facts only to run checks; they MUST NOT appear
in your output. If the live deployment is genuinely unreachable from this environment, confirm each surface's presence
or absence from the SPA/API source at `c805525` where a code artifact can settle it, and record each remaining
criterion that truly needs a running session as `missing`/`partial` with the reason it could not be observed — do not
invent an observation.

### Methodology
Apply the principal-product-designer persona and the relayed **ReleaseBar** guidance: measure the product criterion by
criterion as someone who was not in the design room. For each `manual_user_check` `BAR-*`, exercise the journey its
statement describes and record what the product actually does. Use a single throwaway test account for any action that
needs a signed-in user; stay read-only beyond that account's own normal actions. Judge conservatively where a surface
cannot be reached.

### Output
- `outputs/live-journeys-measurement.md` — a verdict table conforming to `verdict_row_schema` in the sub-contract: one
  row per `manual_user_check` `BAR-*` (`bar_id`, `live_status`, `observation`). A short access-note header records only
  *that* the live product was reached (or why not), by repository/commit identity — no host detail. Rows keyed by
  `bar_id` so the fold unions them mechanically.

### Success criteria
- [ ] Every `BAR-*` tagged `manual_user_check` in the release bar has exactly one `live_status` and a grounded
      observation; no such `BAR-*` is omitted, and no `BAR-*` of another method is included.
- [ ] Each observation is grounded in an actual exercise of the live product (or an actual SPA/API source artifact at
      `c805525` where the running product was unreachable or ambiguous) — never assumed or confabulated; unobservable
      criteria judged conservatively with the reason stated.
- [ ] `live_status` values are from the inherited vocab; `bar_id`s are verbatim.
- [ ] Read-only on the live product; output touches only `Nousix-LLC/nswe-demo` and the project's own deployment; no
      host/system/taskflow detail in the output.

### Constraints
- Read-only on the live product; no product code.
- Environment/host facts for reaching the deployment MUST NOT appear in the output — reference the product only by
  repository identity and commit SHA.
