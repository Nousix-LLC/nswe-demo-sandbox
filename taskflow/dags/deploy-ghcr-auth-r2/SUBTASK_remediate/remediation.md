# remediation.md — SUBTASK_remediate (deploy-ghcr-auth-r2)

**Transform stage of the serial pipeline** (diagnose → remediate → verify_synthesis). This record states
what the change stage did — and, on the branch selected, why **no change was warranted** — so the
verification gate is input-complete. It does **not** render the AC1–5 verdict (the change/verify split;
that is `SUBTASK_verify_synthesis`'s job).

## Decision branch acted on

**`decision_branch = already-working`** (from `../SUBTASK_diagnose/diagnosis.md`).

Per the brief's already-working rule: *no cluster change and no PR are needed; confirm the convergence you
were handed and record that desired state is already met; do not manufacture a change.* That is exactly
what was done. **No change was invented to justify this stage.**

## Action taken

**None that mutates state.** Specifically:

- **No Secret created** — the least-privilege `ghcr-pull` docker-registry Secret already exists in ns `chirp`
  (created out-of-band by the owner ~31h ago); there was nothing to create.
- **No drift reconciled** — ArgoCD reports `Synced` at the committed revision; live == desired, so there was
  no drift to close.
- **No ReplicaSet scaled** — the stale `chirp:local` RS was already at `0/0/0`; nothing to scale.
- **No committed-manifest change / no PR opened** — `diagnosis.md` reports `repo_change_needed = false`. The
  `ghcr-pull` Secret is out-of-band and must never be committed; `c805525` already carries the host-less
  ingress rule; the committed digest pin is current. There is no repository change for this stage to make,
  therefore **no PR** on `work/deploy-ghcr-auth-r2`. (Per the ownership manifest, a PR exists *iff* a repo
  change is genuinely needed — it is not.)

Because **no repository change was opened**, there is no PR body, no branch/commit from this stage, and the
`Closes #32` question does not arise here (it is verdict-gated to `SUBTASK_verify_synthesis` regardless).

## Independent read-only confirmation (not a verdict)

To avoid declaring "no change needed" on stale input, I re-read the live world read-only (via SSH to the
build server per the repo checkout's `CLAUDE.md`, context `k3d-nswe`, ns `chirp`/`argocd`). I did **not**
re-diagnose from scratch, did **not** trigger a reconcile, and did **not** run the full AC suite — those are
the gate's to execute. Observed, consistent with the diagnosis:

| Fact confirmed (read-only) | Observation |
|---|---|
| Committed-digest pod | `chirp-server-bbff68f5b-22spd` — `Running`, `1/1`, 0 restarts, ~31h, IP `10.42.1.10` |
| Running image digest | `ghcr.io/nousix-llc/chirp-server@sha256:054af27f588c13aeebd8698dbddf690e15bf75cd36c9a087b38763fd0902abe3` = committed pin in `deploy/chirp/10-deployment.yaml@c805525` |
| Stale local-image RS | `chirp-server-f6476ccff` — `DESIRED=0 CURRENT=0 READY=0` (not an endpoint) |
| `ghcr-pull` Secret | present in ns `chirp`, type `kubernetes.io/dockerconfigjson`, 1 data key, ~31h |
| Service endpoints | `chirp-server` → only `10.42.1.10:8080` (the digest pod); no stale masking |
| ArgoCD `Application chirp` | `Synced`, revision `c805525`, `targetRevision: main`, `Healthy` |

This is confirmation evidence for the gate, **not** an AC pass/fail declaration.

## Contract identities (`../contracts/_MANIFEST.yaml`) touched by this action

My action was a no-op change, so I **mutated no identity and broke none**. Relative to each identity:

- **I1 (digest running / stale RS at 0)** — confirmed already satisfied read-only; no action required.
- **I2 (ArgoCD Synced + Healthy at head)** — confirmed already satisfied read-only; integration-branch head
  == `main@c805525` (no repo change ⇒ `work/deploy-ghcr-auth-r2` carries nothing beyond `c805525`).
- **I5 (supply-chain / least-privilege posture)** — **preserved by construction**: no digest/pin change, no
  registry secret committed (none created at all — the Secret pre-exists out-of-band), no broad RBAC added,
  AppProject scope untouched (the Secret kind stays excluded from the whitelist ⇒ unmanaged, selfHeal-safe).
- **I6 (single endpoint, no stale masking)** — confirmed already satisfied read-only.
- **I3 (per-route /healthz 200 from the digest pod)** and **I4 (selfHeal/prune survival)** — **left for the
  gate to execute**. This stage is a no-op change and does not curl both routes exhaustively or trigger a
  reconcile rehearsal; `diagnosis.md` already observed both routes at 200 and reasoned the Secret is
  structurally prune-safe. The gate owns the executed AC3/AC4 checks.
- **I7 (no host facts on GitHub)** — nothing was posted to GitHub by this stage (no PR, no commit, no
  comment), so there is no GitHub surface to leak host facts; vacuously preserved.

## Posture / constraint compliance

- No secret committed to the repo; none created (pre-existing out-of-band). ✔
- No `main` force-push or history rewrite; no branch created or pushed by this stage. ✔
- No attribution trailers (no commit/PR authored). ✔
- Scope stayed within ns `chirp*` and ArgoCD Application `chirp`; read-only only. ✔
- Digest pin unchanged, AppProject scope unchanged, no RBAC added. ✔
- `Closes #32` not added (verdict-gated, and no PR exists). ✔

## Handoff to `SUBTASK_verify_synthesis`

Desired state is already met; nothing was changed. The gate should now **execute** (not merely re-read) the
checks this read-only stage deliberately deferred:

1. **AC3** — curl `/healthz` on **both** ingress routes (host-less tailnet address, any Host; and
   `Host: chirp.localhost`) and correlate the serving pod to the digest pod `10.42.1.10` (trivially the only
   endpoint, but execute for independent evidence).
2. **AC4** — trigger/await an ArgoCD reconcile and confirm the digest Deployment **and** the out-of-band
   `ghcr-pull` Secret persist (Secret survives because its kind is excluded from the AppProject whitelist).
3. Finalize the `SYNTHESIS.md` fold; decide `Closes #32` wording **iff** live reachability is verified. No PR
   exists to amend — if the gate concludes a repo change is still unnecessary, `#32` is closed (or not) per
   the overseer's merge, not via a remediation PR from this stage.

**Status: completed — no change needed (already-working / already converged).**
