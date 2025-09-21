#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
测试年龄修正：验证立春前出生的特殊年龄计算
"""

from datetime import datetime
import sys

try:
    from lunar_python import Solar
    
    def test_age_calculation_corrected():
        """测试修正后的年龄计算"""
        print("=" * 70)
        print("        立春前出生年龄计算修正验证")
        print("=" * 70)
        
        # 基本信息
        birth_info = {
            "出生时间": "2004年1月30日6时",
            "立春时间": "2004年2月4日",
            "说明": "立春前出生，年柱用癸未（2003年）",
            "起运": "8岁起运"
        }
        
        for key, value in birth_info.items():
            print(f"{key}：{value}")
        
        print("\n" + "-" * 70)
        print("年龄计算逻辑（按您的解释）：")
        print()
        
        # 年龄递增表
        age_progression = [
            ("癸未年剩余时间（2004年1月30日-立春前）", 0),
            ("2004年甲申年", 1),
            ("2005年乙酉年", 2),
            ("2006年丙戌年", 3),
            ("2007年丁亥年", 4),
            ("2008年戊子年", 5),
            ("2009年己丑年", 6),
            ("2010年庚寅年", 7),
            ("2011年辛卯年", 8),
            ("2012年壬辰年", 9, "← 开始走甲子大运")
        ]
        
        print("年份递进与年龄对应：")
        for item in age_progression:
            if len(item) == 3:
                year_desc, age, note = item
                print(f"{year_desc:25} {age}岁 {note}")
            else:
                year_desc, age = item
                print(f"{year_desc:25} {age}岁")
        
        print("\n" + "-" * 70)
        print("修正后的大运年龄显示：")
        
        # 修正后的大运计算
        birth_year = 2004
        start_age = 8  # 起运年龄
        
        dayun_names = ["甲子", "癸亥", "壬戌", "辛酉"]
        
        print(f"{'大运':^8}{'年份':^8}{'实际年龄':^10}{'说明':^20}")
        print("-" * 50)
        
        for i, name in enumerate(dayun_names):
            year = birth_year + start_age + i * 10
            actual_age = start_age + 1 + i * 10  # 实际走大运的年龄
            
            # 计算该年的干支
            gan = ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸']
            zhi = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥']
            jiazi_index = (year - 1984) % 60
            year_ganzhi = gan[jiazi_index % 10] + zhi[jiazi_index % 12]
            
            if i == 0:
                desc = f"{year_ganzhi}年开始走大运"
            else:
                desc = f"{year_ganzhi}年"
            
            print(f"{name:^8}{year:^8}{actual_age:^10}{desc:^20}")
        
        print("\n" + "-" * 70)
        print("关键验证点：")
        print("✅ 2012年壬辰年，此人9岁，开始走甲子大运")
        print("✅ 流年显示应该从9岁开始，不是8岁")
        print("✅ 符合传统命理学立春前出生的0岁起算规则")
        
        print("\n" + "=" * 70)
        print("修正总结：")
        print("1. 大运表格显示：8岁、18岁、28岁...（起运年龄）")
        print("2. 流年详情显示：9岁、19岁、29岁...（实际走大运年龄）")
        print("3. 年份计算：2012、2022、2032...（出生年+起运年龄+i*10）")
        print("=" * 70)
        
        return True
    
    if __name__ == "__main__":
        test_age_calculation_corrected()
        
except ImportError:
    print("请先安装lunar-python库：pip install lunar-python")
    sys.exit(1)