# Task: Measure the accessibility path (manual_user_check) against the live product at c805525

## Task Specification
**Slug**: SUBTASK_accessibility
**Task Kind**: standard
**Depends on**: none
**Status**: Pending

### Objective
Exercise the product's keyboard & screen-reader path and WCAG checks at commit `c805525` as a user relying on assistive
technology, and judge each of the 18 `manual_user_check` `BAR-*` assigned to this cluster
`met | partial | missing | not_applicable`, each with a recorded observation of what was exercised and seen.

### Context
Part of `SUBTASK_live_journeys` (see `../_GLOBAL.md` and `../contracts/_MANIFEST.yaml`). This cluster covers the
accessibility baseline — distinct surfaces among them: the **keyboard-and-screen-reader core loop**; the **visible
focus indicator**; **keyboard-only** completion of core-loop and get-in actions; **focus order**; **no focus trap**
(modal focus management); **skip-to-content**; **screen-reader component announcement** (names, roles, states);
**landmarks**; **heading structure**; **screen-reader feed navigation**; **icon-only control names**; **200% zoom /
320px reflow**; **greyscale / colour-blind distinguishability**; **no flashing > 3/s**; **reduce-motion**; and
**screen-reader status announcements** for actions, sign-up errors, and loading. These are measured with keyboard
navigation, a screen reader, zoom, and a contrast/colour tool. Weigh these honestly in your own atomic-vs-decompose
evaluation against the real shape and size of the work.

**Dependencies**: none. **Dependents**: `SUBTASK_journeys_fold`.

### Owned criteria (measure every one; measure no other)
BAR-031, BAR-218, BAR-276, BAR-277, BAR-278, BAR-279, BAR-280, BAR-281, BAR-282, BAR-283, BAR-284, BAR-286, BAR-287,
BAR-288, BAR-289, BAR-290, BAR-291, BAR-292.

### Inputs
| Input | Source | Purpose |
|-------|--------|---------|
| Subtree hub | `../_GLOBAL.md` | Shared context, constraints, hygiene |
| Sub-contract | `../contracts/_MANIFEST.yaml` | Your owned cluster, the verdict-row schema, the `live_status` vocab, totality identity |
| id/traceability schema | `../../../../contracts/id_and_traceability_schema.yaml` | `live_status` + `verification_method` vocab (authoritative) |
| Release bar | `../../../../SUBTASK_release_bar/outputs/release-bar.md` | The full statement of each owned `BAR-*` |
| Design PR record | `../../../../SUBTASK_design_pr/outputs/design-pr.md` | PR #, branch, repo `design/` map, for context |
| Live deployment | ArgoCD app `chirp` @ `c805525` (reached per the project `CLAUDE.md` host notes) | Exercise the product read-only |
| Repository @ `c805525` | `../../../../SUBTASK_design_pr/repo` (or a fresh `gh repo clone Nousix-LLC/nswe-demo`, checked out at `c805525`) | Confirm presence/absence of a11y affordances (roles, labels, landmarks) in the SPA/API source where the running UI is ambiguous |

### How the live product is reached (environment facts — keep OUT of the output)
Reach the deployment per the project `CLAUDE.md` host notes. Use those facts only to run checks; they MUST NOT appear
in the output. If the deployment is genuinely unreachable, confirm presence/absence of accessibility affordances from
the SPA/API source at `c805525` (ARIA roles, labels, landmark structure, markup) where a code artifact can settle it,
and record each criterion that truly needs a rendered assistive-technology session as `missing`/`partial` with the
reason — do not invent an observation.

### Methodology
Apply the principal-product-designer persona and the relayed ReleaseBar guidance: measure criterion by criterion as a
person relying on keyboard and a screen reader. Use a single throwaway test account for anything needing a signed-in
user; stay read-only beyond that account's own normal actions. Judge conservatively where a check cannot be run. The
Phase-B `design` loader is unavailable run-wide (`agent_domain_unset`); record the limitation and proceed.

### Output
- `outputs/accessibility-measurement.md` — a verdict table conforming to the inherited `verdict_row_schema`
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
