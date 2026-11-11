<!--
Section source for: product_definition_and_kind (of design/product-requirements.md).
Owner: SUBTASK_product_definition. Composes against the read-only subtree and parent contracts.
Expresses needs in prose and informal `need:` handles only — it mints no REQ-PROD-* ids
(SUBTASK_requirements is the sole minter). Grounded in Nousix-LLC/nswe-demo @ c805525.
-->

# Product definition & kind

## What chirp is

**chirp is a Twitter-style microblogging web application: a place where a person posts
short public messages and reads a running timeline of messages from the people they
follow.** It is a product someone uses in a browser, not a library or a toolkit. The
framework it is built on (`ferric`) is the engagement's other deliverable; chirp is the
product that proves the framework, and this document is about chirp as a thing a stranger
would use.

From the user's side, chirp is the following loop:

- **Get in.** You arrive at the site, identify yourself, and you are in — your handle is
  how everyone else knows you.
- **Post.** You write a short message (a *chirp*, up to 280 characters) and publish it.
  You can post a reply to someone else's chirp.
- **Read.** You read a timeline of chirps, newest first, a page at a time.
- **Follow.** You follow and unfollow other people; who you follow shapes what you read.
- **React.** You like and unlike chirps, and you can open any person's profile to see who
  they are and act on them (follow, view their chirps).

That is the whole product in one sentence a user would recognize: *post short messages,
read a timeline, follow people, like what you like.* Everything else in this design exists
to make that loop something a stranger could actually sign up for, trust with their
account, and rely on.

### How it is shaped (grounded in the repository at `c805525`)

Described by repository identity, not by implementation how:

- A **single-page web application** (`crates/chirp-frontend`), delivered to the browser as
  WebAssembly, built on the in-house `ferric` UI framework and its router. The app presents
  three screens today — a timeline view (`/`), a compose-and-sign-in view (`/compose`), and
  a user-profile view (`/user/:id`) — above a persistent navigation bar.
- A **REST backend** (`crates/chirp-server`, an axum service) that the SPA calls over a
  typed contract shared by both sides (`crates/chirp-types`). The live surface at `c805525`
  is: register a user, fetch a user, open a session, post a chirp, read a timeline
  (cursor-paginated), follow/unfollow a user, like/unlike a chirp, and an unauthenticated
  liveness probe.
- It **ships as one self-contained container** that serves both the API and the SPA, and is
  operated as a hosted service — deployed to a Kubernetes cluster via GitOps (`deploy/`) and
  reachable on the web. There is no separate product the user installs.

### The state of the product at `c805525` (where the design must take it from)

These are observations about the product as it exists, not a design for how to fix them —
the fixes belong to the requirements, the identity/security design, and the
operational-readiness design. The gap between this state and a releasable product is what
the rest of the requirements close.

- **Identity is handle-only.** Signing in means typing a handle; the server opens a session
  for that handle and returns a token. There is no password, no credential, and no
  verification — nothing stops one person from claiming another's handle. For a product
  whose entire premise is *this person said this*, that is the central gap, not a detail.
- **Nothing is remembered across a restart.** All users, chirps, follows, and likes live in
  the server's memory; when the process restarts, the product is empty again. A microblog
  that forgets everything it was told is not yet a product a stranger can rely on.
- **The account-lifecycle and supporting surfaces are absent.** There is no sign-up distinct
  from "type a handle," no password/recovery, no account settings, no way to delete an
  account or take data out, no onboarding, no notifications, no search, no media, no
  direct messages, no blocking or muting, no moderation, and no help/admin surface.

The core loop is real and implemented; what is missing is almost everything that stands
*around* the loop and makes it releasable. Naming that is this definition's job.

---

## Product kind(s)

A product's kind sets the things its users assume without being told. chirp is **one kind**,
and three other candidate kinds do **not** apply — each recorded with its reason, because a
kind that does not apply still shapes what is correctly out of scope.

### chirp is a consumer web application (the applicable kind)

