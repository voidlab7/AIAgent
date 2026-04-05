# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

AIAgent — 一个人的 AI 工作团队。An AI-powered personal workspace covering knowledge accumulation, content production, product incubation, and engineering efficiency. Python backend with a React sub-project (`web_site/pawmbti/`).

## Build & Run Commands

### Python Backend
```bash
pip install -r requirements.txt        # Install dependencies
cp .env.example .env                   # Configure API keys
python main.py init                    # Initialize DB and directories
python main.py status                  # Show module status and DB stats
python main.py funtest --demo          # Run fun-test analyzer with sample data
python main.py hotspot                 # Run hotspot monitor
python main.py trigger "分析趣味测试热点"  # Keyword-triggered analysis
```

### Testing & Linting
```bash
pytest tests/ -v                              # Run all tests
pytest tests/test_module.py::TestClass::test_method -v  # Single test
black .                                       # Format code
mypy . --ignore-missing-imports               # Type check
```

### Frontend (web_site/pawmbti/)
```bash
cd web_site/pawmbti && npm run dev      # Dev server
npm run build                           # Production build → dist/
npm run lint                            # Lint
```

## Architecture

### Four Core Modules

```
AIAgent/
├── knowledge/          # 🧠 AI Knowledge Base
│   ├── articles/       #   Article study notes (wechat-article-learner output)
│   ├── insights/       #   Industry analysis & deep research
│   └── playbooks/      #   Methodologies & experience handbooks
├── pipeline/           # 🏭 Content Creation Pipeline (7-stage)
│   ├── hotspot/        #   1. Hotspot monitoring (Xiaohongshu via RedNote MCP)
│   ├── topic/          #   2. Topic selection (fun-test analyzer + keyword trigger)
│   ├── material/       #   3. Material collection (not yet implemented)
│   ├── writer/         #   4. AI writing (not yet implemented)
│   ├── image/          #   5. Image matching (not yet implemented)
│   ├── formatter/      #   6. Formatting for platforms (not yet implemented)
│   └── publisher/      #   7. Publishing (Xiaohongshu via MCP)
├── products/           # 🚀 Product Incubation
│   └── ideas/          #   Product idea pool (design docs, brainstorms)
├── web_site/           # 🌐 Web Products (independent git repo)
│   └── pawmbti/        #   PawMBTI cat personality test (live at microlab.top)
├── common/             # 🔧 Shared Infrastructure
│   ├── config.py       #   Central config (paths, API keys, account profile)
│   └── database.py     #   SQLite wrapper (global singleton `db`)
└── docs/               # 📚 Project Docs
    ├── RELEASE.md      #   Release & deployment guide
    └── screenshots/    #   Project screenshots
```

### Shared Infrastructure
- **`common/config.py`** — Central config: paths, API keys (from env vars), account profile, content strategy, scheduling. All directories (`data/`, `reports/`, `cache/`) auto-created on import.
- **`common/database.py`** — SQLite wrapper with a global singleton `db`. Tables: `hotspots`, `topics`, `materials`, `articles`, `images`, `publish_records`. Use `db.execute()`, `db.fetchall()`, `db.fetchone()` — returns dicts via `sqlite3.Row`.
- **`main.py`** — CLI entry point with argparse. Commands map to module names (`hotspot`, `topic`, `funtest`, `trigger`, `status`, etc.).

### MCP Integrations
- **RedNote MCP** (`rednote-mcp` npm package) — Xiaohongshu data fetching: `search_feeds`, `get_feed_detail`, login via QR code
- **WeChat Publisher MCP** (`wechat-publisher-mcp` npm package) — WeChat publishing (planned)
- Xiaohongshu publishing uses MCP tools: `check_login_status`, `get_login_qrcode`, `publish_content`, `delete_cookies`

### web_site/ Sub-project
Independent git repo containing **MicroLab** — interactive personality tests:
- **PawMBTI**: Cat personality MBTI test (quick 8Q + deep 12Q)
- **Baby画像**: Baby behavior observation test
- Stack: React 18 + TypeScript + Vite + Tailwind CSS + Zustand + Framer Motion
- Backend: Node.js (`server/count-server.cjs`) for simple counting, JSON file storage
- Invite code system with localStorage caching
- Analytics/tracking built in

## Key Patterns

- **Module path setup**: Each module adds `PROJECT_ROOT` to `sys.path` to import from `common/`
- **Commit message format**: `<type>(<scope>): <subject>` — types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`
- **CI/CD**: Push `v*` tags triggers GitHub Actions → test → package tar.gz → create GitHub Release
- **Hotspot heat scoring**: `likes * 1 + favorites * 1.5 + comments * 2 + shares * 3`
- **Content length targets**: WeChat 1500-3000 chars, Xiaohongshu 300-800, Zhihu 1000-2500
- **Xiaohongshu publishing**: Title ≤ 20 Chinese chars; hashtags go in `tags` array, not in `content` body

## CodeBuddy Skills (`.codebuddy/skills/`)
The project uses CodeBuddy AI assistant with custom skills:
- `wechat-article-learner` — WeChat article knowledge extraction → saves to `knowledge/articles/`
- `trend-analyst` — Automated topic analysis: keyword expansion → Xiaohongshu MCP data → report generation
- `xiaohongshu-automation` — Xiaohongshu publishing workflow: login check → content prep → publish via MCP
- `pet-content-writer` — Pet-themed content creation
- `cb-skill-creator` — Skill creation and evaluation tool
