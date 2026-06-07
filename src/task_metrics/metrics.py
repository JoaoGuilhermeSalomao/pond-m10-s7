from __future__ import annotations

from collections import Counter
from typing import Any

VALID_STATUSES = {"done", "pending", "blocked"}


def validate_task(task: dict[str, Any]) -> None:
    required = {"title", "status", "priority"}
    missing = required.difference(task)
    if missing:
        raise ValueError(f"Task missing required fields: {sorted(missing)}")

    if task["status"] not in VALID_STATUSES:
        raise ValueError(f"Invalid task status: {task['status']}")

    priority = task["priority"]
    if not isinstance(priority, int) or priority < 1 or priority > 5:
        raise ValueError("Task priority must be an integer between 1 and 5")


def count_by_status(tasks: list[dict[str, Any]]) -> dict[str, int]:
    for task in tasks:
        validate_task(task)

    counts = Counter(task["status"] for task in tasks)
    return {status: counts.get(status, 0) for status in sorted(VALID_STATUSES)}


def completion_rate(tasks: list[dict[str, Any]]) -> float:
    if not tasks:
        return 0.0

    counts = count_by_status(tasks)
    return round((counts["done"] / len(tasks)) * 100, 2)


def average_priority(tasks: list[dict[str, Any]]) -> float:
    if not tasks:
        return 0.0

    for task in tasks:
        validate_task(task)

    return round(sum(task["priority"] for task in tasks) / len(tasks), 2)


def filter_by_status(
    tasks: list[dict[str, Any]], status: str
) -> list[dict[str, Any]]:
    if status not in VALID_STATUSES:
        raise ValueError(f"Invalid task status: {status}")

    for task in tasks:
        validate_task(task)

    return [task for task in tasks if task["status"] == status]


def summarize_tasks(tasks: list[dict[str, Any]]) -> dict[str, float | int]:
    counts = count_by_status(tasks)
    return {
        "total": len(tasks),
        "done": counts["done"],
        "pending": counts["pending"],
        "blocked": counts["blocked"],
        "completion_rate": completion_rate(tasks),
        "average_priority": average_priority(tasks),
    }

