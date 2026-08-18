"""
四柱八字计算器

支持公历和农历输入，自动计算四柱八字。
使用 lunar-python 库进行农历转换和八字计算。
"""

import sys
from typing import Tuple, Optional, List
from datetime import datetime, timedelta
import bazi_common
import importlib.util
import ai_analyzer


DEBUG = False
CHART_COL_WIDTH = 14


def debug_print(*args, **kwargs) -> None:
    if DEBUG:
        print(*args, **kwargs)


def ensure_lunar_python() -> bool:
    """委托公共模块检查 lunar-python 库"""
    if importlib.util.find_spec("lunar_python"):
        return True
    
    msg = (
        "未检测到依赖库 lunar-python。\n"
        "请先安装：pip install lunar-python\n"
        "如果使用的是 PowerShell，可执行：python -m pip install lunar-python\n"
    )
    print(msg)
    return False


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


def get_liunian_for_dayun(dayun_ganzhi: str, start_year: int, start_age: int) -> List[Tuple[str, int, int]]:
    """委托公共模块计算指定大运内十年流年"""
    return bazi_common.get_liunian_for_dayun(dayun_ganzhi, start_year, start_age)


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
    liunian_ganzhi_str = "".join([bazi_common.pad_str_to_center(g, 6) for g, _, _ in liunian_list])
    print(f"流年：{liunian_ganzhi_str}")
    
    years_str = "".join([bazi_common.pad_str_to_center(y, 6) for _, y, _ in liunian_list])
    print(f"年份：{years_str}")
    
    ages_str = "".join([bazi_common.pad_str_to_center(a, 6) for _, _, a in liunian_list])
    print(f"岁数：{ages_str}")
    
    print("=" * 50)


def query_liunian_interactive(dayun_list: List[str], dayun_years: List[int], actual_start_age: int) -> None:
    """
    交互式流年查询功能
    
    Args:
        dayun_list: 大运干支列表
        dayun_years: 大运对应年份列表
        actual_start_age: 实际开始大运的年龄（已经是+1后的年龄）
    """
    while True:
        try:
            print("\n" + "-" * 50)
            print("流年查询功能：")
            print(f"可查询的大运：{' '.join(dayun_list)}")
            print("输入 'q' 或 'quit' 退出")
            
            user_input = input("\n请输入要查询的大运干支：").strip()
            
            if user_input.lower() in ['q', 'quit', '退出']:
                print("感谢使用！")
                break
            
            if not user_input:
                print("输入不能为空！")
                continue
            
            # 查找用户输入的大运
            if user_input in dayun_list:
                # 找到对应的大运索引
                dayun_index = dayun_list.index(user_input)
                start_year = dayun_years[dayun_index]
                # 传入实际年龄（已经是+1后的）
                start_age = actual_start_age + dayun_index * 10
                
                # 计算该大运的流年信息
                liunian_list = get_liunian_for_dayun(user_input, start_year, start_age)
                
                # 显示流年结果
                display_liunian_result(user_input, liunian_list)
                
            else:
                print(f"错误：'{user_input}' 不在当前大运列表中！")
                print(f"请从以下选项中选择：{' '.join(dayun_list)}")
                
        except KeyboardInterrupt:
            print("\n\n感谢使用！")
            break
        except Exception as e:
            print(f"查询过程中出现错误：{e}")
def get_dayun_ages(start_age: int) -> List[int]:
    """委托公共模块计算大运对应岁数"""
    return bazi_common.get_dayun_ages(start_age)


def calc_bazi_from_solar(year: int, month: int, day: int, hour: int) -> Tuple[str, str, str, str]:
    """
    从公历日期计算四柱八字
    
    Args:
        year: 公历年份
        month: 公历月份
        day: 公历日期
        hour: 小时
        
    Returns:
        Tuple[str, str, str, str]: 年柱、月柱、日柱、时柱
        
    Raises:
        ValueError: 当日期无效时
    """
    from lunar_python import Solar

    try:
        solar = Solar.fromYmdHms(year, month, day, hour, 0, 0)
        lunar = solar.getLunar()
        ec = lunar.getEightChar()
        return ec.getYear(), ec.getMonth(), ec.getDay(), ec.getTime()
    except Exception as e:
        raise ValueError(f"公历日期无效: {year}-{month:02d}-{day:02d} {hour:02d}:00") from e


