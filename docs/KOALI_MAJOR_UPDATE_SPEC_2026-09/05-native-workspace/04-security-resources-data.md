# Native App Security, Resources, and Data Policy

> **Status:** Standalone major-update specification — not yet merged into the authoritative Koali/kOA documentation.  
> **Baseline reviewed:** 2026-09-09 snapshots of Koali Spaces, Koali Control Panel, kOA Linux, LevelUpDiag, parallel design plans, and the Senior Architecture Patterns reference.  
> **Authority rule:** Until this package is explicitly adopted, existing repository documentation and contracts remain authoritative. This package defines the proposed target and the delta to close.

Native app integration is designed with policy from the start rather than retrofitted after functional success.

## Security classes

At minimum evaluate classes such as:

- web;
- mail;
- office;
- media;
- files.

Each class maps to explicit policy for filesystem, network, audio, GPU, notifications, and secrets.

## Resource policy

Reuse the existing kOA Resource Governor and resource-envelope model. Example intent:

```text
Koali shell         critical-interactive
Firefox             interactive-web
VLC                 foreground-media
LibreOffice         interactive-office
Thunderbird         background-interactive
```

A resource-intensive app must not starve Koali itself.

## Data policy

Define `NativeApplicationDataPolicy` rather than implementing a second backup engine.

Separate:

- binary;
- user documents;
- persistent app profile;
- cache;
- temporary state.

Example concepts:

```yaml
profile: persistent
cache: disposable
rollback:
  requires_compatible_profile: true
upgrade:
  checkpoint_when_required: true
```

Existing kOA backup/restore and restore-verification machinery executes the policy.

## Secrets

Koali never stores owner/native credentials. Where desktop apps require Secret Service behavior, kOA provides/qualifies a compatible substrate under platform security authority.
