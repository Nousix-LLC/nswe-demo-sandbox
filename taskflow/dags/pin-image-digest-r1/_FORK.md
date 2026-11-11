# _FORK.md — pin-image-digest-r1 (authored by NSWE overseer swe-lead, iteration I151)

## Fork context
owner_id: overseer/I151
observation_seam: /home/user/nousix-runtime/nswe-demo/taskflow/dags/pin-image-digest-r1/SYNTHESIS.md

## Reap policy (kernel metadata the reaper reads)
disposition: reap-whole-after-land

## Launch (the launch agent the forked actor boots with)
launch_agent: swe-coder
launch_kernel: inherit
thread_type: dag
launch_context: { application: software, model_default: claude-opus-4-8 }

## Notes (non-schema context)
Minimal one-line deployment manifest change: replace the placeholder image digest in deploy/chirp/10-deployment.yaml with the actual digest published by the post-merge CI run for commit 0d5917dc. Tracks issue #180 and unblocks #64 closure.
