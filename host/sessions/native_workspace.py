#!/usr/bin/env python3
"""Policy-controlled native application projection and user-session launch broker.

This module belongs to the unprivileged graphical user session.  It deliberately
keeps Freedesktop desktop metadata authoritative, consumes kOA admission/data
policy, exposes only a minimized projection, and accepts high-level launch
requests over a local Unix socket.  It never accepts an executable path, shell
command, or arbitrary argv from callers.
"""

from __future__ import annotations

import argparse
import configparser
from collections import deque
from datetime import datetime, timezone
import http.client
from dataclasses import dataclass
import json
import os
from pathlib import Path
import shutil
import socket
import stat
import struct
import subprocess
import sys
import time
import tomllib
from typing import Any, Iterable, Mapping, Sequence
from urllib.parse import urlparse

BROKER_PROTOCOL = "koa.native-workspace/v1"
PROJECTION_VERSION = "1.0.0"
REQUIRED_CAPABILITY = "user.native_workspace"
DEFAULT_SOCKET_NAME = "koa/native-workspace.sock"
MAX_REQUEST_BYTES = 64 * 1024
MAX_RESPONSE_BYTES = 2 * 1024 * 1024
MAX_ID_LENGTH = 160
_ALLOWED_OPERATIONS = frozenset({"status", "list", "launch"})
_ALLOWED_ACTIONS = frozenset({"launch", "open_resource", "open_uri"})
_SECURITY_CLASSES = frozenset({"web", "mail", "office", "media", "files"})
_RESOURCE_SCOPES = frozenset({"documents", "downloads", "music", "pictures", "videos", "desktop"})


class NativeWorkspaceError(RuntimeError):
    """Stable, non-secret native workspace failure."""

    def __init__(self, code: str, message: str) -> None:
        super().__init__(message)
        self.code = code
        self.public_message = message


@dataclass(frozen=True, slots=True)
class DataPolicy:
    policy_id: str
    profile_persistence: str
    cache_policy: str
    documents_ownership: str
    profile_locations: tuple[tuple[str, str], ...]
    cache_locations: tuple[tuple[str, str], ...]
    rollback_requires_compatible_profile: bool
    upgrade_checkpoint_when_required: bool


@dataclass(frozen=True, slots=True)
class NativeWorkspaceRuntimePolicy:
    profile_path: Path
    admission_policy_root: Path
    data_policy_root: Path
    socket_relative_to_xdg_runtime: str
    max_request_bytes: int
    max_response_bytes: int
    max_launches_per_minute: int


@dataclass(frozen=True, slots=True)
class AdmissionPolicy:
    app_id: str
    desktop_entry_refs: tuple[str, ...]
    required_capability: str
    allowed_profile_ids: tuple[str, ...]
    allowed_actions: tuple[str, ...]
    allowed_uri_schemes: tuple[str, ...]
    allowed_resource_scopes: tuple[str, ...]
    security_class: str
    resource_envelope_ref: str
    workload_class: str
    resource_request: Mapping[str, Any]
    criticality: str
    priority: int
    network_policy: str
    audio_policy: str
    gpu_policy: str
    offline_behavior: str
    data_policy_ref: str
    enabled: bool


@dataclass(frozen=True, slots=True)
class DesktopEntry:
    desktop_entry_ref: str
    path: Path
    name: str
    icon: str | None
    mime_types: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class NativeApplicationProjection:
    app_id: str
    display_name: str
    icon_ref: str | None
    available: bool
    allowed_actions: tuple[str, ...]
    security_class: str
    reason: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "projection_version": PROJECTION_VERSION,
            "app_id": self.app_id,
            "display_name": self.display_name,
            "icon_ref": self.icon_ref,
            "available": self.available,
            "allowed_actions": list(self.allowed_actions),
            "security_class": self.security_class,
            "reason": self.reason,
        }


@dataclass(frozen=True, slots=True)
class RuntimeStatus:
    available: bool
    capability_present: bool
    graphical_session_ready: bool
    substrate: Mapping[str, bool]
    reasons: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        return {
            "protocol": BROKER_PROTOCOL,
            "available": self.available,
            "capability_present": self.capability_present,
            "graphical_session_ready": self.graphical_session_ready,
            "substrate": dict(self.substrate),
            "reasons": list(self.reasons),
        }


def _identifier(value: Any, label: str) -> str:
    if not isinstance(value, str):
        raise NativeWorkspaceError("invalid_contract", f"{label} must be a string")
    normalized = value.strip()
    if not normalized or len(normalized) > MAX_ID_LENGTH or "\x00" in normalized:
        raise NativeWorkspaceError("invalid_contract", f"{label} is invalid")
    allowed = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789._:-/")
    if any(ch not in allowed for ch in normalized):
        raise NativeWorkspaceError("invalid_contract", f"{label} contains unsupported characters")
    return normalized


