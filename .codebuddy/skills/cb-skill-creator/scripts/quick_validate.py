#!/usr/bin/env python3
"""
Skill 快速验证脚本 — 检查 Skill 文件的基本格式和必需组件。

用法:
    python cb-skill-creator/scripts/quick_validate.py skills/my-skill.md
    python cb-skill-creator/scripts/quick_validate.py skills/  # 验证整个目录
"""

import sys
import re
from pathlib import Path


def validate_skill_file(skill_path: Path) -> tuple[bool, list[str]]:
    """
    验证一个 Skill .md 文件。

    返回 (is_valid, messages) — messages 包含警告和错误。
    """
    messages: list[str] = []

    if not skill_path.exists():
        return False, [f"❌ 文件不存在: {skill_path}"]

    content = skill_path.read_text(encoding="utf-8")
    lines = content.split("\n")

    # 检查文件不能为空
    if not content.strip():
        return False, [f"❌ 文件为空: {skill_path}"]

    # 检查标题
    has_title = False
    for line in lines:
        if line.startswith("# "):
            has_title = True
            title = line[2:].strip()
            if len(title) > 100:
                messages.append(f"⚠️  标题过长 ({len(title)} 字符)，建议 < 100 字符")
            break

    if not has_title:
        # 检查是否有 YAML frontmatter 中的 name
        if content.startswith("---"):
            match = re.search(r"^name:\s*(.+)$", content, re.MULTILINE)
            if match:
                has_title = True
            else:
                messages.append("❌ 缺少标题（# 标题 或 frontmatter 中的 name 字段）")
                return False, messages
        else:
            messages.append("❌ 缺少标题（需要 # 标题）")
            return False, messages

    # 检查必需部分
    required_sections = {
        "触发条件": False,
        "使用方法": False,
    }

    recommended_sections = {
        "输入参数": False,
        "输出": False,
        "AI 分析提示": False,
    }

    for line in lines:
        line_stripped = line.strip()
        if line_stripped.startswith("## "):
            section_name = line_stripped[3:].strip()
            for key in required_sections:
                if key in section_name:
                    required_sections[key] = True
            for key in recommended_sections:
                if key in section_name:
                    recommended_sections[key] = True

    # 报告缺少的必需部分
    for section, found in required_sections.items():
        if not found:
            messages.append(f"❌ 缺少必需部分: ## {section}")

    # 报告缺少的推荐部分
    for section, found in recommended_sections.items():
        if not found:
            messages.append(f"⚠️  建议添加部分: ## {section}")

    # 检查触发条件是否有实质内容
    in_trigger = False
    trigger_content_lines = 0
    for line in lines:
        if re.match(r"^##\s+触发条件", line):
            in_trigger = True
            continue
        if in_trigger:
            if line.startswith("## "):
                break
            if line.strip() and not line.strip().startswith("#"):
                trigger_content_lines += 1

    if in_trigger and trigger_content_lines < 2:
        messages.append("⚠️  触发条件内容太少，建议至少列出 3-5 个关键词/场景")

    # 检查文件长度
    total_lines = len(lines)
    if total_lines > 500:
        messages.append(f"⚠️  文件较长 ({total_lines} 行)，建议拆分到 references/ 子目录")
    elif total_lines < 10:
        messages.append("⚠️  文件过短，可能缺少必要的指令内容")

    # 检查是否有代码示例
    has_code_block = "```" in content
    if not has_code_block:
        messages.append("⚠️  建议包含代码示例（使用方法、输出格式等）")

    # 判断是否通过
    has_errors = any(msg.startswith("❌") for msg in messages)
    is_valid = not has_errors

    if is_valid and not messages:
        messages.append("✅ Skill 验证通过！")
    elif is_valid:
        messages.insert(0, "✅ Skill 基本格式正确，但有一些建议：")

    return is_valid, messages


def validate_directory(dir_path: Path) -> tuple[int, int]:
    """验证目录下的所有 Skill 文件。返回 (passed, total)。"""
    skill_files = list(dir_path.rglob("*.md"))
    # 排除非 Skill 文件
    skill_files = [
        f for f in skill_files
        if f.name.upper() not in ("README.MD", "SKILLS_ARCHITECTURE.MD", "PROJECT_STRUCTURE.MD")
        and "workspace" not in str(f)
    ]

    if not skill_files:
        print(f"在 {dir_path} 中未找到 Skill 文件")
        return 0, 0

    passed = 0
    total = len(skill_files)

    for skill_file in sorted(skill_files):
        rel_path = skill_file.relative_to(dir_path)
        print(f"\n{'─' * 60}")
        print(f"📄 {rel_path}")
        print(f"{'─' * 60}")

        is_valid, messages = validate_skill_file(skill_file)
        for msg in messages:
            print(f"  {msg}")

        if is_valid:
            passed += 1

    print(f"\n{'═' * 60}")
    print(f"📊 验证结果: {passed}/{total} 通过")
    print(f"{'═' * 60}")

    return passed, total


def main():
    if len(sys.argv) < 2:
        print("用法:")
        print("  python quick_validate.py <skill-file.md>     # 验证单个文件")
        print("  python quick_validate.py <skills-directory>   # 验证整个目录")
        sys.exit(1)

    target = Path(sys.argv[1])

    if target.is_dir():
        passed, total = validate_directory(target)
        sys.exit(0 if passed == total else 1)
    elif target.is_file():
        is_valid, messages = validate_skill_file(target)
        for msg in messages:
            print(msg)
        sys.exit(0 if is_valid else 1)
    else:
        print(f"❌ 路径不存在: {target}")
        sys.exit(1)


if __name__ == "__main__":
    main()
