# NSWE Sandbox — a Nousix taskflow, reconstructed

> **Display only.** This repository is a frozen, read-only snapshot of one NSWE engagement's
> on-disk **taskflow** — the artifact the Nousix OS leaves on the filesystem as it runs. It is here
> to be read, not run; it is not a runtime.

**What it shows:** Nousix does not run an *agent loop* or an *agent graph*. It runs a **process
graph**, and *the files on disk are that graph*. A single serial **overseer thread** evaluates the
project board each turn and **forks** DAGs — a code build, a review, a design; each DAG decomposes
into its own subtree; every node leaves its lifecycle records. Nothing orchestrates from memory: the
scheduler can reconstruct the entire run from these files alone.

## The run, reconstructed

Below is this engagement as rebuilt by Core's **dry-run reconstructor** — `nousix resume --dry-run`,
which walks the on-disk tree and reassembles the actor graph with **zero model calls**. This is its
output: the serial overseer thread, every DAG it forked (in fork order), and each DAG's full
decomposition.

```text
nousix resume --dry-run  (reconstruct thread + forks; no claude -p dispatched)
  request_id:       nswe-demo
  actors:           102   (1 thread + 101 forked DAGs)
  forked actors:    101
  live nodes:       1025
  max-dag:          1   (at most one forked DAG driven at once; rest queued in fork order)

overseer  [root, thread]  COMPLETED  (428 serial nodes  I0…I426)
├── ferric-foundation             [fork, DAG]  COMPLETED (6 nodes)
│   ├── SUBTASK_synthesis
│   ├── SUBTASK_scaffold
│   ├── SUBTASK_reactive_core
│   ├── SUBTASK_view_and_diff
│   └── SUBTASK_dom_runtime
├── review-ferric-foundation      [fork, DAG]  COMPLETED (1 node)
├── ferric-http                   [fork, DAG]  COMPLETED (1 node)
├── review-ferric-router          [fork, DAG]  COMPLETED (1 node)
├── review-ferric-http            [fork, DAG]  COMPLETED (1 node)
├── review-chirp-types            [fork, DAG]  COMPLETED (1 node)
├── ferric-http-relock-r1         [fork, DAG]  COMPLETED (1 node)
├── review-chirp-frontend         [fork, DAG]  COMPLETED (1 node)
├── chirp-server                  [fork, DAG]  COMPLETED (11 nodes)
│   ├── SUBTASK_scaffold_and_repository
│   ├── SUBTASK_integration_tests_and_docs
│   ├── SUBTASK_reverify_gate
│   ├── SUBTASK_fix_validation_error_mapping
│   ├── SUBTASK_synthesis_gate
│   └── SUBTASK_api_layer
│       ├── SUBTASK_api_synthesis
│       ├── SUBTASK_transport_foundations
│       ├── SUBTASK_handlers
│       └── SUBTASK_router_and_bootstrap
├── review-chirp-server           [fork, DAG]  COMPLETED (6 nodes)
│   ├── SUBTASK_test_adequacy_review
│   ├── SUBTASK_code_review_quality_review
│   ├── SUBTASK_architecture_contract_review
│   ├── SUBTASK_rust_soundness_review
│   └── SUBTASK_synthesis_verdict
├── chirp-server-relock-r1        [fork, DAG]  COMPLETED (1 node)
├── ci-actions                    [fork, DAG]  COMPLETED (1 node)
├── containerize                  [fork, DAG]  COMPLETED (1 node)
├── review-containerize           [fork, DAG]  COMPLETED (10 nodes)
│   ├── SUBTASK_verdict_synthesis
│   ├── SUBTASK_rustcode_sigterm
│   ├── SUBTASK_security_supplychain
│   ├── SUBTASK_dockerfile_build
│   ├── SUBTASK_operability_docs
│   └── SUBTASK_scope_verification
│       ├── SUBTASK_findings_synthesis
│       ├── SUBTASK_scope_conformance
│       └── SUBTASK_verification_depth
├── remediate-ci-actions          [fork, DAG]  COMPLETED (1 node)
├── review-ci-actions-r3          [fork, DAG]  COMPLETED (1 node)
├── review-deploy-argocd          [fork, DAG]  COMPLETED (1 node)
├── deploy-ghcr-auth              [fork, DAG]  FAILED    (1 node)
├── review-deploy-ghcr-auth       [fork, DAG]  COMPLETED (1 node)
├── review-ci-actions-r2          [fork, DAG]  COMPLETED (6 nodes)
│   ├── SUBTASK_supply_chain_security
│   ├── SUBTASK_folded_minors
│   ├── SUBTASK_workflow_correctness
│   ├── SUBTASK_image_job
│   └── SUBTASK_synthesis
├── review-epic-persist           [fork, DAG]  COMPLETED (14 nodes)
│   ├── SUBTASK_synthesis
│   ├── SUBTASK_architecture_contract
│   ├── SUBTASK_code_quality
│   ├── SUBTASK_security
│   ├── SUBTASK_durability_proof
│   ├── SUBTASK_ci_doc_diagnosis
│   ├── SUBTASK_operational_readiness
│   └── SUBTASK_correctness
│       ├── SUBTASK_synthesis
│       ├── SUBTASK_ac66_seam_migration
│       ├── SUBTASK_ac67_retention_failclosed
│       ├── SUBTASK_ac65_invariants
│       └── SUBTASK_design_req_and_64
├── deploy-argocd                 [fork, DAG]  COMPLETED (9 nodes)
│   ├── SUBTASK_discovery
│   ├── SUBTASK_app_manifests
│   ├── SUBTASK_argocd_gitops
│   └── SUBTASK_synthesis  (SUSPENDED)
│       ├── SUBTASK_fold
│       ├── SUBTASK_static_gate
│       ├── SUBTASK_deploy_reach
│       └── SUBTASK_land_pr
├── infra-bootstrap               [fork, DAG]  COMPLETED (5 nodes)
│   ├── SUBTASK_synthesis_gate
│   ├── SUBTASK_cluster_k3s
│   ├── SUBTASK_wasm_toolchain
│   └── SUBTASK_gitops_argocd
├── deploy-ghcr-auth-r2           [fork, DAG]  COMPLETED (4 nodes)
│   ├── SUBTASK_verify_synthesis
│   ├── SUBTASK_diagnose
│   └── SUBTASK_remediate
├── chirp-types                   [fork, DAG]  COMPLETED (3 nodes)
│   ├── SUBTASK_implement_crate
│   └── SUBTASK_synthesis_gate
├── review-infra-bootstrap        [fork, DAG]  COMPLETED (5 nodes)
│   ├── SUBTASK_review_honesty_scope_ops
│   ├── SUBTASK_review_correctness_repro
│   ├── SUBTASK_review_security_rbac
│   └── SUBTASK_synthesis_gate
├── chirp-frontend                [fork, DAG]  COMPLETED (7 nodes)
│   ├── SUBTASK_synthesis_gate
│   ├── SUBTASK_scaffold
│   ├── SUBTASK_api_client
│   ├── SUBTASK_compose
│   ├── SUBTASK_profile
│   └── SUBTASK_timeline
├── ferric-router                 [fork, DAG]  COMPLETED (6 nodes)
│   ├── SUBTASK_synthesis
│   ├── SUBTASK_scaffold
│   ├── SUBTASK_matcher
│   ├── SUBTASK_navigation
│   └── SUBTASK_view
├── design-chirp-r1               [fork, DAG]  COMPLETED (105 nodes)
│   ├── SUBTASK_design_pr
│   ├── SUBTASK_delivery_backlog
│   ├── SUBTASK_synthesis  (SUSPENDED)
│   │   ├── SUBTASK_identity_traceability
│   │   │   ├── SUBTASK_matrix_id_ops
│   │   │   ├── SUBTASK_matrix_ux
│   │   │   ├── SUBTASK_concern_surface
│   │   │   ├── SUBTASK_backlog_pr
│   │   │   ├── SUBTASK_matrix_prod_dom
│   │   │   ├── SUBTASK_bar_mapping
│   │   │   └── SUBTASK_assemble
│   │   ├── SUBTASK_fold
│   │   └── SUBTASK_live_measurement
│   │       ├── SUBTASK_measurement_fold
│   │       ├── SUBTASK_inspection_checks
│   │       ├── SUBTASK_operational_checks
│   │       ├── SUBTASK_automated_tests
│   │       └── SUBTASK_live_journeys
│   │           ├── SUBTASK_safety_trust_support
│   │           ├── SUBTASK_web_delivery_api
│   │           ├── SUBTASK_accessibility
│   │           ├── SUBTASK_account_lifecycle
│   │           ├── SUBTASK_visual_craft_nav
│   │           ├── SUBTASK_responsive_phone
│   │           ├── SUBTASK_core_loop
│   │           ├── SUBTASK_getin_identity
│   │           ├── SUBTASK_resilience_states
│   │           └── SUBTASK_journeys_fold
│   ├── SUBTASK_release_bar
│   │   ├── SUBTASK_bar_prod
│   │   ├── SUBTASK_bar_id
│   │   ├── SUBTASK_bar_dom
│   │   ├── SUBTASK_bar_ops
│   │   ├── SUBTASK_bar_synthesis
│   │   └── SUBTASK_bar_ux
│   │       ├── SUBTASK_bar_ux_ia
│   │       ├── SUBTASK_bar_ux_responsive
│   │       ├── SUBTASK_bar_ux_visual
│   │       ├── SUBTASK_bar_ux_a11y
│   │       ├── SUBTASK_bar_ux_screens
│   │       │   ├── SUBTASK_bar_screens_entry_auth
│   │       │   ├── SUBTASK_bar_screens_safety_states
│   │       │   ├── SUBTASK_bar_screens_core_loop
│   │       │   ├── SUBTASK_bar_screens_social_profiles
│   │       │   ├── SUBTASK_bar_screens_account_lifecycle
│   │       │   └── SUBTASK_bar_screens_synthesis
│   │       └── SUBTASK_bar_ux_synthesis
│   ├── SUBTASK_identity_trust
│   │   ├── SUBTASK_auth_sessions
│   │   ├── SUBTASK_abuse_privacy
│   │   ├── SUBTASK_authorization
│   │   ├── SUBTASK_accounts_lifecycle
│   │   └── SUBTASK_synthesis
│   ├── SUBTASK_operational_readiness
│   │   ├── SUBTASK_ops_durable_data
│   │   ├── SUBTASK_ops_limits_quotas
│   │   ├── SUBTASK_ops_observability
│   │   ├── SUBTASK_ops_backups_recovery
│   │   ├── SUBTASK_ops_status_incident
│   │   └── SUBTASK_ops_synthesis
│   ├── SUBTASK_product_requirements
│   │   ├── SUBTASK_synthesis
│   │   ├── SUBTASK_product_definition
│   │   ├── SUBTASK_users_and_journeys
│   │   ├── SUBTASK_requirements
│   │   └── SUBTASK_pr_synthesis
│   ├── SUBTASK_experience_design
│   │   ├── SUBTASK_ia_interaction
│   │   ├── SUBTASK_responsive
│   │   ├── SUBTASK_accessibility
│   │   ├── SUBTASK_synthesis
│   │   ├── SUBTASK_screens_flows
│   │   │   ├── SUBTASK_considered_states
│   │   │   ├── SUBTASK_get_in
│   │   │   ├── SUBTASK_safety_notifications
│   │   │   ├── SUBTASK_core_loop
│   │   │   │   ├── SUBTASK_timeline_reading
│   │   │   │   ├── SUBTASK_profiles_discovery
│   │   │   │   ├── SUBTASK_social_actions
│   │   │   │   ├── SUBTASK_synthesis
│   │   │   │   └── SUBTASK_posting_conversation
│   │   │   │       ├── SUBTASK_synthesis
│   │   │   │       ├── SUBTASK_reply_conversation
│   │   │   │       └── SUBTASK_compose_post
│   │   │   ├── SUBTASK_account_lifecycle
│   │   │   │   ├── SUBTASK_onboarding_profile
│   │   │   │   ├── SUBTASK_leaving
│   │   │   │   ├── SUBTASK_synthesis
│   │   │   │   └── SUBTASK_settings_management
│   │   │   │       ├── SUBTASK_synthesis
│   │   │   │       ├── SUBTASK_settings_hub
│   │   │   │       ├── SUBTASK_account_contact
│   │   │   │       ├── SUBTASK_notification_prefs
│   │   │   │       └── SUBTASK_sessions_devices
│   │   │   └── SUBTASK_synthesis
│   │   └── SUBTASK_visual_system
│   │       ├── SUBTASK_visual_language
│   │       ├── SUBTASK_component_library
│   │       └── SUBTASK_synthesis
│   └── SUBTASK_domain_app_design
│       ├── SUBTASK_domain_model
│       ├── SUBTASK_persistence_state
│       ├── SUBTASK_module_structure
│       └── SUBTASK_dad_synthesis
├── design-ferric-1_0             [fork, DAG]  COMPLETED (38 nodes)
│   ├── SUBTASK_scope_and_requirements
│   ├── SUBTASK_performance_and_benchmark
│   ├── SUBTASK_docs_and_dx
│   ├── SUBTASK_ssr_hydration
│   ├── SUBTASK_authoring_model
│   │   ├── SUBTASK_components_props_slots
│   │   ├── SUBTASK_view_macro
│   │   ├── SUBTASK_context
│   │   └── SUBTASK_synthesis
│   ├── SUBTASK_release_and_distribution
│   │   ├── SUBTASK_versioning_compat
│   │   ├── SUBTASK_semver_changelog
│   │   ├── SUBTASK_publishing
│   │   └── SUBTASK_rel_synthesis
│   ├── SUBTASK_router_and_http
│   │   ├── SUBTASK_synthesis
│   │   ├── SUBTASK_http
│   │   └── SUBTASK_router
│   ├── SUBTASK_async_forms_events
│   │   ├── SUBTASK_afe_synthesis
│   │   ├── SUBTASK_afe_events_payloads
│   │   ├── SUBTASK_afe_async_resources
│   │   └── SUBTASK_afe_forms_binding
│   ├── SUBTASK_release_plan  (SUSPENDED)
│   │   ├── SUBTASK_rplan_epics
│   │   ├── SUBTASK_rplan_work_items
│   │   └── SUBTASK_rplan_synthesis
│   ├── SUBTASK_design_pr
│   ├── SUBTASK_file_backlog
│   ├── SUBTASK_synthesis
│   └── SUBTASK_release_bar
│       ├── SUBTASK_rbar_gap_review
│       ├── SUBTASK_rbar_criteria
│       └── SUBTASK_rbar_synthesis
│           ├── SUBTASK_rbar_criteria
│           ├── SUBTASK_rbar_assembly
│           └── SUBTASK_rbar_gap
├── remediate-epic-persist-r1     [fork, DAG]  COMPLETED (8 nodes)
│   ├── SUBTASK_synthesis
│   ├── SUBTASK_assess
│   ├── SUBTASK_apply_fixes
│   └── SUBTASK_verify_deliver  (SUSPENDED)
│       ├── SUBTASK_synthesis
│       ├── SUBTASK_ci_verify
│       └── SUBTASK_pr_update
├── review-ci-actions             [fork, DAG]  COMPLETED (1 node)
├── remediate-epic-persist-r1b    [fork, DAG]  COMPLETED (1 node)
├── design-ferric-1_0-r2          [fork, DAG]  COMPLETED (18 nodes)
│   ├── SUBTASK_synthesize-root
│   ├── SUBTASK_review-validate
│   │   ├── SUBTASK_synthesis
│   │   ├── SUBTASK_validate-ssr
│   │   ├── SUBTASK_validate-router
│   │   ├── SUBTASK_validate-scope
│   │   ├── SUBTASK_validate-authoring
│   │   ├── SUBTASK_validate-async
│   │   ├── SUBTASK_validate-docs
│   │   ├── SUBTASK_validate-release
│   │   ├── SUBTASK_validate-perf
│   │   ├── SUBTASK_validate-plan
│   │   └── SUBTASK_validate-crossrefs
│   │       ├── SUBTASK_req-reconciliation
│   │       ├── SUBTASK_issue-traceability
│   │       └── SUBTASK_synthesis-crossrefs
│   └── SUBTASK_remediate
├── remediate-epic-persist-r1c    [fork, DAG]  COMPLETED (1 node)
├── review-epic-persist-r2        [fork, DAG]  COMPLETED (1 node)
├── design-ferric-1_0-r3          [fork, DAG]  COMPLETED (9 nodes)
│   ├── SUBTASK_foundation-buildability
│   ├── SUBTASK_ticket-review
│   ├── SUBTASK_design-doc-review  (SUSPENDED)
│   │   ├── SUBTASK_release-bar-quality
│   │   ├── SUBTASK_completeness-review
│   │   ├── SUBTASK_traceability-review
│   │   └── SUBTASK_findings-synthesis
│   └── SUBTASK_synthesis
├── remediate-design-ferric-1_0-r1[fork, DAG]  COMPLETED (1 node)
├── pin-image-digest-r1           [fork, DAG]  COMPLETED (1 node)
├── review-design-ferric-1_0-r4   [fork, DAG]  COMPLETED (1 node)
├── security-persist-r1           [fork, DAG]  COMPLETED (4 nodes)
│   ├── SUBTASK_credential_hashing
│   ├── SUBTASK_ssl_manifest
│   └── SUBTASK_synthesis
├── sweep-seam-r1                 [fork, DAG]  COMPLETED (1 node)
├── review-security-persist-r1    [fork, DAG]  COMPLETED (1 node)
├── sweep-seam-r1-r1              [fork, DAG]  COMPLETED (1 node)
├── review-sweep-seam-r1          [fork, DAG]  COMPLETED (1 node)
├── update-cronjob-digest-r1      [fork, DAG]  COMPLETED (1 node)
├── review-update-sweep-digest-r1 [fork, DAG]  COMPLETED (1 node)
├── ferric-epic-authoring-r1      [fork, DAG]  COMPLETED (17 nodes)
│   ├── T01-137-138-foundation
│   ├── T02-139-view-macro
│   │   ├── SUBTASK_synthesis
│   │   ├── SUBTASK_impl  (SUSPENDED)
│   │   │   ├── SUBTASK_scaffold
│   │   │   ├── SUBTASK_wire
│   │   │   ├── SUBTASK_macro_impl
│   │   │   └── SUBTASK_synthesis
│   │   └── SUBTASK_tests
│   │       ├── SUBTASK_trybuild
│   │       ├── SUBTASK_conformance
│   │       └── SUBTASK_synthesis
│   ├── T03-140-component
│   ├── T05-142-context
│   ├── T04-141-diagnostics
│   └── T06-synthesis
├── review-ferric-epic-authoring-r1[fork, DAG]  COMPLETED (1 node)
├── ferric-async-forms-r1         [fork, DAG]  COMPLETED (6 nodes)
│   ├── SUBTASK_walking_skeleton
│   ├── SUBTASK_async_resource
│   ├── SUBTASK_form_binding
│   ├── SUBTASK_dom_events
│   └── SUBTASK_synthesis
├── ferric-router-r1              [fork, DAG]  COMPLETED (7 nodes)
│   ├── SUBTASK_navigate_replace
│   ├── SUBTASK_active_link
│   ├── SUBTASK_nested_routes
│   ├── SUBTASK_synthesis_gate
│   ├── SUBTASK_clippy_fix
│   └── SUBTASK_synthesis_verify
├── ferric-async-forms-r2         [fork, DAG]  COMPLETED (1 node)
├── review-ferric-router-r1       [fork, DAG]  COMPLETED (1 node)
├── review-ferric-async-forms-r2  [fork, DAG]  COMPLETED (1 node)
├── ferric-router-r2              [fork, DAG]  COMPLETED (4 nodes)
│   ├── SUBTASK_synthesis
│   ├── SUBTASK_router-branch
│   └── SUBTASK_macros-assessment
├── ferric-router-r3              [fork, DAG]  COMPLETED (1 node)
├── review-ferric-router-r3       [fork, DAG]  COMPLETED (1 node)
├── update-chirp-server-digest-r1 [fork, DAG]  COMPLETED (1 node)
├── review-update-chirp-server-digest-r1[fork, DAG]  COMPLETED (6 nodes)
│   ├── review-synthesis
│   ├── review-hygiene
│   ├── review-security
│   ├── review-correctness
│   └── review-safety
├── ferric-http-r1                [fork, DAG]  COMPLETED (1 node)
├── review-ferric-http-r1         [fork, DAG]  COMPLETED (1 node)
├── ferric-http-r2                [fork, DAG]  COMPLETED (1 node)
├── review-ferric-http-r2         [fork, DAG]  COMPLETED (12 nodes)
│   ├── SUBTASK_security
│   ├── SUBTASK_correctness
│   ├── SUBTASK_code_quality  (SUSPENDED)
│   │   ├── SUBTASK_completeness_check
│   │   ├── SUBTASK_format_check
│   │   ├── SUBTASK_placement_check
│   │   │   ├── SUBTASK_synthesis
│   │   │   ├── SUBTASK_placement_analysis
│   │   │   └── SUBTASK_duplication_analysis
│   │   └── SUBTASK_synthesis
│   └── SUBTASK_verdict
├── ferric-ssr-r1                 [fork, DAG]  COMPLETED (6 nodes)
│   ├── SUBTASK_synthesis
│   ├── SUBTASK_skeleton
│   ├── SUBTASK_axum_integration
│   ├── SUBTASK_server_render
│   └── SUBTASK_client_hydrate
├── ferric-ssr-r2                 [fork, DAG]  COMPLETED (1 node)
├── ferric-ssr-r3                 [fork, DAG]  COMPLETED (1 node)
├── review-ferric-ssr-r1          [fork, DAG]  COMPLETED (25 nodes)
│   ├── SUBTASK_synthesis
│   ├── SUBTASK_security_infra
│   ├── SUBTASK_security_xss
│   ├── SUBTASK_code_quality  (SUSPENDED)
│   │   ├── SUBTASK_B_abstraction
│   │   ├── SUBTASK_A_api_surface
│   │   ├── SUBTASK_D_function_design
│   │   ├── SUBTASK_C_error_handling
│   │   ├── SUBTASK_E_test_coverage
│   │   ├── SUBTASK_F_documentation
│   │   └── SUBTASK_synthesis_cq
│   └── SUBTASK_correctness  (SUSPENDED)
│       ├── SUBTASK_ssr_render
│       ├── SUBTASK_hydration
│       │   ├── SUBTASK_hyd_synthesis
│       │   ├── SUBTASK_hyd001
│       │   ├── SUBTASK_hyd002
│       │   ├── SUBTASK_hyd003
│       │   └── SUBTASK_hyd004
│       ├── SUBTASK_axum_mismatch
│       │   ├── SUBTASK_mismatch_synthesis
│       │   ├── SUBTASK_mismatch_detect
│       │   └── SUBTASK_axum_server
│       └── SUBTASK_correctness_synthesis
├── ferric-ssr-r4                 [fork, DAG]  COMPLETED (4 nodes)
│   ├── SUBTASK_b1_hydrate_fix
│   ├── SUBTASK_b2_wasm_tests
│   └── SUBTASK_synthesis_report
├── ferric-async-forms-r3         [fork, DAG]  COMPLETED (6 nodes)
│   ├── SUBTASK_b1_reactive_resource
│   ├── SUBTASK_b2_b3_event_dom  (SUSPENDED)
│   │   ├── SUBTASK_b2_event_handler
│   │   └── SUBTASK_b3_bind_dom
│   └── SUBTASK_synthesis
├── chirp-public-landing-r1       [fork, DAG]  resolved  (1 node)
├── review-ferric-ssr-r2          [fork, DAG]  COMPLETED (34 nodes)
│   ├── SUBTASK_b1_verify
│   ├── SUBTASK_b2_verify
│   ├── SUBTASK_regression  (SUSPENDED)
│   │   ├── SUBTASK_reg_criteria
│   │   ├── SUBTASK_sec_quality
│   │   │   ├── SUBTASK_secq_synthesis
│   │   │   ├── SUBTASK_quality_check  (SUSPENDED)
│   │   │   │   ├── SUBTASK_test_quality
│   │   │   │   ├── SUBTASK_app_quality
│   │   │   │   └── SUBTASK_synthesis
│   │   │   └── SUBTASK_sec_check
│   │   │       ├── SUBTASK_synthesis
│   │   │       ├── SUBTASK_html_inj
│   │   │       ├── SUBTASK_dom_spoof
│   │   │       └── SUBTASK_test_inj
│   │   └── SUBTASK_verdict_synthesis
│   ├── SUBTASK_synthesis
│   ├── SUBTASK_b1-verify
│   ├── SUBTASK_b2-verify
│   └── SUBTASK_regression-quality-sec
│       ├── SUBTASK_security
│       ├── SUBTASK_regression-check
│       ├── SUBTASK_code-quality
│       │   ├── SUBTASK_quality-synthesis
│       │   ├── SUBTASK_app-rs-quality
│       │   └── SUBTASK_hydrate-wasm-quality  (SUSPENDED)
│       │       ├── SUBTASK_dim-duplication
│       │       ├── SUBTASK_dim-naming
│       │       ├── SUBTASK_dim-strings
│       │       ├── SUBTASK_dim-assertions
│       │       ├── SUBTASK_dim-cleanup
│       │       └── SUBTASK_dim-synthesis
│       └── SUBTASK_synthesis
├── review-ferric-async-forms-r3  [fork, DAG]  COMPLETED (32 nodes)
│   ├── SUBTASK_synthesis
│   ├── SUBTASK_correctness_concurrency
│   │   ├── SUBTASK_findings_synthesis
│   │   ├── SUBTASK_b3_form
│   │   ├── SUBTASK_b2_event
│   │   └── SUBTASK_b1_concurrency
│   ├── SUBTASK_security
│   │   ├── SUBTASK_sec_synthesis
│   │   ├── SUBTASK_sec_injection
│   │   ├── SUBTASK_sec_unsafe
│   │   ├── SUBTASK_sec_secrets
│   │   └── SUBTASK_sec_event
│   │       ├── SUBTASK_sec_event_synthesis
│   │       ├── SUBTASK_sec_event_forget
│   │       └── SUBTASK_sec_event_downcast
│   └── SUBTASK_quality_tests_idiom
│       ├── SUBTASK_concern2_quality_design
│       ├── SUBTASK_synthesis_findings
│       ├── SUBTASK_findings_synthesis
│       ├── SUBTASK_concern6_idiom
│       ├── SUBTASK_concern3_tests
│       ├── SUBTASK_concern7_api_stability
│       │   └── SUBTASK_produce_partial_findings
│       ├── SUBTASK_concern2_code_quality
│       │   ├── SUBTASK_synthesis
│       │   ├── SUBTASK_q1_coupling
│       │   ├── SUBTASK_q2_eventhandler
│       │   ├── SUBTASK_q3_gen_counter
│       │   ├── SUBTASK_q4_correct_use
│       │   └── SUBTASK_cq_synthesis
│       └── SUBTASK_qti_synthesis
├── chirp-logged-out              [fork, DAG]  SUSPENDED (13 nodes)
│   ├── SUBTASK_frontend_logged_out
│   ├── SUBTASK_synthesis
│   └── SUBTASK_server_public_timeline  (SUSPENDED)
│       ├── CHILD_skeleton
│       ├── CHILD_in_memory
│       ├── CHILD_postgres
│       └── CHILD_tests  (SUSPENDED)
│           ├── CHILD_write_tests
│           └── CHILD_ci_verify  (FAILED)
│               ├── REMEDIATE_implementation
│               ├── REMEDIATE_write_tests
│               └── REMEDIATE_ci_verify
├── chirp-logged-out-r2           [fork, DAG]  COMPLETED (4 nodes)
│   ├── SUBTASK_server
│   ├── SUBTASK_frontend
│   └── SUBTASK_synthesis
├── chirp-logged-out-r3           [fork, DAG]  COMPLETED (1 node)
├── chirp-logged-out-r4           [fork, DAG]  COMPLETED (12 nodes)
│   ├── SUBTASK_explore_and_setup
│   │   ├── SUBTASK_synthesis
│   │   ├── SUBTASK_git_branch
│   │   ├── SUBTASK_server_analysis
│   │   ├── SUBTASK_ferric_analysis
│   │   ├── SUBTASK_frontend_analysis
│   │   └── SUBTASK_design_analysis
│   ├── SUBTASK_backend
│   ├── SUBTASK_frontend
│   ├── SUBTASK_synthesis
│   └── FIXTASK_frontend_contract
├── chirp-logged-out-r5           [fork, DAG]  SUSPENDED (3 nodes)
│   ├── SUBTASK_discovery
│   └── SUBTASK_synthesis
├── chirp-logged-out-r6           [fork, DAG]  COMPLETED (2 nodes)
│   └── SUBTASK_synthesis
├── chirp-logged-out-r7           [fork, DAG]  COMPLETED (14 nodes)
│   ├── SUBTASK_synthesis
│   ├── SUBTASK_explore-codebase
│   │   ├── SUBTASK_explore-synthesis
│   │   ├── SUBTASK_explore-survey-frontend
│   │   ├── SUBTASK_explore-survey-backend
│   │   ├── SUBTASK_explore-survey-design
│   │   └── SUBTASK_explore-survey-ferric
│   │       ├── SUBTASK_ferric-survey-synthesis
│   │       ├── SUBTASK_ferric-router-survey
│   │       ├── SUBTASK_ferric-ssr-survey
│   │       └── SUBTASK_ferric-async-survey
│   ├── SUBTASK_backend-api
│   └── SUBTASK_frontend-ui
├── chirp-logged-out-r8           [fork, DAG]  COMPLETED (5 nodes)
│   ├── SUBTASK_explore
│   ├── SUBTASK_backend
│   ├── SUBTASK_frontend
│   └── SUBTASK_synthesis
├── chirp-logged-out-r9           [fork, DAG]  COMPLETED (1 node)
├── chirp-logged-out-r10          [fork, DAG]  COMPLETED (1 node)
├── chirp-logged-out-r11          [fork, DAG]  COMPLETED (1 node)
├── chirp-logged-out-r12          [fork, DAG]  COMPLETED (4 nodes)
│   ├── SUBTASK_synthesis
│   ├── SUBTASK_backend_check
│   └── SUBTASK_frontend_check
├── chirp-logged-out-r13          [fork, DAG]  COMPLETED (1 node)
├── chirp-logged-out-r14          [fork, DAG]  COMPLETED (1 node)
├── chirp-logged-out-r15          [fork, DAG]  COMPLETED (1 node)
├── chirp-logged-out-r16          [fork, DAG]  COMPLETED (1 node)
├── chirp-logged-out-r17          [fork, DAG]  COMPLETED (1 node)
├── chirp-logged-out-r18          [fork, DAG]  COMPLETED (1 node)
├── chirp-logged-out-r19          [fork, DAG]  COMPLETED (3 nodes)
│   ├── SUBTASK_synthesis
│   └── SUBTASK_ac-verify-remediate
├── chirp-logged-out-r20          [fork, DAG]  COMPLETED (1 node)
├── chirp-logged-out-r21          [fork, DAG]  COMPLETED (1 node)
├── chirp-logged-out-r22          [fork, DAG]  COMPLETED (1 node)
├── chirp-logged-out-r23          [fork, DAG]  COMPLETED (1 node)
├── chirp-logged-out-r24          [fork, DAG]  COMPLETED (1 node)
├── chirp-logged-out-r25          [fork, DAG]  COMPLETED (1 node)
├── chirp-logged-out-r26          [fork, DAG]  COMPLETED (1 node)
├── review-chirp-logged-out-r1    [fork, DAG]  COMPLETED (36 nodes)
│   ├── synthesis
│   ├── spoke-access-auth
│   ├── spoke-state-machine
│   ├── spoke-ui-states
│   │   ├── SUBTASK_synthesis
│   │   ├── SUBTASK_routing-ctas
│   │   │   ├── SUBTASK_synthesis
│   │   │   ├── SUBTASK_ac4-path
│   │   │   ├── SUBTASK_cta-link
│   │   │   └── SUBTASK_annotation
│   │   └── SUBTASK_landing-states
│   │       ├── SUBTASK_synthesis-findings
│   │       ├── SUBTASK_check-ac2
│   │       ├── SUBTASK_check-ac4p
│   │       └── SUBTASK_check-ac3
│   └── spoke-code-quality
│       ├── spoke-synthesis
│       ├── spoke-prose
│       ├── spoke-correctness  (SUSPENDED)
│       │   ├── SUBTASK_sql-correctness
│       │   ├── SUBTASK_spec-deviation
│       │   └── SUBTASK_synthesis
│       ├── spoke-tests  (SUSPENDED)
│       │   ├── SUBTASK_handler-unit-tests
│       │   ├── SUBTASK_integration-tests
│       │   ├── SUBTASK_frontend-test-validity
│       │   └── SUBTASK_synthesis
│       ├── spoke-code-health
│       │   ├── child-synthesis
│       │   ├── child-dead-code
│       │   └── child-hydrate-scope
│       └── spoke-safety-idiom
│           ├── spoke-safety-synthesis
│           ├── spoke-error-safety
│           └── spoke-rust-idiom
├── chirp-logged-out-r27          [fork, DAG]  COMPLETED (1 node)
└── review-chirp-logged-out-r2    [fork, DAG]  COMPLETED (9 nodes)
    ├── SUBTASK_verify-fixes
    ├── SUBTASK_verify-acs
    │   ├── SUBTASK_synthesis
    │   ├── SUBTASK_ac235-confirm
    │   ├── SUBTASK_ac4-verify
    │   ├── SUBTASK_ac1-verify
    │   └── SUBTASK_acs-gate
    └── SUBTASK_synthesis
```

