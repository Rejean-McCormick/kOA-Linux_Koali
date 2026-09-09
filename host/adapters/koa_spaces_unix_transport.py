#!/usr/bin/env python3
"""Host-owned HTTP-over-Unix transport for the optional Koali Spaces boundary."""

from __future__ import annotations

import http.client
import json
import socket
from typing import Any, Mapping

_OPERATION_MAP = {
    "health.read": ("GET", "/health"),
    "capabilities.read": ("GET", "/capabilities"),
    "capabilities.update": ("POST", "/capabilities/update"),
    "shell.state.read": ("GET", "/shell-state"),
    "manifest.read": ("POST", "/manifest/read"),
    "space.activate": ("POST", "/space/activate"),
    "space.rollback": ("POST", "/space/rollback"),
    "space.deactivate": ("POST", "/space/deactivate"),
}


class HostTransportError(RuntimeError):
    pass


class _UnixHTTPConnection(http.client.HTTPConnection):
    def __init__(self, socket_path: str, timeout: float) -> None:
        super().__init__("localhost", timeout=timeout)
        self.socket_path = socket_path

    def connect(self) -> None:
        sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        sock.settimeout(self.timeout)
        sock.connect(self.socket_path)
        self.sock = sock


class KoaSpacesUnixHttpTransport:
    def __init__(self, socket_path: str = "/run/koa/sockets/koa-spaces.sock") -> None:
        if not socket_path.startswith("/") or len(socket_path) > 512:
            raise ValueError("socket_path must be an absolute bounded path")
        self.socket_path = socket_path

    def request(
        self,
        operation: str,
        payload: Mapping[str, Any] | None,
        *,
        timeout_seconds: float,
    ) -> Mapping[str, Any]:
        if operation not in _OPERATION_MAP:
            raise ValueError(f"unsupported operation {operation}")
        method, path = _OPERATION_MAP[operation]
        body = None
        if method != "GET":
            body = json.dumps(dict(payload or {}), separators=(",", ":"), sort_keys=True).encode()
        headers = {"Accept": "application/json"}
        if body is not None:
            headers.update({"Content-Type": "application/json", "Content-Length": str(len(body))})
        conn = _UnixHTTPConnection(self.socket_path, float(timeout_seconds))
        try:
            conn.request(method, path, body=body, headers=headers)
            response = conn.getresponse()
            raw = response.read(2_000_001)
        finally:
            conn.close()
        if len(raw) > 2_000_000:
            raise HostTransportError("Koali Spaces control response exceeds 2 MB")
        try:
            data = json.loads(raw.decode("utf-8")) if raw else {}
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise HostTransportError("Koali Spaces control response is not JSON") from exc
        if not isinstance(data, dict):
            raise HostTransportError("Koali Spaces control response must be an object")
        if response.status < 200 or response.status >= 300:
            raise HostTransportError(f"Koali Spaces control operation failed with HTTP {response.status}")
        return data