chirp is a **hosted, public, account-based consumer web application**: individual people
sign up directly, use it in a browser, and it is operated as a service by the people who
build it. This is the kind the engagement aim describes — a production-quality, publicly
reachable Twitter-style product (`TASK.md`) — and it is the kind every requirement in this
design is held to.

**What this kind makes its users assume without asking.** A person who signs up for a
hosted consumer web product takes all of the following for granted, and is surprised and
distrustful when any is missing:

- **They can get in, and get back in.** There is a real sign-up and sign-in, and if they
  forget how to get in they can recover access — their account is not lost the first time
  they clear a cookie or forget a detail. `need: real-account-signup-signin`,
  `need: account-recovery`.
- **Their identity is actually theirs.** The handle they claim cannot be silently taken or
  impersonated by anyone who types it; signing in proves it is them.
  `need: authenticated-identity`.
- **It remembers their stuff.** What they posted, who they follow, and what they liked are
  still there the next time they visit, and survive the service being restarted or updated.
  `need: durable-account-data`.
- **The account is theirs to manage and to end.** They can see and adjust their account,
  delete it when they want, and take their data with them. `need: account-settings`,
  `need: account-deletion`, `need: data-export`.
- **Only the right people can see and do the right things.** There is a clear boundary on
  who may act as them and who may change what; private details are not exposed to everyone.
  `need: authorization-boundary`, `need: privacy-basics`.
- **It behaves like a finished thing.** It tells them what is happening when a list is empty,
  something is loading, or something failed; it works on a phone; and it is reachable and
  reasonably available when they come back. `need: considered-states`,
  `need: works-on-mobile`, `need: reachable-and-available`.
- **Someone is minding it.** There is a way to get help and to report abuse, and bad actors
  can be dealt with — a public space with no way to report a problem does not feel safe.
  `need: help-and-abuse-reporting`.

These implications are the backbone of chirp's requirements. Each is surfaced above as a
prose need with an informal `need:` handle for `SUBTASK_requirements` to formalize into the
`REQ-PROD-*` register (or, where another design area owns the detail — identity/security,
experience, operational readiness — to carry as a product-level requirement that traces to
that area). Per the subtree contract (`KIND_IMPLICATIONS`), every implication named here is
either reflected in a requirement or recorded out-of-scope with a reason; the scope draft
below records the out-of-scope judgments.

### Kinds that do NOT apply (recorded with reasons)

- **Multi-tenant SaaS — does not apply.** A SaaS product is sold to organizations, with
  per-tenant isolation, team/seat management, an admin who governs other users, and billing.
  chirp has no notion of a tenant or an organization: it is one shared public social space of
  individual accounts, and no money changes hands. The team-management, tenancy, and billing
  surfaces a SaaS buyer would assume are therefore **out of scope** for chirp — recorded here
  so their absence is a decision, not an oversight. `need: no-tenancy-or-billing` (as an
  explicit non-goal).
- **Commercial off-the-shelf (COTS) — does not apply.** A COTS product is delivered to
  customers to install, license, upgrade, and run in *their* environment. chirp is operated
  as a hosted service by its maker and is not distributed to customers to install or license.
  Customer-side install/licensing/upgrade tooling is therefore **out of scope**. (The
  product does ship as a container and is self-hostable in principle — see the OSS note — but
  it is not *productized for customers to install*, which is what the COTS kind would demand.)
- **Open-source project — does not apply as a product kind.** An OSS product wins users who
  will never pay or file a ticket: it assumes they can self-host it, read how it works, and
  contribute. chirp's repository README declares it a **closed demonstration that does not
  accept contributions**, with issues and pull requests limited to the repository's
  collaborators. So chirp is not an OSS *product* soliciting self-hosting users or
  contributors, and the community surfaces an OSS kind implies (contribution guide, public
  issue intake, a self-host support promise) are **out of scope**.

  One nuance, so it is not mistaken for an OSS obligation: the repository is
  public and source-available, and the app is self-hostable from the single container it
  ships as. A reader *can* run their own copy. That property is a consequence of how the
  demonstration is published, not a product kind — it does not add the assumptions an OSS
  product carries, and it does not reduce the release bar below.

