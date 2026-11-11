# Task: Measure every automated_test BAR-* against the repository test suite at c805525

## Task Specification
**Slug**: SUBTASK_automated_tests
**Task Kind**: standard
**Depends on**: none
**Status**: Pending

### Objective
Run and read the test suite in the `Nousix-LLC/nswe-demo` repository at commit `c805525`, and judge **every `BAR-*`
whose declared `verification_method` is `automated_test`** (36 criteria) as `met | partial | missing |
not_applicable`, each with a recorded observation — which test(s) assert the condition and what running or reading them
showed.

### Context
Part of `SUBTASK_live_measurement` (see `../_GLOBAL.md` and `../contracts/_MANIFEST.yaml`). This is the
automated-test partition: the `BAR-*` a repository test is meant to assert — largely the core-loop behaviors (posting,
timeline, replies, likes, follows, profiles, sign-up/in handle rules, cross-account refusal, field hygiene,
session-ending). The other partitions are owned by siblings; measure only the `automated_test` `BAR-*`, and every one
of them.

For each such `BAR-*`: locate the test(s) that assert it, run the suite (or the relevant tests), and judge `met` when
a present test actually asserts the condition and passes, `partial` when a test asserts only part of the condition or
is skipped/flaky, `missing` when no test asserts it (or the asserting test fails), `not_applicable` only with a stated
reason. A criterion whose condition rests on durable persistence may be asserted by a test that passes against the
in-memory store yet says nothing about restart survival — note that distinction where it applies.

**Dependencies**: none. **Dependents**: `SUBTASK_measurement_fold`.

### Inputs
| Input | Source | Purpose |
|-------|--------|---------|
| Subtree hub | `../_GLOBAL.md` | Shared context, constraints, hygiene |
| Sub-contract | `../contracts/_MANIFEST.yaml` | Your owned partition (`automated_test`), the verdict-row schema, the `live_status` vocab |
| id/traceability schema | `../../../contracts/id_and_traceability_schema.yaml` | `live_status` + `verification_method` vocab (authoritative) |
| Release bar | `../../../SUBTASK_release_bar/outputs/release-bar.md` | The 278 `BAR-*`; filter to those tagged `automated_test` |
| Design PR record | `../../../SUBTASK_design_pr/outputs/design-pr.md` | Repo layout and branch context |
| Repository @ `c805525` | `../../../SUBTASK_design_pr/repo` (or a fresh `gh repo clone Nousix-LLC/nswe-demo`, checked out at `c805525`) | Read and run the test suite |

### Methodology
Apply the principal-product-designer persona and the relayed **ReleaseBar** guidance. Build and run the repository's
tests at `c805525` with its own toolchain; where the suite cannot be built or run in this environment, read the tests
and judge from their assertions, recording that they were read rather than executed and judging conservatively. Ground
every verdict in a named test (path/name) and its observed result.

### Output
- `outputs/automated-test-measurement.md` — a verdict table conforming to `verdict_row_schema` in the sub-contract:
  one row per `automated_test` `BAR-*` (`bar_id`, `live_status`, `observation`), the observation naming the test(s)
  and the result. Keyed by `bar_id`.

### Success criteria
- [ ] Every `BAR-*` tagged `automated_test` in the release bar has exactly one `live_status` and a grounded
      observation; none omitted, none of another method included.
- [ ] Each observation names the repository test artifact at `c805525` it rests on and what running or reading it
      showed — never assumed or confabulated; where the suite could not be executed, that is stated and the verdict is
      conservative.
- [ ] `live_status` values from the inherited vocab; `bar_id`s verbatim.
- [ ] Touches only `Nousix-LLC/nswe-demo`; no host/system/taskflow detail in the output.

### Constraints
- Inspect and run tests only; write no product code and change no test.
- Reference the product only by repository identity and commit SHA in the output.
