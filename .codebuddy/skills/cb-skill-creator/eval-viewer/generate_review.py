#!/usr/bin/env python3
"""
评估审查页面生成器 — 从运行目录生成可视化审查 HTML 页面。

用法:
    # 启动本地服务器（默认方式）
    python cb-skill-creator/eval-viewer/generate_review.py \
        workspace/iteration-1 \
        --skill-name "my-skill" \
        --benchmark workspace/iteration-1/benchmark.json

    # 生成静态 HTML 文件
    python cb-skill-creator/eval-viewer/generate_review.py \
        workspace/iteration-1 \
        --skill-name "my-skill" \
        --static output/review.html

    # 包含上一迭代的对比
    python cb-skill-creator/eval-viewer/generate_review.py \
        workspace/iteration-2 \
        --skill-name "my-skill" \
        --previous-workspace workspace/iteration-1
"""

import sys
import json
import argparse
import http.server
import webbrowser
import threading
import os
from pathlib import Path
from datetime import datetime, timezone
from urllib.parse import parse_qs


def discover_eval_dirs(workspace: Path) -> list[dict]:
    """发现工作区中的评估目录并收集数据。"""
    evals = []

    for eval_dir in sorted(workspace.iterdir()):
        if not eval_dir.is_dir() or eval_dir.name.startswith("."):
            continue

        # 读取元数据
        metadata_path = eval_dir / "eval_metadata.json"
        if not metadata_path.exists():
            continue

        try:
            metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            continue

        eval_data = {
            "eval_id": metadata.get("eval_id", eval_dir.name),
            "eval_name": metadata.get("eval_name", eval_dir.name),
            "prompt": metadata.get("prompt", ""),
            "runs": {},
        }

        # 收集每个配置的运行数据
        for config_dir in sorted(eval_dir.iterdir()):
            if not config_dir.is_dir():
                continue

            config_name = config_dir.name
            run_data = {"outputs": [], "grading": None}

            # 收集输出文件
            outputs_dir = config_dir / "outputs"
            if outputs_dir.exists():
                for f in sorted(outputs_dir.iterdir()):
                    if f.is_file():
                        try:
                            content = f.read_text(encoding="utf-8")
                            run_data["outputs"].append({
                                "name": f.name,
                                "content": content[:50000],  # 限制大小
                                "size": f.stat().st_size,
                            })
                        except (UnicodeDecodeError, OSError):
                            run_data["outputs"].append({
                                "name": f.name,
                                "content": f"[二进制文件, {f.stat().st_size} bytes]",
                                "size": f.stat().st_size,
                            })

            # 读取评分
            grading_path = config_dir / "grading.json"
            if grading_path.exists():
                try:
                    run_data["grading"] = json.loads(grading_path.read_text(encoding="utf-8"))
                except (json.JSONDecodeError, OSError):
                    pass

            eval_data["runs"][config_name] = run_data

        if eval_data["runs"]:
            evals.append(eval_data)

    return evals


def load_previous_data(prev_workspace: Path) -> list[dict]:
    """加载上一迭代的数据用于对比。"""
    if not prev_workspace or not prev_workspace.exists():
        return []

    prev_evals = discover_eval_dirs(prev_workspace)

    # 也加载上一轮的反馈
    feedback_path = prev_workspace / "feedback.json"
    if feedback_path.exists():
        try:
            feedback = json.loads(feedback_path.read_text(encoding="utf-8"))
            reviews = {r["run_id"]: r["feedback"] for r in feedback.get("reviews", [])}
            for eval_data in prev_evals:
                eval_data["previous_feedback"] = reviews
        except (json.JSONDecodeError, OSError):
            pass

    return prev_evals


def generate_html(
    evals: list[dict],
    skill_name: str,
    benchmark: dict | None = None,
    previous_evals: list[dict] | None = None,
    is_static: bool = False,
) -> str:
    """生成审查 HTML 页面。"""
    viewer_template = Path(__file__).parent / "viewer.html"
    if viewer_template.exists():
        html = viewer_template.read_text(encoding="utf-8")
        # 替换占位符
        embedded = {
            "evals": evals,
            "skill_name": skill_name,
            "benchmark": benchmark,
            "previous_evals": previous_evals or [],
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "is_static": is_static,
        }
        html = html.replace("/*__EMBEDDED_DATA__*/", json.dumps(embedded, ensure_ascii=False))
        return html

    # 如果模板不存在，生成简单版本
    embedded_data = json.dumps({
        "evals": evals,
        "skill_name": skill_name,
        "benchmark": benchmark,
        "previous_evals": previous_evals or [],
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "is_static": is_static,
    }, ensure_ascii=False)

    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{skill_name} - 评估审查</title>
