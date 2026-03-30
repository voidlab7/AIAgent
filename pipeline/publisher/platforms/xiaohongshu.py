"""
小红书发布器

支持两种发布方式：
1. MCP 方式（推荐）：通过 xiaohongshu-mcp 服务发布
   - 在 CodeBuddy 中直接使用 Skill 触发
   - 规则文件：.codebuddy/rules/xhs-publish.mdc
   
2. CDP 方式：通过 post-to-xhs Skill 脚本发布（需要配置 Chrome）
   - 适合自动化脚本调用
   - 需要 Chrome 和 post-to-xhs 脚本
"""
import os
import sys
import subprocess
import tempfile
from typing import Dict, List, Optional
from pathlib import Path

# 添加项目根目录到路径
project_root = Path(__file__).parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

# 导入时需要使用完整模块路径
import importlib
base_module = importlib.import_module("7_内容发布.platforms.base")
PublisherBase = base_module.PublisherBase


class XiaohongshuPublisher(PublisherBase):
    """小红书发布器"""
    
    def __init__(self, account: str = "default"):
        super().__init__(account)
        
        # post-to-xhs Skill 脚本路径
        project_root = Path(__file__).parent.parent.parent
        self.skill_dir = project_root / "skills" / "post-to-xhs"
        self.scripts_dir = self.skill_dir / "scripts"
        self.pipeline_script = self.scripts_dir / "publish_pipeline.py"
        self.cdp_script = self.scripts_dir / "cdp_publish.py"
        
        # 验证脚本存在
        if not self.pipeline_script.exists():
            raise FileNotFoundError(
                f"post-to-xhs Skill 未找到: {self.pipeline_script}\n"
                f"请先执行: cp -r xiaohongshu-mcp/skills/post-to-xhs skills/"
            )
    
    def check_login(self) -> bool:
        """检查登录状态"""
        try:
            result = subprocess.run(
                [sys.executable, str(self.cdp_script), "check-login"],
                capture_output=True,
                text=True,
                timeout=30
            )
            return result.returncode == 0
        except Exception as e:
            print(f"检查登录失败: {e}")
            return False
    
    def publish(self, 
                title: str, 
                content: str, 
                images: Optional[List[str]] = None,
                mode: str = "image",  # "image" 或 "long-article"
                headless: bool = True,
                **kwargs) -> Dict:
        """
        发布内容到小红书
        
        Args:
            title: 标题（≤38字符，中文计2，英文计1）
            content: 正文
            images: 图片路径或URL列表（图文模式必需）
            mode: 发布模式，"image"（图文）或 "long-article"（长文）
            headless: 是否使用无头模式（True=后台运行）
            **kwargs: 其他参数
        
        Returns:
            发布结果字典
        """
        # 1. 验证内容
        validation = self.validate_content(title, content)
        if not validation["valid"]:
            return {
                "success": False,
                "message": f"内容验证失败: {', '.join(validation['errors'])}"
            }
        
        # 2. 验证标题长度
        title_length = self._calculate_title_length(title)
        if title_length > 38:
            return {
                "success": False,
                "message": f"标题过长（{title_length}/38），请缩短标题"
            }
        
        # 3. 验证图片（图文模式必需）
        if mode == "image" and (not images or len(images) == 0):
            return {
                "success": False,
                "message": "图文模式必须提供至少一张图片"
            }
        
        # 4. 写入临时文件
        try:
            with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', 
                                            suffix='.txt', delete=False) as title_file:
                title_file.write(title)
                title_path = title_file.name
            
            with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', 
                                            suffix='.txt', delete=False) as content_file:
                content_file.write(content)
                content_path = content_file.name
            
            # 5. 构建发布命令
            if mode == "image":
                result = self._publish_image_post(
                    title_path, content_path, images, headless
                )
            else:  # long-article
                result = self._publish_long_article(
                    title_path, content_path, images, headless
                )
            
            return result
        
        except Exception as e:
            return {
                "success": False,
                "message": f"发布失败: {str(e)}"
            }
        
        finally:
            # 清理临时文件
            try:
                os.unlink(title_path)
                os.unlink(content_path)
            except:
                pass
    
    def _publish_image_post(self, title_path: str, content_path: str, 
                           images: List[str], headless: bool) -> Dict:
        """发布图文"""
        cmd = [
            sys.executable,
            str(self.pipeline_script),
            "--title-file", title_path,
            "--content-file", content_path,
            "--account", self.account
        ]
        
        if headless:
            cmd.append("--headless")
        
        # 添加图片参数
        if images:
            # 判断是本地路径还是URL
            local_images = [img for img in images if os.path.exists(img)]
            url_images = [img for img in images if img.startswith("http")]
            
            if local_images:
                cmd.extend(["--images"] + local_images)
            if url_images:
                cmd.extend(["--image-urls"] + url_images)
        
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=300  # 5分钟超时
            )
            
            if result.returncode == 0:
                return {
                    "success": True,
                    "article_id": "xhs_published",  # 小红书发布后没有直接返回ID
                    "url": "",
                    "message": "发布成功"
                }
            else:
                return {
                    "success": False,
                    "message": f"发布失败: {result.stderr}"
                }
        
        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "message": "发布超时（5分钟）"
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"执行失败: {str(e)}"
            }
    
    def _publish_long_article(self, title_path: str, content_path: str,
                             images: Optional[List[str]], headless: bool) -> Dict:
        """发布长文"""
        # TODO: 实现长文发布流程
        # 需要调用 cdp_publish.py 的多个步骤：
        # 1. long-article (填写内容 + 一键排版)
        # 2. 用户选择模板
        # 3. select-template
        # 4. click-next-step
        # 5. click-publish
        
        return {
            "success": False,
            "message": "长文模式暂未实现，请使用图文模式"
        }
    
    def _calculate_title_length(self, title: str) -> int:
        """
        计算标题长度
        中文字符和中文标点：每个计2
        英文字母/数字/空格/ASCII标点：每个计1
        """
        length = 0
        chinese_punctuation = "，。！？；：""''《》【】（）、"
        
        for char in title:
            if '\u4e00' <= char <= '\u9fff' or char in chinese_punctuation:
                length += 2
            else:
                length += 1
        
        return length
    
    def list_accounts(self) -> List[Dict]:
        """列出所有账号"""
        try:
            result = subprocess.run(
                [sys.executable, str(self.cdp_script), "list-accounts"],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode == 0:
                # 解析输出
                # TODO: 根据实际输出格式解析
                return []
            else:
                return []
        except Exception as e:
            print(f"列出账号失败: {e}")
            return []
    
    def add_account(self, account_name: str, alias: str = "") -> bool:
        """添加新账号"""
        try:
            cmd = [sys.executable, str(self.cdp_script), "add-account", account_name]
            if alias:
                cmd.extend(["--alias", alias])
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            return result.returncode == 0
        except Exception as e:
            print(f"添加账号失败: {e}")
            return False


# 便捷函数
def quick_publish(title: str, content: str, images: List[str], 
                  account: str = "default", headless: bool = True) -> Dict:
    """
    快速发布到小红书（CDP 方式）
    
    Example:
        result = quick_publish(
            title="我的标题",
            content="这是正文内容",
            images=["https://example.com/image.jpg"],
            headless=True
        )
    """
    publisher = XiaohongshuPublisher(account=account)
    return publisher.publish(title, content, images, headless=headless)


# ============================================================
# MCP 发布方式（推荐在 CodeBuddy 中使用）
# ============================================================
"""
MCP 发布使用 xiaohongshu-mcp 服务，通过 Skill 规则触发。

发布流程：
1. 检查登录：xiaohongshu.check_login_status
2. 获取二维码（如未登录）：xiaohongshu.get_login_qrcode
3. 发布内容：xiaohongshu.publish_content

参数格式：
{
    "title": "标题（≤20字）",
    "content": "正文（不含#标签）",
    "images": ["图片路径1", "图片路径2"],
    "tags": ["话题1", "话题2"],
    "is_original": true,
    "schedule_at": "2026-03-26T10:00:00+08:00"  # 可选，定时发布
}

触发方式：
在 CodeBuddy 对话中说：「发布小红书」「发个小红书」等

规则文件位置：
.codebuddy/rules/xhs-publish.mdc
"""
