# _FORK.md — containerize (#12) devops DAG fork hub

owner_id: overseer/I40
observation_seam: /home/user/nousix-runtime/nswe-demo/taskflow/dags/containerize/SYNTHESIS.md
disposition: reap-whole-after-land
launch_agent: swe-coder
launch_kernel: inherit
thread_type: dag
launch_context: { application: software, model_default: claude-opus-4-8 }

## Fork context (human-readable)
Forked by overseer iteration I40 as the one demand-driven fork this iteration (ladder priority-4: next unblocked
devops work-item; app layer complete and nothing landable/reviewable/remediable — #10 infra-bootstrap and #11
ci-actions both in flight and advancing, not folded). Work-item #12 containerize (EPIC #3): a multi-stage
Dockerfile + .dockerignore packaging the chirp-frontend wasm SPA bundle and the chirp-server release binary into
a small, non-root, healthchecked runtime image. Deps #8 chirp-server + #9 chirp-frontend landed on main @
fcfc7a2e02d931ab1b499c8fac1747c77ec3a64e — unblocked now. Its Dockerfile is also what #11's GHCR image-build job
awaits. Methodology concerns are named in _BRIEF.md (the DAG selects/loads its own bundles — do not carry a prior
DAG's selection forward); _FORK.md holds only kernel/identity metadata. Delivers commits on work/containerize, a
PR into main Closes #12, and a root SYNTHESIS.md; does not merge its own PR or push to main (P1). Scratch:
reap-whole-after-land.
