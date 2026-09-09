import json

from koa_spaces_adapter.appearance import validate_accent_palette
from koa_spaces_adapter.interface_theme import validate_theme
from ._support import ROOT


def _theme(name: str):
    path = ROOT / f"integrations/koa-spaces/interface/themes/{name}.json"
    return json.loads(path.read_text(encoding="utf-8"))


def _palette():
    path = ROOT / "integrations/koa-spaces/interface/appearance/accent-palette.json"
    return validate_accent_palette(json.loads(path.read_text(encoding="utf-8")))


def test_default_theme_is_presentation_only():
    theme = validate_theme(_theme("default"), accent_palette=_palette())
    assert theme.design_system_id == "koali.ant5"
    assert len(theme.digest) == 64


def test_reference_spaces_keep_single_konnaxion_aligned_accent():
    for name in ("default", "school", "community"):
        document = _theme(name)
        validate_theme(document, accent_palette=_palette())
        assert document["tokens"]["primary_accent"] == "#1e6864"
        assert document["framework_mapping"]["antd.colorPrimary"] == "#1e6864"
        assert document["tokens"]["surface_family"] == "neutral"
