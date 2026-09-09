from __future__ import annotations

import json
from copy import deepcopy

import pytest
from jsonschema import Draft202012Validator
from referencing import Registry, Resource

from koa_spaces_adapter import (
    AppearanceValidationError,
    ManifestValidationError,
    SpaceActivationError,
    admit_space,
    validate_accent_palette,
    validate_manifest,
    validate_space_appearance,
)

from ._support import ROOT, load_schema


def _validator(name: str) -> Draft202012Validator:
    directory = ROOT / "docs/contracts/artifact-contracts"
    resources = []
    for path in directory.glob("*.schema.json"):
        schema = json.loads(path.read_text(encoding="utf-8"))
        resources.append((schema["$id"], Resource.from_contents(schema)))
    root = load_schema(name)
    return Draft202012Validator(root, registry=Registry().with_resources(resources))


def test_shared_contracts_express_ks2_authority_split():
    topbar = load_schema("topbar-widget.schema.json")
    assert "projection_ref" in topbar["properties"]
    activation_kinds = topbar["properties"]["activation"]["properties"]["kind"]["enum"]
    assert activation_kinds == ["route", "command", "none"]
    assert "status_provider_ref" not in topbar["properties"]["activation"]["properties"]
    assert "surface_ids" not in topbar["properties"]

    space = load_schema("space-definition.schema.json")
    assert space["properties"]["appearance"]["required"] == ["theme_ref"]
    assert "appearance_policy" in space["properties"]
    assert "presentation_preferences" not in space["properties"]

    theme = load_schema("interface-theme.schema.json")
    assert "primary_accent_id" in theme["properties"]["tokens"]["properties"]

    for name in (
        "accent-palette.schema.json",
        "presentation-preferences.schema.json",
        "product-surface-profile.schema.json",
    ):
        assert (ROOT / "docs/contracts/artifact-contracts" / name).is_file()


def test_counter_projection_is_data_source_not_activation(module_manifest):
    manifest = deepcopy(module_manifest)
    manifest["topbar_widgets"] = [{
        "widget_id": "koa_mediatheque.attention",
        "module_id": "koa_mediatheque",
        "scope": "module",
        "slot": "status",
        "kind": "counter",
        "label": "Attention",
        "priority": 10,
        "offline_behavior": "cached_read_only",
        "projection_ref": "koa_mediatheque.attention",
        "activation": {"kind": "route", "route_id": "koa_mediatheque.home"},
    }]
    _validator("module-interface-manifest.schema.json").validate(manifest)
    validate_manifest(manifest)

    missing = deepcopy(manifest)
    missing["topbar_widgets"][0].pop("projection_ref")
    with pytest.raises(Exception):
        _validator("module-interface-manifest.schema.json").validate(missing)
    with pytest.raises(ManifestValidationError, match="requires projection_ref"):
        validate_manifest(missing)


def test_surface_profiles_resolve_declared_navigation_and_default(module_manifest):
    manifest = deepcopy(module_manifest)
    manifest["default_surface_id"] = "work"
    manifest["ui_portability"] = {"integrated_supported": True, "standalone_supported": True, "standalone_entrypoint_ref": "koa-mediatheque:standalone"}
    manifest["surface_profiles"] = [{
        "surface_id": "work",
        "label": "Work",
        "home_route_id": "koa_mediatheque.home",
        "navigation_item_ids": ["library", "actions", "publish"],
        "topbar_widget_ids": ["koa_mediatheque.open_publish"],
        "command_refs": [],
        "inspector_ref": None,
        "density": "comfortable",
    }]
    _validator("module-interface-manifest.schema.json").validate(manifest)
    validated = validate_manifest(manifest)
    assert validated.surface_ids == ("work",)
    assert validated.standalone_supported is True


def test_user_preferences_never_enter_space_activation(space_definition, accent_palette):
    palette = validate_accent_palette(accent_palette)
    bad = deepcopy(space_definition)
    bad["presentation_preferences"] = {"mode": "dark", "accent": "plum", "density": "compact", "surface_style": "elevated"}
    with pytest.raises(AppearanceValidationError, match="must not be stored"):
        validate_space_appearance(bad, palette)


def test_space_appearance_policy_is_bounded(space_definition, accent_palette):
    palette = validate_accent_palette(accent_palette)
    space = deepcopy(space_definition)
    space["appearance"].pop("density", None)
    space["appearance_policy"] = {
        "default_mode": "system",
        "default_accent": "forest",
        "default_density": "comfortable",
        "default_surface_style": "outlined",
        "allowed_modes": ["system", "light", "dark"],
        "allowed_accents": ["forest", "plum"],
        "allowed_densities": ["comfortable", "touch"],
        "allowed_surface_styles": ["minimal", "outlined"],
        "allow_module_accent": True,
    }
    validate_space_appearance(space, palette)
    _validator("space-definition.schema.json").validate(space)

    space["appearance_policy"]["default_accent"] = "ocean"
    with pytest.raises(AppearanceValidationError, match="not allowed"):
        validate_space_appearance(space, palette)
