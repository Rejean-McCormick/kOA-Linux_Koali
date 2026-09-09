from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
BASE = ROOT / "host/image/base-packages.yaml"
OVERLAY = ROOT / "host/image/package-sets/user-lightweight.yaml"


def _load(relative: str, name: str):
    path = ROOT / relative
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_user_lightweight_package_set_extends_baseline_without_mutating_it() -> None:
    materializer = _load("host/image/materialize-rootfs.py", "native_pkg_materializer")
    base = json.loads(BASE.read_text(encoding="utf-8"))
    effective, raw = materializer._select_package_set(base, BASE, "user_lightweight")

    assert raw == OVERLAY.read_bytes()
    assert base["profile_id"] == "sovereign_linux_node"
    assert effective["profile_id"] == "user_lightweight"
    assert effective["package_set_id"] == "koa.host.user-lightweight-packages"

    baseline = {item["id"] for item in base["required_capabilities"]}
    selected = {item["id"] for item in effective["required_capabilities"]}
    assert baseline < selected
    assert {
        "wayland-session",
        "user-dbus",
        "xdg-desktop-portals",
        "desktop-mime-open",
        "desktop-audio",
        "native-firefox",
        "native-vlc",
        "native-libreoffice",
        "native-thunderbird",
    } <= selected


def test_unknown_profile_package_set_fails_closed() -> None:
    materializer = _load("host/image/materialize-rootfs.py", "native_pkg_materializer_unknown")
    base = json.loads(BASE.read_text(encoding="utf-8"))
    try:
        materializer._select_package_set(base, BASE, "unknown_profile")
    except materializer.MaterializationError as exc:
        assert "profile_package_set_unavailable" in str(exc)
    else:
        raise AssertionError("unknown profile package set must fail closed")


def test_rootfs_builder_uses_same_profile_package_set() -> None:
    builder = _load("host/image/build-rootfs.py", "native_pkg_builder")
    base = json.loads(BASE.read_text(encoding="utf-8"))
    effective, raw = builder._select_package_set(base, BASE, "user_lightweight")
    assert raw == OVERLAY.read_bytes()
    assert effective["package_set_id"] == "koa.host.user-lightweight-packages"
    assert effective["profile_id"] == "user_lightweight"
