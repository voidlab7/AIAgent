"""
测试发布模块集成
"""
import sys
from pathlib import Path

# 添加项目根目录到 Python 路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


def test_imports():
    """测试模块导入"""
    print("测试模块导入...")
    
    try:
        from 7_内容发布.platforms.base import PublisherBase
        print("  ✓ 导入 PublisherBase")
        
        from 7_内容发布.platforms.xiaohongshu import XiaohongshuPublisher
        print("  ✓ 导入 XiaohongshuPublisher")
        
        from 7_内容发布.main import PublisherManager
        print("  ✓ 导入 PublisherManager")
        
        return True
    except Exception as e:
        print(f"  ✗ 导入失败: {e}")
        return False


def test_skill_files():
    """测试 Skill 文件是否存在"""
    print("\n测试 Skill 文件...")
    
    skill_dir = project_root / "skills" / "post-to-xhs"
    
    required_files = [
        "SKILL.md",
        "scripts/publish_pipeline.py",
        "scripts/cdp_publish.py",
        "scripts/chrome_launcher.py",
        "scripts/account_manager.py",
    ]
    
    all_exist = True
    for file_path in required_files:
        full_path = skill_dir / file_path
        if full_path.exists():
            print(f"  ✓ {file_path}")
        else:
            print(f"  ✗ {file_path} - 不存在")
            all_exist = False
    
    return all_exist


def test_publisher_creation():
    """测试发布器创建"""
    print("\n测试发布器创建...")
    
    try:
        from 7_内容发布.platforms.xiaohongshu import XiaohongshuPublisher
        
        publisher = XiaohongshuPublisher(account="default")
        print(f"  ✓ 创建发布器成功")
        print(f"    平台名称: {publisher.platform_name}")
        print(f"    账号: {publisher.account}")
        print(f"    Skill 目录: {publisher.skill_dir}")
        
        # 检查脚本路径
        if publisher.pipeline_script.exists():
            print(f"    ✓ pipeline 脚本存在")
        else:
            print(f"    ✗ pipeline 脚本不存在: {publisher.pipeline_script}")
            return False
        
        return True
    except Exception as e:
        print(f"  ✗ 创建失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_title_length():
    """测试标题长度计算"""
    print("\n测试标题长度计算...")
    
    try:
        from 7_内容发布.platforms.xiaohongshu import XiaohongshuPublisher
        
        publisher = XiaohongshuPublisher()
        
        test_cases = [
            ("Hello World", 11),
            ("你好世界", 8),
            ("Hello你好", 9),
            ("《Python教程》", 14),
        ]
        
        all_pass = True
        for title, expected in test_cases:
            actual = publisher._calculate_title_length(title)
            if actual == expected:
                print(f"  ✓ '{title}' = {actual}")
            else:
                print(f"  ✗ '{title}' = {actual}, 期望 {expected}")
                all_pass = False
        
        return all_pass
    except Exception as e:
        print(f"  ✗ 测试失败: {e}")
        return False


def test_manager_creation():
    """测试发布管理器创建"""
    print("\n测试发布管理器创建...")
    
    try:
        from 7_内容发布.main import PublisherManager
        
        manager = PublisherManager()
        print(f"  ✓ 创建管理器成功")
        print(f"    支持的平台: {list(manager.publishers.keys())}")
        
        return True
    except Exception as e:
        print(f"  ✗ 创建失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_database_tables():
    """测试数据库表"""
    print("\n测试数据库表...")
    
    try:
        from common.database import Database
        
        db = Database()
        
        # 检查 articles 表
        db.cursor.execute("SELECT COUNT(*) FROM articles")
        article_count = db.cursor.fetchone()[0]
        print(f"  ✓ articles 表存在，{article_count} 条记录")
        
        # 检查 publish_records 表
        db.cursor.execute("SELECT COUNT(*) FROM publish_records")
        record_count = db.cursor.fetchone()[0]
        print(f"  ✓ publish_records 表存在，{record_count} 条记录")
        
        return True
    except Exception as e:
        print(f"  ✗ 数据库测试失败: {e}")
        return False


def main():
    """运行所有测试"""
    print("="*60)
    print("发布模块集成测试")
    print("="*60)
    
    tests = [
        ("模块导入", test_imports),
        ("Skill 文件", test_skill_files),
        ("发布器创建", test_publisher_creation),
        ("标题长度计算", test_title_length),
        ("管理器创建", test_manager_creation),
        ("数据库表", test_database_tables),
    ]
    
    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"\n✗ {name} 测试出错: {e}")
            results.append((name, False))
    
    # 汇总结果
    print("\n" + "="*60)
    print("测试结果汇总")
    print("="*60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✓ 通过" if result else "✗ 失败"
        print(f"{status:<10} {name}")
    
    print("="*60)
    print(f"总计: {passed}/{total} 通过")
    
    if passed == total:
        print("\n🎉 所有测试通过！集成成功！")
        print("\n下一步:")
        print("  1. 确保 Chrome 浏览器已安装")
        print("  2. 安装 Python 依赖: pip install websockets requests")
        print("  3. 登录小红书: cd skills/post-to-xhs/scripts && python cdp_publish.py login")
        print("  4. 开始发布: cd 7_内容发布 && python main.py --article-id 1 --platform xiaohongshu")
    else:
        print("\n⚠️ 部分测试失败，请检查错误信息")
    
    return passed == total


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
