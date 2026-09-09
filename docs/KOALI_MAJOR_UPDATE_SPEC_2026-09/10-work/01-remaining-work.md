# Remaining Work Register

> **Status:** Standalone major-update specification — not yet merged into the authoritative Koali/kOA documentation.  
> **Baseline reviewed:** 2026-09-09 snapshots of Koali Spaces, Koali Control Panel, kOA Linux, LevelUpDiag, parallel design plans, and the Senior Architecture Patterns reference.  
> **Authority rule:** Until this package is explicitly adopted, existing repository documentation and contracts remain authoritative. This package defines the proposed target and the delta to close.

This is the primary implementation checklist. Status reflects the reviewed 2026-09-09 snapshots and should be updated as work lands.

Legend: `[ ]` missing/not completed; `[~]` specified/partial but canonical adoption or implementation remains; `[x]` baseline already substantially exists and is intended to be preserved.

## WS-A — Governance and contracts

- [~] **KMA-001** Four authority planes are defined in this standalone package; canonical repository adoption/merge remains.
- [~] **KMA-002** Space state vs user presentation preference authority is defined here; canonical contracts/implementation remain.
- [ ] **KMA-003** Define `SpaceAppearancePolicy` contract or compatible extension strategy.
- [ ] **KMA-004** Define `UserPresentationPreferences` persistence/contract boundary.
- [ ] **KMA-005** Correct topbar/sidebar widget contract so `projection_ref` is separate from `activation`.
- [~] **KMA-006** Provider execution envelope is defined here conceptually; canonical types/contracts/runtime remain.
- [~] **KMA-007** Native application admission-policy semantics are defined here; canonical kOA contract remains.
- [~] **KMA-008** Native application data/rollback semantics are defined here; canonical kOA contract remains.
- [~] **KMA-009** `UserSessionAppBroker` authority/locality is defined here; canonical interface/implementation remain.
- [~] **KMA-010** Observability envelope requirements are defined here; canonical field contract/instrumentation remain.
- [~] **KMA-011** Idempotency requirement is defined here; per-operation canonical semantics/tests remain.
- [ ] **KMA-012** Decide canonical URL encoding for Koali surface-selection state.
- [ ] **KMA-013** Add ADRs for authority-moving decisions when merged into canonical repos.

## WS-B — Appearance/preferences

- [x] **KMA-020** Theme provider/token architecture exists.
- [~] **KMA-021** Base theme variants exist but do not yet provide a complete user-facing appearance system.
- [ ] **KMA-022** Implement system/light/dark effective mode with Ant Design algorithms.
- [ ] **KMA-023** Replace hardcoded light colors with semantic tokens/CSS variables.
- [ ] **KMA-024** Implement bounded accent palette.
- [ ] **KMA-025** Implement `minimal` / `outlined` / `elevated` surface token modes.
- [ ] **KMA-026** Implement compact/comfortable/touch density as user preference under Space policy.
- [ ] **KMA-027** Turn Settings into real preference controls.
- [ ] **KMA-028** Persist user preferences separately from Space activation.
- [ ] **KMA-029** Add tests proving preference changes do not change activation authority/digests.

## WS-C — Shell and Home

- [x] **KMA-030** Global shell/module selector/sidebar/topbar primitives exist.
- [ ] **KMA-031** Hide empty owner sidebar and avoid empty mobile drawer.
- [ ] **KMA-032** Reduce technical status noise in normal topbar.
- [ ] **KMA-033** Implement conditional shell/global sections.
- [ ] **KMA-034** Build Home target: Continue / Attention / Applications / Space state.
- [ ] **KMA-035** Add unified launcher view model for hosted modules + native projections without merging authorities.
- [ ] **KMA-036** Implement addressable/restorable surface selection.
- [ ] **KMA-037** Complete sidebar icon/badge projection behavior where contracts declare it.
- [ ] **KMA-038** Complete topbar status/counter rendering under corrected projection-binding contract.

## WS-D — GlobalProjectionRuntime

- [x] **KMA-040** SearchProvider and TaskProvider core execution model exists.
- [ ] **KMA-041** Refactor shared provider execution runtime without erasing type-specific contracts.
- [ ] **KMA-042** Implement ResumeProvider end to end.
- [ ] **KMA-043** Implement StatusProvider end to end.
- [ ] **KMA-044** Implement CounterProvider only for independent stable semantics.
- [ ] **KMA-045** Add `/api/global/overview`.
- [ ] **KMA-046** Add provider state/freshness metadata.
- [ ] **KMA-047** Enforce global/per-owner/per-provider concurrency limits.
- [ ] **KMA-048** Implement timeout-budget propagation for remote/fan-out work.
- [ ] **KMA-049** Add remote circuit breaker where owner adapters need it.
- [ ] **KMA-050** Add bounded background retry/backoff+jitter where appropriate.
- [ ] **KMA-051** Implement staleness/cache-aside semantics with policy opt-in.
- [ ] **KMA-052** Add load-shedding/rate-limit rules for expensive projection endpoints.

## WS-E — Generic hosted onboarding

