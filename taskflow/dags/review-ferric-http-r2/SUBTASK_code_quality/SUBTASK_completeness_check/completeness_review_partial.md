# completeness_review_partial.md
# Spoke: SUBTASK_completeness_check
# PR: Nousix-LLC/nswe-demo #210 — ferric-http CHANGELOG.md

---

## Concerns Covered

- Concern 5: Documentation completeness as API contract — does the CHANGELOG present a
  credible, consumer-sufficient record of the ferric-http public API changes introduced by
  PR #210, relative to what issues #132 (frozen API surface) and #148 (HTTP client
  documentation) required?

---

## Summary

The CHANGELOG.md added by PR #210 creates a readable and largely complete record of the
ferric-http `usable_early` API surface. All six public types and the `Result` alias are
present with Rust signatures, and every acceptance criterion from issue #148 maps to a
documented API member with an explicit pass marker. The entry correctly bounds its own
scope, deferring PATCH / timeout / lean-footprint work to issue #149.

Three completeness gaps are worth fixing before merge. The `Error` type omits the two
standard Rust trait implementations (`Display` and `std::error::Error`) that consumers
depend on for idiomatic error propagation with `?`; their absence leaves a consumer unable
to confirm that the error type integrates with standard wrapper types. Two `Response`
methods that return the response body (`body(&self) -> &str` vs `text(self) -> String`)
have different ownership semantics and no behavioral differentiation in the CHANGELOG; a
consumer cannot determine which to use without reading source. And `ClientBuilder::
default_header` does not document its accumulation behavior, while the sibling
`RequestBuilder::header` explicitly does — an inconsistency that creates a behavioral gap
in the documented contract.

One advisory: the CHANGELOG entry does not cross-reference the containing epic (#132),
so a consumer reading the CHANGELOG has no path to the roadmap showing what the
`one_oh` stage will add.

4 findings raised (1 SHOULD_FIX, 2 ADVISORY) + 7 CLEAN items recorded.

---

## Findings

**[CLEAN] API-surface coverage — all public members present**
- Principle: A CHANGELOG that claims to freeze a public surface must list every member of
  that surface; missing items leave consumers without a contract for things they may rely on.
- Evidence: `Client`, `ClientBuilder`, `RequestBuilder`, `Response`, `Error`, `Method`,
  and `type Result<T>` are all present with signatures. All items from `ferric_http::prelude`
  that the crate exports are accounted for.
- Resolution: N/A — sound.

**[CLEAN] Acceptance-criteria mapping — all #148 criteria satisfied and mapped**
- Principle: A CHANGELOG serving as formal closure of an issue must demonstrate that every
  acceptance criterion the issue states is covered by a documented API member.
- Evidence: The table at the bottom of the `usable_early` section maps all 10 criteria
  from issue #148 to specific API items, each marked ✅. The two REQ-HTTP entries not in
  #148's scope (REQ-HTTP-009, REQ-HTTP-010) are listed in the deferred section.
- Resolution: N/A — sound.

**[CLEAN] `#[non_exhaustive]` on `Error` documented**
- Principle: Stability attributes that affect consumer code — particularly match
  exhaustiveness — are part of the public contract and must appear in the CHANGELOG.
- Evidence: `#[non_exhaustive]` is explicitly shown on the `Error` enum definition. A
  consumer knows they cannot write an exhaustive `match Error { ... }` without a catch-all,
  and that future variants will not be breaking changes.
- Resolution: N/A — sound.

**[CLEAN] Future scope deferred to #149 is explicitly named**
- Principle: A consumer reading a versioned release entry must be able to tell what is
  absent by design versus accidentally omitted.
- Evidence: The "Not in scope (deferred to issue #149)" block explicitly names PATCH
  (`Method` gaining `#[non_exhaustive]`), per-request timeout, and the lean-footprint
  audit. Each item is cross-referenced to issue #149.
- Resolution: N/A — sound.

**[CLEAN] Behavioral contract on `RequestBuilder::send` documented**
- Principle: Error-on-non-2xx vs caller-inspects is the most consequential behavioral
  contract on an HTTP client and must be stated explicitly.
- Evidence: The inline doc on `send` reads "non-2xx responses are NOT an error (caller
  inspects)" and the doc on `send_json` reads "non-2xx → `Err(Error::Status)`". The
  asymmetry between the two methods is correctly and explicitly recorded.
