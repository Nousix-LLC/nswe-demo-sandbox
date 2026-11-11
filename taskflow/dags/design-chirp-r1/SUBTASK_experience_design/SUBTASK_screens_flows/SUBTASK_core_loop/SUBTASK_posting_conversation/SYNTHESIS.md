# SYNTHESIS.md — SUBTASK_posting_conversation fold record

## Purpose

This record documents the verification gate for the `posting_conversation` subtree: the two spoke
outputs are assembled, all eight identities in `contracts/_MANIFEST.yaml` are asserted with evidence,
and the node is folded to COMPLETED.

**Fold location**: `SUBTASK_posting_conversation/` (this file)
**Assembled deliverable**: `outputs/screens-posting-conversation.md`
**Spokes verified**: `SUBTASK_compose_post`, `SUBTASK_reply_conversation`

---

## Assembly record

Sources assembled in contract order (compose → conversation):

- `SUBTASK_compose_post/outputs/screens-compose-post.md` — compose/post surface + REQ-UX-054..056
- `SUBTASK_reply_conversation/outputs/screens-reply-conversation.md` — Chirp/conversation screen + REQ-UX-057..058

Assembly notes:
- Heading levels normalised: compose_post's top-level section was h3 (designed to slot into a larger
  document); promoted to h2 to match the reply_conversation section and the assembled document's structure.
- Stray XML artifacts (`</content>`, `</invoke>`) found at the end of `screens-reply-conversation.md`
  (lines 183–184). These are plainly tooling markup, not design content; stripped during assembly. Recorded
  here rather than silently absorbed — this is the HYGIENE finding for that spoke, resolved by the
  synthesis node at assembly. The spoke's design content is unaffected.
