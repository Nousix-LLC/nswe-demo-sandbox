# _BRIEF.md — NSWE overseer iteration I61 (persona swe-lead) — LAUNCH the Ferric 1.0 + SSR design DAG
**Depends on**: I60

You are the **NSWE project overseer** (`swe-lead`) for `Nousix-LLC/nswe-demo`, continuing the chain
(… → I59 → I60 → **I61**). You are an event loop, **NOT** a designer — **P1: you do not design the product
inline; design is a forked DAG.** Boot the kernel + the NSWE app-files, publish `thread_evaluation`, then Act.

**This turn's filesets: `PRODUCT_DESIGN` + `WORK_SESSION`.** This is an **action**: *launch a design DAG* —
write the design brief from `PRODUCT_DESIGN` and fork one design DAG (`swe-designer`) for directive **#114**
(Ferric → a real 1.0 framework, with server-side rendering + hydration).

## What to do
1. **Re-check the slot budget before forking** (`WORK_SESSION`, "At most four DAGs in flight"): confirm a
   free slot (zombie `design-chirp-r1` = 1; the review DAG from I58 = 1; so typically 2 used, 2 free unless
   the zombie folded). If no slot is free, record `waiting_launches` and pass on (never stop/reap a running
   DAG). Your I61 fork token is FRESH (one `engine_fork` this iteration). One design DAG at a time.
2. **Write the design `_BRIEF.md`** from `PRODUCT_DESIGN` (describe, do not instruct). Objective: take Ferric
   from where it is (a client-side Rust/WASM signals + keyed-VDOM framework; deps wasm-bindgen/web-sys/js-sys)
   to a credible **1.0**, planned under the **Ferric epic #1**, folding in the router and HTTP/JSON-client
   issues already on the board. State as **distinct concerns** the must-haves #114 names — the one must-have
   **server-side rendering + hydration** (Axum integration, hydrate without re-render); a `view!`/JSX-style
   macro; component props/children/slots/composition; context; async resources with suspense-style
   loading/error; forms + two-way binding; full DOM event coverage; a router (params, nested routes, links)
   + HTTP/JSON client; docs (guide, tutorial, API docs, examples, cargo-generate starter); crates.io
   publishing with semver + changelog; a js-framework-benchmark entry — plus the **release-bar + traceable
   backlog** the design must produce (epics/issues tracing to the design, under the Ferric epic). "Nice to
   have after 1.0" (scoped CSS, devtools, hot reload, desktop/mobile) is out of the 1.0 bar. The design must
   let Chirp surface real framework gaps as further issues. Declared output: the design PR, its tickets on
   the board, and the release bar; a root `SYNTHESIS.md`. The DAG selects/loads its own methodologies — do
   NOT name bundles or put methodology in `_FORK.md`/`launch_context`.
   `_FORK.md`: launch agent `swe-designer`, `reap-whole-after-land`, `launch_context: {application: software}`.
3. **Fork** the design DAG; record it in STATE `design.design_dags` + `dispatched_dags` (slug e.g.
   `design-ferric-1_0`, kind `design`, workspace, observation seam root `SYNTHESIS.md`), distinct from the
   superseded `design-chirp-r1` zombie. When it folds, its triage is a **Triage a design** task
   (`PRODUCT_DESIGN`, `BOARD`).
4. **Schedule the successor** (`I62` depends_on `I61`): a **board check** (the home return). Write its brief fresh.

## Carried state (read first)
- `taskflow/overseer/I57/project_state.json` — STATE (design record reconciled; zombie standing watch).
- `taskflow/overseer/I57/CONTINUE.md` — the I57 board-check findings + series plan.
- Directive **#114** body (read live via `gh`) — the authoritative scope.

## Gotchas / scope
- (d) One `engine_fork` per iteration; confirm a free slot first. A reconstructed instance shares a spent
  token — if a prior I61 already forked the design DAG, do NOT re-fork.
- Do NOT confuse this NEW Ferric-1.0 design DAG with the superseded `design-chirp-r1` zombie (triage-and-discard).
- Do NOT Exit. Only `Nousix-LLC/nswe-demo`. **No attribution trailers**; **nothing on GitHub carries
  host/system details** — translate host facts to repository identities.
