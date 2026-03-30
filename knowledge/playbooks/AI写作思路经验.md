
---

# AI 分工协作经验：产品 Agent / 设计 Agent / 开发 Agent + Skill 体系

> 日期：2026-03-18
> 背景：本工程有两条产品线同时运作——自媒体自动化流水线（热点→选题→写稿→发布）和互动小网站/小程序（趣味测试类产品），需要一套 AI 分工方案来提效。

## 一、核心原则：先做 Skill，再做 Agent

- **Skill 是原子能力**：单个明确的任务，开发快、复用性强，是 Agent 的"积木块"
- **Agent 是编排者**：把多个 Skill 串联成 SOP 工作流
- 先有积木再搭房子，不要过度设计

## 二、三个 Agent 角色定义

### 2.1 产品 Agent（策划 + 分析）
**职责**：
- 分析小红书/各平台热点数据，输出选题报告
- 生成产品 IDEA，做竞品分析
- 撰写产品设计文档（页面结构、交互流程、数据模型）
- 定义 MVP 范围、用户画像、变现路径

**对应 Skill**：
| Skill 名称 | 作用 |
|---|---|
| `trend-analyst` | 调用小红书MCP抓数据 → 输出选题分析报告 |
| `product-designer` | 给定选题 → 生成完整设计文档 |
| `competitor-analyzer` | 给定关键词 → 竞品内容分析 + 差异化建议 |

### 2.2 设计 Agent（UI + 交互）
**职责**：
- 根据设计文档，生成页面的 UI 方案（配色、组件、布局）
- 输出设计规范（Design Token），供开发 Agent 直接使用
- 生成分享图、封面图等视觉素材（调用图片生成能力）
- 评审开发 Agent 的实现，提出 UI 优化建议

**对应 Skill**：
| Skill 名称 | 作用 |
|---|---|
| `ui-spec-generator` | 给定设计文档 → 输出 Design Token（颜色/字体/间距/组件规范） |
| `share-card-designer` | 给定产品 → 设计分享卡片模板 |
| `landing-page-reviewer` | 截图审查页面 → 输出 UI/UX 优化清单 |

### 2.3 开发 Agent（实现 + 部署）
**职责**：
- 根据设计文档 + UI 规范，生成完整的网站/小程序代码
- 实现具体功能逻辑（答题引擎、分享图生成、数据统计）
- 处理部署上线（CloudStudio / EdgeOne Pages）
- 维护 `web_site/` 下的所有项目代码

**对应 Skill**：
| Skill 名称 | 作用 |
|---|---|
| `nextjs-scaffold` | 给定设计文档 → 生成 Next.js + shadcn/ui 项目脚手架 |
| `quiz-engine` | 通用"趣味测试"引擎（题目配置→答题→结果计算→分享图） |
| `deploy-helper` | 一键部署到 CloudStudio/EdgeOne Pages |
| `share-image-gen` | 实现 HTML2Canvas 分享图生成功能 |

## 三、协作流程示例（以 PawMBTI 为例）

```
第1步 [产品Agent]  输入产品关键词
        ↓ 调用 trend-analyst skill
        ↓ 输出：选题分析报告 → 产品IDEA/3、宠物MBTI测试.md

第2步 [产品Agent]  基于分析，生成设计文档
        ↓ 调用 product-designer skill
        ↓ 输出：设计文档 → 产品IDEA/3、宠物MBTI测试-设计文档.md

第3步 [设计Agent]  基于设计文档，细化 UI
        ↓ 调用 ui-spec-generator skill
        ↓ 输出：Design Token + 组件规范

第4步 [开发Agent]  基于设计文档 + UI 规范，写代码
        ↓ 调用 nextjs-scaffold + quiz-engine skill
        ↓ 输出：web_site/pawmbti/ 完整代码

第5步 [开发Agent]  部署上线
        ↓ 调用 deploy-helper skill
        ↓ 输出：线上 URL

第6步 [产品Agent]  回到自媒体流水线，生成推广内容
        ↓ 调用写稿模块 → 发布到小红书
```

## 四、Skill 优先级规划

| 优先级 | Skill | 原因 |
|--------|-------|------|
| ⭐ P0 | `trend-analyst`（选题分析） | 已有手动经验，标准化成 Skill 即可反复用 |
| ⭐ P0 | `product-designer`（设计文档生成） | 已有模板，沉淀后每个新产品都能用 |
| ⭐ P0 | `quiz-engine`（趣味测试引擎） | IDEA 里已有 3 个测试类产品（MBTI/天选城市/宠物MBTI），高复用 |
| 🔵 P1 | `deploy-helper`（部署助手） | 做完网站要能上线 |
| 🔵 P1 | `ui-spec-generator`（UI规范生成） | 保证视觉一致性 |
| ⚪ P2 | `share-card-designer` / `share-image-gen` | 分享裂变是增长关键，但可后置 |

## 五、目录结构建议

```
AIAgent/
├── skills/                    # 所有 Skill 存放处
│   ├── trend-analyst.md       # 选题分析
│   ├── product-designer.md    # 设计文档生成
│   ├── quiz-engine.md         # 趣味测试引擎
│   ├── deploy-helper.md       # 部署助手
│   └── ...
├── 产品IDEA/                  # 产品 Agent 的输出
├── web_site/                  # 开发 Agent 的输出
├── 1_热点监控/ ~ 7_内容发布/   # 自媒体流水线（已有）
└── 经验文档/                   # 经验沉淀
```

## 六、关键心得

1. **Skill 的复用性是关键**：`quiz-engine` 能同时服务 MBTI测试、天选城市、宠物MBTI 等多个产品
2. **从最常重复的工作开始 Skill 化**：什么事情你已经手动做了 2 次以上，就该做成 Skill
3. **Agent 不是越多越好**：3 个角色（产品/设计/开发）已经足够，核心是 Skill 的丰富度
4. **每个 Skill 的输入输出要明确**：输入是什么文件/数据，输出到哪个目录，格式是什么——定义清楚了才能被 Agent 自动编排






