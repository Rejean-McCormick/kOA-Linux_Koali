# Home and Global Surfaces

> **Status:** Standalone major-update specification — not yet merged into the authoritative Koali/kOA documentation.  
> **Baseline reviewed:** 2026-09-09 snapshots of Koali Spaces, Koali Control Panel, kOA Linux, LevelUpDiag, parallel design plans, and the Senior Architecture Patterns reference.  
> **Authority rule:** Until this package is explicitly adopted, existing repository documentation and contracts remain authoritative. This package defines the proposed target and the delta to close.

## Home target

Home contains at most four primary regions:

```text
Continue
Attention
Applications
Space state
```

Each region is conditional and absent when empty.

### Continue

Source: `ResumeProvider` projections. Display a small bounded set of resumable owner contexts. Activation routes back to the owner.

### Attention

Source: Task projections and only semantically stable counters. Koali summarizes; it does not become the task engine.

### Applications

Source: admitted hosted modules + local native application projection. No hardcoded product cards in Home.

### Space state

Source: runtime state + bounded `StatusProvider` projections. Keep the default view calm; deeper technical details route to Health.

## Search

Federated read projection from registered owner providers. Koali may normalize/rank/present results, but does not crawl owner databases or profiles.

## Tasks

Aggregated work queue only. State-changing actions remain with the owner.

## Health

Technical runtime/readiness/provider information. Health does not grant permissions and should expose degradation that Home intentionally hides.

## Settings

Settings becomes the owner of user presentation preferences plus other Koali presentation settings that are explicitly local/user-owned.
