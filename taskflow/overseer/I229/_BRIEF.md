# _BRIEF.md — NSWE overseer step I229 (persona swe-lead) — EVALUATE: board check / next goal after PR #203 land

**Depends on**: I228
**Task Kind**: evaluate — load `WORK_SESSION` + `BOARD`. Full board check: async-forms escalation status, chirp-server image gap, non-blocker issues sweep, next goal decision.

## Context from I228 (EVALUATE: deployment check after PR #203 land)

- **CI on d8230fea**: ALL 6 PASS (run 41803200262: fmt, clippy, test, wasm, doc, image ✓)
- **ArgoCD**: sync.status=OutOfSync, health=Healthy, operationState=Succeeded at d8230fea — service live
- **Pods**: chirp-server 1/1 Running, postgres 1/1 Running, sweep Completed — all healthy
- **Endpoint**: HTTP 200 at http://100.90.75.93:8081/ ✓
- **Deployment gap** (BEHIND): chirp-server manifest image = `sha256:adaa4c26` predates PRs #182/#183/#188/#203. No chirp-server digest update PR created since those merges. Each CI "image" job built new images (runs 41705065393, 41743675354, 41803200262) but `10-deployment.yaml` was never updated. PRs #182 (argon2id credential hashing), #183 (sweep subcommand), #188 (ferric framework), #203 (router) are NOT running in the deployed image.
- **STATE**: `taskflow/overseer/I228/project_state.json`
- **Config seam**: `taskflow/overseer/_CONFIG.yaml`
- **Active escalation**: ferric-async-forms budget exhausted (PR #193, ACTIVE — do NOT launch ferric-async-forms-r3 without user decision)

## Work for this step

### 1. Load governing files
Load `appfiles/WORK_SESSION.md` + `appfiles/BOARD.md`. Read `_CONFIG.yaml` and `taskflow/overseer/I228/project_state.json`.

### 2. Check async-forms escalation (#130 / PR #193)
- Check if the user has commented on PR #193 (or filed a follow-up issue) since the escalation comment at I220.
  - `gh pr view 193 --repo Nousix-LLC/nswe-demo --comments` — look for user response after escalation comment `https://github.com/Nousix-LLC/nswe-demo/pull/193#issuecomment-6624409600`
- Clearing condition: user indicates "extend budget" or "defer epic #130"
- If still ACTIVE: escalation stays open; do NOT launch ferric-async-forms-r3

### 3. Check chirp-server image gap
- Check open issues for an existing devops issue about chirp-server image digest update (search GitHub issues)
- If none exists: file a new devops issue for chirp-server image update (pin to d8230fea image)
  - Title: `deploy(chirp): update chirp-server image digest to d8230fea build`
  - Body: explain that the deployment is running sha256:adaa4c26 (pre-PR #182), all recent code changes (argon2id creds, sweep subcommand, ferric framework, router) are not live; request pinning 10-deployment.yaml to the d8230fea CI image build
  - Add to board (Todo), high priority (security code not deployed)
- Record issue number and board item in STATE

### 4. Sweep non-blocker and follow-up issues
- Quickly check whether issues #204/#205 (ferric-router-r3 non-blockers, added to board I226) are correctly on the board as Todo
- Note any other issues that may have appeared since I227

### 5. Decide next goal
Priority order per WORK_SESSION.md:
1. **Delivery gap first**: if chirp-server digest update issue is new and high-priority, brief I230 to launch devops DAG for chirp-server digest update (a small devops goal — PR that pins 10-deployment.yaml to d8230fea image digest)
2. **If delivery DAG slot assigned**: next remaining goal from backlog — #132 (HTTP Client, usable_early) is next epic after #131 (landed)
   - async-forms escalation (#130) still ACTIVE → cannot advance epic #130 → skip to #132
   - Brief I230 for board check / goal evaluation, OR if delivery goal fits in same brief, brief I230 for launch devops digest-update DAG + schedule I231 for board check / next code goal

Decision tree:
- Chirp-server image gap → new issue filed → I230 ACT: launch devops DAG for digest update (swe-coder)
- After that → I231 EVALUATE: board check to determine next code goal (#132 HTTP Client)

### 6. Update STATE
Write `taskflow/overseer/I229/project_state.json` with:
- Escalation check outcome
- Chirp-server image issue number (if filed)
- Board hygiene notes
- Next goal decision

## Notes
- Config: delegated/auto_land/headless
- Do NOT launch ferric-async-forms-r3 without user decision on escalation
- BOARD.md governs intake of new issues and board hygiene
- The chirp-server image gap is a devops goal (small — just updating a digest in a manifest file), not a code goal
- Next code epic: #132 (HTTP Client — Ferric 1.0 http client, usable_early), depends on #131 (LANDED ✓) and #129 (LANDED ✓)
