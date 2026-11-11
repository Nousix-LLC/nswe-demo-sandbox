# _FORK.md — design-chirp-r1 (thread fork hub)

owner_id: overseer/I56
forked_by: overseer/I56
thread_type: dag
launch_agent: swe-designer
launch_kernel: inherit
disposition: reap-whole-after-land
observation_seam: /home/user/nousix-runtime/nswe-demo/taskflow/dags/design-chirp-r1/SYNTHESIS.md
launch_context: { application: software, model_default: claude-opus-4-8 }

## Context
Product design DAG for `Nousix-LLC/nswe-demo` — the engagement's **first product design**. The software has
reached the cluster and runs (ArgoCD `chirp` Synced+Healthy at `c805525`; `/healthz` → 200), but no design and
no explicit, testable **release bar** have ever been written (`design.standing` is null; there is no `design/`
or `docs/` tree in the repo). This DAG establishes the release bar for chirp as a releasable Twitter-style
product, turns it into a reviewable design PR and a traceable board backlog, and measures the live product at
`c805525` against the bar it sets. It writes design and tickets, not product code. The full task spec — the
objective, inputs, the concerns to cover with their bars, the declared output, and the constraints — is in
this directory's `_BRIEF.md`. No methodology is named here or in `launch_context`; the DAG selects and loads
its own design-domain methodologies from what the brief describes.

## Reap policy
`reap-whole-after-land`: scratch DAG, reaped whole once its residue has landed or been recorded by the
overseer (the design PR merged, its tickets placed on the board, and its release bar + measured standing folded
into STATE). Never reaped piecemeal while live. A failed/rejected attempt's lesson goes into the next design
DAG's brief; the deliberation is dropped.
