# _BRIEF.md — chirp-logged-out-r18

**Goal**: Complete the logged-out visitor experience for `Nousix-LLC/nswe-demo` — public timeline, public
user profiles, accurate landing states — and produce a root-level `SYNTHESIS.md` accounting for all five
acceptance criteria.

**Issue covered**: #35 — "Logged-out reading and a useful landing with accurate states"

---

## Acceptance criteria (from issue #35)

- **AC-1**: A logged-out visitor can load the home/public timeline and open a user profile and read chirps
  without being forced to sign up or sign in first. (`REQ-PROD-013`, `BAR-011`)
- **AC-2**: On arrival with no content, the visitor sees a clear statement of what chirp is plus an obvious
  way to sign up or sign in — never a blank page or an unexplained error. (`REQ-PROD-014`, `BAR-011`)
- **AC-3**: If the timeline fails to load, a clear, recoverable error message is shown instead of a broken
  screen. (`REQ-PROD-014`, `BAR-011`)
- **AC-4**: A "create an account" route is visible on the landing and on the sign-in screen, and following
  it reaches sign-up. (`REQ-PROD-015`, `BAR-011`)
- **AC-5**: The logged-out landing/timeline exercises its loading, empty, error, and end-of-list states
  accurately and distinctly. (`REQ-UX-002/030/031/032`, `BAR-011`, one-state-model criterion)

---

## Inputs / branch state

- **Repository**: `Nousix-LLC/nswe-demo`
- **Branch**: `work/chirp-logged-out`
- **Head**: `21dca556301a58c5ae286509a797a6c202225c71`
- **PR**: #263 (open, mergeable) — "feat: logged-out public timeline and user profiles (#35)"
- **CI**: Run 42173990246 — 6/6 ALL PASS on head `21dca556`

### What is already on the branch (do not redo or revert)

r10 pushed the backend APIs (`eaf96cf`) and frontend routes (`e02b1d8a`). r11 pushed a fix commit
(`fed1fc8e`). r12 pushed the AC-4 sign-up form (`21dca556`). These commits are already on the branch; the
task is to verify or complete AC-1 through AC-5, fix any gaps found, and synthesize.

---

## Stall history and the critical requirement

r13 through r17 were each dispatched on this same branch head (`21dca556`) and each **stalled without
producing a `SYNTHESIS.md`**. This is the defining pattern: the DAGs ran, did not push new commits, and did
not produce a synthesis record. That is what must not happen again.

**Critical requirement: this DAG MUST produce a root-level `SYNTHESIS.md` as its final act, even if the
synthesis is a report that some ACs are partially met and some gaps remain.** A synthesis that honestly
reports partial progress is infinitely more useful than stalling without one. The synthesis must account for
each of AC-1 through AC-5 — met, partially met, or not met, with evidence.

Do NOT stall without synthesizing. If the work reaches a point where further progress is blocked, write
the synthesis with what is known and mark the blocked items as such — that is a successful synthesis.

---

## Declared output

- Commits on `work/chirp-logged-out` closing any remaining gaps (may be zero new commits if the branch
  already satisfies all five ACs and only synthesis was missing)
- PR #263 updated (or no-op if already up to date)
- **`taskflow/dags/chirp-logged-out-r18/SYNTHESIS.md`** at the DAG root — verdict `PASS` or `FAIL`, with
  per-AC status and evidence for each of AC-1 through AC-5

---

## Concerns to cover

1. **AC verification**: For each of AC-1 through AC-5, assess whether the current branch code meets the
   criterion. Read the source under `crates/chirp-frontend/` and `crates/chirp-server/` on the branch.

2. **Gap completion**: If an AC is not met, implement the missing piece. The design references are:
   - `design/product-requirements.md` §3 and §4 (`REQ-PROD-013`, `REQ-PROD-014`, `REQ-PROD-015`)
   - `design/experience-design.md` §1, §2, §6 (`REQ-UX-002`, `REQ-UX-030`, `REQ-UX-031`, `REQ-UX-032`)
   - `design/release-bar.md` §C (`BAR-011`)

3. **Synthesis**: Produce `SYNTHESIS.md` before concluding. It must state a verdict (PASS or FAIL), list
   AC-1 through AC-5 with their status (met / partially met / not met) and brief evidence. This is not
   optional — it is the DAG's deliverable.

---

## Constraints

- Branch: `work/chirp-logged-out` only. No force-push.
- Scope: `crates/chirp-frontend/`, `crates/chirp-server/`, `crates/chirp-types/` only. No other crates.
- Do not revert or modify commits already on the branch (`eaf96cf`, `e02b1d8a`, `fed1fc8e`, `21dca556`)
  unless you find a defect that must be corrected.
- Repository scope: `Nousix-LLC/nswe-demo`. Do not reference host paths in any committed file or PR text.
