# SUSPENSION.md — chirp-logged-out-r2

**Status:** Suspended / NeedsDecompose  
**Decompose evaluation:** NeedsDecompose

## Decomposition summary

The task was decomposed into three sequential children after applying the TDF's
scope-based triggers (multiple system components: server + frontend) and both concern
tests (Distinct Concerns Test and Single-Responsibility Test both fired).

Chosen cut: serial pipeline by component layer, with an API contract frozen in
`contracts/_MANIFEST.yaml` before any child runs.

| Group | Task ID | Scope |
|-------|---------|-------|
| 0 | chirp-logged-out-server | Branch creation + server public timeline endpoint |
| 1 | chirp-logged-out-frontend | Frontend logged-out experience (depends on server) |
| 2 | chirp-logged-out-synthesis | Verification gate + PR creation (depends on both) |

## Resumption

This task resumes when its entire subtree resolves to terminal states (all three children
complete and the synthesis gate produces `SYNTHESIS.md` and the PR).
