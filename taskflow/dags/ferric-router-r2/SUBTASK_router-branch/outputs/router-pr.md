# Router-Only PR — ferric-router-r2

## Branch
work/ferric-router-r2

## PR
https://github.com/Nousix-LLC/nswe-demo/pull/202

## Commits on branch (vs main)
```
c03818f feat(ferric-router): nested routes, replace navigation, active links (r1 spoke completions)
9c9fdd8 ferric-router: active-route awareness on Link::build() (REQ-RT-007)
3404dea feat(ferric-router): add navigate_replace (REQ-RT-003)
```

## Issues closed
- #131 (navigate_replace)
- #146 (active-route awareness)
- #147 (nested routes)

## CI Status
pending — CI workflow triggered on branch push; check https://github.com/Nousix-LLC/nswe-demo/actions

## Notes
- Branch created from `origin/main` (aa24687) after pulling 19 commits that had accumulated since the original r1 work
- All 3 original commit SHAs (89687da, cab18b9, 3868b2c) were cherry-picked onto the updated main base; new SHAs on this branch are 3404dea, 9c9fdd8, c03818f
- Branch diff vs main: only `crates/ferric-router/` files (CHANGELOG.md, README.md, examples/app.rs, src/lib.rs, src/link.rs, src/matcher.rs, src/router.rs) — no ferric-macros or other crate changes
- No cherry-pick conflicts; all three landed cleanly
- PR body contains `Closes #131`, `Closes #146`, `Closes #147` per success criteria
