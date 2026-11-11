# Task: Prose Quality Analysis — PR #263

## Task Specification

**Slug**: spoke-prose
**Task Kind**: standard
**Depends on**: none
**Status**: Pending

### Objective

Assess prose quality in PR #263 on `Nousix-LLC/nswe-demo`, covering concern 9 from the parent
spoke brief.

### Context

This task is part of the code-quality review decomposition. See `../_GLOBAL.md` for PR details
and `../contracts/` for the FINDINGS.md output schema.

**Concern assigned to this spoke:**

9. **Prose quality** — Check module docstrings, function docstrings, inline comments, and the
   PR description for AI-writing tells. Report by cluster and density.

   Tells to look for:
   - **Moral/character adjectives attached to technical things**: "honest", "genuine", "real"
     used to describe a metric, function, or behavior. A metric has no honesty. Flag these.
   - **Narrated candor**: "stated plainly", "to be honest", "let's be clear", "to be direct".
     These perform transparency rather than demonstrating it.
   - **Unnamed contrast pairs**: "real X, not the fake kind"; "it's not X, it's Y" where Y is
     not defined on its own terms.
   - **Slot-fill templates**: "a [adjective] step toward [noun]", "whether you're X or Y",
     rhythmic padding in threes.
   - **Inflated filler**: seamless, robust, comprehensive, leverage, Moreover, Furthermore,
     stacked intensifiers.
   - **Machine-writing density**: a single instance is weak signal; a cluster of 3+ tells in
     one block is a finding.

   Judge by cluster and density, not individual words. Report where the density is high enough
   to constitute a finding, and credit prose that reads in a plain human voice.

---

## Input Specification

### Required Inputs

| Input | Source | Purpose |
|-------|--------|---------|
| Hub context | `../_GLOBAL.md` | Concern assignments, pin commit, output schema |
| Contract schema | `../contracts/findings_schema.md` | FINDINGS.md structure |
| PR description | `gh pr view 263 -R Nousix-LLC/nswe-demo` | PR title, body, comments by PR author |
| `api.rs` (types) | `crates/chirp-types/src/api.rs` at HEAD | Module and type docstrings |
| `handlers.rs` | `crates/chirp-server/src/api/handlers.rs` at HEAD | Function docstrings + inline comments |
| `postgres.rs` | `crates/chirp-server/src/repository/postgres.rs` at HEAD | Function/impl docstrings |
| `mod.rs` | `crates/chirp-server/src/repository/mod.rs` at HEAD | Trait docstrings |
| `hydrate.rs` | `crates/ferric/src/hydrate.rs` at HEAD | Module/function comments |

Access PR description:
```bash
gh pr view 263 -R Nousix-LLC/nswe-demo
```

Access source files at pinned commit:
```bash
gh api "repos/Nousix-LLC/nswe-demo/contents/PATH?ref=decb6196c2c1e6ed421d393a642f0c844cc333ba" \
  --jq '.content' | base64 -d
```

You need not read the full implementation — focus on doc comments (`///`, `//!`), inline
comments (`//`), and the PR description text. Skip lines that are pure code with no comment.

---

## Process Specification

For each text corpus (PR description, then each file's comments):
1. Read the prose content
2. Apply the tell inventory: moral adjectives, narrated candor, contrast pairs, slot-fills,
   inflated filler
3. Note whether the tell density in a block is above the threshold (3+ tells in one paragraph
   or one function's doc → finding)
4. Credit passages that are plain and informative

Report by block location, not by individual word. A passage with two stacked tells is worth
noting; a passage with five is a clear finding.

Do not flag technical jargon (Rust terms, endpoint names) as "inflated filler."

---

## Output Specification

| Attribute | Value |
|-----------|-------|
| Filename | `FINDINGS.md` |
| Format | Markdown |
| Location | `spoke-prose/` (this workspace) |

Structure: per `../contracts/findings_schema.md`.

---

## Success Criteria

- Concern 9 appears in the Clean Account
- PR description prose assessed
- Docstrings and inline comments in new files assessed
- Findings report by cluster/density, not by individual words
- An account of what prose was read and found plain
- No internal infrastructure details in any finding
- FINDINGS.md itself must pass the plain-voice bar (do not write a prose-quality review in
  AI-inflated prose)

---

## Suggested Methodology Files

Domain Mapping match: **Code review** → Primary: `Code Review`, Supporting: `Core`

Specific files:
- `code-review/CodeReview_Process_Methodology.md` — the section on prose as part of what ships;
  the reviewer holds review text to the same bar as the code comments it reviews
- `code-review/CodeReview_Feedback_Guidelines_Methodology.md` — how to write finding text that
  is actionable without being harsh

Also consult the avoid-AI-writing tell catalog. If the deployment has an `avoid-ai-writing`
skill available, run it. Otherwise, apply the catalog in the brief above by hand.

These are suggested starting points.

## Out-of-Scope Methodologies

- Technical correctness — handled by other spokes
- Security — handled by `spoke-safety-idiom`
- `synthesis/` bundle — belongs to `spoke-synthesis`

## Inherited Constraints

- Findings point at repository file paths and line numbers at pinned commit
  `decb6196c2c1e6ed421d393a642f0c844cc333ba`; no host paths, private IPs, or infrastructure details
- Do not post to the PR
- Write your FINDINGS.md in a plain voice — the irony of an AI-inflated prose-quality finding
  is a protocol violation
- Repository: `Nousix-LLC/nswe-demo` only
