# COMPLETE — SUBTASK_domain_model

**Task**: Define chirp's domain model (entities, relationships, invariants) as `REQ-DOM-001..049`, held
to `crates/chirp-types` and the current `crates/chirp-server` domain at `Nousix-LLC/nswe-demo @ c805525`.

**Decompose-evaluation**: `Atomic`. One responsibility (model the domain as a requirements register +
canonical vocabulary), one output file, one vocabulary this task is contracted to own as a single
artifact. Scope and Single-Responsibility tests both cleared; only raw output-line count flickered (the
weakest signal, overridden by the passed concern tests).

## Output produced

- `outputs/domain-model.md` — the `domain_model` section content, a labelled **canonical entity
  vocabulary**, the `REQ-DOM-001..040` register (each with id, statement, testable acceptance criteria,
  `release_gating`, and a `traces_to` where it refines a `REQ-PROD-*`), and a traceability table.
  `041..049` left reserved (not padding).

## How it composes with the parent (`SUBTASK_domain_app_design`)

- **Contract compliance** (`../contracts/req_dom_partition.yaml`, `../../contracts/id_and_traceability_schema.yaml`):
  - `REQ-DOM-*` ids used only within `001..049`; `REQ-<AREA>-NNN` format and per-requirement fields not
    redefined.
  - The entity-vocabulary seam is owned here and made explicit as the labelled vocabulary; persistence
    (`REQ-DOM-100..149`) and module-structure (`REQ-DOM-200..249`) reference entities only by these
    canonical names (Account/User, Handle, Display name, Bio, Chirp, Chirp text, Reply, Follow, Like,
    Timeline, Session, ids, Timestamp; plus the referenced Credential and Verified contact).
  - Every `REQ-DOM-*` carries a statement, testable acceptance criteria, and a `release_gating` flag;
    those refining a product requirement cite the `REQ-PROD-*` (traceability table in the output).
- **Held to the existing crates**: each entity names the `chirp-types` type that already carries it;
  invariants (handle format, chirp length, no self-follow, idempotent follow/like, at-most-one like,
  reverse-chronological bounded timeline, denormalized counts, reply-target existence, opaque
  server-assigned ids, UTC timestamps) match `chirp-types` and the `ChirpRepository` seam.
- **What, not how**: persistence/storage mechanics, the credential and session-proof mechanism, and the
  verification of contact are stated as requirements and deferred by prose to the persistence section
  (`REQ-DOM-100..149`) and the identity/security design (`REQ-ID-*`).

## Notes for `SUBTASK_synthesis`

- The output file is the `domain_model` section body. Repo-destined prose is clean of taskflow/host
  detail; the only `SUBTASK_*`/range-partition references remaining are inside HTML comments (build
  provenance), droppable when assembling `design/domain-application-design.md`.
- Gating-`false` `REQ-DOM-*`: `010` (handle-change policy, trace `REQ-PROD-018`) and `016` (reading a
  reply in conversation, trace `REQ-PROD-004`). All others are `release_gating: true`.
- Entities durable per `REQ-PROD-037` (accounts, chirps, follows, likes, sessions) are all in the
  vocabulary, as are the account-associated credential and verified contact (`REQ-DOM-033`, `034`) that
  persistence must carry.

## Environmental note

This invocation ran as a reconstructed taskflow node with the methodology-domain binding unset; the
Phase-B `design` methodology loader returned `agent_domain_unset`. Work proceeded from the principal
product-designer Role Overlay (the design methodology's judgment surface) and the brief's named bundle
intents (Product Strategy; Release Definition / `release_gating`), per the dispatch rule to document an
ambiguity and proceed with the most reasonable interpretation.
