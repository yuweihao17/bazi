#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
演示新增的大运与八字作用关系功能
"""

def demo_new_features():
    """演示新功能"""
    print("=" * 60)
    print("            大运与八字作用关系功能演示")
    print("=" * 60)
    
    # 演示八字：庚辰 乙酉 甲申 戊辰
    print("演示八字：庚辰 乙酉 甲申 戊辰")
    print("出生时间：2000年9月23日7时 （女）")
    print()
    
    # 1. 显示原局关系（按新顺序）
    print("一、原局作用关系（按新顺序）：")
    print("-" * 50)
    print("天干关系：乙庚合化金，甲戊相克，庚甲相克")
    print("地支关系：辰酉合化金，申辰拱合子，辰辰自刑")
    
    # 2. 演示大运与八字的作用关系
    print("\n二、大运与八字作用关系分析演示：")
    print("-" * 50)
    
    demo_dayuns = [
        ("甲子", "天干关系：庚甲相克,甲戊相克", "地支关系：无"),
        ("癸亥", "天干关系：戊癸合化火", "地支关系：无"),
        ("壬戌", "天干关系：戊壬相克", "地支关系：辰戌相冲"),
        ("辛酉", "天干关系：乙庚合化金", "地支关系：辰酉合化金")
    ]
    
    for dayun, tiangan, dizhi in demo_dayuns:
        print(f"\n【{dayun}大运与原局作用关系分析】")
        if "无" not in tiangan:
            print(tiangan)
        if "无" not in dizhi:
            print(dizhi)
        if "无" in tiangan and "无" in dizhi:
            print("大运与原局无明显作用关系")
    
    # 3. 演示流年查询功能
    print("\n三、流年查询中的大运作用关系展示：")
    print("-" * 50)
    print("以甲子大运为例，显示该大运十年流年：")
    print()
    print("=" * 50)
    print("        甲子大运十年流年详情")
    print("=" * 50)
    print()
    
    # 模拟流年表格
    liunian = ["庚子", "辛丑", "壬寅", "癸卯", "甲辰", "乙巳", "丙午", "丁未", "戊申", "己酉"]
    years = [2020, 2021, 2022, 2023, 2024, 2025, 2026, 2027, 2028, 2029]
    ages = [30, 31, 32, 33, 34, 35, 36, 37, 38, 39]
    
    print("流年：", end="")
    for ln in liunian:
        print(f"{ln:^6}", end="")
    print()
    
    print("年份：", end="")
    for yr in years:
        print(f"{yr:^6}", end="")
    print()
    
    print("岁数：", end="")
    for age in ages:
        print(f"{age:^6}", end="")
    print()
    
    print("=" * 50)
    
    # 显示八字与大运的作用关系
    print("\n=" * 50)
    print("        八字与甲子大运作用关系分析")
    print("=" * 50)
    print("【原局作用关系】")
    print("天干关系：乙庚合化金，甲戊相克，庚甲相克")
    print("地支关系：辰酉合化金，申辰拱合子，辰辰自刑")
    print("\n【大运与原局作用关系】")
    print("天干关系：庚甲相克,甲戊相克")
    print("=" * 50)
    
    print("\n" + "=" * 60)
    print("新功能特点总结：")
    print("✅ 原局干支关系按照新顺序输出：天干先合再克")
    print("✅ 地支按六合、三合、三会、半合、暗合、拱合、相刑、六冲、六破、六害顺序")
    print("✅ 大运与八字作用关系分析：包含原局关系和大运作用关系")
    print("✅ 流年查询时自动显示八字与大运的作用关系")
    print("✅ 天干关系：优先合化，后相克")
    print("✅ 地支关系：按传统重要性顺序排列")
    print("=" * 60)
    print("\n使用方法：")
    print("1. 运行 python 2_fixed.py")
    print("2. 输入出生信息，查看八字和大运结果")
    print("3. 在大运结果显示后，程序会自动进入流年查询模式")
    print("4. 输入要查询的大运干支（如：甲子、癸亥等）")
    print("5. 查看该大运十年的流年详情及与八字的作用关系")
    print("6. 输入 'q' 或 'quit' 退出流年查询")
    print("=" * 60)
        
if __name__ == "__main__":
    demo_new_features()