### One thing the kind does NOT reduce

The repository's "closed demonstration" framing governs *contribution and distribution* — it
is why the OSS community surfaces are out of scope. It does **not** lower the product bar:
the engagement aim is a production-quality product, and absent an explicit reduction, chirp
is held to the bar of a releasable consumer web application (`need: releasable-bar-not-prototype`).
A reader should not read "demonstration" as "prototype exemption."

---

## Product-kind-lens scope draft (for `SUBTASK_requirements` to consolidate)

This is an **initial** in/out-of-scope view implied by the consumer-web-app kind, offered
for `SUBTASK_requirements` to fold into the final `in_scope_out_of_scope` section. It is a
draft at the product-definition altitude: it names *what a releasable product of this kind is
expected to include and reasonably leave out*, and defers the detailed requirements to the
owning design areas. Out-of-scope items carry reasons, per the subtree contract
(`SCOPE_RECORDED`).

### In scope — what a releasable chirp of this kind must include

- **The core loop, intact:** post a chirp (incl. replies), read a paginated timeline, view
  profiles, follow/unfollow, like/unlike. This exists at `c805525` and is the product's
  reason to exist.
- **Real accounts and the full account lifecycle:** real sign-up and sign-in, account
  recovery, account settings, account deletion, and data export. (Detailed design owned by
  the identity/security area; carried here as product-level needs because the kind demands
  them.)
- **Authenticated identity and an authorization boundary:** signing in proves who you are,
  and there is a clear rule for who may see and change what. (Identity/security area owns the
  detail.)
- **Durable data:** the product's content and relationships survive restart and
  redeployment. The in-memory store at `c805525` is a **release blocker**, not a style
  choice. (Operational-readiness and domain-application-design areas own the detail.)
- **A finished-feeling experience:** considered empty/error/loading states, a responsive
  layout that works on a phone, and accessibility. (Experience-design area owns the detail.)
- **The supporting surfaces a consumer product is judged on:** first-run/onboarding so a new
  person knows what to do; a baseline notifications story; and a way to get help and report
  abuse. (Experience, identity/security, and operational-readiness areas share these.)
- **Operational readiness to be a live service:** reachable and reasonably available,
  backups and a recovery path for the durable data, basic observability, and
  limits/quotas as a first line against abuse. (Operational-readiness area owns the detail.)

### Out of scope — with reasons

- **Tenancy, organizations, team management, and billing** — chirp is a single public
  consumer product of individual accounts, not a SaaS sold to tenants, and no money changes
  hands. (SaaS kind does not apply.)
- **Customer-side install, licensing, and upgrade tooling** — chirp is operated as a hosted
  service, not distributed for customers to run in their own environment. (COTS kind does not
  apply.)
- **Open-source community infrastructure** (contribution guide, public issue/PR intake, a
  self-host support commitment) — the repository is a closed demonstration that does not
  accept contributions. (OSS kind does not apply.)
- **Native mobile applications** — chirp is a responsive web app; native iOS/Android clients
  are a separate product surface beyond the stated aim.
- **Rich social features beyond the core loop** — direct messages, full-text search, media
  and image uploads, trending/discovery, verified badges, and multi-level threaded
  conversations beyond simple replies. These are **candidates for later scope, not v1
  commitments**: a releasable chirp can ship without them, and the release-bar and
  requirements tasks should decide explicitly which (if any) a first release includes rather
  than treating their absence as a defect. Recorded here so the decision is deliberate.

### A note on altitude

This document deliberately states *product-level* needs (what the kind demands) and defers
every detailed requirement, acceptance criterion, and "how" to the owning design areas and to
`SUBTASK_requirements`, which mints the `REQ-PROD-*` register. The `need:` handles above are
the traceable seam from this definition to those requirements; they are not themselves
requirements, and they assign no identifiers.
