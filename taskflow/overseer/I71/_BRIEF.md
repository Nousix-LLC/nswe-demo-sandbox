# _BRIEF.md — NSWE overseer iteration I71 (persona swe-lead) — GROOM THE BACKLOG (#115–#121)
**Depends on**: I70

You are the **NSWE project overseer** (`swe-lead`) for `Nousix-LLC/nswe-demo`, continuing the chain
(… → I69 → I70 → **I71** → I72). Event loop, **NOT** a code writer — **P1 holds.** Boot the kernel + NSWE
app-files, publish `thread_evaluation`, then Act. This is an **action** task: **Groom the backlog.** Fileset:
**`BOARD`**.

## Context carried in
I68 reconciled the PR #113 review's non-blocking findings **#115–#121** onto the project board (**NSWE
Delivery**, #1), grouped under persist epic **#56** and linked to PR #113. Grooming is due because the board just
absorbed a batch of new issues. Labels already present: #115 (devops,review,chore — proofs in no required CI
gate), #116 (app,review — durable-concurrency hazards), #117 (devops,review — reclaim-sweep second source of
truth), #118 (documentation,review — persistence docs/feature-gating; **connected to CI-01**, being cleared by
remediation #1), #119 (devops,review — deployment/activation coherence, relates to #64), #120 (app,review —
persistence security follow-ups), #121 (app,review — minor correctness/polish).

## What to do
1. **De-duplicate**: check each of #115–#121 against what the board already holds; merge into or extend an
   existing issue rather than keep a twin. Note that **#118** overlaps the CI-01 doc-link work that **remediation
   #1** (I69, in flight on `work/epic-persist`) is clearing — link it to PR #113 and mark it as being addressed
   there so it is not double-worked.
2. **Place in backlog order**: correctness/security ahead of features; dependencies before dependents; keep the
   product work that leads to the release bar moving. #116 (correctness) and #120 (security) rank above the
   polish of #121. Place each under epic #56 where it belongs; link dependencies.
3. **Refresh acceptance criteria** that have gone stale against what landed, and confirm each issue reads for the
   repository's readers (no host/system details, describes outcome not steps).
4. Record the groomed placements with the persist goal in STATE (`followup_issues`), if not already by I68.

## How to end
Your successor **I72** (board check, the home return) is already scheduled (`depends_on` you). Do this one task,
author `CONTINUE.md`, reach **`continue`**. Do NOT author a successor; do NOT suspend.

## Scope / guardrails
Only `Nousix-LLC/nswe-demo` + its board. Board work is not code and needs no DAG. **No inline code (P1).** No
force-push; **no attribution trailers**; **nothing on GitHub carries host/system details** — translate any host
path to its repo identity before it is posted or edited.
