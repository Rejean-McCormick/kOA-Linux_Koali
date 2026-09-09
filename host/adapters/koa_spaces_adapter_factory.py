#!/usr/bin/env python3
"""Host composition root binding the pure kOA Spaces adapter to local Unix IPC."""

from __future__ import annotations

from koa_spaces_adapter import AdapterConfig, build_adapter

from koa_spaces_unix_transport import KoaSpacesUnixHttpTransport


def build_local_koa_spaces_adapter(config: AdapterConfig = AdapterConfig()):
    return build_adapter(
        transport=KoaSpacesUnixHttpTransport(config.socket_path),
        config=config,
    )
