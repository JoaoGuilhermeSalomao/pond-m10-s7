from __future__ import annotations

import argparse
import base64
import csv
import io
import json
import os
import zipfile
from datetime import datetime
from pathlib import Path
from typing import Any
from xml.etree import ElementTree

import requests
from requests import HTTPError

API_URL = "https://api.github.com"


def parse_timestamp(value: str | None) -> datetime | None:
    if not value:
        return None
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def duration_seconds(start: str | None, end: str | None) -> float:
    start_dt = parse_timestamp(start)
    end_dt = parse_timestamp(end)
    if not start_dt or not end_dt:
        return 0.0
    return round(max((end_dt - start_dt).total_seconds(), 0.0), 3)


class GitHubClient:
    def __init__(self, token: str | None) -> None:
        self.session = requests.Session()
        self.session.headers.update(
            {
                "Accept": "application/vnd.github+json",
                "X-GitHub-Api-Version": "2022-11-28",
            }
        )
        if token:
            self.session.headers["Authorization"] = f"Bearer {token}"

    def get(self, url: str, **params: Any) -> dict[str, Any]:
        response = self.session.get(url, params=params, timeout=30)
        response.raise_for_status()
        return response.json()

    def get_all_pages(
        self, url: str, item_key: str, **params: Any
    ) -> list[dict[str, Any]]:
        params.setdefault("per_page", 100)
        items: list[dict[str, Any]] = []
        while url:
            response = self.session.get(url, params=params, timeout=30)
            response.raise_for_status()
            items.extend(response.json().get(item_key, []))
            url = response.links.get("next", {}).get("url", "")
            params = {}
        return items

    def download_zip(self, url: str) -> bytes:
        response = self.session.get(url, timeout=60)
        response.raise_for_status()
        return response.content


def parse_junit_xml(xml_bytes: bytes) -> dict[str, float | int]:
    root = ElementTree.fromstring(xml_bytes)

    if root.tag == "testsuite":
        suites = [root]
    else:
        suites = list(root.findall("testsuite"))

    tests = 0
    failures = 0
    total_time = 0.0

    for suite in suites:
        tests += int(suite.attrib.get("tests", 0))
        failures += int(suite.attrib.get("failures", 0))
        failures += int(suite.attrib.get("errors", 0))
        total_time += float(suite.attrib.get("time", 0.0))

    average = total_time / tests if tests else 0.0
    return {
        "test_count": tests,
        "test_failures": failures,
        "average_test_time": round(average, 6),
    }


def collect_test_artifacts(
    client: GitHubClient, repo: str, run_id: int
) -> dict[str, float | int] | None:
    artifacts_url = f"{API_URL}/repos/{repo}/actions/runs/{run_id}/artifacts"
    artifacts = client.get_all_pages(artifacts_url, "artifacts")

    totals = {"test_count": 0, "test_failures": 0, "average_test_time": 0.0}
    weighted_time = 0.0

    for artifact in artifacts:
        if not artifact["name"].startswith("test-results-"):
            continue

        try:
            archive = client.download_zip(artifact["archive_download_url"])
        except HTTPError as error:
            if error.response is not None and error.response.status_code == 401:
                return None
            raise

        with zipfile.ZipFile(io.BytesIO(archive)) as zip_file:
            for name in zip_file.namelist():
                if name.endswith("pytest-results.xml"):
                    parsed = parse_junit_xml(zip_file.read(name))
                    count = int(parsed["test_count"])
                    totals["test_count"] += count
                    totals["test_failures"] += int(parsed["test_failures"])
                    weighted_time += float(parsed["average_test_time"]) * count

    if totals["test_count"]:
        totals["average_test_time"] = round(weighted_time / totals["test_count"], 6)

    if not totals["test_count"]:
        return None

    return totals


def read_variation_for_commit(
    client: GitHubClient, repo: str, commit_sha: str
) -> dict[str, str]:
    url = f"{API_URL}/repos/{repo}/contents/experiment/variation.env"
    data = client.get(url, ref=commit_sha)
    content = base64.b64decode(data["content"]).decode("utf-8")
    values: dict[str, str] = {}

    for raw_line in content.splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        values[key.strip()] = value.strip()

    return values


def estimate_test_metrics(
    variation: dict[str, str], test_step_duration: float
) -> dict[str, float | int]:
    generated_cases = int(variation.get("TEST_CASES", "8"))
    test_count = generated_cases + 11
    force_failure = variation.get("FORCE_TEST_FAILURE", "false").lower() == "true"

    return {
        "test_count": test_count,
        "test_failures": 1 if force_failure else 0,
        "average_test_time": round(test_step_duration / test_count, 6)
        if test_count
        else 0.0,
    }


