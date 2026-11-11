# Ops Hygiene — PR #209

## Verdict

PASS

## Evidence

**Concern**: Ops hygiene for `deploy(chirp): pin chirp-server image digest to d8230fea build`
(PR #209, `Nousix-LLC/nswe-demo`, opened 2026-11-04)

### 1. Commit message convention

Commit `0b7f447`:

```
deploy(chirp): pin chirp-server image digest to d8230fea build

Updates the chirp-server Deployment image to the digest produced by CI
run 41803200262 for commit d8230fea (all 6 CI jobs SUCCESS).

Deploys PRs now merged to main but not yet live:
- #182 argon2id credential hashing (security)
- #183 sweep subcommand replaces psql CronJob
- #188 Ferric 1.0 Authoring Model: view!, components, context
- #203 Ferric 1.0 router fix

Closes #206.

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>
```

The headline follows `<type>(<scope>): <subject>` (conventional commits). The body identifies the CI run (`41803200262`), the commit short SHA (`d8230fea`), confirms all 6 CI jobs succeeded, lists the PRs that ship with this image, and closes the tracking issue. **Satisfies the convention.**

### 2. PR description completeness

The PR description contains:
- A `## Summary` section identifying the CI run, the commit, the digest, and the PRs being deployed
- An explicit `Closes #206.`
- A `## Test plan` with specific, actionable verification steps (ArgoCD sync, `kubectl get pods`, version check, HTTP 200)

Readable by someone without prior context. `Closes #206` present. **Satisfies completeness.**

### 3. In-manifest comment format

Diff of `deploy/chirp/10-deployment.yaml`:

```diff
-          # never a movable tag. Digest produced by main's CI for commit 0d5917dc (post-merge
-          # image build, run 41687555341). Closes #180; unblocks #64 closure.
-          image: ghcr.io/nousix-llc/chirp-server@sha256:adaa4c26c94d2bffab0342d3dc279eb2d8b42e835494c59385c4b731e246fd41
+          # never a movable tag. Digest produced by main's CI for commit d8230fea (CI run
+          # 41803200262). Closes #206.
+          image: ghcr.io/nousix-llc/chirp-server@sha256:f845ca8c29408fd27d0fc3a6ff3f0f0d661d17ffd63b6427dcceb5b6845f044f
```

The new comment cites the commit short SHA (`d8230fea`) and the CI run number (`41803200262`), following the established pattern. The phrasing shifts from "run NNNNN" to "CI run NNNNN" — a cosmetic change, not a deviation. **Satisfies the comment format.**

### 4. Image reference format

```
ghcr.io/nousix-llc/chirp-server@sha256:f845ca8c29408fd27d0fc3a6ff3f0f0d661d17ffd63b6427dcceb5b6845f044f
```

Pinned with `@sha256:<digest>`, not by tag. **Satisfies the image reference format.**

### Writing voice

Commit body, PR description, and manifest comment reviewed for machine-writing tells. Prose is technical and factual throughout; no moral adjectives on non-agentic nouns, no narrated candor, no slot-fill templates, no hollow filler. No clustered tells found.

## Findings

None.
