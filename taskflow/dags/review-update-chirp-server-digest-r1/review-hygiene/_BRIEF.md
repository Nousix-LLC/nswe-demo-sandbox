# _BRIEF.md — review-digest-r1-hygiene

**Kind**: review concern (atomic)  
**Concern**: Ops Hygiene  
**Parent DAG**: review-update-chirp-server-digest-r1

---

## Objective

Assess whether PR #209 follows the project's conventions for a devops digest-pin change:
commit message format, PR description completeness, and the in-manifest comment format.

---

## Scope

**PR**: #209 (`Nousix-LLC/nswe-demo`)  
**Title**: "deploy(chirp): pin chirp-server image digest to d8230fea build"

What to establish:

1. **Commit message convention**: Does the commit message follow `<type>(<scope>): <subject>` or
   an equivalent project convention appropriate for a deployment change? Is it descriptive enough
   to identify what changed and why?

2. **PR description completeness**: Does the PR description include a summary of the change and
   a `Closes #<issue>` reference (expected: `Closes #206`)? Is the description clear to a reader
   who was not inside the author's head?

3. **In-manifest comment format**: Does the comment in `deploy/chirp/10-deployment.yaml` cite the
   CI run number and the commit SHA (or its short form), following the pattern established by prior
   digest-pin PRs (e.g., the previous block cited run 41687555341 and commit `0d5917dc`)?

4. **Image reference format**: Is the image pinned with `@sha256:<digest>` (not by tag alone)?

Evidence sources:
- PR #209 metadata: `gh pr view 209 --repo Nousix-LLC/nswe-demo`
- Commit message: `gh pr view 209 --repo Nousix-LLC/nswe-demo --json commits`
- Changed file on the PR branch: the comment block in `deploy/chirp/10-deployment.yaml`
- Prior digest-pin PR for comparison (e.g., the PR that introduced the `adaa4c26` digest)

---

## Declared Output

`taskflow/dags/review-update-chirp-server-digest-r1/review-hygiene/FINDINGS.md`

Format: per `taskflow/dags/review-update-chirp-server-digest-r1/contracts/_MANIFEST.yaml`
- `## Verdict` — PASS or FAIL
- `## Evidence` — the commit message text; the PR description (or relevant excerpt); the
  YAML comment block; comparison to expected format
- `## Findings` — None, or a list (hygiene deviations are non-blocking unless the closing
  reference is absent, which is a non-blocking finding)

---

## Success Criteria

The concern is satisfied (PASS) when: the commit message follows the project convention; the PR
description is clear and contains `Closes #206`; the in-manifest comment cites the CI run and
commit; and the image reference uses `@sha256:` format. Deviations are non-blocking findings.
