# Native Application Admission Policy

> **Status:** Standalone major-update specification — not yet merged into the authoritative Koali/kOA documentation.  
> **Baseline reviewed:** 2026-09-09 snapshots of Koali Spaces, Koali Control Panel, kOA Linux, LevelUpDiag, parallel design plans, and the Senior Architecture Patterns reference.  
> **Authority rule:** Until this package is explicitly adopted, existing repository documentation and contracts remain authoritative. This package defines the proposed target and the delta to close.

The update does **not** create a full native application catalog that duplicates Freedesktop metadata.

Instead, kOA owns a **Native Application Admission Policy Catalog** referencing existing desktop entries.

Conceptual example:

```yaml
app_id: firefox
desktop_entry_ref: firefox.desktop

admission:
  capability: user.native_workspace

policy:
  class: web
  resource_envelope: interactive.web
  network: required

data:
  profile: persistent
  cache: disposable

launch:
  allowed_actions:
    - open
```

## Desktop metadata authority

`.desktop`, MIME databases, icons, localized names, and standard associations remain owned by the desktop/Freedesktop mechanisms.

kOA contributes only:

- profile/capability admission;
- security class;
- resource envelope;
- data/offline policy;
- allowed action policy;
- optional product-level presentation override when strictly necessary.

## Koali projection

Koali receives a minimized safe view such as app id, display label/icon reference, availability, and allowed high-level actions. It never receives arbitrary `Exec=` content for frontend execution.
