# COMPLETE — SUBTASK_visual_craft_nav

**Task**: Measure the 16 `manual_user_check` `BAR-*` of the navigation-shell / visual-craft cluster against the
live chirp product at commit `c805525`, each `met | partial | missing | not_applicable` with a grounded
observation.

**Decompose evaluation**: Atomic. One coherent read-only measurement pass over one surface (how the product
navigates, reads, and holds together), producing one verdict table — all triggers cleared, both concern tests
passed (16 homogeneous "judge this `BAR-*` against the rendered product" checks, one output, within the atomic
tool-call envelope).

## Output

- `outputs/visual-craft-nav-measurement.md` — access-note header + a `bar_id`-keyed verdict table conforming to
  the inherited `verdict_row_schema` (columns `bar_id, live_status, observation`), one row per owned `BAR-*`.

## What was done

- Reached the live deployment read-only (web root serves the SPA shell; health endpoint reports the
  `chirp-server` service healthy, version `0.1.0`). Confirmed the deployed revision's product crates are
  byte-identical to `c805525` (only docs/`design/`/deploy manifests differ in that range), so the running
  product renders the `c805525` SPA.
- Grounded each criterion in the `c805525` SPA source (Rust/WASM frontend `crates/chirp-frontend`, `ferric` /
  `ferric-router`) where the rendered judgement needed exact markup/tokens/type treatment, since the build
  carries no CSS or token files beyond the small inline `<style>` in `index.html`.
- Measured contrast with a tool for the product's colours: body text 21:1, button text 18.3:1, default field
  border 4.54:1, accent link `#1d9bf0` 3.0:1 (fails the 4.5:1 normal-text bar). One shipped theme.
- Exercised navigation (History-API back/forward), compose (login + post, counter, busy/error feedback),
  timeline (chirp row, pagination, states), and profile (follow/like) via a single throwaway handle.

## Verdicts

16 `BAR-*` judged, each exactly once; none omitted, none outside the assigned set. Distribution: met 0,
partial 9 (BAR-202, BAR-208, BAR-215, BAR-216, BAR-217, BAR-219, BAR-223, BAR-225, BAR-229), missing 7
(BAR-201, BAR-204, BAR-220, BAR-221, BAR-222, BAR-224, BAR-227), not_applicable 0. The product at `c805525`
is a walking-skeleton SPA: a two-entry nav over three routes, no design-token set, no themes, no library
components, and no menu/dialog/toast/motion surfaces — which drives the seven `missing` verdicts; the nine
`partial` verdicts reflect behaviour that holds by uniform browser defaults or on the compose/post path while
the designed treatment (active-nav marking, per-screen tab title, generous leading, quiet meta text, accent
contrast, phone gutter, counter/card/like treatment, explicit follow confirmation) is absent.

## Success criteria

- [x] Every owned `BAR-*` has exactly one `live_status` from the inherited vocab and a grounded observation;
      none omitted; no `BAR-*` outside this cluster included.
- [x] Each observation grounded in an actual exercise of the live product or a `c805525` source artifact;
      unobservable/absent surfaces judged conservatively with the reason stated.
- [x] `bar_id`s verbatim; `live_status` values from `{met, partial, missing, not_applicable}`.
- [x] Read-only on the live product (GET + one throwaway login); output touches only `Nousix-LLC/nswe-demo`
      and the project's own deployment; no host/system/taskflow detail in the output (repository identity and
      commit SHA only).

## Limitation recorded

The Phase-B `design` methodology loader was unavailable run-wide (`agent_domain_unset`); recorded and proceeded
with the principal-product-designer persona and relayed ReleaseBar guidance, as every gate node did.
