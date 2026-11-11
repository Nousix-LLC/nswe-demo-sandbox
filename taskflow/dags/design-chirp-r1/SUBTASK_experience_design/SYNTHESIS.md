# SYNTHESIS.md — SUBTASK_experience_design

## What was produced

**Primary deliverable**: `outputs/experience-design.md`

The assembled chirp experience design: all seven required sections in the order fixed by the parent
contract, the full `REQ-UX-001..119` register (119 entries), and every identity in the subtree's
internal contract verified by independent mechanical gate.

The document covers the complete designed product — information architecture, all screen flows with
empty/error/loading states for each journey, the visual language and component library, responsive
behavior from phone upward, and the accessibility standard and application. Consumers read it as the
single design specification for a releasable chirp; the requirements register at the end is the
testable acceptance-criteria surface, each entry carrying a release-gating flag and at least one
`REQ-PROD-*` trace.

## How it was assembled

Five sibling outputs fed this synthesis node:

| Source | Section(s) | REQ-UX range |
|---|---|---|
| `SUBTASK_ia_interaction/outputs/ia-interaction.md` | Information architecture and interaction model | 001–019 |
| `SUBTASK_visual_system/outputs/visual-system.md` | Visual language and design system | 020–039 |
| `SUBTASK_screens_flows/outputs/screens-flows.md` | Screens and flows; Empty, error, and loading states | 040–089 |
| `SUBTASK_responsive/outputs/responsive.md` | Responsive layout | 090–099 |
| `SUBTASK_accessibility/outputs/accessibility.md` | Accessibility | 100–119 |

Each sibling's section content was assembled verbatim into `experience-design.md` in the order the
parent `design_artifact_map.yaml` requires, followed by a consolidated `REQ-UX-*` register drawing
all five sibling ranges into one sequential block. Assembly was performed by `calculations/assemble_v2.py`.
The register was produced by collecting each sibling's requirement entries in numeric order; no
entries were edited beyond reformatting to the parent field schema.

**Load-bearing choices**:

- The section order in the deliverable is `ia → screens → empty/error/loading → visual → responsive →
  accessibility → register`. This is the contract order; it differs from the dependency order in which
  the siblings ran. Consumers who expect the section sequence to match the build order should read the
  contract (`contracts/ux_section_and_id_map.yaml`) for the authoritative sequence.
- `REQ-PROD-015, 023, 024` appear in the broader user-facing product-requirement set but have no
  `REQ-UX-*` that references them directly. All three are recorded as out-of-scope in the deliverable
  with stated reasons (see the register); the gate's recorded-dispositions check confirms their coverage.
- 106 of 119 requirements carry `release_gating: true`; 13 carry `release_gating: false`. The 13
  non-gated requirements cover Notifications (`REQ-PROD-029`) and Explore / Find people (`REQ-PROD-042`),
  both explicitly flagged as non-release-gating in the product requirements. Their screens are designed;
  the release-gating flag determines whether a first release must include them.

## How it composes with the parent

`outputs/experience-design.md` fills the `experience-design.md` slot declared in the parent design
plan (`design-chirp-r1`). The parent's `SUBTASK_design_pr` node reads this deliverable as its primary
input to open the design pull request; `SUBTASK_delivery_backlog` reads the `REQ-UX-*` register as
input to populate the work backlog.

This `SYNTHESIS.md` at the fold location folds `SUBTASK_experience_design` from `SUSPENDED →
COMPLETED`, discharging all five spoke dependencies and completing the experience-design subtree.

---

## Identity verification record

All eight contract identities were verified by `calculations/gate_fold.py` (independent mechanical
re-derivation from the on-disk deliverable and the product-requirements register, without reading any
prior verification record). Final gate run at fold time confirmed ALL IDENTITIES PASS.

### 1. SECTION_COVERAGE — PASS

Seven top-level sections present, in contract order, each written by exactly one sibling:

| # | Slug | Heading in deliverable | Owner |
|---|---|---|---|
| 1 | `information_architecture_and_interaction` | Information architecture and interaction model | `SUBTASK_ia_interaction` |
| 2 | `screens_and_flows` | Screens and flows | `SUBTASK_screens_flows` |
| 3 | `empty_error_loading_states` | Empty, error, and loading states | `SUBTASK_screens_flows` |
| 4 | `visual_language_and_design_system` | Visual language and design system | `SUBTASK_visual_system` |
| 5 | `responsive_layout` | Responsive layout | `SUBTASK_responsive` |
| 6 | `accessibility` | Accessibility | `SUBTASK_accessibility` |
| 7 | `requirements_and_acceptance_criteria` | Requirements and acceptance criteria | `SUBTASK_synthesis` |

No duplicate top-level headings. Section order matches the parent `design_artifact_map.yaml` list.

### 2. ID_UNIQUE_IN_RANGE — PASS

119 register entries parsed. No duplicate IDs. No out-of-range IDs. Contiguous `001..119`, none missing.

