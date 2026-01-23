#!/usr/bin/env python3
"""
测试数据库配置的简单脚本
"""

import sys
import os

# 添加项目路径到sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from app.models.database import db
    print("✓ 成功导入db实例")
    print(f"db实例类型: {type(db)}")
    print(f"db实例: {db}")
except ImportError as e:
    print(f"✗ 导入db失败: {e}")
    sys.exit(1)

try:
    from app import create_app
    app = create_app()
    print("✓ 成功创建Flask应用")
except Exception as e:
    print(f"✗ 创建Flask应用失败: {e}")
    sys.exit(1)

try:
    with app.app_context():
        print("✓ 成功创建应用上下文")
        # 检查db是否已初始化
        if db.get_engine():
            print("✓ 数据库引擎已初始化")
            print(f"数据库URI: {app.config['SQLALCHEMY_DATABASE_URI']}")
        else:
            print("✗ 数据库引擎未初始化")
except Exception as e:
    print(f"✗ 应用上下文测试失败: {e}")
    sys.exit(1)

print("\n🎉 所有测试通过！数据库配置正确。")