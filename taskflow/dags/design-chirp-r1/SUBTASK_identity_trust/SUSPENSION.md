# SUSPENSION.md — SUBTASK_identity_trust (NeedsDecompose)

## Outcome
Decomposed. This node evaluated `NeedsDecompose` and materialized a hub-and-spoke subtree. It is now SUSPENDED
pending its subtree reaching terminal states; it resolves via the synthesis fold (no `COMPLETE.md` of its own).

## Why decompose (trigger application against the actual brief)
- **Scope / Distinct Concerns — FIRED.** The brief's "Distinct concerns in this task" heading enumerates five
  distinct concerns (accounts & lifecycle; authentication & sessions; authorization; abuse & privacy; threat
  model). The enumerated-concerns rule fires the scope trigger by that enumeration alone. Honest Distinct
  Concerns Test: the four surface concerns are genuinely parallelizable requirement clusters; the threat model
  is their dependent synthesis.
- **Output size — FIRED.** A six-section requirements-plus-threat-model document with ~20+ `REQ-ID-*` entries
  exceeds the 400-line decompose threshold.
- **Token — cleared** (inputs ≈ 30–35K tokens). Per trigger precedence, scope wins over the cleared token
  trigger; one declared output file does not make the task atomic.

## Subtree materialized (five children)
| Child (id) | Depends on | Owns | REQ-ID range | Section |
|---|---|---|---|---|
| `SUBTASK_accounts_lifecycle` | none | accounts & lifecycle requirements | 001–029 | accounts_and_lifecycle |
| `SUBTASK_auth_sessions` | none | real auth & safe sessions requirements | 030–059 | authentication_and_sessions |
| `SUBTASK_authorization` | none | authority model requirements | 060–079 | authorization |
| `SUBTASK_abuse_privacy` | none | abuse-resistance & privacy requirements | 080–099 | abuse_and_privacy_basics |
| `SUBTASK_identity_trust/SUBTASK_synthesis` (Task Kind: synthesis) | the four spokes | threat model + assembly + verification gate + fold | 100–119 | threat_model + requirements_and_acceptance_criteria |

## Named state authored before this suspension
- `_GLOBAL.md` (subtree hub) at this workspace.
- `contracts/_MANIFEST.yaml` + `contracts/req_id_partition.yaml` (sub-contract; extends the root contract
  additively — partitions the `REQ-ID` number space, fixes the section→owner map and the partial-output format,
  adds the subtree identities the synthesis gate asserts).
- One `_BRIEF.md` per child (five).

## Deliverable and fold
The subtree produces the single `outputs/identity-security.md` (six required sections + consolidated `REQ-ID-*`
register, each requirement tracing to `REQ-PROD-*`), authored by the synthesis child, which folds this node
`SUSPENDED → COMPLETED` via `SYNTHESIS.md` at this workspace.

## Resumption condition
All child tasks reach terminal lifecycle state; the synthesis fold resumes this node.

## Note
Phase B methodology surface was unbound in this reconstructed node (`agent_domain_unset`); the decomposition
proceeded on the principal-product-designer posture and the brief's named bundle IDs, propagated to the children.