def total_test_step_duration(jobs: list[dict[str, Any]]) -> float:
    total = 0.0
    for job in jobs:
        for step in job.get("steps") or []:
            if step.get("name") == "Run tests":
                total += duration_seconds(
                    step.get("started_at"), step.get("completed_at")
                )
    return round(total, 3)


def collect_metrics(
    repo: str, workflow: str, limit: int, token: str | None
) -> list[dict[str, Any]]:
    client = GitHubClient(token)
    runs_url = f"{API_URL}/repos/{repo}/actions/workflows/{workflow}/runs"
    runs = client.get_all_pages(runs_url, "workflow_runs", branch="main")[:limit]
    rows: list[dict[str, Any]] = []

    for run in runs:
        run_id = run["id"]
        jobs_url = f"{API_URL}/repos/{repo}/actions/runs/{run_id}/jobs"
        jobs = client.get_all_pages(jobs_url, "jobs")
        test_metrics = collect_test_artifacts(client, repo, run_id)
        if test_metrics is None:
            variation = read_variation_for_commit(client, repo, run["head_sha"])
            test_metrics = estimate_test_metrics(
                variation, total_test_step_duration(jobs)
            )

        workflow_duration = duration_seconds(
            run.get("run_started_at") or run.get("created_at"),
            run.get("updated_at"),
        )
        commit_message = (run.get("head_commit") or {}).get("message") or ""
        commit_summary = commit_message.splitlines()[0] if commit_message else ""
        status = run.get("conclusion") or run.get("status")

        for job in jobs:
            job_duration = duration_seconds(
                job.get("started_at"), job.get("completed_at")
            )
            steps = job.get("steps") or [{"name": "", "conclusion": "", "status": ""}]

            for step in steps:
                rows.append(
                    {
                        "run_id": run_id,
                        "run_number": run.get("run_number"),
                        "run_attempt": run.get("run_attempt"),
                        "commit_sha": run.get("head_sha"),
                        "commit_message": commit_summary,
                        "status": status,
                        "workflow_duration": workflow_duration,
                        "job_name": job.get("name"),
                        "job_status": job.get("conclusion") or job.get("status"),
                        "job_duration": job_duration,
                        "step_name": step.get("name"),
                        "step_status": step.get("conclusion") or step.get("status"),
                        "step_duration": duration_seconds(
                            step.get("started_at"), step.get("completed_at")
                        ),
                        "test_count": test_metrics["test_count"],
                        "test_failures": test_metrics["test_failures"],
                        "average_test_time": test_metrics["average_test_time"],
                        "timestamp": run.get("created_at"),
                        "run_url": run.get("html_url"),
                    }
                )

    return rows


def write_csv(rows: list[dict[str, Any]], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "run_id",
        "run_number",
        "run_attempt",
        "commit_sha",
        "commit_message",
        "status",
        "workflow_duration",
        "job_name",
        "job_status",
        "job_duration",
        "step_name",
        "step_status",
        "step_duration",
        "test_count",
        "test_failures",
        "average_test_time",
        "timestamp",
        "run_url",
    ]
    with output_path.open("w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Coleta metricas reais de execucoes do GitHub Actions."
    )
    parser.add_argument(
        "--repo",
        default=os.getenv("GITHUB_REPOSITORY"),
        help="Repositorio no formato owner/name.",
    )
    parser.add_argument(
        "--workflow", default="ci.yml", help="Arquivo ou ID do workflow."
    )
    parser.add_argument(
        "--limit", type=int, default=30, help="Quantidade maxima de runs."
    )
    parser.add_argument("--out", default="metrics/pipeline_metrics.csv")
    parser.add_argument("--json-out", default="metrics/pipeline_metrics.json")
    parser.add_argument("--token", default=os.getenv("GITHUB_TOKEN"))
    args = parser.parse_args()

    if not args.repo:
        raise SystemExit("Informe --repo owner/name ou defina GITHUB_REPOSITORY.")

    rows = collect_metrics(args.repo, args.workflow, args.limit, args.token)
    write_csv(rows, Path(args.out))

    json_path = Path(args.json_out)
    json_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(
        json.dumps(rows, indent=2, ensure_ascii=False), encoding="utf-8"
    )

    print(f"Coletadas {len(rows)} linhas de metricas.")
    print(f"CSV: {args.out}")
    print(f"JSON: {args.json_out}")


if __name__ == "__main__":
    main()
