import json
bars=json.load(open('SUBTASK_release_bar/SUBTASK_bar_synthesis/calculations/bars_final.json'))
AREAS=[('prod','Product','design/product-requirements.md','`BAR-001..099`'),
       ('dom','Domain & application','design/domain-application-design.md','`BAR-100..199`'),
       ('ux','Experience','design/experience-design.md','`BAR-200..299`'),
       ('id','Identity, security & trust','design/identity-security.md','`BAR-300..399`'),
       ('ops','Operational readiness','design/operational-readiness.md','`BAR-400..499`')]
def idnum(b): return int(b[4:])
from collections import Counter
final=Counter(b['final'] for b in bars.values())
byarea={a:Counter(v['final'] for v in bars.values() if v['area']==a) for a,_,_,_ in AREAS}

O=[]
O.append("# chirp — release bar")
O.append("")
O.append("The release bar for chirp (`Nousix-LLC/nswe-demo`), measured against the current product at commit "
 "`c805525`. It consolidates the five area designs into one register of checkable release conditions, draws the "
 "line between what a first usable version must meet and what the public release requires on top, and records a "
 "deliberate judgment — in scope or out, with a reason — for every surface a product of this kind is expected to "
 "have.")
O.append("")
O.append("Each criterion (`BAR-NNN`) is a condition someone who was not in the design room can check against the "
 "live product. It enforces one or more requirements (`REQ-<AREA>-NNN`) from the area designs and names how it is "
 "verified — `manual_user_check` (a person exercises the product), `automated_test` (a test in the repository "
 "asserts it), `inspection` (a declared property is read from a config, manifest, or code artifact), or "
 "`operational_check` (a property of the running service is observed, such as data surviving a restart). A "
 "criterion states what must be observably true; it does not prescribe how the product is built.")
O.append("")
O.append("The requirements themselves live in the area designs and are not restated here: "
 + ", ".join("`%s`"%a[2] for a in AREAS) + ".")
O.append("")
O.append("---")
O.append("")

# ---------------- Section 1 ----------------
O.append("## MVP-vs-releasable scoping")
O.append("")
O.append("The register is staged on one line, applied the same way across all five areas.")
O.append("")
O.append("**`usable_early`** marks a condition the first version a real person could actually adopt must already "
 "meet:")
O.append("")
O.append("- the **core loop** works — a signed-in person can post a chirp, read a home timeline of themselves and "
 "the people they follow, reply, like, follow, and view a public profile;")
O.append("- the person's **identity is real and owner-only** — they get in only with a secret they hold, carry a "
 "session that is safe to expose on the public internet, and can act on their own account and data and no one "
 "else's;")
O.append("- **what they create survives** a restart, redeploy, or process replacement — the in-memory store at "
 "`c805525`, which loses every account, chirp, follow, and like on restart, is the headline release blocker, and "
 "closing it is part of the first usable version, not a later polish;")
O.append("- the product stands on the **module and contract structure** it will keep (the four-crate partition, the "
 "one typed client/server contract, a single durable-persistence seam, one web entry point);")
O.append("- the core loop **never shows a blank screen, an endless spinner, or a silent failure**, completes on a "
 "phone, and is reachable by keyboard and a screen reader; and")
O.append("- the service can **run under an orchestrator and be diagnosed** — an honest readiness signal, a liveness "
 "signal, structured logs, and no secrets written to them — and it **refuses the obvious abuse** that threatens "
 "even an early build (oversized request bodies, unbounded list reads).")
O.append("")
O.append("**`releasable`** marks what the public release must add on top:")
O.append("")
O.append("- the rest of the **account lifecycle** — self-service recovery, the settings hub, viewing and changing "
 "the verified contact, the sessions-and-devices list, data export, and self-service account deletion;")
O.append("- the **safety and trust surface** — reporting against stated in-product rules, the rules/terms screen, "
 "help and support, and the provisioned, least-privilege operator surface with an audit trail;")
O.append("- **backups and recovery** — scheduled backups with stated retention, stated recovery-point and "
 "recovery-time objectives, a written restore procedure, and rehearsed restore drills;")
O.append("- the **full limits and quotas** posture beyond the early floor;")
O.append("- the **depth of observability** (serving metrics, a serving/availability signal, the administrative "
 "audit trail) and the **incident, status, and availability** apparatus; the finished-feeling experience beyond "
 "the core loop; and the **WCAG 2.1 AA** completion with its verified, no-open-failure release gate.")
