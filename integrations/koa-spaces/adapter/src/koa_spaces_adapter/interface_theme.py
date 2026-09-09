"""Validation for presentation-only Koali interface themes shared by standalone products and composition hosts."""
from __future__ import annotations
from dataclasses import dataclass
from types import MappingProxyType
from typing import Any, Mapping
from .receipts import artifact_digest
from .appearance import AppearanceValidationError, ValidatedAccentPalette

class ThemeValidationError(ValueError):
    """Raised when an interface theme crosses the presentation contract."""

@dataclass(frozen=True, slots=True)
class ValidatedTheme:
    theme_id: str
    version: str
    design_system_id: str
    digest: str
    document: Mapping[str, Any]


def validate_theme(document: Mapping[str, Any], *, accent_palette: ValidatedAccentPalette | None = None) -> ValidatedTheme:
    if not isinstance(document, Mapping):
        raise ThemeValidationError("theme must be an object")
    required = {"theme_id","version","design_system_id","tokens","icon_policy","motion_policy","authority_boundary"}
    if not required.issubset(document):
        raise ThemeValidationError(f"theme missing fields: {sorted(required-set(document))}")
    boundary=document["authority_boundary"]
    if not isinstance(boundary, Mapping) or dict(boundary)!={
        "presentation_only": True,
        "changes_authorization": False,
        "changes_module_identity": False,
    }:
        raise ThemeValidationError("theme crosses authority boundary")
    motion=document["motion_policy"]
    if not isinstance(motion, Mapping) or motion.get("reduced_motion_supported") is not True:
        raise ThemeValidationError("reduced-motion support is required")
    tokens=document["tokens"]
    if not isinstance(tokens, Mapping) or tokens.get("density") not in {"comfortable","compact","touch"}:
        raise ThemeValidationError("theme density is invalid")
    accent_id = tokens.get("primary_accent_id")
    if accent_id is not None:
        if accent_palette is None:
            raise ThemeValidationError("theme primary_accent_id requires the canonical accent palette")
        expected = accent_palette.accents.get(str(accent_id))
        if expected is None:
            raise ThemeValidationError("theme primary_accent_id is not in the canonical accent palette")
        color = tokens.get("primary_accent")
        if not isinstance(color, str) or color.lower() != expected.lower():
            raise ThemeValidationError("theme primary accent id/color mismatch")
    return ValidatedTheme(
        theme_id=str(document["theme_id"]), version=str(document["version"]),
        design_system_id=str(document["design_system_id"]), digest=artifact_digest(document),
        document=MappingProxyType(dict(document)),
    )
