from __future__ import annotations

import time

from tests.conftest import read_variation


def test_controlled_failure_mode() -> None:
    variation = read_variation()
    assert variation.get("FORCE_TEST_FAILURE", "false").lower() != "true"


def test_optional_slow_test() -> None:
    variation = read_variation()
    delay = float(variation.get("SLOW_TEST_SECONDS", "0"))
    if delay > 0:
        time.sleep(delay)
    assert delay >= 0

