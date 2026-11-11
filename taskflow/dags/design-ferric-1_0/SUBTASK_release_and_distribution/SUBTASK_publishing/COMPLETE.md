# COMPLETE — SUBTASK_publishing

**Task:** Design Ferric 1.0 crates.io publishing readiness & multi-crate release as `REQ-REL-001..019`.
**Decompose evaluation:** Atomic (one responsibility — a single publishing-readiness requirements register; one kind
of output in the parent REQ schema; all triggers cleared, both concern tests passed).

## What was produced
`publishing.md` — the publishing-readiness design and the `REQ-REL-001..011` register (the remaining `012..019` left
unused within this spoke's range). A source partial for `SUBTASK_rel_synthesis` to merge into
`release-and-distribution.md`.

## Register summary
| id | Covers | verification_method | stage / gating |
|---|---|---|---|
| REQ-REL-001 | Permissive license on every crate (the headline gap) | publishability, doc_inspection | one_oh / true |
| REQ-REL-002 | Complete per-crate crates.io metadata | doc_inspection, publishability | one_oh / true |
| REQ-REL-003 | docs.rs API-docs build per crate | automated_test, doc_inspection | one_oh / true |
| REQ-REL-004 | Intra-workspace deps carry path **and** version | doc_inspection, publishability, automated_test | one_oh / true |
| REQ-REL-005 | `cargo publish --dry-run` / `cargo package` passes (incl. `todo!()`) | publishability | one_oh / true |
| REQ-REL-006 | Packaged `.crate` contains license + README, excludes cruft | doc_inspection, publishability | one_oh / true |
| REQ-REL-007 | Crate names owned on crates.io | doc_inspection | one_oh / true |
| REQ-REL-008 | Crates publish in dependency order (`ferric` before `ferric-router`) | doc_inspection, publishability | one_oh / true |
| REQ-REL-009 | One coordinated lockstep version set (`version.workspace = true`) | doc_inspection, publishability | one_oh / true |
| REQ-REL-010 | Documented, repeatable release procedure | doc_inspection, publishability | one_oh / true |
| REQ-REL-011 | Published manifests carry only resolvable crates.io version reqs | publishability, automated_test | one_oh / true |

## Contract conformance
- **J1 (disjoint ranges):** only `REQ-REL-001..011` minted, inside the assigned `001..019`. No collisions.
- **J2 (schema conformance):** every id carries id/statement/rationale/acceptance_criteria/stage/release_gating/references per `../../contracts/id_and_traceability_schema.yaml`.
- **J3 (framework verification):** every acceptance criterion uses `publishability`, `doc_inspection`, or `automated_test` from the parent closed vocabulary.
- Covers the four brief facets (license, metadata, path→version, multi-crate release order) each with ≥1 checkable requirement; contributes to J4 (publishing readiness) and feeds J6 (peers named: Leptos, Dioxus, Yew; Cargo book + Rust API Guidelines cited by name).

## Grounding & evidence
Confirmed against live manifests in `Nousix-LLC/nswe-demo` @ `main` (baseline `276138f`): no license/LICENSE anywhere;
no keywords/categories/documentation/homepage/explicit-readme; `ferric-router → ferric` path dep with no version;
`version.workspace = true` lockstep. Standards verified by fetch/known-reference: Cargo book *Publishing on crates.io*
(license/description required; `--dry-run` ≡ `cargo package`) and *Specifying Dependencies* (path dep needs a version
to publish); Rust API Guidelines C-PERMISSIVE (`MIT OR Apache-2.0`); docs.rs auto-build.

## Writing-voice pass
Ran the avoid-ai-writing check by hand against P0/P1 tells (skill/patterns file not present in this workspace). One
character-adjective tell fixed ("footprint honest" → concrete rephrase). No narrated candor, unpaired contrasts,
slot-fill templates, padded triads, or hollow intensifiers remain.

**Design, not implementation:** no publishing automation, release tool, or CI gate chosen — requirements state the
condition on the published crates and the `cargo` commands that check them.