O.append("")
O.append("### What each stage contains, by area")
O.append("")
O.append("| Area | `usable_early` | `releasable` | Total |")
O.append("|------|---------------:|-------------:|------:|")
for a,label,_,_ in AREAS:
    O.append("| %s | %d | %d | %d |"%(label,byarea[a]['usable_early'],byarea[a]['releasable'],
                                       byarea[a]['usable_early']+byarea[a]['releasable']))
O.append("| **All areas** | **%d** | **%d** | **%d** |"%(final['usable_early'],final['releasable'],
                                                          final['usable_early']+final['releasable']))
O.append("")
O.append("### Where the areas were reconciled")
O.append("")
O.append("Each area proposed a stage for its own criteria; the one cross-cutting line is reconciled here. "
 "Seventeen criteria were moved from the area proposal to `usable_early` so the line holds together across areas. "
 "The cuts are stated, not hidden:")
O.append("")
O.append("- **Durable persistence is part of the first usable version, not a later addition (14 criteria).** "
 "`BAR-130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 141, 143, 144, 145` — the survival of accounts, chirps, "
 "follows, likes, sessions, counts, and the reconstructable timeline across a restart or redeploy, durable "
 "acknowledged writes, stable ids, authoritative state in a store separate from the serving process, and a "
 "readiness signal that reflects the store — were proposed `releasable` by the domain area but are the headline "
 "`c805525` blocker. They move to `usable_early` to agree with the product area (`BAR-013`) and the "
 "operational-readiness durable-data floor (`BAR-400`–`BAR-404`, `BAR-409`, `BAR-410`), and with the plain "
 "meaning of a usable version: what a person creates is still there when they come back.")
O.append("- **A safe, endable session is part of real identity (2 criteria).** `BAR-016` (sign-out ends the "
 "session on the server) and `BAR-113` (a session can be ended and does not live forever) move to `usable_early` "
 "to agree with the identity area's session floor (`BAR-306`, `BAR-307`): a session that cannot be ended or never "
 "expires leaves the next person at a shared device signed in as someone else, which is not acceptable even in an "
 "early build.")
O.append("- **The sign-in signal is part of real authentication (1 criterion).** `BAR-010` (a person can tell "
 "\"no such account\" from \"wrong secret\" without leaking who exists) moves to `usable_early` to agree with the "
 "identity area's `BAR-304`.")
O.append("")
O.append("Five domain persistence criteria were deliberately **left `releasable`**, because each rests on a "
 "release-layer capability rather than the restart-survival floor: `BAR-140` (integrity across a *restore from "
 "backup* — the restart half of its guarantee is already held early by `BAR-403`), `BAR-142` (a *deletion* stays "
 "applied durably — deletion itself is a releasable surface), `BAR-146` (*backup and restore*), `BAR-147` (the "
 "per-account enumeration behind *data export*), and `BAR-148` (an *upgrade* that changes the data shape "
 "preserves data). Staging these `releasable` hides nothing: the restart-survival floor they build on is held at "
 "`usable_early` by the criteria listed above.")
O.append("")
O.append("### The honest cut")
O.append("")
O.append("A person on the **usable-early** version can find chirp, sign up with a real credential, post and read a "
 "timeline, reply, like, follow, and view profiles, on a phone or a desktop, by pointer or by keyboard and screen "
 "reader — and what they create is still there tomorrow. What they do **not** yet have until the **release** is: "
 "recovering a lost credential by themselves, a settings area, changing their contact, seeing and ending their "
 "other sessions, exporting their data, deleting their own account, reporting abuse against stated rules, and the "
 "operator, backup, incident, and status apparatus behind a service people can trust. Those are the release's to "
 "add; none of them is pretended to be present earlier.")
O.append("")
O.append("---")
O.append("")

# ---------------- Section 2: the register ----------------
O.append("## Release bar")
O.append("")
O.append("The consolidated register, by area, in id order. Each line gives the final stage, the verification "
 "method, the release condition, and the requirement(s) it enforces.")
