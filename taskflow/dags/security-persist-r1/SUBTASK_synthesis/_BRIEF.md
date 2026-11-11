# Task: Synthesis — Verify Security Fixes and Open PR

## Task Specification

**Slug**: SUBTASK_synthesis  
**Task Kind**: synthesis  
**Depends on**: SUBTASK_ssl_manifest  
**Status**: Pending  
**Assigned To**: swe-coder

### Objective

This task is a **verification gate**, not a prose summary. It verifies that both security fixes
are correctly implemented on the branch, that no plaintext credential path or `PGSSLMODE: disable`
remains, that CI is green, and then opens the GitHub PR for `work/security-persist-r1` → `main`
referencing issue #120. It folds the parent (`security-persist-r1`) SUSPENDED → COMPLETED by
authoring `SYNTHESIS.md` at the parent workspace and calling `engine_resume_suspended`.

### Context

This is the synthesis gate (spoke 3 of 3) in the `security-persist-r1` subtree (see parent
`_GLOBAL.md`). Both security spokes have completed and pushed to `work/security-persist-r1`.

**Dependencies**: `SUBTASK_ssl_manifest` (which transitively covers `SUBTASK_credential_hashing`)  
**Dependents**: none (terminal)

---

## Input Specification

### Required Inputs

| Input | Source | Purpose |
|-------|--------|---------|
| Subtree hub | `../_GLOBAL.md` | Success criteria, repo facts, PR audience |
| Subtree contract | `../contracts/_MANIFEST.yaml` | Identity assertions to verify |
| Credential hashing output | `../SUBTASK_credential_hashing/COMPLETE.md` | Confirms changes, commit SHA |
| SSL manifest output | `../SUBTASK_ssl_manifest/COMPLETE.md` | Confirms changes, commit SHA |
| Branch state on GitHub | `gh api` / `git show` | Verify commits are on `origin/work/security-persist-r1` |

---

## Process (Four-Check Gate)

Run the four checks. Any check that FAILS triggers a `engine_amend_plan { add_task }` inject to
schedule a remediation task rather than forcing this synthesis to proceed with incomplete work.
All four checks MUST pass for the gate to be declared PASS.

### Check 1 — Behavioral Contract Verification

Verify that the code changes satisfy the security fix contract:

- Grep `crates/chirp-server/src/repository/postgres.rs` and `in_memory.rs` for `stored == secret`
  — must return empty (if not: FAIL, inject fix task)
- Grep those files for `argon2` (import or usage) — must be non-empty (if not: FAIL)
- Grep `deploy/chirp/50-transient-sweep-cronjob.yaml` for `PGSSLMODE` — must show `require`,
  not `disable` (if not: FAIL, inject fix task)
- Grep `crates/chirp-server/Cargo.toml` for `argon2` — must be present (if not: FAIL)

### Check 2 — Wiring Verification

Verify that the combined commit history on `work/security-persist-r1` contains both commits
(one from credential hashing, one from SSL manifest), and that `origin/main` is an ancestor
(i.e. the branch is based on current main with no divergence).

### Check 3 — Duplication / Overlap Detection

Confirm the two spokes touched non-overlapping files (no merge conflicts are latent):
- Credential hashing: `crates/**`
- SSL manifest: `deploy/**`
These are structurally disjoint — verify no file appears in both spoke commits.

### Check 4 — Synthesis Code Review

Review the combined diff on the branch:
- argon2 hashing is used with a fresh salt per credential (not a fixed salt)
- `PasswordVerifier::verify_password` is called for verification (not `==`)
- `complete_account_recovery` path in `postgres.rs` is updated (not just `set_credential`)
- Stale doc comments saying "stored verbatim" are updated
- The CronJob comment is updated (no longer says "TLS is a follow-up")
- No plaintext secrets or credentials in the diff

If all four checks PASS, proceed to open the PR.

---

## Output Specification

### Primary Output

| Attribute | Value |
|-----------|-------|
| File | `SYNTHESIS.md` (fold record — authored at **parent** workspace `../SYNTHESIS.md`) |
| Format | Markdown |

### SYNTHESIS.md contents

- Gate verdict (PASS / FAIL with specific failures listed)
- Check 1–4 outcomes
- PR URL (once opened)
- Commit SHAs from both spokes
- Identity assertions from `contracts/_MANIFEST.yaml` and whether each holds

After authoring `../SYNTHESIS.md`, call `engine_resume_suspended` to fold the parent
`SUSPENDED → COMPLETED`.

### PR Description

Open with `gh pr create --base main --head work/security-persist-r1`, using:
- Title: `fix(security): credential KDF + constant-time verify, sslmode=require (#120)`
- Body: describe both fixes, note that existing plaintext credential rows are invalidated (if a
  migration was added), confirm CI status, close issue #120 with "Closes #120"
- End the body with: `🤖 Generated with [Claude Code](https://claude.com/claude-code)`

---

## Success Criteria

- [ ] All four checks pass (or failing checks have a scheduled remediation inject)
- [ ] PR opened against `main` from `work/security-persist-r1`
- [ ] PR body references issue #120 and closes it
- [ ] `SYNTHESIS.md` authored at parent workspace (`../SYNTHESIS.md`)
- [ ] `engine_resume_suspended` called to fold the parent

---

## Suggested Methodology Files

**Task type match**: "Synthesizing / verifying a hub-and-spoke decomposition" → primary: `synthesis`, supporting: `code-review`, `code-quality`; "PR creation and management via gh CLI" → primary: `operations`, supporting: `code-review`

**Specific files to load**:
- `synthesis/Synthesis_Overview_Methodology.md` — the four-check gate model, pass/fail decision, `SYNTHESIS.md` schema. **Rationale**: this task IS a synthesis gate; the methodology defines what it means to be one.
- `synthesis/Synthesis_Contract_Verification_Methodology.md` — Check 1 mechanics (behavioral contract). **Rationale**: the contract in `../contracts/_MANIFEST.yaml` declares the identities this task verifies.
- `synthesis/Synthesis_Wiring_Verification_Methodology.md` — Check 2 mechanics. **Rationale**: verify both commits are on the branch.
- `synthesis/Synthesis_Code_Review_Methodology.md` — Check 4 mechanics (combined-output review). **Rationale**: reviewing the combined security diff for correctness.
- `operations/GitWorkflow_PR_Lifecycle_Methodology.md` — PR creation conventions via `gh pr create`. **Rationale**: opening the PR is the terminal deliverable of this gate.

*These are the parent's flagged methodologies based on the task type. The child agent SHOULD load these as a starting point but is the final judge of what its work requires — load fewer if some are clearly inapplicable; load more if the child's own reading of the brief reveals additional methodology surface the parent did not anticipate.*

## Inherited Constraints

- The synthesis gate MUST fail (and schedule remediation) if any check fails — do not silently pass a failing check.
- PR must reference and close issue #120.
- Never force-push to `main`.
- SYNTHESIS.md must be authored at `../SYNTHESIS.md` (the parent's workspace), not at this subtask's workspace.
- `engine_resume_suspended` must be called AFTER authoring `../SYNTHESIS.md`.

## Out-of-Scope Methodologies

- `synthesis/Synthesis_Duplication_Detection_Methodology.md` — the two spokes own structurally disjoint file trees (`crates/` vs `deploy/`); cross-spoke duplication detection is not relevant here.
- `synthesis/Synthesis_Remediation_Methodology.md` — only needed if checks fail; load on demand if a remediation inject is required.
