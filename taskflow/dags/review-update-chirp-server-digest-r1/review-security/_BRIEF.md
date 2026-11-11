# _BRIEF.md — review-digest-r1-security

**Kind**: review concern (atomic)  
**Concern**: Security Scan  
**Parent DAG**: review-update-chirp-server-digest-r1

---

## Objective

Scan the diff of PR #209 for content that must not appear in committed files, per the project's
security constraint. Confirm the changed file contains none of the forbidden categories below.

---

## Scope

**PR**: #209 (`Nousix-LLC/nswe-demo`)  
**Changed files**: `deploy/chirp/10-deployment.yaml` (the only changed file)

Forbidden categories to check for:
- Absolute host paths (e.g., `/home/user/...`, `/root/...`, `/home/<user>/...`)
- Tailnet or LAN IP addresses (e.g., any `100.x.x.x` address)
- Internal or non-public server URLs (hostnames or URLs that are not public registry addresses or
  public GitHub URLs)
- SSH key paths or key material
- Secrets, passwords, tokens, or credentials
- Internal infrastructure details: server hostnames, internal service names, cluster addresses,
  node names

This constraint applies to all content in every changed file — not only the diff lines but the
full file, since a changed file ships as-is into the repository.

Evidence sources:
- PR #209 diff: `gh pr diff 209 --repo Nousix-LLC/nswe-demo`
- Full content of `deploy/chirp/10-deployment.yaml` on the PR branch

---

## Declared Output

`taskflow/dags/review-update-chirp-server-digest-r1/review-security/FINDINGS.md`

Format: per `taskflow/dags/review-update-chirp-server-digest-r1/contracts/_MANIFEST.yaml`
- `## Verdict` — PASS or FAIL
- `## Evidence` — the scan method and what was checked; any patterns searched for
- `## Findings` — None, or a list of matches (any match is a blocking finding)

---

## Success Criteria

The concern is satisfied (PASS) when none of the forbidden categories appear anywhere in
`deploy/chirp/10-deployment.yaml` or any other file changed by PR #209. A single instance of
forbidden content is a blocking finding.
