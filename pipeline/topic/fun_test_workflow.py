"""
趣味测试自动化工作流
聊天框关键词触发 -> MCP数据爬取 -> 分析 -> 生成报告
"""
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any

# 添加项目根目录
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from common.config import REPORTS_DIR


class FunTestWorkflow:
    """
    趣味测试自动化工作流
    
    完整流程：
    1. 检测触发关键词
    2. 通过MCP获取小红书数据
    3. 分析热点数据
    4. 生成爆款选题报告
    """
    
    # 搜索配置
    DEFAULT_KEYWORDS = ["趣味测试", "心理测试", "性格测试"]
    DEFAULT_LIMIT = 20  # 每个关键词搜索的数量
    
    def __init__(self):
        """初始化工作流"""
        self.notes_data: List[Dict] = []
        self.analysis_result: Optional[Dict] = None
        self.report_path: Optional[Path] = None
        self.status = "idle"  # idle, running, completed, error
        self.error_message = ""
    
    def run(self, 
            keywords: Optional[List[str]] = None,
            limit: int = None,
            mcp_search_func=None,
            progress_callback=None) -> Dict:
        """
        运行完整工作流
        
        Args:
            keywords: 搜索关键词列表
            limit: 每个关键词的搜索数量
            mcp_search_func: MCP搜索函数（外部注入）
            progress_callback: 进度回调函数
            
        Returns:
            工作流执行结果
        """
        self.status = "running"
        keywords = keywords or self.DEFAULT_KEYWORDS
        limit = limit or self.DEFAULT_LIMIT
        
        result = {
            "success": False,
            "status": "running",
            "steps": [],
            "notes_count": 0,
            "report_path": None,
            "error": None,
        }
        
        try:
            # Step 1: 获取数据
            self._log_progress(progress_callback, "step1", "🔍 正在搜索小红书热门趣味测试...")
            
            if mcp_search_func:
                # 使用MCP搜索
                self.notes_data = self._fetch_via_mcp(keywords, limit, mcp_search_func)
            else:
                # 返回需要MCP调用的指令
                result["needs_mcp"] = True
                result["mcp_instructions"] = self._generate_mcp_instructions(keywords, limit)
                result["steps"].append({
                    "step": 1,
                    "name": "数据获取",
                    "status": "waiting_mcp",
                    "message": "需要调用MCP获取数据"
                })
                return result
            
            result["steps"].append({
                "step": 1,
                "name": "数据获取",
                "status": "completed",
                "message": f"获取到 {len(self.notes_data)} 条笔记"
            })
            
            # Step 2: 数据分析
            self._log_progress(progress_callback, "step2", "📊 正在分析热点数据...")
            
            from fun_test_analyzer import FunTestAnalyzer
            analyzer = FunTestAnalyzer()
            analyzer.load_notes_from_data(self.notes_data)
            self.analysis_result = analyzer.analyze()
            
            result["steps"].append({
                "step": 2,
                "name": "数据分析",
                "status": "completed",
                "message": f"分析完成，识别出 {len(analyzer.analysis_result.get('type_analysis', {}))} 种内容类型"
            })
            
            # Step 3: 生成报告
            self._log_progress(progress_callback, "step3", "📝 正在生成爆款选题报告...")
            
            self.report_path = analyzer.generate_report()
            
            result["steps"].append({
                "step": 3,
                "name": "报告生成",
                "status": "completed",
                "message": f"报告已生成: {self.report_path}"
            })
            
            # 完成
            self.status = "completed"
            result["success"] = True
            result["status"] = "completed"
            result["notes_count"] = len(self.notes_data)
            result["report_path"] = str(self.report_path)
            result["summary"] = self.analysis_result.get("summary", {})
            result["top_5"] = self.analysis_result.get("top_10", [])[:5]
            
            self._log_progress(progress_callback, "complete", "✅ 工作流执行完成！")
            
        except Exception as e:
            self.status = "error"
            self.error_message = str(e)
            result["success"] = False
            result["status"] = "error"
            result["error"] = str(e)
            
            self._log_progress(progress_callback, "error", f"❌ 执行出错: {e}")
        
        return result
    
    def _fetch_via_mcp(self, 
                       keywords: List[str], 
                       limit: int,
                       mcp_search_func) -> List[Dict]:
        """通过MCP获取数据"""
        all_notes = []
        seen_ids = set()
        
        for keyword in keywords:
            try:
                notes = mcp_search_func(keyword, limit)
                
                for note in notes:
                    note_id = note.get('note_id') or note.get('id', '')
                    if note_id and note_id not in seen_ids:
                        seen_ids.add(note_id)
                        all_notes.append(note)
            except Exception as e:
                print(f"⚠️ 搜索 '{keyword}' 失败: {e}")
        
        return all_notes
    
    def _generate_mcp_instructions(self, keywords: List[str], limit: int) -> Dict:
        """生成MCP调用指令"""
        return {
            "description": "需要调用小红书MCP搜索以下关键词",
            "keywords": keywords,
            "limit_per_keyword": limit,
            "mcp_tool": "search_feeds",
            "example_calls": [
                {
                    "keyword": kw,
                    "arguments": {
                        "keyword": kw,
                        "filters": {"sort_by": "最多点赞"}
                    }
                }
                for kw in keywords
            ]
        }
    
    def _log_progress(self, callback, step: str, message: str):
        """记录进度"""
        print(f"[{step}] {message}")
        if callback:
            callback(step, message)
    
    def process_mcp_results(self, mcp_results: List[Dict]) -> Dict:
        """
        处理MCP返回的结果
        
        Args:
            mcp_results: MCP搜索返回的笔记数据
            
        Returns:
            处理结果
        """
        self.notes_data = mcp_results
        
        # 继续执行分析和报告生成
        from fun_test_analyzer import FunTestAnalyzer
        
        analyzer = FunTestAnalyzer()
        analyzer.load_notes_from_data(self.notes_data)
        self.analysis_result = analyzer.analyze()
        self.report_path = analyzer.generate_report()
        
        self.status = "completed"
        
        return {
            "success": True,
            "notes_count": len(self.notes_data),
            "report_path": str(self.report_path),
            "summary": self.analysis_result.get("summary", {}),
            "top_10": self.analysis_result.get("top_10", []),
        }