O.append("")
for a,label,doc,rng in AREAS:
    ids=sorted([b for b,v in bars.items() if v['area']==a],key=idnum)
    ue=sum(1 for b in ids if bars[b]['final']=='usable_early')
    rl=len(ids)-ue
    O.append("### %s (%s) — enforces `%s`"%(label,rng,doc))
    O.append("")
    O.append("_%d criteria — %d `usable_early`, %d `releasable`._"%(len(ids),ue,rl))
    O.append("")
    for b in ids:
        v=bars[b]
        refs=", ".join(v['references'])
        O.append("**%s** (`%s` · `%s`) — %s _Enforces %s._"%(b,v['final'],v['method'],v['statement'],refs))
        O.append("")
    O.append("---")
    O.append("")

# ---------------- Section 3: completeness & gap review ----------------
O.append("## Completeness and gap review")
O.append("")
O.append("A deliberate sweep over the surfaces a product of this kind — a public, consumer, individual-account "
 "social service — is expected to have. For each, a judgment is recorded: in scope (designed, and where it is "
 "held in the bar) or out of scope (with the reason), so an absence is a decision and not an oversight. The sweep "
 "covers the account and operational surfaces the engagement named, and the trust, safety, and discovery surfaces "
 "this product kind adds.")
O.append("")
O.append("### Account and operational surfaces")
O.append("")
O.append("| Surface | Judgment | Where it is held / why it is out |")
O.append("|---------|----------|-----------------------------------|")
rows=[
 ("Sign-up","In scope","Real credential and a point of contact captured; handle format and uniqueness enforced with field-level feedback. `BAR-007`, `BAR-008`, `BAR-231`, `BAR-232`, `BAR-303`, `BAR-321`."),
 ("Sign-in","In scope","Owner-only sign-in with a held secret; a clear not-found vs wrong-credential signal that leaks no private existence. `BAR-009`, `BAR-010`, `BAR-233`, `BAR-300`, `BAR-304`, `BAR-305`."),
 ("Recovery","In scope (releasable)","Self-service recovery gated on proven control of the verified contact, ending sessions that predate the reset. `BAR-015`, `BAR-234`, `BAR-321`–`BAR-324`."),
 ("Account deletion","In scope (releasable)","Self-service, confirmed, with a stated and applied outcome for content and handle; private data erased and sessions ended; durable. `BAR-020`–`BAR-022`, `BAR-118`, `BAR-255`, `BAR-327`–`BAR-329`, `BAR-407`."),
 ("Data export","In scope (releasable)","A person can obtain their own chirps, profile, and follow list in a portable form, excluding secrets and others' data. `BAR-019`, `BAR-119`, `BAR-147`, `BAR-254`, `BAR-325`, `BAR-326`, `BAR-411`."),
 ("Onboarding","In scope","A fresh sign-up lands on an onboarding screen that explains the empty state and offers a first action, never a blank page. `BAR-027`, `BAR-213`, `BAR-237`, `BAR-248`."),
 ("Settings","In scope","One settings hub with labelled sub-sections — edit profile, account & contact, sessions & devices, export, delete (and notification preferences only if notifications ship). `BAR-017`, `BAR-018`, `BAR-214`, `BAR-249`–`BAR-252`, `BAR-317`–`BAR-320`."),
 ("Notifications","Out of scope for v1 (deferred, designed)","A baseline notifications story is designed and expected but is marked non-gating by every area (`REQ-UX-019/072/078`, `REQ-ID-011`); the release does not gate on it. Recorded as a near-term fast-follow rather than a v1 release condition, so its absence at release is a stated decision. No notifications criterion is gated; settings shows the preferences row only where notifications ship."),
 ("Admin / support","In scope (releasable)","A provisioned, least-privilege operator surface (assist recovery, remove content, action an abusive account) that cannot impersonate users or read credentials, with an audit trail; plus user-facing help & support. `BAR-025`, `BAR-258`, `BAR-331`–`BAR-333`, `BAR-335`, `BAR-468`."),
 ("Billing","Out of scope (by product kind)","chirp is a single public consumer product of individual accounts where no money changes hands; tenancy, team/seat management, org-admin, and billing are an explicit non-goal (`need: no-tenancy-or-billing`). There is no billing surface to design, so none is gated."),
]
for s,j,w in rows: O.append("| %s | %s | %s |"%(s,j,w))
O.append("")
O.append("### Trust, safety, and discovery surfaces this product kind adds")
O.append("")
O.append("| Surface | Judgment | Where it is held / why it is out |")
O.append("|---------|----------|-----------------------------------|")
rows2=[
 ("Public first visit / landing","In scope","A visitor with no account sees what chirp is and a clear path to sign up, not a sign-in wall. `BAR-026`, `BAR-230`, `BAR-268`."),
 ("Reporting abuse","In scope (releasable)","A signed-in person can report a chirp or account against stated rules and is acknowledged; reports are routed to the operator surface with enough context to act. `BAR-023`, `BAR-256`, `BAR-334`, `BAR-335`."),
 ("Rules / content policy","In scope (releasable)","The product states its rules as named categories, reachable in-product from both shells, and a report points at one. `BAR-024`, `BAR-257`."),
 ("Block / mute","Out of scope for v1 (deferred, designed)","Designed and expected unwanted-interaction controls, marked non-gating by the product and identity areas (`REQ-PROD`'s unwanted-interaction requirement, `REQ-ID-083/084`). The gated safety floor for v1 is reporting plus operator action, both of which ARE gated; block/mute is recorded as a near-term fast-follow. This is a stated decision, with the residual risk accepted in the identity design."),
 ("Discovery / Explore (find people to follow)","Out of scope for v1 (deferred, designed)","Marked non-gating (`REQ-UX-064`); the area designs flag it as the main social-completeness gap. The bar's explicit call: v1 gates the ability to follow from any profile and from a person row (`BAR-005`, `BAR-245`), so a person can build a timeline without a discovery surface, and a dedicated Explore/discovery surface is a near-term follow-up rather than a v1 gate. Absence is a recorded decision, not a default."),
 ("Sessions & devices management","In scope (releasable)","A person can see where they are signed in and end any session; an ended session can no longer act. `BAR-018`, `BAR-252`, `BAR-308`, `BAR-320`."),
 ("Accessibility statement & conformance","In scope (releasable)","The product states WCAG 2.1 AA and its gated set by name, and the release record shows the gated set has no open A/AA failure. `BAR-275`, `BAR-293`, `BAR-294`."),
 ("Status / incident surface","In scope (releasable)","A status surface reachable when the product itself is down tells a person chirp is affected rather than leaving them to guess. `BAR-482`, `BAR-483`."),
 ("Privacy / data-rights & retention posture","In scope (releasable)","A stated data-rights baseline satisfied through the account's own surfaces, and a published retention and deletion posture that matches observed behaviour. `BAR-330`, `BAR-412`."),
]
for s,j,w in rows2: O.append("| %s | %s | %s |"%(s,j,w))
O.append("")
O.append("### Coverage and findings")
O.append("")
O.append("- **Every release-gating requirement is enforced.** Across the five areas, all 342 requirements marked "
 "`release_gating: true` (Product 35, Domain 79, Experience 106, Identity 63, Operational 59) are each referenced "
 "by at least one `BAR-*`. No release-gating requirement is left without a criterion.")
