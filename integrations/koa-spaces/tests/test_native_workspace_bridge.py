from __future__ import annotations

from typing import Any, Mapping

import pytest

from koa_spaces_adapter.native_workspace import (
    NativeLaunchIntent,
    NativeWorkspaceBridge,
    NativeWorkspaceBridgeError,
)


class Transport:
    def __init__(self) -> None:
        self.requests: list[Mapping[str, Any]] = []

    def request(self, payload: Mapping[str, Any], *, timeout_seconds: float) -> Mapping[str, Any]:
        self.requests.append(dict(payload))
        operation = payload["operation"]
        if operation == "status":
            return {"protocol":"koa.native-workspace/v1","result":"completed","status":{"available":True,"capability_present":True,"graphical_session_ready":True,"substrate":{"wayland":True},"reasons":[]}}
        if operation == "list":
            return {"protocol":"koa.native-workspace/v1","result":"completed","applications":[{"app_id":"firefox","display_name":"Firefox","icon_ref":"firefox","available":True,"allowed_actions":["launch","open_uri"],"security_class":"web","reason":None,"internal_path":"must_not_escape"}]}
        return {"protocol":"koa.native-workspace/v1","result":"launched","app_id":payload["app_id"],"action":payload["action"],"correlation_id":payload["correlation_id"],"pid":1234}


def test_native_workspace_bridge_minimizes_projection() -> None:
    bridge = NativeWorkspaceBridge(Transport())
    assert bridge.status()["available"] is True
    applications = bridge.applications()
    assert applications == ({
        "app_id":"firefox","display_name":"Firefox","icon_ref":"firefox","available":True,
        "allowed_actions":["launch","open_uri"],"security_class":"web","reason":None,
    },)
    assert "internal_path" not in applications[0]


def test_native_workspace_bridge_routes_high_level_launch_only() -> None:
    transport = Transport()
    bridge = NativeWorkspaceBridge(transport)
    result = bridge.launch(NativeLaunchIntent(app_id="firefox", action="open_uri", correlation_id="corr-1", uri="https://example.test"))
    assert result["result"] == "launched"
    request = transport.requests[-1]
    assert request["uri"] == "https://example.test"
    assert not ({"exec","executable","argv","command","shell"} & set(request))


def test_native_workspace_bridge_fails_closed_on_bad_protocol() -> None:
    class Bad:
        def request(self, payload, *, timeout_seconds):
            return {"protocol":"unexpected","result":"completed"}
    with pytest.raises(NativeWorkspaceBridgeError):
        NativeWorkspaceBridge(Bad()).status()
