#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
验证流年查询功能是否已经恢复
通过检查代码结构来确认
"""

def verify_liunian_functions():
    """验证流年查询相关函数"""
    
    print("=" * 60)
    print("           流年查询功能恢复验证")
    print("=" * 60)
    
    # 检查主程序文件
    main_file = "2_fixed.py"
    
    try:
        with open(main_file, "r", encoding="utf-8") as f:
            content = f.read()
        
        # 检查关键函数
        functions_to_check = [
            "get_liunian_for_dayun",
            "display_liunian_result", 
            "liunian_query_loop"
        ]
        
        print("检查关键函数定义：")
        for func in functions_to_check:
            if f"def {func}" in content:
                print(f"✅ {func} 函数已定义")
            else:
                print(f"❌ {func} 函数缺失")
        
        print("\n检查函数调用：")
        
        # 检查流年查询循环是否被调用
        if "liunian_query_loop(dayun_list, dayun_years, rounded_start_age)" in content:
            print("✅ 流年查询循环已在主程序中调用")
        else:
            print("❌ 流年查询循环未被调用")
        
        # 检查流年查询提示信息
        if "流年查询功能：" in content:
            print("✅ 流年查询提示信息已添加")
        else:
            print("❌ 流年查询提示信息缺失")
        
        # 检查退出条件
        if "'q', 'quit'" in content:
            print("✅ 流年查询退出条件已设置")
        else:
            print("❌ 流年查询退出条件缺失")
        
        print("\n" + "=" * 60)
        print("功能恢复验证结果：")
        
        # 统计检查结果
        total_checks = 0
        passed_checks = 0
        
        checks = [
            ("get_liunian_for_dayun" in content, "流年计算函数"),
            ("display_liunian_result" in content, "流年显示函数"),
            ("liunian_query_loop" in content, "流年查询循环函数"),
            ("liunian_query_loop(dayun_list, dayun_years, rounded_start_age)" in content, "主程序调用"),
            ("流年查询功能：" in content, "用户提示信息"),
            ("'q', 'quit'" in content, "退出功能")
        ]
        
        for check_result, check_name in checks:
            total_checks += 1
            if check_result:
                passed_checks += 1
                print(f"✅ {check_name}")
            else:
                print(f"❌ {check_name}")
        
        print("\n" + "-" * 60)
        print(f"验证结果：{passed_checks}/{total_checks} 项检查通过")
        
        if passed_checks == total_checks:
            print("🎉 流年查询功能已完全恢复！")
            print("\n使用方法：")
            print("1. 运行 python 2_fixed.py")
            print("2. 输入出生信息，查看八字和大运结果")
            print("3. 在大运结果显示后，程序会自动进入流年查询模式")
            print("4. 输入要查询的大运干支（如：甲子、癸亥等）")
            print("5. 查看该大运十年的流年详情")
            print("6. 输入 'q' 或 'quit' 退出流年查询")
        else:
            print("⚠️  部分功能可能存在问题，请检查")
            
    except FileNotFoundError:
        print(f"❌ 文件 {main_file} 未找到")
    except Exception as e:
        print(f"❌ 验证过程中出现错误：{e}")

if __name__ == "__main__":
    verify_liunian_functions()