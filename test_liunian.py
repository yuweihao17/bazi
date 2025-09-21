#!/usr/bin/env python3
"""
测试流年查询功能
"""

import sys
import os
from datetime import datetime

# 添加当前目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# 导入主程序的函数
import importlib.util
spec = importlib.util.spec_from_file_location("main", "2.py")
if spec and spec.loader:
    main_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(main_module)

    # 导入需要的函数
    get_liunian_for_dayun = main_module.get_liunian_for_dayun
    display_liunian_result = main_module.display_liunian_result

def test_liunian_query():
    """测试流年查询功能"""
    print("=" * 60)
    print("           测试流年查询功能")
    print("=" * 60)
    
    # 测试甲子大运，从2013年开始，9岁起
    dayun_ganzhi = "甲子"
    start_year = 2013
    start_age = 9
    
    print(f"测试大运：{dayun_ganzhi}")
    print(f"开始年份：{start_year}年")
    print(f"开始年龄：{start_age}岁")
    print("-" * 60)
    
    # 计算流年信息
    liunian_list = get_liunian_for_dayun(dayun_ganzhi, start_year, start_age)
    
    print("计算结果：")
    for liunian_ganzhi, year, age in liunian_list:
        print(f"{year}年（{age}岁）- {liunian_ganzhi}")
    
    print("-" * 60)
    print("✅ 流年计算完成")
    
    # 显示格式化结果
    display_liunian_result(dayun_ganzhi, liunian_list)

if __name__ == "__main__":
    test_liunian_query()