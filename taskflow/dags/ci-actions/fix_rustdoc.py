#!/usr/bin/env python3
"""CRQ-02: resolve the rustdoc intra-doc-link debt that surfaces under
RUSTDOCFLAGS=-D warnings. Deterministic, exact-string replacements scoped
PER FILE to exactly the occurrences rustdoc flagged (so an identical link in
another module, where the bare label does not resolve, is never touched).
Idempotent. Run with the checkout root as argv[1].
"""
import sys
from pathlib import Path

ROOT = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.cwd()

# --- Category 1: redundant explicit link target -> drop the (path) ----------
# Scoped per file to the flagged occurrences only. `[`L`](path)` -> `[`L`]`.
REDUNDANT = {
    "crates/ferric/src/dom.rs": [
        ("[`Component`](crate::component::Component)", "[`Component`]"),
    ],
    "crates/ferric-router/src/link.rs": [
        ("[`navigate`](crate::router::navigate)", "[`navigate`]"),
    ],
    "crates/ferric-router/src/router.rs": [
        ("[`Params`](crate::matcher::Params)", "[`Params`]"),
        ("[`RoutePattern`](crate::matcher::RoutePattern)", "[`RoutePattern`]"),
    ],
    "crates/ferric-http/src/lib.rs": [
        ("[`Result`](crate::Result)", "[`Result`]"),
    ],
    "crates/chirp-server/src/lib.rs": [
        ("[`ChirpRepository`](repository::ChirpRepository)", "[`ChirpRepository`]"),
    ],
    "crates/chirp-server/src/api/mod.rs": [
        ("[`build_router`](router::build_router)", "[`build_router`]"),
    ],
    "crates/chirp-server/src/api/handlers.rs": [
        ("[`ValidatedJson`](crate::api::ValidatedJson)", "[`ValidatedJson`]"),
    ],
    "crates/chirp-server/src/api/json.rs": [
        ("[`Json`](axum::Json)", "[`Json`]"),
    ],
    "crates/chirp-server/src/api/state.rs": [
        ("[`ChirpRepository`](crate::repository::ChirpRepository)", "[`ChirpRepository`]"),
    ],
    "crates/chirp-server/src/error.rs": [
        ("[`ApiError`](chirp_types::api::ApiError)", "[`ApiError`]"),
        ("[`ErrorCode`](chirp_types::api::ErrorCode)", "[`ErrorCode`]"),
        ("[`FieldError`](chirp_types::api::FieldError)", "[`FieldError`]"),
    ],
    "crates/chirp-server/src/repository/mod.rs": [
        ("[`SessionToken`](chirp_types::api::SessionToken)", "[`SessionToken`]"),
        ("[`UserId`](chirp_types::ids::UserId)", "[`UserId`]"),
        ("[`AuthResponse`](chirp_types::api::AuthResponse)", "[`AuthResponse`]"),
    ],
}

# --- Category 2: ambiguous `axum::serve` -> link the function ---------------
AMBIGUOUS = {
    "crates/chirp-server/src/api/router.rs": [
        ("[`axum::serve`]", "[`axum::serve()`]"),
    ],
}

# --- Category 3: de-link `[`X`]` -> `` `X` `` ------------------------------
# Private items referenced from public docs, the binary `main` (not in the lib
# doc graph), `async_trait` (ambiguous crate/attr-macro — this rustdoc rejects
# the `attribute@` disambiguator, so de-link), and the chirp-frontend
# walking-skeleton forward-references (items a later feature spoke adds).
DELINK = {
    "crates/ferric/src/signal.rs": ["Runtime", "ReactiveScope"],
    "crates/chirp-server/src/repository/in_memory.rs": ["Store"],
    "crates/chirp-server/src/repository/mod.rs": ["async_trait"],
    "crates/chirp-server/src/api/router.rs": ["crate::main", "static_dir"],
    "crates/chirp-frontend/src/api.rs": [
        "ApiClient", "AppError", "chirp_types::ApiError",
    ],
    "crates/chirp-frontend/src/app.rs": [
        "api_base_url", "Session", "AppContext", "AppContext::new",
        "AppContext::client", "Router", "Username::parse", "ChirpText::parse",
        "ValidationError", "ComposeState", "request_rerender", "read_field_value",
    ],
    "crates/chirp-frontend/src/error.rs": [
        "AppError", "chirp_types::ApiError", "AppError::from_http",
        "AppError::Transport",
    ],
    "crates/chirp-frontend/src/compose.rs": [
        "Username::parse", "Session", "ChirpText::parse", "ValidationError",
        "ComposeState", "AppContext", "request_rerender", "read_field_value",
    ],
    "crates/chirp-frontend/src/profile.rs": [
        "profile_view", "User", "set_follow", "set_like", "request_render",
    ],
    "crates/chirp-frontend/src/timeline.rs": [
        "timeline_view", "Page<Chirp>", "TimelineModel", "Signal",
        "RERENDER", "ROUTE_PATH", "bump", "thread_local!",
    ],
}
DELINK_WITH_PATH = {
    "crates/chirp-frontend/src/timeline.rs": [
        ("[`mount`](ferric::mount)", "`mount`"),
    ],
}

def apply(path, pairs, label):
    p = ROOT / path
    txt = p.read_text()
    n = 0
    for old, new in pairs:
        c = txt.count(old)
        if c:
            txt = txt.replace(old, new); n += c
    if n:
        p.write_text(txt)
        print(f"[{label}] {path}: {n}")
    return n

total = 0
for path, pairs in REDUNDANT.items():
    total += apply(path, pairs, "redundant")
for path, pairs in AMBIGUOUS.items():
    total += apply(path, pairs, "ambiguous")
for path, idents in DELINK.items():
    pairs = [(f"[`{i}`]", f"`{i}`") for i in idents]
    total += apply(path, pairs, "delink")
for path, pairs in DELINK_WITH_PATH.items():
    total += apply(path, pairs, "delink*")
print(f"TOTAL replacements: {total}")
