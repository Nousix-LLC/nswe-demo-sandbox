# SUBTASK_placement_analysis: Placement Findings

Repo: `Nousix-LLC/nswe-demo` — PR #210 (`work/ferric-http-r1` → `main`, head `0436218`)
Schema: `../contracts/sub_spoke_findings_schema.yaml`

---

## Concern Covered

Concern 2 (placement correctness)

---

## Findings

**[CLEAN] Unreleased entries under the Unreleased section**: The `usable_early` API surface
documentation — all types, methods, acceptance-criteria table, and deferred-items note — is placed under
`## Unreleased — usable_early surface (#148)`, the topmost section of the CHANGELOG. This is the correct
target for unreleased work. No entry from either commit lands outside this section.

- Principle: Keep a Changelog convention — new entries for unreleased work belong in the `[Unreleased]`
  block, not in a released version block.
- Evidence: PR diff shows the entire `crates/ferric-http/CHANGELOG.md` created as a new file; the
  `usable_early` surface entries occupy the first section (`## Unreleased — usable_early surface (#148)`).
  Commit `d6a9b6eb` authored both sections; commit `0436218` modified only content within the Unreleased
  section (corrected API signatures for `query()`, `Response::text()`, `header()`/`default_header()`, and
  added missing API members).
- Resolution: No action required.

**[CLEAN] Remediation commit does not place entries in a released version section**: The remediation
commit (`0436218`) makes corrections exclusively within `## Unreleased — usable_early surface (#148)`.
It does not introduce or modify any released version block.

- Principle: A remediation fixing documentation errors in an in-flight PR MUST NOT write into released
  version sections, whose content records historical shipped state.
- Evidence: The CHANGELOG contains no released version blocks (no `## [x.y.z] - YYYY-MM-DD` headers).
  All changes by both commits are confined to the two sections created by the PR. The remediation commit
  message explicitly names the Unreleased section as its target ("correct API signatures in CHANGELOG.md").
- Resolution: No action required.

**[CLEAN] Version section ordering intact**: The `## Unreleased` section is at the top; the
`## Initial implementation (#6)` section is at the bottom. No ordering inversion is present.

- Principle: Keep a Changelog ordering — `[Unreleased]` first, then released versions from newest to
  oldest.
- Evidence: Lines 1–155 of the diff (the full file) show `## Unreleased — usable_early surface (#148)`
  preceding `## Initial implementation (#6)`. No section appears out of order.
- Resolution: No action required.
