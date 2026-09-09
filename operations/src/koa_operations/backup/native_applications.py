"""Resolve native-application data policy into owner-preserving backup selections.

This module does not execute backups and does not copy application data. It converts
NativeApplicationDataPolicy logical locations into normalized user-local paths that
can be checkpointed by the existing backup coordinator. Documents remain externally
owned, and disposable caches are explicitly excluded from ordinary backup members.
"""
from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
from typing import Any, Mapping


class NativeApplicationDataPolicyError(ValueError):
    """Raised when native application data semantics are ambiguous or unsafe."""


_ROOTS = frozenset({"home", "xdg_config", "xdg_data", "xdg_state", "xdg_cache"})


@dataclass(frozen=True, slots=True)
class NativeDataLocation:
    root: str
    relative_path: str
    resolved_path: Path


@dataclass(frozen=True, slots=True)
class NativeApplicationBackupSelection:
    policy_id: str
    persistent_profile_paths: tuple[NativeDataLocation, ...]
    disposable_cache_paths: tuple[NativeDataLocation, ...]
    documents_external: bool
    requires_compatible_profile: bool
    checkpoint_when_required: bool


def _mapping(value: object, field: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise NativeApplicationDataPolicyError(f"{field} must be an object")
    return value


def _safe_relative(value: object, field: str) -> str:
    if not isinstance(value, str) or not value or "\\x00" in value or "\\" in value:
        raise NativeApplicationDataPolicyError(f"{field} must be a normalized relative path")
    path = Path(value)
    if path.is_absolute() or ".." in path.parts or "." in path.parts:
        raise NativeApplicationDataPolicyError(f"{field} must be a normalized relative path")
    return path.as_posix()


def _resolve_location(
    value: object,
    *,
    roots: Mapping[str, Path],
    field: str,
) -> NativeDataLocation:
    item = _mapping(value, field)
    root_id = item.get("root")
    if not isinstance(root_id, str) or root_id not in _ROOTS or root_id not in roots:
        raise NativeApplicationDataPolicyError(f"{field}.root is not available")
    relative = _safe_relative(item.get("relative_path"), f"{field}.relative_path")
    root = roots[root_id].expanduser().resolve(strict=False)
    resolved = (root / relative).resolve(strict=False)
    try:
        resolved.relative_to(root)
    except ValueError as exc:
        raise NativeApplicationDataPolicyError(f"{field} escapes its declared root") from exc
    return NativeDataLocation(root=root_id, relative_path=relative, resolved_path=resolved)


def resolve_native_application_data_policy(
    policy_path: str | Path,
    *,
    home: str | Path,
    xdg_config: str | Path | None = None,
    xdg_data: str | Path | None = None,
    xdg_state: str | Path | None = None,
    xdg_cache: str | Path | None = None,
) -> NativeApplicationBackupSelection:
    path = Path(policy_path)
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise NativeApplicationDataPolicyError("native application data policy is unavailable") from exc
    if not isinstance(value, Mapping) or value.get("kind") != "NativeApplicationDataPolicy" or value.get("version") != "1.0.0":
        raise NativeApplicationDataPolicyError("unsupported native application data policy")

    home_path = Path(home).expanduser().resolve(strict=False)
    roots = {
        "home": home_path,
        "xdg_config": Path(xdg_config).resolve(strict=False) if xdg_config is not None else home_path / ".config",
        "xdg_data": Path(xdg_data).resolve(strict=False) if xdg_data is not None else home_path / ".local/share",
        "xdg_state": Path(xdg_state).resolve(strict=False) if xdg_state is not None else home_path / ".local/state",
        "xdg_cache": Path(xdg_cache).resolve(strict=False) if xdg_cache is not None else home_path / ".cache",
    }

    profile_persistence = value.get("profile_persistence")
    cache_policy = value.get("cache_policy")
    documents_ownership = value.get("documents_ownership")
    profile_values = value.get("profile_locations")
    cache_values = value.get("cache_locations")
    if not isinstance(profile_values, list) or not isinstance(cache_values, list):
        raise NativeApplicationDataPolicyError("native application data locations must be arrays")

    profiles = tuple(
        _resolve_location(item, roots=roots, field=f"profile_locations[{index}]")
        for index, item in enumerate(profile_values)
    )
    caches = tuple(
        _resolve_location(item, roots=roots, field=f"cache_locations[{index}]")
        for index, item in enumerate(cache_values)
    )
    if profile_persistence == "persistent" and not profiles:
        raise NativeApplicationDataPolicyError("persistent native profile requires at least one profile location")
    if profile_persistence != "persistent" and profiles:
        raise NativeApplicationDataPolicyError("non-persistent native profile cannot declare backup profile locations")
    if cache_policy == "disposable" and any(item.root != "xdg_cache" for item in caches):
        raise NativeApplicationDataPolicyError("disposable cache locations must use xdg_cache")

    rollback = _mapping(value.get("rollback"), "rollback")
    upgrade = _mapping(value.get("upgrade"), "upgrade")
    policy_id = value.get("policy_id")
    if not isinstance(policy_id, str) or not policy_id:
        raise NativeApplicationDataPolicyError("policy_id is required")

    return NativeApplicationBackupSelection(
        policy_id=policy_id,
        persistent_profile_paths=profiles if profile_persistence == "persistent" else (),
        disposable_cache_paths=caches if cache_policy == "disposable" else (),
        documents_external=documents_ownership == "external_logical_owner",
        requires_compatible_profile=rollback.get("requires_compatible_profile") is True,
        checkpoint_when_required=upgrade.get("checkpoint_when_required") is True,
    )


__all__ = [
    "NativeApplicationBackupSelection",
    "NativeApplicationDataPolicyError",
    "NativeDataLocation",
    "resolve_native_application_data_policy",
]
