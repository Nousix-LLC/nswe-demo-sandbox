# Task: Assemble, verify, and fold the core-loop screens

## Task Specification
**Slug**: SUBTASK_synthesis
**Task Kind**: synthesis
**Status**: Pending

### Objective
Assemble the four core-loop spoke outputs into the one deliverable `../outputs/screens-core-loop.md`,
consolidate the `REQ-UX-051..064` register, assert this subtree's contract identities with recorded
evidence, and fold the `SUBTASK_core_loop` node to COMPLETED.

### Context
This is the verification gate and fold for the core-loop screens subtree (see `../_GLOBAL.md`,
`../contracts/`). It reads the four spoke outputs and composes them; it does not redesign any screen. Its
job is mechanical: coverage, single-ownership, id uniqueness/range, not-skeletal, testable+gated+traced,
composed-against-vocabulary, states-consistent, hygiene — the identities declared in `../contracts/`. A
failing identity is reported and remediated by decomposing a remediation subtree, never silently plugged.

**Dependencies**: `SUBTASK_timeline_reading`, `SUBTASK_posting_conversation`, `SUBTASK_social_actions`,
`SUBTASK_profiles_discovery` (all four spokes). **Dependents**: the parent `../../SUBTASK_synthesis`
(screens-&-flows) consumes `../outputs/screens-core-loop.md` and the consolidated register.

### Inputs
| Input | Source | Purpose |
|-------|--------|---------|
| Subtree hub | `../_GLOBAL.md` | Shared context, the assembled order, identities, hygiene. |
| Internal contract | `../contracts/` (read-only) | The surface→owner map, id sub-ranges, identities to assert, the derived register spec. |
| Timeline reading output | `../SUBTASK_timeline_reading/outputs/screens-timeline-reading.md` | Home timeline design + `REQ-UX-051..053`. |
| Posting & conversation output | `../SUBTASK_posting_conversation/outputs/screens-posting-conversation.md` | Compose/post + conversation design + `REQ-UX-054..058`. |
| Social-action output | `../SUBTASK_social_actions/outputs/screens-social-actions.md` | Like & follow in-place + `REQ-UX-059..060`. |
| Profiles & discovery output | `../SUBTASK_profiles_discovery/outputs/screens-profiles-discovery.md` | Profiles/followers/following + explore + `REQ-UX-061..064`. |

### Output
- `../outputs/screens-core-loop.md` — the `core_loop` part assembled from the four spoke outputs in the
  order the seam fixes (timeline_reading → posting_conversation → social_actions → profiles_discovery),
  followed by the consolidated `REQ-UX-051..064` register. Repository-ready; no host/system/taskflow
  detail, no workspace paths, no attribution.
- `../SYNTHESIS.md` — the fold record: per-identity evidence (coverage & single-owner, id
  uniqueness/range, not-skeletal, testable+gated+traced, composed-against-vocab, states-consistent,
  hygiene), any gaps found and how remediated, and the fold of the `SUBTASK_core_loop` node.

### Success criteria
- [ ] `../outputs/screens-core-loop.md` carries all seven core-loop surfaces, each from exactly one spoke,
      assembled in the seam's order.
- [ ] The consolidated `REQ-UX-051..064` register is complete, unique, in-range, each testable, gated, and
      tracing to ≥1 `REQ-PROD-*`.
- [ ] Every identity in `../contracts/_MANIFEST.yaml` is asserted with recorded evidence; no silent plug.
- [ ] `../SYNTHESIS.md` authored at the fold location and the node folded to COMPLETED.

### Constraints
- Design/verify only — no front-end code. Repository-ready hygiene on all output content.
- Methodology: Experience Design. Load bundle bodies on demand; if the `design` loader is unavailable,
  verify from the bundle intent and competence and record the limitation (do not block).
- A failing identity is reported and remediated by decomposing a remediation subtree, never silently
  plugged.
- Write in a plain, checkable human voice; run the avoid-ai-writing checklist over the narrative before
  finalizing.
