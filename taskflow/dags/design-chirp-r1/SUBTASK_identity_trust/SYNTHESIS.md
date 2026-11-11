# SYNTHESIS — SUBTASK_identity_trust (identity, security & trust)

Fold record for the identity-trust subtree. The synthesis gate read the four spoke partials, authored the
integrating threat model and its two threat-driven requirements, confirmed the assembled deliverable
`outputs/identity-security.md` (six sections + the consolidated `REQ-ID-*` register), verified the eight
subtree-contract identities against recorded evidence, and folds the result up into the parent node.

## What was produced

- **`outputs/identity-security.md`** — the parent node's declared output: the assembled, repository-ready
  design-area deliverable. Six required sections in `design_artifact_map.yaml` order
  (`accounts_and_lifecycle`, `authentication_and_sessions`, `authorization`, `abuse_and_privacy_basics`,
  `threat_model`, `requirements_and_acceptance_criteria`), and a consolidated register of all 73 `REQ-ID-*`
  entries, each with its five fields (statement, acceptance_criteria, release_gating, verification_method,
  traces_to).
- **`threat_model` section + `REQ-ID-100`, `REQ-ID-101`** — the gate's integrating cross-cutting view,
  derived from the four areas: `REQ-ID-100` (product-wide transport confidentiality, generalizing the
  session-only `REQ-ID-041` to the whole private surface) and `REQ-ID-101` (anti-automation / bot
  resistance on the sign-up and public write surfaces). Operator-action auditability was deliberately
  **not** minted — it is already owned by `REQ-ID-073`.

## Register composition — the 73 REQ-ID entries

| Owner area | Section | Range allotted | Ids minted | Count |
|------------|---------|----------------|------------|-------|
| `SUBTASK_accounts_lifecycle` | accounts_and_lifecycle | 001–029 | 001–024 | 24 |
| `SUBTASK_auth_sessions` | authentication_and_sessions | 030–059 | 030–048, 050, 051 (049 unused) | 21 |
| `SUBTASK_authorization` | authorization | 060–079 | 060–074 | 15 |
| `SUBTASK_abuse_privacy` | abuse_and_privacy_basics | 080–099 | 080–090 | 11 |
| `SUBTASK_synthesis` (this gate) | threat_model | 100–119 | 100, 101 | 2 |
| **Total** | | | | **73** |

## Subtree contract identities — evidence

Asserted against `contracts/_MANIFEST.yaml`. Each was checked, in this reconstructed invocation,
independently against the assembled deliverable, the four partials, and the product-requirements register.
No identity was silently plugged.