<style>
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: #f5f5f5; color: #333; }}
.header {{ background: #1a73e8; color: #fff; padding: 1.5rem 2rem; }}
.header h1 {{ font-size: 1.5rem; }}
.tabs {{ display: flex; background: #fff; border-bottom: 2px solid #eee; padding: 0 2rem; }}
.tab {{ padding: 0.8rem 1.5rem; cursor: pointer; border-bottom: 3px solid transparent; font-weight: 500; color: #666; }}
.tab.active {{ color: #1a73e8; border-bottom-color: #1a73e8; }}
.content {{ padding: 2rem; max-width: 1200px; margin: 0 auto; }}
.eval-card {{ background: #fff; border-radius: 8px; padding: 1.5rem; margin-bottom: 1.5rem; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }}
.eval-card h3 {{ color: #1a73e8; margin-bottom: 0.5rem; }}
.prompt {{ background: #f8f9fa; padding: 1rem; border-radius: 4px; margin-bottom: 1rem; border-left: 3px solid #4285f4; font-size: 0.9rem; }}
.output-section {{ margin: 1rem 0; }}
.output-content {{ background: #1e1e1e; color: #d4d4d4; padding: 1rem; border-radius: 4px; overflow: auto; max-height: 400px; font-family: 'Fira Code', monospace; font-size: 0.85rem; white-space: pre-wrap; }}
.grading {{ margin: 1rem 0; }}
.grading-item {{ padding: 0.4rem 0; display: flex; gap: 0.5rem; align-items: flex-start; }}
.pass {{ color: #34a853; }} .fail {{ color: #ea4335; }}
.feedback-box {{ width: 100%; min-height: 80px; border: 1px solid #ddd; border-radius: 4px; padding: 0.8rem; font-family: inherit; resize: vertical; }}
.feedback-box:focus {{ border-color: #4285f4; outline: none; }}
.nav {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.5rem; }}
.nav-btn {{ padding: 0.5rem 1rem; border: 1px solid #ddd; background: #fff; border-radius: 4px; cursor: pointer; }}
.nav-btn:hover {{ background: #f1f1f1; }}
.submit-btn {{ padding: 0.6rem 2rem; background: #34a853; color: #fff; border: none; border-radius: 4px; cursor: pointer; font-size: 1rem; }}
.submit-btn:hover {{ background: #2d8e47; }}
.benchmark {{ margin-top: 1rem; }}
.benchmark table {{ width: 100%; border-collapse: collapse; }}
.benchmark th, .benchmark td {{ padding: 0.6rem 1rem; text-align: left; border-bottom: 1px solid #eee; }}
.benchmark th {{ background: #f8f9fa; font-weight: 500; }}
.collapsible {{ cursor: pointer; user-select: none; padding: 0.5rem 0; color: #1a73e8; }}
.collapsible::before {{ content: '▶ '; font-size: 0.8rem; }}
.collapsible.open::before {{ content: '▼ '; }}
.collapse-content {{ display: none; padding: 0.5rem 0 0.5rem 1rem; }}
.collapse-content.show {{ display: block; }}
#outputs-view, #benchmark-view {{ display: none; }}
#outputs-view.active, #benchmark-view.active {{ display: block; }}
</style>
</head>
<body>
<div class="header">
    <h1>📊 {skill_name} — 评估审查</h1>
</div>
<div class="tabs">
    <div class="tab active" onclick="switchTab('outputs')">📄 Outputs</div>
    <div class="tab" onclick="switchTab('benchmark')">📊 Benchmark</div>
</div>
<div class="content">
    <div id="outputs-view" class="active"></div>
    <div id="benchmark-view"></div>
</div>

<script>
const DATA = {embedded_data};
let currentEvalIdx = 0;
const feedbacks = {{}};

function switchTab(tab) {{
    document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
    document.getElementById('outputs-view').classList.remove('active');
    document.getElementById('benchmark-view').classList.remove('active');
    if (tab === 'outputs') {{
        document.querySelectorAll('.tab')[0].classList.add('active');
        document.getElementById('outputs-view').classList.add('active');
    }} else {{
        document.querySelectorAll('.tab')[1].classList.add('active');
        document.getElementById('benchmark-view').classList.add('active');
    }}
}}

function renderOutputs() {{
    const container = document.getElementById('outputs-view');
    const evals = DATA.evals;
    if (!evals.length) {{ container.innerHTML = '<p>没有评估结果</p>'; return; }}

    const eval_ = evals[currentEvalIdx];
    let html = `
        <div class="nav">
            <button class="nav-btn" onclick="navigate(-1)" ${{currentEvalIdx === 0 ? 'disabled' : ''}}>← 上一个</button>
            <span>${{currentEvalIdx + 1}} / ${{evals.length}} — ${{eval_.eval_name}}</span>
            <button class="nav-btn" onclick="navigate(1)" ${{currentEvalIdx === evals.length - 1 ? 'disabled' : ''}}>下一个 →</button>
        </div>
        <div class="eval-card">
            <h3>Prompt</h3>
            <div class="prompt">${{escapeHtml(eval_.prompt)}}</div>
    `;

    for (const [config, run] of Object.entries(eval_.runs)) {{
        html += `<div class="output-section"><h4>📁 ${{config}}</h4>`;
        for (const output of (run.outputs || [])) {{
            html += `<p><strong>${{output.name}}</strong> (${{formatSize(output.size)}})</p>
                <div class="output-content">${{escapeHtml(output.content)}}</div>`;
        }}

        if (run.grading) {{
            html += `<div class="collapsible" onclick="toggleCollapse(this)">评分结果 (${{run.grading.summary?.pass_rate ? (run.grading.summary.pass_rate * 100).toFixed(0) + '%' : 'N/A'}} 通过)</div>
                <div class="collapse-content"><div class="grading">`;
            for (const exp of (run.grading.expectations || [])) {{
                const cls = exp.passed ? 'pass' : 'fail';
                const icon = exp.passed ? '✅' : '❌';
                html += `<div class="grading-item"><span class="${{cls}}">${{icon}}</span> ${{escapeHtml(exp.text)}}</div>`;
            }}
            html += `</div></div>`;
        }}
        html += `</div>`;
    }}

    // Previous output
    const prevEvals = DATA.previous_evals || [];
    const prevEval = prevEvals.find(e => e.eval_id === eval_.eval_id || e.eval_name === eval_.eval_name);
    if (prevEval) {{
        html += `<div class="collapsible" onclick="toggleCollapse(this)">上一迭代输出</div><div class="collapse-content">`;
        for (const [config, run] of Object.entries(prevEval.runs)) {{
            for (const output of (run.outputs || [])) {{
                html += `<div class="output-content" style="max-height:200px">${{escapeHtml(output.content)}}</div>`;
            }}
        }}
        if (prevEval.previous_feedback) {{
            const fb = Object.values(prevEval.previous_feedback).find(f => f);
            if (fb) html += `<p><strong>上轮反馈:</strong> ${{escapeHtml(fb)}}</p>`;
        }}
        html += `</div>`;
    }}

    const runId = `eval-${{eval_.eval_id}}-with_skill`;
    html += `<h4 style="margin-top:1rem">💬 反馈</h4>
        <textarea class="feedback-box" data-run-id="${{runId}}"
            oninput="saveFeedback('${{runId}}', this.value)"
            placeholder="输入你的反馈...">${{feedbacks[runId] || ''}}</textarea>
    </div>`;

    // Submit button on last page
    if (currentEvalIdx === evals.length - 1) {{
        html += `<div style="text-align:center;margin-top:1.5rem">
            <button class="submit-btn" onclick="submitReviews()">📤 提交所有反馈</button>
        </div>`;
    }}

    container.innerHTML = html;
}}

function renderBenchmark() {{
    const container = document.getElementById('benchmark-view');
    const bm = DATA.benchmark;
    if (!bm) {{ container.innerHTML = '<p>没有基准测试数据</p>'; return; }}

    let html = `<div class="benchmark"><h3>📊 基准测试摘要</h3><table><tr><th>配置</th><th>通过率</th><th>时间</th></tr>`;
    const summary = bm.run_summary || {{}};
    for (const [config, stats] of Object.entries(summary)) {{
        if (config === 'delta') continue;
        const pr = stats.pass_rate || {{}};
        const ts = stats.time_seconds || {{}};
        html += `<tr><td>${{config}}</td><td>${{(pr.mean * 100).toFixed(1)}}% ± ${{(pr.stddev * 100).toFixed(1)}}%</td><td>${{ts.mean?.toFixed(1) || 'N/A'}}s</td></tr>`;
    }}
    html += `</table>`;

    if (bm.notes?.length) {{
        html += `<h4 style="margin-top:1.5rem">📝 分析备注</h4><ul>`;
        for (const note of bm.notes) html += `<li>${{escapeHtml(note)}}</li>`;
        html += `</ul>`;
    }}
    html += `</div>`;
    container.innerHTML = html;
}}

function navigate(delta) {{
    currentEvalIdx = Math.max(0, Math.min(DATA.evals.length - 1, currentEvalIdx + delta));
    renderOutputs();
}}

function saveFeedback(runId, value) {{ feedbacks[runId] = value; }}

function toggleCollapse(el) {{
    el.classList.toggle('open');
    const content = el.nextElementSibling;
    content.classList.toggle('show');
}}

function submitReviews() {{
    const reviews = Object.entries(feedbacks).map(([runId, feedback]) => ({{
        run_id: runId,
        feedback: feedback,
        timestamp: new Date().toISOString(),
    }}));
    const data = {{ reviews, status: 'complete' }};
    const blob = new Blob([JSON.stringify(data, null, 2)], {{ type: 'application/json' }});

    if (DATA.is_static) {{
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url; a.download = 'feedback.json'; a.click();
        URL.revokeObjectURL(url);
        alert('反馈已下载为 feedback.json');
    }} else {{
        fetch('/save-feedback', {{
            method: 'POST',
            headers: {{ 'Content-Type': 'application/json' }},
            body: JSON.stringify(data),
        }}).then(r => r.ok ? alert('反馈已保存！') : alert('保存失败'));
    }}
}}

function escapeHtml(str) {{
    if (!str) return '';
    return str.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
}}

function formatSize(bytes) {{
    if (bytes < 1024) return bytes + 'B';
    if (bytes < 1024*1024) return (bytes/1024).toFixed(1) + 'KB';
    return (bytes/1024/1024).toFixed(1) + 'MB';
}}

document.addEventListener('keydown', e => {{
    if (e.key === 'ArrowLeft') navigate(-1);
    if (e.key === 'ArrowRight') navigate(1);
}});

renderOutputs();
renderBenchmark();
</script>
</body>
</html>"""


class ReviewHandler(http.server.BaseHTTPRequestHandler):
    """HTTP 请求处理器。"""

    html_content = ""
    workspace_path = None

    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(self.html_content.encode("utf-8"))

    def do_POST(self):
        if self.path == "/save-feedback":
            content_length = int(self.headers["Content-Length"])
            body = self.rfile.read(content_length).decode("utf-8")

            if self.workspace_path:
                feedback_path = self.workspace_path / "feedback.json"
                feedback_path.write_text(body, encoding="utf-8")

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(b'{"status": "saved"}')
        else:
            self.send_response(404)
            self.end_headers()

    def log_message(self, format, *args):
        pass  # 静默日志


def main():
    parser = argparse.ArgumentParser(description="评估审查页面生成器")
    parser.add_argument("workspace", help="迭代工作区目录")
    parser.add_argument("--skill-name", default="skill", help="Skill 名称")
    parser.add_argument("--benchmark", help="benchmark.json 路径")
    parser.add_argument("--previous-workspace", help="上一迭代工作区（用于对比）")
    parser.add_argument("--static", help="生成静态 HTML 文件（而非启动服务器）")
    parser.add_argument("--port", type=int, default=8765, help="服务器端口")
    args = parser.parse_args()

    workspace = Path(args.workspace)
    if not workspace.exists():
        print(f"❌ 工作区不存在: {workspace}")
        sys.exit(1)

    # 收集数据
    print(f"📂 扫描工作区: {workspace}")
    evals = discover_eval_dirs(workspace)
    print(f"  找到 {len(evals)} 个评估")

    # 加载基准测试
    benchmark = None
    if args.benchmark:
        bm_path = Path(args.benchmark)
        if bm_path.exists():
            benchmark = json.loads(bm_path.read_text(encoding="utf-8"))
            print(f"  📊 加载了基准测试数据")

    # 加载上一迭代
    previous_evals = None
    if args.previous_workspace:
        prev_path = Path(args.previous_workspace)
        previous_evals = load_previous_data(prev_path)
        print(f"  📁 加载了 {len(previous_evals)} 个上轮评估")

    # 生成 HTML
    is_static = args.static is not None
    html = generate_html(evals, args.skill_name, benchmark, previous_evals, is_static)

    if args.static:
        output_path = Path(args.static)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(html, encoding="utf-8")
        print(f"✅ 静态 HTML 已保存到: {output_path}")
        return

    # 启动服务器
    ReviewHandler.html_content = html
    ReviewHandler.workspace_path = workspace

    server = http.server.HTTPServer(("127.0.0.1", args.port), ReviewHandler)
    url = f"http://127.0.0.1:{args.port}"

    print(f"🌐 审查服务器启动: {url}")
    print("   按 Ctrl+C 停止")

    # 在浏览器中打开
    threading.Timer(0.5, lambda: webbrowser.open(url)).start()

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 服务器已停止")
        server.shutdown()


if __name__ == "__main__":
    main()
