from __future__ import annotations

import pytest

from koa_spaces_adapter import bootstrap_adapter


def test_concrete_unix_transport_is_not_owned_by_integration_package():
    with pytest.raises(ValueError, match="transport is required"):
        bootstrap_adapter()
