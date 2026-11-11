# Task: hydrate_wasm.rs — Dimension 3: Hardcoded Strings vs. Imported Constants

## Task Specification

**Slug**: SUBTASK_dim-strings
**Task Kind**: standard
**Depends on**: none
**Status**: Pending
**Assigned To**: swe-reviewer

### Objective

Assess whether `hydrate_wasm.rs` (commit `75c1eef`) injects HTML that reflects what
actual SSR output would contain — specifically, whether the SSR text-node sentinel
markers (`TEXT_OPEN_MARKER` = `<!--$t-->`, `TEXT_CLOSE_MARKER` = `<!--/$t-->`) appear
in the injected HTML strings, or whether the tests silently test a different input than
real SSR would produce. Produce `finding.md` with a severity label and cited evidence.

### Context

This task is one of five parallel dimension spokes within SUBTASK_hydrate-wasm-quality
(see `../_GLOBAL.md`). It assesses exactly one dimension: hardcoded strings vs.
imported constants.

`crates/ferric/src/ssr.rs` defines:
```rust
pub const TEXT_OPEN_MARKER: &str  = "<!--$t-->";
pub const TEXT_CLOSE_MARKER: &str = "<!--/$t-->";
```
Doc comments state: "Both sides MUST use this exact literal — never define a local copy."

The `render_to_string` function in `ssr.rs` wraps every `VNode::Text` in these markers,
so actual SSR output for a text node "hello" would be:
```
<!--$t-->hello<!--/$t-->
```

The hydration path in `hydrate.rs` must strip these sentinels before comparing or
adopting text nodes. If the tests inject HTML without the sentinels, the
sentinel-stripping logic is never exercised, and the tests pass on input that real
SSR would never produce.

The concern is whether the test file defines its own string constants that duplicate
or diverge from production values, OR whether the injected HTML strings simply omit
the sentinel markers entirely — either way producing false confidence in the coverage.

---

## Input Specification

| Input | Source | Purpose |
|---|---|---|
| Subtree hub | `../_GLOBAL.md` | Subtree constraints and shared context |
| `hydrate_wasm.rs` | commit `75c1eef` | Primary file for this dimension |
| `ssr.rs` | commit `75c1eef` | Reference for SSR marker constants and their doc contract |

**Reading the files:**
```bash
gh api "repos/Nousix-LLC/nswe-demo/contents/crates/ferric/tests/hydrate_wasm.rs?ref=75c1eef776953993ddd62dba1436845a0d53a281" \
  --jq '.content' | base64 -d

gh api "repos/Nousix-LLC/nswe-demo/contents/crates/ferric/src/ssr.rs?ref=75c1eef776953993ddd62dba1436845a0d53a281" \
  --jq '.content' | base64 -d
```

---

## Dimension Scope

Assess hardcoded strings vs. imported constants in `hydrate_wasm.rs`:

1. **Check the injected HTML strings** in each test: do any text nodes appear as bare
   strings (e.g., `>hello<`) rather than sentinel-wrapped strings
   (e.g., `<!--$t-->hello<!--/$t-->`)?

2. **Check whether the test file defines local string constants** that duplicate values
   already defined in production code (ssr.rs, hydrate.rs). If so, they can diverge
   silently.

3. **Assess the coverage gap**: if the injected HTML omits sentinels, what hydration
   code paths are never exercised? Does this produce false confidence in REQ-SSR-004
   coverage (adopt walk without structural mutations)?

4. **Check imports**: does the test file import `TEXT_OPEN_MARKER` / `TEXT_CLOSE_MARKER`
   from `ferric::ssr`, or does it use inline string literals?

Do NOT assess: test naming, cleanup, assertion quality, or structural duplication.

---

## Output Specification

**File**: `finding.md`
**Location**: `SUBTASK_dim-strings/`

```markdown
## Hardcoded strings vs. imported constants

**Severity**: [Blocker | Warning | Pass]
**Evidence**: [hydrate_wasm.rs:line or N/A]

[Finding text — plain voice, concrete, citable]
```

Severity semantics:
- **Blocker**: Tests inject HTML that omits SSR sentinel markers that actual SSR output
  would contain, exercising a materially different code path than production — produces
  false confidence in coverage.
- **Warning**: Local string constants duplicate production values but match them today;
  risk of silent divergence on future change.
- **Pass**: Injected HTML reflects real SSR output; sentinel markers imported from or
  consistent with production constants.

---

## Success Criteria

- [ ] Each injected HTML string in every test checked against actual SSR output format
- [ ] Whether sentinel markers appear in injected HTML explicitly stated
- [ ] Import check: whether `TEXT_OPEN_MARKER` / `TEXT_CLOSE_MARKER` are imported
- [ ] Coverage gap described if sentinels are absent
- [ ] Severity assigned with rationale tied to REQ-SSR-004
- [ ] Evidence cites specific line(s) in hydrate_wasm.rs
- [ ] `finding.md` written to this task's workspace

---

## Methodology Guidance

**Primary**: `rust/Rust_Testing_Methodology.md` — test fidelity and coverage gaps
**Secondary**: `rust/Rust_WebAssembly_Browser_Methodology.md` — wasm-bindgen-test specifics

---

## Inherited Constraints

- **Repository**: Nousix-LLC/nswe-demo, commit `75c1eef776953993ddd62dba1436845a0d53a281`
- **Do not re-raise**: Issues #229–#242
- **Do not reference**: Overseer I267 escalation comments
- **Prose bar**: No AI-tell patterns in output text
- **Scope**: Code quality only — security scope (HTML injection, XSS) belongs to SUBTASK_security
