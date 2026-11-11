# Task: Synthesis Gate — Combine Concern Findings into FINDINGS.md

## Task Specification

**Slug**: child-synthesis
**Task Kind**: synthesis
**Depends on**: child-dead-code, child-hydrate-scope
**Status**: Pending

### Objective

This task is a **verification gate**. Read the per-concern findings from the two analysis
children, verify that concerns 6 and 7 are covered with definitive verdicts, and produce
the final `spoke-code-health/FINDINGS.md` conforming to the parent schema.

This is not a prose summary. The gate checks:
1. Both concern findings are present and have definitive verdicts
2. Each finding entry has location (file + line at pinned commit), principle, severity, and
   satisfying condition
3. No internal host paths, private IPs, or infrastructure details appear in any finding
4. Prose passes the plain-voice bar

If any check fails, the gate FAILS and must schedule a remediation fix-task via
`engine_amend_plan { add_task }` before reporting failure.

### Context

This task synthesizes `child-dead-code/finding_c6.md` (concern 6) and
`child-hydrate-scope/finding_c7.md` (concern 7) into the single `spoke-code-health/FINDINGS.md`
declared by the parent spoke `spoke-code-health`.

See `../_GLOBAL.md` for subtree context. See `../contracts/_MANIFEST.yaml` for ownership and
identities this gate must assert.

**Pin commit**: `decb6196c2c1e6ed421d393a642f0c844cc333ba`

---

## Input Specification

### Required Inputs

| Input | Source | Purpose |
|-------|--------|---------|
| Subtree hub | `../_GLOBAL.md` | Concern assignments, identity assertions |
| Contracts manifest | `../contracts/_MANIFEST.yaml` | Ownership and identities |
| Parent findings schema | `../../contracts/findings_schema.md` | FINDINGS.md structure |
| Concern finding schema | `../contracts/concern_finding_schema.md` | Per-concern file structure |
| Concern 6 finding | `../child-dead-code/finding_c6.md` | Dead-code reachability findings |
| Concern 7 finding | `../child-hydrate-scope/finding_c7.md` | hydrate.rs scope/sync findings |

---

## Process Specification

### Four-Check Gate

**Check 1 — Coverage**: Both concern files exist and each covers exactly its assigned concern.
Fail if `finding_c6.md` or `finding_c7.md` is absent or empty.

**Check 2 — Completeness of findings**: Every `## Finding` entry has all required fields:
location (file + line at pinned commit), principle at stake, why it matters, severity, and
satisfying condition. Fail if any field is absent or vague ("somewhere in the file").

**Check 3 — No leaked infrastructure details**: No finding contains host paths, private IPs,
SSH config, or server-side paths. Fail if any are present.

**Check 4 — Prose bar**: No finding text contains moral/character adjectives on technical things,
narrated candor, unnamed contrast pairs, slot-fill templates, or inflated filler.

If all four checks pass: write `FINDINGS.md` as a PASS or FINDINGS verdict based on what the
per-concern files report, and complete.

If any check fails: schedule a remediation fix-task (amend plan), write `FINDINGS.md` as a
placeholder noting the gate failure, and fail with the gap documented.

### Assembling FINDINGS.md

After the gate passes, assemble `spoke-code-health/FINDINGS.md` as follows:
1. `## Verdict`: PASS if no findings in either concern file; FINDINGS if at least one finding
2. `## Findings`: copy and renumber all `### Finding` entries from both concern files, in
   concern-number order (concern 6 findings first, then concern 7 findings)
3. `## Clean Account`: one bullet per concern (6 and 7), stating what was checked and what was
   found, referencing any Finding entries by number

### Methodology

Domain Mapping match: **Synthesizing / verifying a hub-and-spoke decomposition** → Primary:
`Synthesis`, Supporting: `Code Review`, `Code Quality`

Suggested methodology files:
- `synthesis/Synthesis_Overview_Methodology.md` — gate model, four-check framework (always load first)
- `synthesis/Synthesis_Contract_Verification_Methodology.md` — verify the two concern findings
  cover the declared concerns per the contracts manifest
- `synthesis/Synthesis_Wiring_Verification_Methodology.md` — verify all findings are wired
  into FINDINGS.md (no detached finding left in a child file)
- `synthesis/Synthesis_Code_Review_Methodology.md` — combined prose and content quality review

These are suggested starting points. The child agent is the final judge of what the work requires.

---

## Output Specification

| Attribute | Value |
|-----------|-------|
| Filename | `FINDINGS.md` |
| Format | Markdown |
| Location | `../` (i.e., `spoke-code-health/FINDINGS.md`) |
| Fold record | `../COMPLETE.md` (this task's terminal record and the fold seam) |

Structure: per `../../contracts/findings_schema.md`.

Required sections in FINDINGS.md:
1. `## Verdict` (PASS or FINDINGS)
2. `## Findings` (required when at least one finding; omit when PASS)
3. `## Clean Account` (one bullet per concern: 6 and 7)

---

## Success Criteria

- All four gate checks pass
- `spoke-code-health/FINDINGS.md` exists and conforms to the parent schema
- Both concerns 6 and 7 appear in the Clean Account
- If any finding exists: location is at pinned commit `decb6196c2c1e6ed421d393a642f0c844cc333ba`
- Prose passes the plain-voice bar throughout

---

## Suggested Methodology Files

Domain Mapping match: **Synthesizing / verifying a hub-and-spoke decomposition** →
Primary: `Synthesis`, Supporting: `Code Review`, `Code Quality`

Specific files:
- `synthesis/Synthesis_Overview_Methodology.md` — anchor; always load first; defines the gate model
- `synthesis/Synthesis_Contract_Verification_Methodology.md` — concern coverage verification
- `synthesis/Synthesis_Wiring_Verification_Methodology.md` — wiring findings into the output
- `synthesis/Synthesis_Code_Review_Methodology.md` — prose and quality review of combined output
- `synthesis/Synthesis_Remediation_Methodology.md` — remediation path if gate checks fail

These are suggested starting points. The child agent is the final judge of what the work requires.

## Inherited Constraints

- Findings in FINDINGS.md point at repository file paths and line numbers at pinned commit
  `decb6196c2c1e6ed421d393a642f0c844cc333ba`
- No host paths, private IPs, or infrastructure details in FINDINGS.md
- Do not post to the PR
- Prose in FINDINGS.md must pass the plain-voice bar
- Repository: `Nousix-LLC/nswe-demo` only

## Out-of-Scope

- Re-doing the analysis — take the per-concern findings as inputs, do not re-read the source code
- Adding concerns beyond 6 and 7
- Writing REVIEW.md — that is `spoke-synthesis`'s task (the parent spoke-code-quality's synthesis)
