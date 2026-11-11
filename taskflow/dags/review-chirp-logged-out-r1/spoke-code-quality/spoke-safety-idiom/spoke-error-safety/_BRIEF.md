# Task: Concern 8 — Error Message Safety (AppError / user_message())

## Task Specification

**Slug**: spoke-error-safety
**Task Kind**: standard
**Depends on**: none
**Status**: Pending

### Objective

Assess whether error messages surfaced in the UI via `AppError`/`user_message()` expose
internal details — stack traces, internal server paths, raw database errors, SQL query text,
or any detail that aids an attacker or leaks implementation — in PR #263 on
`Nousix-LLC/nswe-demo` at pinned commit `decb6196c2c1e6ed421d393a642f0c844cc333ba`.

### Context

This task covers concern 8 from the parent code-quality review. It is part of a decomposition
of `spoke-safety-idiom` (see `../_GLOBAL.md`). The sibling `spoke-rust-idiom` runs concern 10
concurrently; `spoke-safety-synthesis` depends on both and produces the combined FINDINGS.md.

---

## Input Specification

### Required Inputs

| Input | Source | Purpose |
|-------|--------|---------|
| Hub context | `../_GLOBAL.md` | Subtree constraints, pinned commit, access instructions |
| Contract manifest | `../contracts/_MANIFEST.yaml` | Output ownership |
| Ancestor schema | `../../../contracts/findings_schema.md` | FINDINGS.md structure |
| `AppError` definition | `crates/` tree at pinned commit | Identify variants and their messages |
| `error_banner` frontend usage | Frontend component(s) at pinned commit | What the UI renders |

Access repository files via:
```bash
gh api "repos/Nousix-LLC/nswe-demo/contents/PATH?ref=decb6196c2c1e6ed421d393a642f0c844cc333ba" \
  --jq '.content' | base64 -d
```

To locate error-related files:
```bash
gh api "repos/Nousix-LLC/nswe-demo/git/trees/decb6196c2c1e6ed421d393a642f0c844cc333ba?recursive=1" \
  --jq '.tree[] | select(.path | test("error|Error"; "i")) | .path'
```

---

## Output Specification

| Attribute | Value |
|-----------|-------|
| Filename | `error_safety_findings.md` |
| Format | Markdown conforming to `../../../contracts/findings_schema.md` |
| Location | `spoke-error-safety/` (this workspace) |

The partial findings cover concern 8 only. The synthesis child reads this file and merges it
with `../spoke-rust-idiom/rust_idiom_findings.md` to produce the final combined FINDINGS.md.

---

## Success Criteria

- Every `AppError` variant's `user_message()` return value examined
- Verdict declared: PASS if no variant can surface internal detail; FINDINGS if any can
- For each finding: file path + line number at pinned commit, principle, severity, satisfying condition
- Clean Account covers concern 8 with what was checked and what was found
- Output file at `spoke-error-safety/error_safety_findings.md`
- No internal infrastructure details in any finding or prose

---

## Suggested Methodology Files

Domain Mapping match: **Security review** → Primary: `Security`, Supporting: `Code Review`

Specific files to load (starting points — the executing agent is the final judge):

- `security/Security_Secure_Coding_Methodology.md` — information leakage through error messages;
  the principle that user-facing errors must not expose internal state. Central to concern 8.
- `code-review/CodeReview_Checklist_Methodology.md` — security rows; use to confirm the
  error-path checklist is applied.

These are the parent's flagged starting points. Load fewer if some are clearly inapplicable;
load more if the codebase reveals additional methodology surface the parent did not anticipate.

## Out-of-Scope Methodologies

- `rust/` bundle — Rust idiom analysis belongs to `spoke-rust-idiom`
- `testing/` bundle — test depth is handled by `spoke-tests` at the parent review level
- Prose quality — handled by `spoke-prose` at the parent review level

## Inherited Constraints

- Findings point at repository file paths and line numbers at pinned commit
  `decb6196c2c1e6ed421d393a642f0c844cc333ba`; no host paths, private IPs, or infrastructure
  details
- Do not post to the PR
- Prose in `error_safety_findings.md` must pass the plain-voice bar in
  `../../../contracts/findings_schema.md`
- Repository: `Nousix-LLC/nswe-demo` only
