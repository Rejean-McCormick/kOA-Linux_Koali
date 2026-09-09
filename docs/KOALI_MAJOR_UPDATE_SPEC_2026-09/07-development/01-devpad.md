# DevPad Target

> **Status:** Standalone major-update specification — not yet merged into the authoritative Koali/kOA documentation.  
> **Baseline reviewed:** 2026-09-09 snapshots of Koali Spaces, Koali Control Panel, kOA Linux, LevelUpDiag, parallel design plans, and the Senior Architecture Patterns reference.  
> **Authority rule:** Until this package is explicitly adopted, existing repository documentation and contracts remain authoritative. This package defines the proposed target and the delta to close.

DevPad is a small, reliable editor/context tool optimized for the actual ChatGPT → edit → validate → context loop. It is not a general IDE initiative.

## Core abstractions

```text
EditorDocument
EditorStorage
EditorSession
EditorView
```

The UI technology is replaceable. The architecture must not depend on Tk Text, Scintilla, CodeMirror, or another widget.

## Required behavior

- tabs and session restoration;
- open/save/save-all;
- find/replace/goto;
- undo/redo;
- encoding and BOM preservation;
- CRLF/LF preservation;
- external modification detection;
- atomic save;
- recovery journal outside repositories;
- read-only support;
- large paste handling;
- `Paste as File` preview/confirmation;
- Context Cart and tool adapters.

## Invariant

No silent source transformation:

- no auto-format;
- no automatic EOL normalization;
- no automatic encoding changes;
- no background AI rewrite.

## Dependency rule

If DevPad is absent, every repository must still build, validate, test, diagnose, and release through canonical commands.