*(1 `FAILED`, 2 `SUSPENDED`, the rest `COMPLETED` — reconstructed as they actually landed, not idealized.)*

## Reading it

- **`overseer [root, thread]`** → `taskflow/overseer/I0 … I426`: the serial overseer thread, one
  directory per turn (a thread node). It evaluates the board and decides what to fork next —
  zero-token while idle.
- **`<name> [fork, DAG]`** → `taskflow/dags/<name>/`: a forked DAG, one unit of work. Each has a
  `_GLOBAL.md` hub and decomposes into the `SUBTASK_*` children shown beneath it, recursively (up to
  13 levels deep here).
- **`<state> (<n> nodes)`**: the fork's terminal state and live node count, exactly as the
  reconstructor reports per actor; subtask nodes are tagged `(FAILED)` / `(SUSPENDED)` only where they
  did not complete.
- **`max-dag: 1`**: at most one forked DAG is driven at a time; the rest queue in fork order.

## The files *are* the DAG

Every node leaves the same on-disk lifecycle records, and the live engine state is only a cache of them:

| File | Meaning |
|---|---|
| `_BRIEF.md` | the node's task — what it was asked to do |
| `_GLOBAL.md` | a decomposition hub — a parent that split into children |
| `_FORK.md` | a forked root prompt — a new isolated DAG |
| `SYNTHESIS.md` | the fold — a parent validating and folding its children's outputs (a verification gate) |
| `COMPLETE.md` / `FAILURE.md` / `SUSPENSION.md` | terminal state |

Open any `taskflow/dags/<name>/` to see a real decomposition; open
`taskflow/overseer/I<n>/_BRIEF.md` to see the thread's reasoning at that turn.

## Not included

The DAG nodes checked out and compiled real code — the **chirp** app on the **ferric** Rust/WASM
framework. Those git clones and their `cargo` build output are omitted (regenerable, ~8 GB); the code
itself lives in **[`Nousix-LLC/nswe-demo`](https://github.com/Nousix-LLC/nswe-demo)**. What remains
here is the taskflow: the briefs, the decomposition, the syntheses, the lifecycle.