def _string_list(value: Any, label: str, *, maximum: int = 32) -> tuple[str, ...]:
    if not isinstance(value, list) or len(value) > maximum:
        raise NativeWorkspaceError("invalid_contract", f"{label} must be a bounded array")
    items = tuple(_identifier(item, f"{label}[]") for item in value)
    if len(items) != len(set(items)):
        raise NativeWorkspaceError("invalid_contract", f"{label} contains duplicates")
    return items


def _read_json(path: Path, *, maximum: int = 512 * 1024) -> Mapping[str, Any]:
    try:
        raw = path.read_bytes()
    except OSError as exc:
        raise NativeWorkspaceError("policy_unavailable", "native workspace policy is unavailable") from exc
    if len(raw) > maximum:
        raise NativeWorkspaceError("invalid_contract", "native workspace policy exceeds size limit")
    try:
        value = json.loads(raw)
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise NativeWorkspaceError("invalid_contract", "native workspace policy is invalid JSON") from exc
    if not isinstance(value, Mapping):
        raise NativeWorkspaceError("invalid_contract", "native workspace policy root must be an object")
    return value


def load_data_policy(path: Path) -> DataPolicy:
    value = _read_json(path)
    if value.get("kind") != "NativeApplicationDataPolicy" or value.get("version") != "1.0.0":
        raise NativeWorkspaceError("invalid_contract", "unsupported native application data policy")
    rollback = value.get("rollback")
    upgrade = value.get("upgrade")
    if not isinstance(rollback, Mapping) or not isinstance(upgrade, Mapping):
        raise NativeWorkspaceError("invalid_contract", "native application data policy is incomplete")
    def locations(field: str) -> tuple[tuple[str, str], ...]:
        raw = value.get(field)
        if not isinstance(raw, list) or len(raw) > 16:
            raise NativeWorkspaceError("invalid_contract", f"{field} must be a bounded array")
        result: list[tuple[str, str]] = []
        for index, item in enumerate(raw):
            if not isinstance(item, Mapping):
                raise NativeWorkspaceError("invalid_contract", f"{field}[{index}] must be an object")
            root = _identifier(item.get("root"), f"{field}[{index}].root")
            if root not in {"home", "xdg_config", "xdg_data", "xdg_state", "xdg_cache"}:
                raise NativeWorkspaceError("invalid_contract", f"{field}[{index}].root is unsupported")
            relative = item.get("relative_path")
            if not isinstance(relative, str) or not relative or "\x00" in relative or "\\" in relative:
                raise NativeWorkspaceError("invalid_contract", f"{field}[{index}].relative_path is invalid")
            rel = Path(relative)
            if rel.is_absolute() or ".." in rel.parts or "." in rel.parts:
                raise NativeWorkspaceError("invalid_contract", f"{field}[{index}].relative_path is unsafe")
            result.append((root, rel.as_posix()))
        if len(result) != len(set(result)):
            raise NativeWorkspaceError("invalid_contract", f"{field} contains duplicates")
        return tuple(result)

    profile_persistence = _identifier(value.get("profile_persistence"), "profile_persistence")
    cache_policy = _identifier(value.get("cache_policy"), "cache_policy")
    profile_locations = locations("profile_locations")
    cache_locations = locations("cache_locations")
    if profile_persistence == "persistent" and not profile_locations:
        raise NativeWorkspaceError("invalid_contract", "persistent native profile requires a location")
    if cache_policy == "disposable" and any(root != "xdg_cache" for root, _ in cache_locations):
        raise NativeWorkspaceError("invalid_contract", "disposable native caches must use xdg_cache")
    return DataPolicy(
        policy_id=_identifier(value.get("policy_id"), "policy_id"),
        profile_persistence=profile_persistence,
        cache_policy=cache_policy,
        documents_ownership=_identifier(value.get("documents_ownership"), "documents_ownership"),
        profile_locations=profile_locations,
        cache_locations=cache_locations,
        rollback_requires_compatible_profile=bool(rollback.get("requires_compatible_profile")),
        upgrade_checkpoint_when_required=bool(upgrade.get("checkpoint_when_required")),
    )


