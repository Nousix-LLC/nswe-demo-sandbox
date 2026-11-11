# SUSPENSION — SUBTASK_bar_ux_screens (NeedsDecompose, reconstructed resume)

## Status
Suspended — `decompose_evaluation = NeedsDecompose`. This node was reconstructed from its
on-disk file image and resumed. It had already evaluated `NeedsDecompose` in a prior
invocation and fanned its screens-&-flows release-bar authoring (`BAR-230..264`, the 43
release-gating `REQ-UX-040..089`) into five chapter spokes plus a synthesis gate. This
invocation re-ran the decompose-evaluation independently against the actual brief, reached
the same `NeedsDecompose` verdict, confirmed the materialized subtree is sound, and
re-suspends pending its resolution.

## Decompose-evaluation (re-run this invocation, independent of the prior one)
- **Scope-Based trigger — FIRES.** The brief enumerates eight distinct screen groups, each a
  body of gating requirements (entry & auth; home timeline & compose core loop;
  conversation/like/follow; profiles & discovery lists; onboarding & profile edit; settings &
  account lifecycle; safety/help/rules/not-found; cross-screen state patterns). Enumerated-concerns
  rule: ≥2 distinct areas fire the Scope trigger by enumeration alone.
- **Distinct Concerns Test — decompose.** The chapters are authorable by parallel specialists.
- **Output-Size** (~280–330 lines) is in the "consider" band — the weakest signal; MUST NOT
  override the fired Scope trigger. **Token** estimate clears but cannot override scope either.
- **Independence at depth:** "my parent already split UX into areas" is not grounds for `Atomic`;
  the designer instinct to hold the screens picture whole is explicitly disqualified.
- Verdict: **NeedsDecompose**, matching the already-materialized subtree.

## Subtree state on resume (observed from disk)
| Child | BAR sub-range | Task Kind | Depends on | State |
|-------|---------------|-----------|------------|-------|
| `SUBTASK_bar_screens_entry_auth` | BAR-230..237 | standard | none | **COMPLETED** (output + COMPLETE.md) |
| `SUBTASK_bar_screens_core_loop` | BAR-238..242 | standard | none | PENDING |
| `SUBTASK_bar_screens_social_profiles` | BAR-243..247 | standard | none | PENDING |
| `SUBTASK_bar_screens_account_lifecycle` | BAR-248..255 | standard | none | PENDING |
| `SUBTASK_bar_screens_safety_states` | BAR-256..263 | standard | none | **COMPLETED** (output + COMPLETE.md) |
| `SUBTASK_bar_screens_synthesis` | BAR-264 (cross-cutting) | synthesis | all five spokes | PENDING (verification gate + fold) |

Subtree hub (`_GLOBAL.md`), frozen seam (`contracts/_MANIFEST.yaml`, `contracts/bar_screens_partition.yaml`),
and all six child briefs are present and internally consistent: the hub Task Summary, the per-child
`Task Kind` / `Depends on` edges, and the partition's disjoint `BAR-*` sub-ranges agree. No repair or
re-materialization was required, and no child's work was executed in this invocation.

## Why no `add_task` this invocation
The six children already exist as DAG nodes placed under this task in the reconstructed graph
(files are canonical; the DAG is rebuilt from them). Re-issuing `add_task` would duplicate nodes
and is not performed. The NeedsDecompose terminal precondition is satisfied by the reconstructed
placement (≥1 child whose recursive-depth parent is this task).

## Resumption condition
All children reach terminal lifecycle state. `SUBTASK_bar_screens_synthesis` assembles the five
sub-fragments into `outputs/bar-ux-screens.md`, asserts the eight sub-identities with recorded
evidence, authors `SYNTHESIS.md`, and folds this node (`SUSPENDED → COMPLETED`) via the synthesis
fold. This node is not re-run; it resolves by the fold.

## Methodology posture
The `design` methodology loader is unavailable run-wide (`agent_domain_unset`); ancestors recorded
the same and proceeded. The product-designer persona's release-definition judgment plus the relayed
bundle guidance (Release Definition primary; Experience Design, Product Strategy supporting) stand in.
This note is taskflow-internal and is not repository content.
