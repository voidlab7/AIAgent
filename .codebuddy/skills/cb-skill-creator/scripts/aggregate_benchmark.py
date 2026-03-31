#!/usr/bin/env python3
"""
基准测试聚合脚本 — 从运行目录收集 grading.json 结果，计算统计数据。

用法:
    python cb-skill-creator/scripts/aggregate_benchmark.py \
        <workspace>/iteration-N --skill-name my-skill

生成:
    <workspace>/iteration-N/benchmark.json
    <workspace>/iteration-N/benchmark.md
"""

import sys
import json
import math
import argparse
from pathlib import Path
from datetime import datetime, timezone


def load_grading(grading_path: Path) -> dict | None:
    """加载 grading.json 文件。"""
    if not grading_path.exists():
        return None
    try:
        return json.loads(grading_path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as e:
        print(f"  ⚠️  无法读取 {grading_path}: {e}")
        return None


def load_timing(timing_path: Path) -> dict | None:
    """加载 timing.json 文件。"""
    if not timing_path.exists():
        return None
    try:
        return json.loads(timing_path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return None


def compute_stats(values: list[float]) -> dict:
    """计算均值、标准差、最小值、最大值。"""
    if not values:
        return {"mean": 0, "stddev": 0, "min": 0, "max": 0}

    n = len(values)
    mean = sum(values) / n

    if n > 1:
        variance = sum((x - mean) ** 2 for x in values) / (n - 1)
        stddev = math.sqrt(variance)
    else:
        stddev = 0

    return {
        "mean": round(mean, 4),
        "stddev": round(stddev, 4),
        "min": round(min(values), 4),
        "max": round(max(values), 4),
    }


def discover_runs(iteration_dir: Path) -> list[dict]:
    """发现迭代目录中的所有运行结果。"""
    runs = []

    for eval_dir in sorted(iteration_dir.iterdir()):
        if not eval_dir.is_dir() or eval_dir.name.startswith("."):
            continue

        # 读取 eval_metadata.json
        metadata_path = eval_dir / "eval_metadata.json"
        eval_metadata = {}
        if metadata_path.exists():
            try:
                eval_metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
            except (json.JSONDecodeError, OSError):
                pass

        eval_id = eval_metadata.get("eval_id", eval_dir.name)
        eval_name = eval_metadata.get("eval_name", eval_dir.name)

        # 检查每个配置
        for config_dir in sorted(eval_dir.iterdir()):
            if not config_dir.is_dir():
                continue

            config_name = config_dir.name  # with_skill, without_skill, old_skill
            grading = load_grading(config_dir / "grading.json")
            timing = load_timing(config_dir / "timing.json")

            if grading is None:
                continue

            summary = grading.get("summary", {})
            run = {
                "eval_id": eval_id,
                "eval_name": eval_name,
                "configuration": config_name,
                "run_number": 1,
                "result": {
                    "pass_rate": summary.get("pass_rate", 0),
                    "passed": summary.get("passed", 0),
                    "failed": summary.get("failed", 0),
                    "total": summary.get("total", 0),
                    "time_seconds": timing.get("total_duration_seconds", 0) if timing else 0,
                    "errors": grading.get("execution_metrics", {}).get("errors_encountered", 0),
                },
                "expectations": grading.get("expectations", []),
            }
            runs.append(run)

    return runs


def aggregate(runs: list[dict]) -> dict:
    """聚合运行结果为 run_summary。"""
    by_config: dict[str, list[dict]] = {}
    for run in runs:
        config = run["configuration"]
        by_config.setdefault(config, []).append(run)

    summary = {}
    for config, config_runs in by_config.items():
        pass_rates = [r["result"]["pass_rate"] for r in config_runs]
        times = [r["result"]["time_seconds"] for r in config_runs if r["result"]["time_seconds"] > 0]

        summary[config] = {
            "pass_rate": compute_stats(pass_rates),
            "time_seconds": compute_stats(times) if times else compute_stats([0]),
        }

    # 计算 delta
    delta = {}
    if "with_skill" in summary and "without_skill" in summary:
        ws = summary["with_skill"]
        wos = summary["without_skill"]
        pr_delta = ws["pass_rate"]["mean"] - wos["pass_rate"]["mean"]
        time_delta = ws["time_seconds"]["mean"] - wos["time_seconds"]["mean"]
        delta = {
            "pass_rate": f"{pr_delta:+.4f}",
            "time_seconds": f"{time_delta:+.1f}",
        }

    return {"summary": summary, "delta": delta}


def generate_markdown(benchmark: dict) -> str:
    """生成 benchmark.md 报告。"""
    lines = ["# 基准测试报告", ""]

    metadata = benchmark.get("metadata", {})
    lines.append(f"- **Skill**: {metadata.get('skill_name', 'unknown')}")
    lines.append(f"- **时间**: {metadata.get('timestamp', 'unknown')}")
    lines.append(f"- **评估数量**: {len(metadata.get('evals_run', []))}")
    lines.append("")

    # 摘要表格
    run_summary = benchmark.get("run_summary", {})
    if run_summary:
        lines.append("## 配置对比")
        lines.append("")
        lines.append("| 配置 | 通过率 (均值±标准差) | 时间 (均值±标准差) |")
        lines.append("|------|---------------------|-------------------|")

        for config, stats in run_summary.items():
            if config == "delta":
                continue
            pr = stats.get("pass_rate", {})
            ts = stats.get("time_seconds", {})
            pr_str = f"{pr.get('mean', 0):.1%} ± {pr.get('stddev', 0):.1%}"
            ts_str = f"{ts.get('mean', 0):.1f}s ± {ts.get('stddev', 0):.1f}s"
            lines.append(f"| {config} | {pr_str} | {ts_str} |")

        delta = run_summary.get("delta", benchmark.get("run_summary", {}).get("delta", {}))
        if delta:
            lines.append("")
            lines.append(f"**Delta**: 通过率 {delta.get('pass_rate', 'N/A')}, "
                         f"时间 {delta.get('time_seconds', 'N/A')}s")

    # 逐个运行结果
    runs = benchmark.get("runs", [])
    if runs:
        lines.append("")
        lines.append("## 详细结果")
        lines.append("")

        for run in runs:
            result = run.get("result", {})
            lines.append(f"### {run.get('eval_name', 'unknown')} ({run.get('configuration', '')})")
            lines.append(f"- 通过率: {result.get('pass_rate', 0):.1%}")
            lines.append(f"- 通过: {result.get('passed', 0)}/{result.get('total', 0)}")
            if result.get("time_seconds"):
                lines.append(f"- 时间: {result['time_seconds']:.1f}s")

            expectations = run.get("expectations", [])
            if expectations:
                lines.append("")
                for exp in expectations:
                    status = "✅" if exp.get("passed") else "❌"
                    lines.append(f"  {status} {exp.get('text', '')}")
            lines.append("")

    # 分析备注
    notes = benchmark.get("notes", [])
    if notes:
        lines.append("## 分析备注")
        lines.append("")
        for note in notes:
            lines.append(f"- {note}")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="聚合基准测试结果")
    parser.add_argument("iteration_dir", help="迭代目录路径")
    parser.add_argument("--skill-name", required=True, help="Skill 名称")
    args = parser.parse_args()

    iteration_dir = Path(args.iteration_dir)
    if not iteration_dir.exists():
        print(f"❌ 目录不存在: {iteration_dir}")
        sys.exit(1)

    print(f"📊 正在聚合 {iteration_dir} 的基准测试结果...")

    # 发现所有运行
    runs = discover_runs(iteration_dir)
    if not runs:
        print("⚠️  未发现任何运行结果")
        sys.exit(1)

    print(f"  找到 {len(runs)} 个运行结果")

    # 聚合
    agg = aggregate(runs)

    # 构建 benchmark.json
    eval_ids = list(set(r["eval_id"] for r in runs))
    benchmark = {
        "metadata": {
            "skill_name": args.skill_name,
            "skill_path": "",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "evals_run": eval_ids,
            "runs_per_configuration": 1,
        },
        "runs": runs,
        "run_summary": {**agg["summary"], "delta": agg["delta"]},
        "notes": [],
    }

    # 保存
    benchmark_json_path = iteration_dir / "benchmark.json"
    benchmark_json_path.write_text(
        json.dumps(benchmark, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(f"  ✅ 已保存 {benchmark_json_path}")

    benchmark_md_path = iteration_dir / "benchmark.md"
    benchmark_md_path.write_text(generate_markdown(benchmark), encoding="utf-8")
    print(f"  ✅ 已保存 {benchmark_md_path}")


if __name__ == "__main__":
    main()
