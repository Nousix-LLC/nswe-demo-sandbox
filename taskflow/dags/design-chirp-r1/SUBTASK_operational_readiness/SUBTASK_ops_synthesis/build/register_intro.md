## requirements_and_acceptance_criteria

This is the consolidated `REQ-OPS-*` register: the verbatim union of the five concern sections' requirements,
collected in one place in id order. Each requirement is stated once above, in the concern section that owns
it, and once here, so the register is the single list a release check or a downstream code DAG can read
end to end. Every requirement carries a `statement`, a testable `acceptance_criteria`, a `verification_method`
from the vocabulary (`manual_user_check`, `automated_test`, `inspection`, `operational_check`), a
`release_gating` flag, and a `traces_to` the product/domain requirement it refines (empty for an OPS-internal
requirement). The number space is partitioned by concern — durable data `001..019`, backups and recovery
`020..039`, limits and quotas `040..059`, observability `060..079`, status and incident `080..099` — and no
number is used twice.