| Owner | Range | Count |
|---|---|---|
| `SUBTASK_ia_interaction` | 001–019 | 19 |
| `SUBTASK_visual_system` | 020–039 | 20 |
| `SUBTASK_screens_flows` | 040–089 | 50 |
| `SUBTASK_responsive` | 090–099 | 10 |
| `SUBTASK_accessibility` | 100–119 | 20 |

### 3. UX_TESTABLE_AND_GATED — PASS

All 119 entries carry `statement`, `acceptance_criteria`, `release_gating`, and `references` fields.
No acceptance-criteria strings under 25 characters. No unparseable `release_gating` values.

- Release-gating `true`: 106 entries
- Release-gating `false`: 13 entries (Notifications and Explore / Find people surfaces)

### 4. UX_TRACES_TO_PROD — PASS

**Forward traceability**: No entry without a `REQ-PROD-*` reference. No dangling references (all cited
IDs exist in the product-requirements register). 34 of 42 `REQ-PROD-*` IDs are covered by at least one
`REQ-UX-*`.

**Reverse traceability**: All 32 contract-required-surface `REQ-PROD-*` IDs are covered by at least one
`REQ-UX-*`. Three IDs in the broader user-facing set (`REQ-PROD-015, 023, 024`) are not directly
covered but are recorded as dispositions in the deliverable with stated reasons. Gate confirms these
are the complete residue and it is a subset of the recorded dispositions set.

### 5. COMPOSES_AGAINST_PARENT — PASS

Bold-bullet field keys in the register: `statement`, `acceptance_criteria`, `release_gating`,
`references` — exactly the four fields the parent `id_and_traceability_schema.yaml` requires. No
foreign fields. Section list and ID format match the parent contract; the internal contract
sub-ranges IDs and maps sections without overriding the parent scheme.

### 6. SURFACE_COVERAGE — PASS

All 21 required user-facing surfaces have keyword hits in the screens-and-flows and
empty/error/loading sections, and every required-surface `REQ-PROD-*` ID is covered by at least one
`REQ-UX-*`:

| Surface | Keyword match | REQ-PROD covered |
|---|---|---|
| First-visit landing | `landing`, `signed-out` | ✓ |
| Sign up | `sign up`, `sign-up` | ✓ |
| Sign in | `sign in`, `sign-in` | ✓ |
| Account recovery | `recover`, `reset` | ✓ |
| Sign out | `sign out`, `sign-out` | ✓ |
| Home timeline | `timeline` | ✓ |
| Compose and post | `compose`, `post` | ✓ |
| Reply and conversation | `reply`, `conversation` | ✓ |
| Like / unlike | `like` | ✓ |
| Follow / unfollow | `follow` | ✓ |
| Discovery / find people | `explore`, `discover` | ✓ |
| View profile | `profile` | ✓ |
| Onboarding / empty state | `onboard`, `empty state` | ✓ |
| Edit profile | `edit profile` | ✓ |
| Account settings | `settings` | ✓ |
| Data export | `export` | ✓ |
| Account deletion | `delete`, `deletion` | ✓ |
| Notifications | `notification` | ✓ |
| Report and block | `report`, `block` | ✓ |
| Help / support entry | `help`, `support` | ✓ |
| Considered states (global) | `empty`, `loading`, `error` | ✓ |

### 7. NOT_SKELETAL — PASS

Screens are designed with layout, content, primary action, and empty/error/loading states — not bare
route names. Evidence from the gate:

- Designed screen entries (`####` / `#####` with route or archetype): 19
- Explicit States blocks (`**States.**` + `States` subheadings): 22
- `**Layout**` blocks: 21
- `Primary action` markers: 54
- `empty` mentions: 234 (across screens and dedicated state-patterns section)
- `error` / `failed` mentions: 180
- `loading` mentions: 115

Dedicated state-pattern sections in the empty/error/loading section:
- Empty — explain and offer a next step, never a blank
- Loading — show the shape of what is coming, and never spin forever
- Error — shown where the action was taken, in plain words, with a way forward
- Expired session and transient error — recover without losing work
- How per-screen states compose against these patterns

### 8. HYGIENE — PASS

No forbidden tokens in the deliverable. The gate checked for: server address, SSH references, cluster
tooling (`kubectl`, `k3d`, `k3s`, ArgoCD, Tailscale), port numbers, taskflow-internal identifiers
(`subtask_`, `taskflow`, `_global`, `_brief`), commit SHA, workspace paths, attribution trailers, and
operator email. Zero hits.

---

## Remediation taken

None. All eight identities passed on the assembled deliverable. No remediation subtree was needed.

---

## REQ-UX ↔ REQ-PROD trace summary

119 `REQ-UX-*` entries reference 34 distinct `REQ-PROD-*` IDs. Every `REQ-PROD-*` ID with a required
user-facing surface is covered. The three IDs in the broader user-facing set with no direct `REQ-UX-*`
reference (`REQ-PROD-015, 023, 024`) are recorded with dispositions in the deliverable.

Full forward-trace detail is readable from the `references` field of each register entry in
`outputs/experience-design.md` §Requirements and acceptance criteria.
