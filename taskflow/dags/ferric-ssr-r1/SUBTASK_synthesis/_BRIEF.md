# _BRIEF.md — ferric-ssr-r1-synthesis

## Objective

Verify the complete SSR + hydration implementation, assemble the final branch, run the
identity assertions from `contracts/_MANIFEST.yaml`, and deliver: a GitHub PR closing issues
#223, #224, #226 (from branch `work/ferric-ssr-r1`) and the root `SYNTHESIS.md` accounting
for each issue.

This task is the synthesis gate. It runs after all three parallel spokes
(ferric-ssr-r1-server-render, ferric-ssr-r1-client-hydrate, ferric-ssr-r1-axum-integration)
have completed and committed to their respective branches.

## Inputs

- **Branches to assemble** (all based on the post-skeleton state of `work/ferric-ssr-r1`):
  - `work/ferric-ssr-r1-server` — server-render spoke output
  - `work/ferric-ssr-r1-client` — client-hydrate spoke output
  - `work/ferric-ssr-r1-axum` — axum-integration spoke output
- **Contract** (read-only): `contracts/_MANIFEST.yaml` — the identity assertions to run.
- **Brief** (read-only): `_BRIEF.md` — acceptance criteria for #223, #224, #226.

## Declared Output

1. **Branch `work/ferric-ssr-r1`** with all three spoke branches merged (disjoint ownership
   guarantees no conflicts). The branch is in a passing build state across all identities.

2. **GitHub PR** (repo `Nousix-LLC/nswe-demo`) from branch `work/ferric-ssr-r1`:
   - Title: concise summary of the SSR + hydration implementation
   - Closes #223, #224, #226 (using GitHub auto-close syntax)
   - Body describes: what was implemented, how it was verified (the identity assertions
     passed), which requirements are addressed, and the following mandatory sentence:
     "BAR-005 / #225 (state carry + async resource resume) is a follow-up issue dependent
     on #130 and is NOT part of this goal."
   - Body ends with: `🤖 Generated with [Claude Code](https://claude.com/claude-code)`
   - Body must NOT contain host paths, server IP addresses, SSH key paths, or taskflow
     internals.

3. **`taskflow/dags/ferric-ssr-r1/SYNTHESIS.md`** — structured account for each issue:
   - #223 (BAR-003): met / not met, evidence (test results, compilation check)
   - #224 (BAR-004): met / not met, evidence
   - #226 (BAR-006): met / not met, evidence (both mismatch detection and Axum integration)
   - Any known gaps, deviations, or items for follow-up

## Success Criteria (identity assertions from `contracts/_MANIFEST.yaml`)

All of the following must pass before creating the PR:

- **native-compile**: `cargo check --lib -p ferric` exits zero on native target.
- **wasm-compile**: `cargo check --target wasm32-unknown-unknown -p ferric` exits zero.
- **native-tests-pass**: `cargo test -p ferric` exits zero on native target.
- **chirp-server-compile**: `cargo build -p chirp-server` exits zero.
- **frozen-prelude-unchanged**: `git diff` on the four frozen files produces no output.
- **marker-format-agreement**: `grep -r 'TEXT_OPEN_MARKER\|<!--\$t-->' crates/ferric/src/ssr.rs`
  and `crates/ferric/src/hydrate.rs` both show the marker used. No other marker format.
- **issues-closed**: PR body includes "Closes #223", "Closes #224", "Closes #226" and the
  BAR-005 follow-up sentence.

If any identity assertion fails, record the failure in `SYNTHESIS.md` and do NOT create the
PR until the failure is resolved or escalated.

## Constraints

- Merge order: merge `work/ferric-ssr-r1-server`, then `work/ferric-ssr-r1-client`, then
  `work/ferric-ssr-r1-axum` into `work/ferric-ssr-r1`. Disjoint file ownership guarantees
  no merge conflicts; if conflicts appear, they signal an ownership violation — stop and
  record the finding in `SYNTHESIS.md` before escalating.
- Do not force-push to `main` or rewrite merged history.
- PR target base: `main`.
- Commit attribution: end commit messages with `Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>`.
- Security: no host paths, server IP addresses, SSH key paths, or cluster details in any
  committed file or PR content (per CLAUDE.md).
