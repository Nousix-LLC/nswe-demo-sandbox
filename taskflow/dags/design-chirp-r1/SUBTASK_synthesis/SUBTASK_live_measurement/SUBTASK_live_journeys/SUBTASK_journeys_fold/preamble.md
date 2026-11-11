# Live-product measurement — `manual_user_check` journeys (chirp)

This is the `manual_user_check` partition of the live-product measurement for chirp
(`Nousix-LLC/nswe-demo`), judged against the deployed product at commit `c805525`. It holds
one verdict row for each of the 139 release-bar criteria whose declared `verification_method`
is `manual_user_check`, keyed by `bar_id`, with columns `bar_id, live_status, observation`
and exactly one `live_status` ∈ {met, partial, missing, not_applicable} per criterion.

The 139 criteria were measured across nine journey and surface clusters — getting in and
identity, the core value loop, account management and lifecycle, resilience and feedback
states, safety and trust and support, the navigation shell and visual craft, the
typical-phone responsive experience, the keyboard and screen-reader accessibility path, and
web delivery with the API as a user experiences it — and this table is their union. Each
criterion is measured once, by the cluster the sub-contract assigns it; the partition is
disjoint and total — nine clusters, 139 criteria, each under exactly one cluster. The
verdicts and their observations are carried through from the clusters verbatim: this fold
unions the nine tables and checks totality and vocabulary, and does not re-judge any
criterion.

**Access.** The live product was reached and exercised read-only for every cluster. Both
surfaces answered at `c805525`: the single-page app was served and the JSON API responded.
Identity and account surfaces were walked with throwaway test accounts doing only their own
ordinary actions; nothing else was mutated. Where the running UI — a compiled WebAssembly
single-page app — could not be driven to settle a verdict in this environment, the presence
or absence of a surface was confirmed against the SPA and API source at `c805525`, cited by
repository-relative path in the observation. The product at `c805525` runs on an in-memory
store and omits whole release-layer surfaces (recovery, settings, sessions and devices,
export, deletion, reporting, the operator surface, status); those absences are confirmed,
not presumed, and are recorded as grounded `missing`, `partial`, or `not_applicable` with
the reason stated.

**Design methodology loader.** The `design` methodology loader was unavailable for this run
(`agent_domain_unset`); the measurement applied the principal-product-designer persona and
the relayed release-bar guidance, recorded the limitation, and proceeded.

**Standing against the bar (this partition).** Of the 139 `manual_user_check` criteria:
**met 27, partial 46, missing 65, not_applicable 1**. The backend core loop and the
one-address web and API delivery are largely present; the get-in and identity surfaces, the
whole account-lifecycle and safety/trust/support surfaces, and the designed visual and
resilience treatments are where the product falls short of the bar. This is one of the four
verification-method partitions of the live measurement; the cross-method union, the
traceability matrix, and the product's overall standing against the release bar are
assembled above this fold.

## Verdict table

One row per `manual_user_check` `BAR-*`, ordered by `bar_id`.

