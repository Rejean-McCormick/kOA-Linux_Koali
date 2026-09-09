"""Appearance-policy validation for the kOA/Koali Spaces boundary.

The accent palette document is the single source of truth for bounded accent IDs.
User presentation preferences never enter Space activation state.
"""
from __future__ import annotations

from dataclasses import dataclass
from types import MappingProxyType
from typing import Any, Mapping


class AppearanceValidationError(ValueError):
    """Raised when appearance data crosses the presentation boundary."""


@dataclass(frozen=True, slots=True)
class ValidatedAccentPalette:
    default_accent: str
    accents: Mapping[str, str]


def validate_accent_palette(document: Mapping[str, Any]) -> ValidatedAccentPalette:
    if not isinstance(document, Mapping):
        raise AppearanceValidationError("accent palette must be an object")
    if document.get("schema_version") != 1:
        raise AppearanceValidationError("accent palette schema_version must be 1")
    raw = document.get("accents")
    if not isinstance(raw, list) or not raw:
        raise AppearanceValidationError("accent palette must contain accents")
    accents: dict[str, str] = {}
    for item in raw:
        if not isinstance(item, Mapping):
            raise AppearanceValidationError("accent entry must be an object")
        accent_id, color = item.get("id"), item.get("color")
        if not isinstance(accent_id, str) or not accent_id:
            raise AppearanceValidationError("accent id is invalid")
        if accent_id in accents:
            raise AppearanceValidationError(f"duplicate accent id {accent_id}")
        if not isinstance(color, str) or len(color) != 7 or not color.startswith("#"):
            raise AppearanceValidationError(f"accent color is invalid for {accent_id}")
        try:
            int(color[1:], 16)
        except ValueError as exc:
            raise AppearanceValidationError(f"accent color is invalid for {accent_id}") from exc
        accents[accent_id] = color.lower()
    default = document.get("default_accent")
    if default not in accents:
        raise AppearanceValidationError("default accent does not resolve")
    return ValidatedAccentPalette(str(default), MappingProxyType(accents))


def validate_space_appearance(space: Mapping[str, Any], palette: ValidatedAccentPalette) -> None:
    if "presentation_preferences" in space:
        raise AppearanceValidationError("user presentation preferences must not be stored in Space activation state")
    appearance = space.get("appearance")
    if not isinstance(appearance, Mapping) or not isinstance(appearance.get("theme_ref"), str):
        raise AppearanceValidationError("Space must select an interface theme")
    if appearance.get("density") is not None and appearance.get("density") not in {"comfortable", "compact", "touch"}:
        raise AppearanceValidationError("Space compatibility density is invalid")
    if appearance.get("allow_module_accent") is not None and not isinstance(appearance.get("allow_module_accent"), bool):
        raise AppearanceValidationError("Space compatibility allow_module_accent is invalid")

    policy = space.get("appearance_policy")
    if policy is None:
        return
    if not isinstance(policy, Mapping):
        raise AppearanceValidationError("Space appearance_policy must be an object")
    allowed_keys = {
        "default_mode", "default_accent", "default_density", "default_surface_style",
        "allowed_modes", "allowed_accents", "allowed_densities", "allowed_surface_styles",
        "allow_module_accent",
    }
    unknown = set(policy) - allowed_keys
    if unknown:
        raise AppearanceValidationError(f"Space appearance_policy contains unsupported fields: {sorted(unknown)}")

    universes = {
        "allowed_modes": {"system", "light", "dark"},
        "allowed_densities": {"comfortable", "compact", "touch"},
        "allowed_surface_styles": {"minimal", "outlined", "elevated"},
        "allowed_accents": set(palette.accents),
    }
    resolved: dict[str, set[str] | None] = {}
    for key, universe in universes.items():
        value = policy.get(key)
        if value is None:
            resolved[key] = None
            continue
        if not isinstance(value, list) or not value or len(value) != len(set(value)) or any(item not in universe for item in value):
            raise AppearanceValidationError(f"Space {key} is invalid")
        resolved[key] = set(value)

    defaults = {
        "default_mode": ("allowed_modes", {"system", "light", "dark"}),
        "default_density": ("allowed_densities", {"comfortable", "compact", "touch"}),
        "default_surface_style": ("allowed_surface_styles", {"minimal", "outlined", "elevated"}),
        "default_accent": ("allowed_accents", set(palette.accents)),
    }
    for key, (allowed_key, universe) in defaults.items():
        value = policy.get(key)
        if value is None:
            continue
        if value not in universe:
            raise AppearanceValidationError(f"Space {key} is invalid")
        allowed = resolved[allowed_key]
        if allowed is not None and value not in allowed:
            raise AppearanceValidationError(f"Space {key} is not allowed by appearance policy")
    if policy.get("allow_module_accent") is not None and not isinstance(policy.get("allow_module_accent"), bool):
        raise AppearanceValidationError("Space appearance policy allow_module_accent is invalid")