- [x] **KMA-060** Manifest, ACP, runtime-registration concepts and runtime validation primitives exist.
- [ ] **KMA-061** Specify/implement Koali-owned `SpaceActivationCompiler` around existing validators/control server.
- [ ] **KMA-062** Keep Integration Package as packaging/reference only, never new authority.
- [ ] **KMA-063** Add structured compiler diagnostics and conformance/activation receipt linkage.
- [ ] **KMA-064** Ensure control mutations are idempotent where semantics permit.
- [ ] **KMA-065** Add generic multi-module removal/failure/origin tests.
- [ ] **KMA-066** Expose stable invocation surface for Control Panel without moving compiler logic into Control Panel.

## WS-F — Hosted conformance applications

- [~] **KMA-070** Konnaxion development pilot is navigable.
- [ ] **KMA-071** Move canonical Konnaxion manifest ownership out of Control Panel.
- [ ] **KMA-072** Complete real Konnaxion ACP/evidence and runtime ownership split.
- [ ] **KMA-073** Add useful Konnaxion Search/Resume and only meaningful Status projections.
- [ ] **KMA-074** Delete Konnaxion-specific pilot manifest/runtime path after generic parity.
- [ ] **KMA-075** Create/validate Médiathèque ACP/runtime integration.
- [ ] **KMA-076** Qualify Streamlit/WebSocket/XSRF/base-path/download/storage behavior generically.
- [ ] **KMA-077** Requalify official Orgo UI/runtime before final ACP.
- [ ] **KMA-078** Add Orgo Task/Resume/Status projections; actions remain owner-owned.
- [ ] **KMA-079** Prove fourth hosted integration has substantially lower marginal cost.

## WS-G/H/I — Native Workspace

- [x] **KMA-080** kOA graphical session/profile/resource/security/release foundations exist.
- [ ] **KMA-081** Add explicit native-workspace capability and profile/overlay matrix.
- [ ] **KMA-082** Implement Native Application Admission Policy using desktop-entry references.
- [ ] **KMA-083** Implement unprivileged endpoint-local `UserSessionAppBroker`.
- [ ] **KMA-084** Add Koali local native-app projection/list API.
- [ ] **KMA-085** Add Koali native launch API with safe high-level actions and rate limiting.
- [ ] **KMA-086** Qualify user D-Bus/audio/clipboard/XDG/portals/MIME/notifications/secrets substrate.
- [ ] **KMA-087** Decide/qualify file-manager conformance application.
- [ ] **KMA-088** Map native app classes to existing security controls/LSM.
- [ ] **KMA-089** Map native apps to Resource Governor envelopes and stress-test Koali priority.
- [ ] **KMA-090** Add NativeApplicationDataPolicy and integrate existing backup/restore verification.
- [ ] **KMA-091** Qualify VLC conformance suite.
- [ ] **KMA-092** Qualify Firefox conformance suite.
- [ ] **KMA-093** Qualify LibreOffice conformance suite.
- [ ] **KMA-094** Qualify Thunderbird + Secret Service + cross-app attachment/URL handoff.
- [ ] **KMA-095** Prove sixth compatible native app mostly requires policy + evidence, not broker code.
- [ ] **KMA-096** Define critical native-app security-update SLO and verify release cadence can satisfy it.

## WS-J — Development Environment / DevPad

- [x] **KMA-100** Control Panel development orchestration/backends/workspaces exist.
- [ ] **KMA-101** Create DevPad architecture around EditorDocument/Storage/Session/View.
- [ ] **KMA-102** Implement reliable editor/session/atomic-save/recovery behavior.
- [ ] **KMA-103** Add explicit `edit_root` / `execution_root` awareness.
- [ ] **KMA-104** Add SmartDump adapter without reimplementation.
- [ ] **KMA-105** Add File Puller adapter after verifying its real interface.
- [ ] **KMA-106** Implement Context Cart / AI Change Set / Context Profiles.
- [ ] **KMA-107** Implement Paste as File with preview and recovery point.
- [ ] **KMA-108** Add context safety checks for likely secrets/private runtime data.
- [ ] **KMA-109** Add narrow Control Panel IPC only as delegation to existing operations.
- [ ] **KMA-110** Prove repos remain fully operable when DevPad is absent.

## WS-K — Observability and conformance

- [~] **KMA-120** Health/readiness/runtime diagnostics exist in several subsystems.
- [ ] **KMA-121** Standardize boundary structured-log fields without creating a monolithic log service requirement.
- [ ] **KMA-122** Add correlation/trace propagation across Koali ↔ remote owner/service calls.
- [ ] **KMA-123** Add provider latency/error/saturation metrics and bulkhead rejection metrics.
- [ ] **KMA-124** Add native broker launch/error/saturation metrics.
- [ ] **KMA-125** Add activation/compiler duration/failure/idempotency evidence.
- [ ] **KMA-126** Extend LevelUpDiag only where diagnostic ownership fits its boundary; do not turn it into an orchestrator.
- [ ] **KMA-127** Add cross-repo conformance recipes/receipts for hosted/native/distributed scenarios.

## WS-L — Distributed/VPS qualification

- [ ] **KMA-130** Qualify reverse proxy/TLS/CSP/origin/redirect behavior in real network topology.
- [ ] **KMA-131** Qualify WebSocket stacks and cookies/storage through chosen transport/proxy.
- [ ] **KMA-132** Qualify remote provider timeout/circuit/degradation behavior.
- [ ] **KMA-133** Add deployment-safe blue-green/canary policy only for services where justified.
- [ ] **KMA-134** Qualify backup/restore/rollback and partial outage in distributed Space.
- [ ] **KMA-135** Verify no implicit remote native-exec path exists.
