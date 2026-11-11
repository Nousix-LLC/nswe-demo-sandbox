# _FORK.md — review-security-persist-r1 (authored by NSWE overseer swe-lead)

## Fork context
owner_id: proc-72edf6e1-d6be-4a8e-9501-c556acaf8cd8
observation_seam: /home/user/nousix-runtime/nswe-demo/taskflow/dags/review-security-persist-r1/SYNTHESIS.md

## Reap policy (kernel metadata the reaper reads)
disposition: reap-whole-after-land

## Launch (the launch agent the forked actor boots with)
launch_agent: swe-reviewer
launch_kernel: inherit
thread_type: dag
launch_context: { application: software, model_default: claude-opus-4-8 }

## Notes (non-schema context)
Review of PR #182 (work/security-persist-r1 → main) closing issue #120 (persistence security hardening: argon2id KDF credential storage + CronJob TLS). Code DAG security-persist-r1 folded PASS (all four gate checks clear). This review DAG (swe-reviewer) reviews PR #182 against the five concerns in the brief, posts the review on PR #182, and lands under delegated authority (auto_land: true) on APPROVE.
