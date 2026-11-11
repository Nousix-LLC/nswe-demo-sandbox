## Status and incident

Observability (`REQ-OPS-060..079`) gives an operator the signals to see that chirp is degraded. This
section states what has to happen next: that a degradation visible in those signals is **noticed and acted
on**, that **users are told** when the product is down or going down for maintenance, and that the product
owes a person a usable experience while it is impaired. It also states, as an operated commitment, what
"reasonably available" (`REQ-PROD-040`) means for this product in a number someone can measure against.

The posture here is sized for what chirp is: a small hosted service run by the people who build it
(operator journey J9), not a large product with a staffed on-call rotation. So the requirements ask for a
detection path, a named person who is responsible when something fires, a way to reach users that does not
itself go down with the product, and a stated availability target — and they stop there. The incident
*tooling* (which alerting backend, which status-page service), the paging schedule, and the written
runbooks are deferred to later code work; this section states the requirements they have to satisfy.

Three boundaries keep this section from redrawing its neighbours. Incident **detection** builds directly on
the observability serving/availability signal (`REQ-OPS-075`) and the request, saturation, and
store-interaction metrics (`REQ-OPS-072`, `REQ-OPS-074`, `REQ-OPS-076`) — it does not define new signals.
The **user-facing error and degraded screens** — what a person actually sees when an action fails or a list
will not load — are the experience design's (`REQ-UX-*`, and the product-level `REQ-PROD-033` and
`REQ-PROD-034`); this section requires that an incident lands the user *in* those designed states rather
than in a blank page or a crash, and does not specify the states themselves. The **data** recovery-point
and recovery-time targets belong to backups and recovery (`REQ-OPS-020..039`); the time target here is
time-to-restore-serving during an incident, which is a different thing from restoring lost data.

### Incident detection and response

A product is not being operated if the first notice of an outage is a user complaint. The serving signal
that observability exposes has to be watched, and a degradation in it has to reach a person who is
responsible for acting. For a product this size that means a detection path from the signals to an alert, a
light severity split so the response is proportionate to what broke, and a named expectation of who
responds — not an organisation chart.

### Telling users: status and maintenance communication

When chirp is down or degraded, a person trying to use it should be able to find out that it is chirp that
is affected and not their own connection, without guessing. That calls for a status surface or an
in-product notice — and, critically, one that does not travel down the same path that just failed, because
a status page served by the same process that is down tells a user nothing. The same surface carries
advance notice of planned maintenance, and reflects recovery when service returns. Whatever it shows is
held to the product's no-secrets/no-private-data rule (`REQ-DOM-035`), the same rule that binds the logs
and the audit trail.

### The degraded-state experience boundary

What a person sees on a failed action or an unreachable list — the explained error, the preserved draft,
the routed-to-sign-in on an expired session — is designed by the experience area (`REQ-UX-*`,
`REQ-PROD-033`, `REQ-PROD-034`). The operational requirement is the join: when a dependency the product
needs is unavailable in production (for example the durable store, per `REQ-DOM-115`), the operated product
fails *into* those designed states rather than into a blank screen or a process crash, and contains a
partial failure to the capability that is actually affected where its design allows.

### Availability as an operated commitment

"Reasonably available" (`REQ-PROD-040`) is only testable if it is a number. This product states an
availability target proportionate to a small hosted service, measures it from the serving/availability
signal (`REQ-OPS-075`) over a stated window rather than asserting it, and accounts for announced
maintenance so a routine deploy is not counted as an unplanned outage. Incident response aims to restore
serving within a stated time that is consistent with that target.

---

### Requirements: `REQ-OPS-080..099`

#### REQ-OPS-080 — A serving degradation is detected, not waited for
- **statement**: The product's serving/availability signal (`REQ-OPS-075`) is watched in production so that
  a degradation — the product not serving its core loop, or serving it with elevated errors — is detected
  as an operational event and does not depend on a user reporting it. Detection reaches a responsible
  operator (`REQ-OPS-083`).
- **acceptance_criteria**: Put the product into a state where the core loop does not work for users; within
  a bounded time the configured detection raises a notification to the responsible operator, without a user
  having had to report the problem first. Return the product to serving; no further alert for that incident
  is raised.
- **verification_method**: operational_check
- **release_gating**: true
- **traces_to**: REQ-PROD-040

#### REQ-OPS-081 — Detection is driven by the observability signals
- **statement**: Incident detection is built on the observability signals — the serving/availability signal
  (`REQ-OPS-075`), the request- and error-rate metrics (`REQ-OPS-072`), the saturation/headroom signal
  (`REQ-OPS-074`), and the durable-store interaction health (`REQ-OPS-076`) — rather than on a person
  watching a screen. The conditions that constitute an incident are expressed against those signals.
