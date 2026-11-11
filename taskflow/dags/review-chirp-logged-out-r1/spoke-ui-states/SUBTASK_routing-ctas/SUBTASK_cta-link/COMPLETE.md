# COMPLETE — SUBTASK_cta-link

## Task

Assess the correctness of `link("/compose", "Log in →")` in `compose.rs`'s `render_signup()`.

## Work Done

1. Read `crates/chirp-frontend/src/compose.rs` at commit `decb6196`. Located `render_signup()`.
   Found `link("/compose", "Log in →")` at line 519.

2. Read `crates/chirp-frontend/src/app.rs` at commit `decb6196`. Confirmed:
   - `/compose` routes to `compose_view` (line 150) — the write-chirp view
   - `/signin` routes to `sign_in_view` (line 146) — the dedicated sign-in view
   - `/signup` routes to `signup_view` (line 148) — the source of this CTA

3. Assessed whether `/compose` is the correct destination for a "Log in →" CTA on the sign-up
   page. Verdict: **fail — blocker**.

## Output

`concern-cta.md` written at this workspace. Schema follows `concern_output_schema`.

**Verdict**: fail  
**Severity**: blocker  
**Finding**: `link("/compose", "Log in →")` at `compose.rs:519` routes to the compose view
instead of the dedicated sign-in view. A `sign_in_view` is registered at `/signin` and is the
correct destination for this CTA.  
**Resolution**: Change to `link("/signin", "Log in →")`.
