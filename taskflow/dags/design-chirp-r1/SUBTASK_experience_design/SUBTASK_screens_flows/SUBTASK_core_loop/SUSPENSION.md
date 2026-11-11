# SUSPENSION — SUBTASK_core_loop (NeedsDecompose)

## Why this node suspended

`SUBTASK_core_loop` evaluated its brief against the decomposition triggers at dispatch time and found the
work spans **seven distinct core-loop surfaces**, each a separate design responsibility. It therefore
decomposed rather than executing as one invocation.

### Trigger evaluation (recorded for audit)

| Trigger / test | Outcome | Evidence |
|---|---|---|
| Token-Based | cleared | ~60–70K tokens of inputs read, well under 50% of context. |
| Scope-Based (enumerated-concerns rule) | **FIRED** | The brief enumerates 7 distinct surfaces: home timeline, compose & post, reply & conversation, like/unlike, follow/unfollow, discovery, view profile. |
| Output-Size | **FIRED** | 7 surfaces × (happy path + empty/error/loading) + 14 REQ-UX entries estimated ~530 lines (> 400). |
| Distinct Concerns Test | **fails** | The surfaces are designable by parallel specialists against the already-frozen screen inventory and component library. |
| Single-Responsibility Test | **fails** | The faithful description joins seven distinct surface-design responsibilities with "and". |
| Trigger precedence / independence | decompose | A fired scope trigger is not overridden by the cleared token trigger; "my parent already made this a spoke" is not grounds for Atomic. |

Verdict: **NeedsDecompose.**

## What was authored

- `_GLOBAL.md` — this subtree's hub (context, constraints, the Task Summary DAG, the contract section).
- `contracts/_MANIFEST.yaml` + `contracts/core_loop_seam.yaml` — the internal seam: surface→owner map,
  the `REQ-UX-051..064` sub-range partition, the shared-vocabulary composition rule, the
  per-screen↔global-pattern cross-reference, the trace rule, and the identities synthesis asserts.
- One `_BRIEF.md` per child (four spokes + one synthesis gate).

## Children materialized (via engine_amend_plan add_task)

| Task id | Role | Depends on | Output | REQ-UX |
|---|---|---|---|---|
| `SUBTASK_timeline_reading` | spoke | none | `outputs/screens-timeline-reading.md` | 051..053 |
| `SUBTASK_posting_conversation` | spoke | none | `outputs/screens-posting-conversation.md` | 054..058 |
| `SUBTASK_social_actions` | spoke | none | `outputs/screens-social-actions.md` | 059..060 |
| `SUBTASK_profiles_discovery` | spoke | none | `outputs/screens-profiles-discovery.md` | 061..064 |
| `SUBTASK_core_loop_synthesis` | synthesis gate + fold | the four spokes | `../outputs/screens-core-loop.md` + `../SYNTHESIS.md` | consolidated 051..064 |

## Resumption condition

All child tasks reach a terminal lifecycle state. The synthesis gate assembles the four spoke outputs into
`outputs/screens-core-loop.md`, consolidates the `REQ-UX-051..064` register, asserts the contract
identities with recorded evidence, authors `SYNTHESIS.md`, and folds this node (`SUBTASK_core_loop`)
`SUSPENDED → COMPLETED`.
