# Architecture Pattern Alignment

> **Status:** Standalone major-update specification — not yet merged into the authoritative Koali/kOA documentation.  
> **Baseline reviewed:** 2026-09-09 snapshots of Koali Spaces, Koali Control Panel, kOA Linux, LevelUpDiag, parallel design plans, and the Senior Architecture Patterns reference.  
> **Authority rule:** Until this package is explicitly adopted, existing repository documentation and contracts remain authoritative. This package defines the proposed target and the delta to close.

This update uses the Senior Architecture Patterns reference as a **decision aid**, not a checklist of technologies to install.

## Patterns intentionally applied

| Pattern | Application in this update |
|---|---|
| Anti-Corruption Layer | owner/native-specific models are translated into Koali projections/policies |
| Hexagonal / Ports & Adapters | runtime, providers, native projection, DevPad tool adapters |
| Backend for Frontend | GlobalProjectionRuntime serves Koali presentation only |
| Modular Monolith | Koali Spaces remains one deployable application with internal modules |
| Bulkhead | bounded concurrency per provider/owner and resource governance for native workloads |
| Graceful Degradation | missing provider/owner/native workspace degrades locally |
| Timeout Budgets | bounded end-to-end remote/fan-out request deadlines |
| Circuit Breaker | remote owner/service calls only where repeated failure is meaningful |
| Backoff + Jitter | background recovery/reconnect/polling, not long interactive retry chains |
| Rate Limiting | externally exposed/expensive endpoints and native launch abuse protection |
| Idempotency | activation/deactivation/policy/control mutations where semantics permit |
| Cache-Aside | bounded provider projection caching with staleness policy |
| Health Check API | liveness/readiness separated from user status and authorization |
| Structured Logging | machine-readable boundary events with correlation context |
| Distributed Tracing | network boundaries in distributed Space topology |
| Metrics / Golden Signals | latency, traffic, errors, saturation on critical paths |
| Immutable Infrastructure | existing kOA signed image/release architecture |
| Strangler Fig | migrate Konnaxion pilot to generic activation path, then delete fallback |

## Patterns deliberately not introduced without need

- Event Sourcing
- Saga orchestration
- Transactional Outbox
- Pub/Sub and DLQ
- Claim Check
- Sharding
- Service Mesh
- Data Mesh
- Cell-based architecture
- CDN as an architectural requirement

Their absence is intentional. Multiple applications do not by themselves justify asynchronous/distributed complexity.

## Anti-patterns explicitly avoided

- distributed monolith;
- microservices-first decomposition;
- universal API for every client;
- abstraction overdose;
- infinite retry loops;
- silent degradation;
- configuration drift;
- zombie migration paths;
- dashboard proliferation without actionable signals.
