# SYNTHESIS — review-infra-bootstrap · SUBTASK_synthesis_gate

Verification-gate fold record for the review-infra-bootstrap subtree (the authoritative human-landing
observation seam for PR #20 / #10). Run **cold** over the three review-lens spokes' COMPLETED outputs
against the frozen review contract `contracts/_MANIFEST.yaml` + `contracts/finding_schema.md`. This is a
**gate, not a prose summary**: it asserts the contract identities R1–R7 over the combined output and emits a
single verdict consistent with the consolidated finding set. No failing identity is silently plugged.

## Verdict
**verdict: APPROVE**
round: 1

APPROVE is the review judgment on the PR #20 diff (`016bd44`, +912/−0 across 11 files under
`deploy/bootstrap/`): **zero open `block` findings**, and the single open `major` (CORR-1) is explicitly
dispositioned as **non-land-blocking** (must-fix-before-relying-on-native). Per the contract `verdict_rule`
(REQUEST-CHANGES **iff** ≥1 open block; APPROVE requires zero open block + an explicit call on every open
major), the verdict is APPROVE.

> **Observed landing state (GATE-1, recorded for honesty).** At gate run time PR #20 is already **MERGED**
> (not OPEN, as the review DAG planned) and remote `main` has advanced `fcfc7a2` → `61f924af` (the merge
> commit). This gate is a resumed/reconstructed node; the landing occurred out-of-band between planning and
> this fold. The review verdict is a judgment on the **immutable diff `016bd44`** and is therefore unaffected
> by the merge; an already-merged PR is **consistent with** this APPROVE outcome (no contradiction to flag as
> a defect). The merge was **not** performed by any task in this review subtree (R7 below).

## Checks (four-check posture, adapted to a review fold — over *review coverage*, not compiled artifacts)
| Check | Result | Evidence | Notes |
|---|---|---|---|
| Concern coverage (≡ wiring) | pass | All 8 named concerns each covered by exactly one lens output; none unowned, none double-owned (R1 table). | 3 lens docs, disjoint ownership. |
| Finding consolidation + well-formedness (≡ contract) | pass | 15 lens findings + F1 merged into one per-severity list; each carries all `finding_schema.md` fields; CORR-1 (major) carries actionable remediation (R3). | 1 major, 7 minor, 7 nit, 0 block. |
| AC assembly (≡ duplication/coverage) | pass | AC1..AC4 each carry an explicit pass/fail computed from the union of findings touching them (R2 checklist). | 4/4 PASS. |
| Cross-cutting adjudication + review (≡ code-review) | pass | Single k3d verdict (R4) and single F1 disposition (R5) rendered; verdict consistent with finding set (R6); review-only honored (R7). | k3d acceptable; F1 carry. |

## Consolidated findings (per severity, merged from the three lens docs + gate cross-read)

### block (0)
_None._ No lens raised a block-severity finding; the gate cross-read surfaced none.

### major (1)
- **[CORR-1]** severity=major concern=reproducibility_idempotency lens=correctness
  location=`cluster/install-k3s.sh:61–65` (`install_native`) · acceptance_criteria_touched=[AC1_cluster, AC4_runbook]
  statement: In NATIVE mode on a non-root host the pinned k3s version is silently dropped — the command
  expands to `INSTALL_K3S_VERSION="$K3S_VERSION" sudo sh -s - server …`, and the `VAR=val` prefix sets the
  variable in *sudo's own* environment, which default sudoers `env_reset` does not forward to the `sh` sudo
  runs; the cluster comes up at an unpinned (`latest`) version.
  evidence: `install-k3s.sh:61` `sh_pfx="sudo"` path + `:63–65` the piped install; sudoers(5) `env_reset`
  default. Latent — the native path was not exercised on this (k3d) host; `verify-cluster.sh` prints but does
  not assert the version (CORR-2), so it would not catch the drift.
  remediation: pass the version inside the privileged shell — `… | $sh_pfx env INSTALL_K3S_VERSION="$K3S_VERSION" sh -s - server …` or `sudo --preserve-env=INSTALL_K3S_VERSION`.
  **gate disposition: NON-LAND-BLOCKING (carry as must-fix-before-native-reliance follow-up).** Rationale:
  the native path is transparently documented as *unexercised/carried-for-a-privileged-host*, and #10's
  mandate ("stand up and **prove** the environment") is satisfied via the genuine, proven-Ready k3d cluster —
  so the defect does not falsify the landed, proven deliverable. It is nonetheless a real silent
  reproducibility break on the production-target path and MUST be fixed before native mode is relied upon;
  the fix is one line. It does not meet the "must fix before land" bar for a k3d-proven #10.

