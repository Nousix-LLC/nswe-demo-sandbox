# _FORK.md — deploy-ghcr-auth (thread fork hub)

owner_id: overseer/I51
forked_thread_id: deploy-ghcr-auth
thread_type: dag
launch_agent: swe-coder
launch_kernel: inherit
disposition: reap-whole-after-land
observation_seam: /home/user/nousix-runtime/nswe-demo/taskflow/dags/deploy-ghcr-auth/SYNTHESIS.md
launch_context: { application: software, model_default: claude-opus-4-8 }

## Fork context

Devops remediation DAG forked by the NSWE project overseer (`overseer/I51`) for `Nousix-LLC/nswe-demo`. It
resolves review finding **F1 of issue #29** on the just-merged `#13` (deploy-argocd): after `main @ 22d2df6`,
ArgoCD applies the committed private-GHCR digest and the pod is in ImagePullBackOff (`401`, no `ghcr-pull`
credential). The DAG makes the committed GitOps desired state pull the digest and stay reachable. Full task
spec, acceptance criteria, inputs, and constraints are in this workspace's `_BRIEF.md`.

## Reap policy

- `reap-whole-after-land`: scratch DAG, reaped whole once its residue has landed (any PR merged) or been
  recorded in the overseer's STATE and the item is closed. Failed/rejected attempts are reaped too; the lesson
  carries forward into the next DAG's brief, the deliberation is dropped.
- The overseer observes this DAG only via the `observation_seam` (root `SYNTHESIS.md`); it gates on the folded
  root verdict, never on a side-effect. P1: the overseer never edits this DAG's code.

## Methodology

None pinned here. The DAG selects and loads its own methodology from the concerns named in `_BRIEF.md`
(rollout correctness, GitOps convergence, supply-chain/least-privilege security, operability). Do not carry any
previous DAG's methodology selection forward.
