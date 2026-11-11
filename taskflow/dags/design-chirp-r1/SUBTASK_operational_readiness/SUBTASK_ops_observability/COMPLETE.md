# COMPLETE — SUBTASK_ops_observability

## What was done
Authored `outputs/observability.md`: the `observability` section of the chirp operational-readiness
design, with the section prose and the full `REQ-OPS-060..079` requirement register. The section states,
as testable requirements, what must be visible to operate chirp — a trustworthy health/readiness signal,
structured operational logs, serving metrics, and an operator/admin audit trail — each as a requirement on
what the product exposes, with tooling (log shipper, metrics backend, dashboards, alert rules) deferred to
later code work.

## Output
- `outputs/observability.md` — repository-ready fragment (section prose + `REQ-OPS-060..079`), owning the
  `observability` section and the `REQ-OPS-060..079` number range per `../contracts/reqs_ops_partition.yaml`.

## Coverage of the brief's four aspects
- **Health vs readiness** (`REQ-OPS-060..065`): readiness distinct from liveness and meaning "serving
  users"; readiness reflects durable-store reachability; liveness reports process health only, not
  dependency health; the endpoint is unauthenticated and leaks no private data; readiness is
  machine-consumable and recovers continuously without a restart. Traces `REQ-PROD-039`, `REQ-DOM-115`,
  `REQ-DOM-226`.
- **Structured logs + no-secrets/no-PII** (`REQ-OPS-066..071`): structured parseable records; request
  correlation; coverage of the events needed to explain operation and failure; a firm rule that
  credentials, session tokens, verified-contact values, and other private account data are never logged
  (`REQ-OPS-069`, traces `REQ-DOM-035`); consistent severity; error diagnostic context.
- **Serving metrics** (`REQ-OPS-072..076`): request/error rates, latency distribution, saturation/headroom,
  a serving/availability signal the status-and-incident child builds detection on, and durable-store
  interaction health. Traces `REQ-PROD-040`, `REQ-DOM-115`, `REQ-DOM-035`.
- **Operator/admin audit trail** (`REQ-OPS-077..079`): administrative actions recorded (who/what/target/
  when); audit records durable and not silently editable; audit carries no secrets or private data. Traces
  `REQ-PROD-028`, `REQ-DOM-035`.

## How it composes with the parent
- Uses only `REQ-OPS-060..079`; does not renumber outside the range, write another child's section, or
  redefine the ancestor id scheme or verification vocabulary.
- Every requirement carries `statement`, `acceptance_criteria`, `verification_method` (from the closed
  vocabulary: `operational_check`, `inspection`, `manual_user_check`), `release_gating`, and `traces_to`.
- Supports the subtree identities the synthesis gate asserts: the `observability` section is present and
  covered; the OPS ids are testable and release-gating-flagged; traced ids are real `REQ-PROD-*`/`REQ-DOM-*`.

## Dependents
- `SUBTASK_ops_status_incident` builds incident detection and user communication on the serving/availability
  and log/metric signals stated here — especially `REQ-OPS-075` (the degraded-product signal) and
  `REQ-OPS-068`/`REQ-OPS-072`.
- `SUBTASK_ops_synthesis` consolidates this fragment into `operational-readiness.md` and the consolidated
  register.

## Follow-up reference (for the synthesis fold, not re-filed)
- Issue **#23** (exercise/harden the native install path) touches operational visibility — it is where the
  readiness signal, logs, and metrics are first confirmed wired and observable in a real deployment. Flagged
  in the fragment prose so `SUBTASK_ops_synthesis` can place it in `existing_followups` against the
  observability requirements it exercises, rather than duplicating it as a new requirement.

## Environment note (recorded, not a blocker)
The Phase-B `design` methodology loader is unavailable in this environment (`engine_load_methodology`
returned `agent_domain_unset`; the app bundle exposes no filesets). As directed by the brief and the subtree
hub, the work was carried out on the product-design persona and the relayed guidance (bundle IDs: Release
Readiness primary; Release Definition, Identity and Trust supporting), and the unavailability is recorded
here rather than blocking.

## Writing hygiene pass
Ran the avoid-ai-writing checklist by hand against the P0/P1 catalog (no `avoid-ai-writing` skill present in
this node). Trimmed decorative "actually" from the readiness prose where the liveness/readiness contrast
already carried the meaning; retained one "genuinely crashed" where it names a real contrast (a crashed
process vs. one merely waiting on its store). No category-error adjectives, slot-fill templates, padded
triads, or hollow intensifiers remain.
