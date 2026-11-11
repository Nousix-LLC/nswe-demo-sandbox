# Abuse and privacy basics

chirp is a public space where strangers post at each other. That is its appeal and its risk: the
same open write surface that lets anyone reply to anyone also lets anyone harass, flood, or dox
anyone. A product that invites that interaction without giving people a way to report it, rules to
report it against, a way to stop an account that is bothering them, and a limit on how fast one
actor can act, is not finished — it has shipped the interaction and withheld the safety that makes
the interaction survivable. This section specifies that floor as requirements, together with the
privacy and data-rights surface a product that holds people's contact details, credentials, and
posts is expected to have.

The scope here is deliberately the minimum a releasable public microblog needs, not a full trust-
and-safety platform. Two concerns interlock through this section. **Abuse resistance** is what lets a
person who is being targeted act: report the content, point at the rule it breaks, block or mute the
account, and rely on the service not being trivially floodable. **Privacy and data rights** is what
the product owes every account whether or not it is ever abused: collect only what the account
needs, never leak a person's private fields to other users, erase their data when they leave, and
let them see, take, and remove their own data. The two meet at a single seam — what a report or a
public view is allowed to expose about an account is bounded by the private-field rule below.

These are requirements, not mechanisms. How a limiter is implemented, how reports are queued, how
erasure is executed against a datastore, and what retention windows are configured are the concern
of later code work and of the operational-readiness area; this section says only what must be true
from the user's, operator's, and attacker's side.

Three handoffs to sibling areas are called out here and recorded in the notes for the synthesis so
they are reconciled rather than duplicated:

- **The public/private field boundary** — *who is authorized to read which field* — is the
  authorization area's. This section owns the *data-protection guarantee*: that a person's contact,
  credential, and session data never reach another user, a public response, or the report surface.
  The two must agree on which fields are private; they are coordinated in prose, not re-specified.
- **Acting on a report** — the operator/support surface that reviews reports and actions an account
  — is the authorization area's (it carries the supported-operator requirement). This section
  requires only that a report is captured and routed to that surface.
- **The deletion outcome** for content and handle is the accounts-and-lifecycle area's, and
  **session invalidation** is the authentication-and-sessions area's. This section requires that a
  deletion erases the private data it is responsible for and leaves no usable session behind,
  consistent with that stated outcome.

Rate and volume limits are stated here as an identity-and-trust requirement because they are a first
line against abuse, but their enforcement, quota values, and operational tuning belong to the
operational-readiness area's limits-and-quotas surface. The requirement below traces to the product
limit requirement and names that area; it does not define the enforcement.

## Requirements (REQ-ID-*)

### REQ-ID-080 — Report a chirp or an account
- **statement**: A signed-in person can report a chirp or an account that breaks the rules, and is
  shown that the report was received.
- **acceptance_criteria**: Signed in, submit a report against a chirp and, separately, against an
  account; each submission returns an acknowledgement that the report was received. The report
  lets the reporter indicate which rule it concerns (see REQ-ID-081).
- **release_gating**: true
- **verification_method**: manual_user_check
- **traces_to**: REQ-PROD-025

### REQ-ID-081 — Stated rules a report can reference
- **statement**: The product states, in a place reachable from within the product, the rules that
  say what is and is not allowed, and a report can reference them.
- **acceptance_criteria**: From within the product, reach the rules/terms without an external link;
  the report flow (REQ-ID-080) lets the reporter point at a rule the content or account breaks.
- **release_gating**: true
- **verification_method**: manual_user_check
- **traces_to**: REQ-PROD-026

### REQ-ID-082 — A report is captured and routed for action
- **statement**: A filed report is recorded and made available to the authorized operator/support
  surface, so it can be acted on; it is not merely acknowledged to the reporter and discarded.
- **acceptance_criteria**: Submit a report; afterward, through the supported operator/support
  surface (owned by the authorization area), the report is present with enough context to act on
  it — what was reported, by whom, against whom, and which rule. The acting itself (remove content,
  action the account) is the authorization area's requirement, not this one.
- **release_gating**: true
- **verification_method**: operational_check
- **traces_to**: REQ-PROD-025

### REQ-ID-083 — Block an account
- **statement**: A person can block another account, after which that account can no longer interact
  with them (reply to, follow, or otherwise reach them) per the block's stated effect.
- **acceptance_criteria**: Signed in, block another account; afterward that account's attempts to
  interact with you are refused or hidden per the stated effect of a block, and the product states
  what a block does.
