# NSWE Sandbox — a Nousix taskflow, reconstructed

> **Display only.** This repository is a frozen, read-only snapshot of one NSWE engagement's
> on-disk **taskflow** — the artifact the Nousix OS leaves on the filesystem as it runs. It is here
> to be read, not run; it is not a runtime.

**What it shows:** Nousix does not run an *agent loop* or an *agent graph*. It runs a **process
graph**, and *the files on disk are that graph*. A single serial **overseer thread** evaluates the
project board each turn and **forks** DAGs — a code build, a review, a design; each DAG decomposes
into its own subtree; every node leaves its lifecycle records. Nothing orchestrates from memory: the
scheduler can reconstruct the entire run from these files alone.

## The run, reconstructed

Below is this engagement as rebuilt by Core's **dry-run reconstructor** — `nousix resume --dry-run`,
which walks the on-disk tree and reassembles the actor graph with **zero model calls**. This is its
output: the serial overseer thread and every DAG it forked, in fork order.

```text
nousix resume --dry-run  (reconstruct thread + forks; no claude -p dispatched)
  request_id:       nswe-demo
  actors:           102   (1 thread + 101 forked DAGs)
  forked actors:    101
  live nodes:       1017
  max-dag:          1   (at most one forked DAG driven at once; rest queued in fork order)

overseer  [root, thread]  COMPLETED  (428 serial nodes  I0…I426)
├── ferric-foundation            [fork, DAG]  COMPLETED  (6 nodes)
├── review-ferric-foundation     [fork, DAG]  COMPLETED  (1 node)
├── ferric-http                  [fork, DAG]  COMPLETED  (1 node)
├── review-ferric-router         [fork, DAG]  COMPLETED  (1 node)
├── review-ferric-http           [fork, DAG]  COMPLETED  (1 node)
├── review-chirp-types           [fork, DAG]  COMPLETED  (1 node)
├── ferric-http-relock-r1        [fork, DAG]  COMPLETED  (1 node)
├── review-chirp-frontend        [fork, DAG]  COMPLETED  (1 node)
├── chirp-server                 [fork, DAG]  COMPLETED  (11 nodes)
├── review-chirp-server          [fork, DAG]  COMPLETED  (6 nodes)
├── chirp-server-relock-r1       [fork, DAG]  COMPLETED  (1 node)
├── ci-actions                   [fork, DAG]  COMPLETED  (1 node)
├── containerize                 [fork, DAG]  COMPLETED  (1 node)
├── review-containerize          [fork, DAG]  COMPLETED  (10 nodes)
├── remediate-ci-actions         [fork, DAG]  COMPLETED  (1 node)
├── review-ci-actions-r3         [fork, DAG]  COMPLETED  (1 node)
├── review-deploy-argocd         [fork, DAG]  COMPLETED  (1 node)
├── deploy-ghcr-auth             [fork, DAG]  FAILED     (1 node)
├── review-deploy-ghcr-auth      [fork, DAG]  COMPLETED  (1 node)
├── review-ci-actions-r2         [fork, DAG]  COMPLETED  (6 nodes)
├── review-epic-persist          [fork, DAG]  COMPLETED  (14 nodes)
├── deploy-argocd                [fork, DAG]  COMPLETED  (9 nodes)
├── infra-bootstrap              [fork, DAG]  COMPLETED  (5 nodes)
├── deploy-ghcr-auth-r2          [fork, DAG]  COMPLETED  (4 nodes)
├── chirp-types                  [fork, DAG]  COMPLETED  (3 nodes)
├── chirp-frontend               [fork, DAG]  COMPLETED  (7 nodes)
├── review-infra-bootstrap       [fork, DAG]  COMPLETED  (5 nodes)
├── ferric-router                [fork, DAG]  COMPLETED  (6 nodes)
├── design-chirp-r1              [fork, DAG]  COMPLETED  (105 nodes)
├── design-ferric-1_0            [fork, DAG]  COMPLETED  (38 nodes)
├── remediate-epic-persist-r1    [fork, DAG]  COMPLETED  (8 nodes)
├── review-ci-actions            [fork, DAG]  COMPLETED  (1 node)
├── remediate-epic-persist-r1b   [fork, DAG]  COMPLETED  (1 node)
├── design-ferric-1_0-r2         [fork, DAG]  COMPLETED  (18 nodes)
├── remediate-epic-persist-r1c   [fork, DAG]  COMPLETED  (1 node)
├── review-epic-persist-r2       [fork, DAG]  COMPLETED  (1 node)
├── design-ferric-1_0-r3         [fork, DAG]  COMPLETED  (9 nodes)
├── remediate-design-ferric-1_0-r1 [fork, DAG]  COMPLETED  (1 node)
├── pin-image-digest-r1          [fork, DAG]  COMPLETED  (1 node)
├── review-design-ferric-1_0-r4  [fork, DAG]  COMPLETED  (1 node)
├── security-persist-r1          [fork, DAG]  COMPLETED  (4 nodes)
├── sweep-seam-r1                [fork, DAG]  COMPLETED  (1 node)
├── review-security-persist-r1   [fork, DAG]  COMPLETED  (1 node)
├── sweep-seam-r1-r1             [fork, DAG]  COMPLETED  (1 node)
├── review-sweep-seam-r1         [fork, DAG]  COMPLETED  (1 node)
├── update-cronjob-digest-r1     [fork, DAG]  COMPLETED  (1 node)
├── review-update-sweep-digest-r1 [fork, DAG]  COMPLETED  (1 node)
├── ferric-epic-authoring-r1     [fork, DAG]  COMPLETED  (17 nodes)
├── review-ferric-epic-authoring-r1 [fork, DAG]  COMPLETED  (1 node)
├── ferric-async-forms-r1        [fork, DAG]  COMPLETED  (6 nodes)
├── ferric-router-r1             [fork, DAG]  COMPLETED  (7 nodes)
├── ferric-async-forms-r2        [fork, DAG]  COMPLETED  (1 node)
├── review-ferric-router-r1      [fork, DAG]  COMPLETED  (1 node)
├── review-ferric-async-forms-r2 [fork, DAG]  COMPLETED  (1 node)
├── ferric-router-r2             [fork, DAG]  COMPLETED  (4 nodes)
├── ferric-router-r3             [fork, DAG]  COMPLETED  (1 node)
├── review-ferric-router-r3      [fork, DAG]  COMPLETED  (1 node)
├── update-chirp-server-digest-r1 [fork, DAG]  COMPLETED  (1 node)
├── review-update-chirp-server-digest-r1 [fork, DAG]  COMPLETED  (6 nodes)
├── ferric-http-r1               [fork, DAG]  COMPLETED  (1 node)
├── review-ferric-http-r1        [fork, DAG]  COMPLETED  (1 node)
├── ferric-http-r2               [fork, DAG]  COMPLETED  (1 node)
├── review-ferric-http-r2        [fork, DAG]  COMPLETED  (12 nodes)
├── ferric-ssr-r1                [fork, DAG]  COMPLETED  (6 nodes)
├── ferric-ssr-r2                [fork, DAG]  COMPLETED  (1 node)
├── ferric-ssr-r3                [fork, DAG]  COMPLETED  (1 node)
├── review-ferric-ssr-r1         [fork, DAG]  COMPLETED  (25 nodes)
├── ferric-ssr-r4                [fork, DAG]  COMPLETED  (3 nodes)
├── ferric-async-forms-r3        [fork, DAG]  COMPLETED  (5 nodes)
├── chirp-public-landing-r1      [fork, DAG]  resolved   (1 node)
├── review-ferric-ssr-r2         [fork, DAG]  COMPLETED  (33 nodes)
├── review-ferric-async-forms-r3 [fork, DAG]  COMPLETED  (31 nodes)
├── chirp-logged-out             [fork, DAG]  SUSPENDED  (13 nodes)
├── chirp-logged-out-r2          [fork, DAG]  COMPLETED  (4 nodes)
├── chirp-logged-out-r3          [fork, DAG]  COMPLETED  (2 nodes)
├── chirp-logged-out-r4          [fork, DAG]  COMPLETED  (11 nodes)
├── chirp-logged-out-r5          [fork, DAG]  SUSPENDED  (2 nodes)
├── chirp-logged-out-r6          [fork, DAG]  COMPLETED  (1 node)
├── chirp-logged-out-r7          [fork, DAG]  COMPLETED  (13 nodes)
├── chirp-logged-out-r8          [fork, DAG]  COMPLETED  (4 nodes)
├── chirp-logged-out-r9          [fork, DAG]  COMPLETED  (1 node)
├── chirp-logged-out-r10         [fork, DAG]  COMPLETED  (1 node)
├── chirp-logged-out-r11         [fork, DAG]  COMPLETED  (1 node)
├── chirp-logged-out-r12         [fork, DAG]  COMPLETED  (4 nodes)
├── chirp-logged-out-r13         [fork, DAG]  COMPLETED  (1 node)
├── chirp-logged-out-r14         [fork, DAG]  COMPLETED  (1 node)
├── chirp-logged-out-r15         [fork, DAG]  COMPLETED  (1 node)
├── chirp-logged-out-r16         [fork, DAG]  COMPLETED  (1 node)
├── chirp-logged-out-r17         [fork, DAG]  COMPLETED  (1 node)
├── chirp-logged-out-r18         [fork, DAG]  COMPLETED  (1 node)
├── chirp-logged-out-r19         [fork, DAG]  COMPLETED  (3 nodes)
├── chirp-logged-out-r20         [fork, DAG]  COMPLETED  (1 node)
├── chirp-logged-out-r21         [fork, DAG]  COMPLETED  (1 node)
├── chirp-logged-out-r22         [fork, DAG]  COMPLETED  (1 node)
├── chirp-logged-out-r23         [fork, DAG]  COMPLETED  (1 node)
├── chirp-logged-out-r24         [fork, DAG]  COMPLETED  (1 node)
├── chirp-logged-out-r25         [fork, DAG]  COMPLETED  (1 node)
├── chirp-logged-out-r26         [fork, DAG]  COMPLETED  (1 node)
├── review-chirp-logged-out-r1   [fork, DAG]  COMPLETED  (36 nodes)
├── chirp-logged-out-r27         [fork, DAG]  COMPLETED  (1 node)
└── review-chirp-logged-out-r2   [fork, DAG]  COMPLETED  (9 nodes)
```

