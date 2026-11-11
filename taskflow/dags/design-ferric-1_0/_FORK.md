owner_id: overseer/I61
observation_seam: /home/user/nousix-runtime/nswe-demo/taskflow/dags/design-ferric-1_0/SYNTHESIS.md
disposition: reap-whole-after-land
launch_agent: swe-designer
launch_kernel: inherit
thread_type: dag
launch_context: { application: software, model_default: claude-opus-4-8 }

# Fork hub — design-ferric-1_0

Design DAG for owner directive #114: take Ferric from a client-side Rust/WASM signals + keyed-VDOM framework
(deps wasm-bindgen/web-sys/js-sys) to a credible 1.0, with server-side rendering + hydration as the one
must-have. Planned under the Ferric epic (#1), folding in the router (#5) and HTTP/JSON-client (#6) issues
already on the board.

- **Kind:** design (product/framework design). Runs as `swe-designer`.
- **Owner:** the NSWE project overseer thread (`overseer`), launched this fork at iteration I61.
- **Observation seam:** the root `SYNTHESIS.md` above — the overseer reads only that folded root verdict
  (release bar + issues indexed by epic), never a subtask synthesis or a posted side effect.
- **Disposition:** `reap-whole-after-land` — reaped whole once the design PR has landed and its tickets are on
  the board.
- **Distinct from** the superseded `design-chirp-r1` zombie (that one is triage-and-discard on fold; this is a
  live, new design to adopt).
- The task spec is in `_BRIEF.md` at this root. Methodology selection belongs to the DAG; none is named here.
