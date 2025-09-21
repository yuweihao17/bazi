#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
四柱八字计算器（修复版）

支持公历和农历输入，自动计算四柱八字。
使用 lunar-python 库进行农历转换和八字计算。
"""

import sys
from typing import Tuple, Optional, List
from datetime import datetime, timedelta

# 导入干支关系分析模块
try:
    from ganzhi_relations import analyze_ganzhi_relations
except ImportError:
    def analyze_ganzhi_relations(year_pillar: str, month_pillar: str, day_pillar: str, hour_pillar: str) -> str:
        return "干支关系分析模块未找到"


def ensure_lunar_python() -> bool:
    """
    检查并确保 lunar-python 库已安装
    
    Returns:
        bool: 如果库可用返回 True，否则返回 False
    """
    try:
        from lunar_python import Solar, Lunar  # noqa: F401
        return True
    except ImportError:
        msg = (
            "未检测到依赖库 lunar-python。\n"
            "请先安装：pip install lunar-python\n"
            "如果使用的是 PowerShell，可执行：python -m pip install lunar-python\n"
        )
        print(msg)
        return False


def read_int(prompt: str, min_value: Optional[int] = None, max_value: Optional[int] = None) -> int:
    """
    读取并验证整数输入
    
    Args:
        prompt: 提示信息
        min_value: 最小值限制（可选）
        max_value: 最大值限制（可选）
        
    Returns:
        int: 验证通过的整数值
    """
    while True:
        try:
            s = input(prompt).strip()
            if not s:
                print("输入不能为空！")
                continue
                
            v = int(s)
            
            if min_value is not None and v < min_value:
                print(f"数值需不小于 {min_value}")
                continue
                
            if max_value is not None and v > max_value:
                print(f"数值需不大于 {max_value}")
                continue
                
            return v
            
        except ValueError:
            print("请输入有效的整数！")
        except KeyboardInterrupt:
            print("\n程序已取消")
            sys.exit(0)


def read_choice(prompt: str, choices: List[str]) -> str:
    """
    读取并验证选择输入
    
    Args:
        prompt: 提示信息
        choices: 可选选项列表
        
    Returns:
        str: 用户选择的选项
    """
    while True:
        try:
            s = input(prompt).strip()
            if not s:
                print("输入不能为空！")
                continue
                
            # 对于中文选项，直接比较；对于英文选项，转小写比较
            if s in choices:
                return s
            elif s.lower() in [c.lower() for c in choices]:
                # 找到匹配的选项（忽略大小写）
                for c in choices:
                    if s.lower() == c.lower():
                        return c
                
            print(f"请输入 {', '.join(choices)} 之一！")
            
        except KeyboardInterrupt:
            print("\n程序已取消")
            sys.exit(0)


def get_gender_input() -> str:
    """
    获取性别输入
    
    Returns:
        str: 性别（'男' 或 '女'）
    """
    print("\n【性别信息】")
    return read_choice("请输入性别（男/女）：", ["男", "女"])


def get_24_solar_terms(year: int) -> List[Tuple[str, datetime]]:
    """
    获取指定年份的二十四节气时间
    
    Args:
        year: 年份
        
    Returns:
        List[Tuple[str, datetime]]: 节气名称和时间的列表
    """
    from lunar_python import Solar
    
    # 使用近似日期，这些日期是根据平均值计算的
    approximate_terms = [
        ("小寒", datetime(year, 1, 6, 0, 0)),  # 小寒在年初
        ("立春", datetime(year, 2, 4, 6, 0)),
        ("惊蛰", datetime(year, 3, 5, 11, 0)),
        ("清明", datetime(year, 4, 4, 17, 0)),
        ("立夏", datetime(year, 5, 5, 22, 0)),
        ("芒种", datetime(year, 6, 5, 13, 0)),
        ("小暑", datetime(year, 7, 7, 6, 35)),
        ("立秋", datetime(year, 8, 7, 16, 20)),
        ("白露", datetime(year, 9, 7, 13, 0)),
        ("寒露", datetime(year, 10, 8, 6, 0)),
        ("立冬", datetime(year, 11, 7, 19, 0)),
        ("大雪", datetime(year, 12, 7, 7, 0))
    ]
    
    return sorted(approximate_terms, key=lambda x: x[1])


def calculate_dayun_start_time(birth_datetime: datetime, gender: str, year_stem: str) -> Tuple[int, int, int, int, int]:
    """
    计算大运起始时间
    
    Args:
        birth_datetime: 出生时间
        gender: 性别（'男' 或 '女'）
        year_stem: 年柱天干
        
    Returns:
        Tuple[int, int, int, int, int]: (年, 月, 日, 时辰, 四舍五入年龄)
    """
    # 判断年干的阴阳性
    yang_stems = ['甲', '丙', '戊', '庚', '壬']
    is_yang_year = year_stem in yang_stems
    
    # 获取出生年份的节气
    birth_year = birth_datetime.year
    # 获取当年和前后年的节气，确保能找到跨年的节令
    terms_prev = get_24_solar_terms(birth_year - 1)
    terms_current = get_24_solar_terms(birth_year)
    terms_next = get_24_solar_terms(birth_year + 1)
    
    # 合并三年的节气
    all_terms = terms_prev + terms_current + terms_next
    
    # 确定计算方向
    if (is_yang_year and gender == '男') or (not is_yang_year and gender == '女'):
        # 顺行：计算到下一个节令的时间
        target_term = None
        for term_name, term_time in all_terms:
            if term_time > birth_datetime:
                target_term = term_time
                print(f"找到下一个节令：{term_name} - {term_time}")
                break
    else:
        # 逆行：计算到上一个节令的时间
        target_term = None
        for term_name, term_time in reversed(all_terms):
            if term_time < birth_datetime:
                target_term = term_time
                print(f"找到上一个节令：{term_name} - {term_time}")
                break
    
    if target_term is None:
        # 如果找不到对应节令，使用默认计算
        target_term = birth_datetime + timedelta(days=90)  # 约3个月后
        print(f"未找到对应节令，使用默认值：{target_term}")
    
    # 计算时间差
    if target_term > birth_datetime:
        time_diff = target_term - birth_datetime
    else:
        time_diff = birth_datetime - target_term
    
    print(f"出生时间：{birth_datetime}")
    print(f"目标节令：{target_term}")
    print(f"时间差：{time_diff}")
    
    # 按照三天计一岁的规则计算
    total_days = time_diff.days
    total_seconds = time_diff.seconds
    total_hours = total_seconds // 3600
    total_minutes = (total_seconds % 3600) // 60
    
    print(f"总天数：{total_days}，总小时数：{total_hours}，总分钟数：{total_minutes}")
    
    # 计算起运年龄：3天=1岁
    total_years_float = total_days / 3.0  # 精确计算岁数
    
    # 四舍五入到最近的整数岁数（用于计算大运年份）
    rounded_years = round(total_years_float)
    
    # 显示用的精确计算（传统方式）
    display_years = total_days // 3
    remaining_days = total_days % 3
    display_months = remaining_days * 4  # 1天=4个月
    
    # 小时转换为时辰（显示用）
    extra_hours_from_minutes = total_minutes // 30  # 30分钟=1个时辰
    
    # 最终结果：返回四舍五入的年龄用于计算，但显示精确值
    final_days = 0
    final_hours = extra_hours_from_minutes
    
    # 如果显示月份超过12，转换为年份
    if display_months >= 12:
        display_years += display_months // 12
        display_months = display_months % 12
    
    print(f"最终计算结果：{display_years}岁{display_months}个月{final_days}天{final_hours}个时辰")
    
    return display_years, display_months, final_days, final_hours, rounded_years


def get_dayun_sequence(month_pillar: str, gender: str, year_stem: str) -> List[str]:
    """
    获取大运排列顺序
    
    Args:
        month_pillar: 月柱干支
        gender: 性别（'男' 或 '女'）
        year_stem: 年柱天干
        
    Returns:
        List[str]: 八部大运的干支列表
    """
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
        # 如果找不到，默认从甲子开始
        current_index = 0
    
    # 判断年干的阴阳性
    yang_stems = ['甲', '丙', '戊', '庚', '壬']
    is_yang_year = year_stem in yang_stems
    
    # 确定排列方向
    if (is_yang_year and gender == '男') or (not is_yang_year and gender == '女'):
        # 顺行排列
        direction = 1
    else:
        # 逆行排列
        direction = -1
    
    # 生成八部大运
    dayun_list = []
    for i in range(8):  # 只生成8个大运
        index = (current_index + (i + 1) * direction) % 60
        dayun_list.append(jiazi[index])
    
    return dayun_list


def calculate_dayun_years(birth_year: int, start_age: int) -> List[int]:
    """
    计算大运对应的年份（传统0岁起算）
    
    Args:
        birth_year: 出生公历年份
        start_age: 起运年龄（传统算法，0岁起）
        
    Returns:
        List[int]: 八部大运对应的年份
    """
    years = []
    for i in range(8):
        # 传统算法：出生年为0岁，所以实际年份 = 出生年 + 起运年龄 + i*10
        year = birth_year + start_age + i * 10
        years.append(year)
    return years


def get_dayun_ages(start_age: int) -> List[int]:
    """
    获取大运对应的岁数（实际走大运时的年龄）
    
    Args:
        start_age: 起运年龄（传统算法，0岁起）
        
    Returns:
        List[int]: 八部大运对应的实际年龄
    """
    ages = []
    for i in range(8):
        # 实际走大运的年龄 = 起运年龄 + 1 + i*10
        # 因为起运后的第二年才开始走大运
        age = start_age + 1 + i * 10
        ages.append(age)
    return ages


def get_liunian_for_dayun(dayun_ganzhi: str, start_year: int, start_age: int) -> List[Tuple[str, int, int]]:
    """
    计算指定大运内的十年流年信息
    
    Args:
        dayun_ganzhi: 大运干支
        start_year: 开始年份
        start_age: 开始年龄（实际走大运的年龄）
        
    Returns:
        List[Tuple[str, int, int]]: 流年信息列表 (干支, 年份, 年龄)
    """
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
        age = start_age + i
        
        # 根据公历年份计算流年干支
        jiazi_index = (year - 1984) % 60
        if jiazi_index < 0:
            jiazi_index += 60
        
        liunian_ganzhi = jiazi[jiazi_index]
        liunian_list.append((liunian_ganzhi, year, age))
    
    return liunian_list


def display_liunian_result(dayun_ganzhi: str, liunian_list: List[Tuple[str, int, int]]) -> None:
    """
    显示流年查询结果
    
    Args:
        dayun_ganzhi: 大运干支
        liunian_list: 流年信息列表
    """
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


def liunian_query_loop(dayun_list: List[str], dayun_years: List[int], rounded_start_age: int) -> None:
    """
    流年查询循环
    
    Args:
        dayun_list: 大运列表
        dayun_years: 大运年份列表
        rounded_start_age: 起运年龄
    """
    print("\n" + "-" * 50)
    print("流年查询功能：")
    print(f"可查询的大运：{' '.join(dayun_list)}")
    print("输入 'q' 或 'quit' 退出")
    print()
    
    while True:
        try:
            user_input = input("请输入要查询的大运干支：").strip()
            
            if user_input.lower() in ['q', 'quit', '退出']:
                print("流年查询已退出")
                break
            
            if user_input in dayun_list:
                # 找到对应的大运索引
                dayun_index = dayun_list.index(user_input)
                start_year = dayun_years[dayun_index]
                
                # 计算实际走大运的年龄（起运年龄 + 1 + 大运序号*10）
                actual_start_age = rounded_start_age + 1 + dayun_index * 10
                
                # 计算该大运的流年信息
                liunian_list = get_liunian_for_dayun(user_input, start_year, actual_start_age)
                
                # 显示流年结果
                display_liunian_result(user_input, liunian_list)
                print()
            else:
                print(f"❌ 请输入有效的大运干支：{' '.join(dayun_list)}")
                
        except KeyboardInterrupt:
            print("\n流年查询已退出")
            break
        except EOFError:
            print("\n流年查询已退出")
            break


def display_dayun_result(year_pillar: str, month_pillar: str, day_pillar: str, hour_pillar: str,
                        solar_time: str, lunar_time: str, gender: str, 
                        start_age: int, start_months: int, start_days: int, start_hours: int,
                        dayun_list: List[str], dayun_years: List[int], rounded_start_age: int) -> None:
    """显示计算结果和大运信息"""
    print("\n" + "=" * 50)
    print("        四柱八字及大运计算结果")
    print("=" * 50)
    print(f"公历时间：{solar_time}")
    print(f"农历时间：{lunar_time}")
    print(f"性别：{gender}")
    print("-" * 50)
    print(f"年柱：{year_pillar}")
    print(f"月柱：{month_pillar}")
    print(f"日柱：{day_pillar}")
    print(f"时柱：{hour_pillar}")
    print("-" * 50)
    print(f"四柱八字：{year_pillar} {month_pillar} {day_pillar} {hour_pillar}")
    print("-" * 50)
    
    # 添加干支关系分析
    try:
        ganzhi_analysis = analyze_ganzhi_relations(year_pillar, month_pillar, day_pillar, hour_pillar)
        print(ganzhi_analysis)
        print("-" * 50)
    except Exception as e:
        print(f"干支关系分析出现错误：{e}")
        print("-" * 50)
    
    print(f"起大运时间：{start_age}岁{start_months}个月{start_days}天{start_hours}个时辰")
    print("-" * 50)
    print("八部大运排列：")
    print()
    
    # 显示大运表格（仅显示8个）
    headers = []
    ages = get_dayun_ages(rounded_start_age)  # 使用实际走大运的年龄
    years = []
    
    for i in range(min(8, len(dayun_list))):
        headers.append(dayun_list[i])
        years.append(str(dayun_years[i]))
    
    # 使用固定宽度格式化，确保对齐
    print("大运：", end="")
    for h in headers:
        print(f"{h:^8}", end="")
    print()
    
    print("岁数：", end="")
    for a in ages:
        print(f"{a:^8}", end="")
    print()
    
    print("年份：", end="")
    for y in years:
        print(f"{y:^8}", end="")
    print()
    
    print("=" * 50)


def calc_bazi_from_solar(year: int, month: int, day: int, hour: int) -> Tuple[str, str, str, str]:
    """
    从公历日期计算四柱八字
    """
    from lunar_python import Solar

    try:
        solar = Solar.fromYmdHms(year, month, day, hour, 0, 0)
        lunar = solar.getLunar()
        ec = lunar.getEightChar()
        return ec.getYear(), ec.getMonth(), ec.getDay(), ec.getTime()
    except Exception as e:
        raise ValueError(f"公历日期无效: {year}-{month:02d}-{day:02d} {hour:02d}:00") from e


def get_date_info_from_solar(year: int, month: int, day: int, hour: int) -> Tuple[str, str]:
    """
    从公历日期获取公历和农历时间信息
    """
    from lunar_python import Solar
    
    solar = Solar.fromYmdHms(year, month, day, hour, 0, 0)
    lunar = solar.getLunar()
    
    # 公历时间
    solar_str = f"{year}年{month}月{day}日 {hour:02d}:00"
    
    # 农历时间
    lunar_year = lunar.getYear()
    lunar_month = lunar.getMonth()
    lunar_day = lunar.getDay()
    
    lunar_str = f"{lunar_year}年{lunar_month}月{lunar_day}日 {hour:02d}:00"
    
    return solar_str, lunar_str


def get_solar_input() -> Tuple[int, int, int, int]:
    """
    获取公历输入
    """
    print("\n【公历输入】")
    year = read_int("请输入公历年份（例如 2023）：", 1900, 2100)
    month = read_int("请输入公历月份（1-12）：", 1, 12)
    
    # 根据月份和年份计算该月的最大天数
    import calendar
    max_day = calendar.monthrange(year, month)[1]
    day = read_int(f"请输入公历日（1-{max_day}）：", 1, max_day)
    hour = read_int("请输入小时（0-23）：", 0, 23)
    
    return year, month, day, hour


def display_banner() -> None:
    """显示程序横幅"""
    print("=" * 60)
    print("           四柱八字及大运计算器")
    print("     支持公历与农历输入，自动计算大运")
    print("=" * 60)
    print("使用说明：")
    print("- 公历示例：2023 10 1 15 表示 2023-10-01 15:00")
    print("- 农历闰月将自动识别，无需手动选择是否闰月")
    print("- 大运计算遵循传统命理学规则，结合性别、出生时间及节令")
    print("- 按 Ctrl+C 可随时退出程序")
    print("-" * 60)


def main() -> None:
    """主函数"""
    try:
        display_banner()

        if not ensure_lunar_python():
            sys.exit(1)

        # 获取性别信息
        gender = get_gender_input()

        mode = read_choice("\n请选择输入历法（g=公历, n=农历）：", ["g", "n"])

        if mode == "g":
            year, month, day, hour = get_solar_input()
            try:
                year_pillar, month_pillar, day_pillar, hour_pillar = calc_bazi_from_solar(year, month, day, hour)
                solar_time, lunar_time = get_date_info_from_solar(year, month, day, hour)
                birth_datetime = datetime(year, month, day, hour)
            except ValueError as e:
                print(f"\n❌ 错误：{e}")
                sys.exit(1)
        else:
            print("农历输入功能暂不可用")
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
                year_pillar, month_pillar, day_pillar, hour_pillar,
                solar_time, lunar_time, gender,
                start_age, start_months, start_days, start_hours,
                dayun_list, dayun_years, rounded_start_age
            )
            
            # 流年查询功能
            liunian_query_loop(dayun_list, dayun_years, rounded_start_age)
            
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
        sys.exit(1)


if __name__ == "__main__":
    main()