*(1 `FAILED`, 2 `SUSPENDED`, the rest `COMPLETED` — reconstructed as they actually landed, not idealized.)*

## Reading it

- **`overseer [root, thread]`** → `taskflow/overseer/I0 … I426`: the serial overseer thread, one
  directory per turn (a thread node). It evaluates the board and decides what to fork next —
  zero-token while idle.
- **`<name> [fork, DAG]`** → `taskflow/dags/<name>/`: a forked DAG, one unit of work. Each has a
  `_GLOBAL.md` hub and decomposes into `SUBTASK_*` children, recursively (up to 13 levels deep here).
- **`<state> (<n> nodes)`**: the actor's terminal state and live node count, exactly as the
  reconstructor reports per actor.
- **`max-dag: 1`**: at most one forked DAG is driven at a time; the rest queue in fork order.

## The files *are* the DAG

Every node leaves the same on-disk lifecycle records, and the live engine state is only a cache of them:

| File | Meaning |
|---|---|
| `_BRIEF.md` | the node's task — what it was asked to do |
| `_GLOBAL.md` | a decomposition hub — a parent that split into children |
| `_FORK.md` | a forked root prompt — a new isolated DAG |
| `SYNTHESIS.md` | the fold — a parent validating and folding its children's outputs (a verification gate) |
| `COMPLETE.md` / `FAILURE.md` / `SUSPENSION.md` | terminal state |

Open any `taskflow/dags/<name>/` to see a real decomposition; open
`taskflow/overseer/I<n>/_BRIEF.md` to see the thread's reasoning at that turn.

## Not included

The DAG nodes checked out and compiled real code — the **chirp** app on the **ferric** Rust/WASM
framework. Those git clones and their `cargo` build output are omitted (regenerable, ~8 GB); the code
itself lives in **[`Nousix-LLC/nswe-demo`](https://github.com/Nousix-LLC/nswe-demo)**. What remains
here is the taskflow: the briefs, the decomposition, the syntheses, the lifecycle.
