## Observability

To operate chirp an operator has to be able to answer two questions at any moment: **is it serving
users, and what is it doing?** This section states what the product must expose so those questions can
be answered — a health and readiness signal, operational logs, serving metrics, and an audit trail of
operator actions. Each is stated as a requirement on what the product makes visible, not as a choice of
tooling: which log shipper, which metrics backend, which dashboard, and which alert rules are deferred to
later code work. The requirements here describe the *signals*; the status-and-incident posture
(`REQ-OPS-080..099`) builds detection, alerting, and user communication on top of them.

Three things anchor this section. First, chirp already answers a liveness probe (`/healthz` at `c805525`)
that reports only that the process is running; the release needs a **readiness** meaning that reflects
whether the product can serve users — including that its durable store is reachable
(`REQ-PROD-039`, `REQ-DOM-115`, `REQ-DOM-226`). Second, chirp holds private account data — credentials,
session tokens, verified contact — that is never public (`REQ-DOM-035`); that same rule binds everything
the product logs or emits as telemetry, so operational visibility is never bought with a privacy leak.
Third, the operator has a supported administrative surface (`REQ-PROD-028`, operator journey J9) that can
reach into accounts and content; actions taken through it must leave a record.

> **Note for the synthesis fold (issue #23):** the open follow-up #23 (exercise and harden the native
> install path) touches operational visibility — exercising that path is where the readiness signal, the
> logs, and the metrics below are first confirmed wired and observable in a real deployment. It is
> referenced here so the `existing_followups` fold can place it against the operational-visibility
> requirements it exercises, rather than being re-filed as a new requirement.

### Health and readiness

