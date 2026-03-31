#!/usr/bin/env python3
"""
Skill 触发评估脚本 — 测试 Skill 的触发条件是否能正确匹配用户查询。

用法:
    python cb-skill-creator/scripts/run_trigger_eval.py \
        --eval-set trigger_eval.json \
        --skill-path skills/extension-analyze.md \
        --max-iterations 5

这个脚本通过关键词匹配来评估 Skill 触发条件的覆盖范围，
不依赖外部 CLI 工具，完全在本地运行。
"""

import sys
import json
import re
import argparse
from pathlib import Path
from datetime import datetime, timezone

# 添加父目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))
from scripts.utils import parse_skill_md


def extract_trigger_keywords(skill_content: str) -> list[str]:
    """从 Skill 内容中提取触发关键词。"""
    keywords = []
    lines = skill_content.split("\n")

    in_trigger = False
    for line in lines:
        if re.match(r"^##\s+触发条件", line):
            in_trigger = True
            continue
        if in_trigger:
            if line.startswith("## "):
                break
            # 提取 ` 包裹的关键词
            backtick_matches = re.findall(r"`([^`]+)`", line)
            keywords.extend(backtick_matches)
            # 提取 - 开头的列表项中的文本
            list_match = re.match(r"^[-*]\s+(.+)", line.strip())
            if list_match:
                text = list_match.group(1)
                # 去掉 markdown 格式
                clean = re.sub(r"[`*_]", "", text)
                # 按 / 分割
                parts = [p.strip() for p in clean.split("/")]
                for part in parts:
                    if part and len(part) > 1:
                        keywords.append(part)

    # 去重并转小写
    seen = set()
    unique = []
    for kw in keywords:
        kw_lower = kw.lower().strip()
        if kw_lower and kw_lower not in seen:
            seen.add(kw_lower)
            unique.append(kw_lower)

    return unique


def check_trigger(query: str, keywords: list[str], description: str = "") -> tuple[bool, list[str]]:
    """
    检查查询是否应该触发 Skill。

    返回 (triggered, matched_keywords)。
    """
    query_lower = query.lower()
    matched = []

    for kw in keywords:
        if kw in query_lower:
            matched.append(kw)

    # 也检查 description 中的关键信息
    if description:
        desc_words = re.findall(r"[\u4e00-\u9fff]+|[a-zA-Z]+", description.lower())
        for word in desc_words:
            if len(word) >= 3 and word in query_lower and word not in matched:
                matched.append(word)

    return len(matched) > 0, matched


def run_evaluation(
    eval_set: list[dict],
    keywords: list[str],
    description: str = "",
) -> dict:
    """
    运行一轮触发评估。

    返回评估结果字典。
    """
    results = {
        "true_positives": [],   # 应触发且触发了
        "true_negatives": [],   # 不应触发且没触发
        "false_positives": [],  # 不应触发但触发了
        "false_negatives": [],  # 应触发但没触发
    }

    for item in eval_set:
        query = item["query"]
        should_trigger = item["should_trigger"]
        triggered, matched = check_trigger(query, keywords, description)

        result = {
            "query": query,
            "should_trigger": should_trigger,
            "triggered": triggered,
            "matched_keywords": matched,
        }

        if should_trigger and triggered:
            results["true_positives"].append(result)
        elif not should_trigger and not triggered:
            results["true_negatives"].append(result)
        elif not should_trigger and triggered:
            results["false_positives"].append(result)
        elif should_trigger and not triggered:
            results["false_negatives"].append(result)

    # 计算指标
    tp = len(results["true_positives"])
    tn = len(results["true_negatives"])
    fp = len(results["false_positives"])
    fn = len(results["false_negatives"])
    total = tp + tn + fp + fn

    precision = tp / (tp + fp) if (tp + fp) > 0 else 0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0
    accuracy = (tp + tn) / total if total > 0 else 0
    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0

    results["metrics"] = {
        "precision": round(precision, 4),
        "recall": round(recall, 4),
        "accuracy": round(accuracy, 4),
        "f1_score": round(f1, 4),
        "true_positives": tp,
        "true_negatives": tn,
        "false_positives": fp,
        "false_negatives": fn,
        "total": total,
    }

    return results