def calc_bazi_from_lunar(year: int, month: int, day: int, hour: int, is_leap: bool = False) -> Tuple[str, str, str, str]:
    """
    从农历日期计算四柱八字
    
    Args:
        year: 农历年份
        month: 农历月份
        day: 农历日期
        hour: 小时
        is_leap: 是否为闰月
        
    Returns:
        Tuple[str, str, str, str]: 年柱、月柱、日柱、时柱
        
    Raises:
        ValueError: 当农历日期无效时
    """
    from lunar_python import Lunar

    try:
        try:
            lunar = Lunar.fromYmdHms(year, month, day, hour, 0, 0, is_leap)
        except TypeError:
            # 兼容旧版本（无 is_leap 形参）
            lunar = Lunar.fromYmdHms(year, month, day, hour, 0, 0)
        
        ec = lunar.getEightChar()
        return ec.getYear(), ec.getMonth(), ec.getDay(), ec.getTime()
    except Exception as e:
        leap_str = "闰" if is_leap else ""
        error_msg = (
            f"农历日期无效: {year}年{leap_str}{month}月{day}日。"
            "请检查该月份是否存在此日期（例如，是否为小月）。"
        )
        raise ValueError(error_msg) from e


def calc_bazi_from_lunar_auto(year: int, month: int, day: int, hour: int) -> Tuple[str, str, str, str]:
    """
    自动判断闰月并计算四柱八字
    
    自动判断闰月逻辑：
    - 若当年无闰月，或闰月与输入月份不同，则按非闰月处理
    - 若当年该月为闰月：优先尝试非闰月，若该日不存在则尝试闰月
    - 兼容旧版 lunar_python（无 LunarYear 或 fromYmdHms 无 is_leap 形参）
    
    Args:
        year: 农历年份
        month: 农历月份
        day: 农历日期
        hour: 小时
        
    Returns:
        Tuple[str, str, str, str]: 年柱、月柱、日柱、时柱
        
    Raises:
        ValueError: 当农历日期无效时
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
            return calc_bazi_from_lunar(year, month, day, hour, False)
            
        # 若当年该月为闰月：优先尝试非闰月，若该日不存在则尝试闰月
        try:
            return calc_bazi_from_lunar(year, month, day, hour, False)
        except ValueError:
            return calc_bazi_from_lunar(year, month, day, hour, True)
            
    except ImportError:
        # 兼容旧版 lunar_python（无 LunarYear）
        try:
            return calc_bazi_from_lunar(year, month, day, hour, False)
        except ValueError:
            return calc_bazi_from_lunar(year, month, day, hour, True)


def display_banner() -> None:
    """委托公共模块显示程序标题和说明"""
    bazi_common.display_banner()


def get_solar_input() -> Tuple[int, int, int, int]:
    """委托公共模块获取公历输入"""
    return bazi_common.get_solar_input()


def get_lunar_input() -> Tuple[int, int, int, int]:
    """委托公共模块获取农历输入"""
    return bazi_common.get_lunar_input()


def format_lunar_day(day: int) -> str:
    """委托公共模块格式化农历日期"""
    return bazi_common.format_lunar_day(day)


def get_date_info_from_solar(year: int, month: int, day: int, hour: int) -> Tuple[str, str]:
    """
    从公历日期获取公历和农历时间信息
    
    Args:
        year: 公历年份
        month: 公历月份
        day: 公历日期
        hour: 小时
        
    Returns:
        Tuple[str, str]: (公历时间字符串, 农历时间字符串)
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
    # 尝试不同的方法获取闰月信息
    try:
        is_leap = lunar.getLeap()
    except AttributeError:
        try:
            is_leap = lunar.isLeap()
        except AttributeError:
            # 如果都没有，尝试从月份名称判断
            try:
                month_str = str(lunar_month)
                is_leap = "闰" in month_str
            except:
                is_leap = False
    
    leap_str = "闰" if is_leap else ""
    day_str = format_lunar_day(lunar_day)
    lunar_str = f"{lunar_year}年{leap_str}{lunar_month}月{day_str} {hour:02d}:00"
    
    return solar_str, lunar_str


def get_date_info_from_lunar(year: int, month: int, day: int, hour: int) -> Tuple[str, str]:
    """
    从农历日期获取公历和农历时间信息
    
    Args:
        year: 农历年份
        month: 农历月份
        day: 农历日期
        hour: 小时
        
    Returns:
        Tuple[str, str]: (公历时间字符串, 农历时间字符串)
    """
    from lunar_python import Lunar
    
    # 先尝试非闰月
    try:
        lunar = Lunar.fromYmdHms(year, month, day, hour, 0, 0, False)
    except (TypeError, ValueError):
        # 兼容旧版本或无闰月参数
        try:
            lunar = Lunar.fromYmdHms(year, month, day, hour, 0, 0)
        except ValueError:
            # 尝试闰月
            try:
                lunar = Lunar.fromYmdHms(year, month, day, hour, 0, 0, True)
            except TypeError:
                raise ValueError(f"农历日期无效: {year}年{month}月{day}日")
    
    solar = lunar.getSolar()
    
    # 公历时间
    solar_year = solar.getYear()
    solar_month = solar.getMonth()
    solar_day = solar.getDay()
    solar_str = f"{solar_year}年{solar_month}月{solar_day}日 {hour:02d}:00"
    
    # 农历时间
    lunar_year = lunar.getYear()
    lunar_month = lunar.getMonth()
    lunar_day = lunar.getDay()
    # 尝试不同的方法获取闰月信息
    try:
        is_leap = lunar.getLeap()
    except AttributeError:
        try:
            is_leap = lunar.isLeap()
        except AttributeError:
            # 如果都没有，尝试从月份名称判断
            try:
                month_str = str(lunar_month)
                is_leap = "闰" in month_str
            except:
                is_leap = False
    
    leap_str = "闰" if is_leap else ""
    day_str = format_lunar_day(lunar_day)
    lunar_str = f"{lunar_year}年{leap_str}{lunar_month}月{day_str} {hour:02d}:00"
    
    return solar_str, lunar_str


