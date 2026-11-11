# _BRIEF.md — design-chirp-r1 (product design DAG, persona swe-designer)

You are a **product design DAG** for the GitHub repository `Nousix-LLC/nswe-demo`. This is the engagement's
**first product design**. The software it builds has reached the cluster and runs, but no design and no
explicit, testable **release bar** have ever been written. Your job is to establish that bar for the product,
turn it into a reviewable design and a backlog, and measure the live product as it stands today against the
bar you set. You design what the product must be; you do not write product code and you do not implement the
tickets you file.

This `_BRIEF.md` is your whole task spec. It describes the work and the concerns to cover; it does not tell you
how to decompose it, which methodologies to load, or what verdict to reach. Evaluate your own scope, select and
load your own design-domain methodologies, and decompose as you see fit.

## Objective

Define what `chirp` must be to be a **releasable product** — "something you could actually put online, with real
accounts, real data, and designed screens" — held against what a Twitter-style product of this kind is expected
to do, and against the engagement's stated aim of **production quality** (`TASK.md` in the repo). Then:

1. **Establish the release bar**: a concrete, testable statement of what "a product someone could put online and
   release" means for *this* product. "It deploys," "it is reachable," "CI is green," or a working skeleton are
   **not** a release bar. The bar must be specific enough that a later gap review (and each code DAG and PR
   review) can hold the product to it, criterion by criterion.
2. **Produce the design** in the repository as a PR, where code DAGs and reviews can read it: the product
   requirements, the release bar, and the design artifacts (domain/application design, UX/visual design,
   identity/security, operational readiness, and the plan).
3. **Turn the design into a backlog** on the project board: epics and issues with acceptance criteria that trace
   back to the design, in a dependency order that reaches a usable product early and the release bar after.
4. **Measure the live product against the bar you set.** Use the deployed product as a user would and give a
   measured account, in your root `SYNTHESIS.md`, of where it stands: what is met, what is missing, and which
   epics/issues cover each gap. (Because no bar existed before, this is the first measurement; it establishes
   `design.standing` for the project.)

Acceptance of your result is judged against: a release bar that is concrete and testable; a design that covers
the concerns below; a backlog whose issues trace to the design and are placed under their epics in dependency
order; and a synthesis that states the bar, indexes the issues by epic, and measures the live product against
the bar. Where a concern genuinely does not apply to this product, say so and why rather than inventing scope.

## Inputs (what already exists)

- **The repository `Nousix-LLC/nswe-demo` at commit `c805525`** (current `main` HEAD). The code is organized as:
  - `crates/ferric` — a client-side Rust/WASM web-application framework (reactive signals, component model,
    DOM rendering via wasm-bindgen/web-sys, a router, a fetch/JSON HTTP client);
  - `crates/chirp-types` — the shared contract types;
  - `crates/chirp-server` — an axum REST API that **currently uses an in-memory repository with no external
    database**, and also serves the built SPA and static assets;
  - `crates/chirp-frontend` — the chirp SPA built on ferric.
  - `deploy/` — k8s manifests and an ArgoCD Application; `.github/` — GitHub Actions CI.
- **The live deployment** of chirp, reachable and healthy on the project's k3s cluster at `c805525` (ArgoCD
  Application `chirp` Synced + Healthy; `/healthz` → 200). Exercise it as a user would, over its public
  endpoint, to measure the product. (Live-cluster facts and how to reach the endpoint are environment facts for
  running your checks; they are **not** product content and must never appear in anything you post to GitHub.)
- **The engagement request** in `TASK.md` (production-quality Rust/WASM framework + Twitter-style clone, built,
  tested, continuously delivered, reachable). The "what done looks like" there is the engagement's aim, **not**
  a release bar — translating it into a concrete, testable bar for chirp is your job.
- **The current board**: open issues #27, #25, #24, #23 (non-release-gating hardening/polish follow-ups under
  the devops epic) and EPIC trackers #1 (ferric), #2 (chirp), #3 (devops). There is **no** existing design doc,
  no `design/` or `docs/` tree, and no release bar in the repository. Check the board before filing so you
  extend or supersede existing issues rather than duplicating them.

