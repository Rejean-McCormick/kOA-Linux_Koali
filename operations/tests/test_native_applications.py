from __future__ import annotations

import json
from pathlib import Path

import pytest

from koa_operations.backup.native_applications import (
    NativeApplicationDataPolicyError,
    resolve_native_application_data_policy,
)

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent


def test_firefox_policy_resolves_persistent_profile_and_disposable_cache(tmp_path: Path) -> None:
    home = tmp_path / "user"
    selection = resolve_native_application_data_policy(
        REPO / "profiles/native-applications/data/firefox.json",
        home=home,
    )
    assert selection.policy_id == "native.firefox.data"
    assert [item.resolved_path for item in selection.persistent_profile_paths] == [home / ".mozilla/firefox"]
    assert [item.resolved_path for item in selection.disposable_cache_paths] == [home / ".cache/mozilla/firefox"]
    assert selection.documents_external is True
    assert selection.requires_compatible_profile is True
    assert selection.checkpoint_when_required is True


def test_native_data_policy_rejects_path_escape(tmp_path: Path) -> None:
    source = json.loads((REPO / "profiles/native-applications/data/vlc.json").read_text(encoding="utf-8"))
    source["profile_locations"] = [{"root": "xdg_config", "relative_path": "../escape"}]
    policy = tmp_path / "invalid.json"
    policy.write_text(json.dumps(source), encoding="utf-8")
    with pytest.raises(NativeApplicationDataPolicyError):
        resolve_native_application_data_policy(policy, home=tmp_path / "home")


def test_disposable_cache_cannot_be_reclassified_outside_xdg_cache(tmp_path: Path) -> None:
    source = json.loads((REPO / "profiles/native-applications/data/libreoffice.json").read_text(encoding="utf-8"))
    source["cache_locations"] = [{"root": "home", "relative_path": ".cache/libreoffice"}]
    policy = tmp_path / "invalid-cache.json"
    policy.write_text(json.dumps(source), encoding="utf-8")
    with pytest.raises(NativeApplicationDataPolicyError):
        resolve_native_application_data_policy(policy, home=tmp_path / "home")