def get_workflow_prompt() -> str:
    """获取工作流提示信息"""
    return """
🎯 **趣味测试爆款选题分析工作流**

我将为您执行以下步骤：

1️⃣ **数据采集**
   - 搜索关键词：趣味测试、心理测试、性格测试
   - 获取热门笔记数据（点赞、收藏、评论、分享）

2️⃣ **热点分析**
   - 计算热度分数
   - 分类内容类型
   - 识别高互动内容

3️⃣ **报告生成**
   - TOP 10 热门笔记
   - 内容类型分析
   - 爆款选题建议
   - 创作指南

---
正在启动工作流...
"""


def format_workflow_result(result: Dict) -> str:
    """格式化工作流结果"""
    if not result.get("success"):
        return f"❌ 工作流执行失败: {result.get('error', '未知错误')}"
    
    output = f"""
✅ **趣味测试爆款选题分析完成！**

📊 **数据概览**
- 分析笔记数: {result.get('notes_count', 0)} 篇
- 总点赞数: {result.get('summary', {}).get('total_likes', 0):,}
- 总收藏数: {result.get('summary', {}).get('total_collects', 0):,}
- 总评论数: {result.get('summary', {}).get('total_comments', 0):,}

🔥 **热门 TOP 5**
"""
    
    for i, note in enumerate(result.get('top_5', [])[:5], 1):
        title = note.get('title', '')[:25]
        output += f"{i}. [{title}]({note.get('url', '')}) - 👍{note.get('likes', 0):,}\n"
    
    output += f"""
📝 **完整报告**
报告路径: `{result.get('report_path', '')}`

💡 **下一步建议**
1. 查看报告中的「爆款选题建议」部分
2. 选择一个热门类型进行创作
3. 参考标题模板和创作建议
"""
    
    return output


# 主入口函数
def trigger_fun_test_analysis(mcp_client=None) -> str:
    """
    触发趣味测试分析（主入口）
    
    Args:
        mcp_client: MCP客户端（可选）
        
    Returns:
        执行结果消息
    """
    workflow = FunTestWorkflow()
    
    # 如果没有MCP客户端，返回需要MCP调用的指令
    if mcp_client is None:
        return get_workflow_prompt() + """

⚠️ **需要MCP支持**

请使用以下MCP工具获取数据：

```
工具: search_feeds
参数:
  - keyword: "趣味测试" / "心理测试" / "性格测试"
  - filters: {"sort_by": "最多点赞"}
```

获取数据后，请将结果传入分析器。
"""
    
    # 有MCP客户端，执行完整流程
    result = workflow.run(mcp_search_func=mcp_client.search)
    return format_workflow_result(result)


if __name__ == "__main__":
    print(get_workflow_prompt())
    print("\n测试工作流初始化...")
    
    workflow = FunTestWorkflow()
    result = workflow.run()
    
    if result.get("needs_mcp"):
        print("\n需要MCP调用:")
        print(result.get("mcp_instructions"))
    else:
        print(format_workflow_result(result))
