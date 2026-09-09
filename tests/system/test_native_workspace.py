from __future__ import annotations

import importlib.util
import json
import os
from pathlib import Path
import sys

import pytest
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[2]
MODULE_PATH = ROOT / "host/sessions/native_workspace.py"
SPEC = importlib.util.spec_from_file_location("koa_native_workspace_session", MODULE_PATH)
assert SPEC and SPEC.loader
native = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = native
SPEC.loader.exec_module(native)


def _write_profile(path: Path, *, capability: str = "user.native_workspace") -> None:
    path.write_text(
        json.dumps(
            {
                "effective_profile_id": "user_lightweight",
                "capabilities": {capability: {"state": "required"}},
            }
        ),
        encoding="utf-8",
    )


def _copy_policies(tmp_path: Path) -> Path:
    root = tmp_path / "native-applications"
    (root / "admission").mkdir(parents=True)
    (root / "data").mkdir()
    for source in (ROOT / "profiles/native-applications/admission").glob("*.json"):
        (root / "admission" / source.name).write_bytes(source.read_bytes())
    for source in (ROOT / "profiles/native-applications/data").glob("*.json"):
        (root / "data" / source.name).write_bytes(source.read_bytes())
    return root / "admission"


def _desktop(tmp_path: Path, name: str, display: str) -> None:
    app_dir = tmp_path / "share/applications"
    app_dir.mkdir(parents=True, exist_ok=True)
    (app_dir / name).write_text(
        f"[Desktop Entry]\nType=Application\nName={display}\nExec=/ignored/by/koa %U\nIcon={display.lower()}\n",
        encoding="utf-8",
    )


def _ready(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        native,
        "probe_substrate",
        lambda: {
            "wayland": True,
            "user_dbus": True,
            "audio": True,
            "gio": True,
            "xdg_mime": True,
            "portal": True,
            "resource_governor": True,
        },
    )


def test_native_policy_artifacts_validate_against_canonical_schemas() -> None:
    schema_root = ROOT / "docs/contracts/artifact-contracts"
    admission_schema = json.loads((schema_root / "native-application-admission-policy.schema.json").read_text())
    data_schema = json.loads((schema_root / "native-application-data-policy.schema.json").read_text())
    for path in (ROOT / "profiles/native-applications/admission").glob("*.json"):
        Draft202012Validator(admission_schema).validate(json.loads(path.read_text()))
    for path in (ROOT / "profiles/native-applications/data").glob("*.json"):
        Draft202012Validator(data_schema).validate(json.loads(path.read_text()))


def test_projection_uses_freedesktop_metadata_without_exposing_exec(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    profile = tmp_path / "profile.json"
    _write_profile(profile)
    policies = _copy_policies(tmp_path)
    _desktop(tmp_path, "firefox.desktop", "Firefox")
    monkeypatch.setenv("XDG_DATA_HOME", str(tmp_path / "share"))
    _ready(monkeypatch)
    broker = native.UserSessionAppBroker(
        profile_path=profile,
        admission_root=policies,
        resource_admission=native.PermissiveTestResourceAdmission(),
        launcher=("/bin/true",),
    )
    firefox = next(item for item in broker.list_applications() if item.app_id == "firefox")
    payload = firefox.to_dict()
    assert payload["display_name"] == "Firefox"
    assert payload["available"] is True
    assert "exec" not in json.dumps(payload).lower()


def test_launch_rejects_executable_and_argv_even_for_admitted_app(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    profile = tmp_path / "profile.json"
    _write_profile(profile)
    policies = _copy_policies(tmp_path)
    _desktop(tmp_path, "firefox.desktop", "Firefox")
    monkeypatch.setenv("XDG_DATA_HOME", str(tmp_path / "share"))
    _ready(monkeypatch)
    broker = native.UserSessionAppBroker(
        profile_path=profile,
        admission_root=policies,
        resource_admission=native.PermissiveTestResourceAdmission(),
        launcher=("/bin/true",),
    )
    with pytest.raises(native.NativeWorkspaceError, match="executable and argv"):
        broker.launch(
            {
                "app_id": "firefox",
                "action": "launch",
                "correlation_id": "corr-1",
                "argv": ["--private-window"],
            }
        )


def test_resource_scope_rejects_path_traversal(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    downloads = tmp_path / "Downloads"
    downloads.mkdir()
    monkeypatch.setenv("XDG_DOWNLOADS_DIR", str(downloads))
    with pytest.raises(native.NativeWorkspaceError, match="escapes"):
        native.resolve_resource("downloads", "../secret.txt")


def test_default_resource_admission_is_fail_closed(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    profile = tmp_path / "profile.json"
    _write_profile(profile)
    policies = _copy_policies(tmp_path)
    _desktop(tmp_path, "firefox.desktop", "Firefox")
    monkeypatch.setenv("XDG_DATA_HOME", str(tmp_path / "share"))
    _ready(monkeypatch)
    broker = native.UserSessionAppBroker(
        profile_path=profile,
        admission_root=policies,
        resource_admission=native.FailClosedResourceAdmission(),
        launcher=("/bin/true",),
    )
    with pytest.raises(native.NativeWorkspaceError) as error:
        broker.launch({"app_id": "firefox", "action": "launch", "correlation_id": "corr-2"})
    assert error.value.code == "resource_admission_blocked"


def test_remote_network_transport_is_not_part_of_broker_contract() -> None:
    text = MODULE_PATH.read_text(encoding="utf-8")
    assert "AF_INET" not in text
    assert "0.0.0.0" not in text
    assert "SO_PEERCRED" in text
    assert native.BROKER_PROTOCOL == "koa.native-workspace/v1"


def test_runtime_policy_is_loaded_and_enforces_local_security_invariants(tmp_path: Path) -> None:
    source = ROOT / "host/sessions/native-workspace.toml"
    policy = native.load_runtime_policy(source)
    assert policy.profile_path == Path("/etc/koa/active/profile.json")
    assert policy.admission_policy_root == Path("/usr/share/koa/native-apps/admission")
    assert policy.socket_relative_to_xdg_runtime == "koa/native-workspace.sock"
    assert policy.max_launches_per_minute == 12

    bad = tmp_path / "bad.toml"
    text = source.read_text(encoding="utf-8").replace("network_listener = false", "network_listener = true")
    bad.write_text(text, encoding="utf-8")
    with pytest.raises(native.NativeWorkspaceError, match="network_listener"):
        native.load_runtime_policy(bad)


def test_runtime_policy_rejects_socket_escape(tmp_path: Path) -> None:
    source = ROOT / "host/sessions/native-workspace.toml"
    bad = tmp_path / "bad-socket.toml"
    text = source.read_text(encoding="utf-8").replace(
        'socket_relative_to_xdg_runtime = "koa/native-workspace.sock"',
        'socket_relative_to_xdg_runtime = "../outside.sock"',
    )
    bad.write_text(text, encoding="utf-8")
    with pytest.raises(native.NativeWorkspaceError, match="relative"):
        native.load_runtime_policy(bad)