Name everything you reference by its repository identity (`owner/repo`, a path relative to the repo root, an
issue/PR number, a commit SHA) — never by a path on the host or any cluster/host address.

## Concerns to cover (each a distinct concern, with its goal and its bar)

Cover the concerns a releasable, user-facing Twitter-style product needs. Name only the ones that apply; for any
you judge out of scope for this product, record that judgment. The usual set:

- **Product scope & requirements** — who the users are, what they must be able to do, the journeys through the
  product (sign up, sign in, post, read a timeline, follow, etc. as the product warrants), and what a releasable
  product of this kind includes and leaves out. *Bar*: stated as requirements and acceptance criteria someone
  can test.
- **Domain & application design** — the domain model, the modules and their responsibilities, how data persists
  (the current in-memory store does not survive a restart — decide what durable persistence the bar requires),
  the interfaces between parts, the entry points, and where state lives. *Bar*: held to ferric's and the
  existing crates' contracts; concrete enough to build against.
- **User experience & visual design** — information architecture, the screens and flows (including sign-up,
  sign-in, the core posting/timeline loops, and empty/error/loading states), a visual language and design
  system, responsive layout, and accessibility. *Bar*: designed screens, not a bare skeleton.
- **Identity, security & trust** — accounts and their lifecycle, real authentication and sessions, authorization
  (what each user may see and change), abuse/privacy basics, and the threat model this product's surface
  implies. *Bar*: real auth, not a stub; sessions that are safe to expose publicly.
- **Operational readiness for release** — what must be true in production beyond "it runs": durable data,
  backups, limits/quotas, observability, and a path to recover. *Bar*: a product that can be operated, not just
  started. (Note the existing hardening follow-ups #23/#24/#25 and fold them in where they belong rather than
  duplicating them.)
- **The plan** — the design turned into **epics and work-items**, each with acceptance criteria tied to the
  requirements, dependencies stated, and an order that reaches a usable product early and the release bar after.
  Each epic must be a coherent capability that can be built, reviewed, and landed as one change (one epic = one
  code goal), with its dependencies on other epics stated.

How you evaluate each concern, and which methodologies you bring to it, is yours to decide and load; this brief
describes the work well enough that you can.

## Declared output

- **A design PR** into `main` on a branch `work/design-chirp-r1`, adding the design to the repository (the
  requirements, the release bar, and the design artifacts) where code DAGs and reviews can read them. The PR
  goes through the review gate like any change; write its body for the repository's readers, with a plain-text
  `Closes`/`Refs` linkage to the relevant epics/issues as appropriate.
- **The backlog it implies, on the project board**: epics and issues with acceptance criteria that trace to the
  design, de-duplicated against what the board already holds, each placed under its epic in dependency order.
  The tickets say what the product needs and how it will be judged, not how to build it, and read as the
  repository's own (they trace to the design document in the repository, not to any taskflow).
- **A root `SYNTHESIS.md`** at this DAG's workspace root that: states the release bar; indexes the issues filed,
  by epic; and gives a measured account of where the live product (at `c805525`) stands against the bar — what
  is met, what is missing, and which epics/issues cover each gap. This is the DAG's fold and verdict.

Everything posted to GitHub (the design doc, the PR, issues, epics, comments) is written for the repository's
readers and carries **no** host/system details: no host or cluster addresses, no filesystem or taskflow paths,
no agent/DAG/run ids, no `SYNTHESIS.md` locations, no attribution trailers. Provenance is a link a reader can
open, not a footer about the machinery.

## Constraints

- Scope is `Nousix-LLC/nswe-demo` only (its code, branches, PRs, issues, labels, milestones, Project, and
  Actions) plus read-only use of the live deployment to measure the product. Do not touch other repos, clusters,
  or namespaces.
- Design branch `work/design-chirp-r1`; open one PR into `main`. Never force-push `main`; never rewrite merged
  history. No attribution trailers on commits or PR bodies (the engagement forbids them; see #27/HYG-1).
- You write **design and tickets, not product code.** Implementing the design is later code DAGs' work, one epic
  at a time.
- This is not a prototype/spike exemption: unless something in the repository or the engagement explicitly
  reduces it, the bar is a **releasable product**.
