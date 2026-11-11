# Task: Measure every inspection BAR-* by reading declared properties in the repository at c805525

## Task Specification
**Slug**: SUBTASK_inspection_checks
**Task Kind**: standard
**Depends on**: none
**Status**: Pending

### Objective
Inspect the config, manifest, and code artifacts of the `Nousix-LLC/nswe-demo` repository at commit `c805525`, and
judge **every `BAR-*` whose declared `verification_method` is `inspection`** (35 criteria) as `met | partial |
missing | not_applicable`, each with a recorded observation — which artifact was read, the property found there, and
how it settles the criterion.

### Context
Part of `SUBTASK_live_measurement` (see `../_GLOBAL.md` and `../contracts/_MANIFEST.yaml`). This is the inspection
partition: the `BAR-*` settled by reading a declared property from a code/config/manifest artifact rather than by
exercising the running product or running a test — among them module/contract structure (the crate partition, the one
typed client/server contract, the single persistence seam, one web entry point), stated deletion/retention outcomes,
the stated in-product rules, structured-logging and no-secrets-in-logs declarations, and similar declared properties.
The other partitions are owned by siblings; measure only the `inspection` `BAR-*`, and every one of them.

For each such `BAR-*`: find the artifact that is supposed to declare the property, read it, and judge `met` when the
declared property is present and matches the criterion, `partial` when present but incomplete, `missing` when absent,
`not_applicable` only with a stated reason. Cite the repo-relative path (and the relevant section/line sense) in the
observation.

**Dependencies**: none. **Dependents**: `SUBTASK_measurement_fold`.

### Inputs
| Input | Source | Purpose |
|-------|--------|---------|
| Subtree hub | `../_GLOBAL.md` | Shared context, constraints, hygiene |
| Sub-contract | `../contracts/_MANIFEST.yaml` | Your owned partition (`inspection`), the verdict-row schema, the `live_status` vocab |
| id/traceability schema | `../../../contracts/id_and_traceability_schema.yaml` | `live_status` + `verification_method` vocab (authoritative) |
| Release bar | `../../../SUBTASK_release_bar/outputs/release-bar.md` | The 278 `BAR-*`; filter to those tagged `inspection` |
| Design PR record | `../../../SUBTASK_design_pr/outputs/design-pr.md` | The repo `design/` map and branch, for locating artifacts |
| Repository @ `c805525` | `../../../SUBTASK_design_pr/repo` (or a fresh `gh repo clone Nousix-LLC/nswe-demo`, checked out at `c805525`) | Read config/manifest/code artifacts |

### Methodology
Apply the principal-product-designer persona and the relayed **ReleaseBar** guidance. Read the actual artifact at
`c805525` for each criterion and ground the verdict in what it declares; do not infer a property from the product's
behavior (that is another method's job) or from what the design intends. Where no artifact declares the property, the
grounded verdict is `missing`.

### Output
- `outputs/inspection-measurement.md` — a verdict table conforming to `verdict_row_schema` in the sub-contract: one
  row per `inspection` `BAR-*` (`bar_id`, `live_status`, `observation`), the observation citing the repo-relative
  artifact path and the property read. Keyed by `bar_id`.

### Success criteria
- [ ] Every `BAR-*` tagged `inspection` in the release bar has exactly one `live_status` and a grounded observation;
      none omitted, none of another method included.
- [ ] Each observation cites the repository artifact at `c805525` it rests on and the property found there — never
      assumed or confabulated.
- [ ] `live_status` values from the inherited vocab; `bar_id`s verbatim.
- [ ] Touches only `Nousix-LLC/nswe-demo`; no host/system/taskflow detail in the output.

### Constraints
- Read-only repository inspection; write no product code.
- Reference the product only by repository identity, commit SHA, and repo-relative paths in the output.
