# Final System Target

> **Status:** Standalone major-update specification — not yet merged into the authoritative Koali/kOA documentation.  
> **Baseline reviewed:** 2026-09-09 snapshots of Koali Spaces, Koali Control Panel, kOA Linux, LevelUpDiag, parallel design plans, and the Senior Architecture Patterns reference.  
> **Authority rule:** Until this package is explicitly adopted, existing repository documentation and contracts remain authoritative. This package defines the proposed target and the delta to close.

## TARGET

```text
                              USER
                               │
                               ▼
                    ┌────────────────────┐
                    │    KOALI SPACES    │
                    │                    │
                    │ Experience         │
                    │ Presentation       │
                    │ Global projections │
                    │ User preferences   │
                    └─────────┬──────────┘
                              │
                ┌─────────────┴─────────────┐
                │                           │
                ▼                           ▼
      ┌────────────────────┐      ┌──────────────────────┐
      │ Hosted integration │      │ Native projection    │
      │                    │      │                      │
      │ Manifest           │      │ desktop metadata     │
      │ ACP                │      │ + kOA admission      │
      │ RuntimeRegistration│      │ + session availability│
      └─────────┬──────────┘      └──────────┬───────────┘
                │                            │
                ▼                            ▼
       owner applications             UserSessionAppBroker
                │                            │
                └────────────┬───────────────┘
                             ▼
                    ┌────────────────┐
                    │    kOA Linux   │
                    │ profiles       │
                    │ session        │
                    │ security       │
                    │ resources      │
                    │ storage        │
                    │ networking     │
                    │ release        │
                    │ recovery       │
                    └────────────────┘

DEVELOPMENT — separate authority

ChatGPT ⇄ clipboard/files ⇄ DevPad
                              │
                     SmartDump / File Puller
                              │
                              ▼
                       Control Panel
                              │
                     repository commands
```

## Architectural objective

A user sees one coherent Space while the underlying systems remain independently authoritative and independently degradable.

The architecture optimizes for:

- generic integration rather than product-specific branching;
- explicit authority rather than convenient duplication;
- local-first endpoint behavior without pretending remote services are local;
- graceful partial failure;
- low marginal onboarding cost;
- observable and testable boundaries;
- compatibility with existing Koali/kOA contracts.

## BASELINE

Koali Spaces already has the key hosted-rendering primitives. kOA Linux already has profile/session/security/resource/release concepts. Control Panel already delegates important repository-owned operations. Therefore the update should be a **major integration and authority clarification**, not a platform rewrite.