def load_runtime_policy(path: Path) -> NativeWorkspaceRuntimePolicy:
    try:
        with path.open("rb") as stream:
            value = tomllib.load(stream)
    except (OSError, tomllib.TOMLDecodeError) as exc:
        raise NativeWorkspaceError("runtime_policy_unavailable", "native workspace runtime policy is unavailable") from exc
    if value.get("schema_version") != "1.0.0":
        raise NativeWorkspaceError("invalid_runtime_policy", "native workspace runtime policy version is unsupported")
    invariants = {
        "required_capability": REQUIRED_CAPABILITY,
        "transport": "json_line_over_unix",
        "peer_authentication": "same_uid_so_peercred",
        "network_listener": False,
        "raw_executable_input": False,
        "raw_argv_input": False,
        "resource_admission": "resource_governor_required",
    }
    for key, expected in invariants.items():
        if value.get(key) != expected:
            raise NativeWorkspaceError("invalid_runtime_policy", f"native workspace runtime invariant {key} is invalid")
    required = value.get("substrate", {}).get("required", {}) if isinstance(value.get("substrate"), Mapping) else {}
    for key in ("wayland", "user_dbus", "gio"):
        if required.get(key) is not True:
            raise NativeWorkspaceError("invalid_runtime_policy", f"required substrate {key} must remain enabled")
    relative_socket = value.get("socket_relative_to_xdg_runtime")
    if not isinstance(relative_socket, str) or not relative_socket or Path(relative_socket).is_absolute() or ".." in Path(relative_socket).parts:
        raise NativeWorkspaceError("invalid_runtime_policy", "native workspace socket must remain relative to XDG_RUNTIME_DIR")
    limits = value.get("limits")
    if not isinstance(limits, Mapping):
        raise NativeWorkspaceError("invalid_runtime_policy", "native workspace limits are required")
    def bounded_int(name: str, minimum: int, maximum: int) -> int:
        raw = limits.get(name)
        if isinstance(raw, bool) or not isinstance(raw, int) or raw < minimum or raw > maximum:
            raise NativeWorkspaceError("invalid_runtime_policy", f"native workspace limit {name} is invalid")
        return raw
    profile_path = value.get("profile_path")
    admission_root = value.get("admission_policy_root")
    data_root = value.get("data_policy_root")
    if not all(isinstance(item, str) and item.startswith("/") for item in (profile_path, admission_root, data_root)):
        raise NativeWorkspaceError("invalid_runtime_policy", "native workspace runtime paths must be absolute")
    return NativeWorkspaceRuntimePolicy(
        profile_path=Path(profile_path),
        admission_policy_root=Path(admission_root),
        data_policy_root=Path(data_root),
        socket_relative_to_xdg_runtime=relative_socket,
        max_request_bytes=bounded_int("max_request_bytes", 1024, 1024 * 1024),
        max_response_bytes=bounded_int("max_response_bytes", 1024, 16 * 1024 * 1024),
        max_launches_per_minute=bounded_int("max_launches_per_minute", 1, 600),
    )


def load_admission_policy(path: Path) -> AdmissionPolicy:
    value = _read_json(path)
    if value.get("kind") != "NativeApplicationAdmissionPolicy" or value.get("version") != "1.0.0":
        raise NativeWorkspaceError("invalid_contract", "unsupported native application admission policy")
    runtime = value.get("runtime")
    security = value.get("security")
    resources = value.get("resources")
    launch = value.get("launch")
    if not all(isinstance(item, Mapping) for item in (runtime, security, resources, launch)):
        raise NativeWorkspaceError("invalid_contract", "native application admission policy is incomplete")
    security_class = _identifier(security.get("class"), "security.class")
    if security_class not in _SECURITY_CLASSES:
        raise NativeWorkspaceError("invalid_contract", "unsupported native application security class")
    actions = _string_list(launch.get("allowed_actions"), "launch.allowed_actions")
    if not set(actions).issubset(_ALLOWED_ACTIONS):
        raise NativeWorkspaceError("invalid_contract", "native application action is unsupported")
    scopes = _string_list(launch.get("allowed_resource_scopes", []), "launch.allowed_resource_scopes")
    if not set(scopes).issubset(_RESOURCE_SCOPES):
        raise NativeWorkspaceError("invalid_contract", "native application resource scope is unsupported")
    uri_schemes = tuple(item.lower() for item in _string_list(launch.get("allowed_uri_schemes", []), "launch.allowed_uri_schemes"))
    return AdmissionPolicy(
        app_id=_identifier(value.get("app_id"), "app_id"),
        desktop_entry_refs=_string_list(value.get("desktop_entry_refs"), "desktop_entry_refs", maximum=8),
        required_capability=_identifier(runtime.get("required_capability"), "runtime.required_capability"),
        allowed_profile_ids=_string_list(runtime.get("allowed_profile_ids"), "runtime.allowed_profile_ids", maximum=16),
        allowed_actions=actions,
        allowed_uri_schemes=uri_schemes,
        allowed_resource_scopes=scopes,
        security_class=security_class,
        resource_envelope_ref=_identifier(resources.get("resource_envelope_ref"), "resources.resource_envelope_ref"),
        workload_class=_identifier(resources.get("workload_class"), "resources.workload_class"),
        resource_request=dict(resources.get("resource_request") or {}),
        criticality=_identifier(resources.get("criticality"), "resources.criticality"),
        priority=int(resources.get("priority", 50)),
        network_policy=_identifier(security.get("network"), "security.network"),
        audio_policy=_identifier(security.get("audio"), "security.audio"),
        gpu_policy=_identifier(security.get("gpu"), "security.gpu"),
        offline_behavior=_identifier(value.get("offline_behavior"), "offline_behavior"),
        data_policy_ref=_identifier(value.get("data_policy_ref"), "data_policy_ref"),
        enabled=bool(value.get("enabled", True)),
    )


