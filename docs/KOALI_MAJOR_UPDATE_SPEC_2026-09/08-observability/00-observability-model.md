# Observability Model

> **Status:** Standalone major-update specification — not yet merged into the authoritative Koali/kOA documentation.  
> **Baseline reviewed:** 2026-09-09 snapshots of Koali Spaces, Koali Control Panel, kOA Linux, LevelUpDiag, parallel design plans, and the Senior Architecture Patterns reference.  
> **Authority rule:** Until this package is explicitly adopted, existing repository documentation and contracts remain authoritative. This package defines the proposed target and the delta to close.

Observability is a cross-cutting requirement of the update, especially at owner/network/native-launch boundaries.

## Common event context

Boundary events should carry where applicable:

- `operation_id`;
- `correlation_id` / trace context;
- component;
- owner/module/app id;
- provider or runtime id;
- result/state;
- duration;
- error class;
- degraded/stale indicators.

Do not log credentials, tokens, private content, or unnecessary PII.

## Golden Signals

Critical components expose actionable:

- latency;
- traffic;
- errors;
- saturation.

Examples:

- provider p95/p99 latency and timeout rate;
- provider bulkhead saturation/rejection;
- runtime unavailable/origin rejection counts;
- native launch success/error and broker queue saturation;
- Space activation duration/failure;
- remote transport circuit state.

## User UX versus operations

The UI may intentionally hide non-actionable technical noise. Operations must still be able to distinguish empty, stale, degraded, failed, and unavailable states.