- **release_gating**: false — block and mute (REQ-ID-083, REQ-ID-084) are expected unwanted-
  interaction controls, but the product requirement that defines them lets a first release ship with
  reporting (REQ-ID-080) and operator action (authorization area) as the gated safety floor and add
  block/mute as a fast follow. The release bar decides which of block/mute v1 must include; at least
  the reporting floor above is gated.
- **verification_method**: manual_user_check
- **traces_to**: REQ-PROD-027

### REQ-ID-084 — Mute an account
- **statement**: A person can mute another account, after which that account's content no longer
  appears to them, without the muted account being told.
- **acceptance_criteria**: Signed in, mute another account; afterward that account's chirps and
  replies are suppressed from your views per the stated effect of a mute, and the product states
  what a mute does and that it is not disclosed to the muted account.
- **release_gating**: false — see the reason on REQ-ID-083; the bar decides whether v1 includes mute.
- **verification_method**: manual_user_check
- **traces_to**: REQ-PROD-027

### REQ-ID-085 — Rate and volume limits as a first line against abuse
- **statement**: The product applies basic rate and volume limits to writes and requests so one
  account or client cannot trivially flood other users or overwhelm the service. Stated here as an
  identity-and-trust requirement; the enforcement, quota values, and tuning are the operational-
  readiness area's limits-and-quotas surface (REQ-OPS-*), not defined here.
- **acceptance_criteria**: Exceed a reasonable posting or request rate from one account; the product
  throttles or rejects the excess rather than serving it without limit, and a legitimate user at a
  normal rate is not blocked. The specific thresholds are the operational-readiness area's to set.
- **release_gating**: true
- **verification_method**: operational_check
- **traces_to**: REQ-PROD-041

### REQ-ID-086 — Data minimization
- **statement**: The product collects only the data an account needs to function — a handle, a
  display name, an optional bio, the authentication credential, and a point of contact for recovery
  and notifications — and does not require data beyond that to use the core product.
- **acceptance_criteria**: Inspect what sign-up and the account surfaces collect and store; every
  collected field maps to a stated account function (identity, authentication, recovery/contact,
  profile). No field is collected that no function needs.
- **release_gating**: true
- **verification_method**: inspection
- **traces_to**: REQ-PROD-024

### REQ-ID-087 — Private-field protection
- **statement**: A person's private data — their point of contact, their authentication credential,
  and their session data — is never exposed to another user, never returned in a public or
  unauthenticated response, and never surfaced through the report or block/mute flows. Only the
  intended public fields (handle, display name, bio, public chirps, public counts) are visible to
  others.
- **acceptance_criteria**: As another user and as an unauthenticated visitor, view a person's
  profile, their public chirps, and any public responses; only the public fields appear. File a
  report against an account (REQ-ID-080); the report flow does not reveal the reported or reporting
  account's contact, credential, or session data. A person's credential is never returned to anyone,
  including the owner, in readable form.
- **release_gating**: true
- **verification_method**: manual_user_check
- **traces_to**: REQ-PROD-024

### REQ-ID-088 — Erasure on account deletion
- **statement**: When a person deletes their account, their private data — contact, credential, and
  session data — is erased, and every session for the account is invalidated, consistent with the
  product's stated deletion outcome for content and handle.
- **acceptance_criteria**: Delete an account; afterward the account cannot sign in, no session for
  it remains usable, and its contact and credential data are no longer held. What happens to the
  account's public chirps and to its handle follows the stated deletion outcome (the accounts-and-
  lifecycle area's requirement); this requirement covers the erasure of the private data and the
  invalidation of sessions.
- **release_gating**: true
- **verification_method**: operational_check
- **traces_to**: REQ-PROD-021, REQ-PROD-024

### REQ-ID-089 — A stated retention posture
- **statement**: The product states how long it keeps account data, reports, and operational records
  that contain personal data, and keeps them no longer than that stated posture, so data is not
  retained indefinitely by default.
- **acceptance_criteria**: Find the product's stated retention posture for account data, reports,
  and personal-data-bearing records; the product's behavior is consistent with it (records past the
  stated window are not retained). Reports are kept long enough to act on and to establish a pattern,
  then handled per the stated posture.
- **release_gating**: false — a stated retention posture is expected, but a first release may ship
  with a simple, stated posture and refine the windows later; the release bar decides the minimum.
  The operational-readiness area owns how records are aged out in practice.
- **verification_method**: inspection
- **traces_to**: REQ-PROD-024

### REQ-ID-090 — A data-rights baseline
- **statement**: A person has a baseline set of rights over their own data, proportionate to a public
  microblog: to access and obtain a portable copy of it, and to have it erased. This baseline is
  satisfied by the account's own surfaces, not by a manual request process.
