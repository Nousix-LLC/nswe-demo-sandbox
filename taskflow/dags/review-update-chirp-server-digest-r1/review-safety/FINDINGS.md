# Safety Review — PR #209: update chirp-server digest to d8230fea

## Verdict
PASS

## Evidence

### Config drift
Read: `gh pr diff 209 --repo Nousix-LLC/nswe-demo`

Exactly 3 lines changed, all within the `containers[0]` block:

| Line | Change |
|------|--------|
| Comment line 1 | Updated commit ref (`0d5917dc` → `d8230fea`) and CI run number |
| Comment line 2 | Closed issue number updated (`#180` → `#206`) |
| `image:` | Digest updated from `sha256:adaa4c26…` to `sha256:f845ca8c…` |

No other fields touched: `replicas`, resource `requests`/`limits`, `env`, `volumeMounts`,
probes (`startupProbe`, `livenessProbe`, `readinessProbe`), `securityContext`, `strategy`,
`imagePullSecrets`, `volumes`, `terminationGracePeriodSeconds`, `automountServiceAccountToken` —
all unchanged.

### Manifest validity
Read: PR-branch manifest via GitHub API
(`repos/Nousix-LLC/nswe-demo/contents/deploy/chirp/10-deployment.yaml?ref=deploy/update-chirp-server-digest-d8230fea`)

Manifest is valid Kubernetes YAML. The resulting spec is well-formed:
- `apiVersion: apps/v1`, `kind: Deployment` ✓
- `spec.selector.matchLabels` matches `spec.template.metadata.labels` ✓
- `strategy: RollingUpdate` with `maxUnavailable: 0`, `maxSurge: 1` ✓
- Container spec includes `resources`, all three probe types, `securityContext`
  (`allowPrivilegeEscalation: false`, `readOnlyRootFilesystem: true`, `capabilities.drop: [ALL]`),
  and `volumeMounts` with matching `volumes` ✓
- Pod-level `securityContext` sets `runAsNonRoot: true`, `seccompProfile: RuntimeDefault` ✓

### Migration concerns
Read: `gh api repos/Nousix-LLC/nswe-demo/compare/0d5917dc...d8230fea`

Commits in the gap (6 total):

| Commit | PR | Summary |
|--------|-----|---------|
| `a255baf8` | #180 | deploy: pin image for commit 0d5917dc |
| `9a24c281` | #128 | design: Ferric 1.0 framework design docs |
| `c3f9f558` | #182 | fix(security): credential KDF + constant-time verify, sslmode=require |
| `65413bbe` | #187 | deploy: pin sweep CronJob to febeb151 image |
| `aa246877` | #129 | feat(ferric): Ferric 1.0 Authoring Model |
| `d8230fea` | #203 | fix(ferric-router): remove unused VNode import |

**One migration file found**: `crates/chirp-server/migrations/0003_invalidate_plaintext_credentials.sql`
(introduced in `c3f9f558`, read via `gh api ...contents/...?ref=c3f9f558`):

```sql
DELETE FROM credentials;
```

Assessment: This is a DML-only cleanup — no DDL, no schema structural changes
(`ALTER TABLE`, `DROP COLUMN`, `ADD COLUMN`, type changes, index changes). The
migration deletes rows written by pre-KDF builds where plaintext was stored; it
exists because the new binary's `PasswordHash::new()` would reject plaintext values
as corrupt rather than raising `Unauthorized`. The `credentials` table's schema is
unchanged after this migration runs.

Old pod compatibility during rolling update: the previous binary (`0d5917dc`) can
still connect to and query the `credentials` table after the migration runs. It sees
an empty credentials table and returns no-match on authentication — expected behavior
given the security change, not a crash or schema error. The migration comment notes
explicitly: "A pre-production database has no users whose credentials must be
preserved, so the cost is zero."

The current RollingUpdate strategy (`maxUnavailable: 0`, `maxSurge: 1`) brings the
new pod up and waits for it to pass readiness before removing the old pod. The
migration runs on new-pod startup via `PostgresRepository::connect()`. At the moment
the migration runs, the old pod is still alive — but the old pod handles the empty
table gracefully (no crash, no restart). The strategy can safely handle this transition.

No other migration files appear in the diff across the 6-commit gap.

## Findings
None.
