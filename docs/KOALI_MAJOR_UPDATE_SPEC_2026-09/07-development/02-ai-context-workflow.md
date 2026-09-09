# AI Context Workflow

> **Status:** Standalone major-update specification — not yet merged into the authoritative Koali/kOA documentation.  
> **Baseline reviewed:** 2026-09-09 snapshots of Koali Spaces, Koali Control Panel, kOA Linux, LevelUpDiag, parallel design plans, and the Senior Architecture Patterns reference.  
> **Authority rule:** Until this package is explicitly adopted, existing repository documentation and contracts remain authoritative. This package defines the proposed target and the delta to close.

The external-AI boundary remains explicit:

```text
ChatGPT
  ↕ clipboard / files
DevPad
  ↕ local source and context artifacts
Control Panel / repository validators
```

## SmartDump

Used for broad/horizontal architecture context and full snapshots. DevPad adapts the existing tool rather than reimplementing it.

## File Puller

Used for targeted/vertical context. It becomes the main engine behind Context Cart exports where compatible with its actual interface.

## Context Cart sources

- open files;
- selected files;
- modified files / AI Change Set;
- diagnostics/failures;
- explicit architecture context profile;
- full snapshot.

## Safety check

Before context export, block or require explicit handling of likely secrets/private runtime data such as `.env`, keys, credentials, private DBs, tokens, and user runtime stores.

No silent content sanitization: exclusions are explicit and reported.

## Workspace roots

Dev tooling must distinguish `edit_root` and `execution_root`; no heuristic silently chooses which workspace is authoritative for editing.
