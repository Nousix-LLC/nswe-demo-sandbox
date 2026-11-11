# COMPLETE: SUBTASK_ac1-verify

## Task
Verify AC-1 at HEAD `7f4b684671cab7eb778f5ad7f54dfdc82d57b3c4`.

## Verdict
**ac_1_verdict: PASS**

## What was checked

**Primary (B1 fix)**:
- `crates/chirp-frontend/src/timeline.rs:218` confirmed as `ctx.client().timeline(&query)` by direct GitHub API file read at SHA `7f4b684`. Cross-checked against r1 HEAD `decb6196` where the same line read `pub_timeline`. Fix is real and present.
- Fix not visible in `gh pr diff 263` because the bug was introduced and reverted intra-branch; aggregate diff from main cancels both commits. Direct per-SHA file verification is the evidence.

**Secondary (unchanged from r1)**:
- `public_chirps`, `user_chirps`, `public_timeline` backend handlers: added in this PR diff; confirmed no `AuthUser` extractor.
- Auth-gated handlers (`create_chirp`, `timeline`, `follow`, `unfollow`, `like`, `unlike`): not in diff; confirmed at HEAD all retain `AuthUser`.
- Frontend routes `/` → `landing_view` and `/@:handle` → `public_profile_view`: in this diff (app.rs); confirmed unguarded.
- No new auth layer: not modified; confirmed router uses only `TraceLayer` at HEAD.

## Output
`SUBTASK_ac1-verify/verdict-ac1.md` — written with `ac_1_verdict: PASS`.