### minor (7)
- **[CORR-2]** concern=script_correctness lens=correctness · location=`verify-cluster.sh:49–50`, `verify-argocd.sh:60–62` · AC=[AC1,AC2,AC4] — verification proves readiness genuinely but *prints* rather than *asserts* the pinned version; a version-drifted install (incl. the CORR-1 case) would still report PASS. Remediation: assert observed version/image contains the pin.
- **[CORR-3]** concern=code_quality_shell_k8s_gitops_idiom lens=correctness · location=`install-k3s.sh:72` · AC=[AC1,AC4] — k3d existence probe greps compact JSON (`"name":"…"`); correct on pinned k3d v5.9.0, brittle if k3d pretty-prints (idempotency would break on a k3d bump). Remediation: `k3d cluster get "$CLUSTER_NAME"`.
- **[SEC-1]** concern=security_secrets_posture lens=security · location=`install-k3s.sh:62,65` · AC=[AC1,AC2] — native-mode kubeconfig written `--write-kubeconfig-mode 0644` (world-readable admin cred); native-only, documented "tighten for shared hosts"; rises to major on a shared/multi-tenant host. Remediation: default `0600`, gate `0644` behind explicit opt-in.
- **[SEC-2]** concern=least_privilege_rbac_cluster_posture lens=security · location=`install-argocd.sh:62` + `gitops/README.md:107–128` · AC=[AC2] — stock ArgoCD `application-controller` carries a `*/*/*` (cluster-admin-equivalent) ClusterRole; applied unmodified, namespace-isolated, zero Applications at bring-up. Must be scoped **before #13's first Application**. Remediation: scope apiGroups/resources + AppProjects, or namespace-install.yaml.
- **[SEC-3]** concern=security_secrets_posture lens=security · location=`install-k3s.sh:63–65`, `install-argocd.sh:41,62` · AC=[AC1,AC2] — remote installers HTTPS + version-pinned but not digest-/checksum-pinned and not signature-verified (ArgoCD manifest pinned to a movable git **tag**, images by tag not digest). Upstream-recommended paths; low risk. Remediation: pin manifest by commit SHA + images by `@sha256:`; cosign verify at admission (#13-era).
- **[HSO-1]** concern=honest_blocker_k3d_substitution lens=honesty_scope_ops · location=`install-k3s.sh:59–67` + `cluster/README.md:59–69` · AC=[AC1] — NATIVE systemd path is shipped but **unproven** on the sandbox host, and a durable #13 app deploy needs a persistent/privileged cluster the ephemeral k3d instance does not provide. Honest forward-dependency, not a landed defect. Remediation: tracked issue to exercise native on a privileged host + provision a durable #13 target.
- **[HSO-2]** concern=operability lens=honesty_scope_ops · location=`deploy/bootstrap/README.md:57–70` vs `verify-cluster.sh:23` · AC=[AC4] — unified runbook's verify step omits the native-mode `KUBE_CONTEXT=default` (+ `KUBECONFIG`) note while `verify-cluster.sh` defaults context to `k3d-nswe`; a native-path newcomer hits a confusing context failure. Remediation: add a one-line native-mode note / pointer.

### nit (7)
- **[CORR-4]** `build-chirp-wasm.sh:89` — post-build sanity note greps wrong token (`as default` vs `export default`); misleading diagnostic only, never fails. AC=[AC3].
- **[CORR-5]** `install-k3s.sh:63` — `curl -sfL` omits `-S`, suppressing curl error text (exit still propagates under `-f`+pipefail). AC=[AC1].
- **[CORR-6]** `verify-cluster.sh:40` — `kubectl wait … --all` vacuously satisfied on zero nodes; fully backstopped by the downstream CoreDNS-Running gate, so net verification stays genuine. AC=[AC1].
- **[CORR-7]** gitops vs cluster/wasm scripts — logging idiom inconsistent (stdout `echo` vs stderr `printf`). AC=[].
- **[SEC-4]** `install-argocd.sh:62` — `--force-conflicts` re-run silently reverts any out-of-band narrowing of the SEC-2 ClusterRole back to stock `*/*/*`. AC=[AC2]. (Keep `--force-conflicts`; express hardening as GitOps-managed overlay.)
- **[SEC-5]** `install-k3s.sh:48,69–88` — k3d mode requires Docker-group membership (root-equivalent on host); security consequence of the substitution only. AC=[AC1].
- **[HSO-3]** PR #20 body verification table — Cluster row not inline-annotated "(k3d mode on this host)"; full disclosure is in the caveat section just below, so not misleading in context. AC=[AC1].

### gate-level (1)
- **[GATE-1]** severity=nit concern=(cross-cutting / provenance) lens=gate
  location=PR #20 state vs review-DAG plan · acceptance_criteria_touched=[]
  statement: PR #20 was observed **MERGED** at gate run time (review DAG planned for OPEN), with `main`
  advanced `fcfc7a2` → `61f924af`. The gate is a resumed/reconstructed node; landing occurred out-of-band.
  evidence: `gh pr view 20 --json state` → `"MERGED"`; `git ls-remote origin main` → `61f924af…` (≠ the code
  DAG's recorded base `fcfc7a2`). Checkout clean, still on `work/infra-bootstrap` @ `016bd44`.
  disposition: informational only. The verdict is a judgment on the immutable diff `016bd44` and is
  consistent with the merge (an approvable PR was landed). The merge was not a write by any subtree task
  (R7). No defect in the PR; recorded for audit honesty, not remediated.

**Gate cross-read note (no new defect).** The cross-read surfaced no finding beyond those the lenses already
own. It surfaced one *convergence*: three lenses independently flag the **native install path** as the weak
spot (CORR-1 latent pin bug, SEC-1 `0644` kubeconfig, HSO-1 unproven) — consolidated into the single
"harden/exercise native before relying on it" follow-up below, strengthening but not re-minting those
findings.

## Acceptance-criteria checklist (R2 — each computed from the union of findings touching it)
| AC | Verdict | Findings touching | Evidence / reasoning |
|----|---------|-------------------|----------------------|
| **AC1_cluster** (k3s installed + proven Ready; versions recorded) | **PASS** | CORR-1(maj), CORR-2, CORR-3, SEC-1, SEC-3, HSO-1 + nits CORR-5/6, SEC-5, HSO-3 | Genuine k3s proven Ready via k3d (identical pin `v1.35.5+k3s1`, real `kubectl wait`+CoreDNS gate, fail-closed); versions in `versions.txt`. The only major (CORR-1) affects the **unexercised native path**, not the proven path → non-blocking. No block/major blocks the proven-Ready claim. |
| **AC2_gitops** (ArgoCD own-namespace + healthy; access documented, runtime-retrieved, never staged) | **PASS** | CORR-2, SEC-1, SEC-2, SEC-3 + nit SEC-4 | ArgoCD isolated in `argocd` ns, proven healthy (`verify-argocd.sh` genuine), ClusterIP-closed-by-default + stock NetworkPolicies; admin credential + kubeconfig runtime-retrieved, independent secret scan clean. Open items (SEC-2 `*/*/*`, SEC-3 pinning) are minor pre-#13 hardening, none blocking. |
| **AC3_wasm** (wasm32 + wasm-bindgen PROVEN building chirp-frontend; CLI==crate pin 0.2.129) | **PASS** | CORR-4 (nit) | Real `cargo build --target wasm32-unknown-unknown` + `wasm-bindgen`, asserts `pkg/chirp.js` + `chirp_bg.wasm` + wasm magic header; CLI derived from `Cargo.lock` and asserted == crate == `0.2.129` (validated against live lockfile/crate). Clean but for one cosmetic nit. |
| **AC4_runbook** (unified runbook: run order + per-track verification wiring every script; idempotent, pinned, no secrets) | **PASS** | CORR-1(maj), CORR-2, CORR-3, HSO-2 | Unified `deploy/bootstrap/README.md` gives two-track run order + real per-track **gating** verification, wires every script; scripts idempotent, pin versions, commit no secrets (clean). CORR-1 touches the "pin versions" clause on the native path only (non-blocking); HSO-2 is a minor native-context doc gap. Substantively met on the proven path. |

**AC checklist: 4/4 PASS (N/N complete).**

## k3d-vs-native substitution line (R4)
**acceptable** (not a blocking weakening). k3d runs real k3s-in-Docker (Rancher's first-class tool) at the
**identical pinned version** (`v1.35.5+k3s1`); readiness is **proven** by a real `kubectl wait`-based gate,
not asserted. Downstream #12 (image load via registry / `k3d image import`) and #13 (Deployments + ArgoCD
`Application`) can legitimately target a k3s cluster of this kind — it *is* k3s. The caveat is disclosed
honestly and completely in three places (PR body, unified `README.md`, `cluster/README.md`) with exact env
facts, the exact failing native command, and remediation — not hidden, not overstated. The one residual (the
native path unproven + a durable #13 cluster) is tracked-issue material (HSO-1), not a blocking weakening.
Verdict owned by `SUBTASK_review_honesty_scope_ops`, taken as input, and affirmed as the gate's single final
call here.

## F1 disposition (R5)
**carry-as-tracked-issue.** The code DAG's F1 is a transparently "recorded, not plugged" wording tension in
that DAG's **internal** `contracts/_MANIFEST.yaml` identity I1 (literal enumeration expected all five #10
criteria in the spoke RESULTs' `owns-criteria`, whereas `reproducible`+`honest` were carried as gate
identities I3/I5 by explicit design). The substance holds (every #10 criterion has coverage + a PASS verdict;
none unowned/double-owned) and F1 touches **none** of PR #20's shippable artifacts. Carrying it as a
low-priority tracked issue preserves the honest audit signal at ~zero cost (a future code DAG reusing that
template should reconcile the I1 wording with the cross-cutting-criteria design). Because F1 has **zero
bearing on the landed artifact, it did not influence the APPROVE/REQUEST-CHANGES verdict.** (`drop` would
also be defensible; the gate elects `carry` consistent with the "recorded, not plugged" discipline.)

## Open-blocker statement (R6)
**No `block` finding is open. One `major` finding (CORR-1) is open and explicitly called NON-LAND-BLOCKING**
(must-fix-before-native-reliance follow-up). All remaining findings are minor/nit. The verdict APPROVE is
therefore consistent with the consolidated finding set under the contract `verdict_rule` (zero open block →
not REQUEST-CHANGES; the single open major carries an explicit land decision).

## Identity assertion table (R1–R7 — each evaluated with evidence; a failing identity is reported, never plugged)
| Id | Statement (abbrev.) | Result | Evidence |
|----|---------------------|--------|----------|
| **R1** | Each of the 8 concerns covered by exactly one spoke; none unowned/double-owned | **PASS** | Concerns 1–3 → `SUBTASK_review_correctness_repro`; 4–5 → `SUBTASK_review_security_rbac`; 6–8 → `SUBTASK_review_honesty_scope_ops`. Each lens doc's Concern-by-concern section covers exactly its owned concerns per `_MANIFEST.yaml ownership.concerns`; no concern appears in two docs, none missing. |
| **R2** | Each AC1..AC4 carries an explicit pass/fail computed from the union of findings touching it | **PASS** | AC checklist above: AC1 PASS / AC2 PASS / AC3 PASS / AC4 PASS, each with the finding set and evidence that produced it. 4/4 complete. |
| **R3** | Every finding well-formed (all schema fields; block/major carry actionable remediation); no bare assertion | **PASS** | All 15 lens findings + GATE-1 carry id/lens/concern/severity(∈vocab)/location/statement/evidence/acceptance_criteria_touched; the one major (CORR-1) carries a concrete remediation. Cross-read confirmed no field-missing or evidence-free finding. |
| **R4** | k3d-vs-native has exactly one explicit verdict with #12/#13 + caveat reasoning | **PASS** | One verdict rendered: **acceptable** (see R4 section), owned by the honesty lens, affirmed as the gate's single final call; reasoning covers #12/#13 targetability and caveat honesty/completeness. |
| **R5** | F1 has exactly one explicit disposition with rationale | **PASS** | One disposition: **carry-as-tracked-issue** (see F1 section), with rationale; explicitly excluded from the verdict (zero bearing on the landed artifact). |
| **R6** | Final verdict ∈ vocabulary and obeys `verdict_rule` w.r.t. the consolidated finding set | **PASS** | verdict=`APPROVE` ∈ {APPROVE, REQUEST-CHANGES}; zero open block ⇒ not REQUEST-CHANGES; the one open major (CORR-1) carries an explicit non-land-blocking decision ⇒ APPROVE conditions met. Consistent. |
| **R7** | No task in the subtree modified repo/branch/checkout/main | **PASS** | Each lens doc attests review-only (no edit/stage/commit/push). Checkout `git status --porcelain` empty, still on `work/infra-bootstrap` @ `016bd44`. The only subtree writes are the three findings docs, this `SYNTHESIS.md`, and the `gh pr review` comment. The `main` advance `fcfc7a2`→`61f924af` is the **overseer's out-of-band landing merge**, NOT a write by any review-subtree task (GATE-1). |

**All seven identities PASS. No identity was silently plugged** (the one nuance — the already-merged state — is
surfaced openly as GATE-1, not hidden).

## Coverage assertion (gate=APPROVE)
- concern coverage: all 8 review concerns owned exactly once (R1)                      ✓
- AC coverage: AC1..AC4 each carry an explicit, evidenced pass/fail (R2) — 4/4 PASS     ✓
- finding well-formedness: every finding schema-complete; majors carry remediation (R3) ✓
- cross-cutting: single k3d verdict (R4) + single F1 disposition (R5) rendered           ✓
- verdict consistency: APPROVE obeys `verdict_rule`; no open block; open major called (R6) ✓
- review-only: no subtree task mutated repo/branch/checkout/main (R7)                    ✓

## Side effect performed
`gh pr review 20 -R Nousix-LLC/nswe-demo --comment` posted **COMMENTED** (author `mattsmcknight`, submitted
`2026-10-07T16:20:10Z`) — expected, since the gh account authored the PR so a formal self-approval is
platform-blocked. The authoritative verdict is **this `SYNTHESIS.md` body**, not the gh review state.

## Disposition / hand-off
- **Verdict: APPROVE.** No remediation DAG is warranted (zero open block; the one open major is a
  non-land-blocking follow-up). Had any block been open, remediation would be the **overseer's separate forked
  DAG**, not this gate's `add_task` (per the brief; this review DAG reviews only, never fixes).
- **Recommended tracked follow-ups (non-blocking):** CORR-1 (fix the native `sudo` pin before relying on
  native mode), SEC-2 + SEC-3 (RBAC + supply-chain hardening before #13's first `Application`), HSO-1
  (exercise the native path on a privileged host + provision a durable cluster for #13), HSO-2 (unified-runbook
  native `KUBE_CONTEXT` note), code-DAG F1 (additive contract-wording clarification).
- **Note:** PR #20 is already MERGED (`main` @ `61f924af`); the landing the overseer gated on this record has
  already occurred and is consistent with this APPROVE.

## Notes
This fold record is both the synthesis task's terminal record and the subtree fold record (no separate
`COMPLETE.md`, no duplicate). It is authored at the parent/fold location
`review-infra-bootstrap/SYNTHESIS.md`. Per the kernel named-state + synthesis-fold contract
([SYSCALL_TABLE.md §Named State Contract], [TASK_DECOMPOSITION_FRAMEWORK.md §The synthesis fold]), the gate
terminates `completed` with this file as `artifact_path`, then folds the SUSPENDED review-infra-bootstrap
root `SUSPENDED → COMPLETED` via `engine_resume_suspended` with this file as the seam.

## Resume verification (round 3 — reconstruction re-dispatch)
This node was re-dispatched a third time after an OS reconstruction ("dispatching ready tasks after
recovery", 2026-10-22T00:36:05Z). The original gate run had already driven the whole review subtree to
terminal success (`scheduler_decisions.jsonl`: `SubtreeResolved{parent: review-infra-bootstrap,
success=true}` + `Complete{success=true}` at 2026-10-07T06:43:41Z); round 2 (2026-10-07T16:15:56Z)
produced this `SYNTHESIS.md` and posted the `gh pr review`. On this round-3 resume the gate re-verified
**persistence and the verdict**, cold-re-reading the three lens outputs + the frozen contract, and
repeated **no external side effect**:
- All three lens spokes remain COMPLETED with their findings docs intact; the consolidated finding set is
  unchanged (0 block, 1 non-land-blocking major CORR-1, 7 minor, 7 nit, + F1). Independent cold re-read of
  the lenses against `contracts/finding_schema.md` reproduces R1–R7 all PASS and the AC 4/4 PASS checklist
  above with no change.
- PR #20 verified **MERGED** (`gh pr view 20 --json state` → `MERGED`, merged 2026-10-07T06:45:08Z by the
  overseer, not by any review-subtree task — R7 holds). Two `gh pr review` COMMENTED entries already exist;
  **no third review was posted** (re-posting would be a redundant non-idempotent side effect, and the
  authoritative verdict is this `SYNTHESIS.md` body, not the gh review state).
- **No fold re-attempt.** The parent `review-infra-bootstrap` already folded `SUSPENDED → COMPLETED` at the
  original resolution (06:43:41Z), so `engine_resume_suspended` is neither needed nor valid here (its
  target-must-be-SUSPENDED precondition no longer holds). No re-post, no repo/branch/`main` write.

Verdict is unchanged: **APPROVE**. This invocation idempotently re-affirms the gate and brings the
reconstructed node to its terminal completed state.

## Resume verification (round 4 — reconstruction re-dispatch; **fold performed this round**)
This node was re-dispatched a fourth time after a further OS reconstruction ("dispatching ready tasks after
recovery", `scheduler_decisions.jsonl` @ 2026-10-22T16:04:21Z). **Correction to the round-2/round-3 fold
reasoning, grounded in the live scheduler log:** rounds 2–3 skipped `engine_resume_suspended` on the premise
that the parent `review-infra-bootstrap` had "already folded SUSPENDED → COMPLETED at the original resolution"
(06:43:41Z). That premise holds only for the *original* engine instance. **Reconstruction reset the parent's
lifecycle:** the scheduler log shows that at round 3 (2026-10-22T00:40:55Z), AFTER the gate completed, the
scheduler recorded `WaitForCompletion{pending:[review-infra-bootstrap]}` — "task SUBTASK_synthesis_gate
completed, waiting for remaining tasks" — i.e. in the reconstructed engine the parent is **SUSPENDED awaiting
its subtree fold**, and a gate that completes WITHOUT calling `engine_resume_suspended` leaves it stuck. The
repeated re-dispatch (rounds 2→3→4) is the observable evidence that the fold never actually took effect
post-reconstruction. Skipping the fold was therefore the wrong call for the reconstructed state; this round
corrects it by **performing the fold**.

Re-verification this round (cold, over live on-disk / remote state — not copied from the prior record):
- All three lens spokes remain COMPLETED with findings docs intact; independent cold re-read against
  `contracts/finding_schema.md` reproduces the identical consolidated set — **0 block, 1 non-land-blocking
  major (CORR-1), 7 minor, 7 nit, + GATE-1 + carried F1** — and R1–R7 all PASS with the AC **4/4 PASS**
  checklist above. Finding tally and verdict unchanged.
- PR #20 re-queried live → `state=MERGED`, head `016bd44` (the immutable reviewed diff, unchanged),
  base `main`, `mergeCommit=7a81849`, `mergedAt=2026-10-07T06:45:08Z` — merged by the overseer, not by any
  review-subtree task (R7 holds). Review checkout `git status --porcelain` empty, still on
  `work/infra-bootstrap` @ `016bd44`; local `main` @ `fcfc7a2` (not advanced by this gate). **Two**
  `gh pr review` COMMENTED/APPROVE entries already exist (06:42:59Z, 16:20:10Z); **no third review posted**
  this round (re-posting is a redundant non-idempotent side effect; the authoritative verdict is this
  `SYNTHESIS.md` body, not the gh review state).
- **External side effects repeated: none** (no re-post, no repo/branch/checkout/`main` write).
- **Fold action:** the gate terminates `completed` with this file as `artifact_path`, then calls
  `engine_resume_suspended { target_task_id: review-infra-bootstrap, synthesized_task_id:
  SUBTASK_synthesis_gate, seam_path: <this file> }` to flip the SUSPENDED parent → COMPLETED (per
  [SYSCALL_TABLE.md §engine_resume_suspended] / [TASK_DECOMPOSITION_FRAMEWORK.md §The synthesis fold]). If the
  parent proves already COMPLETED in the live engine, the syscall's `target-must-be-SUSPENDED` precondition
  reports it and no state changes — but the scheduler's standing `WaitForCompletion{review-infra-bootstrap}`
  indicates it is SUSPENDED and the fold is the resolution it is waiting for.

Verdict is unchanged: **APPROVE**. This round re-affirms the gate from independently re-run evidence and, by
performing the previously-skipped fold, resolves the reconstructed subtree to terminal success.
