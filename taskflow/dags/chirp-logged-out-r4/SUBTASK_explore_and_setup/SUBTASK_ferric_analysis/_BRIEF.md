# Task: Ferric Framework API Analysis

## Task Specification

**Slug**: SUBTASK_ferric_analysis
**Task Kind**: standard
**Depends on**: none
**Status**: Pending
**Assigned To**: swe-coder

### Objective

Read the ferric framework source code to document the APIs relevant to building a new public
(logged-out) route: the `Resource`/async data-loading API and its loading/error/loaded state
representation, the Router API and how routes are defined/mounted, the SSR and hydration APIs,
and any relevant signal/component patterns for distinct UI states. Record findings in
`ferric_findings.md` with a recommendation on whether to use SSR for the public timeline.

---

## Input Specification

### Required Inputs

| Input | Source | Purpose |
|-------|--------|---------|
| Subtree hub | `taskflow/dags/chirp-logged-out-r4/SUBTASK_explore_and_setup/_GLOBAL.md` | Project constraints |
| Ferric source | `crates/ferric/src/` | Router API, Resource/async, SSR/hydrate APIs |

All paths are relative to `/home/user/nousix-runtime/nswe-demo`.

---

## Process Specification

1. Explore `crates/ferric/src/` to understand the directory layout.
2. Find and document the `Resource` / async data-loading API:
   - Type name and struct/trait definition
   - How it represents three states: loading, error, loaded
   - Usage pattern (how it is used in a component)
3. Find and document the Router API:
   - How routes are defined (function signature, macro, builder pattern?)
   - How routes are mounted/composed
   - Any route parameter syntax
4. Find and document the SSR and hydration APIs:
   - Is SSR available and how is it invoked?
   - How does hydration work?
   - Recommendation: should the new public home/timeline route use SSR? (yes/no + rationale
     based on what the framework supports and performance implications)
5. Document any signal or state patterns relevant to managing distinct UI states (loading,
   empty, error, populated list, end-of-list).
6. Write `ferric_findings.md` with the required sections.
7. Write `COMPLETE.md`.

---

## Output Specification

### Primary Output

| Attribute | Value |
|-----------|-------|
| Filename | `ferric_findings.md` |
| Location | `taskflow/dags/chirp-logged-out-r4/SUBTASK_explore_and_setup/SUBTASK_ferric_analysis/` |

### Required Sections in `ferric_findings.md`

```markdown
# Ferric Framework API Findings

## Resource / Async Data-Loading API
- Type name: <e.g. Resource<T, E>>
- Loading state representation: <field/variant name>
- Error state representation: <field/variant name>
- Loaded state representation: <field/variant name>
- Usage pattern:
  ```rust
  // <example>
  ```

## Router API
- Route definition: <function signature or macro>
- Route mounting: <how routes are added to the app>
- Route parameter syntax: <e.g. :param or {param}>
- Example:
  ```rust
  // <example>
  ```

## SSR and Hydration
- SSR available: yes | no
- SSR invocation: <how to enable SSR for a route>
- Hydration API: <how the client hydrates server-rendered HTML>
- Recommendation: use SSR for the public home/timeline route?
  - Decision: yes | no
  - Rationale: <why — framework support, SEO, performance, complexity>

## Signal / State Patterns
- Signal type: <name>
- Pattern for managing loading/error/loaded/empty states: <description>
- Relevant component patterns for displaying a list with multiple states

## Module / File Locations
- Resource API: <file path>
- Router API: <file path>
- SSR/hydrate API: <file path>
```

---

## Success Criteria

- [ ] Resource API documented with loading/error/loaded state names
- [ ] Router API documented with usage pattern
- [ ] SSR recommendation made (yes/no with rationale)
- [ ] `ferric_findings.md` exists with all required sections
- [ ] `COMPLETE.md` written

---

## Suggested Methodology Files

**Task-type row:** Framework API analysis — Primary: `rust`, Supporting: `framework-design`

**Specific files:**
- `rust/Rust_Trait_Design_Methodology.md` — Rationale: ferric likely exposes its APIs via traits; understanding trait patterns helps read and document the API surface correctly.
- `framework-design/FrameworkDesign_Library_API_Design_Methodology.md` — Rationale: analyzing a framework's API design helps identify and document the intended usage patterns.

**These are SUGGESTIONS.** The child agent is the final judge.

## Inherited Constraints

- Repository is at `/home/user/nousix-runtime/nswe-demo`
- Read-only — do NOT modify any ferric source files
- Note: the cluster SSH pattern from CLAUDE.md is NOT needed for this task

## Out-of-Scope Methodologies

- chirp-server analysis — covered by SUBTASK_server_analysis
- chirp-frontend structure — covered by SUBTASK_frontend_analysis