The product must distinguish **liveness** ("the process is running") from **readiness** ("the process can
serve users"). An orchestrator uses liveness to decide whether to restart a crashed process and readiness
to decide whether to send it traffic; conflating them either kills a process that is merely waiting on a
recoverable dependency, or sends users to a process that cannot serve them. Because chirp's
authoritative state now lives in a durable store distinct from the serving process, a process that cannot
reach that store is running but not ready — and readiness must say so.

### Structured operational logs

The product must record what it is doing in a form an operator can read and search after the fact,
covering the events needed to explain normal operation and to investigate a failure — and it must do so
without ever writing private account data. Logs are the operator's primary account of "what happened"
when something goes wrong.

### Serving metrics

The product must expose enough quantitative signal to tell, at a glance and over time, whether it is
serving users well: how much traffic it is handling, how much of that is failing, how slow it is, and how
close it is to overload. These are the signals that make "the product is degraded" something an operator
(and the status-and-incident posture) can detect rather than infer from user complaints.

### Operator and administrative audit trail

Because the supported administrative surface (`REQ-PROD-028`) can assist users, remove content, and action
accounts, the product must record who did what, to what, and when. An audit trail makes operator action
accountable and reviewable, and it is held to the same no-secrets/no-PII rule as the logs.

---

### Requirements: `REQ-OPS-060..079`

#### REQ-OPS-060 — Readiness is a distinct signal meaning "serving users"
- **statement**: The product exposes a readiness signal, distinct from liveness, whose meaning is that the
  product can serve users — not merely that the process is running. An operator or orchestrator
  can obtain readiness separately from liveness.
- **acceptance_criteria**: With the product fully able to serve, the readiness signal reports ready. With
  the product running but unable to serve its core loop, the readiness signal reports not-ready while the
  liveness signal still reports alive; the two are separately observable and can disagree.
- **verification_method**: operational_check
- **release_gating**: true
- **traces_to**: REQ-PROD-039, REQ-DOM-226

#### REQ-OPS-061 — Readiness reflects durable-store reachability
- **statement**: The readiness signal reports not-ready when the product's durable store is unreachable
  from the serving process, and ready when the store is reachable and the product can serve. Readiness is
  not satisfied by process liveness alone.
- **acceptance_criteria**: Make the durable store unreachable to a running serving process; the readiness
  signal reports not-ready. Restore reachability so the product can serve; the readiness signal reports
  ready.
- **verification_method**: operational_check
- **release_gating**: true
- **traces_to**: REQ-PROD-039, REQ-DOM-115

#### REQ-OPS-062 — Liveness reports process health only, not dependency health
- **statement**: The liveness signal reports whether the serving process itself is alive and able to make
  progress; it does not report not-alive solely because a recoverable dependency (such as the durable
  store) is temporarily unreachable. A dependency outage is reflected in readiness, not liveness, so an
  orchestrator restarts a genuinely crashed process but does not kill one that is alive and waiting on its
  store.
- **acceptance_criteria**: With the durable store unreachable but the serving process otherwise healthy,
  the liveness signal reports alive while the readiness signal reports not-ready. Liveness reports
  not-alive only when the process itself cannot make progress.
- **verification_method**: operational_check
- **release_gating**: true
- **traces_to**: REQ-DOM-226

#### REQ-OPS-063 — The health/readiness endpoint is unauthenticated and exposes no private data
- **statement**: The health and readiness signal can be queried without an account or session, so an
  operator or orchestrator can reach it, and its response discloses no private account data and no
  internal secret — it conveys serving status, not the contents of the system.
- **acceptance_criteria**: Query the health/readiness endpoint with no session; it responds with the
  serving status. Inspect the response; it contains no credential, session token, verified-contact value,
  or other private account data, and no secret such as a connection string.
- **verification_method**: manual_user_check
- **release_gating**: true
- **traces_to**: REQ-DOM-226, REQ-DOM-035

#### REQ-OPS-064 — Readiness is machine-consumable
- **statement**: The readiness signal is expressed so that an orchestrator or load balancer can
  mechanically distinguish ready from not-ready without interpreting prose — a decidable ready/not-ready
  outcome an automated caller can branch on.
- **acceptance_criteria**: Inspect the readiness signal while ready and while not-ready; in each state the
  signal carries a machine-distinguishable indication of the state (such that an automated caller routes
  traffic only when ready) without requiring a human to read a message.
- **verification_method**: inspection
- **release_gating**: true
- **traces_to**: REQ-PROD-039

#### REQ-OPS-065 — Readiness tracks current state and recovers without a restart
- **statement**: The readiness signal reflects the product's current ability to serve, continuously: when
  the condition that made it not-ready clears (for example the durable store becomes reachable again), the
  signal returns to ready on its own, without restarting or redeploying the serving process.
- **acceptance_criteria**: Drive readiness to not-ready by making the durable store unreachable, then
  restore reachability without restarting the process; the readiness signal returns to ready on its own.
- **verification_method**: operational_check
- **release_gating**: true
- **traces_to**: REQ-PROD-039

#### REQ-OPS-066 — Operational events are recorded in a structured, parseable form
- **statement**: The product records its operational events as structured, machine-parseable records with
  consistent fields (such as a timestamp, a severity, an event category, and an outcome), not as
  free-form prose, so an operator can search and filter them rather than reading them line by line.
- **acceptance_criteria**: Exercise the product and inspect its log output; operational events appear as
  structured records with consistent, named fields that a log tool can parse and filter.
- **verification_method**: inspection
- **release_gating**: true
- **traces_to**:

#### REQ-OPS-067 — Logs let one request be followed end to end
- **statement**: Log records carry a correlation identifier that ties together the events of a single
  request or user action, so an operator can follow one action through the product's logs from receipt to
  outcome.
- **acceptance_criteria**: Perform a single user action that touches more than one logged step; the log
  records for that action share a correlation identifier by which they can be selected together and read in
  order.
- **verification_method**: operational_check
- **release_gating**: false
- **traces_to**:

#### REQ-OPS-068 — Logs cover the events needed to explain operation and failure
- **statement**: The log record covers the operational events an operator needs to answer "what is it
  doing, and what went wrong": request handling and its outcome, errors and failures with a cause
  category, process start and stop, changes in durable-store connectivity, and authentication outcomes
  (success and failure) without the secret material involved.
- **acceptance_criteria**: Provoke, in a running product, a handled request, an error, a process restart, a
  loss and recovery of durable-store connectivity, and a failed and a successful sign-in; each is present
  in the logs as a distinct, categorized event with enough context to tell what happened.
- **verification_method**: operational_check
- **release_gating**: true
- **traces_to**: REQ-PROD-040

#### REQ-OPS-069 — Logs never contain credentials or private account data
- **statement**: Credentials, session tokens, verified-contact values, and any other private account data
  (`REQ-DOM-035`) are never written to the product's logs, in any field, at any severity. Operational
  visibility is never obtained at the cost of exposing private data in the logs.
- **acceptance_criteria**: Exercise sign-up, sign-in, recovery, and session use so that private data flows
  through the product, then inspect the logs produced; no credential, session token, verified-contact
  value, or other private account field appears in any log record. References to an account in a log use a
  non-secret identifier, not its private data.
- **verification_method**: inspection
- **release_gating**: true
- **traces_to**: REQ-DOM-035

#### REQ-OPS-070 — Severity is applied consistently
- **statement**: Log records carry a severity that is applied consistently, so an operator can separate
  normal operation from warnings and errors by filtering on severity rather than by reading every line.
- **acceptance_criteria**: Inspect logs from a period that includes both normal operation and at least one
  error; normal events and error events carry distinct severities consistent with their nature, and
  filtering to error severity surfaces the error events.
- **verification_method**: inspection
- **release_gating**: false
- **traces_to**:

#### REQ-OPS-071 — Errors are logged with enough context to investigate
- **statement**: When the product logs an error it includes enough diagnostic context — what operation
  failed, a cause category, and identifiers needed to locate the affected request or resource — that an
  operator can investigate without reproducing the failure, subject always to the no-secrets/no-PII rule
  (`REQ-OPS-069`).
- **acceptance_criteria**: Provoke a representative failure; its log record names the failing operation and
  a cause category and carries a correlation or resource identifier sufficient to investigate, and contains
  no private account data or secret.
- **verification_method**: inspection
- **release_gating**: false
- **traces_to**: REQ-DOM-035

#### REQ-OPS-072 — The product exposes request-rate and error-rate metrics
- **statement**: The product exposes serving metrics that report the rate of requests it is handling and
  the rate that are failing, broken down enough to see which class of surface is affected (for example
  reads versus writes, or by outcome category). Metric labels carry no private account data.
- **acceptance_criteria**: Generate a known mix of successful and failing requests; the metrics reflect the
  request rate and the error rate, distinguishable by surface class or outcome. Inspect the metric labels;
  they contain no handle-linked private data, credential, or contact value.
- **verification_method**: operational_check
- **release_gating**: true
- **traces_to**: REQ-PROD-040, REQ-DOM-035

#### REQ-OPS-073 — Request latency is observable as a distribution
- **statement**: The product exposes request-handling latency as a distribution (not only an average), so
  that a product which is up but slow — tail latency degrading while the mean looks acceptable — is
  visible.
- **acceptance_criteria**: Drive traffic including some slow requests; the latency metric reflects the
  spread of response times (for example percentiles or buckets), not a single averaged value, and the slow
  requests are visible in the distribution.
- **verification_method**: operational_check
- **release_gating**: false
- **traces_to**: REQ-PROD-040

#### REQ-OPS-074 — A saturation/headroom signal is observable
- **statement**: The product exposes a saturation or headroom signal — a measure of how close it is to its
  serving capacity, such as in-flight work against available capacity — so that approaching overload is
  detectable before it turns into errors or timeouts.
- **acceptance_criteria**: Drive load toward the product's capacity; the saturation signal rises as
  headroom shrinks, giving an observable indication of approaching overload ahead of widespread failures.
- **verification_method**: operational_check
- **release_gating**: false
- **traces_to**: REQ-PROD-040

#### REQ-OPS-075 — A serving/availability signal detects a degraded product
- **statement**: The product exposes an availability or serving signal sufficient to detect that it is
  degraded or not serving its core loop — the signal on which the status-and-incident posture
  (`REQ-OPS-080..099`) builds incident detection. It makes "the product is not serving users" an
  observable fact rather than an inference from complaints.
- **acceptance_criteria**: Put the product into a degraded state in which the core loop does not work for
  users; the serving/availability signal reflects the degradation. Return it to serving; the signal
  reflects recovery. The signal is suitable to drive automated detection.
- **verification_method**: operational_check
- **release_gating**: true
- **traces_to**: REQ-PROD-040

#### REQ-OPS-076 — Durable-store interaction is observable
- **statement**: Because serving now depends on the durable store, the product exposes the health of its
  interaction with that store — the rate of store errors and the latency of store operations — so an
  operator can tell a store problem from an application problem.
- **acceptance_criteria**: Induce elevated store latency or store errors; the product's store-interaction
  metrics reflect it, distinguishably from application-level request errors.
- **verification_method**: operational_check
- **release_gating**: false
- **traces_to**: REQ-DOM-115

#### REQ-OPS-077 — Administrative actions are recorded in an audit trail
- **statement**: Every action taken through the supported administrative surface (`REQ-PROD-028`) —
  assisting a user's recovery, removing content, and disabling or actioning an account — is recorded in an
  audit trail that captures the acting operator/administrator identity, the action taken, the target
  account or content, and the time.
- **acceptance_criteria**: Through the supported administrative surface, assist a user's recovery, remove a
  named chirp, and action an account; each action produces an audit entry naming who acted, what they did,
  which account or content was affected, and when. An administrative action that reaches accounts or
  content leaves no untraced path.
- **verification_method**: operational_check
- **release_gating**: true
- **traces_to**: REQ-PROD-028

#### REQ-OPS-078 — Audit records are durable and not silently editable
- **statement**: Audit-trail entries are durable — they survive restart and redeploy like the rest of the
  product's authoritative state — and are not silently editable or erasable through the product's ordinary
  surfaces, so the trail remains trustworthy when it is reviewed after the fact.
- **acceptance_criteria**: Produce audit entries, then restart or redeploy the product; the entries are
  still present and unchanged. No ordinary product surface offers a way to alter or delete an existing
  audit entry without trace.
- **verification_method**: operational_check
- **release_gating**: false
- **traces_to**: REQ-PROD-028

#### REQ-OPS-079 — The audit trail carries no secrets or private data
- **statement**: The audit trail records who acted, what they did, and on which account or content using
  stable, non-secret identifiers, and never stores credentials, session tokens, or verified-contact values
  (`REQ-DOM-035`). The same no-secrets/no-PII rule that binds the logs binds the audit trail.
- **acceptance_criteria**: Inspect audit entries produced by representative administrative actions; each
  names the actor, action, and target by non-secret identifier and contains no credential, session token,
  or verified-contact value.
- **verification_method**: inspection
- **release_gating**: true
- **traces_to**: REQ-DOM-035
