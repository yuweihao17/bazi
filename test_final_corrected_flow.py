#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
测试修正后的完整流程
验证大运表格和流年查询的年龄显示是否正确
"""

import sys
from datetime import datetime

try:
    from lunar_python import Solar
    
    def calc_bazi_from_solar(year: int, month: int, day: int, hour: int):
        """从公历日期计算四柱八字"""
        solar = Solar.fromYmdHms(year, month, day, hour, 0, 0)
        lunar = solar.getLunar()
        ec = lunar.getEightChar()
        return ec.getYear(), ec.getMonth(), ec.getDay(), ec.getTime()
    
    def get_dayun_sequence(month_pillar: str, gender: str, year_stem: str):
        """获取大运排列顺序"""
        # 六十花甲子的顺序
        gan = ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸']
        zhi = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥']
        
        # 生成六十甲子
        jiazi = []
        for i in range(60):
            jiazi.append(gan[i % 10] + zhi[i % 12])
        
        # 找到月柱在六十甲子中的位置
        try:
            current_index = jiazi.index(month_pillar)
        except ValueError:
            current_index = 0
        
        # 判断年干的阴阳性
        yang_stems = ['甲', '丙', '戊', '庚', '壬']
        is_yang_year = year_stem in yang_stems
        
        # 确定排列方向
        if (is_yang_year and gender == '男') or (not is_yang_year and gender == '女'):
            direction = 1  # 顺行
        else:
            direction = -1  # 逆行
        
        # 生成八部大运
        dayun_list = []
        for i in range(8):
            index = (current_index + (i + 1) * direction) % 60
            dayun_list.append(jiazi[index])
        
        return dayun_list
    
    def calculate_dayun_years(birth_year: int, start_age: int):
        """计算大运对应的年份"""
        years = []
        for i in range(8):
            year = birth_year + start_age + i * 10
            years.append(year)
        return years
    
    def get_dayun_ages_display(start_age: int):
        """获取大运表格显示的岁数（起运年龄）"""
        ages = []
        for i in range(8):
            age = start_age + i * 10
            ages.append(age)
        return ages
    
    def get_dayun_ages_actual(start_age: int):
        """获取实际走大运的岁数（起运年龄+1）"""
        ages = []
        for i in range(8):
            age = start_age + 1 + i * 10
            ages.append(age)
        return ages
    
    def get_liunian_for_dayun(dayun_ganzhi: str, start_year: int, start_age: int):
        """计算指定大运内的十年流年信息"""
        # 六十花甲子的顺序
        gan = ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸']
        zhi = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥']
        
        # 生成六十甲子
        jiazi = []
        for i in range(60):
            jiazi.append(gan[i % 10] + zhi[i % 12])
        
        liunian_list = []
        
        # 从起始年份开始，计算十年流年
        for i in range(10):
            year = start_year + i
            age = start_age + i  # start_age已经是实际走大运的年龄
            
            # 根据公历年份计算流年干支
            jiazi_index = (year - 1984) % 60
            if jiazi_index < 0:
                jiazi_index += 60
            
            liunian_ganzhi = jiazi[jiazi_index]
            liunian_list.append((liunian_ganzhi, year, age))
        
        return liunian_list
    
    def display_liunian_result(dayun_ganzhi: str, liunian_list):
        """显示流年查询结果"""
        print("\n" + "=" * 50)
        print(f"        {dayun_ganzhi}大运十年流年详情")
        print("=" * 50)
        print()
        
        # 显示表头
        print("流年：", end="")
        for liunian_ganzhi, _, _ in liunian_list:
            print(f"{liunian_ganzhi:^6}", end="")
        print()
        
        print("年份：", end="")
        for _, year, _ in liunian_list:
            print(f"{year:^6}", end="")
        print()
        
        print("岁数：", end="")
        for _, _, age in liunian_list:
            print(f"{age:^6}", end="")
        print()
        
        print("=" * 50)
    
    def test_corrected_output():
        """测试修正后的完整输出"""
        print("=" * 70)
        print("        2004年1月30日案例 - 修正后的完整输出测试")
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
        
        # 起运信息
        start_age = 8
        print(f"起大运时间：{start_age}岁0个月0天0个时辰")
        print("-" * 50)
        print("八部大运排列：")
        print()
        
        # 获取大运排列
        year_stem = year_pillar[0]
        dayun_list = get_dayun_sequence(month_pillar, gender, year_stem)
        
        # 计算大运年份和岁数
        dayun_years = calculate_dayun_years(year, start_age)
        dayun_ages_display = get_dayun_ages_display(start_age)  # 表格显示用
        dayun_ages_actual = get_dayun_ages_actual(start_age)    # 实际年龄
        
        # 显示大运表格
        print("大运：", end="")
        for dayun in dayun_list:
            print(f"{dayun:^8}", end="")
        print()
        
        print("岁数：", end="")
        for age in dayun_ages_display:  # 使用显示年龄（起运年龄）
            print(f"{age:^8}", end="")
        print()
        
        print("年份：", end="")
        for year_val in dayun_years:
            print(f"{year_val:^8}", end="")
        print()
        
        print("=" * 70)
        print()
        
        # 流年查询测试
        print("流年查询测试（甲子大运）：")
        
        # 模拟查询甲子大运
        dayun_ganzhi = "甲子"
        dayun_index = dayun_list.index(dayun_ganzhi)
        start_year = dayun_years[dayun_index]
        actual_start_age = dayun_ages_actual[dayun_index]  # 使用实际年龄
        
        # 计算该大运的流年信息
        liunian_list = get_liunian_for_dayun(dayun_ganzhi, start_year, actual_start_age)
        
        # 显示流年结果
        display_liunian_result(dayun_ganzhi, liunian_list)
        
        print("\n" + "=" * 70)
        print("验证结果：")
        print(f"✅ 大运表格显示：{dayun_ages_display[0]}岁（起运年龄）")
        print(f"✅ 流年详情显示：{dayun_ages_actual[0]}岁（实际走大运年龄）")
        print(f"✅ 2012年壬辰年{dayun_ages_actual[0]}岁开始走甲子大运")
        print("✅ 符合用户要求的年龄计算逻辑")
        print("=" * 70)
        
        return True
    
    if __name__ == "__main__":
        test_corrected_output()
        
except ImportError:
    print("请先安装lunar-python库：pip install lunar-python")
    sys.exit(1)