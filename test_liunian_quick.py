#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
快速测试流年查询功能
"""

import subprocess
import sys

def test_liunian_with_file():
    """使用文件输入测试流年查询功能"""
    
    # 创建输入文件
    input_data = """女
g
2000
9
23
7
甲子
q
"""
    
    with open("test_input_liunian.txt", "w", encoding="utf-8") as f:
        f.write(input_data)
    
    # 运行程序
    try:
        result = subprocess.run(
            [sys.executable, "2_fixed.py"],
            input=input_data,
            capture_output=True,
            text=True,
            encoding='utf-8',
            timeout=30
        )
        
        if result.returncode == 0:
            print("✅ 程序运行成功！")
            print("输出内容：")
            print(result.stdout)
            
            # 检查是否包含流年查询功能
            if "流年查询功能" in result.stdout:
                print("✅ 流年查询功能已恢复！")
            else:
                print("❌ 流年查询功能可能有问题")
                
        else:
            print(f"❌ 程序运行失败，返回码：{result.returncode}")
            print("错误信息：")
            print(result.stderr)
            
    except Exception as e:
        print(f"测试过程中出现错误：{e}")

if __name__ == "__main__":
    test_liunian_with_file()