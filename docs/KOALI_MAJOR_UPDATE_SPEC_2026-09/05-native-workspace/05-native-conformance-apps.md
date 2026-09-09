# Native Conformance Applications

> **Status:** Standalone major-update specification — not yet merged into the authoritative Koali/kOA documentation.  
> **Baseline reviewed:** 2026-09-09 snapshots of Koali Spaces, Koali Control Panel, kOA Linux, LevelUpDiag, parallel design plans, and the Senior Architecture Patterns reference.  
> **Authority rule:** Until this package is explicitly adopted, existing repository documentation and contracts remain authoritative. This package defines the proposed target and the delta to close.

Native applications are **permanent conformance fixtures**, not implementation phases.

## VLC

Proves Wayland windowing, audio/video, GPU, local files, MIME/open-with, fullscreen, and crash isolation.

## Firefox

Proves network/HTTPS, URI handler, downloads, clipboard, file chooser, certificates/policies, persistent profile, and web media.

## LibreOffice

Proves complex MIME handling, open/save, file chooser, persistent profile, import/export, and document workflows.

## Thunderbird

Proves network + persistent mail profile, Secret Service needs, notifications, `mailto`, URL handoff, and attachment handoff.

## Files application

Proves filesystem navigation, Open With, permitted volumes, and removable-media behavior when the profile allows it. The exact file-manager product remains an explicit technical selection rather than an architecture assumption.

## Cross-application proof

```text
Thunderbird URL            → Firefox
Thunderbird attachment.odt → LibreOffice
Thunderbird attachment.mp4 → VLC
```

## Marginal-cost gate

After these fixtures, the next compatible native application should require mostly:

- admission policy;
- security/resource/data mapping;
- conformance evidence;

not a new launch architecture.
