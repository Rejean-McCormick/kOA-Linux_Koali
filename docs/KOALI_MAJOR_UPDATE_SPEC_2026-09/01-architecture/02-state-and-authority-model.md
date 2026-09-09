# State and Authority Model

> **Status:** Standalone major-update specification — not yet merged into the authoritative Koali/kOA documentation.  
> **Baseline reviewed:** 2026-09-09 snapshots of Koali Spaces, Koali Control Panel, kOA Linux, LevelUpDiag, parallel design plans, and the Senior Architecture Patterns reference.  
> **Authority rule:** Until this package is explicitly adopted, existing repository documentation and contracts remain authoritative. This package defines the proposed target and the delta to close.

The update separates state into explicit domains.

| State domain | Authority | Examples |
|---|---|---|
| Space definition | Koali/kOA activation input | admitted modules, base theme/default density, capability projection |
| Owner manifest | owner application | routes, sidebar, widgets, surface profiles |
| ACP/evidence | integration qualification | auth/browser/offline/lifecycle/health evidence |
| Runtime registration | environment/control runtime | transport, local target, runtime reference, readiness binding |
| User presentation | Koali local/user state | light/dark/system, accent, density, surface style |
| Owner business state | owner | tasks, documents, workflows, auth decisions |
| Native desktop metadata | desktop/Freedesktop | `.desktop`, MIME, icon, localized app name |
| Native admission policy | kOA | allowed profiles/capabilities/actions/resources/data policy |
| Release state | kOA release system | image/service/governance/Kristal channels, provenance, rollback |

## Critical separation: Space versus user preferences

```text
SpaceDefinition / activation
          │
          ├── deterministic shared defaults
          │
          └── does NOT contain personal runtime choices

UserPresentationPreferences
          │
          └── local/personal choices only
```

Changing from light to dark must not create a new Space activation receipt or alter owner conformance evidence.

## Critical separation: widget data versus action

```text
projection_ref → where the widget obtains display data
activation     → what happens on user interaction
```

A counter may be provided by Orgo and open an Orgo route. These are related but independent contracts.