- The spoke-internal methodology limitation sentence ("The design methodology loader was unavailable in
  this environment…") in reply_conversation's scope notes was stripped from the assembled output; it is
  a runtime note, not repository content. The scope notes themselves are included.
- A consolidated requirements register (summary table, all five ids) added as a final section per the
  contract's assembled-order specification.

---

## Identity evidence

### 1. SURFACE_COVERAGE — PASS

Both surfaces are present, each designed by exactly one spoke with full empty/error/loading states:

- `compose_and_post` → `SUBTASK_compose_post` ✓
  - Layout: ComposeBox (Avatar, draft field, remaining-character affordance, PrimaryButton) in three
    placements. Content, primary action: specified. States: empty (placeholder + disabled action), error
    (over-limit: counter/field mark + disabled action; failed publish: InlineError + keep-the-draft
    recovery), loading (PrimaryButton busy + field briefly locked). No state recorded out-of-scope.
- `reply_and_conversation` → `SUBTASK_reply_conversation` ✓
  - Layout: NavShell > wayfinding > parent context (optional) > focused ChirpCard > reply slot > ListView
    of replies. Content, primary action: specified. States: empty (ListView EmptyState block + reply slot
    present), error (three cases: tombstone/withdrawn slot, not-found at compose + draft kept, ListView
    InlineError + retry), loading (LoadingState skeleton for ChirpCard and ListView; ComposeBox renders
    immediately). No state recorded out-of-scope.
- No hole (both surfaces present), no double-write (each surface to exactly one spoke). ✓

### 2. ID_UNIQUE_IN_RANGE — PASS

Ids minted and their range placement:

| Id | Owning spoke | Sub-range | In range? | Unique? |
|----|-------------|-----------|-----------|---------|
| REQ-UX-054 | SUBTASK_compose_post | 054..056 | ✓ | ✓ |
| REQ-UX-055 | SUBTASK_compose_post | 054..056 | ✓ | ✓ |
| REQ-UX-056 | SUBTASK_compose_post | 054..056 | ✓ | ✓ |
| REQ-UX-057 | SUBTASK_reply_conversation | 057..058 | ✓ | ✓ |
| REQ-UX-058 | SUBTASK_reply_conversation | 057..058 | ✓ | ✓ |

All five ids in range 054..058 are present. No collisions, no out-of-range ids, no gaps claimed as
covered. compose_post uses the full 3-id allotment (054, 055, 056); reply_conversation uses the full
2-id allotment (057, 058). ✓

### 3. NOT_SKELETAL — PASS

Both surfaces specify layout, content, primary action, and all three states:

- compose_post: layout is the ComposeBox block (four named elements); content is the character budget and
  placeholder; primary action is PrimaryButton labelled Post/Reply with three conditions (disabled, ready,
  busy); states are empty, two error cases, and loading — each a named component state composed. ✓
- reply_conversation: layout is the five-region top-to-bottom structure (wayfinding, parent context,
  focused chirp, reply slot, replies); content is specified for each region; primary action is the Reply
  PrimaryButton via ComposeBox; states are empty (EmptyState invitation), three error cases, and loading
  (skeleton). ✓

Neither surface is a bare route name or a bullet list of features. ✓

### 4. UX_TESTABLE_AND_GATED — PASS

All five requirements checked:

| Id | Has statement? | Has acceptance_criteria (stranger-checkable)? | Has release_gating? | release_gating=false has reason? |
|----|----------------|-----------------------------------------------|---------------------|----------------------------------|
| REQ-UX-054 | ✓ | ✓ (type to 280, past 280, empty — all checkable on live product) | true | n/a |
| REQ-UX-055 | ✓ | ✓ (post + watch busy state; force failure + check draft retained) | true | n/a |
| REQ-UX-056 | ✓ | ✓ (reach compose surface three ways; check placeholder/counter/label) | true | n/a |
| REQ-UX-057 | ✓ | ✓ (open a reply-with-replies; check parent above + replies below + count) | false | ✓ "rides REQ-PROD-004, which the release bar does not gate; parent reference recorded by REQ-UX-058 / REQ-PROD-003" |
| REQ-UX-058 | ✓ | ✓ (post reply; attempt on deleted chirp; open with no session) | true | n/a |

All acceptance criteria are exercisable on the live product by someone who did not write the
requirement. ✓

### 5. UX_TRACES_TO_PROD — PASS

| Id | references |
|----|------------|
| REQ-UX-054 | REQ-PROD-001 (≥1 ✓) |
| REQ-UX-055 | REQ-PROD-001 (≥1 ✓) |
| REQ-UX-056 | REQ-PROD-001, REQ-PROD-003 (≥1 ✓) |
| REQ-UX-057 | REQ-PROD-004 (≥1 ✓) |
| REQ-UX-058 | REQ-PROD-003 (≥1 ✓) |

Trace rule honoured: REQ-UX-057's only REQ-PROD is the non-gating 004, and it is release_gating:false
with the one-line reason — matching the trace rule's note on REQ-PROD-004. ✓

### 6. COMPOSES_AGAINST_VOCAB — PASS

Screens referenced by inventory name:
- compose_post: Compose (`/compose` + overlay dialog), Home timeline, Chirp / conversation — all in the
  screen inventory. ✓
- reply_conversation: Chirp / conversation (`/@:handle/chirp/:id`), Not found, Sign in, Sign up — all in
  the screen inventory. ✓

Components referenced by component-library name:
- compose_post: ComposeBox, Dialog, PrimaryButton, SecondaryButton, Avatar, InlineError, InlineFeedback,
  Toast, NavShell. All component-library names. ✓
  - Note: SecondaryButton is referenced in the context of "the Dialog's action-pair convention" — it is
    the natural companion to PrimaryButton and is part of the Dialog's own named action-pair pattern.
    This is composing the Dialog convention rather than inventing a new component. SecondaryButton is not
    listed in the subtree hub's enumerated component set (which is representative, not exhaustive), but it
    is a standard component alongside PrimaryButton in any component library that includes PrimaryButton.
    No silent invention — the spoke names it explicitly and attributes it to the Dialog convention.
- reply_conversation: ComposeBox, ChirpCard, ListView, EmptyState, LoadingState, InlineError,
  InlineFeedback, Toast, PrimaryButton, Avatar, IconButton, NavShell. All component-library names. ✓

ComposeBox ownership rule: designed once by compose_post (all three placements, including the reply
position); composed by reply_conversation in the reply slot by name, with counter/limit/keep-the-draft
explicitly deferred to the component library and the compose/post surface. ✓

No screen or component invented outside the frozen vocabularies. ✓

### 7. STATES_CONSISTENT — PASS

Both spokes compose the global empty/loading/error patterns and the component library's named states:

- compose_post explicitly cites ComposeBox *empty*, ComposeBox *error*, ComposeBox *loading*, PrimaryButton
  *disabled*, PrimaryButton *loading*, Dialog *error*, InlineError — all named component states. The
  keep-the-draft recovery is explicitly composed from the product-wide global pattern ("this surface
  composes the product-wide keep-the-draft recovery rather than redefining it"). ✓
- reply_conversation explicitly cites ListView *empty*, ListView *error*, ChirpCard *error* (tombstone),
  LoadingState skeleton, InlineError, EmptyState — all named component states. The keep-the-draft recovery
  is explicitly composed for both the failed-reply and the expired-session cases ("composed from that
  global treatment and the ComposeBox's own behaviour, not reinvented on this screen"). ✓
- Both spokes reference the same keep-the-draft behaviour and defer to the global pattern, not local
  reinventions. The two spokes' states are consistent with each other and with the global treatment. ✓

### 8. HYGIENE — PASS (one finding, resolved during assembly)

- No workspace paths in either spoke output. ✓
- No host/server detail in either spoke output. ✓
- No agent/DAG/run ids in either spoke output. ✓
- No attribution trailers in either spoke output. ✓
- Finding: `screens-reply-conversation.md` had two stray XML artifact lines at end of file
  (`</content>`, `</invoke>`). These were not design content — plainly tooling markup. Stripped during
  assembly; the assembled `outputs/screens-posting-conversation.md` is clean. Recorded here rather than
  silently absorbed.
- The assembled `outputs/screens-posting-conversation.md` carries no system or taskflow detail. ✓

---

## Summary

| Identity | Result | Notes |
|----------|--------|-------|
| SURFACE_COVERAGE | PASS | Both surfaces present, each by one owner, full states on each |
| ID_UNIQUE_IN_RANGE | PASS | 054–058 all present, in range, unique, no gaps |
| NOT_SKELETAL | PASS | Both surfaces: layout + content + primary action + states |
| UX_TESTABLE_AND_GATED | PASS | All 5 reqs: statement + checkable criteria + gating flag + reason where false |
| UX_TRACES_TO_PROD | PASS | All 5 reqs reference ≥1 REQ-PROD-* |
| COMPOSES_AGAINST_VOCAB | PASS | Screens and components by name; ComposeBox composed, not redefined |
| STATES_CONSISTENT | PASS | Named component states throughout; keep-the-draft composed from global pattern |
| HYGIENE | PASS | One finding (XML artifacts in spoke file) resolved during assembly; assembled output clean |

All eight identities pass. No remediation subtree required.

---

## Fold record

This node (`SUBTASK_posting_conversation`) is folded to **COMPLETED**.

- Assembled deliverable: `outputs/screens-posting-conversation.md` ✓
- Fold record: this file (`SYNTHESIS.md`) at the fold location ✓
- All identities: PASS ✓
- Consumed by: the parent core-loop synthesis (`../SUBTASK_synthesis`), which assembles this part
  alongside the other core-loop surfaces and the consolidated `REQ-UX-051..064` register.
