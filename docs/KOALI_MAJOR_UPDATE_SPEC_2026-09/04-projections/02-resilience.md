# Projection Resilience Policy

> **Status:** Standalone major-update specification — not yet merged into the authoritative Koali/kOA documentation.  
> **Baseline reviewed:** 2026-09-09 snapshots of Koali Spaces, Koali Control Panel, kOA Linux, LevelUpDiag, parallel design plans, and the Senior Architecture Patterns reference.  
> **Authority rule:** Until this package is explicitly adopted, existing repository documentation and contracts remain authoritative. This package defines the proposed target and the delta to close.

Resilience controls protect the Space from downstream failure without decorating local calls with unnecessary frameworks.

## Timeout budgets

Every interactive global request receives an end-to-end deadline. Providers receive a bounded portion of the remaining budget. Downstream adapters must not start work that cannot complete within the remaining budget.

## Bulkheads

At minimum:

- global in-flight provider ceiling;
- per-owner limit;
- per-provider limit;
- bounded queue or immediate load shedding.

`Promise.allSettled` remains useful for result isolation but is not a substitute for resource isolation.

## Circuit breakers

Use only for remote/unreliable boundaries where repeated failures would otherwise waste resources. Do not add circuit breakers around local registry lookups or ordinary in-process functions.

## Retry policy

Interactive path:

```text
bounded attempt → timeout/failure → degraded response
```

Background recovery path:

```text
retryable failure → exponential backoff + jitter → bounded attempts / circuit state
```

## Rate limiting

Apply at expensive/exposed boundaries, including public/remote APIs where appropriate and local native-launch endpoints to prevent accidental launch storms.

## Degradation rule

A failed provider is distinguishable operationally from an empty valid result even if the end-user surface chooses not to show an error banner.
