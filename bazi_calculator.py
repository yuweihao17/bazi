#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
四柱八字计算器（优化版）

支持公历和农历输入，自动计算四柱八字、大运和流年。
使用 lunar-python 库进行农历转换和八字计算。

功能特点：
- 四柱八字计算
- 大运计算（顺逆行规则）
- 流年查询
- 干支关系分析（包含六柱作用关系）
- 支持公历和农历输入
"""

import sys
from typing import Tuple, Optional, List, Any
from datetime import datetime, timedelta
import bazi_common
import shishen
import changsheng
from ai_analyzer import AIAnalyzer
from lunar_python import Solar, Lunar

# --- 全局常量 ---
DEBUG: bool = False
CHART_COL_WIDTH: int = 14  # 统一所有排盘的列宽

# --- 核心函数 ---

def debug_print(*args: Any, **kwargs: Any) -> None:
    """如果 DEBUG 为 True，则打印调试信息。"""
    if DEBUG:
        print(*args, **kwargs)

# 导入干支关系分析模块
try:
    from ganzhi_relations import analyze_ganzhi_relations
except ImportError:
    def analyze_ganzhi_relations(year_pillar: str, month_pillar: str, day_pillar: str, hour_pillar: str) -> str:
        return "干支关系分析模块未找到"


def read_int(prompt: str, min_value: Optional[int] = None, max_value: Optional[int] = None) -> int:
    """委托公共模块读取并验证整数输入"""
    return bazi_common.read_int(prompt, min_value, max_value)


def read_choice(prompt: str, choices: List[str]) -> str:
    """委托公共模块读取并验证选择输入"""
    return bazi_common.read_choice(prompt, choices)


def get_gender_input() -> str:
    """委托公共模块获取性别输入"""
    return bazi_common.get_gender_input()


def get_24_solar_terms(year: int) -> List[Tuple[str, datetime]]:
    """委托公共模块获取二十四节气时间"""
    return bazi_common.get_24_solar_terms(year)


def calculate_dayun_start_time(birth_datetime: datetime, gender: str, year_stem: str) -> Tuple[int, int, int, int, int]:
    """委托公共模块计算大运起始时间（传递 DEBUG 控制）"""
    return bazi_common.calculate_dayun_start_time(birth_datetime, gender, year_stem, debug=DEBUG)


def get_dayun_sequence(month_pillar: str, gender: str, year_stem: str) -> List[str]:
    """委托公共模块生成大运顺序"""
    return bazi_common.get_dayun_sequence(month_pillar, gender, year_stem)


def calculate_dayun_years(birth_year: int, start_age: int) -> List[int]:
    """委托公共模块计算大运年份"""
    return bazi_common.calculate_dayun_years(birth_year, start_age)


def get_dayun_ages(start_age: int) -> List[int]:
    """委托公共模块获取大运年龄列表"""
    return bazi_common.get_dayun_ages(start_age)


def get_liunian_for_dayun(dayun_ganzhi: str, start_year: int, start_age: int) -> List[Tuple[str, int, int]]:
    """委托公共模块获取指定大运的流年信息"""
    return bazi_common.get_liunian_for_dayun(dayun_ganzhi, start_year, start_age)


def display_liunian_result(dayun_ganzhi: str, liunian_list: List[Tuple[str, int, int]],
                          year_pillar: str, month_pillar: str, day_pillar: str, hour_pillar: str, gender: str) -> None:
    """
    显示大运排盘、流年列表，并附上原局与大运(五柱)的作用关系分析
    """
    print("\n" + "=" * 60)
    print(bazi_common.pad_str_to_center(f"{dayun_ganzhi}大运排盘及流年详情", 60))
    print("=" * 60)
    print()

    # 显示五柱排盘
    pillars_for_chart = [
        {'name': '大运', 'ganzhi': dayun_ganzhi},
        {'name': '年柱', 'ganzhi': year_pillar},
        {'name': '月柱', 'ganzhi': month_pillar},
        {'name': '日柱', 'ganzhi': day_pillar},
        {'name': '时柱', 'ganzhi': hour_pillar}
    ]
    day_master = day_pillar[0]
    _display_bazi_chart(pillars_for_chart, day_master, gender)
    print()

    # 显示流年表格
    print("【十年流年】")
    # 动态调整宽度以适应6个字符的干支
    liunian_col_width = 8
    liunian_ganzhi_str = "".join([bazi_common.pad_str_to_center(g, liunian_col_width) for g, _, _ in liunian_list])
    print(f"流年：{liunian_ganzhi_str}")
    
    years_str = "".join([bazi_common.pad_str_to_center(str(y), liunian_col_width) for _, y, _ in liunian_list])
    print(f"年份：{years_str}")
    
    ages_str = "".join([bazi_common.pad_str_to_center(str(a), liunian_col_width) for _, _, a in liunian_list])
    print(f"岁数：{ages_str}")
    
    table_width = len("年份：") * 2 + len(years_str) # 近似计算宽度
    print("-" * table_width)

    # 分析并显示五柱（原局+大运）关系
    print("\n【原局与大运作用关系】")
    relations = analyze_ganzhi_relations(year_pillar, month_pillar, day_pillar, hour_pillar, dayun_ganzhi)
    print(relations)
    print("-" * table_width)


def _display_bazi_chart(pillars: List[dict], day_master: str, gender: str) -> None:
    """
    显示格式化的八字排盘，包含主星、天干、地支、藏干和十神
    """
    col_width = 12
    label_col_width = 6  # 左侧标签列的宽度
    gender_char = "男" if gender == "男" else "女"
    
    chart_data = []
    max_hidden_stems = 0
    
    for p in pillars:
        gan = p['ganzhi'][0]
        zhi = p['ganzhi'][1]
        
        if p['name'] == '日柱':
            main_star = f'元{gender_char}'
        else:
            main_star = shishen.get_shishen(gan, day_master)
            
        hidden_stems_list = shishen.HIDDEN_STEMS.get(zhi, [])
        hidden_stems_with_shishen = [
            f"{s} {shishen.get_shishen(s, day_master)}" for s in hidden_stems_list
        ]
        max_hidden_stems = max(max_hidden_stems, len(hidden_stems_with_shishen))
        
        chart_data.append({
            'name': p['name'],
            'main_star': main_star,
            'gan': gan,
            'zhi': zhi,
            'hidden': hidden_stems_with_shishen,
            'xing_yun': changsheng.get_changsheng_state(day_master, zhi), # 星运
            'zi_zuo': changsheng.get_changsheng_state(gan, zhi) # 自坐
        })
        
    def print_row(data_key: str, label: str):
        row_items = [bazi_common.pad_str_to_center(d[data_key], col_width) for d in chart_data]
        
        # 手动计算标签填充，以实现精确对齐
        label_width = bazi_common.get_str_display_width(label)
        padding = ' ' * max(0, label_col_width - label_width)
        padded_label = label + padding
        
        print(f"{padded_label}{''.join(row_items)}")

    total_width = label_col_width + col_width * len(chart_data)
    print("-" * total_width)
    
    print_row('name', '') # 柱名
    print_row('main_star', '主星')
    print_row('gan', '天干')
    print_row('zhi', '地支')
    
    print("-" * total_width)

    for i in range(max_hidden_stems):
        row_items = []
        for d in chart_data:
            item = d['hidden'][i] if i < len(d['hidden']) else ""
            row_items.append(bazi_common.pad_str_to_center(item, col_width))
        
        label = "藏干" if i == 0 else ""
        
        # 手动计算标签填充
        label_width = bazi_common.get_str_display_width(label)
        padding = ' ' * max(0, label_col_width - label_width)
        padded_label = label + padding
        
        print(f"{padded_label}{''.join(row_items)}")
    
    # 增加星运和自坐
    print_row('xing_yun', '星运')
    print_row('zi_zuo', '自坐')
    
    print("-" * total_width)


def liunian_query_loop(analyzer: AIAnalyzer, dayun_list: List[str], dayun_years: List[int], rounded_start_age: int,
                       year_pillar: str, month_pillar: str, day_pillar: str, hour_pillar: str, gender: str) -> None:
    """流年查询的交互式循环"""
    print("\n" + "-" * 50)
    print("大运和流年分析选项：")
    print("你可以选择一个大运进行整体分析，或者在选定大运后，进一步分析其中的具体流年。")
    print(f"可查询的大运：{' '.join(dayun_list)}")
    print("输入 'q' 或 'quit' 退出")
    print("-" * 50)
    
    current_dayun = None
    current_liunian_list = None
    
    while True:
        try:
            # 阶段一：选择大运
            if current_dayun is None:
                user_input = input("\n请输入要查询的大运干支：").strip()
                if user_input.lower() in ['q', 'quit', '退出']:
                    print("查询已退出。")
                    break
                
                if user_input in dayun_list:
                    current_dayun = user_input
                    dayun_index = dayun_list.index(current_dayun)
                    start_year = dayun_years[dayun_index]
                    actual_start_age = rounded_start_age + dayun_index * 10
                    current_liunian_list = get_liunian_for_dayun(current_dayun, start_year, actual_start_age)
                    
                    # 首先显示所有信息
                    display_liunian_result(current_dayun, current_liunian_list, year_pillar, month_pillar, day_pillar, hour_pillar, gender)

                    # 然后进行AI解读
                    analyzer.get_interpretation(
                        analysis_type="dayun_yingxiang", 
                        data={
                            "gender": gender,
                            "year_pillar": year_pillar,
                            "month_pillar": month_pillar,
                            "day_pillar": day_pillar,
                            "hour_pillar": hour_pillar,
                            "dayun_pillar": current_dayun,
                            "dayun_start_age": actual_start_age,
                            "dayun_end_age": actual_start_age + 9,
                            "start_year": start_year,
                            "end_year": start_year + 9,
                            "dayun_relations": analyze_ganzhi_relations(year_pillar, month_pillar, day_pillar, hour_pillar, current_dayun),
                            
                            # 依赖项所需的数据
                            "day_master": day_pillar[0],
                            "yuanju_relations": analyze_ganzhi_relations(year_pillar, month_pillar, day_pillar, hour_pillar)
                        },
                        dependencies=["bazi_yuanju"]
                    )
                else:
                    print(f"❌ 请输入有效的大运干支：{' '.join(dayun_list)}")
                    continue

            # 阶段二：在大运内选择操作
            print("\n请选择操作：")
            print("1. 查询当前大运内的具体流年")
            print("2. 查询另一个大运")
            print("3. 退出")
            
            choice = input("请输入选项 (1/2/3): ").strip()

            if choice == '1':
                if not current_liunian_list:
                    print("错误：无流年信息可查。")
                    continue
                    
                liunian_ganzhi_options = [item[0] for item in current_liunian_list]
                print(f"\n可查询的流年: {' '.join(liunian_ganzhi_options)}")
                liunian_input = input("请输入要分析的流年干支 (输入'b'返回): ").strip()
                    
                if liunian_input.lower() == 'b':
                    continue
                    
                if liunian_input in liunian_ganzhi_options:
                    # 查找选定流年的详细信息
                    selected_liunian_info = next((item for item in current_liunian_list if item[0] == liunian_input), None)
                    if not selected_liunian_info:
                        print("❌ 内部错误：无法找到流年信息。")
                        continue
                    
                    liunian_ganzhi, liunian_year, liunian_age = selected_liunian_info
                    dayun_index = dayun_list.index(current_dayun)
                    dayun_start_age = rounded_start_age + dayun_index * 10

                    title = f"六柱（原局+大运+流年）作用关系分析"
                    subtitle = f"大运[{current_dayun}] - 流年[{liunian_ganzhi}]"
                    total_width = (CHART_COL_WIDTH * 6) + 6 # 6柱 + 左侧标签宽度
                    
                    print("\n" + "=" * total_width)
                    print(bazi_common.pad_str_to_center(title, total_width))
                    print(bazi_common.pad_str_to_center(subtitle, total_width))
                    print("=" * total_width)
                    
                    # 显示包含流年和大运的六柱排盘
                    pillars_for_chart = [
                        {'name': '流年', 'ganzhi': liunian_ganzhi},
                        {'name': '大运', 'ganzhi': current_dayun},
                        {'name': '年柱', 'ganzhi': year_pillar},
                        {'name': '月柱', 'ganzhi': month_pillar},
                        {'name': '日柱', 'ganzhi': day_pillar},
                        {'name': '时柱', 'ganzhi': hour_pillar}
                    ]
                    day_master = day_pillar[0]
                    _display_bazi_chart(pillars_for_chart, day_master, gender)
                    print()

                    # 分析六柱关系
                    relations = analyze_ganzhi_relations(year_pillar, month_pillar, day_pillar, hour_pillar, current_dayun, liunian_ganzhi)
                    print(relations)
                    print("=" * total_width)

                    # AI 解读流年
                    analyzer.get_interpretation(
                        analysis_type="liunian_fenxi",
                        data={
                            # 通用数据
                            "gender": gender,
                            "year_pillar": year_pillar,
                            "month_pillar": month_pillar,
                            "day_pillar": day_pillar,
                            "hour_pillar": hour_pillar,
                            "day_master": day_master,

                            # 原局依赖数据
                            "yuanju_relations": analyze_ganzhi_relations(year_pillar, month_pillar, day_pillar, hour_pillar),

                            # 大运依赖数据
                            "dayun_pillar": current_dayun,
                            "dayun_start_age": dayun_start_age,
                            "dayun_end_age": dayun_start_age + 9,
                            "start_year": dayun_years[dayun_index],
                            "end_year": dayun_years[dayun_index] + 9,
                            "dayun_relations": analyze_ganzhi_relations(year_pillar, month_pillar, day_pillar, hour_pillar, current_dayun),

                            # 当前流年分析所需数据
                            "liunian_pillar": liunian_ganzhi,
                            "liunian_year": liunian_year,
                            "liunian_age": liunian_age,
                            "liunian_relations": relations
                        },
                        dependencies=["bazi_yuanju", "dayun_yingxiang"]
                    )
                else:
                    print("❌ 无效的流年输入。")
            
            elif choice == '2':
                # 重置，返回大运选择阶段
                current_dayun = None
                current_liunian_list = None
                print("\n" + "-" * 50)
                print(f"可查询的大运：{' '.join(dayun_list)}")
                print("-" * 50)
                        
            elif choice == '3':
                print("查询已退出。")
                break
            else:
                print("❌ 无效选项，请输入 1, 2, 或 3。")

        except (KeyboardInterrupt, EOFError):
            print("\n查询已退出。")
            break


def display_dayun_result(analyzer: AIAnalyzer, year_pillar: str, month_pillar: str, day_pillar: str, hour_pillar: str,
                        solar_time: str, lunar_time: str, gender: str, 
                        start_age: int, start_months: int, start_days: int, start_hours: int,
                        dayun_list: List[str], dayun_years: List[int], rounded_start_age: int) -> None:
    """显示计算结果和大运信息"""
    title = "四柱八字及大运计算结果"
    total_width = (CHART_COL_WIDTH * 4) + 6 # 4柱 + 左侧标签宽度

    print("\n" + "=" * total_width)
    print(bazi_common.pad_str_to_center(title, total_width))
    print("=" * total_width)
    
    print(bazi_common.pad_str(f"公历时间：{solar_time}", total_width))
    print(bazi_common.pad_str(f"农历时间：{lunar_time}", total_width))
    print(bazi_common.pad_str(f"性别：{gender}", total_width))
    
    # 使用新的排盘函数显示四柱
    pillars_for_chart = [
        {'name': '年柱', 'ganzhi': year_pillar},
        {'name': '月柱', 'ganzhi': month_pillar},
        {'name': '日柱', 'ganzhi': day_pillar},
        {'name': '时柱', 'ganzhi': hour_pillar}
    ]
    day_master = day_pillar[0]
    _display_bazi_chart(pillars_for_chart, day_master, gender)
    
    # 添加原局干支关系分析
    print("\n【原局作用关系】")
    relations = analyze_ganzhi_relations(year_pillar, month_pillar, day_pillar, hour_pillar)
    print(relations)
    print("-" * total_width)

    # AI 解读原局
    analyzer.get_interpretation("bazi_yuanju", {
        "gender": gender,
        "year_pillar": year_pillar,
        "month_pillar": month_pillar,
        "day_pillar": day_pillar,
        "day_master": day_master,
        "hour_pillar": hour_pillar,
        "yuanju_relations": relations
    })
    
    print(bazi_common.pad_str(f"起大运时间：{start_age}岁{start_months}个月{start_days}天{start_hours}个时辰", total_width))
    print(bazi_common.pad_str(f"实际起运年份：{dayun_years[0]} 年，实际起运年龄：{rounded_start_age} 岁", total_width))
    print("-" * total_width)
    print("八部大运排列：")
    print()
    
    # 显示大运表格（仅显示8个）
    headers = dayun_list[:8]
    ages = bazi_common.get_dayun_ages(rounded_start_age)[:8]
    years = dayun_years[:8]
    
    # 使用固定宽度格式化，确保对齐
    headers_str = "".join([bazi_common.pad_str_to_center(h, CHART_COL_WIDTH // 2) for h in headers])
    print(f"大运：{headers_str}")
    
    ages_str = "".join([bazi_common.pad_str_to_center(str(a), CHART_COL_WIDTH // 2) for a in ages])
    print(f"岁数：{ages_str}")
    
    years_str = "".join([bazi_common.pad_str_to_center(str(y), CHART_COL_WIDTH // 2) for y in years])
    print(f"年份：{years_str}")
    
    print("=" * total_width)

    # AI 解读人生大运趋势
    day_master = day_pillar[0]
    dayun_list_str = "\n".join([f"- {age}岁起: {ganzhi} ({year}年开始)" 
                                for ganzhi, age, year in zip(headers, ages, years)])

    analyzer.get_interpretation(
        analysis_type="bazi_dayun_trend", 
        data={
            "gender": gender,
            "year_pillar": year_pillar,
            "month_pillar": month_pillar,
            "day_pillar": day_pillar,
            "day_master": day_master,
            "hour_pillar": hour_pillar,
            "dayun_list_str": dayun_list_str,
            # 为依赖项添加数据
            "yuanju_relations": relations
        },
        dependencies=["bazi_yuanju"]
    )


def calc_bazi_from_solar(year: int, month: int, day: int, hour: int) -> Tuple[str, str, str, str]:
    """
    从公历日期计算四柱八字
    """
    try:
        solar = Solar.fromYmdHms(year, month, day, hour, 0, 0)
        lunar = solar.getLunar()
        ec = lunar.getEightChar()
        return ec.getYear(), ec.getMonth(), ec.getDay(), ec.getTime()
    except Exception as e:
        raise ValueError(f"公历日期无效: {year}-{month:02d}-{day:02d} {hour:02d}:00") from e


def get_date_info_from_solar(year: int, month: int, day: int, hour: int) -> Tuple[str, str]:
    """从公历获取日期信息，包括农历"""
    solar = Solar.fromYmdHms(year, month, day, hour, 0, 0)
    lunar = solar.getLunar()
    
    solar_str = f"{year}年{month}月{day}日 {hour:02d}:00"
    lunar_str = bazi_common.format_lunar_dt_from_object(lunar, hour)
    
    return solar_str, lunar_str


def calc_bazi_from_lunar(year: int, month: int, day: int, hour: int) -> Tuple[str, str, str, str]:
    """
    从农历日期计算四柱八字（闰月由负数月份表示）
    """
    try:
        lunar = Lunar.fromYmdHms(year, month, day, hour, 0, 0)
        ec = lunar.getEightChar()
        return ec.getYear(), ec.getMonth(), ec.getDay(), ec.getTime()
    except Exception as e:
        is_leap = month < 0
        month_abs = abs(month)
        leap_str = "闰" if is_leap else ""
        error_msg = (
            f"农历日期无效: {year}年{leap_str}{month_abs}月{day}日。"
            "请检查该月份是否存在此日期（例如，是否为小月）。"
        )
        raise ValueError(error_msg) from e


def calc_bazi_from_lunar_auto(year: int, month: int, day: int, hour: int) -> Tuple[str, str, str, str]:
    """
    自动判断闰月并计算四柱八字
    """
    try:
        from lunar_python import LunarYear  # type: ignore
        leap_month = 0
        try:
            leap_month = LunarYear.fromYear(year).getLeapMonth()
        except Exception:
            leap_month = 0
        # 若当年无闰月，或闰月与输入月份不同，则按非闰月处理
        if leap_month == 0 or leap_month != month:
            return calc_bazi_from_lunar(year, month, day, hour)
        # 若当年该月为闰月：优先尝试非闰月，不存在则尝试闰月
        try:
            return calc_bazi_from_lunar(year, month, day, hour)
        except ValueError:
            return calc_bazi_from_lunar(year, month, day, hour)
    except ImportError:
        # 兼容旧版 lunar_python（无 LunarYear）
        try:
            return calc_bazi_from_lunar(year, month, day, hour)
        except ValueError:
            return calc_bazi_from_lunar(year, month, day, hour)


def get_date_info_from_lunar(year: int, month: int, day: int, hour: int) -> Tuple[str, str]:
    """从农历获取日期信息，包括公历"""
    lunar = Lunar.fromYmdHms(year, month, day, hour, 0, 0)
    solar = lunar.getSolar()
    
    solar_str = f"{solar.getYear()}年{solar.getMonth()}月{solar.getDay()}日 {hour:02d}:00"
    lunar_str = bazi_common.format_lunar_dt_from_object(lunar, hour)
    
    return solar_str, lunar_str


def get_solar_input() -> Tuple[int, int, int, int]:
    """委托公共模块获取公历输入"""
    return bazi_common.get_solar_input()


def get_lunar_input() -> Tuple[int, int, int, int]:
    """委托公共模块获取农历输入"""
    return bazi_common.get_lunar_input()


def display_banner() -> None:
    """委托公共模块显示程序横幅"""
    bazi_common.display_banner()


def get_bazi_input_and_find_dates() -> Optional[Tuple[datetime, str]]:
    """
    获取用户输入的四柱八字，并在1800-2100年范围内查找所有匹配的日期。
    返回用户选择的日期时间和性别。
    """
    print("\n请输入四柱八字进行反查（例如：年柱输入“癸卯”，月柱输入“甲子”等）")
    
    # 地支与小时的映射关系 (取小时范围的中间值)
    ZHI_TO_HOUR = {
        '子': 0, '丑': 2, '寅': 4, '卯': 6, '辰': 8, '巳': 10,
        '午': 12, '未': 14, '申': 16, '酉': 18, '戌': 20, '亥': 22
    }
    
    # 获取并验证输入
    while True:
        year_pillar = input("请输入年柱：").strip()
        if year_pillar not in bazi_common.JIAZI_CYCLE:
            print(f"❌ 年柱输入错误，请输入有效的干支组合。")
            continue
        break
        
    while True:
        month_pillar = input("请输入月柱：").strip()
        if month_pillar not in bazi_common.JIAZI_CYCLE:
            print(f"❌ 月柱输入错误，请输入有效的干支组合。")
            continue
        break

    while True:
        day_pillar = input("请输入日柱：").strip()
        if day_pillar not in bazi_common.JIAZI_CYCLE:
            print(f"❌ 日柱输入错误，请输入有效的干支组合。")
            continue
        break

    while True:
        hour_pillar = input("请输入时柱：").strip()
        if hour_pillar not in bazi_common.JIAZI_CYCLE:
            print(f"❌ 时柱输入错误，请输入有效的干支组合。")
            continue
        if hour_pillar[1] not in ZHI_TO_HOUR:
            print(f"❌ 时柱地支“{hour_pillar[1]}”无法识别，请输入有效的时柱。")
            continue
        break

    target_hour = ZHI_TO_HOUR[hour_pillar[1]]
    
    print("\n正在优化算法并在 1800-2100 年间查找匹配的日期，请稍候...")
    
    found_dates = []
    start_date = datetime(1800, 1, 1)
    end_date = datetime(2100, 12, 31)

    # 优化算法：
    # 1. 先找到第一个日柱匹配的公历日期作为起点
    first_match_date = None
    search_date = start_date
    while search_date <= end_date:
        try:
            # 使用中午12点来确定当天的日柱，避免跨日子时(23点)的边界问题
            solar_day_check = Solar.fromYmdHms(search_date.year, search_date.month, search_date.day, 12, 0, 0)
            day_gz = solar_day_check.getLunar().getEightChar().getDay()
            if day_gz == day_pillar:
                first_match_date = search_date
                break
        except Exception:
            pass  # 忽略无效日期
        search_date += timedelta(days=1)

    if first_match_date is None:
        print("\n在 1800-2100 年间未找到任何匹配日柱的日期。")
        return None

    # 2. 从第一个匹配日开始，以60天为步长进行“跳跃”搜索
    current_date = first_match_date
    while current_date <= end_date:
        try:
            # 在这个日柱正确的日期，精确检查所有四柱
            solar = Solar.fromYmdHms(current_date.year, current_date.month, current_date.day, target_hour, 0, 0)
            ec = solar.getLunar().getEightChar()
            
            calc_year = ec.getYear()
            calc_month = ec.getMonth()
            calc_day = ec.getDay()
            calc_hour = ec.getTime()
            
            # 进行全匹配校验
            if (calc_year == year_pillar and
                calc_month == month_pillar and
                calc_day == day_pillar and
                calc_hour == hour_pillar):
                found_dates.append(solar)
                
        except Exception:
            pass # 忽略计算错误
        
        # 直接跳到60天后，那天的日柱必然相同
        current_date += timedelta(days=60)
        
    if not found_dates:
        print("\n在 1800-2100 年间未找到与该八字匹配的日期。")
        return None
        
    print("\n" + "=" * 50)
    print("        找到以下匹配的时间点")
    print("=" * 50)
    for i, solar_obj in enumerate(found_dates):
        lunar_obj = solar_obj.getLunar()
        solar_str = solar_obj.toYmdHms()
        lunar_str = bazi_common.format_lunar_dt_from_object(lunar_obj, solar_obj.getHour())
        print(f"[{i+1}] 公历: {solar_str} | 农历: {lunar_str}")
    print("=" * 50)

    # 让用户选择
    while True:
        try:
            choice_idx = read_int(f"请选择一个时间点进行后续分析 (1-{len(found_dates)}): ", 1, len(found_dates))
            selected_solar = found_dates[choice_idx - 1]
            
            # 获取性别信息
            gender = get_gender_input()
            
            birth_dt = datetime(
                selected_solar.getYear(),
                selected_solar.getMonth(),
                selected_solar.getDay(),
                selected_solar.getHour()
            )
            return birth_dt, gender

        except (ValueError, IndexError):
            print("❌ 无效输入，请输入列表中的数字编号。")


def main() -> None:
    """
    程序主入口：
    1. 检查依赖。
    2. 显示欢迎横幅。
    3. 根据用户选择的模式（公历、农历、八字反查）获取八字信息。
    4. 计算并显示详细的排盘、大运、流年及 AI 解读。
    """
    bazi_common.ensure_dependencies([
        ("lunar_python", "pip install lunar-python>=1.2.13"),
        ("wcwidth", "pip install wcwidth"),
        ("openai", "pip install openai")
    ])
    
    try:
        analyzer = AIAnalyzer() # 创建 AI 分析器实例
        display_banner()

        while True: # 主循环，允许重新开始
            analyzer.reset_history() # 为每次新的排盘重置AI对话历史

            birth_datetime = None
            gender = None
            year_pillar, month_pillar, day_pillar, hour_pillar = "", "", "", ""
            solar_time, lunar_time = "", ""

            mode = read_choice("\n请选择输入方式（g=公历, n=农历, b=八字反查）：", ["g", "n", "b"])

            if mode == 'b':
                result = get_bazi_input_and_find_dates()
                if result is None:
                    sys.exit(0) # 未找到或用户退出
                
                birth_datetime, gender = result
                
                # 从反查得到的日期时间直接获取所有信息
                year, month, day, hour = birth_datetime.year, birth_datetime.month, birth_datetime.day, birth_datetime.hour
                year_pillar, month_pillar, day_pillar, hour_pillar = calc_bazi_from_solar(year, month, day, hour)
                solar_time, lunar_time = get_date_info_from_solar(year, month, day, hour)
            else:
                # 原有的公历/农历输入逻辑
                gender = get_gender_input()
                if mode == "g":
                    year, month, day, hour = get_solar_input()
                    try:
                        year_pillar, month_pillar, day_pillar, hour_pillar = calc_bazi_from_solar(year, month, day, hour)
                        solar_time, lunar_time = get_date_info_from_solar(year, month, day, hour)
                        birth_datetime = datetime(year, month, day, hour)
                    except ValueError as e:
                        print(f"\n❌ 错误：{e}")
                        sys.exit(1)
                else: # mode == "n"
                    year, month, day, hour = get_lunar_input()
                    try:
                        year_pillar, month_pillar, day_pillar, hour_pillar = calc_bazi_from_lunar_auto(year, month, day, hour)
                        solar_time, lunar_time = get_date_info_from_lunar(year, month, day, hour)
                        # 从农历转为公历获取datetime对象
                        lunar = Lunar.fromYmdHms(year, month, day, hour, 0, 0)
                        solar = lunar.getSolar()
                        birth_datetime = datetime(solar.getYear(), solar.getMonth(), solar.getDay(), hour)
                    except ValueError as e:
                        print(f"\n❌ 错误：{e}")
                        sys.exit(1)
            
            if birth_datetime is None or gender is None:
                print("\n❌ 未能获取到有效的出生日期或性别，程序终止。")
                sys.exit(1)

            # 计算大运信息
            try:
                # 提取年柱天干
                year_stem = year_pillar[0]
                
                # 计算起运时间
                start_age, start_months, start_days, start_hours, rounded_start_age = calculate_dayun_start_time(
                    birth_datetime, gender, year_stem
                )
                
                # 获取大运排列
                dayun_list = get_dayun_sequence(month_pillar, gender, year_stem)
                
                # 计算对应年份（传统算法：出生年为0岁）
                dayun_years = calculate_dayun_years(birth_datetime.year, rounded_start_age)
                
                # 显示结果
                display_dayun_result(
                    analyzer, year_pillar, month_pillar, day_pillar, hour_pillar,
                    solar_time, lunar_time, gender,
                    start_age, start_months, start_days, start_hours,
                    dayun_list, dayun_years, rounded_start_age
                )
                
                # 流年查询功能
                liunian_query_loop(analyzer, dayun_list, dayun_years, rounded_start_age, year_pillar, month_pillar, day_pillar, hour_pillar, gender)
                
                # 询问是否继续
                if bazi_common.read_choice("\n是否要排一个新的八字？(y/n): ", ['y', 'n']).lower() != 'y':
                    print("感谢使用，再见！")
                    break # 退出主循环

            except Exception as e:
                print(f"\n❌ 大运计算错误：{e}")
                # 即使大运计算失败，也显示基本八字信息
                print("\n" + "=" * 40)
                print("        四柱八字结果")
                print("=" * 40)
                print(f"公历时间：{solar_time}")
                print(f"农历时间：{lunar_time}")
                print(f"性别：{gender}")
                print("-" * 40)
                print(f"年柱：{year_pillar}")
                print(f"月柱：{month_pillar}")
                print(f"日柱：{day_pillar}")
                print(f"时柱：{hour_pillar}")
                print("-" * 40)
                print(f"四柱八字：{year_pillar} {month_pillar} {day_pillar} {hour_pillar}")
                print("=" * 40)
        
    except KeyboardInterrupt:
        print("\n\n程序已退出")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ 程序出现意外错误：{e}")
        # 询问是否重试
        if bazi_common.read_choice("\n程序出现意外错误，是否要重新开始？(y/n): ", ['y', 'n']).lower() == 'y':
            main() # 递归调用 main，不推荐，但对于简单脚本可行
        else:
            sys.exit(1)


if __name__ == "__main__":
    main()