| Identity | Result | Evidence |
|----------|--------|----------|
| `REQ_ID_UNIQUE_IN_RANGE` | PASS | The register holds 73 distinct ids with no duplicate. Each sits within its owner's declared range: accounts `001–024` (⊂ 001–029), auth `030–048, 050, 051` (⊂ 030–059; 049 intentionally unused per the auth spoke's note), authorization `060–074` (⊂ 060–079), abuse/privacy `080–090` (⊂ 080–099), threat-driven `100, 101` (⊂ 100–119). No id crosses an owner boundary. |
| `REQ_ID_TESTABLE_AND_TRACED` | PASS | All 73 entries carry a statement, a testable `acceptance_criteria`, a `release_gating` flag, and a `traces_to` (field counts 73/73/73/73). The distinct set of `traces_to` targets actually referenced is the 30 ids {001, 002, 003, 005, 006, 007, 008, 009, 010, 011, 012, 013, 014, 015, 016, 017, 018, 019, 020, 021, 022, 023, 024, 025, 026, 027, 028, 029, 031, 041} — every one resolves to an existing `REQ-PROD-*` in the product-requirements register `REQ-PROD-001..042`. (`REQ-PROD-004` and `REQ-PROD-030/032–040/042` are simply not cited by any identity requirement; no cited target falls outside the register.) |
| `GATING_REQ_NAMES_VERIFICATION` | PASS | Every entry's `verification_method` is drawn only from the inherited vocabulary [`manual_user_check`, `automated_test`, `inspection`, `operational_check`]; no out-of-vocabulary value appears. |
| `SIX_SECTIONS_PRESENT` | PASS | The assembled file carries all six required sections as `##` headings in `design_artifact_map.yaml` order (verified at the document headings; a closing additive `## Coverage note` does not displace them). |
| `PROD_IDENTITY_NEEDS_COVERED` | PASS | Every `REQ-PROD-*` identity/security need (008–014, 016–024, and the identity aspects of 025–028) is answered by ≥1 `REQ-ID-*` (coverage table below). Two product needs are carried by sibling areas by design and recorded with a reason, not left as holes. |
| `THREAT_MODEL_ANSWERS` | PASS | The threat model walks all six STRIDE categories plus content-abuse over chirp's public surface; each threat names the `REQ-ID-*` that answers it or records a residual risk (R1/R2/R3) with why it is acceptable for the bar. |
| `NO_SCHEMA_REDEFINITION` | PASS | The deliverable composes against the inherited `REQ-<AREA>-NNN` format, required fields, verification vocabulary, and design-artifact map, and redefines none of them. The two new ids sit within this subtree's own partitioned range (100–119); additions are additive only. |
| `DELIVERABLE_HYGIENE` | PASS | A pattern scan of `outputs/identity-security.md` found no host/cluster address, no filesystem or taskflow path, no `SUBTASK_`/`_BRIEF`/`_GLOBAL`/`SYNTHESIS.md` reference, no agent/DAG/run id, no stray tool-call tags (the `auth-sessions.md` partial's trailing `</content>`/`</invoke>` artifacts did not reach the assembled file), and no attribution trailer. References are by repository identity (`Nousix-LLC/nswe-demo` @ `c805525`) and sibling design-area names only. A writing-voice scan found none of the flagged tells (moral/character adjective on a non-agent, narrated candor, hollow filler, slot-fill templates, stacked connectives). |

## Accepted residual risks (recorded, not plugged)

- **R1** — a phished or guessed single secret can reach an account (MFA out of scope, `REQ-ID-050`);
  bounded by `REQ-ID-035, 038, 039, 045, 046`. Acceptable for a public microblog of individual accounts
  with no regulatory obligation; not foreclosed later.
- **R2** — full volumetric / infrastructure DoS resistance is not owned here; the first line is
  `REQ-ID-035, 085, 101`, with enforcement depth carried by the operational-readiness area (`REQ-OPS-*`)
  and the `REQ-PROD-040` availability target.
- **R3** — block/mute are non-gating (`REQ-ID-083, 084`); the gated harassment floor is reporting
  (`REQ-ID-080–082`) + operator action (`REQ-ID-070–074`) + rate limits (`REQ-ID-085`). The release bar
  may elect to gate one of block/mute.

## Coverage — product identity/security needs

| REQ-PROD need | Answered by |
|---------------|-------------|
| 008 real sign-up credential | REQ-ID-002, 030, 034, 036 |
| 009 handle validation | REQ-ID-003 |
| 010 owner-only sign-in | REQ-ID-030–037, 040–043, 046, 050, 051, 060, 064 |
| 011 not-found vs failed signal | REQ-ID-033, 015, 035, 069 |
| 012 verified contact | REQ-ID-004, 005, 009, 014 |
| 013 recovery | REQ-ID-013, 014, 015, 016 |
| 014 server-side sign-out / session hygiene | REQ-ID-039 (+ 038, 040–046, 048, 010, 024) |
| 015 stay-signed-in (convenience) | REQ-ID-047, 048 |
| 016 edit profile | REQ-ID-007, 066 |
| 017 settings surface | REQ-ID-008, 009, 010, 011, 066 |
| 018 handle-change policy | REQ-ID-012 |
| 019 data export | REQ-ID-017, 018, 019, 090 |
| 020 deletion | REQ-ID-020, 023, 024, 067 |
| 021 deletion outcome | REQ-ID-021, 023, 074, 088 |
| 022 confirmed deletion | REQ-ID-022 |
| 023 authorization boundary | REQ-ID-060, 064, 065, 066, 067, 068 |
| 024 privacy basics | REQ-ID-001, 018, 019, 023, 061, 062, 063, 069, 072, 086, 087, 100 |
| 025 report abuse (identity aspect) | REQ-ID-080, 082, 071 |
| 026 stated rules (identity aspect) | REQ-ID-081 |
| 027 block/mute (identity aspect) | REQ-ID-083, 084 |
| 028 admin/support authority (identity aspect) | REQ-ID-070, 071, 072, 073, 074 |

**Carried by sibling areas, named not re-minted** (so coverage reads as answered, not as a hole):
`REQ-PROD-041` (limits/quotas enforcement depth) → operational-readiness `REQ-OPS-*`, to which
`REQ-ID-035, 085, 101` defer; `REQ-PROD-037` (durable storage) → domain + operational-readiness, on which
every lifecycle and session requirement here depends.

## REQ-ID ↔ REQ-PROD trace list

For the parent synthesis to fold into the design-wide traceability matrix. All targets exist in the
product-requirements register (`REQ-PROD-001..042`).

| REQ-ID | release_gating | traces_to (REQ-PROD) |
|--------|----------------|----------------------|
| REQ-ID-001 | true | 007, 024 |
| REQ-ID-002 | true | 008 |
| REQ-ID-003 | true | 009 |
| REQ-ID-004 | true | 012 |
| REQ-ID-005 | true | 012 |
| REQ-ID-006 | false | 012, 031 |
| REQ-ID-007 | true | 016 |
| REQ-ID-008 | true | 017 |
| REQ-ID-009 | true | 017, 012 |
| REQ-ID-010 | true | 017, 014 |
| REQ-ID-011 | false | 017, 029 |
| REQ-ID-012 | false | 018 |
| REQ-ID-013 | true | 013 |
| REQ-ID-014 | true | 013, 012 |
| REQ-ID-015 | true | 013, 011 |
| REQ-ID-016 | true | 013, 014 |
| REQ-ID-017 | true | 019 |
| REQ-ID-018 | true | 019, 024 |
| REQ-ID-019 | true | 019, 024 |
| REQ-ID-020 | true | 020 |
| REQ-ID-021 | true | 021 |
| REQ-ID-022 | true | 022 |
| REQ-ID-023 | true | 020, 024 |
| REQ-ID-024 | true | 020, 014 |
| REQ-ID-030 | true | 008, 010 |
| REQ-ID-031 | true | 010 |
| REQ-ID-032 | true | 010 |
| REQ-ID-033 | true | 011 |
| REQ-ID-034 | true | 008, 010 |
| REQ-ID-035 | true | 010, 011 |
| REQ-ID-036 | true | 008, 010 |
| REQ-ID-037 | true | 010 |
| REQ-ID-038 | true | 014, 015 |
| REQ-ID-039 | true | 014 |
| REQ-ID-040 | true | 010, 014 |
| REQ-ID-041 | true | 010, 014 |
| REQ-ID-042 | true | 010, 014 |
| REQ-ID-043 | true | 010 |
| REQ-ID-044 | true | 014, 015 |
| REQ-ID-045 | true | 014 |
| REQ-ID-046 | true | 010, 014 |
| REQ-ID-047 | false | 015 |
| REQ-ID-048 | false | 015, 014 |
| REQ-ID-050 | false | 010 |
| REQ-ID-051 | false | 008, 010 |
| REQ-ID-060 | true | 023, 010 |
| REQ-ID-061 | true | 007, 024 |
| REQ-ID-062 | true | 024 |
| REQ-ID-063 | true | 002, 024 |
| REQ-ID-064 | true | 023, 010 |
| REQ-ID-065 | true | 001, 003, 005, 006, 023 |
| REQ-ID-066 | true | 016, 017, 023 |
| REQ-ID-067 | true | 020, 023 |
| REQ-ID-068 | true | 023, 001 |
| REQ-ID-069 | true | 024, 011 |
| REQ-ID-070 | true | 028 |
| REQ-ID-071 | true | 028, 025 |
| REQ-ID-072 | true | 028, 024 |
| REQ-ID-073 | true | 028 |
| REQ-ID-074 | true | 028, 021 |
| REQ-ID-080 | true | 025 |
| REQ-ID-081 | true | 026 |
| REQ-ID-082 | true | 025 |
| REQ-ID-083 | false | 027 |
| REQ-ID-084 | false | 027 |
| REQ-ID-085 | true | 041 |
| REQ-ID-086 | true | 024 |
| REQ-ID-087 | true | 024 |
| REQ-ID-088 | true | 021, 024 |
| REQ-ID-089 | false | 024 |
| REQ-ID-090 | true | 019, 024 |
| REQ-ID-100 | true | 024, 010, 014 |
| REQ-ID-101 | true | 041, 010 |

## Fold

- Parent node: `SUBTASK_identity_trust`.
- Parent's declared output now present and verified: `outputs/identity-security.md`.
- This record is authored at the fold location (the parent's directory) and consumed by
  `engine_resume_suspended` to flip the parent `SUBTASK_identity_trust` from `SUSPENDED` to `COMPLETED`.
- No remediation subtree was required: all eight identities passed with recorded evidence; no gap,
  collision, untraceable requirement, schema redefinition, or hygiene defect was found.

## Note on this invocation

This gate ran as a resumed, reconstructed node. An earlier invocation authored the deliverable and a fold
record but ended before the terminal report and the fold syscall, so the parent stayed `SUSPENDED` and the
gate was re-dispatched. This invocation re-verified the eight identities independently against the real
artifacts — the assembled `outputs/identity-security.md`, the four spoke partials, and the
product-requirements register — rather than trusting the prior record's claims. The checks and their
evidence:

- 73 `REQ-ID-*` headings, unique and ascending, each within its owner's range (accounts 001–024, auth
  030–048 + 050 + 051, authorization 060–074, abuse/privacy 080–090, threat 100–101); the owned-id set
  matches the four partials' owned ranges exactly (cross-area ids in the partials are prose references).
- All 73 entries carry statement, acceptance_criteria, release_gating, verification_method, and traces_to
  (field counts 73/73/73/73/73). The distinct `traces_to` target set {001, 002, 003, 005, 006, 007,
  008–029, 031, 041} resolves entirely within the product register `REQ-PROD-001..042`; no target is
  dangling. Every `verification_method` is drawn from the inherited vocabulary (manual_user_check 31,
  inspection 17, operational_check 14, automated_test 11).
- Six required sections present as `##` headings in `design_artifact_map.yaml` order; the closing
  `## Coverage note` is additive and does not displace them.
- Every `REQ-PROD-*` identity need (008–014, 016–024, identity aspects of 025–028) answered; two needs
  (`REQ-PROD-041`, `REQ-PROD-037`) carried by sibling areas with recorded reasons.
- Threat model walks the six STRIDE categories plus content-abuse, each naming its mitigating `REQ-ID-*`
  or a recorded residual (R1/R2/R3).
- No schema redefinition; a pattern scan of the deliverable found no host/cluster/path/taskflow detail, no
  workspace-file reference, no tool-call artifact, and no attribution trailer; a writing-voice scan found
  none of the flagged tells.

All eight identities passed; no gap, collision, untraceable requirement, schema redefinition, or hygiene
defect was found, so no remediation subtree was needed. The fold is completed from this invocation. The
Phase-B methodology surface was unbound in the reconstructed node (`agent_domain_unset`); verification
proceeded on the principal-product-designer posture and the subtree contract's own identity list.
