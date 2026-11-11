# SUBTASK_axum_mismatch — Mismatch Detection + Axum Integration Subtree Hub

## Project Context

**Status**: Active

### Objective

Review PR #228 (`work/ferric-ssr-r1`, `Nousix-LLC/nswe-demo`) against three acceptance criteria for issue
#226, and confirm one non-goal. Produce `axum_mismatch_findings.md` in this workspace for
`SUBTASK_correctness_synthesis` (parent DAG) to consume.

Criteria in scope:
- **REQ-SSR-006**: mismatch detection — client-side behavior, error handling, fallback, test coverage
- **REQ-MIS-001**: Axum handler pattern — server-side Rust code calling `render_to_string`, returning `Html`
- **REQ-MIS-002**: HTML well-formedness — balanced tags, valid attributes, hydration markers present
- **REQ-SSR-007 / #225**: non-goal — confirm async resource state carry is absent or stubbed, not deficient

### Scope

**In scope:**
- REQ-SSR-006 (mismatch detection, client-side WASM code path)
- REQ-MIS-001, REQ-MIS-002 (server-side Axum integration)
- REQ-SSR-007 non-goal confirmation

**Out of scope:**
- REQ-SSR-001–005 (render_to_string), REQ-HYD-001–004 (hydrate()) — sibling spokes in parent DAG
- Code quality, style, security — sibling spokes in parent DAG
- Modifying source code
- Evaluating REQ-SSR-007 as a deficiency

### Success Criteria

- [ ] REQ-SSR-006 verdict: CLEAN or FINDING, with evidence
- [ ] REQ-MIS-001 verdict: CLEAN or FINDING, with evidence
- [ ] REQ-MIS-002 verdict: CLEAN or FINDING, with evidence
- [ ] REQ-SSR-007: explicitly confirmed absent/stubbed (evidence of what was examined)
- [ ] `axum_mismatch_findings.md` in this workspace before `SUBTASK_mismatch_synthesis` reports completed

---

## Input Specifications

All spoke tasks share:

| Source | Access | Purpose |
|--------|--------|---------|
| Parent context | `../_GLOBAL.md` | PR coordinates, shared constraints, schema |
| PR diff | `gh pr diff 228 --repo Nousix-LLC/nswe-demo` | The change under review |
| Branch source | `gh api repos/Nousix-LLC/nswe-demo/contents/<path>?ref=work/ferric-ssr-r1 \| jq -r '.content' \| base64 -d` | Full file content for context |
| Issue #226 | `gh issue view 226 --repo Nousix-LLC/nswe-demo` | Mismatch detection + Axum acceptance criteria |

---

## Subtree Methodology Posture

**Dominant task type**: Ferric PR review (Rust library)

**Primary bundles** every child draws from:
- `code-review` — review process, checklist, evidence anchoring
- `rust` — `Rust_Web_Services_Axum_Methodology.md` (handler patterns, `Html(...)`, router setup)
- `framework-design` — `FrameworkDesign_UI_Reactivity_And_Rendering_Internals_Methodology.md` (SSR + hydration internals, mismatch detection semantics in a Rust UI framework)

**Client/server boundary**: `SUBTASK_mismatch_detect` examines WASM / `#[cfg(target_arch = "wasm32")]` code
(mismatch detection fires on the client during hydration). `SUBTASK_axum_server` examines server-side Axum
code (handler, `render_to_string` call, HTML output). The hydration-marker format is the seam: both spokes
MUST note the exact marker schema they observe. The synthesis cross-checks them for agreement.

**Suggestion-not-prescription**: Child agents retain final judgment over what they load and how deeply they go.

---

## Subtree-Wide Constraints

Inherited from `../_GLOBAL.md`:
- **Read-only**: No source code modification
- **Non-goal**: REQ-SSR-007 / #225 (async resource state) is not a finding or blocker; confirm as absent/stubbed
- **Evidence standard**: All findings cite files and line numbers in `Nousix-LLC/nswe-demo`, never host paths
  or taskflow paths
