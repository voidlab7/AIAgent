"""
关键词触发器
支持聊天框关键词检测，触发相应的自动化任务
"""
import re
from typing import Callable, Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum


class TriggerType(Enum):
    """触发器类型"""
    FUN_TEST = "fun_test"           # 趣味测试分析
    HOT_TOPIC = "hot_topic"         # 热点监控
    CONTENT_CREATE = "content"      # 内容创作
    PUBLISH = "publish"             # 内容发布


@dataclass
class TriggerRule:
    """触发规则"""
    trigger_type: TriggerType
    keywords: List[str]             # 触发关键词
    patterns: List[str]             # 正则模式
    description: str                # 描述
    handler: Optional[Callable] = None  # 处理函数


class KeywordTrigger:
    """
    关键词触发器
    
    用于检测用户输入中的关键词，触发相应的自动化任务
    """
    
    # 默认触发规则
    DEFAULT_RULES = [
        TriggerRule(
            trigger_type=TriggerType.FUN_TEST,
            keywords=[
                "趣味测试", "心理测试", "性格测试", "MBTI",
                "测试分析", "测试报告", "爆款选题",
                "小红书测试", "测试热点"
            ],
            patterns=[
                r".*分析.*趣味测试.*",
                r".*趣味测试.*分析.*",
                r".*抓取.*测试.*",
                r".*测试.*热点.*",
                r".*爆款.*测试.*",
                r".*测试.*报告.*",
                r".*小红书.*测试.*",
            ],
            description="小红书趣味测试热点分析，生成爆款选题报告"
        ),
        TriggerRule(
            trigger_type=TriggerType.HOT_TOPIC,
            keywords=[
                "热点监控", "热搜", "热门话题", "刷热点",
                "抓取热点", "热门内容"
            ],
            patterns=[
                r".*抓取.*热点.*",
                r".*监控.*热门.*",
                r".*刷.*热搜.*",
            ],
            description="热点内容监控和抓取"
        ),
        TriggerRule(
            trigger_type=TriggerType.CONTENT_CREATE,
            keywords=[
                "写文章", "创作内容", "生成文案", "AI写稿",
                "内容创作"
            ],
            patterns=[
                r".*写.*文章.*",
                r".*生成.*内容.*",
                r".*AI.*创作.*",
            ],
            description="AI内容创作"
        ),
        TriggerRule(
            trigger_type=TriggerType.PUBLISH,
            keywords=[
                "发布内容", "发布文章", "定时发布", "自动发布"
            ],
            patterns=[
                r".*发布.*",
                r".*定时.*发.*",
            ],
            description="内容发布"
        ),
    ]
    
    def __init__(self, custom_rules: Optional[List[TriggerRule]] = None):
        """
        初始化触发器
        
        Args:
            custom_rules: 自定义规则（可选）
        """
        self.rules = custom_rules or self.DEFAULT_RULES
        self._compile_patterns()
    
    def _compile_patterns(self):
        """预编译正则表达式"""
        for rule in self.rules:
            rule._compiled_patterns = [
                re.compile(p, re.IGNORECASE) for p in rule.patterns
            ]
    
    def detect(self, text: str) -> Optional[Tuple[TriggerType, TriggerRule]]:
        """
        检测文本中是否包含触发关键词
        
        Args:
            text: 用户输入文本
            
        Returns:
            触发类型和规则，如果没有匹配则返回None
        """
        text_lower = text.lower()
        
        for rule in self.rules:
            # 检查关键词
            for keyword in rule.keywords:
                if keyword.lower() in text_lower:
                    return (rule.trigger_type, rule)
            
            # 检查正则模式
            for pattern in rule._compiled_patterns:
                if pattern.match(text):
                    return (rule.trigger_type, rule)
        
        return None
    
    def get_trigger_info(self, text: str) -> Dict:
        """
        获取触发信息
        
        Args:
            text: 用户输入文本
            
        Returns:
            触发信息字典
        """
        result = self.detect(text)
        
        if result:
            trigger_type, rule = result
            return {
                "triggered": True,
                "type": trigger_type.value,
                "description": rule.description,
                "keywords_matched": [
                    kw for kw in rule.keywords 
                    if kw.lower() in text.lower()
                ],
            }
        
        return {
            "triggered": False,
            "type": None,
            "description": None,
            "keywords_matched": [],
        }
    
    def register_handler(self, trigger_type: TriggerType, handler: Callable):
        """
        注册触发处理函数
        
        Args:
            trigger_type: 触发类型
            handler: 处理函数
        """
        for rule in self.rules:
            if rule.trigger_type == trigger_type:
                rule.handler = handler
                break
    
    def execute(self, text: str, **kwargs) -> Optional[Dict]:
        """
        检测并执行触发任务
        
        Args:
            text: 用户输入文本
            **kwargs: 传递给处理函数的额外参数
            
        Returns:
            执行结果
        """
        result = self.detect(text)
        
        if result:
            trigger_type, rule = result
            
            if rule.handler:
                return rule.handler(text, **kwargs)
            else:
                return {
                    "status": "no_handler",
                    "trigger_type": trigger_type.value,
                    "message": f"触发了 {rule.description}，但没有注册处理函数"
                }
        
        return None


