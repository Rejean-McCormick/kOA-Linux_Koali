"""Presentation-only projection of the declared Orgo module interface."""
from __future__ import annotations

from dataclasses import dataclass
from types import MappingProxyType
from typing import Any, Iterable, Mapping

from .capabilities import CapabilityState, CapabilityStatus


@dataclass(frozen=True, slots=True)
class SurfaceProjection:
    manifest_id: str
    module_id: str
    product_id: str
    public_name: str
    home_route_id: str
    routes: tuple[Mapping[str, Any], ...]
    sidebar: Mapping[str, Any]
    topbar_widgets: tuple[Mapping[str, Any], ...]
    capability_states: Mapping[str, str]
    surface_ids: tuple[str, ...]
    commands: tuple[Mapping[str, Any], ...]
    inspectors: tuple[Mapping[str, Any], ...]
    presentation_only: bool = True
    may_grant_capabilities: bool = False
    direct_domain_writes: bool = False
    menu_visibility_is_authorization: bool = False

    def __post_init__(self) -> None:
        object.__setattr__(self, "sidebar", MappingProxyType(dict(self.sidebar)))
        object.__setattr__(self, "capability_states", MappingProxyType(dict(self.capability_states)))


class SurfaceBridge:
    def __init__(self, *, manifest: Mapping[str, Any]) -> None:
        self._manifest = _validate_manifest(manifest)

    def project(self, *, capabilities: Iterable[CapabilityStatus]) -> SurfaceProjection:
        states = {item.capability_id: item.state.value for item in capabilities}
        required = set(self._manifest.get("required_capabilities", []))
        unknown = required - set(states)
        if unknown:
            raise ValueError(f"surface references unknown capabilities: {sorted(unknown)}")
        routes = tuple(MappingProxyType(dict(item)) for item in self._manifest["routes"])
        widgets = tuple(MappingProxyType(dict(item)) for item in self._manifest["topbar_widgets"])
        return SurfaceProjection(
            manifest_id=self._manifest["manifest_id"],
            module_id=self._manifest["module_id"],
            product_id=self._manifest.get("product_id", "orgo"),
            public_name=self._manifest["public_name"],
            home_route_id=self._manifest["home_route_id"],
            routes=routes,
            sidebar=self._manifest["sidebar"],
            topbar_widgets=widgets,
            capability_states=states,
            surface_ids=tuple(item["surface_id"] for item in self._manifest.get("surface_profiles", [])),
            commands=tuple(MappingProxyType(dict(item)) for item in self._manifest.get("commands", [])),
            inspectors=tuple(MappingProxyType(dict(item)) for item in self._manifest.get("inspectors", [])),
        )


def _validate_manifest(value: Mapping[str, Any]) -> Mapping[str, Any]:
    required = {
        "manifest_id",
        "manifest_version",
        "module_id",
        "public_name",
        "home_route_id",
        "routes",
        "sidebar",
        "topbar_widgets",
        "offline_behavior",
        "authority_boundary",
    }
    missing = required - set(value)
    if missing:
        raise ValueError(f"module interface manifest missing fields: {sorted(missing)}")
    boundary = value["authority_boundary"]
    if not isinstance(boundary, Mapping):
        raise ValueError("authority_boundary must be an object")
    expected = {
        "presentation_only": True,
        "may_grant_capabilities": False,
        "direct_domain_writes": False,
        "menu_visibility_is_authorization": False,
    }
    if dict(boundary) != expected:
        raise ValueError("surface authority boundary must remain presentation-only")
    if value.get("product_id", value.get("module_id")) != "orgo":
        raise ValueError("surface product_id must be orgo")
    modes = value.get("ui_modes")
    if modes is not None:
        if not isinstance(modes, Mapping):
            raise ValueError("ui_modes must be an object")
        if modes.get("composition_host_required_for_standalone") is not False:
            raise ValueError("standalone Orgo cannot require the optional composition host")
        if modes.get("private_cross_product_ui_imports") is not False:
            raise ValueError("private cross-product UI imports are prohibited")
    for field in ("routes", "topbar_widgets"):
        if not isinstance(value[field], list):
            raise ValueError(f"{field} must be a list")
    if not isinstance(value["sidebar"], Mapping):
        raise ValueError("sidebar must be an object")
    return MappingProxyType(dict(value))
