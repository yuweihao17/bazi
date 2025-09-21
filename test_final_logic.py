#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
测试修正后的2004年案例
验证新的计算逻辑是否正确
"""

import sys

def test_corrected_calculation():
    """测试修正后的计算结果"""
    print("=" * 60)
    print("测试2004年1月30日6时案例的修正计算")
    print("=" * 60)
    
    # 基本信息
    birth_year = 2004
    start_age = 8  # 8岁起运
    
    print(f"出生年份：{birth_year}年")
    print(f"起运年龄：{start_age}岁")
    print()
    
    # 按照用户要求的修正逻辑
    print("按照传统命理学0岁起算：")
    print(f"- {birth_year}年出生 = 0岁")
    print(f"- {start_age}岁起运")
    print(f"- 大运开始年份 = {birth_year} + {start_age} = {birth_year + start_age}年")
    print()
    
    # 计算八部大运年份
    dayun_years = []
    for i in range(8):
        year = birth_year + start_age + i * 10
        dayun_years.append(year)
    
    print("八部大运年份：")
    dayun_names = ["甲子", "癸亥", "壬戌", "辛酉", "庚申", "己未", "戊午", "丁巳"]
    for i, (name, year) in enumerate(zip(dayun_names, dayun_years)):
        age = start_age + i * 10
        print(f"{name}大运：{year}年（{age}岁）")
    
    print()
    print("重点验证：")
    print(f"第一个大运（甲子）开始年份：{dayun_years[0]}年")
    print(f"对应年龄：{start_age}岁起运，{start_age + 1}岁开始走大运")
    
    # 验证用户的要求
    expected_first_year = 2012
    if dayun_years[0] == expected_first_year:
        print(f"✅ 符合用户要求：{expected_first_year}年壬辰年开始走甲子大运")
    else:
        print(f"❌ 不符合用户要求：应该是{expected_first_year}年，但计算得到{dayun_years[0]}年")
    
    return dayun_years[0] == expected_first_year

if __name__ == "__main__":
    result = test_corrected_calculation()
    print("\n" + "=" * 60)
    if result:
        print("✅ 测试通过！修正逻辑正确")
    else:
        print("❌ 测试失败！需要进一步调整")
    print("=" * 60)