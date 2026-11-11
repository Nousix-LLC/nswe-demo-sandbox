# _BRIEF.md — remediate-design-ferric-1_0-r1

**DAG kind**: coder (remediation of design documents)
**Branch**: `work/design-ferric-1_0`
**PR**: #128 — "design: Ferric 1.0 framework design"
**Repo**: Nousix-LLC/nswe-demo

---

## Objective

Clear the 5 BLOCKING findings identified by design-ferric-1_0-r3 in `design/ferric/release-bar.md`.
All 5 findings are in Concern 2 (release bar testability). No structural design changes are needed —
each finding is a targeted edit to `design/ferric/release-bar.md` to make each criterion mechanically
checkable by an outside reviewer.

## Background

PR #128 received a design gap review verdict of REQUEST-CHANGES from design-ferric-1_0-r3. The review
identified 5 BLOCKING criteria in `design/ferric/release-bar.md` that an outside reviewer cannot
produce a pass/fail determination for as written. The review is posted at:
https://github.com/Nousix-LLC/nswe-demo/pull/128#pullrequestreview-5747989451

The full findings are in: `taskflow/dags/design-ferric-1_0-r3/SYNTHESIS.md`

## Acceptance criteria

Each of the 5 BLOCKING criteria, after your edits, must be mechanically checkable — an outside
reviewer can produce a pass/fail determination without ambiguity:

1. **BAR-FERRIC-001** (backward compatibility, ferric core): the criterion names a specific version
   anchor — a named git tag (e.g. `v0.1.0-usable_early`) or the earliest published crates.io version,
   or enumerates the frozen prelude items explicitly in the compatibility policy (BAR-FERRIC-029).

2. **BAR-FERRIC-003** (HTML sanitization): the criterion names a specific sanitizer (e.g. the Rust
   `ammonia` crate) and states the exact assertion (e.g. "output is unchanged after `ammonia::clean`"),
   and the automated verification test specifies what it checks.

3. **BAR-FERRIC-006** (hydration mismatch detection): the criterion specifies the observable outcome
   for both detection and recovery when client-rendered structure diverges from server HTML — e.g.
   "in development builds, Ferric logs a warning to the browser console identifying the mismatched
   node; in production builds, the mismatch triggers a full client-side re-render of the affected
   subtree." The `example_build` verification step names the expected observable result when a
   deliberate mismatch is induced.

4. **BAR-FERRIC-015** (backward compatibility, ferric-router): the criterion names the same kind of
   version anchor as BAR-FERRIC-001, applied to `ferric-router`.

5. **BAR-FERRIC-017** (backward compatibility, ferric-http): the criterion names the same kind of
   version anchor as BAR-FERRIC-001, applied to `ferric-http`.

## Scope

- **In scope**: Edits to `design/ferric/release-bar.md` to address the 5 BLOCKING findings.
  If any cross-references to other design files are needed for consistency (e.g. a compatibility policy
  section in another file), those files may be updated.
- **Out of scope**: Design direction changes, implementation changes, changes to the codebase, changes
  to the 36 Ferric 1.0 feature issues (#129–#164), the 16 non-blocking findings (#165–#179).

## Inputs

- `design/ferric/release-bar.md` — the primary file to edit (in the repository, on `work/design-ferric-1_0`)
- `taskflow/dags/design-ferric-1_0-r3/SYNTHESIS.md` — the BLOCKING findings with full context and
  resolution guidance
- The existing design files for context: `design/ferric/` directory

## Declared output

- Commits on branch `work/design-ferric-1_0` fixing the 5 BLOCKING findings
- PR #128 updated with the new commits
- `SYNTHESIS.md` at this workspace root with verdict (APPROVE if all 5 are cleared, REQUEST-CHANGES
  if blockers remain) and a brief per-finding status

## Concerns to evaluate

1. **Each BLOCKING criterion addressed**: Verify each of the 5 criteria is now mechanically checkable
   per its resolution guidance.
2. **No regressions**: The edits do not introduce new ambiguities or remove any existing clear criteria.
3. **Consistency**: Cross-references within release-bar.md and to other design files remain intact.

## Notes

- Commit messages and PR comments are written for repository readers — no host paths, taskflow
  internals, or agent/methodology names.
- No attribution trailers on commits or PR comments.
- The `swe-coder` identity writes the edits; load methodologies as the work requires.
