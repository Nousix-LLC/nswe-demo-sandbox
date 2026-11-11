## existing_followups

Three open items already sit on the board as non-release-gating hardening and polish, not as release
requirements. They are folded here into the operational-readiness section each belongs to, so a reader meets
each one next to the requirements it bears on rather than as a free-floating backlog entry. None of the three
gates the release: each is work that improves an already-releasable posture, and the substance each touches is
already carried by existing `REQ-OPS-*` requirements above. They are recorded here and **not** re-minted as new
requirements.

| Follow-up | Subject | Folded into | Already covered by | Release-gating |
|-----------|---------|-------------|--------------------|----------------|
| #23 | Harden and exercise the native install path | `observability` | `REQ-OPS-060`, `REQ-OPS-061`, `REQ-OPS-066`, `REQ-OPS-068`, `REQ-OPS-072`, `REQ-OPS-075` | No |
| #24 | Least-privilege delivery RBAC + supply-chain hardening | `limits_and_quotas` | (delivery/control-plane posture; no owning `REQ-OPS-*`) | No |
| #25 | Containerize follow-ups (non-blocking polish) | `durable_data` | `REQ-OPS-001`, `REQ-OPS-002`, `REQ-OPS-003`, `REQ-OPS-004` | No |

**#23 — harden and exercise the native install path → `observability`.** Exercising the install path end to end
is where the operational-visibility requirements are first confirmed wired in a real deployment: the
readiness signal and its store-reachability meaning (`REQ-OPS-060`, `REQ-OPS-061`), the structured logs
(`REQ-OPS-066`, `REQ-OPS-068`), the serving and request/error metrics (`REQ-OPS-072`), and the
serving/availability signal the incident posture builds on (`REQ-OPS-075`). Those requirements already fix
that the signals must exist and be observable; #23 is the non-gating work of hardening and exercising the
install path so they are demonstrably observable in a running deployment. It is hardening on top of a met
requirement, not a new requirement, and it does not gate the release.

**#24 — least-privilege delivery RBAC + supply-chain hardening → `limits_and_quotas`.** #24 bounds who and what
may change the *running system* through the delivery and control plane — a privileged, operator- and
automation-facing access posture. It is folded into `limits_and_quotas` as that section's
operational-security neighbour, but it is deliberately distinct in subject from the requirements that section
owns: `REQ-OPS-040..048` bound *public clients'* request rate, payload size, and created volume, whereas #24
bounds *privileged control-plane actors*. It is also distinct from the operator audit trail
(`REQ-OPS-077..079`), which records actions taken through the product's own administrative surface rather than
governing delivery-plane access. Because its subject is the delivery and control plane rather than the
product's own request surface, no `REQ-OPS-*` owns it; it is recorded here as non-gating hardening and is not
minted as a new requirement.

**#25 — containerize follow-ups (non-blocking polish) → `durable_data`.** The remaining containerization polish
bears on the deploy and redeploy posture the durable-data section states as operated properties: that a
restart, redeploy, and upgrade lose no user data (`REQ-OPS-001`), that authoritative state is operated in a
durable store distinct from the serving process (`REQ-OPS-002`), that replacing the serving process touches no
user data (`REQ-OPS-003`), and that an operated upgrade preserves existing data (`REQ-OPS-004`). Those
requirements already fix the durability properties a deploy must preserve; #25 is non-blocking polish on the
containerization path on top of them. It does not gate the release and is not a new requirement.
