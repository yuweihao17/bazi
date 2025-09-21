#!/usr/bin/env python3
"""
测试1974年案例的大运计算功能
使用1974年10月13日6时出生的女性作为测试案例
"""

import sys
import os
from datetime import datetime

# 添加当前目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# 导入主程序的函数
import importlib.util
spec = importlib.util.spec_from_file_location("main", "2.py")
if spec and spec.loader:
    main_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(main_module)

    # 导入需要的函数
    ensure_lunar_python = main_module.ensure_lunar_python
    calc_bazi_from_solar = main_module.calc_bazi_from_solar
    get_date_info_from_solar = main_module.get_date_info_from_solar
    calculate_dayun_start_time = main_module.calculate_dayun_start_time
    get_dayun_sequence = main_module.get_dayun_sequence
    calculate_dayun_years = main_module.calculate_dayun_years
    display_dayun_result = main_module.display_dayun_result

def test_1974_case():
    """测试1974年案例"""
    print("=" * 60)
    print("           测试1974年案例")
    print("=" * 60)
    
    # 测试数据：1974年10月13日6时，女性
    year, month, day, hour = 1974, 10, 13, 6
    gender = "女"
    
    print(f"测试案例：{year}年{month}月{day}日{hour}时出生，性别：{gender}")
    print("期望：阳年女性，逆着找最近的节令")
    print("距离寒露5天，5/3=1.67，四舍五入应该是2岁起运")
    print("-" * 60)
    
    try:
        # 检查lunar-python库
        if not ensure_lunar_python():
            print("❌ 未安装lunar-python库")
            return
        
        # 计算四柱八字
        year_pillar, month_pillar, day_pillar, hour_pillar = calc_bazi_from_solar(year, month, day, hour)
        print(f"四柱八字：{year_pillar} {month_pillar} {day_pillar} {hour_pillar}")
        
        # 获取公历和农历时间信息
        solar_time, lunar_time = get_date_info_from_solar(year, month, day, hour)
        print(f"公历时间：{solar_time}")
        print(f"农历时间：{lunar_time}")
        
        # 创建出生时间对象
        birth_datetime = datetime(year, month, day, hour)
        
        # 提取年柱天干
        year_stem = year_pillar[0]
        print(f"年柱天干：{year_stem} ({'阳年' if year_stem in ['甲', '丙', '戊', '庚', '壬'] else '阴年'})")
        
        # 计算起运时间
        start_age, start_months, start_days, start_hours, rounded_start_age = calculate_dayun_start_time(
            birth_datetime, gender, year_stem
        )
        print(f"修改后起大运时间（显示）：{start_age}岁{start_months}个月{start_days}天{start_hours}个时辰")
        print(f"四舍五入后年龄（计算用）：{rounded_start_age}岁")
        
        # 获取大运排列
        dayun_list = get_dayun_sequence(month_pillar, gender, year_stem)
        print(f"大运排列：{' '.join(dayun_list)}")
        
        # 计算对应年份
        dayun_years = calculate_dayun_years(year, rounded_start_age)
        print(f"对应年份：{' '.join(map(str, dayun_years))}")
        
        print("-" * 60)
        print("✅ 计算完成")
        
        # 显示完整结果
        display_dayun_result(
            year_pillar, month_pillar, day_pillar, hour_pillar,
            solar_time, lunar_time, gender,
            start_age, start_months, start_days, start_hours,
            dayun_list, dayun_years, rounded_start_age
        )
        
    except Exception as e:
        print(f"❌ 测试过程中出现错误：{e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_1974_case()