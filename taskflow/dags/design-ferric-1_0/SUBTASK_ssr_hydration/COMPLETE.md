# COMPLETE — SUBTASK_ssr_hydration

## What was done
Designed Ferric's server-side-rendering + hydration architecture — the single 1.0 must-have — and authored the
`REQ-SSR-*` register, as a design (what, not how), grounded in the live baseline.

**Output:** `ssr-hydration.md` (456 lines). Repo target `design/ferric/ssr-hydration.md` (placed later by
`SUBTASK_design_pr`, identity I8).

## The three facets, co-designed as one mechanism
- **Render to HTML on the server (§2.1):** a pure, off-wasm `VNode → HTML` render (the baseline view layer is
  already `web-sys`-free), text-boundary markers so the client re-locates nodes by the shared path addressing,
  per-request reactive isolation, and the Axum integration shape composing with the existing `chirp-server`.
- **Hydration without re-render (§2.2):** a `hydrate` entry distinct from `mount` (which clears-and-rebuilds)
  that *adopts* the server DOM — creates/replaces/removes nothing, attaches event listeners, and establishes
  the reactive effect so later updates patch in place.
- **State carry & resume (§2.3):** a declared, typed, stably-keyed state island (not the un-serializable
  reactive arena of `Box<dyn Any>`/closures) read before hydration, resuming server-resolved async resources as
  already-resolved with no refetch.
Plus mismatch detection + bounded recovery (§3), injection-safe markup/state-island (§4), SSR-area deferrals
recorded (§5), and the hydration-vs-resumability trade stated against named peers (§6).

## Why atomic (decompose evaluation)
The brief named three concerns, but the no-re-render guarantee exists only in their agreement — the hydration
protocol is fixed by the server-render output, which is fixed by the carried-state format. They are not
independently parallelizable (Distinct-Concerns Test fails to fire → one responsibility); one kind of change,
one register, one doc (Single-Responsibility passes); output size matches the application norm for a design
spoke. Declared `Atomic`.

## Success criteria
- [x] Architecture states server render, hydrate-without-re-render, and state carry/resume — concretely enough
      for a code DAG to build.
- [x] `REQ-SSR-*` acceptance criteria are testable (REQ-SSR-004: a headless `wasm-bindgen-test` asserting zero
      structural DOM mutation on hydrate); conforms to `../contracts/id_and_traceability_schema.yaml`.
- [x] ≥1 `REQ-SSR-*` is `stage: one_oh` and flagged the gating must-have: REQ-SSR-004 (feeds identity I4).
- [x] Peers compared by name (Leptos, Sycamore, Dioxus, Yew, Solid, Qwik); the chosen trade-off stated.

## Constraints honored
- Only `REQ-SSR-*` ids minted; all cross-references read-only (identity I1). Design, not implementation.
- Axum is the named server integration (REQ-SSR-011). Grounded at `276138f`.
- avoid-ai-writing pass run (skill unavailable this deployment; checked by hand against P0/P1 — no tells).

## Notes for downstream
- `SUBTASK_release_bar`: REQ-SSR-004 is the must-have to mark with a `one_oh` `BAR-FERRIC-*` carrying
  `must_have: true` (I4); the full register (001–012, all `one_oh`/gating) is the gating-coverage set for I3.
- Boundary: `REQ-ASYNC-*` owns the resource primitive REQ-SSR-006/007 resume; `REQ-API-*` owns the macro whose
  `VNode` output is rendered; `REQ-DX-*` owns the server-integration docs; `REQ-REL-*` owns semver/compat.
</content>
