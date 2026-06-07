from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


def load_metrics(path: Path) -> pd.DataFrame:
    if not path.exists():
        raise SystemExit(f"Arquivo de metricas nao encontrado: {path}")

    df = pd.read_csv(path)
    if df.empty:
        raise SystemExit("Arquivo de metricas esta vazio.")

    numeric_columns = [
        "workflow_duration",
        "job_duration",
        "step_duration",
        "test_count",
        "test_failures",
        "average_test_time",
    ]
    for column in numeric_columns:
        df[column] = pd.to_numeric(df[column], errors="coerce").fillna(0)

    return df


def unique_runs(df: pd.DataFrame) -> pd.DataFrame:
    runs = df.sort_values("run_number").drop_duplicates("run_id")
    return runs.sort_values("run_number")


def plot_total_duration(df: pd.DataFrame, output_dir: Path) -> None:
    runs = unique_runs(df)
    colors = runs["status"].map({"success": "#2e7d32", "failure": "#c62828"}).fillna(
        "#455a64"
    )

    plt.figure(figsize=(11, 6))
    plt.bar(runs["run_number"].astype(str), runs["workflow_duration"], color=colors)
    plt.title("Tempo total do pipeline por execucao")
    plt.xlabel("Numero da execucao")
    plt.ylabel("Duracao do workflow (s)")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(output_dir / "tempo-total-pipeline.png", dpi=160)
    plt.close()


def plot_job_duration(df: pd.DataFrame, output_dir: Path) -> None:
    jobs = (
        df[df["job_status"] != "skipped"]
        .drop_duplicates(["run_id", "job_name"])
        .groupby("job_name", as_index=False)["job_duration"]
        .mean()
        .sort_values("job_duration", ascending=False)
    )

    plt.figure(figsize=(11, 6))
    plt.barh(jobs["job_name"], jobs["job_duration"], color="#1565c0")
    plt.title("Tempo medio por job")
    plt.xlabel("Duracao media (s)")
    plt.ylabel("Job")
    plt.gca().invert_yaxis()
    plt.tight_layout()
    plt.savefig(output_dir / "tempo-por-job.png", dpi=160)
    plt.close()


def plot_success_failure(df: pd.DataFrame, output_dir: Path) -> None:
    runs = unique_runs(df)
    counts = (
        runs["status"].value_counts().rename_axis("status").reset_index(name="total")
    )
    colors = counts["status"].map({"success": "#2e7d32", "failure": "#c62828"}).fillna(
        "#455a64"
    )

    plt.figure(figsize=(8, 6))
    plt.bar(counts["status"], counts["total"], color=colors)
    plt.title("Taxa de sucesso e falha")
    plt.xlabel("Status")
    plt.ylabel("Quantidade de execucoes")
    plt.tight_layout()
    plt.savefig(output_dir / "taxa-sucesso-falha.png", dpi=160)
    plt.close()


def plot_tests_vs_duration(df: pd.DataFrame, output_dir: Path) -> None:
    runs = unique_runs(df)
    colors = runs["status"].map({"success": "#2e7d32", "failure": "#c62828"}).fillna(
        "#455a64"
    )

    plt.figure(figsize=(10, 6))
    plt.scatter(
        runs["test_count"],
        runs["workflow_duration"],
        c=colors,
        s=90,
        edgecolors="#263238",
        linewidths=0.8,
    )
    for _, row in runs.iterrows():
        plt.annotate(
            str(row["run_number"]),
            (row["test_count"], row["workflow_duration"]),
        )
    plt.title("Relacao entre quantidade de testes e duracao do pipeline")
    plt.xlabel("Quantidade de testes")
    plt.ylabel("Duracao do workflow (s)")
    plt.tight_layout()
    plt.savefig(output_dir / "testes-vs-duracao.png", dpi=160)
    plt.close()


def main() -> None:
    parser = argparse.ArgumentParser(description="Gera graficos das metricas de CI/CD.")
    parser.add_argument("--input", default="metrics/pipeline_metrics.csv")
    parser.add_argument("--out-dir", default="charts")
    args = parser.parse_args()

    output_dir = Path(args.out_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    df = load_metrics(Path(args.input))

    plot_total_duration(df, output_dir)
    plot_job_duration(df, output_dir)
    plot_success_failure(df, output_dir)
    plot_tests_vs_duration(df, output_dir)

    print(f"Graficos salvos em: {output_dir}")


if __name__ == "__main__":
    main()
