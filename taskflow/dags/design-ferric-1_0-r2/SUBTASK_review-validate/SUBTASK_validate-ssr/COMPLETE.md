# COMPLETE — SUBTASK_validate-ssr

## What was done

Read `ssr-hydration.md` from branch `work/design-ferric-1_0` and validated it against
`crates/ferric/` at commit `276138f` on `main`. Produced `concern-findings.md` conforming to
`../contracts/_MANIFEST.yaml` §concern_findings_schema.

## Outputs

- `concern-findings.md` — validation findings for the SSR + Hydration concern

## Summary

**Status**: needs-fix

**REQ-SSR-* register**: 12 requirements found (REQ-SSR-001 through REQ-SSR-012), all
`stage: one_oh`, all `release_gating: true`. REQ-SSR-004 is the gating must-have.

**Architecture accuracy**: All factual claims about the codebase at `276138f` check out —
`dom::mount` clearing root before render, `vdom`/`component` being `web-sys`-free, path-based
DOM resolution, thread-local reactive arena with `Box<dyn Any>`, and `Rc<dyn Fn()>` event
handlers are all confirmed by reading the source.

**Gaps found**: 2

- GAP-010 (major): The reactive context contract for `render_to_string` is not specified. The
  design requires per-request isolation (REQ-SSR-003) and mentions "performs no effects" (§2.1)
  but does not make "bypass the reactive observer stack" an explicit design constraint. An
  implementer who follows `mount`'s `create_effect` pattern would silently leak subscriptions
  and violate isolation. The fix is to name this constraint in REQ-SSR-001 or §2.1.

- GAP-011 (minor): No bar for component panics during server-side rendering. The document
  specifies mismatch recovery on the client (§3) but is silent on what happens if a component
  panics during `render_to_string`. A short recorded deferral or a `Result<String, ...>` contract
  would close this.
