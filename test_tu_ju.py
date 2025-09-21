#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
测试土局的各种情况
"""

from ganzhi_relations import analyze_ganzhi_relations

def test_tu_ju():
    """测试土局的不同情况"""
    
    # 测试1：没有完整土局的情况（实际案例）
    print("测试1：癸未 乙丑 戊申 乙卯（只有丑未，无土局）")
    result1 = analyze_ganzhi_relations("癸未", "乙丑", "戊申", "乙卯")
    print(result1)
    print("=" * 50)
    
    # 测试2：有完整四个土支的情况
    print("测试2：辰辰 戌戌 丑丑 未未（四个土支都有）")
    result2 = analyze_ganzhi_relations("辰辰", "戌戌", "丑丑", "未未")
    print(result2)
    print("=" * 50)
    
    # 测试3：只有三个土支的情况
    print("测试3：辰辰 戌戌 丑丑 甲子（三个土支）")
    result3 = analyze_ganzhi_relations("辰辰", "戌戌", "丑丑", "甲子")
    print(result3)
    print("=" * 50)

if __name__ == "__main__":
    test_tu_ju()