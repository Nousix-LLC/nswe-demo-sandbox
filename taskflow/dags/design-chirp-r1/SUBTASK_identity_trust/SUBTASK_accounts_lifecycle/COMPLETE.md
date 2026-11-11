# COMPLETE — SUBTASK_accounts_lifecycle

## What this task did
Designed chirp's account object and its full lifecycle as testable `REQ-ID-*` requirements for the
`accounts_and_lifecycle` section of `design/identity-security.md`, to the bar of a releasable,
publicly-exposed, account-based consumer product. Requirements only; implementation "how" deferred
to code DAGs and to the sibling auth area by prose.

## Output produced
- `outputs/accounts-lifecycle.md` — the `accounts_and_lifecycle` section partial in the format fixed
  by `../contracts/req_id_partition.yaml`: section prose (account object, sign-up, manage, recovery,
  leaving) + `REQ-ID-001..024` + a "Notes for synthesis" block (cross-area seams, REQ-PROD coverage
  map, STRIDE threat hints).

## REQ-ID minted
`REQ-ID-001..024`, all within the assigned `001..029` range (025..029 intentionally unused — the
range need not be filled). Clusters: account object + public/private boundary (001); sign-up
(002–006); profile + settings (007–011); handle-change policy (012); recovery (013–016); export
(017–019); deletion (020–024).

## Contract compliance
- Ids only within `REQ-ID-001..029`; no `REQ-PROD-*`/`REQ-DOM-*`/`REQ-UX-*`/`REQ-OPS-*`/`BAR-*` minted.
- Each requirement has statement, testable acceptance_criteria, a release_gating flag (with inline
  reason where false), a verification_method from the inherited vocabulary, and traces_to ≥1
  existing `REQ-PROD-*`.
- Id format, required fields, verification vocabulary, and section map composed against, not redefined.
- Deliverable carries no host/system/taskflow detail and no attribution trailer; writing-voice pass run.

## REQ-PROD identity needs answered (primary traces)
008→002, 009→003, 012→004/005/009, 013→013/014/015/016, 016→007, 017→008/009/010/011, 018→012,
019→017/018/019, 020→020/023/024, 021→021/023, 022→022. REQ-PROD-014 and REQ-PROD-024 referenced
from the account side but owned by the auth and authorization/abuse-privacy areas (flagged so
synthesis does not double-count ownership).

## How it composes with the parent
Feeds `SUBTASK_synthesis`, which consolidates this partial with the auth, authorization, and
abuse/privacy partials, authors the threat model, and assembles `outputs/identity-security.md`.
The "Notes for synthesis" block hands off the four cross-area seams (auth mechanism, authorization
enforcement, privacy/retention/erasure, durability) and the threat hints the STRIDE walk needs.

## Decompose evaluation
Atomic — one requirements cluster (the account lifecycle), one owned section, one id range, one
output file; the five facets are tightly-coupled stages of one responsibility, not separable
analyses, so no scope or single-responsibility trigger fired.
