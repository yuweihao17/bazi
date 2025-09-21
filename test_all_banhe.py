#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
测试所有8种半合关系
"""

from ganzhi_relations import analyze_ganzhi_relations

def test_all_banhe():
    """测试所有8种半合关系"""
    
    # 水局半合
    print("=== 水局半合 ===")
    print("1. 申子半合水局：")
    result1 = analyze_ganzhi_relations("甲申", "乙子", "丙寅", "丁巳")
    print(f"   甲申 乙子 丙寅 丁巳 -> {result1.split('地支关系：')[1] if '地支关系：' in result1 else '无地支关系'}")
    
    print("2. 子辰半合水局：")
    result2 = analyze_ganzhi_relations("甲寅", "乙子", "丙辰", "丁巳")
    print(f"   甲寅 乙子 丙辰 丁巳 -> {result2.split('地支关系：')[1] if '地支关系：' in result2 else '无地支关系'}")
    
    # 火局半合
    print("\n=== 火局半合 ===")
    print("3. 寅午半合火局：")
    result3 = analyze_ganzhi_relations("甲寅", "乙午", "丙申", "丁亥")
    print(f"   甲寅 乙午 丙申 丁亥 -> {result3.split('地支关系：')[1] if '地支关系：' in result3 else '无地支关系'}")
    
    print("4. 午戌半合火局：")
    result4 = analyze_ganzhi_relations("甲申", "乙午", "丙戌", "丁亥")
    print(f"   甲申 乙午 丙戌 丁亥 -> {result4.split('地支关系：')[1] if '地支关系：' in result4 else '无地支关系'}")
    
    # 木局半合
    print("\n=== 木局半合 ===")
    print("5. 亥卯半合木局：")
    result5 = analyze_ganzhi_relations("甲申", "乙亥", "丙卯", "丁午")
    print(f"   甲申 乙亥 丙卯 丁午 -> {result5.split('地支关系：')[1] if '地支关系：' in result5 else '无地支关系'}")
    
    print("6. 卯未半合木局：")
    result6 = analyze_ganzhi_relations("甲申", "乙卯", "丙未", "丁午")
    print(f"   甲申 乙卯 丙未 丁午 -> {result6.split('地支关系：')[1] if '地支关系：' in result6 else '无地支关系'}")
    
    # 金局半合
    print("\n=== 金局半合 ===")
    print("7. 巳酉半合金局：")
    result7 = analyze_ganzhi_relations("甲申", "乙巳", "丙酉", "丁午")
    print(f"   甲申 乙巳 丙酉 丁午 -> {result7.split('地支关系：')[1] if '地支关系：' in result7 else '无地支关系'}")
    
    print("8. 酉丑半合金局：")
    result8 = analyze_ganzhi_relations("甲申", "乙酉", "丙丑", "丁午")
    print(f"   甲申 乙酉 丙丑 丁午 -> {result8.split('地支关系：')[1] if '地支关系：' in result8 else '无地支关系'}")

if __name__ == "__main__":
    test_all_banhe()