def suggest_improvements(results: dict, keywords: list[str]) -> list[str]:
    """基于评估结果建议改进。"""
    suggestions = []

    # 分析 false negatives（应触发但没触发）
    fn = results.get("false_negatives", [])
    if fn:
        suggestions.append(f"🔴 有 {len(fn)} 个应触发但未触发的查询：")
        for item in fn:
            suggestions.append(f"   - \"{item['query'][:80]}...\"")
            # 建议可能需要添加的关键词
            query_words = re.findall(r"[\u4e00-\u9fff]+|[a-zA-Z]{3,}", item["query"].lower())
            new_words = [w for w in query_words if w not in keywords and len(w) >= 2]
            if new_words:
                suggestions.append(f"     → 建议添加关键词: {', '.join(new_words[:5])}")

    # 分析 false positives（不应触发但触发了）
    fp = results.get("false_positives", [])
    if fp:
        suggestions.append(f"🟡 有 {len(fp)} 个不应触发但触发了的查询：")
        for item in fp:
            suggestions.append(f"   - \"{item['query'][:80]}...\"")
            suggestions.append(f"     → 匹配了: {', '.join(item['matched_keywords'])}")

    return suggestions


def print_results(results: dict, iteration: int = 0) -> None:
    """打印评估结果。"""
    metrics = results["metrics"]

    print(f"\n{'═' * 60}")
    print(f"📊 触发评估结果 (迭代 {iteration})")
    print(f"{'═' * 60}")
    print(f"  准确率 (Accuracy):  {metrics['accuracy']:.1%}")
    print(f"  精确率 (Precision): {metrics['precision']:.1%}")
    print(f"  召回率 (Recall):    {metrics['recall']:.1%}")
    print(f"  F1 分数:            {metrics['f1_score']:.4f}")
    print(f"  TP: {metrics['true_positives']}  TN: {metrics['true_negatives']}  "
          f"FP: {metrics['false_positives']}  FN: {metrics['false_negatives']}")
    print(f"{'─' * 60}")


def main():
    parser = argparse.ArgumentParser(description="Skill 触发评估")
    parser.add_argument("--eval-set", required=True, help="触发评估集 JSON 文件路径")
    parser.add_argument("--skill-path", required=True, help="Skill 文件路径")
    parser.add_argument("--max-iterations", type=int, default=1, help="最大迭代次数")
    parser.add_argument("--output", help="输出结果文件路径")
    parser.add_argument("--verbose", action="store_true", help="详细输出")
    args = parser.parse_args()

    # 加载评估集
    eval_set_path = Path(args.eval_set)
    if not eval_set_path.exists():
        print(f"❌ 评估集文件不存在: {eval_set_path}")
        sys.exit(1)

    eval_set = json.loads(eval_set_path.read_text(encoding="utf-8"))

    # 解析 Skill
    skill_path = Path(args.skill_path)
    if not skill_path.exists():
        print(f"❌ Skill 文件不存在: {skill_path}")
        sys.exit(1)

    title, description, content = parse_skill_md(skill_path)
    keywords = extract_trigger_keywords(content)

    print(f"📄 Skill: {title or skill_path.name}")
    print(f"🔑 提取到 {len(keywords)} 个触发关键词")
    if args.verbose:
        print(f"   关键词: {', '.join(keywords[:20])}")
    print(f"📋 评估集: {len(eval_set)} 个查询")

    # 运行评估
    results = run_evaluation(eval_set, keywords, description)
    print_results(results, iteration=0)

    # 建议改进
    suggestions = suggest_improvements(results, keywords)
    if suggestions:
        print("\n💡 改进建议:")
        for s in suggestions:
            print(f"  {s}")

    # 保存结果
    output_path = Path(args.output) if args.output else skill_path.parent / f"{skill_path.stem}_trigger_eval.json"
    output_data = {
        "skill_name": title or skill_path.stem,
        "skill_path": str(skill_path),
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "keywords_count": len(keywords),
        "keywords": keywords,
        "eval_set_size": len(eval_set),
        "metrics": results["metrics"],
        "false_negatives": results.get("false_negatives", []),
        "false_positives": results.get("false_positives", []),
        "suggestions": suggestions,
    }

    output_path.write_text(
        json.dumps(output_data, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(f"\n✅ 结果已保存到 {output_path}")


if __name__ == "__main__":
    main()
