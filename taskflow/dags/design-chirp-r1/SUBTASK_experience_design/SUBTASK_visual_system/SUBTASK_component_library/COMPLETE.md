# COMPLETE — SUBTASK_component_library

## What was done
Designed chirp's **component library** — the named, reusable UI components with their behavior and
states — and published it as the canonical **component vocabulary** that the screens, responsive, and
accessibility siblings refer to by name, plus the component-library requirements `REQ-UX-033..039`.

Evaluation: **Atomic**. The brief's three listed concerns (component vocabulary; behavior and states;
composition against tokens and archetypes) are facets of each single component, not parallel-farmable
analyses, so every decomposition trigger cleared and both concern tests passed — one responsibility,
one coherent catalog.

## Output produced
- `outputs/component-library.md` — the clearly-headed **"Component library"** content in the shape
  `../contracts/visual_system_seam.yaml` requires, followed by the `REQ-UX-033..039` register entries.

## Composition against inputs
- **Design tokens** (`../SUBTASK_visual_language/outputs/visual-language.md`): every component is built
  from published token names (`color.*`, `type.*`, `space.*`, `radius.*`, `elevation.*`, `motion.*`,
  plus `icon.*` / `avatar.*`); no ad-hoc values are introduced and the token vocabulary is not redefined.
- **IA screen inventory & archetypes** (`../../SUBTASK_ia_interaction/outputs/ia-interaction.md`):
  components refer to screens by their inventory names, and an archetype-coverage table maps each of the
  seven archetypes (feed/list, form, profile, settings, modal/dialog, confirmation, empty/landing) to a
  named component or documented composition.
- **Internal contract** (`../contracts/`): the "Component library" required shape, the required-component
  floor, the state rule, the archetype-coverage rule, the `REQ-UX-033..039` sub-range, the `REQ-UX` field
  set, and the trace rule are composed against, not redefined.
- **Product requirements** (`../../../SUBTASK_product_requirements/outputs/product-requirements.md`):
  every requirement traces to ≥1 `REQ-PROD-*`.

## Coverage
- All 13 required-named components present (ChirpCard, ComposeBox, PrimaryButton, SecondaryButton,
  TextField, NavShell, Dialog, Toast, InlineFeedback, EmptyState, InlineError, LoadingState, Avatar),
  extended with ProfileHeader, Toggle, IconButton, ListView, and SettingRow to furnish every archetype.
- Each component records which of {default, empty, error, loading, disabled} apply and states plainly
  where one does not.
- `REQ-UX-033..039`: 7 entries, unique and in range, each with a statement, stranger-testable
  acceptance criteria on the live product, a `release_gating` flag (all true), and ≥1 `REQ-PROD-*` trace.

## Verification performed
- Floor-component presence, REQ-id range (exactly 033..039 minted), and repository-ready hygiene
  (no host/system/taskflow detail, workspace paths, ids, or attribution) checked mechanically against
  the output.

## Limitation recorded
The design-domain methodology loader was unavailable in the reconstructed environment (`agent_domain_unset`);
the library was designed from the Experience Design bundle intent and product-design competence, recorded
in a methodology note in the output. Per the brief this does not block.

## For the downstream synthesis
`SUBTASK_synthesis` assembles this "Component library" fragment after the `visual_language_and_design_system`
section and consolidates `REQ-UX-033..039` with `REQ-UX-020..032` into the one `REQ-UX-020..039` register.
Identities TOKENS_PUBLISHED_AND_COMPOSED and ARCHETYPE_AND_COMPONENT_COVERAGE are satisfied by this output.