- **acceptance_criteria**: Inspect what drives detection; each alerting condition names an observability
  signal and a threshold or state on it. Induce an elevated error rate, approaching saturation, and a
  store-interaction fault in turn; each is capable of being surfaced as a detected condition from its
  signal.
- **verification_method**: operational_check
- **release_gating**: true
- **traces_to**: REQ-PROD-040

#### REQ-OPS-082 — Incidents carry a proportionate severity
- **statement**: A detected incident is classified by a small severity scheme that at least distinguishes
  "the product is not serving its core loop" (a major incident) from "the product is degraded or partially
  impaired but still serving" (a minor incident), so that response and communication are proportionate to
  what is actually broken. The scheme is kept to the scale of a small hosted product.
- **acceptance_criteria**: Find the stated severity scheme; it defines at least a major and a minor level
  with a criterion for each expressed against the serving signal. Classify a total-outage case and a
  partial-degradation case; each maps to the intended level.
- **verification_method**: inspection
- **release_gating**: false
- **traces_to**: REQ-PROD-040

#### REQ-OPS-083 — A responsible operator is identified for incident response
- **statement**: There is a stated expectation of who is responsible for responding when an incident is
  detected — a role, not a staffed rotation — so that a fired alert has an owner rather than reaching no
  one. This is the operator of operator journey J9.
- **acceptance_criteria**: Find the stated responsibility; it names the role accountable for acknowledging
  and acting on a detected incident. A detected major incident has a defined responder; no detected incident
  is left with no one responsible for it.
- **verification_method**: inspection
- **release_gating**: true
- **traces_to**: REQ-PROD-040

#### REQ-OPS-084 — An incident has a defined response path
- **statement**: A detected incident has a defined response expectation — acknowledge, investigate using the
  observability signals and logs, communicate to users per the status requirements, and resolve — recorded
  so the responder follows a known path rather than improvising. The detailed step-by-step runbooks are
  deferred to later operational work; this requires that the response path exist and be written down.
- **acceptance_criteria**: Find the recorded incident-response expectation; it covers acknowledgement,
  investigation against the observability signals, user communication, and resolution. Walk a representative
  incident through it; each step has a defined owner and outcome.
- **verification_method**: inspection
- **release_gating**: false
- **traces_to**: REQ-PROD-040

#### REQ-OPS-085 — Users can learn that the product is down or degraded
- **statement**: When the product is unavailable or degraded, a person has a way to learn that chirp itself
  is affected — a status surface or an in-product notice — rather than being left to infer it from a
  failed action or a spinner. The notice states, at least, that the product is experiencing a problem.
- **acceptance_criteria**: With the product in an outage or degraded state, a user consulting the status
  surface or in-product notice sees that chirp is affected and is not left only with an unexplained failure.
  With the product serving normally, the surface shows normal operation.
- **verification_method**: manual_user_check
- **release_gating**: true
- **traces_to**: REQ-PROD-040

#### REQ-OPS-086 — The status surface does not depend on the failed product
- **statement**: The surface users consult to learn of an outage is reachable when the product itself is
  down — it does not depend on the serving path, the durable store, or the process that may be the thing
  that has failed. A status page that goes down with the product conveys nothing at the moment it is needed.
- **acceptance_criteria**: Take the serving product fully offline, including its durable store; the status
  surface is still reachable and reports the product as unavailable. The surface's availability does not
  require the product's serving path to be up.
- **verification_method**: operational_check
- **release_gating**: true
- **traces_to**: REQ-PROD-040

#### REQ-OPS-087 — Planned maintenance is announced in advance
- **statement**: When the operator plans maintenance that will make the product unavailable or degraded,
  users are given advance notice through the same status surface or in-product notice, stating the expected
  window, so a planned interruption is distinguishable to a user from an unexpected outage.
- **acceptance_criteria**: Schedule a maintenance window and publish the notice; before the window a user
  consulting the status surface sees the planned maintenance and its expected timing. During the window the
  interruption is presented as planned, not as an unexplained failure.
- **verification_method**: manual_user_check
- **release_gating**: false
- **traces_to**: REQ-PROD-040

#### REQ-OPS-088 — Status and incident communication carries no private or secret data
- **statement**: Nothing published on the status surface, in an in-product outage notice, or in a
  maintenance announcement contains private account data or secret material — no credential, session token,
  verified-contact value (`REQ-DOM-035`), nor internal secret such as a connection string or a stack trace
  that exposes them. Telling users about an outage never leaks the data the outage is around.
- **acceptance_criteria**: Inspect the content published for a representative outage and a representative
  maintenance notice; it describes product status in terms a user needs and contains no credential, session
  token, verified-contact value, connection string, or raw internal error detail that discloses private or
  secret data.