def display_dayun_result(year_pillar: str, month_pillar: str, day_pillar: str, hour_pillar: str,
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
    
    # 显示四柱八字
    print("-" * total_width)
    print(bazi_common.pad_str(f"年柱：{year_pillar}", total_width))
    print(bazi_common.pad_str(f"月柱：{month_pillar}", total_width))
    print(bazi_common.pad_str(f"日柱：{day_pillar}", total_width))
    print(bazi_common.pad_str(f"时柱：{hour_pillar}", total_width))
    print("-" * total_width)
    print(bazi_common.pad_str(f"四柱八字：{year_pillar} {month_pillar} {day_pillar} {hour_pillar}", total_width))
    
    # 添加原局干支关系分析
    print("\n【原局作用关系】")
    relations = "该功能仅在 bazi_calculator.py 中可用"
    try:
        from ganzhi_relations import analyze_ganzhi_relations
        relations = analyze_ganzhi_relations(year_pillar, month_pillar, day_pillar, hour_pillar)
    except ImportError:
        pass
    print(relations)
    
    print("-" * total_width)
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


def main() -> None:
    """主函数"""
    bazi_common.ensure_dependencies([
        ("lunar_python", "pip install lunar-python>=1.2.13"),
        ("wcwidth", "pip install wcwidth")
    ])

    try:
        display_banner()

        # 获取性别信息
        gender = get_gender_input()

        mode = read_choice("\n请选择输入历法（g=公历, n=农历）：", ["g", "n"])

        year_pillar = month_pillar = day_pillar = hour_pillar = ""
        birth_datetime: Optional[datetime] = None

        # Get date input
        if mode == "g":
            year, month, day, hour = get_solar_input()
            solar_time = f"{year}年{month}月{day}日 {hour:02d}:00"
            
            from lunar_python import Solar  # type: ignore
            year_pillar, month_pillar, day_pillar, hour_pillar = calc_bazi_from_solar(
                year, month, day, hour
            )
            birth_datetime = datetime(year, month, day, hour)
            lunar = Solar.fromYmdHms(year, month, day, hour, 0, 0).getLunar()
            lunar_time = bazi_common.format_lunar_dt_from_object(lunar, hour)

        else: # Lunar
            year, month, day, hour = get_lunar_input()
            
            from lunar_python import Lunar # type: ignore
            try:
                lunar = Lunar.fromYmdHms(year, month, day, hour, 0, 0)
                solar = lunar.getSolar()
                solar_time = f"{solar.getYear()}年{solar.getMonth()}月{solar.getDay()}日 {hour:02d}:00"
                lunar_time = bazi_common.format_lunar_dt_from_object(lunar, hour)
                year_pillar, month_pillar, day_pillar, hour_pillar = calc_bazi_from_lunar(
                    year, month, day, hour
                )
                birth_datetime = datetime(solar.getYear(), solar.getMonth(), solar.getDay(), hour)
            except ValueError as e:
                print(f"\n❌ 错误：{e}")
                sys.exit(1)

        print("-" * 50)
        
        # Calculate Bazi
        try:
            # 提取年柱天干
            year_pillar = year_pillar
            
            # 计算起运时间
            start_age, start_months, start_days, start_hours, rounded_start_age = calculate_dayun_start_time(
                birth_datetime, gender, year_pillar
            )
            
            # 获取大运排列
            dayun_list = get_dayun_sequence(month_pillar, gender, year_pillar)
            
            # 计算对应年份（传统算法：出生年为0岁，实际起运年龄不需要+1）
            # 使用公历出生年份计算，因为传统0岁起算就是以实际出生年为准
            dayun_years = calculate_dayun_years(birth_datetime.year, rounded_start_age)
            
            # 显示结果
            display_dayun_result(
                year_pillar, month_pillar, day_pillar, hour_pillar,
                solar_time, lunar_time, gender,
                start_age, start_months, start_days, start_hours,
                dayun_list, dayun_years, rounded_start_age
            )
            
            # 流年查询功能
            # 传入实际开始走大运的年龄（起运年龄+1）
            actual_dayun_start_age = rounded_start_age + 1
            query_liunian_interactive(dayun_list, dayun_years, actual_dayun_start_age)
            
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


