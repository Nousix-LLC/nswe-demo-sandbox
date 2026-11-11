# _BRIEF.md — SUBTASK_synthesis

## Task Specification

**Slug**: SUBTASK_synthesis  
**Task Kind**: synthesis  
**Depends on**: SUBTASK_design-doc-review, SUBTASK_foundation-buildability, SUBTASK_ticket-review  
**Status**: Pending

### Objective

Synthesis and verification gate for the Ferric 1.0 design gap review.

Read the three spoke findings files. Assert the contract identities. Compile all findings into a final verdict. Post the verdict as a review comment on PR#128. File all non-blocking findings as board issues. Write the root `SYNTHESIS.md`.

This task is a verification gate — not a summary writer. Its job is to:

1. **Assert the contract identities** (from `contracts/_MANIFEST.yaml`): every finding has severity, every BLOCKING finding has a location, every non-blocking finding gets filed as a board issue.
2. **Determine the verdict**: `REQUEST-CHANGES` if any BLOCKING finding exists; `APPROVE` if all findings are non-blocking.
3. **Post the review comment** on PR#128 with: the verdict, a per-concern breakdown, and specific findings.
4. **File board issues** for every non-blocking finding (one issue per finding or one per cluster where the findings are closely related). Each issue should be labeled `design-review`, `type:enhancement` or appropriate labels, linked to PR#128.
5. **Write `SYNTHESIS.md`** at the parent workspace root (`taskflow/dags/design-ferric-1_0-r3/SYNTHESIS.md`).

If any identity assertion fails (e.g., a spoke's findings file is missing a required field), this task must note the gap and treat it as a non-blocking finding about the review process itself — it MUST NOT silently plug the failure or fabricate a missing field.

### Context

This task is part of the Ferric 1.0 design gap review (see `_GLOBAL.md` in the parent workspace at `taskflow/dags/design-ferric-1_0-r3/`).

**Depends on**: all three analysis spokes must reach COMPLETED before this task runs  
**Dependents**: none (this is the terminal task)

### Inputs

| Input | Source | Purpose |
|---|---|---|
| Parent hub | `taskflow/dags/design-ferric-1_0-r3/_GLOBAL.md` | Context, verdict rule, methodology posture |
| Contract manifest | `taskflow/dags/design-ferric-1_0-r3/contracts/_MANIFEST.yaml` | Identities to assert |
| Findings schema | `taskflow/dags/design-ferric-1_0-r3/contracts/findings_schema.yaml` | Schema for validation |
| Design doc findings | `taskflow/dags/design-ferric-1_0-r3/SUBTASK_design-doc-review/design-doc-findings.md` | Spoke 1 output |
| Buildability findings | `taskflow/dags/design-ferric-1_0-r3/SUBTASK_foundation-buildability/buildability-findings.md` | Spoke 2 output |
| Ticket findings | `taskflow/dags/design-ferric-1_0-r3/SUBTASK_ticket-review/ticket-findings.md` | Spoke 3 output |

### Process

1. Read all three spoke findings files.
2. Validate each against `findings_schema.yaml` — note any schema violations.
3. Assert each identity from `contracts/_MANIFEST.yaml` — note any violations.
4. Count BLOCKING findings across all spokes. If any: verdict = REQUEST-CHANGES. Otherwise: verdict = APPROVE.
5. Draft the PR review comment (plain text, no internal paths, no taskflow internals). The comment must include:
   - Explicit verdict line ("**APPROVE**" or "**REQUEST-CHANGES**")
   - Per-concern section (concerns 1–5) with what was checked and what was found
   - For REQUEST-CHANGES: each BLOCKING finding listed with location, statement, and what would resolve it
   - For non-blocking findings: listed under "Non-blocking findings (filed as issues below)"
6. Post the review comment on PR#128 via `gh pr review 128 --comment --body "..."` or `gh pr review 128 --approve --body "..."` (use `--approve` if APPROVE, `--comment` if REQUEST-CHANGES since REQUEST-CHANGES requires code changes).
7. File one GitHub issue per non-blocking finding (or per cluster). Use `gh issue create`. Each issue must:
   - Have a clear title referencing the design area
   - Reference PR#128 in the body
   - Have appropriate labels (at minimum `design-review`)
   - Not name internal host paths, taskflow paths, or internal addresses
8. Write `SYNTHESIS.md` at `taskflow/dags/design-ferric-1_0-r3/SYNTHESIS.md`.

### Output

| Artifact | Location | Role |
|---|---|---|
| `SYNTHESIS.md` | `taskflow/dags/design-ferric-1_0-r3/SYNTHESIS.md` | Terminal record for this node + synthesis fold record |
| PR#128 review comment | Posted to GitHub | Verdict and findings visible on the PR |
| Board issues (N) | Posted to GitHub | Non-blocking findings tracked on the board |

### SYNTHESIS.md structure

The `SYNTHESIS.md` at the parent workspace root serves as both this subtree's synthesis record and the terminal lifecycle artifact. It must contain:

- **Verdict**: APPROVE or REQUEST-CHANGES (clearly labeled)
- **Review URL**: direct URL to the posted PR review comment
- **Per-concern breakdown** (concerns 1–5): what was checked, what was found, findings with severity
- **BLOCKING findings** (if any): full list with location and recommendation
- **Non-blocking findings**: full list with issue URLs for each filed board issue
- **Identity assertion results**: confirmation that all contract identities held (or a note on any that did not)

### Acceptance Criteria

- All three spoke findings files read.
- Contract identities asserted with recorded outcomes.
- Verdict matches the identity rule (REQUEST-CHANGES iff BLOCKING findings exist).
- Review comment posted to PR#128 (URL recorded in SYNTHESIS.md).
- Every non-blocking finding filed as a board issue (issue URL recorded in SYNTHESIS.md).
- `SYNTHESIS.md` written at `taskflow/dags/design-ferric-1_0-r3/SYNTHESIS.md`.
- Nothing in the posted review comment or filed issues names host paths, taskflow internals, SSH keys, or internal network addresses.
