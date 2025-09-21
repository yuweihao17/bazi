#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
自动化测试脚本，模拟用户输入测试八字计算功能
"""

import subprocess
import sys
import os

def test_bazi_calculator():
    """自动测试八字计算器"""
    
    test_data = "女\ng\n2000\n9\n23\n7\n"
    
    try:
        # 使用subprocess运行程序并提供输入
        result = subprocess.run(
            [sys.executable, "2_fixed.py"],
            input=test_data,
            capture_output=True,
            text=True,
            encoding='utf-8',
            timeout=30,
            cwd=os.getcwd()
        )
        
        if result.returncode == 0:
            print("程序运行成功！")
            print("=" * 60)
            print("程序输出：")
            print(result.stdout)
            
            # 检查输出是否包含关键信息
            output = result.stdout
            if "天干关系：" in output and "地支关系：" in output:
                print("✅ 干支关系分析功能正常！")
            else:
                print("❌ 干支关系分析可能有问题")
                
            if "乙庚合化金" in output:
                print("✅ 输出格式简化成功，没有位置信息！")
            else:
                print("❌ 输出格式可能需要调整")
        else:
            print(f"程序运行失败，返回码：{result.returncode}")
            print("错误信息：")
            print(result.stderr)
            
    except subprocess.TimeoutExpired:
        print("程序运行超时")
    except Exception as e:
        print(f"测试过程中出现错误：{e}")

if __name__ == "__main__":
    print("开始自动化测试...")
    test_bazi_calculator()