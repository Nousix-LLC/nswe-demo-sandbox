# SUSPENSION.md — ferric-epic-authoring-r1

**Status:** NeedsDecompose  
**Suspended at:** 2026-11-03

---

## Why suspended

This hub node declared `NeedsDecompose`. The brief enumerates six distinct sub-issues (#137–#142),
each a separate technical concern (reactive core, virtual DOM, view! macro, component model,
component diagnostics, context API), satisfying the kernel's scope trigger for decomposition.

The hub has authored the full subtree:
- `_GLOBAL.md` — hub context, task tree, dependency graph, shared branch protocol, subtree posture
- `contracts/_MANIFEST.yaml` — six identity assertions (IA1–IA6)
- `T01-137-138-foundation/_BRIEF.md` — branch setup + verify #137 and #138
- `T02-139-view-macro/_BRIEF.md` — view! proc-macro, diagnostics, closes #139
- `T03-140-component/_BRIEF.md` — #[component] + Children/Slot/SlotFn<T>, closes #140
- `T04-141-diagnostics/_BRIEF.md` — component trybuild diagnostic suite, closes #141
- `T05-142-context/_BRIEF.md` — provide_context/use_context/expect_context, closes #142
- `T06-synthesis/_BRIEF.md` — PR, CI check, SYNTHESIS.md, closes epic #129

Six `amend_plan { add_task }` calls have been issued to materialize the children in HAL.

---

## Resumption

This hub resumes when the materialized child subtree reaches terminal states. The observation seam
(`SYNTHESIS.md`) is authored by T06; the overseer reads it.

Dependency order:
1. T01 (no deps) → T02 → T03 → {T04 ∥ T05} → T06
