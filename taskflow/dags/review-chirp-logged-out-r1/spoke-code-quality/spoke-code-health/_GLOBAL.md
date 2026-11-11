# spoke-code-health — Code Health Review Subtree Hub

## Project Context

**Status**: Active
**Parent task**: `spoke-code-health` in `spoke-code-quality` subtree of DAG `review-chirp-logged-out-r1`
**PR**: #263 on `Nousix-LLC/nswe-demo`
**Head commit**: `decb6196c2c1e6ed421d393a642f0c844cc333ba`

### Objective

Decompose concerns 6 and 7 from the code-quality spoke into two parallel investigations, then
synthesize their per-concern findings into the single `spoke-code-health/FINDINGS.md` declared
by the parent spoke.

### Scope

**In scope:**
- Concern 6: reachability of `sign_up::sign_up_view` from any live route
- Concern 7: causal necessity of `hydrate.rs` EventKind expansion for the public timeline feature,
  and sync safety of `static_event_kinds()` vs the `EventKind` enum

**Out of scope:**
- Any concern not assigned to `spoke-code-health`
- Posting to the PR
- Files outside the route table, sign_up.rs, compose.rs, and hydrate.rs

### Success Criteria

- Concern 6 has a definitive reachability verdict in `child-dead-code/finding_c6.md`
- Concern 7 has a scope/sync verdict in `child-hydrate-scope/finding_c7.md`
- `spoke-code-health/FINDINGS.md` combines both per schema (## Verdict, ## Findings, ## Clean Account)
- No internal host paths, private IPs, or infrastructure details
- Prose passes the plain-voice bar

---

## Input Specification

| Input | Location | Description |
|-------|----------|-------------|
| Parent hub | `../_GLOBAL.md` | PR context, concern assignment table, pin commit |
| Parent schema | `../contracts/findings_schema.md` | FINDINGS.md schema |
| This hub | `_GLOBAL.md` | Subtree context (this file) |
| Concern finding schema | `contracts/concern_finding_schema.md` | Structure each analysis child produces |
| `sign_up.rs` | `crates/chirp-frontend/src/pages/sign_up.rs` at HEAD | Module containing `sign_up_view` |
| `compose.rs` | `crates/chirp-frontend/src/pages/compose.rs` or similar | Competing signup view |
| Route table | `crates/chirp-frontend/src/main.rs` or similar | Router definition |
| `hydrate.rs` | `crates/ferric/src/hydrate.rs` at HEAD | Full file — EventKind and table |
| PR diff | `gh pr diff 263 -R Nousix-LLC/nswe-demo` | What changed |

Access file contents via:
```bash
gh api "repos/Nousix-LLC/nswe-demo/contents/PATH?ref=decb6196c2c1e6ed421d393a642f0c844cc333ba" \
  --jq '.content' | base64 -d
```

---

## Task Structure

```
_GLOBAL.md (this document)
├── contracts/
│   ├── _MANIFEST.yaml
│   └── concern_finding_schema.md
├── child-dead-code/_BRIEF.md   (concern 6: sign_up::sign_up_view reachability)
├── child-hydrate-scope/_BRIEF.md  (concern 7: hydrate.rs scope and sync risk)
└── child-synthesis/_BRIEF.md   (synthesis gate: combines findings into FINDINGS.md)
```

## Task Summary

| Task id | Depends on | Description | Output |
|---------|------------|-------------|--------|
| `child-dead-code` | none | Reachability analysis of `sign_up::sign_up_view` | `child-dead-code/finding_c6.md` |
| `child-hydrate-scope` | none | Scope and sync assessment of `hydrate.rs` EventKind expansion | `child-hydrate-scope/finding_c7.md` |
| `child-synthesis` | `child-dead-code`, `child-hydrate-scope` | Synthesis gate: combine per-concern findings into FINDINGS.md | `../spoke-code-health/FINDINGS.md` |

## Dependency Graph

```
child-dead-code      ──┐
                       ├── child-synthesis
child-hydrate-scope  ──┘
```

---

## Contract

**Contract location**: `contracts/` (read-only for all descendants)
**Contract kind**: yaml_schema + markdown_schema

| Artifact | Kind | Declares |
|----------|------|----------|
| `contracts/_MANIFEST.yaml` | yaml | Ownership, identities, derived artifacts |
| `contracts/concern_finding_schema.md` | markdown | Structure for per-concern finding files produced by analysis children |

### Ownership

| Artifact | Owning subtask |
|----------|----------------|
| `child-dead-code/finding_c6.md` | `child-dead-code` |
| `child-hydrate-scope/finding_c7.md` | `child-hydrate-scope` |
| `spoke-code-health/FINDINGS.md` | `child-synthesis` |
| `spoke-code-health/COMPLETE.md` | `child-synthesis` (fold record) |

### Identities

- [ ] Concern 6 is covered exactly once, in `child-dead-code/finding_c6.md`
- [ ] Concern 7 is covered exactly once, in `child-hydrate-scope/finding_c7.md`
- [ ] `FINDINGS.md` contains a `## Verdict` section, a `## Findings` section (when verdict = FINDINGS), and a `## Clean Account` section covering both concerns 6 and 7
- [ ] Every finding cites a file path and line number at commit `decb6196c2c1e6ed421d393a642f0c844cc333ba`

### Derived Artifacts

None. The contract artifacts are schema documents; no code generation is needed.

---

## Subtree Methodology Posture

**Dominant task type**: Code review (dead-code and scope analysis)
**Primary bundles**: `code-review`, `code-quality`
**Cross-cutting binding**: All findings hold the principal-reviewer bar — location (file + line at
pinned commit), principle at stake, why it matters, severity, satisfying condition. Prose must pass
the avoid-AI-writing bar: no moral/character adjectives on technical things, no narrated candor,
no unnamed contrast pairs, no slot-fill templates.

---

## Output Specification

| Deliverable | Format | Location |
|-------------|--------|----------|
| Concern 6 finding | Markdown | `child-dead-code/finding_c6.md` |
| Concern 7 finding | Markdown | `child-hydrate-scope/finding_c7.md` |
| Combined findings | Markdown | `spoke-code-health/FINDINGS.md` (parent schema) |
