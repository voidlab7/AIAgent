# 工作流编排 (Workflows)

## 功能描述
将 7 个独立模块串联成完整的自动化工作流。

## 工作流类型

### 1. 每日创作流（daily_creator.py）
**全自动模式**：从热搜到发布的完整链路

```
刷热搜 → 找选题 → 搜资料 → 写稿 → 找配图 → 排版 → 发布
```

**运行时间**：每天 7:00 开始，8:00 发布

### 2. 手动辅助流（manual_helper.py）
**半自动模式**：人工确认关键节点

```
刷热搜 → [人工选择热点] → AI生成选题 → [人工确认选题] → 自动搜资料 → AI写稿 → [人工审核] → 自动配图+排版 → [人工确认] → 发布
```

### 3. 爆款复制流（viral_replicate.py）
**竞品分析模式**：基于竞品爆款逆向创作

```
输入竞品URL → 分析爆款原因 → 生成相似选题 → 自动创作 → 发布
```

## 文件结构
```
workflows/
├── daily_creator.py    # 每日全自动
├── manual_helper.py    # 半自动辅助
├── viral_replicate.py  # 爆款复制
└── README.md
```

## 使用方式

### 全自动每日创作
```bash
# 立即执行一次完整流程
python -m workflows.daily_creator --run-once

# 启动定时任务（每天 7:00）
python -m workflows.daily_creator --schedule
```

### 半自动辅助模式
```bash
python -m workflows.manual_helper
# 进入交互式界面，逐步确认
```

### 爆款复制
```bash
python -m workflows.viral_replicate --url "https://mp.weixin.qq.com/s/xxx"
```

## 配置
工作流参数在 `common/config.py` 中配置：
- `PUBLISH_SCHEDULE`：发布时间表
- `ACCOUNT_PROFILE`：账号定位
- `CONTENT_LENGTH`：内容长度

## 开发状态
📋 待开发
