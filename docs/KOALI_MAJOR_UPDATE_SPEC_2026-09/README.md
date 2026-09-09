# Koali Major Update — Standalone Target Specification

> **Status:** Standalone major-update specification — not yet merged into the authoritative Koali/kOA documentation.  
> **Baseline reviewed:** 2026-09-09 snapshots of Koali Spaces, Koali Control Panel, kOA Linux, LevelUpDiag, parallel design plans, and the Senior Architecture Patterns reference.  
> **Authority rule:** Until this package is explicitly adopted, existing repository documentation and contracts remain authoritative. This package defines the proposed target and the delta to close.

This documentation bundle defines the **major Koali upgrade target** as a separate specification so that the target architecture, required changes, and remaining work can be reviewed without blurring the current authoritative documentation.

It is intentionally **not a phase roadmap**. The system is defined as a final target. Implementation work is organized into workstreams and dependency edges only.

## Why this bundle exists

The current Koali Spaces core is substantially more mature than the visible multi-application product experience. The reviewed baseline already contains a generic Surface Layer, `ApplicationHost`, server-side runtime registry, origin/URL policy, activation receipts, standalone packaging, shell/global routes, and Search/Tasks provider execution. The main gaps are now integration ownership, generic onboarding, missing global projections, product UX, native-workspace integration, resilience/observability hardening, and development workflow integration.

This update therefore **extends and clarifies the existing architecture** instead of introducing a replacement framework.

## Target in one sentence

> **Koali presents the Space; owner applications own their business behavior; kOA Linux authorizes and executes platform capabilities; development tooling remains a separate, non-authoritative plane.**

## Four authority planes

```text
1. EXPERIENCE PLANE
   Koali Spaces
   presentation / shell / global projections / user preferences

2. APPLICATION PLANE
   hosted owner apps + native applications
   owner UI/data/workflows + kOA native admission policy

3. PLATFORM PLANE
   kOA Linux
   profiles / session / security / resources / storage / release / recovery

4. DEVELOPMENT PLANE
   Control Panel / DevPad / SmartDump / File Puller / LevelUpDiag
   development orchestration and diagnostics only
```

Contracts, resilience, observability, conformance, security, and recovery are **cross-cutting concerns**, not additional authority planes.

## Start here

1. [`00-governance/00-status-and-authority.md`](00-governance/00-status-and-authority.md)
2. [`00-governance/02-architecture-invariants.md`](00-governance/02-architecture-invariants.md)
3. [`01-architecture/00-system-target.md`](01-architecture/00-system-target.md)
4. [`01-architecture/04-reference-patterns.md`](01-architecture/04-reference-patterns.md)
5. [`10-work/01-remaining-work.md`](10-work/01-remaining-work.md)
6. [`09-conformance/00-system-definition-of-done.md`](09-conformance/00-system-definition-of-done.md)

## Reading rule

Documents use four labels:

- **TARGET** — normative behavior proposed by this update.
- **BASELINE** — observed behavior from the reviewed snapshots.
- **DELTA** — required change from baseline to target.
- **NON-GOAL** — explicitly excluded from this update.

The most useful operational document while implementing the update is [`10-work/01-remaining-work.md`](10-work/01-remaining-work.md). It is deliberately explicit so completed items can be checked off while this bundle remains separate from the canonical docs.
