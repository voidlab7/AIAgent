"""cb-skill-creator 共享工具模块。"""

import re
import json
from pathlib import Path
from typing import Optional


def parse_skill_md(skill_path: Path) -> tuple[str, str, str]:
    """
    解析 Skill .md 文件，返回 (title, trigger_keywords, full_content)。

    支持两种格式：
    1. 带 YAML frontmatter 的（--- name/description ---）
    2. 项目标准格式（# 标题 + ## 触发条件）
    """
    if skill_path.is_dir():
        # 如果是目录，查找 README.md 或 SKILL.md
        for name in ["SKILL.md", "README.md"]:
            candidate = skill_path / name
            if candidate.exists():
                skill_path = candidate
                break
        else:
            raise ValueError(f"在目录 {skill_path} 中未找到 SKILL.md 或 README.md")

    content = skill_path.read_text(encoding="utf-8")
    lines = content.split("\n")

    # 尝试解析 YAML frontmatter
    if lines[0].strip() == "---":
        end_idx = None
        for i, line in enumerate(lines[1:], start=1):
            if line.strip() == "---":
                end_idx = i
                break

        if end_idx is not None:
            name = ""
            description = ""
            frontmatter_lines = lines[1:end_idx]
            i = 0
            while i < len(frontmatter_lines):
                line = frontmatter_lines[i]
                if line.startswith("name:"):
                    name = line[len("name:"):].strip().strip('"').strip("'")
                elif line.startswith("description:"):
                    value = line[len("description:"):].strip()
                    if value in (">", "|", ">-", "|-"):
                        continuation: list[str] = []
                        i += 1
                        while i < len(frontmatter_lines) and (
                            frontmatter_lines[i].startswith("  ")
                            or frontmatter_lines[i].startswith("\t")
                        ):
                            continuation.append(frontmatter_lines[i].strip())
                            i += 1
                        description = " ".join(continuation)
                        continue
                    else:
                        description = value.strip('"').strip("'")
                i += 1
            return name, description, content

    # 解析项目标准格式
    title = ""
    trigger_keywords = ""

    for line in lines:
        if line.startswith("# ") and not title:
            title = line[2:].strip()
            break

    # 提取触发条件
    in_trigger = False
    trigger_lines: list[str] = []
    for line in lines:
        if re.match(r"^##\s+触发条件", line):
            in_trigger = True
            continue
        if in_trigger:
            if line.startswith("## "):
                break
            if line.strip():
                trigger_lines.append(line.strip())

    trigger_keywords = " | ".join(trigger_lines) if trigger_lines else ""

    return title, trigger_keywords, content


def load_evals(evals_path: Path) -> dict:
    """加载 evals.json 文件。"""
    if not evals_path.exists():
        return {"skill_name": "", "evals": []}
    return json.loads(evals_path.read_text(encoding="utf-8"))


def save_json(data: dict | list, path: Path, indent: int = 2) -> None:
    """保存 JSON 数据到文件。"""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(data, ensure_ascii=False, indent=indent),
        encoding="utf-8",
    )


def find_skill_files(skills_dir: Path) -> list[Path]:
    """查找 skills/ 目录下的所有 Skill 文件。"""
    skill_files = []
    for path in skills_dir.rglob("*.md"):
        # 排除 README 和非 Skill 文件
        if path.name.upper() in ("README.MD",):
            continue
        skill_files.append(path)
    return sorted(skill_files)


def format_duration(seconds: float) -> str:
    """格式化秒数为人类可读的时间字符串。"""
    if seconds < 60:
        return f"{seconds:.1f}s"
    minutes = int(seconds // 60)
    secs = seconds % 60
    if minutes < 60:
        return f"{minutes}m {secs:.0f}s"
    hours = int(minutes // 60)
    mins = minutes % 60
    return f"{hours}h {mins}m"
