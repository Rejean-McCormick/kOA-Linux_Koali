# Logs, Metrics, and Tracing

> **Status:** Standalone major-update specification — not yet merged into the authoritative Koali/kOA documentation.  
> **Baseline reviewed:** 2026-09-09 snapshots of Koali Spaces, Koali Control Panel, kOA Linux, LevelUpDiag, parallel design plans, and the Senior Architecture Patterns reference.  
> **Authority rule:** Until this package is explicitly adopted, existing repository documentation and contracts remain authoritative. This package defines the proposed target and the delta to close.

## Structured logs

Prefer stable fields and error classes over prose-only logs. Human-readable messages may be included but must not be the only machine signal.

## Correlation

Generate/propagate correlation context at request entry points. Network calls between Koali and remote owners/services propagate a standard trace context where feasible (for example W3C Trace Context).

## Tracing scope

Do not instrument every local function for the sake of tracing. Trace distributed boundaries that materially help diagnose latency/failure.

## Metrics scope

Measure what informs capacity and failure behavior. Avoid dashboard graveyards. Each production alert should correspond to an operator/user symptom or an approaching hard limit.

## Security

Observability data is itself governed data. Logs/traces must respect kOA privacy, disclosure, and selective-audit boundaries.
