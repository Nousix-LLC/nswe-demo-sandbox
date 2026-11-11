# _BRIEF.md — T06: PR, CI verification, and synthesis

**Task ID:** ferric-authoring-synthesis  
**Hub:** ferric-epic-authoring-r1  
**Branch:** `work/ferric-epic-authoring-r1` (fully populated by T01–T05)  
**Closes:** Epic #129 (via closing all sub-issues #137–#142 in the PR)

---

## Objective

Open the pull request for the Ferric 1.0 Authoring Model epic, verify CI passes, confirm all six
sub-issues are closed, and author the hub's `SYNTHESIS.md` verdict that the overseer reads.

This task does not add feature code. It synthesizes the evidence left by T01–T05 into a
machine-readable verdict and delivers the PR.

---

## Inputs

- Branch `work/ferric-epic-authoring-r1` as left by T04 and T05 (all code complete, CI-ready).
- The hub contracts at `contracts/_MANIFEST.yaml` (six identity assertions IA1–IA6).
- The `COMPLETE.md` files from each of T01–T05.
- GitHub issues #129, #137, #138, #139, #140, #141, #142.

---

## Acceptance criteria

**PR is open and all CI jobs pass:**
- All GitHub Actions jobs pass on the branch: `fmt`, `clippy`, `test` (including `trybuild`),
  `wasm` (if applicable), `doc`.
- The PR title is concise and names the epic.
- The PR body closes all six sub-issues using GitHub's close syntax.

**All sub-issues are confirmed satisfied:**
For each sub-issue, record the evidence:
- #137: Signal prelude exports and test names demonstrating memoization, batch, scope cleanup.
- #138: Test names demonstrating keyed move (not replace) and partial patch on signal change.
- #139: Compilation of the stated valid view! inputs; trybuild suite for diagnostics.
- #140: Compilation of the stated component forms (props, children, slots, dyn dispatch).
- #141: trybuild component diagnostic suite with committed stderr.
- #142: Context API in prelude; test coverage for provide/use/expect/scope cleanup.

**All six identity assertions from `contracts/_MANIFEST.yaml` pass:**
- IA1: Every sub-issue has exactly one covering task.
- IA2: Invocation seam (macro → component model) confirmed.
- IA3: Context seam (context callable from component body) confirmed.
- IA4: Baseline compatibility — counter example compiles unchanged.
- IA5: Every code task left commits on the branch.
- IA6: trybuild fixtures have committed stderr and pass.

**Machine-gate verdict**: PASS if all six assertions pass and all CI jobs pass; PARTIAL if any
assertion passes but one or more have caveats; FAIL if any assertion fails.

---

## Declared outputs

- One pull request from `work/ferric-epic-authoring-r1` to `main` with the PR body closing
  all six sub-issues.
- `SYNTHESIS.md` at the hub workspace root
  (`taskflow/dags/ferric-epic-authoring-r1/SYNTHESIS.md`) — this is the overseer's observation
  seam. It records the verdict (PASS / PARTIAL / FAIL), the evidence for each sub-issue, the
  identity assertion results, and the PR URL.
- Issues #137, #138, #139, #140, #141, #142 closed (via the PR merge or explicit close).

---

## Constraints

- Do not force-push or rebase history already in the PR.
- Do not add feature code. If a CI job fails, diagnose and commit a fix — but only for
  issues that are strictly within the established scope (a compilation error, a test failure,
  a clippy warning on newly added code). Do not scope-creep.
- The `SYNTHESIS.md` is the ONLY output the overseer reads. Its verdict and evidence must be
  complete enough for an outside reviewer to verify.
- The PR must reference the epic (#129) and all sub-issues (#137–#142).
