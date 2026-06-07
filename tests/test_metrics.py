from __future__ import annotations

import pytest
from task_metrics import (
    average_priority,
    completion_rate,
    count_by_status,
    filter_by_status,
    summarize_tasks,
)

TASKS = [
    {"title": "Estudar CI/CD", "status": "done", "priority": 3},
    {"title": "Configurar Actions", "status": "pending", "priority": 4},
    {"title": "Gerar graficos", "status": "blocked", "priority": 2},
    {"title": "Escrever relatorio", "status": "done", "priority": 5},
]


def test_count_by_status() -> None:
    assert count_by_status(TASKS) == {"blocked": 1, "done": 2, "pending": 1}


def test_completion_rate() -> None:
    assert completion_rate(TASKS) == 50.0


def test_average_priority() -> None:
    assert average_priority(TASKS) == 3.5


def test_filter_by_status() -> None:
    done_tasks = filter_by_status(TASKS, "done")
    assert len(done_tasks) == 2
    assert all(task["status"] == "done" for task in done_tasks)


def test_summarize_tasks() -> None:
    assert summarize_tasks(TASKS) == {
        "total": 4,
        "done": 2,
        "pending": 1,
        "blocked": 1,
        "completion_rate": 50.0,
        "average_priority": 3.5,
    }


def test_empty_task_list() -> None:
    assert completion_rate([]) == 0.0
    assert average_priority([]) == 0.0
    assert summarize_tasks([])["total"] == 0


@pytest.mark.parametrize(
    ("task", "message"),
    [
        ({"status": "done", "priority": 3}, "missing required"),
        ({"title": "X", "status": "invalid", "priority": 3}, "Invalid task status"),
        ({"title": "X", "status": "done", "priority": 8}, "priority"),
    ],
)
def test_invalid_tasks_raise_error(task: dict[str, object], message: str) -> None:
    with pytest.raises(ValueError, match=message):
        summarize_tasks([task])

