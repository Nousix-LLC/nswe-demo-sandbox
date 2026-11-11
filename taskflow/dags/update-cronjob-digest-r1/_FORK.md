# _FORK.md — update-cronjob-digest-r1 (authored by NSWE overseer swe-lead, iteration I180)

## Fork context
owner_id: overseer/I180
observation_seam: /home/user/nousix-runtime/nswe-demo/taskflow/dags/update-cronjob-digest-r1/SYNTHESIS.md

## Reap policy (kernel metadata the reaper reads)
disposition: reap-whole-after-land

## Launch (the launch agent the forked actor boots with)
launch_agent: swe-coder
launch_kernel: inherit
thread_type: dag
launch_context: { application: software, model_default: claude-opus-4-8 }

## Notes (non-schema context)
Minimal one-file manifest change: update the image digest in deploy/chirp/50-transient-sweep-cronjob.yaml from sha256:adaa4c26... (old c3f9f558 build) to sha256:2c5eafbe... (new febeb151 build from CI run 41710206505). The new image contains the chirp-server sweep subcommand introduced by PR #183 (issue #117). Until this lands, ArgoCD is OutOfSync/Degraded on febeb151 — the CronJob fails loudly with the old binary.
