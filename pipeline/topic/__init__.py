"""
选题筛选模块初始化
"""
from pathlib import Path

# 模块根目录
MODULE_ROOT = Path(__file__).parent

# 导出主要类和函数
from .fun_test_analyzer import FunTestAnalyzer, NoteData, run_analysis
from .keyword_trigger import KeywordTrigger, FunTestTrigger, TriggerType
from .fun_test_workflow import FunTestWorkflow, trigger_fun_test_analysis

__all__ = [
    # 分析器
    'FunTestAnalyzer',
    'NoteData',
    'run_analysis',
    
    # 触发器
    'KeywordTrigger',
    'FunTestTrigger',
    'TriggerType',
    
    # 工作流
    'FunTestWorkflow',
    'trigger_fun_test_analysis',
]
