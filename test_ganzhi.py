#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
测试干支关系分析的简化输出格式
"""

from ganzhi_relations import analyze_ganzhi_relations

def test_ganzhi_relations():
    """测试干支关系分析功能"""
    # 测试案例1：2000年9月23日7时（女）
    print("测试案例1：2000年9月23日7时")
    print("八字：庚辰 乙酉 甲申 戊辰")
    result1 = analyze_ganzhi_relations("庚辰", "乙酉", "甲申", "戊辰")
    print(result1)
    print("=" * 50)
    
    # 测试案例2：2004年案例
    print("测试案例2：癸未 乙丑 戊申 乙卯")
    result2 = analyze_ganzhi_relations("癸未", "乙丑", "戊申", "乙卯")
    print(result2)
    print("=" * 50)

if __name__ == "__main__":
    test_ganzhi_relations()