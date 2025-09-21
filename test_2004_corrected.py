#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
测试2004年1月30日6时案例的修正结果
验证传统命理学0岁起算，从年柱年份开始计算大运
"""

from datetime import datetime
import sys

# 导入主程序的函数
try:
    from lunar_python import Solar
    
    def calc_bazi_from_solar(year: int, month: int, day: int, hour: int):
        """从公历日期计算四柱八字"""
        solar = Solar.fromYmdHms(year, month, day, hour, 0, 0)
        lunar = solar.getLunar()
        ec = lunar.getEightChar()
        return ec.getYear(), ec.getMonth(), ec.getDay(), ec.getTime()
    
    def get_year_from_ganzhi(year_ganzhi: str, reference_year: int) -> int:
        """根据年柱干支和参考年份，计算年柱对应的具体年份"""
        # 六十花甲子的顺序
        gan = ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸']
        zhi = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥']
        
        # 生成六十甲子
        jiazi = []
        for i in range(60):
            jiazi.append(gan[i % 10] + zhi[i % 12])
        
        # 找到年柱干支在六十甲子中的位置
        try:
            ganzhi_index = jiazi.index(year_ganzhi)
        except ValueError:
            # 如果找不到，返回参考年份
            return reference_year
        
        # 以甲子年1984年为基准，计算年柱对应的年份
        # 找到离参考年份最近的该干支年份
        base_year = 1984  # 甲子年
        
        # 计算参考年份对应的干支索引
        ref_index = (reference_year - base_year) % 60
        if ref_index < 0:
            ref_index += 60
        
        # 计算干支差值
        diff = ganzhi_index - ref_index
        
        # 找到最接近的年份（可能是前一年或后一年）
        candidate_years = [
            reference_year + diff,
            reference_year + diff - 60,
            reference_year + diff + 60
        ]
        
        # 选择最接近参考年份的年份
        closest_year = min(candidate_years, key=lambda x: abs(x - reference_year))
        
        return closest_year
    
    def calculate_dayun_years_corrected(year_ganzhi: str, reference_year: int, start_age: int):
        """计算大运对应的年份（修正版：使用年柱年份，传统0岁起）"""
        # 先获取年柱对应的具体年份
        year_pillar_year = get_year_from_ganzhi(year_ganzhi, reference_year)
        
        years = []
        for i in range(8):  # 只显示8个大运
            # 传统算法：年柱年份为0岁，所以实际年份 = 年柱年份 + 年龄
            year = year_pillar_year + start_age + i * 10
            years.append(year)
        return years, year_pillar_year
    
    def test_2004_case():
        """测试2004年1月30日6时的案例"""
        print("=" * 60)
        print("测试案例：2004年1月30日6时（男性）")
        print("=" * 60)
        
        # 基本信息
        year, month, day, hour = 2004, 1, 30, 6
        
        # 计算八字
        year_pillar, month_pillar, day_pillar, hour_pillar = calc_bazi_from_solar(year, month, day, hour)
        
        print(f"公历时间：{year}年{month}月{day}日 {hour:02d}:00")
        print(f"四柱八字：{year_pillar} {month_pillar} {day_pillar} {hour_pillar}")
        print()
        
        # 起运信息（已知结果）
        start_age = 8  # 8岁起运
        print(f"起运年龄：{start_age}岁")
        print()
        
        # 原来的计算方法（用公历年份）
        print("原来的计算方法（用公历年份2004年）：")
        old_years = []
        for i in range(8):
            year_val = 2004 + start_age + i * 10
            old_years.append(year_val)
        print(f"大运年份：{old_years}")
        print()
        
        # 修正后的计算方法（用年柱对应年份）
        print("修正后的计算方法（用年柱对应年份）：")
        new_years, year_pillar_year = calculate_dayun_years_corrected(year_pillar, year, start_age)
        print(f"年柱 {year_pillar} 对应的年份：{year_pillar_year}年")
        print(f"大运年份：{new_years}")
        print()
        
        # 对比说明
        print("对比分析：")
        print(f"公历出生年：{year}年")
        print(f"年柱对应年：{year_pillar_year}年（立春前，用前一年的干支）")
        print(f"差异：{year - year_pillar_year}年")
        print()
        
        print("修正结果：")
        print(f"2004年出生，但年柱是{year_pillar}（{year_pillar_year}年）")
        print(f"按传统算法，{year_pillar_year}年为0岁")
        print(f"8岁起运，应该在{year_pillar_year + 8} = {new_years[0]}年开始走甲子大运")
        print(f"而不是{old_years[0]}年")
        
        return new_years[0] == 2012  # 期望第一个大运年份是2012年
    
    # 运行测试
    if __name__ == "__main__":
        try:
            result = test_2004_case()
            print("\n" + "=" * 60)
            if result:
                print("✅ 测试通过！修正结果正确：2012年开始走甲子大运")
            else:
                print("❌ 测试失败！修正结果不正确")
            print("=" * 60)
        except Exception as e:
            print(f"测试过程中出现错误：{e}")
            
except ImportError:
    print("请先安装lunar-python库：pip install lunar-python")
    sys.exit(1)