- **acceptance_criteria**: Signed in, obtain a portable copy of your own data (posts, profile,
  follows) through the product (the export mechanics are the accounts-and-lifecycle area's
  requirement), and erase your own data by deleting your account (REQ-ID-088 and the deletion
  outcome). No step requires contacting an operator by hand. The product states this baseline so a
  person can find it.
- **release_gating**: true
- **verification_method**: manual_user_check
- **traces_to**: REQ-PROD-019, REQ-PROD-024

## Notes for synthesis

**Cross-area seams (coordinate, do not duplicate):**

- **Public/private field boundary ↔ authorization (REQ-ID-060..079).** The authorization area owns
  *who is authorized to read/change which field*. This area owns the *data-protection guarantee* that
  contact, credential, and session data never reach another user, a public response, or the report
  surface (REQ-ID-087). Both must name the same set of private fields (contact, credential, session)
  and the same public set (handle, display name, bio, public chirps, public counts). If the two lists
  diverge, the stricter one wins; the synthesis should confirm they agree.
- **Acting on reports ↔ authorization (REQ-PROD-028).** REQ-ID-082 requires a report be *captured and
  routed* to the operator/support surface. The surface itself and the authority to act (remove
  content, action an account, assist recovery) are the authorization area's requirement. No operator-
  action requirement is minted here, and no REQ-OPS id is minted here.
- **Deletion outcome ↔ accounts-and-lifecycle (REQ-ID-001..029).** That area owns the stated outcome
  for a deleted account's chirps and handle (REQ-PROD-020/021). REQ-ID-088 covers only erasure of the
  private data and invalidation of sessions, consistent with that outcome. **Session invalidation
  mechanics ↔ authentication-and-sessions (REQ-ID-030..059)** — REQ-ID-088 depends on that area's
  server-side invalidation requirement; it states the privacy outcome, not the session mechanism.
- **Export ↔ accounts-and-lifecycle.** REQ-ID-090's access/export half is satisfied by that area's
  data-export requirement (REQ-PROD-019); this area states the right exists and is self-service, and
  does not redefine the export mechanics.
- **Rate/volume limits ↔ operational-readiness (REQ-OPS limits-and-quotas).** REQ-ID-085 states the
  requirement and traces to REQ-PROD-041; the enforcement, thresholds, and quota tuning are that
  area's. No REQ-OPS id is minted here; the synthesis should record REQ-PROD-041's enforcement as
  carried by the operational-readiness area so the coverage check does not read it as a hole.

**Threats each requirement answers (for the threat model):**

- **Harassment / unwanted interaction** (a content-abuse threat specific to a public social surface):
  REQ-ID-080 (report), REQ-ID-081 (rules to report against), REQ-ID-082 (report reaches an actor who
  can act), REQ-ID-083 (block), REQ-ID-084 (mute).
- **Denial of service / flooding**: REQ-ID-085 (rate and volume limits) is the first line; the
  operational-readiness area carries the enforcement depth.
- **Information disclosure** (the privacy threat): REQ-ID-087 (private fields never leak to other
  users, public responses, or the report surface) is the primary mitigation; REQ-ID-086 (minimize
  what is collected) and REQ-ID-089 (don't retain it longer than stated) reduce the blast radius;
  REQ-ID-088 (erase on deletion) closes residual-data disclosure after a person leaves.
- **Repudiation** (partial): REQ-ID-082 (a report is recorded with who/what/which-rule) gives the
  operator a record to act on and establishes a pattern across reports.
- **Trust / data rights** (not a STRIDE letter but a releasability property): REQ-ID-090 (access,
  export, erasure) is what lets a person leave with their data and remove it, which the product-
  requirements leaving journey (J8) treats as part of trusting the product in the first place.

**Residual notes for the threat-model author:**

- A classic STRIDE spoofing/tampering/elevation walk is owned by the authentication, authorization,
  and accounts areas; this area contributes the information-disclosure, denial-of-service (abuse
  flooding), and content-abuse mitigations above. A cross-cutting transport-confidentiality
  requirement (protecting private fields in transit) is a candidate for the synthesis to mint in its
  own range (REQ-ID-100..119) if no sibling area has stated it — REQ-ID-087 assumes private fields
  are protected end to end but does not itself own the transport requirement.
- Block/mute (REQ-ID-083/084) are ungated here by the product requirement's own decision; if the
  release bar elects to gate one of them, the threat model should note harassment mitigation then
  rests on more than reporting alone.
