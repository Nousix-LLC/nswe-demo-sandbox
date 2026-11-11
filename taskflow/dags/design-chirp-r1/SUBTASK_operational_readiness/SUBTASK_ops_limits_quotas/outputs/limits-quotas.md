## limits_and_quotas

chirp is a public, internet-facing consumer web application: anyone can reach it, and the write surface —
posting a chirp, following an account, liking a chirp — is open to any signed-in account, with an
unauthenticated surface (the landing page, sign-up, sign-in) open to anyone at all. A surface like that,
released with no limits, can be driven past what the service can carry by a single script, and can be used
by one account to bury everyone else's timeline. This section states the rate, size, and volume limits a
release needs so that neither happens: the operational first line against overload and trivial abuse.

These are requirements, not an implementation. Where a limit belongs (the edge, a gateway, the application),
which algorithm enforces it (token bucket, leaky bucket, fixed window), and the exact numeric thresholds are
the later code work's to decide. What a release owes is that the limits exist, that exceeding one is handled
by refusing or slowing the excess rather than serving it without bound, and that the caller is told. The
numbers themselves are deliberately left to enforcement: a requirement that hard-codes "N requests per
minute" ages badly and tells a tester nothing they can check against intent. The requirements below fix the
*behaviour* and leave the *threshold* to be set — and re-set — operationally.

**What this section covers and what it leaves to its neighbours.**

- **Rate and volume.** A per-client limit on the overall request rate, tighter limits on the actions that
  create state, and a bounded volume of created content per account over a longer window. Together these are
  the two halves of "cannot overwhelm the service" and "cannot flood others" (`REQ-PROD-041`).
- **Size, at the edge.** A cap on request body size, and the page-size cap on list reads. The per-field
  content bounds are already fixed by the domain design and are **referenced, not restated** here: a chirp
  body is 1–280 characters (`REQ-DOM-012`) and a handle is 1–15 characters (`REQ-DOM-002`). The operational
  requirement is that oversized input is refused at the edge, before it reaches a handler, consistent with
  those bounds. Timeline reads are already required to come back a bounded page at a time behind an opaque
  cursor with a server-enforced maximum (`REQ-DOM-027`, `REQ-DOM-218`); the operational requirement is that
  this cap is enforced on every list surface so no client can ask for an unbounded page.
- **The over-limit response.** When a limit is hit, the product rejects or throttles the excess and tells the
  caller with a typed, machine-readable error, consistent with the error contract (`REQ-DOM-220`). A limit
  that silently drops work, or that answers with an ad-hoc string the frontend cannot branch on, is not a
  finished limit.

**Boundaries — what this section references but does not own.**

- **Account-level abuse controls belong to identity and trust (`REQ-ID-*`).** The limits here are coarse and
  content-blind: they bound how fast and how much any client may do, not *who* a client is or whether a
  specific account is behaving abusively. Blocking and muting another account, reporting abuse, stated rules,
  and the operator's supported action on an abusive account are the identity/security and product-safety
  designs' (`REQ-ID-*`, and `REQ-PROD-025` / `REQ-PROD-028`). Rate and volume limiting is the first line that
  holds while those controls do their slower, account-specific work; it is not a substitute for them.
- **Operational access control (board follow-up #24).** Follow-up **#24** (least-privilege delivery RBAC and
  supply-chain hardening) concerns who and what may change the *running system* through the delivery and
  control plane — a privileged, operator-and-automation-facing access posture, distinct in subject from the
  public, client-facing rate and volume limits owned here. Its substance is an operational access/limits
  matter, but it bounds privileged control-plane actors rather than public clients. It is **referenced here
  for the synthesis gate to place**, not re-filed and not owned as a `REQ-OPS-04x` limit; the synthesis gate
  owns the final placement of #24 across the operational-readiness sections.

### Requirements

#### REQ-OPS-040 — The public request rate is bounded per client
- **statement**: The product bounds the rate of requests it will accept from a single client, so one client cannot drive the service past what it can serve for everyone else by issuing requests as fast as it can. The threshold, the client-identification basis, and the enforcement point are set operationally; the requirement is that a bound exists and is applied per client rather than only in aggregate.
- **acceptance_criteria**: From a single client, issue requests far faster than a person using the product would; past a point the product stops serving the excess (it refuses or slows further requests) rather than accepting every request without limit, and other clients continue to be served normally meanwhile.
- **verification_method**: operational_check
- **release_gating**: true
- **traces_to**: REQ-PROD-041

#### REQ-OPS-041 — State-creating actions are rate-limited more tightly than reads
- **statement**: The actions that create state — posting a chirp, following an account, liking a chirp — are subject to their own, tighter rate limit than ordinary reads, so a single account cannot flood timelines or follow/like en masse at machine speed. The specific limits are operational; the requirement is that a write-rate bound exists on each state-creating action.
- **acceptance_criteria**: Signed in, perform one state-creating action (for example posting) repeatedly, far faster than a person would; past a point the product refuses or throttles the further writes rather than accepting them without limit. Reading remains possible within its own limit while writes are being throttled.
- **verification_method**: operational_check
- **release_gating**: true
- **traces_to**: REQ-PROD-041