- **Non-blockers**: Flag them but they do not hold the landing
- **Machine gate**: CI passed — treat as a floor; check substance beyond what tests assert

---

## Task Structure

```
_GLOBAL.md (this document)
├── contracts/
│   └── _MANIFEST.yaml                 (ownership, seam identity)
├── SUBTASK_mismatch_detect/
│   └── _BRIEF.md                      → mismatch_detect_findings.md
├── SUBTASK_axum_server/
│   └── _BRIEF.md                      → axum_server_findings.md
└── SUBTASK_mismatch_synthesis/
    └── _BRIEF.md                      → axum_mismatch_findings.md (at this workspace)
```

### Task Summary

| Task id | Depends on | Description | Output |
|---------|------------|-------------|--------|
| `SUBTASK_mismatch_detect` | none | REQ-SSR-006: client-side mismatch detection behavior, error handling, fallback, test coverage | `mismatch_detect_findings.md` |
| `SUBTASK_axum_server` | none | REQ-MIS-001, REQ-MIS-002, REQ-SSR-007: server-side Axum handler pattern, HTML output quality, non-goal confirmation | `axum_server_findings.md` |
| `SUBTASK_mismatch_synthesis` | `SUBTASK_mismatch_detect`, `SUBTASK_axum_server` | Verification gate: assemble spoke findings into axum_mismatch_findings.md; fold this SUSPENDED parent | `axum_mismatch_findings.md` (written to this workspace) |

### Dependency Graph

```
SUBTASK_mismatch_detect ──┐
                           ├── SUBTASK_mismatch_synthesis
SUBTASK_axum_server     ──┘
```

---

## Contract

**Contract location**: `contracts/`
**Contract kind**: `yaml_schema`

### Inherited Contracts

| Ancestor contract | Path | What it binds here |
|---|---|---|
| Correctness review findings schema | `../_GLOBAL.md` §Contract | Each criterion entry: id, status (CLEAN/FINDING_BLOCKER/FINDING_NON_BLOCKER), what_checked, evidence (file:line in nswe-demo), finding |

### Structural Declarations

Each spoke output MUST include per-criterion sections carrying (markdown framing acceptable):
```
Criterion: REQ-XXX-NNN
Status: CLEAN | FINDING (BLOCKER) | FINDING (NON-BLOCKER)
What was checked: <text>
Evidence: <"file:line" or "file:start–end" in Nousix-LLC/nswe-demo>
Finding: <text | none>
```

The `axum_server_findings.md` additionally MUST include a non-goal section:
```
Non-goal: REQ-SSR-007 / #225
Status: CONFIRMED NON-GOAL
What was checked: <code examined to confirm absence or stubbing>
Evidence: <file:line>
```

### Ownership

| Artifact | Owning subtask |
|---|---|
| `mismatch_detect_findings.md` | `SUBTASK_mismatch_detect` |
| `axum_server_findings.md` | `SUBTASK_axum_server` |
| `axum_mismatch_findings.md` | `SUBTASK_mismatch_synthesis` (written to this workspace, `SUBTASK_axum_mismatch/`) |

### Identities

- [ ] REQ-SSR-006 verdict present in `mismatch_detect_findings.md`
- [ ] REQ-MIS-001, REQ-MIS-002 verdicts present in `axum_server_findings.md`
- [ ] REQ-SSR-007 non-goal confirmed in `axum_server_findings.md`
- [ ] All four entries assembled into `axum_mismatch_findings.md` with no criterion silently omitted
- [ ] Evidence citations use `Nousix-LLC/nswe-demo` file:line, not host/taskflow paths
- [ ] Mismatch-marker format noted by `SUBTASK_mismatch_detect` and `SUBTASK_axum_server` must agree (synthesis cross-checks; mismatch if they disagree)

### Derived Artifacts

None. Spokes work directly from PR diff and branch source via GitHub CLI.