def _xdg_data_dirs() -> tuple[Path, ...]:
    roots: list[Path] = []
    home = os.environ.get("XDG_DATA_HOME")
    if home:
        roots.append(Path(home))
    else:
        roots.append(Path.home() / ".local/share")
    for value in os.environ.get("XDG_DATA_DIRS", "/usr/local/share:/usr/share").split(":"):
        if value:
            roots.append(Path(value))
    return tuple(dict.fromkeys(roots))


def resolve_desktop_entry(refs: Sequence[str]) -> DesktopEntry | None:
    for ref in refs:
        if "/" in ref or "\\" in ref or ref.startswith("."):
            continue
        for root in _xdg_data_dirs():
            candidate = root / "applications" / ref
            try:
                resolved = candidate.resolve(strict=True)
            except OSError:
                continue
            try:
                resolved.relative_to((root / "applications").resolve(strict=True))
            except (OSError, ValueError):
                continue
            if not resolved.is_file():
                continue
            parser = configparser.ConfigParser(interpolation=None, strict=True)
            parser.optionxform = str
            try:
                parser.read(resolved, encoding="utf-8")
                section = parser["Desktop Entry"]
            except (OSError, UnicodeError, configparser.Error, KeyError):
                continue
            if section.get("Type", "") != "Application" or section.get("Hidden", "false").lower() == "true":
                continue
            name = section.get("Name", "").strip()
            if not name:
                continue
            mime = tuple(sorted(item for item in section.get("MimeType", "").split(";") if item))
            icon = section.get("Icon") or None
            return DesktopEntry(ref, resolved, name, icon, mime)
    return None


def _capability_state(profile: Mapping[str, Any], capability_id: str) -> bool:
    candidates: list[Mapping[str, Any]] = []
    for owner in (profile, profile.get("effective_profile")):
        if isinstance(owner, Mapping):
            capabilities = owner.get("capabilities")
            if isinstance(capabilities, Mapping):
                candidates.append(capabilities)
    for capabilities in candidates:
        value = capabilities.get(capability_id)
        if isinstance(value, Mapping):
            state = str(value.get("state", "")).lower()
            return state in {"required", "enabled", "available"}
        if value is True:
            return True
    # Effective-profile generators may normalize dotted capability identifiers.
    normalized = capability_id.replace(".", "_")
    for capabilities in candidates:
        value = capabilities.get(normalized)
        if isinstance(value, Mapping):
            state = str(value.get("state", "")).lower()
            return state in {"required", "enabled", "available"}
        if value is True:
            return True
    return False


def _effective_profile_id(profile: Mapping[str, Any]) -> str | None:
    for owner in (profile, profile.get("effective_profile")):
        if not isinstance(owner, Mapping):
            continue
        for key in ("effective_profile_id", "profile_id"):
            value = owner.get(key)
            if isinstance(value, str) and value:
                return value
    return None


def load_effective_profile(path: Path) -> Mapping[str, Any]:
    value = _read_json(path, maximum=2 * 1024 * 1024)
    return value


def _is_unix_socket(path: Path) -> bool:
    try:
        return stat.S_ISSOCK(path.stat().st_mode)
    except OSError:
        return False


def probe_substrate() -> Mapping[str, bool]:
    runtime_dir = os.environ.get("XDG_RUNTIME_DIR")
    dbus = os.environ.get("DBUS_SESSION_BUS_ADDRESS")
    return {
        "wayland": bool(os.environ.get("WAYLAND_DISPLAY")),
        "user_dbus": bool(dbus),
        "audio": bool(runtime_dir and ((Path(runtime_dir) / "pipewire-0").exists() or os.environ.get("PULSE_SERVER"))),
        "gio": shutil.which("gio") is not None,
        "xdg_mime": shutil.which("xdg-mime") is not None,
        "portal": bool(dbus and runtime_dir),
        "resource_governor": _is_unix_socket(Path("/run/koa/sockets/resource-governor.sock")),
    }


def runtime_status(profile_path: Path) -> RuntimeStatus:
    reasons: list[str] = []
    try:
        profile = load_effective_profile(profile_path)
        capability = _capability_state(profile, REQUIRED_CAPABILITY)
    except NativeWorkspaceError:
        profile = {}
        capability = False
        reasons.append("profile_unavailable")
    substrate = probe_substrate()
    graphical = substrate["wayland"] and substrate["user_dbus"]
    if not capability:
        reasons.append("capability_unavailable")
    if not graphical:
        reasons.append("graphical_session_unavailable")
    if not substrate["gio"]:
        reasons.append("freedesktop_launcher_unavailable")
    if not substrate["resource_governor"]:
        reasons.append("resource_governor_unavailable")
    return RuntimeStatus(
        available=capability and graphical and substrate["gio"] and substrate["resource_governor"],
        capability_present=capability,
        graphical_session_ready=graphical,
        substrate=substrate,
        reasons=tuple(reasons),
    )



