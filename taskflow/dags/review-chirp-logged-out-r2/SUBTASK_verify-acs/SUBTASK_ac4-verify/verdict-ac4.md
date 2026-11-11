# Verdict: AC-4

**ac_4_verdict**: PASS

## Evidence

### B2 fix check

`compose.rs:519` at HEAD `7f4b684671cab7eb778f5ad7f54dfdc82d57b3c4` reads:

```rust
                .child(link("/signin", "Log in →")),
```

Confirmed by direct read of the file at the new HEAD via the GitHub API (lines 515–519 of `compose.rs`). The surrounding context:

```
515:         .child(
516:             VElement::new("p")
517:                 .attr("class", "chirp-hint")
518:                 .child(text("Already have an account? "))
519:                 .child(link("/signin", "Log in →")),
520:         )
```

The PR 263 diff also shows the corrected line as an addition (`+`) in the `compose.rs` hunk. B2 is fixed: the sign-up page's "Log in →" CTA now routes to `/signin`, not `/compose`.

### /signin route resolution

`app.rs` is in the PR 263 diff. The diff adds a route binding:

```rust
.route("/signin", move |_params| sign_in_view(&signin_ctx))
```

The module-level doc comment in the same diff hunk documents the entry:

```
//! - `/signin`    -- [`sign_in_view`](crate::sign_in::sign_in_view)
//! - `/sign-in`   -- [`sign_in_view`](crate::sign_in::sign_in_view) (alias for AC-3)
```

`/signin` resolves to `sign_in_view`. The file changed in this PR, but the net state at `7f4b684` satisfies the check.

### Sign-in-to-sign-up path (sign_in.rs:68)

`sign_in.rs` is a new file in PR 263 (diff shows `--- /dev/null`). At HEAD `7f4b684`, line 68 reads:

```rust
                .child(link("/signup", "Create an account"))
```

Confirmed by direct read via the GitHub API (lines 65–72). The sign-in view presents a "New to Chirp? Create an account" link that routes to `/signup`. Path is present and correct.

### Header nav on landing page

`landing.rs` is in the PR 263 diff. The diff adds a `header_nav()` function and calls it unconditionally from `landing_view` before the branch on page state (hoist-before-branch):

```rust
fn header_nav() -> VNode {
    VElement::new("div")
        .attr("class", "chirp-landing-nav")
        .child(link("/signup", "Create account"))
        .child(text(" · "))
        .child(link("/signin", "Sign in"))
        .into()
}

// In landing_view:
.child(header_nav())
.child(body)
```

Both "Create account" (→ `/signup`) and "Sign in" (→ `/signin`) CTAs are present and structurally guaranteed on every render of the landing view.

## Conclusion

All four AC-4 checks pass at HEAD `7f4b684`. The B2 regression is corrected (`compose.rs:519` routes "Log in →" to `/signin`), the `/signin` route resolves to `sign_in_view`, the sign-in page links back to `/signup`, and the landing-page header nav exposes both entry points on every render.
