# COMPLETE — SUBTASK_validate-router

**Task**: Validate router-and-http.md (REQ-RT-*, REQ-HTTP-*) against prior-art drafts  
**Status**: completed  
**Evaluation**: Atomic

## What was done

Read `router-and-http.md` from branch `work/design-ferric-1_0` via `git show` at `/home/user/nswe-demo`. Read prior-art drafts at `../prior-art/router-and-http.md` and `../prior-art/router-and-http.SYNTHESIS.md`. Compared content against all validation criteria in the brief and assessed each in turn.

## Declared output

`concern-findings.md` — written at `SUBTASK_validate-router/concern-findings.md`.

## Findings summary

- **Status**: needs-fix (two minor issues)
- **REQ-RT-* ids found**: REQ-RT-001 through REQ-RT-009 (9 total; REQ-RT-009 is a recorded post-1.0 deferral)
- **REQ-HTTP-* ids found**: REQ-HTTP-001 through REQ-HTTP-013 (13 total; all release-gating true)
- **All core validation criteria pass**: additive over #5/#6, nested routes testable, route parameters testable, active-link state testable, typed JSON testable, per-request timeouts testable, no prefix mixing
- **Two minor gaps logged**: GAP-040 (missing REQ-FW-007 coverage table) and GAP-041 (Metadata section cites internal SYNTHESIS.md artifact)

## Composition note

The branch version is essentially identical to the prior-art `router-and-http.md` in content. The synthesis fold record (`router-and-http.SYNTHESIS.md`) confirms all six identities (SI1–SI6) passed in the original authoring DAG. The branch version adds conformance annotations (`*(section: ...)*` markers) and explicit contract references at the top, consistent with the design system conventions.