# 趣味测试触发器专用
class FunTestTrigger:
    """
    趣味测试专用触发器
    
    用于检测趣味测试相关的关键词并执行分析任务
    """
    
    # 触发关键词
    TRIGGER_KEYWORDS = [
        # 主要关键词
        "趣味测试",
        "心理测试", 
        "性格测试",
        "MBTI测试",
        "测试热点",
        "测试分析",
        "爆款选题",
        
        # 组合关键词
        "小红书测试",
        "测试报告",
        "热门测试",
    ]
    
    # 触发短语模式
    TRIGGER_PATTERNS = [
        r"分析.*趣味测试",
        r"趣味测试.*分析",
        r"抓取.*测试",
        r"爬取.*测试",
        r"测试.*热点",
        r"测试.*报告",
        r"生成.*测试.*报告",
        r"小红书.*测试.*分析",
    ]
    
    def __init__(self):
        self._compiled_patterns = [
            re.compile(p, re.IGNORECASE) for p in self.TRIGGER_PATTERNS
        ]
    
    def should_trigger(self, text: str) -> bool:
        """
        检查是否应该触发趣味测试分析
        
        Args:
            text: 用户输入
            
        Returns:
            是否触发
        """
        text_lower = text.lower()
        
        # 检查关键词
        for keyword in self.TRIGGER_KEYWORDS:
            if keyword.lower() in text_lower:
                return True
        
        # 检查模式
        for pattern in self._compiled_patterns:
            if pattern.search(text):
                return True
        
        return False
    
    def extract_params(self, text: str) -> Dict:
        """
        从文本中提取参数
        
        Args:
            text: 用户输入
            
        Returns:
            提取的参数
        """
        params = {
            "keywords": ["趣味测试"],  # 默认关键词
            "limit": 50,               # 默认数量
            "output_report": True,     # 默认输出报告
        }
        
        # 提取自定义关键词
        keyword_match = re.search(r"关键词[：:]\s*(.+?)(?:\s|$)", text)
        if keyword_match:
            keywords = keyword_match.group(1).split("、")
            params["keywords"] = keywords
        
        # 检查是否有特定测试类型
        test_types = ["心理测试", "性格测试", "MBTI", "情感测试"]
        for tt in test_types:
            if tt in text:
                params["keywords"].append(tt)
        
        # 去重
        params["keywords"] = list(set(params["keywords"]))
        
        return params
    
    def get_trigger_message(self) -> str:
        """获取触发提示消息"""
        return """
🎯 检测到关键词触发：**趣味测试分析**

我将为您执行以下任务：
1. 🔍 搜索小红书热门趣味测试内容
2. 📊 分析热点数据和互动指标
3. 📝 生成爆款选题报告

正在启动分析...
"""


# 导出
__all__ = [
    'KeywordTrigger',
    'FunTestTrigger', 
    'TriggerType',
    'TriggerRule',
]


if __name__ == "__main__":
    # 测试触发器
    trigger = FunTestTrigger()
    
    test_texts = [
        "帮我分析一下小红书趣味测试的热点",
        "抓取趣味测试数据",
        "生成测试报告",
        "小红书上爬取和分析当下最热门的趣味测试话题",
        "我想看看今天的天气",  # 不应该触发
        "帮我写一篇文章",     # 不应该触发
    ]
    
    for text in test_texts:
        result = trigger.should_trigger(text)
        print(f"'{text[:30]}...' -> {'✅ 触发' if result else '❌ 不触发'}")
        
        if result:
            params = trigger.extract_params(text)
            print(f"  参数: {params}")
