#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
测试带有干支关系分析的完整八字排盘
"""

import sys
from datetime import datetime

try:
    from lunar_python import Solar
    from ganzhi_relations import analyze_ganzhi_relations
    
    def calc_bazi_from_solar(year: int, month: int, day: int, hour: int):
        """从公历日期计算四柱八字"""
        solar = Solar.fromYmdHms(year, month, day, hour, 0, 0)
        lunar = solar.getLunar()
        ec = lunar.getEightChar()
        return ec.getYear(), ec.getMonth(), ec.getDay(), ec.getTime()
    
    def test_complete_bazi_analysis():
        """测试完整的八字排盘和关系分析"""
        print("=" * 70)
        print("        四柱八字及大运计算结果（含干支关系分析）")
        print("=" * 70)
        
        # 基本信息
        year, month, day, hour = 2004, 1, 30, 6
        gender = "男"
        
        # 计算八字
        year_pillar, month_pillar, day_pillar, hour_pillar = calc_bazi_from_solar(year, month, day, hour)
        
        print(f"公历时间：{year}年{month}月{day}日 {hour:02d}:00")
        print(f"农历时间：2004年1月初九 06:00")
        print(f"性别：{gender}")
        print("-" * 50)
        print(f"年柱：{year_pillar}")
        print(f"月柱：{month_pillar}")
        print(f"日柱：{day_pillar}")
        print(f"时柱：{hour_pillar}")
        print("-" * 50)
        print(f"四柱八字：{year_pillar} {month_pillar} {day_pillar} {hour_pillar}")
        print("-" * 50)
        
        # 干支关系分析
        print("干支关系分析：")
        analysis_result = analyze_ganzhi_relations(year_pillar, month_pillar, day_pillar, hour_pillar)
        print(analysis_result)
        print("-" * 50)
        
        # 起运信息
        start_age = 8
        print(f"起大运时间：{start_age}岁0个月0天0个时辰")
        print("-" * 50)
        print("八部大运排列：")
        print()
        
        # 模拟大运显示
        dayun_names = ["甲子", "癸亥", "壬戌", "辛酉", "庚申", "己未", "戊午", "丁巳"]
        dayun_ages = [8, 18, 28, 38, 48, 58, 68, 78]
        dayun_years = [2012, 2022, 2032, 2042, 2052, 2062, 2072, 2082]
        
        print("大运：", end="")
        for name in dayun_names:
            print(f"{name:^8}", end="")
        print()
        
        print("岁数：", end="")
        for age in dayun_ages:
            print(f"{age:^8}", end="")
        print()
        
        print("年份：", end="")
        for year_val in dayun_years:
            print(f"{year_val:^8}", end="")
        print()
        
        print("=" * 70)
        print()
        
        # 关系分析说明
        print("关系分析说明：")
        print("✅ 天干关系：先合再克")
        print("✅ 地支关系：六合→三合→三会→暗合→拱合→相刑→六冲→六破→六害")
        print("✅ 显示位置信息，便于理解干支间的相互作用")
        print("=" * 70)
        
        return True
    
    if __name__ == "__main__":
        test_complete_bazi_analysis()
        
except ImportError as e:
    print(f"请先安装lunar-python库：pip install lunar-python")
    print(f"错误信息：{e}")
    sys.exit(1)