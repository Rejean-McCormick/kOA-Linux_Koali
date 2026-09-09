"""Pure Koali Spaces bridge to the local kOA Native Workspace protocol.

The integration adapter exposes only minimized availability/projection data and
high-level launch intents.  Concrete Unix socket ownership remains in host/adapters.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping, Protocol


class NativeWorkspaceBridgeError(RuntimeError):
    """Stable presentation bridge failure."""


class NativeWorkspaceTransport(Protocol):
    def request(self, payload: Mapping[str, Any], *, timeout_seconds: float) -> Mapping[str, Any]: ...


@dataclass(frozen=True, slots=True)
class NativeLaunchIntent:
    app_id: str
    action: str
    correlation_id: str
    resource_scope: str | None = None
    relative_path: str | None = None
    uri: str | None = None

    def to_payload(self) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "protocol": "koa.native-workspace/v1",
            "operation": "launch",
            "app_id": self.app_id,
            "action": self.action,
            "correlation_id": self.correlation_id,
        }
        if self.resource_scope is not None:
            payload["resource_scope"] = self.resource_scope
        if self.relative_path is not None:
            payload["relative_path"] = self.relative_path
        if self.uri is not None:
            payload["uri"] = self.uri
        return payload


class NativeWorkspaceBridge:
    def __init__(self, transport: NativeWorkspaceTransport, *, timeout_seconds: float = 0.5) -> None:
        if timeout_seconds <= 0 or timeout_seconds > 5:
            raise ValueError("timeout_seconds must be within (0, 5]")
        self.transport = transport
        self.timeout_seconds = timeout_seconds

    def _call(self, payload: Mapping[str, Any]) -> Mapping[str, Any]:
        try:
            result = self.transport.request(payload, timeout_seconds=self.timeout_seconds)
        except (OSError, TimeoutError, ConnectionError) as exc:
            raise NativeWorkspaceBridgeError("native workspace is unavailable") from exc
        if not isinstance(result, Mapping) or result.get("protocol") != "koa.native-workspace/v1":
            raise NativeWorkspaceBridgeError("native workspace returned an invalid response")
        return result

    def status(self) -> Mapping[str, Any]:
        result = self._call({"protocol": "koa.native-workspace/v1", "operation": "status"})
        if result.get("result") != "completed" or not isinstance(result.get("status"), Mapping):
            raise NativeWorkspaceBridgeError("native workspace status is unavailable")
        status = result["status"]
        # Minimize for Koali presentation: health/readiness remains non-authoritative.
        return {
            "available": status.get("available") is True,
            "capability_present": status.get("capability_present") is True,
            "graphical_session_ready": status.get("graphical_session_ready") is True,
            "reasons": list(status.get("reasons") or []),
        }

    def applications(self) -> tuple[Mapping[str, Any], ...]:
        result = self._call({"protocol": "koa.native-workspace/v1", "operation": "list"})
        raw = result.get("applications")
        if result.get("result") != "completed" or not isinstance(raw, list):
            raise NativeWorkspaceBridgeError("native application projection is unavailable")
        projected: list[Mapping[str, Any]] = []
        for item in raw:
            if not isinstance(item, Mapping):
                raise NativeWorkspaceBridgeError("native application projection is invalid")
            required = {"app_id", "display_name", "available", "allowed_actions", "security_class"}
            if not required <= set(item):
                raise NativeWorkspaceBridgeError("native application projection is incomplete")
            projected.append({
                "app_id": item["app_id"],
                "display_name": item["display_name"],
                "icon_ref": item.get("icon_ref"),
                "available": item["available"] is True,
                "allowed_actions": list(item.get("allowed_actions") or []),
                "security_class": item["security_class"],
                "reason": item.get("reason"),
            })
        return tuple(projected)

    def launch(self, intent: NativeLaunchIntent) -> Mapping[str, Any]:
        payload = intent.to_payload()
        forbidden = {"exec", "executable", "argv", "command", "shell"} & set(payload)
        if forbidden:
            raise NativeWorkspaceBridgeError("raw executable launch fields are prohibited")
        result = self._call(payload)
        if result.get("result") != "launched":
            raise NativeWorkspaceBridgeError(str(result.get("error") or "native application launch rejected"))
        return {
            "result": "launched",
            "app_id": result.get("app_id"),
            "action": result.get("action"),
            "correlation_id": result.get("correlation_id"),
        }


__all__ = [
    "NativeLaunchIntent",
    "NativeWorkspaceBridge",
    "NativeWorkspaceBridgeError",
    "NativeWorkspaceTransport",
]