- **verification_method**: inspection
- **release_gating**: true
- **traces_to**: REQ-DOM-035

#### REQ-OPS-089 — Recovery is communicated when service returns
- **statement**: When a communicated incident is resolved and the product is serving again, the status
  surface or in-product notice reflects the recovery, so a user who saw the outage can tell that it is over
  rather than being left unsure whether the problem persists.
- **acceptance_criteria**: Communicate an outage, then resolve it and restore serving; the status surface
  updates to show the product operating normally. A user who saw the outage notice can see that service has
  recovered.
- **verification_method**: manual_user_check
- **release_gating**: false
- **traces_to**: REQ-PROD-040

#### REQ-OPS-090 — The product fails into its designed degraded states
- **statement**: When a dependency the product needs is unavailable in production — in particular the
  durable store (`REQ-DOM-115`) — the operated product presents the user the degraded and error experiences
  designed by the experience area (`REQ-UX-*`, `REQ-PROD-033`, `REQ-PROD-034`): an explained error, a
  preserved in-progress draft, a routed-to-sign-in on an expired session. This requirement is the
  operational join to those states; it does not define them.
- **acceptance_criteria**: In production, make the durable store unreachable while the serving process stays
  up; a user exercising the core loop meets an explained degraded or error state, not a blank page or a
  crashed process. The states a user sees are the ones the experience design specifies.
- **verification_method**: manual_user_check
- **release_gating**: true
- **traces_to**: REQ-PROD-033, REQ-PROD-034

#### REQ-OPS-091 — A partial failure is contained to the affected capability
- **statement**: When one capability is degraded rather than the whole product — for example the durable
  store is slow but reachable — the parts of the product that can still serve continue to do so, to the
  extent the product's design allows, rather than a single fault turning into a total outage.
- **acceptance_criteria**: Induce degradation in one capability (for example elevated store latency); the
  product continues to serve the surfaces that do not depend on the degraded capability, and the impact a
  user sees is scoped to the affected capability rather than a blanket failure.
- **verification_method**: operational_check
- **release_gating**: false
- **traces_to**: REQ-PROD-040, REQ-DOM-115

#### REQ-OPS-092 — A stated, proportionate availability target
- **statement**: The product states an availability target that defines what "reasonably available"
  (`REQ-PROD-040`) means for it — a figure proportionate to a small hosted service, expressed over a stated
  window (for example a monthly serving-availability target). The target is written down, not left implicit.
- **acceptance_criteria**: Find the stated availability target; it gives a specific availability figure and
  the window it is measured over, and it is proportionate to a small hosted product rather than an
  enterprise commitment.
- **verification_method**: inspection
- **release_gating**: true
- **traces_to**: REQ-PROD-040

#### REQ-OPS-093 — Availability is measured from the serving signal, not asserted
- **statement**: The availability target is measured in production from the serving/availability signal
  (`REQ-OPS-075`) over the stated window, so that whether the product met its target is a measured fact
  rather than a claim. Unavailability is counted when the serving signal shows the product not serving its
  core loop.
- **acceptance_criteria**: Over a measurement window that includes at least one serving interruption,
  compute availability from the serving signal; the result reflects the observed interruption and can be
  compared against the stated target to say whether it was met.
- **verification_method**: operational_check
- **release_gating**: true
- **traces_to**: REQ-PROD-040

#### REQ-OPS-094 — Announced maintenance is accounted for in availability
- **statement**: Availability measurement distinguishes announced planned maintenance (`REQ-OPS-087`) from
  unplanned outage, so that routine, pre-announced deploys and maintenance do not register as unplanned
  unavailability against the target.
- **acceptance_criteria**: Take the product down during an announced maintenance window and, separately,
  during an unplanned incident; the availability accounting attributes the first to planned maintenance and
  the second to unplanned unavailability, per the stated rule.
- **verification_method**: inspection
- **release_gating**: false
- **traces_to**: REQ-PROD-040

#### REQ-OPS-095 — A stated time-to-restore-serving objective for incidents
- **statement**: Incident response works to a stated objective for how quickly serving is restored after a
  detected outage, consistent with the availability target (`REQ-OPS-092`). This is time-to-restore
  serving; it is distinct from the data recovery-time objective owned by backups and recovery
  (`REQ-OPS-020..039`), which concerns restoring lost data rather than resuming service.
- **acceptance_criteria**: Find the stated time-to-restore-serving objective; it gives a target duration
  from detection to restored serving and is consistent with the availability target. For a representative
  resolved incident, the time from detection to restored serving is measurable against it.
- **verification_method**: operational_check
- **release_gating**: false
- **traces_to**: REQ-PROD-040
