# Appearance and User Preferences

> **Status:** Standalone major-update specification — not yet merged into the authoritative Koali/kOA documentation.  
> **Baseline reviewed:** 2026-09-09 snapshots of Koali Spaces, Koali Control Panel, kOA Linux, LevelUpDiag, parallel design plans, and the Senior Architecture Patterns reference.  
> **Authority rule:** Until this package is explicitly adopted, existing repository documentation and contracts remain authoritative. This package defines the proposed target and the delta to close.

## TARGET model

```text
InterfaceTheme
      ↓
SpaceAppearancePolicy
      ↓
UserPresentationPreferences
      ↓
ModuleContext
      ↓
EffectiveAppearance
```

### InterfaceTheme

Base design-system semantics: typography, spacing, radius, semantic colors, focus, and default accent family.

### SpaceAppearancePolicy

Shared defaults and allowed choices. It may constrain what a Space permits, but it does not store the current personal selection.

### UserPresentationPreferences

```ts
{
  mode: "system" | "light" | "dark",
  accent: "forest" | string,
  density: "compact" | "comfortable" | "touch",
  surfaceStyle: "minimal" | "outlined" | "elevated"
}
```

### ModuleContext

Optional owner accent/context hint only when allowed by Space policy. It does not force the owner's internal theme to match Koali.

## Default visual language

- system/light by default according to policy;
- accent near the current Koali forest tone;
- slightly off-white layout background in light mode;
- outlined surfaces by default;
- 1px subtle borders;
- radius 8px normal, with a small bounded radius scale;
- shadows only for floating/elevated elements;
- outline-style icons;
- comfortable density;
- short color/border/shadow transitions only.

## Surface styles

- `minimal`: separators, almost no card framing, no permanent shadow;
- `outlined`: subtle 1px borders, default;
- `elevated`: same information architecture with restrained shadow.

The three styles modify tokens, not JSX structure.

## Migration rule

Existing theme/density values remain valid compatibility inputs. Where density currently lives in Space/theme/surface contracts, it becomes a default or contextual input rather than the final user preference authority.
