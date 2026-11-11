# COMPLETE — SUBTASK_auth_sessions

## What was done
Designed real authentication and publicly-safe sessions for chirp as the `authentication_and_sessions`
section partial, in the format fixed by `../contracts/req_id_partition.yaml`: section prose, a
`REQ-ID-*` register, and notes for the synthesis. The partial closes the critical handle-only sign-in
gap (sign-in now proves ownership of a secret the owner holds) and gives sessions a safe public-internet
posture (bounded lifetime, server-side invalidation and sign-out, fixation resistance, transport and
theft protection, per-session revocation, recovery that ends old sessions).

## What was produced
- `outputs/auth-sessions.md` — the repository-ready section partial. 21 requirements minted
  (`REQ-ID-030`..`REQ-ID-048`, `REQ-ID-050`, `REQ-ID-051`; `049` and `052`..`059` left free), all within
  the allotted `REQ-ID-030..059` range.

## How it composes with the parent
- **Contracts**: composes against both the subtree contract (`req_id_partition.yaml` partial format,
  id range, section ownership) and the root schema (`id_and_traceability_schema.yaml` required fields +
  verification vocabulary); redefines neither. Every `REQ-ID-*` carries a statement, testable
  `acceptance_criteria`, a `release_gating` flag (false flags state their reason inline), a
  `verification_method` from the inherited vocabulary, and `traces_to` ≥1 existing `REQ-PROD-*`
  (008, 010, 011, 014, 015).
- **Scope decision recorded**: MFA (`REQ-ID-050`) and third-party/social sign-in (`REQ-ID-051`) are
  stated out of scope for the release bar, each with its reason and a "do not foreclose later" note.
- **Seams flagged for synthesis**: sign-up/recovery flows (owned by `accounts_lifecycle`), the
  active-sessions settings surface (REQ-PROD-017), anti-guessing enforcement (`REQ-OPS-*`), the durable
  session store (`REQ-DOM-*`/`REQ-OPS-*`), and a possible product-wide transport-confidentiality
  generalization in the synthesis's `REQ-ID-100..119` range. The notes also map each requirement cluster
  to the STRIDE threats it answers and record the residual risk accepted for the bar given MFA is out.

## Verification performed
- Id range, five-field completeness, verification-vocabulary conformance, and `REQ-PROD` trace existence
  checked mechanically — all pass.
- Writing-voice pass (plain, checkable; no machine-writing tells) and repository-hygiene pass (no
  host/system/taskflow/path/id detail, no attribution trailer) run over the deliverable — both clean.
</content>
