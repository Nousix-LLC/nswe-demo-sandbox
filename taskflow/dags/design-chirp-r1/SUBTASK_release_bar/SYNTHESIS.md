# SYNTHESIS — SUBTASK_release_bar (release-bar assembly, staging, gap review, fold)

Fold record for the `SUBTASK_release_bar` subtree. This is the synthesis gate's terminal record and the record
the fold consumes to flip `SUBTASK_release_bar` SUSPENDED → COMPLETED. Taskflow-internal (not repository content).

## What this task did

Integrated the five per-area `BAR-*` fragments into the single deliverable `SUBTASK_release_bar/outputs/release-bar.md`
(the parent's declared output, repo path `design/release-bar.md`) with its three required sections; finalized the one
cross-cutting MVP-vs-releasable staging line; ran the whole-design completeness & gap review; asserted the eight
subtree contract identities with recorded evidence; and folds the parent.

**Resume note.** This node was reconstructed and re-dispatched: an earlier invocation had assembled
`outputs/release-bar.md` and a draft fold record but had not completed the fold. This invocation did not trust the
prior artifacts on faith. It re-ran the gate from scratch — a fresh, independent verification that parses the five
fragments, the five area design docs, and the assembled deliverable directly and re-derives every mechanical identity —
before completing the terminal sequence. The independent run reproduced the prior assembly exactly (278 criteria,
148/130 staging, gating total 342); the deliverable was left unchanged because verification found it correct, not
because it was assumed correct.

**Fragments merged** (owning spoke → range → count, confirmed by parsing each fragment's `BAR-*` blocks):
- `SUBTASK_bar_prod/outputs/bar-prod.md` → `BAR-001..035` → 35
- `SUBTASK_bar_dom/outputs/bar-dom.md` → `BAR-100..120, 130..148, 160..179` → 60
- `SUBTASK_bar_ux/outputs/bar-ux.md` → `BAR-200..263, 265..294` → 94 (`BAR-264, 295..299` reserved, unused)
- `SUBTASK_bar_id/outputs/bar-id.md` → `BAR-300..339` → 40
- `SUBTASK_bar_ops/outputs/bar-ops.md` → `BAR-400..412, 420..432, 440..445, 460..468, 480..487` → 49

Total **278** criteria. The register in `release-bar.md` is generated directly from the fragment blocks; the
verification confirmed that every register entry's `references` (`REQ-*`) and `verification_method` match its source
fragment block verbatim (0 mismatches over 278 bars), so no criterion was altered or paraphrased in the merge. The
fragments carry mixed heading depths (`### BAR-*` in prod/ux, `#### BAR-*` in dom/id/ops); the parser reads both.

**Methodology posture.** The Phase-B `design` methodology loader was unavailable run-wide (`agent_domain_unset`), as
recorded in `_GLOBAL.md`; the product-design persona's release-definition judgment and the relayed bundle guidance
(Release Definition primary; Release Readiness, Product Strategy, Identity and Trust, Product Surfaces supporting)
were applied instead. This note is internal; it is not in the repository-bound deliverable.

## Identity verdicts (independent evidence recorded; no silent plugs)

All eight identities in `contracts/_MANIFEST.yaml` hold. Evidence is from this invocation's own verification pass over
the five fragments, the five area design docs, and the assembled `release-bar.md`. The gating sets were derived by
walking each design doc's `#### REQ-<AREA>-NNN` blocks and reading each block's `release_gating` flag — not by a naive
line count, which over-reports (e.g. the operational-readiness doc carries 118 `release_gating: true` lines across 75
distinct `REQ-OPS-*` blocks; the authoritative gating set is the 59 distinct ids flagged true in their own blocks).

1. **BAR_RANGE_RESPECTED — PASS.** Every defined `BAR-NNN` lies within its owning spoke's partition: prod 35 ⊂
   001–099; dom 60 ⊂ 100–199; ux 94 ⊂ 200–299; id 40 ⊂ 300–399; ops 49 ⊂ 400–499. Out-of-range ids: **0**.
2. **NO_BAR_COLLISION — PASS.** 278 ids defined across the five fragments plus the (unused) synthesis cross-cutting
   range; 278 distinct; duplicates: **0**.
3. **GATING_REQ_COVERAGE — PASS.** Gating set per area, computed per-`REQ`-block from each design doc, then checked ⊆
   the set of `REQ` ids referenced by the `BAR-*` blocks (cross-area references allowed). Gating counts: PROD 35,
   DOM 79, UX 106, ID 63, OPS 59 = **342**, each referenced by ≥1 `BAR-*`. Uncovered gating requirements in every
   area: **0**. No per-block `release_gating` flag was missing or self-conflicting in any area.
4. **BAR_TESTABLE — PASS.** All 278 `BAR-*` name a `verification_method` from the frozen vocabulary
   (`manual_user_check | automated_test | inspection | operational_check`) and reference ≥1 `REQ-*`. Bars missing a
   method or a reference: **0**.
5. **BAR_STAGED — PASS.** The register's final stages are the authoritative map. Every `BAR-*` carries exactly one
   stage ∈ {`usable_early`, `releasable`} (bad/absent stages: 0). The register's bar-id set equals the fragments'
   bar-id set (missing from register: 0; extra in register: 0). The per-area final-stage counts computed from the
   register — PROD 14/21, DOM 50/10, UX 51/43, ID 18/22, OPS 15/34 (**148 `usable_early` / 130 `releasable`**) — match
   the `mvp_vs_releasable_scoping` "by area" table exactly, so the scoping section and the per-bar stages agree. The
   17 reconciliation moves and the 5 deliberately-left-`releasable` persistence criteria were spot-checked against the
   register and land as the scoping section states.
6. **SURFACE_GAP_RECORDED — PASS.** The `completeness_and_gap_review` section records an in/out-of-scope judgment with
   a reason for each of the ten engagement-named surfaces (sign-up, sign-in, recovery, account deletion, data export,
   onboarding, settings, notifications, admin/support, billing) and for nine additional surfaces this product kind
   adds (public landing, reporting abuse, rules/policy, block/mute, discovery/Explore, sessions & devices,
   accessibility statement, status/incident, privacy/retention). Each judgment names where the surface is held
   (`BAR-*`) or why it is out. The three deferrals (notifications, block/mute, discovery) and the one by-product-kind
   exclusion (billing) are each recorded as a stated decision, not an oversight — confirmed by reading the section,
   not only by keyword presence.
7. **THREE_SECTIONS_PRESENT — PASS.** `release-bar.md` contains exactly three top-level `##` sections, in order —
   "MVP-vs-releasable scoping", "Release bar", "Completeness and gap review" — mapping to the required section ids
   `mvp_vs_releasable_scoping`, `release_bar`, `completeness_and_gap_review` in `../contracts/design_artifact_map.yaml`.
8. **HYGIENE — PASS.** A scan for host/cluster addresses, filesystem/taskflow paths, agent/DAG/run ids, internal
   record names (`SYNTHESIS.md`/`SUSPENSION.md`/`_GLOBAL`/`_BRIEF`), attribution trailers, and operator/user/host
   identifiers found **0** hits in the deliverable. It names things only by repository identity (`Nousix-LLC/nswe-demo`,
   commit `c805525`, repo-relative `design/*.md`, `REQ-*`/`BAR-*`). (One candidate flagged by an over-broad first-pass
   pattern — the design phrase "the one namespaced API … in `chirp-types`" — was confirmed to be domain-design content,
   not a cluster namespace reference; the precise host/cluster scan is clean.)

## Staging decisions (the cross-cutting MVP line)

The spokes proposed per-area stages (131 `usable_early` / 147 `releasable`). The final cross-cutting line moved **17**
criteria to `usable_early` so one definition holds across all areas, giving **148 `usable_early` / 130 `releasable`**.
The moves (proposal → final), each stated in the deliverable's "Where the areas were reconciled" subsection:

- **Durable persistence is part of the first usable version (14):** `BAR-130, 131, 132, 133, 134, 135, 136, 137, 138,
  139, 141, 143, 144, 145`, proposed `releasable` by the domain area, moved to `usable_early` to agree with the
  product area (`BAR-013`) and the operational-readiness durable-data floor (`BAR-400..404, 409, 410`) and with the
  stated meaning of a usable version ("what they create persists"). This is the headline `c805525` in-memory-store
  blocker; it belongs in the first usable version, not a later polish.
- **A safe, endable session is part of real identity (2):** `BAR-016` (server-side sign-out), `BAR-113` (session end
  + bounded lifetime), to agree with the identity session floor (`BAR-306`, `BAR-307`).
- **The sign-in signal is part of real authentication (1):** `BAR-010` (no-such-account vs wrong-secret), to agree
  with `BAR-304`.

Deliberately **left `releasable`** (recorded, not hidden): five domain persistence criteria that rest on a
release-layer capability rather than the restart-survival floor — `BAR-140` (restore-integrity; the restart half is
held early by `BAR-403`), `BAR-142` (deletion durability), `BAR-146` (backup/restore), `BAR-147` (export
enumeration), `BAR-148` (upgrade-preserves-data). Their restart-survival dependency is held at `usable_early`.

## Gap-review findings and remediation

The whole-design Product-Surfaces sweep found **no release-gating requirement left without a `BAR-*`** (identity 3)
and **no expected surface that is neither designed nor deliberately waived**. No cross-cutting `BAR-900..999` was
minted: every gap either is held by an area criterion or rests on a requirement the area designs mark non-gating, so
a new bar would duplicate an area criterion or gate a deliberately non-gating item. The reserved cross-cutting range
is therefore unused.

Three surfaces the area designs explicitly left for the release bar to decide were decided here and recorded:
- **Notifications** — not release-gating for v1 (designed, deferred as a near-term fast-follow). Settings shows the
  preferences row only where notifications ship.
- **Block / mute** — not release-gating for v1; the gated safety floor is reporting (`BAR-023/334`) plus operator
  action (`BAR-025/331`), both gated. Block/mute recorded as a fast-follow (identity design's accepted residual risk).
- **Discovery / Explore** — not release-gating for v1; following from a profile or a person row is gated
  (`BAR-005/245`), so a person can build a timeline without a discovery surface; a dedicated Explore surface is a
  near-term follow-up. Recorded as a decision, not left absent by default.

**Billing / tenancy** is out of scope by product kind (a single public consumer product of individual accounts where
no money changes hands — explicit non-goal `need: no-tenancy-or-billing`), so no billing surface exists to gate.

## Derived artifact

The BAR↔REQ coverage map (every `BAR-*` and the `REQ-*` it references, built from the five fragments and confirmed
against each area's per-block gating set) backs the whole-DAG traceability matrix that the DAG-root gate
`SUBTASK_synthesis` consumes. The checked mapping and this invocation's verification script live in this task's
`calculations/` (`verify_gate.py`, re-runnable; plus the prior `bars_final.json` / `barmap.json`).

## Fold

`SUBTASK_release_bar/outputs/release-bar.md` exists and is verified (the parent's declared output). After this record
is reported completed, the parent `SUBTASK_release_bar` is resumed (fold: target `SUBTASK_release_bar`, synthesized
`SUBTASK_bar_synthesis`, seam this file), flipping it SUSPENDED → COMPLETED with `outputs/release-bar.md` as its
output.
