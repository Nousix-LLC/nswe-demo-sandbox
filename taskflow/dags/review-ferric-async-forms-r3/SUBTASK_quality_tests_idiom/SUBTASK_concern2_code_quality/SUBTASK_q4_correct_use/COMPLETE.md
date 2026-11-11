# COMPLETE — SUBTASK_q4_correct_use

Task completed. `sub_findings.md` produced at this workspace root.

## Summary

Examined all four changed files for Q4 (correct-use design from a caller's perspective). Found four non-blocker issues and five clean verifications.

**Non-blockers (4):**

- NB-1: `create_resource` is not in the prelude alongside `Resource`; a caller using `use ferric::prelude::*` sees `Resource::new` first and may not discover `create_resource`, the right API for reactive refetching.
- NB-2: `Resource::new` / `Resource::new_fallible` call `spawn_local` without a `#[cfg(target_arch = "wasm32")]` gate or docstring WASM note, inconsistent with `create_resource` which documents and gates this explicitly.
- NB-3: `Bind::on_input_handler` requires `set_input` to be called before the handler fires; violating the ordering silently writes stale buffer data to the field signal.
- NB-4: No `VElement` builder method accepts a pre-built `EventHandler`; wiring a `Bind`-produced handler to a `VElement` requires direct `events.push()` field access, bypassing the builder API.

**Clean (5):**

- `ResourceState<T>` exhaustive enum forces handling all three lifecycle states.
- `FormField::parsed()` returns `Result` — no silent coercion path.
- `on_input_event_handler` is properly `#[cfg(target_arch = "wasm32")]` gated.
- `VElement` event registration has one clear primary path for component authors.
- `EventKind` exhaustive matches in `event_name` / `stash_key` enforce table synchrony at compile time.

## Output

- `sub_findings.md` — findings with severity, concern, location, and description for each entry.
