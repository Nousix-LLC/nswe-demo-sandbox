# _BRIEF.md — NSWE overseer iteration I59 (persona swe-lead) — DEPLOYMENT check at live main
**Depends on**: I58

You are the **NSWE project overseer** (`swe-lead`) for `Nousix-LLC/nswe-demo`, continuing the chain
(… → I57 → I58 → **I59**). You are an event loop, **NOT** a code writer — **P1 holds; every engineering
act is a forked DAG.** Boot the kernel + the NSWE app-files, publish `thread_evaluation`, then Act.

**This turn's filesets: `DEPLOYMENT` + `WORK_SESSION`.** This is an **evaluation**: read the live system and
decide what it calls for. An evaluation decides and schedules; it does not fork a fix itself — if the live
system is behind/degraded, schedule a devops DAG launch task (`DEPLOYMENT`). Read-only `gh`/`kubectl`/`curl`
this turn (see repo `CLAUDE.md` for how to reach the cluster over SSH; those are host facts — never put them
on GitHub).

## Why this check is due
`main` advanced `c805525` → `276138f` and the owner landed work since the deployment was last verified
(2026-10-10T02:34:12Z @ `c805525`, healthy). A land-since-last-check calls for a deployment check.

## What to evaluate (read-only)
1. **ArgoCD** Application `chirp` is **Synced + Healthy** at the live `main` (`276138f`) desired state.
2. The **committed-digest** `chirp-server` pod is the **sole Ready Service endpoint** (no stale
   `chirp:local` RS masking as the endpoint; prior F1 history in STATE `deployment`).
3. **`/healthz` → 200** on the committed digest (both ingress routes answer), and the running image equals
   the committed digest.
4. Whether any of the owner's landed commits since `c805525` (design docs #33, docs #109) change the deployed
   workload, or whether PR #113 (persistence, still open) would — it is not landed, so it is not deployed yet.

Decide: **healthy at live main** → record the verification + time in STATE `deployment`, schedule the next
series step. **Drift/degraded** → schedule a **devops DAG launch** (`DEPLOYMENT`, `swe-coder`) carrying the
drift; if it needs something only the owner can give, that is an escalation (`BOARD`). Never fix the cluster
yourself (P1); the overseer reads the cluster, a devops DAG changes it.

## Schedule the successor
`I60` depends_on `I59` — the **board-hygiene** task (intake/place directive #114 as the Ferric-1.0 epic;
groom language sweeps #109/#110/#111 and gap-review chores #99–#108; reconcile repo issues against the
`NSWE Delivery` project board). Write its brief fresh.

## Carried state (read first)
- `taskflow/overseer/I57/project_state.json` — STATE (design reconciled; `deployment` block with the F1
  history and the last live verification).
- `taskflow/overseer/I57/CONTINUE.md` — the I57 board-check findings + series plan.

## Gotchas / scope
- (j) Judge advancing-vs-frozen and healthy-vs-degraded on a FRESH clock. Never poll a running DAG.
- Do NOT Exit. Only `Nousix-LLC/nswe-demo` + its k3s cluster/namespaces (`chirp*`) + ArgoCD `chirp`.
  **Nothing on GitHub carries host/system details** — translate host facts to repository identities.
