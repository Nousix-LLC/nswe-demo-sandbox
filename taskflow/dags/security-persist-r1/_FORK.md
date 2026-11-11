# _FORK.md — security-persist-r1 (authored by NSWE overseer swe-lead)

## Fork context
owner_id: proc-92e571d0-9def-4b16-b7a1-5982d4c564de
observation_seam: /home/user/nousix-runtime/nswe-demo/taskflow/dags/security-persist-r1/SYNTHESIS.md

## Reap policy (kernel metadata the reaper reads)
disposition: reap-whole-after-land

## Launch (the launch agent the forked actor boots with)
launch_agent: swe-coder
launch_kernel: inherit
thread_type: dag
launch_context: { application: software, model_default: claude-opus-4-8 }

## Notes (non-schema context)
Persistence security follow-ups from PR #113 review (issue #120). Two security concerns: (1) plaintext
credential at rest with non-constant-time compare in the durable store — fix with salted KDF (argon2/bcrypt)
and constant-time verify; (2) in-cluster DB traffic unencrypted in the CronJob manifest — fix with
sslmode=require. Priority: high. Branch: work/security-persist-r1.
