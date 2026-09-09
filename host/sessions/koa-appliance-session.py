#!/usr/bin/env python3
"""Entry point for the ordinary restricted kOA appliance session.

The user-session Native Workspace broker is an optional, unprivileged companion
process.  It is started only when the already-resolved profile explicitly grants
``user.native_workspace``.  Broker failure degrades native launching without
replacing or terminating the Koali/appliance session.
"""

from __future__ import annotations

import os
from pathlib import Path
import subprocess

from native_workspace import native_workspace_enabled
from session_runtime import main_for_mode


def _start_native_workspace_broker() -> subprocess.Popen[bytes] | None:
    profile_value = os.environ.get("KOA_EFFECTIVE_PROFILE_PATH")
    if not profile_value:
        return None
    profile = Path(profile_value)
    if not native_workspace_enabled(profile):
        return None
    broker = Path(__file__).with_name("koa-native-workspace-broker")
    if not broker.exists():
        broker = Path(__file__).with_name("koa-native-workspace-broker.py")
    try:
        return subprocess.Popen(
            [str(broker), "--profile", str(profile)],
            stdin=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL,
            stderr=None,
            close_fds=True,
        )
    except OSError:
        return None


def main() -> int:
    broker = _start_native_workspace_broker()
    try:
        return main_for_mode("interactive_user")
    finally:
        if broker is not None and broker.poll() is None:
            broker.terminate()
            try:
                broker.wait(timeout=2)
            except subprocess.TimeoutExpired:
                broker.kill()
                broker.wait(timeout=1)


if __name__ == "__main__":
    raise SystemExit(main())
