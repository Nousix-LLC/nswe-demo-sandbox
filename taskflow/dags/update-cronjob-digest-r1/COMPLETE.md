# COMPLETE — update-cronjob-digest-r1

## Status: COMPLETED

## What was done

Updated the `chirp-transient-sweep` CronJob image digest in
`deploy/chirp/50-transient-sweep-cronjob.yaml` from the `c3f9f558` build
(`sha256:adaa4c26c94d2bffab0342d3dc279eb2d8b42e835494c59385c4b731e246fd41`)
to the `febeb151` build (`sha256:2c5eafbe4e4009652ec0f0bc3d6aeac594904debcd3776b9dacb6b78ed98e06c`),
published by CI run 41710206505 after PR #183 merged.

Also removed the stale "NOTE: update this digest after post-merge CI" comments
that described the interim state.

## Outputs

- **PR**: https://github.com/Nousix-LLC/nswe-demo/pull/187
  - Branch: `work/update-sweep-digest-r1`
  - Commit: `61206a2`
  - Base: `main`

## Digest provenance

- CI run: 41710206505
- Head SHA: `febeb151ba50f6c2635d922b5c3da6e01371c617` (PR #183 merge commit)
- Image job: `126176340502` — conclusion: success
- Published manifest digest: `sha256:2c5eafbe4e4009652ec0f0bc3d6aeac594904debcd3776b9dacb6b78ed98e06c`
- Pushed tags: `latest`, `sha-febeb151ba50f6c2635d922b5c3da6e01371c617`

## Cluster state at completion

- ArgoCD application `chirp`: OutOfSync/Degraded (expected — PR #187 is open but not yet merged)
- Cluster still running old image (`sha256:adaa4c26...`) — will auto-sync once PR #187 merges to main
- CronJob `chirp-transient-sweep` will be updated by ArgoCD on next reconcile after merge

## References

- PR #183 (post-merge trigger): fix(#117): replace psql sweep CronJob with chirp-server sweep subcommand
- CronJob was failing with "command not found" because the old binary (c3f9f558) lacked the `sweep` subcommand
- PR #187 (this change, auto_land: true): closes the follow-up noted in #183
