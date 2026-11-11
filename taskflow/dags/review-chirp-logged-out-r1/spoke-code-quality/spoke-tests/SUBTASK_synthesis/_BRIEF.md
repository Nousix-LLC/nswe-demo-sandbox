# Task: spoke-tests Synthesis Gate

## Task Specification

**Slug**: SUBTASK_synthesis
**Task Kind**: synthesis
**Depends on**: SUBTASK_handler-unit-tests, SUBTASK_integration-tests, SUBTASK_frontend-test-validity
**Status**: Pending

### Objective

This task is a verification gate. It reads the three concern analyses, confirms each concern
(1, 2, 5) is explicitly covered, and assembles the results into `../FINDINGS.md` conforming
to `../../contracts/findings_schema.md`.

### Context

Synthesis gate for the `spoke-tests` decomposition. See `../_GLOBAL.md`.
The parent spoke's declared output is `spoke-tests/FINDINGS.md`.

---

## Input Specification

| Input | Source | Purpose |
|-------|--------|---------|
| Hub context | `../_GLOBAL.md` | Concern assignments, ownership table |
| Parent findings schema | `../../contracts/findings_schema.md` | FINDINGS.md structure |
| This level's analysis schema | `../contracts/analysis_schema.md` | Intermediate analysis format |
| Concern 1 analysis | `../SUBTASK_handler-unit-tests/analysis.md` | Handler unit test findings |
| Concern 2 analysis | `../SUBTASK_integration-tests/analysis.md` | Integration test findings |
| Concern 5 analysis | `../SUBTASK_frontend-test-validity/analysis.md` | Frontend test validity findings |

---

## Process Specification

This task is a verification gate — not a prose summary. Run the following checks before
assembling the output:

**Check 1 — Coverage**: Every concern (1, 2, 5) has a Verdict in an analysis spoke output.
No concern is absent or silently skipped.

**Check 2 — Schema compliance**: Each `analysis.md` has the sections required by
`../contracts/analysis_schema.md`: Verdict, Findings (if any), Evidence.

**Check 3 — Finding quality**: Each finding in the analysis outputs cites a file path,
line number, and the pinned commit. No finding is at the level of suspicion without evidence.

**Check 4 — Assembly into FINDINGS.md**: Merge outputs using the structure from
`../../contracts/findings_schema.md`:
- `## Verdict`: PASS if all 3 concern analyses are CLEAN; FINDINGS if any has findings
- `## Findings`: one numbered subsection per finding from the 3 analyses (if any),
  renumbered sequentially (Finding 1, Finding 2, …); include Concern N tag in each entry
- `## Clean Account`: one bullet per concern (1, 2, 5) stating what was checked and what
  was found — either clean or a reference to the finding(s)

If checks 1–3 reveal a gap (missing coverage, missing evidence, missing section), record the
gap explicitly in the Clean Account rather than papering over it.

---

## Output Specification

**Primary output:**

| Attribute | Value |
|-----------|-------|
| Filename | `FINDINGS.md` |
| Format | Markdown |
| Location | `../` (parent spoke-tests workspace) |

Structure: exactly per `../../contracts/findings_schema.md`.

**Lifecycle artifacts** (this workspace):
- `SYNTHESIS.md` — fold record for this synthesis task
- `COMPLETE.md` — completion record

---

## Success Criteria

- `../FINDINGS.md` exists and conforms to `../../contracts/findings_schema.md`
- Concerns 1, 2, and 5 each appear in the Clean Account section
- Each finding (if any) cites file, line, and pinned commit
- No concern silently omitted
- Prose passes the plain-voice bar from `../../contracts/findings_schema.md`

---

## Suggested Methodology Files

Domain Mapping match: **Synthesizing / verifying a hub-and-spoke decomposition** →
Primary: `Synthesis`, Supporting: `Code Review`

Specific files:
- `synthesis/Synthesis_Overview_Methodology.md` — the four-check model; run it as the
  gate for this decomposition
- `synthesis/Synthesis_Contract_Verification_Methodology.md` — verify contracts are honored
  in each spoke output
- `synthesis/Synthesis_Wiring_Verification_Methodology.md` — verify all three analysis
  outputs are present and reference the correct concerns
- `code-review/CodeReview_Checklist_Methodology.md` — reviewing the assembled FINDINGS.md
  before finalizing

These are the parent's suggested starting point. Load fewer if one is clearly inapplicable;
load more if the brief reveals additional methodology surface needed.

## Out-of-Scope

- Re-doing any concern analysis — that work is complete in the spoke outputs; this gate
  reads and verifies them, it does not re-execute them
- Synthesis bundle's Decomposition content (belongs to the spoke tasks, not the gate)

## Inherited Constraints

- Findings cite file path and line number at pinned commit
  `decb6196c2c1e6ed421d393a642f0c844cc333ba`
- No host paths, private IPs, or infrastructure details in any output
- Prose bar: no moral adjectives on technical things, no narrated candor, no slot-fill templates
- Repository: `Nousix-LLC/nswe-demo` only
