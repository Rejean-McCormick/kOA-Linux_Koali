#!/usr/bin/env python3
"""Installed entrypoint for the unprivileged kOA Native Workspace broker."""
from native_workspace import main

if __name__ == "__main__":
    raise SystemExit(main())
