"""
四柱八字计算器

支持公历和农历输入，自动计算四柱八字。
使用 lunar-python 库进行农历转换和八字计算。
"""

import sys
from typing import Tuple, Optional, List
from datetime import datetime


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
        str: 用户选择的小写选项
    """
    choices_lower = [c.lower() for c in choices]
    while True:
        try:
            s = input(prompt).strip().lower()
            if not s:
                print("输入不能为空！")
                continue
                
            if s in choices_lower:
                return s
                
            print(f"请输入 {', '.join(choices)} 之一！")
            
        except KeyboardInterrupt:
            print("\n程序已取消")
            sys.exit(0)


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


def calc_bazi_from_lunar(year: int, month: int, day: int, hour: int, is_leap: bool) -> Tuple[str, str, str, str]:
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
        raise ValueError(f"农历日期无效: {year}年{leap_str}{month}月{day}日 {hour:02d}:00") from e


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
    """显示程序标题和说明"""
    print("=" * 50)
    print("           四柱八字计算器")
    print("     支持公历与农历输入")
    print("=" * 50)
    print("使用说明：")
    print("- 公历示例：2023 10 1 15 表示 2023-10-01 15:00")
    print("- 农历闰月将自动识别，无需手动选择是否闰月")
    print("- 按 Ctrl+C 可随时退出程序")
    print("-" * 50)


def get_solar_input() -> Tuple[int, int, int, int]:
    """获取公历输入"""
    print("\n【公历输入】")
    year = read_int("请输入公历年份（例如 2023）：", 1, 9999)
    month = read_int("请输入公历月份（1-12）：", 1, 12)
    day = read_int("请输入公历日（1-31）：", 1, 31)
    hour = read_int("请输入小时（0-23）：", 0, 23)
    return year, month, day, hour


def get_lunar_input() -> Tuple[int, int, int, int]:
    """获取农历输入"""
    print("\n【农历输入】")
    year = read_int("请输入农历年份（例如 2023）：", 1, 9999)
    month = read_int("请输入农历月份（1-12）：", 1, 12)
    day = read_int("请输入农历日（1-30）：", 1, 30)
    hour = read_int("请输入小时（0-23）：", 0, 23)
    return year, month, day, hour


def display_result(year_pillar: str, month_pillar: str, day_pillar: str, hour_pillar: str) -> None:
    """显示计算结果"""
    print("\n" + "=" * 30)
    print("        计算结果")
    print("=" * 30)
    print(f"年柱：{year_pillar}")
    print(f"月柱：{month_pillar}")
    print(f"日柱：{day_pillar}")
    print(f"时柱：{hour_pillar}")
    print("-" * 30)
    print(f"四柱八字：{year_pillar} {month_pillar} {day_pillar} {hour_pillar}")
    print("=" * 30)


def main() -> None:
    """主函数"""
    try:
        display_banner()

        if not ensure_lunar_python():
            sys.exit(1)

        mode = read_choice("\n请选择输入历法（g=公历, n=农历）：", ["g", "n"])

        if mode == "g":
            year, month, day, hour = get_solar_input()
            try:
                year_pillar, month_pillar, day_pillar, hour_pillar = calc_bazi_from_solar(year, month, day, hour)
            except ValueError as e:
                print(f"\n❌ 错误：{e}")
                sys.exit(1)
        else:
            year, month, day, hour = get_lunar_input()
            try:
                year_pillar, month_pillar, day_pillar, hour_pillar = calc_bazi_from_lunar_auto(year, month, day, hour)
            except ValueError as e:
                print(f"\n❌ 错误：{e}")
                sys.exit(1)

        display_result(year_pillar, month_pillar, day_pillar, hour_pillar)
        
    except KeyboardInterrupt:
        print("\n\n程序已退出")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ 程序出现意外错误：{e}")
        sys.exit(1)


if __name__ == "__main__":
    main()


