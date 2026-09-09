#!/usr/bin/env python3
"""Host-owned Unix transport for the user-session Native Workspace broker."""
from __future__ import annotations

import json
import os
from pathlib import Path
import socket
from typing import Any, Mapping

_MAX_RESPONSE_BYTES = 2 * 1024 * 1024


class NativeWorkspaceUnixTransport:
    def __init__(self, socket_path: str | Path | None = None) -> None:
        if socket_path is None:
            runtime = os.environ.get("XDG_RUNTIME_DIR")
            if not runtime:
                raise ValueError("XDG_RUNTIME_DIR is required for local Native Workspace")
            socket_path = Path(runtime) / "koa/native-workspace.sock"
        self.socket_path = Path(socket_path)
        if not self.socket_path.is_absolute():
            raise ValueError("native workspace socket path must be absolute")

    def request(self, payload: Mapping[str, Any], *, timeout_seconds: float) -> Mapping[str, Any]:
        forbidden = {"exec", "executable", "argv", "command", "shell"} & set(payload)
        if forbidden:
            raise ValueError("raw executable launch fields are prohibited")
        raw = json.dumps(dict(payload), sort_keys=True, separators=(",", ":")).encode("utf-8") + b"\n"
        if len(raw) > 65536:
            raise ValueError("native workspace request exceeds size limit")
        sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        sock.settimeout(float(timeout_seconds))
        try:
            sock.connect(str(self.socket_path))
            sock.sendall(raw)
            chunks: list[bytes] = []
            total = 0
            while True:
                chunk = sock.recv(min(8192, _MAX_RESPONSE_BYTES + 1 - total))
                if not chunk:
                    break
                total += len(chunk)
                if total > _MAX_RESPONSE_BYTES:
                    raise ValueError("native workspace response exceeds size limit")
                chunks.append(chunk)
                if b"\n" in chunk:
                    break
        finally:
            sock.close()
        response = b"".join(chunks).split(b"\n", 1)[0]
        value = json.loads(response.decode("utf-8"))
        if not isinstance(value, dict):
            raise ValueError("native workspace response must be an object")
        return value
