# _FORK.md — design-ferric-1_0-r3 (authored by NSWE overseer swe-lead, iteration I146)

## Fork context
owner_id: overseer/I146
observation_seam: /home/user/nousix-runtime/nswe-demo/taskflow/dags/design-ferric-1_0-r3/SYNTHESIS.md

## Reap policy (kernel metadata the reaper reads)
disposition: reap-whole-after-land

## Launch (the launch agent the forked actor boots with)
launch_agent: swe-designer
launch_kernel: inherit
thread_type: dag
launch_context: { application: software, model_default: claude-opus-4-8 }

## Notes (non-schema context)
Design gap review of PR#128 (`design: Ferric 1.0 framework design`, branch work/design-ferric-1_0, head bbdeb480). PR is OPEN, CLEAN, all CI green. No prior review. The design covers the complete Ferric 1.0 framework under design/ferric/ (14 documents). Issues #129–#164 (36 items: 8 epics + 28 features) were filed from this design and are now on the project board as Todo. This review evaluates: completeness against the 1.0 directive (#114), the release bar (concrete and testable), internal coherence and traceability, buildability on the existing foundation (ferric-foundation/router/http), and ticket quality and wave plan. Delivers APPROVE or REQUEST-CHANGES verdict posted on PR#128 and in SYNTHESIS.md. Non-blocking findings filed as board issues.
