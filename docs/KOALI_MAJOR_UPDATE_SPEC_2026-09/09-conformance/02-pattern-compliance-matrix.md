# Reference Pattern Compliance Matrix

> **Status:** Standalone major-update specification — not yet merged into the authoritative Koali/kOA documentation.  
> **Baseline reviewed:** 2026-09-09 snapshots of Koali Spaces, Koali Control Panel, kOA Linux, LevelUpDiag, parallel design plans, and the Senior Architecture Patterns reference.  
> **Authority rule:** Until this package is explicitly adopted, existing repository documentation and contracts remain authoritative. This package defines the proposed target and the delta to close.

| Pattern | Required? | Concrete use | Do not over-apply |
|---|---:|---|---|
| Circuit Breaker | Yes, selective | remote owner/service boundaries | local functions |
| Bulkhead | Yes | provider fan-out; native resource envelopes | separate process per tiny feature |
| Backoff + jitter | Yes, selective | background reconnect/recovery | blocking user retries |
| Graceful degradation | Yes | partial owner/provider/native failure | silent operational failure |
| Rate limiting | Yes, selective | exposed/expensive endpoints, launch storms | trivial local reads |
| Timeout budgets | Yes | interactive distributed/fan-out calls | unrelated static config |
| Strangler Fig | Yes | Konnaxion pilot migration | permanent dual path |
| Anti-Corruption Layer | Yes | owner/native model translation | redundant mapping layers |
| Hexagonal | Yes | real external boundaries/adapters | abstraction for every class |
| BFF | Yes | Koali GlobalProjectionRuntime | universal platform API |
| Modular Monolith | Yes | Koali Spaces | forced microservices |
| CQRS principle | Partial | projections read; mutations owner-owned | full CQRS/event stack |
| Idempotency | Yes, semantic | activation/deactivation/policy operations | `launch` pretending to be idempotent |
| Cache-aside | Selective | allowed projection cache | sensitive/authoritative owner data |
| Health checks | Yes | liveness/readiness/user-status separation | health as authorization |
| Tracing | Selective | network boundaries | every in-process function |
| Structured logs | Yes | boundary and control events | secrets/PII dumps |
| Metrics | Yes | golden signals | dashboard graveyard |
| Blue-green/canary | Selective | remote service deployment | unnecessary endpoint complexity |
| Immutable infrastructure | Yes | existing kOA image/release model | mutable ad hoc endpoint changes |
| Event sourcing/Saga/Outbox/PubSub/DLQ | No current requirement | — | adding because system is distributed |
