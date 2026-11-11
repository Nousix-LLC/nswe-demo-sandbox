# _FORK.md — fork hub for deploy-argocd (#13 code DAG)

owner_id: overseer/I48
forked_thread_id: deploy-argocd
thread_type: dag
launch_agent: swe-coder
launch_kernel: inherit
disposition: reap-whole-after-land
observation_seam: /home/user/nousix-runtime/nswe-demo/taskflow/dags/deploy-argocd/SYNTHESIS.md
launch_context: { application: software, model_default: claude-opus-4-8 }

## Fork context
This DAG is NSWE work-item #13 (deploy-argocd): author `deploy/` k8s manifests + an ArgoCD Application (GitOps on
k3s) for the chirp app, demonstrate reachability on the live k3d-hosted k3s cluster, and open a PR into `main`
that closes #13. Its whole task spec is `_BRIEF.md` at this workspace root (objective, acceptance criteria,
inputs, declared output, the named concerns incl. #24 RBAC/supply-chain and #23 durability caveats, and
constraints). The DAG selects and loads its own methodology and decides its own decomposition.

## Reap policy
Scratch. Reaped whole (`reap-whole-after-land`) once its residue has landed or been recorded: the PR merged (or
rejected) and its review's findings on the board. Failed/rejected attempts are reaped too; the lesson is carried
forward into the next DAG's brief, the deliberation is dropped. Not reaped while live.

## Observation seam
The owner (`overseer/I49`, continuing the overseer thread) gates on the folded ROOT `SYNTHESIS.md` at
`observation_seam` — never on a side-effect (pushed branch, posted comment, subtask marker) or a reconstruct-time
force-complete with no SYNTHESIS.md.