def native_workspace_enabled(profile_path: Path) -> bool:
    try:
        profile = load_effective_profile(profile_path)
    except NativeWorkspaceError:
        return False
    return _capability_state(profile, REQUIRED_CAPABILITY)


def _policy_files(root: Path) -> tuple[Path, ...]:
    if not root.is_dir():
        return ()
    return tuple(sorted(path for path in root.glob("*.json") if path.is_file()))


def load_policy_catalog(root: Path) -> tuple[AdmissionPolicy, ...]:
    policies = tuple(load_admission_policy(path) for path in _policy_files(root))
    app_ids = [policy.app_id for policy in policies]
    if len(app_ids) != len(set(app_ids)):
        raise NativeWorkspaceError("invalid_contract", "native application app_id values must be unique")
    return policies


def _data_policy_path(data_policy_root: Path, reference: str) -> Path:
    ref = Path(reference)
    if ref.is_absolute() or ".." in ref.parts:
        raise NativeWorkspaceError("invalid_contract", "data_policy_ref must remain repository-relative")
    parts = ref.parts[1:] if ref.parts and ref.parts[0] == "data" else ref.parts
    if not parts:
        raise NativeWorkspaceError("invalid_contract", "data_policy_ref must identify a data policy")
    candidate = (data_policy_root / Path(*parts)).resolve()
    try:
        candidate.relative_to(data_policy_root.resolve())
    except ValueError as exc:
        raise NativeWorkspaceError("invalid_contract", "data_policy_ref escapes data policy root") from exc
    return candidate


def _projection_for(policy: AdmissionPolicy, *, profile_id: str | None, status: RuntimeStatus) -> NativeApplicationProjection:
    entry = resolve_desktop_entry(policy.desktop_entry_refs)
    reason: str | None = None
    available = status.available and policy.enabled
    if not policy.enabled:
        reason = "policy_disabled"
    elif profile_id not in policy.allowed_profile_ids:
        available = False
        reason = "profile_not_admitted"
    elif entry is None:
        available = False
        reason = "desktop_entry_unavailable"
    elif not status.available:
        available = False
        reason = status.reasons[0] if status.reasons else "native_workspace_unavailable"
    return NativeApplicationProjection(
        app_id=policy.app_id,
        display_name=entry.name if entry else policy.app_id,
        icon_ref=entry.icon if entry else None,
        available=available,
        allowed_actions=policy.allowed_actions if available else (),
        security_class=policy.security_class,
        reason=reason,
    )


def _xdg_user_dir(scope: str) -> Path:
    if scope not in _RESOURCE_SCOPES:
        raise NativeWorkspaceError("resource_scope_denied", "resource scope is not admitted")
    env_key = f"XDG_{scope.upper()}_DIR"
    if os.environ.get(env_key):
        return Path(os.environ[env_key]).expanduser().resolve()
    defaults = {
        "documents": "Documents",
        "downloads": "Downloads",
        "music": "Music",
        "pictures": "Pictures",
        "videos": "Videos",
        "desktop": "Desktop",
    }
    return (Path.home() / defaults[scope]).resolve()


def resolve_resource(scope: str, relative_path: str) -> Path:
    if not isinstance(relative_path, str) or not relative_path or "\x00" in relative_path:
        raise NativeWorkspaceError("invalid_request", "resource path is invalid")
    rel = Path(relative_path)
    if rel.is_absolute() or ".." in rel.parts:
        raise NativeWorkspaceError("resource_scope_denied", "resource path escapes its XDG scope")
    root = _xdg_user_dir(scope)
    candidate = (root / rel).resolve(strict=True)
    try:
        candidate.relative_to(root)
    except ValueError as exc:
        raise NativeWorkspaceError("resource_scope_denied", "resource path escapes its XDG scope") from exc
    if not candidate.is_file():
        raise NativeWorkspaceError("resource_unavailable", "resource is not a regular file")
    return candidate


class LaunchRateLimiter:
    def __init__(self, *, max_launches: int = 12, window_seconds: float = 60.0) -> None:
        self.max_launches = max_launches
        self.window_seconds = window_seconds
        self._events: deque[float] = deque()

    def admit(self, now: float | None = None) -> None:
        current = time.monotonic() if now is None else now
        while self._events and current - self._events[0] >= self.window_seconds:
            self._events.popleft()
        if len(self._events) >= self.max_launches:
            raise NativeWorkspaceError("rate_limited", "native application launch rate is temporarily limited")
        self._events.append(current)


class ResourceAdmissionPort:
    """Optional runtime port.  Production wiring must bind this to Resource Governor."""

    def admit(self, *, app_id: str, envelope_ref: str, correlation_id: str) -> bool:
        raise NotImplementedError


