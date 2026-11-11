## What this is

This updates **`design/`** — chirp's product design and release bar — to the current reviewed set. It
describes what the product must be to be a *releasable* Twitter-style product, and the concrete, testable
**release bar** that defines "releasable", grounded in the product as it stands at `c805525`.

It is **design, not code.** It describes what the product must do, for whom, and why, and what "done"
looks like from the user's and operator's side. Every topic with an engineering "how" — durable
persistence, authentication, sessions, rate limiting, backups — is stated as a **requirement with a
testable bar**, with the implementation deferred to later code work. No product code is changed here.

## Why

chirp runs, but "it runs" is not "it's releasable". Sign-in is handle-only (anyone can act as anyone),
data lives in an in-memory store that is lost on restart, and the surfaces a public, account-holding
product owes its users — recovery, deletion, data export, abuse handling, backups, observability — need to
be designed, not assumed. This design names the whole releasable product and sets a bar a later review,
code change, or PR can hold the product to, criterion by criterion. This revision deepens and reconciles
that design across all six areas and the consolidated bar.

## What's in it

Start with [`design/README.md`](design/README.md) — it indexes the set and explains how the bar and the
delivery backlog relate.

- **`product-requirements.md`** — what chirp is, the users and personas, their end-to-end journeys, and
  the product requirements and acceptance criteria (`REQ-PROD-*`). Every other area traces back here.
- **`domain-application-design.md`** — the domain model, module responsibilities, and the
  **durable-persistence requirement** (the in-memory store is a release blocker), as requirements and
  structure (`REQ-DOM-*`).
- **`experience-design.md`** — every screen and flow with its empty / error / loading / not-found /
  session-expired / validation states, the visual design system, responsive layout, and accessibility
  (WCAG 2.1 AA) (`REQ-UX-*`).
- **`identity-security.md`** — accounts and their full lifecycle (sign-up/in/recovery, deletion, data
  export), credentialed authentication and safe sessions, authorization, abuse/privacy basics, and the
  threat model (`REQ-ID-*`).
- **`operational-readiness.md`** — durable data, backups and a proven recovery path, limits, observability,
  and incident response (`REQ-OPS-*`).
- **`release-bar.md`** — the MVP-vs-releasable scoping, the testable **`BAR-*`** criteria (each with a
  verification method and the `REQ-*` it enforces, at a `usable_early` or `releasable` stage), and a
  completeness & gap review recording an in/out-of-scope judgment for every expected surface.

## How to review

The design is self-contained; no code or deployment changes are required to merge it. Read `README.md`,
then `release-bar.md` for the bar itself. Requirements and bar criteria carry stable ids so the follow-on
delivery backlog (epics + issues on the project board) can trace to them.

## Traceability

This design informs the existing epic trackers and folds the open hardening follow-ups into the
operational-readiness design where they belong (it does not complete them — they remain code work):

Refs #1
Refs #2
Refs #3
Refs #23
Refs #24
Refs #25