- Resolution: N/A — sound.

**[CLEAN] Accumulation semantics on `RequestBuilder::query` and `header` documented**
- Principle: Fluent builder methods that accumulate (rather than overwrite) on repeated
  calls must say so explicitly; a consumer who calls `.header("X-Req-Id", "a").header
  ("X-Req-Id", "b")` needs to know whether that sets one header or two.
- Evidence: `query` says "accumulates across calls"; `header` says "same-named headers
  accumulate; Fetch API combines them". Both are recorded.
- Resolution: N/A — sound.

**[CLEAN] `Method::Display` implementation documented**
- Principle: `impl Display for Method` is part of the public surface (consumers format
  method names for logging, tracing, and display).
- Evidence: The `Method` block ends with `impl std::fmt::Display for Method { /* delegates
  to as_str() */ }`, confirming the relationship and the delegation.
- Resolution: N/A — sound.

---

**[SHOULD_FIX] `Error` omits `Display` and `std::error::Error` trait implementations**
- Principle: A Rust error type's `impl Display` and `impl std::error::Error` are part of
  its public contract (FrameworkDesign_Documentation_As_Contract: each API documents its
  full behavioral contract, including invariants; BestPractices_Documentation: API
  documentation covers all interfaces). Without `std::error::Error`, `Error` cannot be
  wrapped in `Box<dyn std::error::Error>` or `anyhow::Error`, making it incompatible with
  the most common error-propagation patterns in Rust.
- Evidence: The `Error` block documents six variants, three helper methods (`is_network`,
  `is_status`, `status`), and the `#[non_exhaustive]` attribute. No `impl Display` or `impl
  std::error::Error` block appears. `impl Display for Method` is documented in the same
  CHANGELOG, so the omission on `Error` is not a formatting choice — it is a gap.
- Resolution: Add an `impl Display for Error` and `impl std::error::Error for Error` block
  to the `Error` section, following the same style as `impl Display for Method`. If the
  current implementation does not provide these, that is a correctness question for
  `SUBTASK_correctness` (out of scope here); this spoke only requires that whatever the
  implementation provides be documented.

---

**[ADVISORY] `Response::body()` and `Response::text()` — no behavioral differentiation**
- Principle: Two methods on the same type that appear to return the same information must
  explain their semantic difference; a consumer choosing between them needs that in the
  CHANGELOG (CodeReview_Checklist: documentation covers non-obvious behavior).
- Evidence: `body(&self) -> &str` borrows from the `Response`; `text(self) -> String`
  consumes it and returns an owned string. The ownership difference is evident from the
  signatures for a Rust reader, but the semantic question — are they the same string? is
  either transformed? — is not answered. Neither has an inline doc comment in the CHANGELOG,
  unlike `query` and `header` on `RequestBuilder`.
- Resolution: Add a one-line inline comment to each explaining the relationship: e.g.,
  `body()` returns a borrow of the raw body; `text()` consumes the response and returns
  ownership. If they are semantically equivalent (same string, different ownership), say so.

---

**[ADVISORY] `ClientBuilder::default_header` accumulation behavior not documented**
- Principle: Accumulating methods must document that they accumulate; the same standard
  applied to `RequestBuilder::header` should apply to `ClientBuilder::default_header`.
- Evidence: `ClientBuilder::default_header` has no inline doc comment in the CHANGELOG.
  `RequestBuilder::header` has "same-named headers accumulate; Fetch API combines them".
  If a consumer calls `default_header` twice with the same name, they cannot tell from the
  CHANGELOG whether the second call overwrites or accumulates the first.
- Resolution: Add an inline doc to `ClientBuilder::default_header` analogous to the one
  on `RequestBuilder::header`.

---

**[ADVISORY] No cross-reference to containing epic #132**
- Principle: A consumer reading a CHANGELOG to understand the crate's planned public
  surface benefits from a pointer to the roadmap item that governs the freeze decision.
  CodeReview_Checklist documentation review: changelog updated for applicable changes.
- Evidence: The `usable_early` section references issue #148 and issue #149, but not
  issue #132 (the EPIC that owns both). A reader knows the deferred items go to #149 but
  has no path to the full work-item tree (#132 → #148, #149) without searching.
- Resolution: Add a one-line reference in the `Unreleased` header or at the top of the
  section, e.g., "Part of EPIC #132." This does not alter the documented API surface; it
  adds traceability.
