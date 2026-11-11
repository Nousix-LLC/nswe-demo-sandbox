## Findings

### Q3.1 — Declaration site carries no inline comment

- severity: non-blocker
- concern: code-quality
- location: crates/ferric/src/async_resource.rs:217

`let gen = Rc::new(Cell::new(0u64));` at line 217 has no inline comment. The
function docstring's `# Cancellation (REQ-ASYNC-016)` section (lines 186–193)
explains the counter at the function level, and the increment comment at lines
226–227 explains it in the body. Neither is visible from the declaration line
itself.

A reader navigating to line 217 via "Go to definition" from the comparison guard
at line 240 hits the declaration without context, and must scroll backward nine
lines to the first in-body explanation. The docstring covers it at the function
boundary but a function body is long enough (about 30 lines) that a reader working
through it without the docstring visible does not get the same benefit.

A brief inline comment at line 217 — e.g., `// generation counter: captures current gen in spawned future, discard if superseded` — would make the invariant legible at first contact. The existing docstring and increment-site comment already contain accurate prose; an inline note at the declaration would not duplicate them so much as connect them to the declaration itself.

This does not rise to a blocker: the invariant is documented and no information is
absent; the gap is one of locality.

### Q3.2 — Increment site comment covers action and effect

- severity: clean
- concern: code-quality
- location: crates/ferric/src/async_resource.rs:226-229

Lines 226–227:
```
// Bump the generation so any in-flight future from the previous source value will
// see a stale generation and discard its result (REQ-ASYNC-016).
```
The comment names what the increment does, what it causes in concurrent futures, and
references the requirement. A reader catching a bug in this path would know immediately
what the counter protects without reading beyond this block. This is the kind of
why-not-what comment that makes state-mutation sites self-explanatory.

### Q3.3 — Comparison guard comment is clear

- severity: clean
- concern: code-quality
- location: crates/ferric/src/async_resource.rs:239-240

Line 239:
```
// Only write if our generation is still the latest (no newer fetch started).
```
The guard condition is stated in terms of behavior (a newer fetch) rather than
mechanics (integer equality), which is the right level for a reader debugging a
missed update or stale overwrite. `next_gen` is a captured `u64` and `gen_check.get()`
is the shared counter's current value; both are single-purpose enough that the comment
closes any remaining gap. No simulation required.

### Q3.4 — Abstraction level is appropriate; counter cannot be misread

- severity: clean
- concern: code-quality
- location: crates/ferric/src/async_resource.rs:217-240

The counter is `Rc<Cell<u64>>`. `u64` is not idiomatic for a length or loop variable
in Rust (those would be `usize`), and the `Rc<Cell<_>>` wrapper signals shared mutable
state rather than a simple accumulator. The read-snapshot-compare pattern
(`gen.get() + 1 → gen.set(next_gen); ... gen_check.get() == next_gen`) is the
canonical optimistic-concurrency generation check; a reader familiar with concurrent
Rust patterns will recognise it immediately, and the increment comment equips a reader
who is not. No extra abstraction layer is missing or needed.

### Q3.5 — Naming distinguishes the counter from incidental variables

- severity: clean
- concern: code-quality
- location: crates/ferric/src/async_resource.rs:217

`gen` does not resemble a loop variable (`i`, `j`) or a size variable (`len`,
`count`). The name is terse but established for the generation-counter pattern. The
Rc and Cell wrappers in the type make the shared-mutable-integer semantics explicit
even without a comment.

`gen_check` (line 236, the clone moved into the async block) is functional — it names
the clone's use rather than its nature. Three lines later the guard at line 239 makes
the purpose clear. The name is adequate; a reader would not confuse `gen_check` with
a separate counter.

---

## What was examined

| Location | Lines | Sub-question |
|----------|-------|--------------|
| `crates/ferric/src/async_resource.rs` | 186–193 | Q3.1: `# Cancellation` docstring — invariant documented at function boundary |
| `crates/ferric/src/async_resource.rs` | 217 | Q3.1, Q3.4, Q3.5: declaration site — presence/absence of inline comment; type choice; naming |
| `crates/ferric/src/async_resource.rs` | 226–229 | Q3.1, Q3.2: increment site — comment content, action vs. effect framing |
| `crates/ferric/src/async_resource.rs` | 236 | Q3.5: clone site — `gen_check` naming and absence of inline comment |
| `crates/ferric/src/async_resource.rs` | 239–241 | Q3.3: comparison guard — comment clarity, guard semantics |
| `crates/ferric/src/async_resource.rs` | 648–668 | Q3.1, Q3.3: test `create_resource_two_source_changes_stay_loading` — counter behavior exercised; test name and docstring align with guard semantics |