class FailClosedResourceAdmission(ResourceAdmissionPort):
    def admit(self, *, app_id: str, envelope_ref: str, correlation_id: str) -> bool:
        return False


class _UnixHTTPConnection(http.client.HTTPConnection):
    def __init__(self, socket_path: str, timeout: float) -> None:
        super().__init__("localhost", timeout=timeout)
        self.socket_path = socket_path

    def connect(self) -> None:
        sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        sock.settimeout(self.timeout)
        sock.connect(self.socket_path)
        self.sock = sock


class ResourceGovernorUnixAdmission(ResourceAdmissionPort):
    """Bounded client for RG-IF-002/003 over the canonical local Unix socket."""

    def __init__(self, socket_path: str = "/run/koa/sockets/resource-governor.sock", *, timeout_seconds: float = 0.5) -> None:
        self.socket_path = socket_path
        self.timeout_seconds = timeout_seconds

    def admit_policy(self, policy: AdmissionPolicy, *, correlation_id: str) -> bool:
        requested_at = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
        request_id = f"native:{policy.app_id}:{correlation_id}"
        body = {
            "request_id": request_id,
            "workload_owner_ref": f"native-app:{policy.app_id}",
            "workload_class": policy.workload_class,
            "target_scope": {"kind": "user_session", "app_id": policy.app_id},
            "resource_request": dict(policy.resource_request),
            "criticality": policy.criticality,
            "priority": policy.priority,
            "requested_at": requested_at,
        }
        raw = json.dumps(body, sort_keys=True, separators=(",", ":")).encode("utf-8")
        conn = _UnixHTTPConnection(self.socket_path, self.timeout_seconds)
        try:
            conn.request(
                "POST",
                "/v1/commands/admit_workload",
                body=raw,
                headers={
                    "content-type": "application/json",
                    "content-length": str(len(raw)),
                    "x-koa-contract-version": "1.0.0",
                    "x-koa-correlation-id": correlation_id,
                },
            )
            response = conn.getresponse()
            response_raw = response.read(MAX_RESPONSE_BYTES + 1)
        except (OSError, TimeoutError, ConnectionError):
            return False
        finally:
            conn.close()
        if response.status < 200 or response.status >= 300 or len(response_raw) > MAX_RESPONSE_BYTES:
            return False
        try:
            value = json.loads(response_raw.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError):
            return False
        if not isinstance(value, Mapping) or value.get("outcome") != "completed":
            return False
        payload = value.get("payload")
        return isinstance(payload, Mapping) and payload.get("outcome") == "admitted"

    def admit(self, *, app_id: str, envelope_ref: str, correlation_id: str) -> bool:
        # This generic method intentionally cannot invent the workload request;
        # UserSessionAppBroker calls admit_policy with the complete policy.
        return False


class PermissiveTestResourceAdmission(ResourceAdmissionPort):
    """Test-only helper; never selected by the production CLI."""

    def admit(self, *, app_id: str, envelope_ref: str, correlation_id: str) -> bool:
        return True


