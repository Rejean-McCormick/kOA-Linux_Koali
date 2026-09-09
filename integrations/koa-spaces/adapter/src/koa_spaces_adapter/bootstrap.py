"""Composition root for the kOA-owned Koali Spaces integration adapter.

Concrete IPC belongs to the host layer.  This package accepts an injected
transport and therefore remains independently testable and free of socket,
process, database, or HTTP-client implementation ownership.
"""
from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Callable
from .capabilities import CapabilityResolver
from .client import SpacesClient, SpacesTransport
from .health import HealthChecker
from .host_bridge import HostBridge, HostLifecyclePort
from .shell_state import ShellStateReader
from .space_activation import SpaceActivator

@dataclass(frozen=True,slots=True)
class AdapterConfig:
    subsystem_id:str="koa_spaces"; timeout_seconds:float=5.0; socket_path:str="/run/koa/sockets/koa-spaces.sock"; host_start_operation_id:str=""; host_stop_operation_id:str=""; host_status_operation_id:str=""
    def __post_init__(self):
        if self.subsystem_id!="koa_spaces": raise ValueError("subsystem_id must be koa_spaces")
        if not 0<self.timeout_seconds<=60: raise ValueError("timeout_seconds must be in (0,60]")
        if not self.socket_path.startswith("/"): raise ValueError("socket_path must be absolute")

@dataclass(frozen=True,slots=True)
class KoaSpacesAdapter:
    client:SpacesClient; health:HealthChecker; capabilities:CapabilityResolver; shell:ShellStateReader; activation:SpaceActivator; host:HostBridge|None

def build_adapter(*,transport:SpacesTransport,config:AdapterConfig=AdapterConfig(),host_port:HostLifecyclePort|None=None,clock:Callable[[],datetime]=lambda:datetime.now(timezone.utc))->KoaSpacesAdapter:
    client=SpacesClient(transport,config.timeout_seconds); host=None
    if host_port is not None:
        ids=(config.host_start_operation_id,config.host_stop_operation_id,config.host_status_operation_id)
        if not all(ids): raise ValueError("all host operation identifiers are required when host_port is supplied")
        host=HostBridge(host_port,*ids)
    return KoaSpacesAdapter(client,HealthChecker(client,clock),CapabilityResolver(client,clock),ShellStateReader(client),SpaceActivator(client),host)

def bootstrap_adapter(**kwargs)->KoaSpacesAdapter:
    """Compatibility entrypoint requiring an explicit injected transport."""
    if "transport" not in kwargs or kwargs["transport"] is None:
        raise ValueError("transport is required; concrete local IPC is host-owned")
    return build_adapter(**kwargs)
