#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
测试半合和三合的优先级逻辑
"""

from ganzhi_relations import analyze_ganzhi_relations

def test_banhe_sanhe():
    """测试半合和三合的关系"""
    
    # 测试1：只有半合的情况（申子半合水局）
    print("测试1：甲申 乙子 丙寅 丁亥（申子半合水局）")
    result1 = analyze_ganzhi_relations("甲申", "乙子", "丙寅", "丁亥")
    print(result1)
    print("=" * 60)
    
    # 测试2：完整三合的情况（申子辰合水局，应该不显示申子半合和子辰半合）
    print("测试2：甲申 乙子 丙辰 丁亥（完整三合，不显示半合）")
    result2 = analyze_ganzhi_relations("甲申", "乙子", "丙辰", "丁亥")
    print(result2)
    print("=" * 60)
    
    # 测试3：火局半合（寅午半合火局）
    print("测试3：甲寅 乙午 丙申 丁亥（寅午半合火局）")
    result3 = analyze_ganzhi_relations("甲寅", "乙午", "丙申", "丁亥")
    print(result3)
    print("=" * 60)
    
    # 测试4：完整火局三合（寅午戌合火局，不显示半合）
    print("测试4：甲寅 乙午 丙戌 丁亥（完整三合，不显示半合）")
    result4 = analyze_ganzhi_relations("甲寅", "乙午", "丙戌", "丁亥")
    print(result4)
    print("=" * 60)
    
    # 测试5：原始案例（癸未 乙丑 戊申 乙卯）
    print("测试5：癸未 乙丑 戊申 乙卯（检查是否有新的半合）")
    result5 = analyze_ganzhi_relations("癸未", "乙丑", "戊申", "乙卯")
    print(result5)
    print("=" * 60)

if __name__ == "__main__":
    test_banhe_sanhe()