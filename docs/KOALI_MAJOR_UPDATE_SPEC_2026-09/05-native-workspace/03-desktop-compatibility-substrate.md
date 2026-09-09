# Desktop Compatibility Substrate

> **Status:** Standalone major-update specification — not yet merged into the authoritative Koali/kOA documentation.  
> **Baseline reviewed:** 2026-09-09 snapshots of Koali Spaces, Koali Control Panel, kOA Linux, LevelUpDiag, parallel design plans, and the Senior Architecture Patterns reference.  
> **Authority rule:** Until this package is explicitly adopted, existing repository documentation and contracts remain authoritative. This package defines the proposed target and the delta to close.

The endpoint remains a minimal kOA appliance/session, not GNOME/KDE by default. Native apps require a deliberately qualified micro-desktop substrate.

Target services/protocols include as required by admitted apps:

- Wayland multi-window graphical session;
- user D-Bus;
- audio;
- clipboard;
- XDG config/data/cache locations;
- desktop entries and MIME database;
- OpenURI / file chooser / app chooser portals or equivalent standard interfaces;
- notifications;
- Secret Service compatibility where required;
- accessibility bus support where required;
- DPI/multi-display qualification;
- XWayland only when a conformance app proves it necessary.

Printing, scanners, advanced webcam/screen sharing, remote desktop, and general desktop-environment replacement remain outside this update unless separately admitted.

The substrate should use standard Freedesktop/XDG behavior before introducing Koali-specific equivalents.
