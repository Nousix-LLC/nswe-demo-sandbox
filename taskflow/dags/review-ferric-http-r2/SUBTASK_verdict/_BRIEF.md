# SUBTASK_verdict: Final Verdict and Synthesis

## Task Specification

**Slug**: SUBTASK_verdict  
**Task Kind**: synthesis  
**Depends on**: SUBTASK_correctness, SUBTASK_code_quality, SUBTASK_security  
**Status**: Pending

### Objective

Integrate the findings from all three concern spokes, produce a final APPROVE or REQUEST-CHANGES verdict for PR #210, post the verdict as a review comment on the PR, file any new non-blocking findings as GitHub issues, and author `SYNTHESIS.md` as the authoritative record.

This task is the **verification gate** for the review-ferric-http-r2 subtree. It asserts the identities in `../contracts/_MANIFEST.yaml` and either passes (APPROVE) or fails (REQUEST-CHANGES) based on whether any BLOCKER findings remain unresolved.

### Context

This is the synthesis task in review-ferric-http-r2. See `../_GLOBAL.md` for full background, blocker/should-fix definitions, and subtree constraints.

**Depends on**: SUBTASK_correctness, SUBTASK_code_quality, SUBTASK_security  
**Dependents**: none — this is the terminal gate

---

## Input Specification

### Required Inputs

| Input | Source | Purpose |
|-------|--------|---------|
| Project context | `../_GLOBAL.md` | Full background, identities to assert |
| Contract manifest | `../contracts/_MANIFEST.yaml` | Identities to verify before accepting |
| Findings schema | `../contracts/findings_schema.yaml` | Expected structure to validate against |
| Correctness findings | `../SUBTASK_correctness/correctness_findings.md` | B1, B2, SF3, SF4, SF5 resolution status |
| Code quality findings | `../SUBTASK_code_quality/code_quality_findings.md` | CHANGELOG structure assessment |
| Security findings | `../SUBTASK_security/security_findings.md` | Information hygiene assessment |
| PR #210 | `gh pr view 210 --repo Nousix-LLC/nswe-demo` | PR details needed for review comment |

---

## Process Specification

This task runs as a **verification gate**. The four-check model applies:

1. **Contract verification**: Assert that every declared identity in `../contracts/_MANIFEST.yaml` holds across the three findings files. If any identity fails (e.g., a blocker exists alongside an APPROVE verdict contribution), record it.

2. **Wiring verification**: Confirm that every declared output file exists and contains the required sections (per `../contracts/findings_schema.yaml`). If any spoke output is missing or malformed, raise a BLOCKER.

3. **Correctness gate**: Does any spoke contribute REQUEST-CHANGES? If yes, the overall verdict is REQUEST-CHANGES. Identify the specific blocker(s).

4. **Synthesis**: Compile the findings into a coherent verdict comment and SYNTHESIS.md. The verdict comment must:
   - State APPROVE or REQUEST-CHANGES clearly
   - For each of B1, B2, SF3, SF4, SF5: state its resolution status and the evidence
   - For each concern area (Correctness, Code Quality, Security): say what was checked and found
   - Any new non-blocking findings stated as numbered items

**Verdict logic:**
- If any BLOCKER finding appears in ANY spoke output: REQUEST-CHANGES
- If all three spokes contribute APPROVE and no BLOCKER findings exist: APPROVE

**After producing the verdict comment text:**
- Post it on PR #210: `gh pr review 210 --repo Nousix-LLC/nswe-demo --comment --body "..."` (use `--comment` since the PR author may be the same account; a `--approve` or `--request-changes` formal review should be attempted first, falling back to `--comment` if the platform rejects it)
- For any new ADVISORY or SHOULD_FIX finding not covered by an existing open issue: file as `gh issue create --repo Nousix-LLC/nswe-demo --title "..." --body "..."`
- Write `SYNTHESIS.md` at the parent workspace root (`../SYNTHESIS.md`)

**SYNTHESIS.md must contain:**
- Verdict line: `## Verdict: APPROVE` or `## Verdict: REQUEST-CHANGES`
- Per-blocker resolution: B1, B2 — RESOLVED or UNRESOLVED
- Per-should-fix resolution: SF3, SF4, SF5 — RESOLVED or UNRESOLVED or PARTIAL
- Concern-by-concern account: what was checked and found for Correctness, Code Quality, Security
- Any new blockers or non-blocking findings
- Link to the posted review comment (if obtainable)

**Prose bar**: All review text (comment, SYNTHESIS.md) must be in a plain human voice. Run the avoid-ai-writing checklist before finalizing: no moral/character adjectives glued to technical objects ("honest" metrics, "genuine" reliability), no narrated candor ("stated plainly", "to be honest"), no unnamed contrast pairs, no slot-fill templates, no padding to a rhythmic three, no inflated filler (seamless, robust, comprehensive, leverage). Check against `references/patterns.md` P0/P1 patterns if that file exists in the repo.

---

## Output Specification

**Primary output**: `../SYNTHESIS.md` (at the parent workspace root — the fold record)  
**Additional actions**: Review comment posted on PR #210; new GitHub issues filed for new ADVISORY/SHOULD_FIX findings

---

## Success Criteria

- [ ] All three spoke findings files read and verified against schema
- [ ] Contract identities in `../contracts/_MANIFEST.yaml` asserted
- [ ] Verdict (APPROVE or REQUEST-CHANGES) determined with explicit rationale
- [ ] Review comment posted on PR #210 (or attempted — record result)
- [ ] New non-blocking findings filed as GitHub issues (if any)
- [ ] `../SYNTHESIS.md` written with all required sections
- [ ] Prose bar checked: no machine-writing tells in published text

---

## Suggested Methodology Files

**Task-type row (from Domain Mapping):** "Synthesizing / verifying a hub-and-spoke decomposition" — Primary: Synthesis; Supporting: Code Review, Code Quality

Suggested files:
- `synthesis/Synthesis_Overview_Methodology.md` — the four-check model and gate pass/fail decision. **Always load this first.** Rationale: this task IS a verification gate; Synthesis_Overview defines its behavior.
- `synthesis/Synthesis_Contract_Verification_Methodology.md` — verify that the spoke outputs satisfy the declared identities. Rationale: `../contracts/_MANIFEST.yaml` declares identities this task must assert.
- `synthesis/Synthesis_Wiring_Verification_Methodology.md` — verify all outputs are present and wired. Rationale: confirms that every spoke produced its declared output before proceeding.
- `code-review/CodeReview_Process_Methodology.md` — the review process framework; writing the verdict comment. Rationale: the task posts a review comment that must follow review quality standards.
- `code-review/CodeReview_Feedback_Guidelines_Methodology.md` — how to write actionable, courteous findings. Rationale: the posted comment is external-facing reviewer output.

These are suggestions. Load the Synthesis files first. Load Code Review files for the comment authoring phase. Load fewer if some are clearly inapplicable.

## Inherited Constraints

- Repo: `Nousix-LLC/nswe-demo`
- Verdict must be binary: APPROVE or REQUEST-CHANGES
- SYNTHESIS.md goes at `../SYNTHESIS.md` (the fold location, NOT inside this task's workspace)
- Do not expose server addresses, SSH key paths, or internal host paths in the review comment, SYNTHESIS.md, or any filed issue
- The posted PR comment is a PUBLIC artifact — apply output hygiene rigorously
- If `gh pr review --approve` fails (same account as PR author), fall back to `gh pr review --comment`

## Out-of-Scope Methodologies

- Decomposition methodology — this is a synthesis gate, not a decomposer
- Rust-specific methodology — signature verification was done by SUBTASK_correctness
