## Concern: AC-2 — empty_view() content and CTA

**Status**: clean

---

## Checked

**File examined**: `crates/chirp-frontend/src/landing.rs`  
**Function examined**: `empty_view()` (lines 286–306)  
**Pinned commit**: `decb6196c2c1e6ed421d393a642f0c844cc333ba`

Three sub-criteria applied from AC-2:
1. Human-readable description — does the view explain what Chirp is to a new visitor?
2. Sign-up / sign-in CTA — is a visually prominent link to signup and signin present?
3. Blank-page check — does the view avoid "No items" or empty-page patterns?

Corroborating evidence also read: the module-level doc comment (file lines 1–6), the
`view_tree` call site (lines 248–253 and 262–283), and the test
`empty_model_renders_welcome_statement_and_cta_links` (lines 526–542).

---

## Findings

None.

---

## Clean Notes

**Sub-criterion 1 — Human-readable description**: CLEAN

`empty_view()` renders two pieces of identifying content in sequence:

- `crates/chirp-frontend/src/landing.rs:290 at decb6196c2c1e6ed421d393a642f0c844cc333ba`
  — `VElement::new("h2").child(text("Welcome to Chirp"))`: an h2 heading that names the
  product by name.

- `crates/chirp-frontend/src/landing.rs:293–296 at decb6196c2c1e6ed421d393a642f0c844cc333ba`
  — a `p.chirp-landing-description` containing the text "Chirp is a place to share short
  thoughts and follow people you find interesting." This is specific: it names what the
  product does and who it is for in one plain sentence.

Neither element is generic ("No items," "Nothing here," "No content") or blank. The module
doc comment at line 4 independently confirms the intent: "The empty state explains what Chirp
is and offers prominent sign-up and sign-in entry points."

**Sub-criterion 2 — Sign-up / sign-in CTA**: CLEAN

`empty_view()` renders a `div.chirp-landing-cta` (line 299) containing exactly two navigation
links:

- `crates/chirp-frontend/src/landing.rs:301 at decb6196c2c1e6ed421d393a642f0c844cc333ba`
  — `link("/signup", "Create an account")`: explicit route and readable label.

- `crates/chirp-frontend/src/landing.rs:303 at decb6196c2c1e6ed421d393a642f0c844cc333ba`
  — `link("/signin", "Sign in")`: explicit route and readable label.

Both are present, labelled clearly, and routed to the correct paths. They are wrapped in a
dedicated `.chirp-landing-cta` container, which signals distinct CTA styling. The function's
doc comment at line 286 explicitly names "provides sign-up / sign-in entry points (AC-2)",
confirming the intent is deliberate and not incidental.

Note: visual prominence depends on CSS, which is not in scope for this file. What is verifiable
from the code is structural prominence — a dedicated container, correct routes, and clear labels.
The structural evidence is sufficient.

**Sub-criterion 3 — Blank-page check**: CLEAN

The empty state is not blank. `empty_view()` (lines 287–306) produces a `div.chirp-landing-empty`
with three child elements: an h2 heading, a descriptive paragraph, and a CTA block containing
two links. No element of this tree is "No items" text, an empty list, or a zero-child container.
The class name `chirp-landing-empty` is a UI state name, not a user-visible message.

The test `empty_model_renders_welcome_statement_and_cta_links` (line 526) exercises this
state directly and asserts `chirp-landing-empty` is present and that text content includes both
"Welcome"/"Chirp" and "Create an account"/"Sign in". The assertions would fail if `empty_view()`
returned a blank or generic node — the test is an honest behavioral check, not an existence check.