O.append("- **No cross-cutting criterion was required.** The synthesis range `BAR-900..999` is reserved for a "
 "gap-review finding that needs a release condition no single area already holds. The sweep found none: every "
 "expected surface is either held by an area criterion or recorded out of scope above, and the three deferred "
 "surfaces (notifications, block/mute, discovery) rest on requirements the area designs mark non-gating, so "
 "minting a bar for them would either duplicate an area criterion or gate something the designs deliberately did "
 "not. The reserved range is therefore unused.")
O.append("- **The product can be adopted end to end.** A stranger can find chirp, sign up, post and read, follow "
 "and be followed, get help, report what breaks the rules, export their data, and delete their account — each of "
 "those is a gated release condition above — and what they create survives a restart. The one structural blocker "
 "in the current product at `c805525`, the in-memory store, is closed by the durable-persistence criteria at "
 "`usable_early`.")
O.append("- **The honest gaps at release are named, not hidden.** Notifications, block/mute, and a discovery "
 "surface are real parts of a finished social product and are deliberately deferred as near-term follow-ups; the "
 "safety floor that covers for block/mute (reporting plus operator action) and the ability to follow without a "
 "discovery surface are gated, so the deferral is a scoped decision rather than a hole.")
O.append("")

open('SUBTASK_release_bar/outputs/release-bar.md','w').write("\n".join(O)+"\n")
import os
print("wrote release-bar.md:", os.path.getsize('SUBTASK_release_bar/outputs/release-bar.md'),"bytes")
