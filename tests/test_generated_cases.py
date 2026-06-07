from __future__ import annotations

import pytest
from task_metrics import summarize_tasks

from tests.conftest import read_variation


def build_tasks(size: int) -> list[dict[str, object]]:
    statuses = ["done", "pending", "blocked"]
    return [
        {
            "title": f"Tarefa gerada {index}",
            "status": statuses[index % len(statuses)],
            "priority": (index % 5) + 1,
        }
        for index in range(size)
    ]


variation = read_variation()
case_count = int(variation.get("TEST_CASES", "8"))


@pytest.mark.parametrize("size", range(1, case_count + 1))
def test_generated_task_summaries(size: int) -> None:
    summary = summarize_tasks(build_tasks(size))
    assert summary["total"] == size
    assert summary["done"] + summary["pending"] + summary["blocked"] == size
    assert 0.0 <= summary["completion_rate"] <= 100.0
    assert 1.0 <= summary["average_priority"] <= 5.0