class UserSessionAppBroker:
    def __init__(
        self,
        *,
        profile_path: Path,
        admission_root: Path,
        resource_admission: ResourceAdmissionPort | None = None,
        data_policy_root: Path | None = None,
        launcher: Sequence[str] = ("gio", "launch"),
        rate_limiter: LaunchRateLimiter | None = None,
    ) -> None:
        self.profile_path = profile_path
        self.admission_root = admission_root
        self.data_policy_root = data_policy_root or (admission_root.parent / "data")
        self.resource_admission = resource_admission or FailClosedResourceAdmission()
        self.launcher = tuple(launcher)
        self.rate_limiter = rate_limiter or LaunchRateLimiter()
        if not self.launcher or not self.launcher[0]:
            raise ValueError("launcher must be a fixed argv prefix")

    def status(self) -> RuntimeStatus:
        return runtime_status(self.profile_path)

    def list_applications(self) -> tuple[NativeApplicationProjection, ...]:
        profile = load_effective_profile(self.profile_path)
        profile_id = _effective_profile_id(profile)
        status = self.status()
        policies = load_policy_catalog(self.admission_root)
        return tuple(_projection_for(policy, profile_id=profile_id, status=status) for policy in policies)

    def _policy(self, app_id: str) -> AdmissionPolicy:
        for policy in load_policy_catalog(self.admission_root):
            if policy.app_id == app_id:
                return policy
        raise NativeWorkspaceError("application_not_admitted", "native application is not admitted")

    def launch(self, request: Mapping[str, Any]) -> Mapping[str, Any]:
        app_id = _identifier(request.get("app_id"), "app_id")
        action = _identifier(request.get("action"), "action")
        correlation_id = _identifier(request.get("correlation_id"), "correlation_id")
        forbidden = {"executable", "exec", "argv", "command", "shell"} & set(request)
        if forbidden:
            raise NativeWorkspaceError("invalid_request", "executable and argv fields are prohibited")
        policy = self._policy(app_id)
        if not policy.enabled or action not in policy.allowed_actions:
            raise NativeWorkspaceError("action_not_admitted", "native application action is not admitted")
        profile = load_effective_profile(self.profile_path)
        profile_id = _effective_profile_id(profile)
        if profile_id not in policy.allowed_profile_ids or not _capability_state(profile, policy.required_capability):
            raise NativeWorkspaceError("capability_unavailable", "native workspace capability is unavailable")
        status = self.status()
        if not status.available:
            raise NativeWorkspaceError("native_workspace_unavailable", "native workspace runtime is unavailable")
        entry = resolve_desktop_entry(policy.desktop_entry_refs)
        if entry is None:
            raise NativeWorkspaceError("desktop_entry_unavailable", "desktop application metadata is unavailable")
        data_policy_path = _data_policy_path(self.data_policy_root, policy.data_policy_ref)
        load_data_policy(data_policy_path)  # fail closed when declared data semantics are unavailable
        admitted = (
            self.resource_admission.admit_policy(policy, correlation_id=correlation_id)
            if isinstance(self.resource_admission, ResourceGovernorUnixAdmission)
            else self.resource_admission.admit(
                app_id=app_id, envelope_ref=policy.resource_envelope_ref, correlation_id=correlation_id
            )
        )
        if not admitted:
            raise NativeWorkspaceError("resource_admission_blocked", "native application resource admission is blocked")

        args: list[str] = [*self.launcher, str(entry.path)]
        if action == "open_resource":
            scope = _identifier(request.get("resource_scope"), "resource_scope")
            if scope not in policy.allowed_resource_scopes:
                raise NativeWorkspaceError("resource_scope_denied", "resource scope is not admitted for this application")
            relative_path = request.get("relative_path")
            if not isinstance(relative_path, str):
                raise NativeWorkspaceError("invalid_request", "relative_path is required")
            args.append(resolve_resource(scope, relative_path).as_uri())
        elif action == "open_uri":
            uri = request.get("uri")
            if not isinstance(uri, str) or len(uri) > 4096 or "\x00" in uri:
                raise NativeWorkspaceError("invalid_request", "URI is invalid")
            parsed = urlparse(uri)
            if parsed.scheme.lower() not in policy.allowed_uri_schemes:
                raise NativeWorkspaceError("uri_scheme_denied", "URI scheme is not admitted for this application")
            args.append(uri)
        elif action != "launch":
            raise NativeWorkspaceError("action_not_admitted", "native application action is unsupported")

        self.rate_limiter.admit()
        try:
            process = subprocess.Popen(
                args,
                stdin=subprocess.DEVNULL,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                close_fds=True,
                start_new_session=True,
            )
        except OSError as exc:
            raise NativeWorkspaceError("launch_failed", "native application launcher is unavailable") from exc
        return {
            "protocol": BROKER_PROTOCOL,
            "result": "launched",
            "app_id": app_id,
            "action": action,
            "pid": process.pid,
            "correlation_id": correlation_id,
        }