#### REQ-OPS-042 — Created volume per account is bounded over a longer window
- **statement**: Beyond the short-term write rate, the volume of content a single account can create over a longer rolling window is bounded, so an account cannot flood others by sustaining an at-the-limit rate indefinitely. This is the "volume" half of the product's rate-and-volume requirement, distinct from the burst limit of REQ-OPS-041. The window and the cap are operational; the requirement is that a sustained-volume bound exists per account.
- **acceptance_criteria**: With one account, create content continuously at or just under the per-action rate limit for a sustained period; the product eventually bounds the account's further creation for that window rather than allowing unbounded accumulation, and resumes in a later window.
- **verification_method**: operational_check
- **release_gating**: true
- **traces_to**: REQ-PROD-041

#### REQ-OPS-043 — Oversized request bodies are refused at the edge
- **statement**: The product enforces a maximum request body size and refuses a request whose body exceeds it before the body is processed, so a client cannot consume unbounded memory or processing by sending an enormous payload. The cap is consistent with the already-fixed content bounds — a chirp body of 1–280 characters (REQ-DOM-012) and a handle of 1–15 characters (REQ-DOM-002) — and exists to stop payloads far larger than any valid request, not to re-enforce those per-field rules.
- **acceptance_criteria**: Send a request whose body is far larger than any valid chirp or form submission (for example a multi-megabyte body to a write endpoint); the product refuses it with an error and does not attempt to process the oversized body. A normal, within-bounds request to the same endpoint succeeds.
- **verification_method**: automated_test
- **release_gating**: true
- **traces_to**: REQ-PROD-041, REQ-DOM-012, REQ-DOM-002

#### REQ-OPS-044 — List reads are served only as bounded pages
- **statement**: Every endpoint that returns a list enforces the server's maximum page size, so no client can force the product to assemble and return an unbounded result in one response. This is the operational enforcement of the domain requirement that timelines are read a bounded page at a time behind an opaque cursor (REQ-DOM-027, REQ-DOM-218); the operational requirement is that the cap holds on every list surface, not only the timeline.
- **acceptance_criteria**: Request a list with no page size, and request one with a page size well above the server maximum; in both cases the response carries at most the server's maximum number of items, with a continuation cursor when more remain, rather than the full result set.
- **verification_method**: automated_test
- **release_gating**: true
- **traces_to**: REQ-PROD-041, REQ-DOM-218, REQ-DOM-027

#### REQ-OPS-045 — Exceeding a limit refuses or throttles the excess and says so
- **statement**: When any limit in this section is exceeded, the product rejects or throttles the excess rather than serving it without bound, and tells the caller with a typed, machine-readable error carrying a distinct category for being rate- or size-limited, consistent with the error contract (REQ-DOM-220). The caller can tell "you were limited" apart from other failures and can act on it (for example back off and retry later).
- **acceptance_criteria**: Drive any one of the limits above past its threshold; the response is an error whose machine-readable category identifies it as a limit being hit — distinct from a validation error or a not-found — and the excess work is not performed. The error is the typed contract category, not an ad-hoc string.
- **verification_method**: operational_check
- **release_gating**: true
- **traces_to**: REQ-PROD-041, REQ-DOM-220

#### REQ-OPS-046 — The unauthenticated surface is limited too
- **statement**: The request-rate limit applies to the unauthenticated surface — the landing page, sign-up, and sign-in — identified by client rather than by account, so a client cannot escape limiting simply by not signing in, and the pre-sign-in surface cannot be used as an unbounded overwhelm or credential-guessing vector. This bounds request volume on that surface; account-specific abuse handling and credential-attempt lockout belong to the identity design (REQ-ID-*) and are referenced, not owned here.
- **acceptance_criteria**: Without signing in, issue requests to a public, unauthenticated endpoint far faster than a person would; past a point the product refuses or throttles the excess, the same as for an authenticated client.
- **verification_method**: operational_check
- **release_gating**: true
- **traces_to**: REQ-PROD-041

#### REQ-OPS-047 — Under aggregate overload, the product sheds rather than collapses
- **statement**: When total load exceeds what the product can serve — even from many within-limit clients at once — the product sheds or throttles the excess and keeps serving the traffic it can, rather than failing wholesale for everyone. This protects the product's reachability and reasonable availability (REQ-PROD-040) and is the aggregate counterpart to the per-client limits above. The capacity point and the shedding policy are operational.
- **acceptance_criteria**: Apply aggregate load beyond the product's serving capacity; the product continues to serve a bounded share of requests (and reports the rest as limited or unavailable per REQ-OPS-045) rather than becoming unresponsive to all callers, and it recovers to normal service when the load subsides.
- **verification_method**: operational_check
- **release_gating**: false
- **traces_to**: REQ-PROD-040, REQ-PROD-041

#### REQ-OPS-048 — Limits sit above ordinary use
- **statement**: The limits in this section are set above the rate and volume of ordinary legitimate use, so a person using the product normally — reading a timeline, posting through the day, following and liking as they browse — does not hit them. Limiting targets abuse and overload, not use; a limit that blocks a normal person is a worse product than a more generous one. The thresholds are operational, but the requirement that they clear ordinary use is a release requirement.
- **acceptance_criteria**: As one person, use the product the way a normal user would over a normal session — browse, post several times, follow and like a reasonable number of accounts — without being rate- or volume-limited. Only usage well beyond what a person does by hand triggers a limit.
- **verification_method**: manual_user_check
- **release_gating**: false
- **traces_to**: REQ-PROD-041
