# _FORK.md — remediate-design-ferric-1_0-r1 (authored by NSWE overseer swe-lead, iteration I150)

## Fork context
owner_id: overseer/I150
observation_seam: /home/user/nousix-runtime/nswe-demo/taskflow/dags/remediate-design-ferric-1_0-r1/SYNTHESIS.md

## Reap policy (kernel metadata the reaper reads)
disposition: reap-whole-after-land

## Launch (the launch agent the forked actor boots with)
launch_agent: swe-coder
launch_kernel: inherit
thread_type: dag
launch_context: { application: software, model_default: claude-opus-4-8 }

## Notes (non-schema context)
Design document remediation for PR #128 (`design: Ferric 1.0 framework design`, branch work/design-ferric-1_0). The design-ferric-1_0-r3 review issued REQUEST-CHANGES with 5 BLOCKING findings, all in design/ferric/release-bar.md (Concern 2: release bar testability). This DAG fixes those 5 criteria to be mechanically checkable, commits to work/design-ferric-1_0, and delivers an APPROVE or REQUEST-CHANGES verdict in SYNTHESIS.md. Non-blocking findings (#165-#179) are on the board as Todo and are not in scope for this remediation.