class UnixBrokerServer:
    def __init__(
        self,
        broker: UserSessionAppBroker,
        socket_path: Path,
        *,
        max_request_bytes: int = MAX_REQUEST_BYTES,
        max_response_bytes: int = MAX_RESPONSE_BYTES,
    ) -> None:
        self.broker = broker
        self.socket_path = socket_path
        self.max_request_bytes = max_request_bytes
        self.max_response_bytes = max_response_bytes

    @staticmethod
    def _peer_uid(connection: socket.socket) -> int:
        if not hasattr(socket, "SO_PEERCRED"):
            raise NativeWorkspaceError("peer_unverified", "peer credential verification is unavailable")
        raw = connection.getsockopt(socket.SOL_SOCKET, socket.SO_PEERCRED, struct.calcsize("3i"))
        _, uid, _ = struct.unpack("3i", raw)
        return uid

    def _read_request(self, connection: socket.socket) -> Mapping[str, Any]:
        chunks: list[bytes] = []
        total = 0
        while True:
            chunk = connection.recv(min(8192, self.max_request_bytes + 1 - total))
            if not chunk:
                break
            total += len(chunk)
            if total > self.max_request_bytes:
                raise NativeWorkspaceError("request_too_large", "native workspace request exceeds size limit")
            chunks.append(chunk)
            if b"\n" in chunk:
                break
        raw = b"".join(chunks).split(b"\n", 1)[0]
        try:
            value = json.loads(raw.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise NativeWorkspaceError("invalid_request", "native workspace request is invalid JSON") from exc
        if not isinstance(value, Mapping):
            raise NativeWorkspaceError("invalid_request", "native workspace request must be an object")
        return value

    def _send(self, connection: socket.socket, payload: Mapping[str, Any]) -> None:
        raw = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8") + b"\n"
        if len(raw) > self.max_response_bytes:
            raw = b'{"protocol":"koa.native-workspace/v1","result":"failed","error":"response_too_large"}\n'
        connection.sendall(raw)

    def _dispatch(self, request: Mapping[str, Any]) -> Mapping[str, Any]:
        if request.get("protocol") != BROKER_PROTOCOL:
            raise NativeWorkspaceError("protocol_unsupported", "native workspace protocol is unsupported")
        operation = _identifier(request.get("operation"), "operation")
        if operation not in _ALLOWED_OPERATIONS:
            raise NativeWorkspaceError("operation_not_declared", "native workspace operation is not declared")
        if operation == "status":
            return {"protocol": BROKER_PROTOCOL, "result": "completed", "status": self.broker.status().to_dict()}
        if operation == "list":
            return {
                "protocol": BROKER_PROTOCOL,
                "result": "completed",
                "applications": [item.to_dict() for item in self.broker.list_applications()],
            }
        return {"protocol": BROKER_PROTOCOL, **self.broker.launch(request)}

    def serve_forever(self) -> None:
        runtime_root = self.socket_path.parent
        runtime_root.mkdir(mode=0o700, parents=True, exist_ok=True)
        info = runtime_root.lstat()
        if stat.S_ISLNK(info.st_mode) or info.st_uid != os.getuid() or info.st_mode & 0o077:
            raise NativeWorkspaceError("runtime_directory_unsafe", "native workspace runtime directory is unsafe")
        if self.socket_path.exists() or self.socket_path.is_symlink():
            info = self.socket_path.lstat()
            if not stat.S_ISSOCK(info.st_mode) or info.st_uid != os.getuid():
                raise NativeWorkspaceError("socket_path_unsafe", "native workspace socket path is unsafe")
            self.socket_path.unlink()
        server = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        try:
            server.bind(str(self.socket_path))
            os.chmod(self.socket_path, 0o600)
            server.listen(16)
            while True:
                connection, _ = server.accept()
                with connection:
                    started = time.monotonic()
                    try:
                        if self._peer_uid(connection) != os.getuid():
                            raise NativeWorkspaceError("peer_denied", "native workspace peer is not the session user")
                        request = self._read_request(connection)
                        response = self._dispatch(request)
                        self._send(connection, response)
                        result = response.get("result", "completed")
                        error_class = None
                    except NativeWorkspaceError as exc:
                        self._send(connection, {"protocol": BROKER_PROTOCOL, "result": "rejected", "error": exc.code})
                        result = "rejected"
                        error_class = exc.code
                    event = {
                        "operation_id": "native_workspace.request",
                        "correlation_id": request.get("correlation_id") if 'request' in locals() and isinstance(request, Mapping) else None,
                        "component": "user_session_app_broker",
                        "duration_ms": round((time.monotonic() - started) * 1000, 3),
                        "result": result,
                        "degraded": result != "completed" and result != "launched",
                        "error_class": error_class,
                    }
                    print(json.dumps(event, sort_keys=True, separators=(",", ":")), file=sys.stderr, flush=True)
        finally:
            server.close()
            try:
                self.socket_path.unlink()
            except FileNotFoundError:
                pass


def _default_socket(relative_name: str = DEFAULT_SOCKET_NAME) -> Path:
    runtime = os.environ.get("XDG_RUNTIME_DIR")
    if not runtime:
        raise NativeWorkspaceError("runtime_directory_unavailable", "XDG_RUNTIME_DIR is required")
    return Path(runtime) / relative_name


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="kOA user-session native application broker")
    parser.add_argument("--config", default="/usr/share/koa/native-workspace/native-workspace.toml")
    parser.add_argument("--profile", default=None, help="test/development override")
    parser.add_argument("--policies", default=None, help="test/development override")
    parser.add_argument("--socket", default=None, help="test/development override")
    args = parser.parse_args(argv)
    runtime_policy = load_runtime_policy(Path(args.config))
    profile_path = Path(args.profile) if args.profile else runtime_policy.profile_path
    admission_root = Path(args.policies) if args.policies else runtime_policy.admission_policy_root
    socket_path = Path(args.socket) if args.socket else _default_socket(runtime_policy.socket_relative_to_xdg_runtime)
    broker = UserSessionAppBroker(
        profile_path=profile_path,
        admission_root=admission_root,
        data_policy_root=runtime_policy.data_policy_root,
        resource_admission=ResourceGovernorUnixAdmission(),
        rate_limiter=LaunchRateLimiter(max_launches=runtime_policy.max_launches_per_minute),
    )
    UnixBrokerServer(
        broker,
        socket_path,
        max_request_bytes=runtime_policy.max_request_bytes,
        max_response_bytes=runtime_policy.max_response_bytes,
    ).serve_forever()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
