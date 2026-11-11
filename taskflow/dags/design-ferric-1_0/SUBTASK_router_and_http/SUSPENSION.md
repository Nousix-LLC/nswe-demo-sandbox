# SUSPENSION.md — SUBTASK_router_and_http (NeedsDecompose)

## Why suspended

This concern designs **two distinct capabilities** — a client-side **router** and an **HTTP/JSON client** —
and the kernel's decomposition triggers fired on that enumeration:

- **Scope-Based trigger — fired.** Two separate system components: separate frozen crates
  (`ferric-router` / `ferric-http`), separate id registers (`REQ-RT-*` / `REQ-HTTP-*`), separate board issues
  (#5 / #6), disjoint peer evidence (leptos_router / Dioxus router vs `reqwest` / `gloo-net`).
- **Distinct Concerns Test — fired.** A routing specialist and a network-client specialist could design these
  in parallel; a route matcher and a JSON fetch client share no structural seam.
- **Single-Responsibility conjunction — fired.** "Router **and** HTTP/JSON client" joins two distinct nouns —
  two kinds of output.
- **Output-Size — fired.** Two capabilities each to a testable REQ register with acceptance criteria and peer
  comparison exceeds the decompose threshold.
- **Independence rule honored.** That the parent already carved this as "one spoke absorbing #5/#6" is not
  evidence of atomicity; my own brief still spans two distinct concerns, so I decomposed as the root would.

Verdict: **NeedsDecompose**. I authored the subtree and suspend pending its resolution. I executed none of the
children's work.

## Subtree materialized

Hub `_GLOBAL.md` and sub-contract `contracts/_MANIFEST.yaml` authored at this workspace; one `_BRIEF.md` per
child authored at each child's workspace; each child materialized via `engine_amend_plan { add_task }`.

| Child task id | Role | Depends on | Output |
|---|---|---|---|
| `SUBTASK_router` | Router design (owns `REQ-RT-*`, folds #5) | none | `SUBTASK_router/router.md` |
| `SUBTASK_http` | HTTP/JSON client design (owns `REQ-HTTP-*`, folds #6) | none | `SUBTASK_http/http.md` |
| `SUBTASK_rt_http_synthesis` | Synthesis gate: assert SI1–SI6, compose, fold | `SUBTASK_router`, `SUBTASK_http` | `router-and-http.md` + `SYNTHESIS.md` (at this workspace) |

(The synthesis child carries the id `SUBTASK_rt_http_synthesis` — distinct from the root subtree's
`SUBTASK_synthesis` — to avoid an id collision; its workspace is the `SUBTASK_synthesis/` directory.)

## Resumption condition

All child tasks reach a terminal lifecycle state. The synthesis gate composes `router.md` + `http.md` into the
deliverable `router-and-http.md` at this workspace (repo target `design/ferric/router-and-http.md`) and folds
this task `SUSPENDED → COMPLETED` via `engine_resume_suspended` with `SYNTHESIS.md` as the seam.

## Note recorded during decomposition

The engine's methodology loader returned `agent_domain_unset` throughout this invocation, so no methodology
bundle was loadable. Decomposition proceeded on the brief, the hub, the inherited contract, and the design
persona. Each child brief instructs the child to load its own methodology and, if it meets the same condition,
to proceed on its brief and the persona and record the assumption.
