
import sys
from typing import Tuple, List, Optional, Dict
from datetime import datetime, timedelta
import importlib.util
try:
    from wcwidth import wcswidth
except ImportError:
    wcswidth = None

GAN = ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸']
ZHI = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥']
JIAZI_CYCLE = [f"{GAN[i % 10]}{ZHI[i % 12]}" for i in range(60)]

LUNAR_MONTH_NAMES = {
    1: "正月", 2: "二月", 3: "三月", 4: "四月", 5: "五月", 6: "六月",
    7: "七月", 8: "八月", 9: "九月", 10: "十月", 11: "冬月", 12: "腊月"
}

def format_lunar_dt_from_object(lunar_obj, hour: int) -> str:
    """
    根据lunar-python的Lunar对象，格式化完整的农历日期时间字符串
    """
    year = lunar_obj.getYear()
    month = lunar_obj.getMonth()
    day_in_chinese = lunar_obj.getDayInChinese()

    is_leap = month < 0
    month_abs = abs(month)
    
    month_str = LUNAR_MONTH_NAMES.get(month_abs, f"{month_abs}月")
    if is_leap:
        month_str = f"闰{month_str}"
        
    return f"{year}年{month_str}{day_in_chinese} {hour:02d}:00"


def get_24_solar_terms(year: int) -> List[Tuple[str, datetime]]:
    """
    获取指定年份的二十四节气时间（使用近似平均日期）。
    返回以日期排序的列表。
    """
    approximate_terms = [
        ("小寒", datetime(year, 1, 6, 0, 0)),
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
        ("大雪", datetime(year, 12, 7, 7, 0)),
    ]
    return sorted(approximate_terms, key=lambda x: x[1])


def calculate_dayun_start_time(
    birth_datetime: datetime,
    gender: str,
    year_stem: str,
    *,
    debug: bool = False,
) -> Tuple[int, int, int, int, int]:
    """
    计算大运起始时间（按“3天=1岁”），返回(年,月,日,时辰,四舍五入年龄)。
    debug=True 时打印中间过程。
    """
    yang_stems = ['甲', '丙', '戊', '庚', '壬']
    is_yang_year = year_stem in yang_stems

    birth_year = birth_datetime.year
    terms_prev = get_24_solar_terms(birth_year - 1)
    terms_current = get_24_solar_terms(birth_year)
    terms_next = get_24_solar_terms(birth_year + 1)
    all_terms = terms_prev + terms_current + terms_next

    if (is_yang_year and gender == '男') or (not is_yang_year and gender == '女'):
        target_term = None
        for term_name, term_time in all_terms:
            if term_time > birth_datetime:
                target_term = term_time
                if debug:
                    print(f"找到下一个节令：{term_name} - {term_time}")
                break
    else:
        target_term = None
        for term_name, term_time in reversed(all_terms):
            if term_time < birth_datetime:
                target_term = term_time
                if debug:
                    print(f"找到上一个节令：{term_name} - {term_time}")
                break

    if target_term is None:
        target_term = birth_datetime + timedelta(days=90)
        if debug:
            print(f"未找到对应节令，使用默认值：{target_term}")

    time_diff = target_term - birth_datetime if target_term > birth_datetime else birth_datetime - target_term

    if debug:
        print(f"出生时间：{birth_datetime}")
        print(f"目标节令：{target_term}")
        print(f"时间差：{time_diff}")

    total_days = time_diff.days
    total_seconds = time_diff.seconds
    total_hours = total_seconds // 3600
    total_minutes = (total_seconds % 3600) // 60

    if debug:
        print(f"总天数：{total_days}，总小时数：{total_hours}，总分钟数：{total_minutes}")

    total_years_float = total_days / 3.0
    rounded_years = round(total_years_float)

    display_years = total_days // 3
    remaining_days = total_days % 3
    display_months = remaining_days * 4

    final_days = 0
    final_hours = total_hours // 2  # 1时辰=2小时

    if display_months >= 12:
        display_years += display_months // 12
        display_months = display_months % 12

    if debug:
        print(f"最终计算结果：{display_years}岁{display_months}个月{final_days}天{final_hours}个时辰")

    return display_years, display_months, final_days, final_hours, rounded_years


def get_dayun_sequence(month_pillar: str, gender: str, year_stem: str) -> List[str]:
    """生成八部大运顺序"""
    try:
        current_index = JIAZI_CYCLE.index(month_pillar)
    except ValueError:
        current_index = 0

    yang_stems = ['甲', '丙', '戊', '庚', '壬']
    is_yang_year = year_stem in yang_stems
    direction = 1 if (is_yang_year and gender == '男') or (not is_yang_year and gender == '女') else -1

    return [JIAZI_CYCLE[(current_index + (i + 1) * direction) % 60] for i in range(8)]


def calculate_dayun_years(birth_year: int, start_age: int) -> List[int]:
    """按传统0岁起算，返回八部大运对应年份"""
    return [birth_year + start_age + i * 10 for i in range(8)]


def get_dayun_ages(start_age: int) -> List[int]:
    """返回八部大运实际开始时的年龄（起运年龄+1，每步加10）"""
    return [start_age + 1 + i * 10 for i in range(8)]


def get_liunian_for_dayun(dayun_ganzhi: str, start_year: int, start_age: int) -> List[Tuple[str, int, int]]:
    """计算指定大运内的十年流年 (干支, 年份, 年龄)"""
    liunian_list: List[Tuple[str, int, int]] = []
    for i in range(10):
        year = start_year + i
        age = start_age + i
        jiazi_index = (year - 1984) % 60
        if jiazi_index < 0:
            jiazi_index += 60
        liunian_ganzhi = JIAZI_CYCLE[jiazi_index]
        liunian_list.append((liunian_ganzhi, year, age))
    return liunian_list


def ensure_dependencies(dependencies: List[Tuple[str, str]]) -> None:
    """检查依赖库是否存在，如果不存在则提示安装并退出"""
    missing_deps = []
    for package_name, install_command in dependencies:
        if importlib.util.find_spec(package_name) is None:
            missing_deps.append(install_command)
    
    if missing_deps:
        print("错误：缺少必要的依赖库。请安装：")
        for cmd in missing_deps:
            print(f"  {cmd}")
        sys.exit(1)

def ensure_lunar_python() -> None:
    """旧的依赖检查函数，重定向到新的通用函数"""
    ensure_dependencies([("lunar_python", "pip install lunar-python>=1.2.13")])


def read_int(prompt: str, min_value: Optional[int] = None, max_value: Optional[int] = None) -> int:
    """读取并验证整数输入"""
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
    """读取并验证选择输入"""
    while True:
        try:
            s = input(prompt).strip()
            if not s:
                print("输入不能为空！")
                continue
            if s in choices:
                return s
            elif s.lower() in [c.lower() for c in choices]:
                for c in choices:
                    if s.lower() == c.lower():
                        return c
            print(f"请输入 {', '.join(choices)} 之一！")
        except KeyboardInterrupt:
            print("\n程序已取消")
            sys.exit(0)


def get_gender_input() -> str:
    """获取性别输入"""
    print("\n【性别信息】")
    return read_choice("请输入性别（男/女）：", ["男", "女"])


def get_solar_input() -> Tuple[int, int, int, int]:
    """获取公历输入"""
    print("\n【公历输入】")
    year = read_int("请输入公历年份（例如 2023）：", 1, 9999)
    month = read_int("请输入公历月份（1-12）：", 1, 12)
    try:
        import calendar
        max_day = calendar.monthrange(year, month)[1]
    except Exception:
        max_day = 31
    day = read_int(f"请输入公历日（1-{max_day}）：", 1, max_day)
    hour = read_int("请输入小时（0-23）：", 0, 23)
    return year, month, day, hour


def get_lunar_input() -> Tuple[int, int, int, int]:
    """获取农历输入，并处理闰月"""
    print("\n【农历输入】")
    year = read_int("请输入农历年份（例如 2023）：", 1, 9999)
    month = read_int("请输入农历月份（1-12）：", 1, 12)
    day = read_int("请输入农历日（1-30）：", 1, 30)
    hour = read_int("请输入小时（0-23）：", 0, 23)
    
    # 自动检测当年是否有闰月，如果有，则询问用户
    try:
        from lunar_python import LunarYear # type: ignore
        lunar_year_obj = LunarYear.fromYear(year)
        leap_month = lunar_year_obj.getLeapMonth()
        if leap_month == month:
            is_leap_input = read_choice(f"检测到{year}年有闰{month}月，您输入的是否为闰月？(y/n)", ['y', 'n'])
            if is_leap_input == 'y':
                month = -month  # 负数月份代表闰月
    except (ImportError, Exception):
        # 兼容旧版或库出错时，跳过闰月检测
        pass
        
    return year, month, day, hour


def display_banner() -> None:
    """显示程序标题和说明"""
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


def get_str_display_width(s: str) -> int:
    """计算字符串的显示宽度，优先使用 wcwidth 库"""
    if wcswidth:
        # 使用 wcwidth 计算宽度，-1表示控制字符等，视为0
        return max(0, wcswidth(str(s)))
    
    # 如果 wcwidth 未安装，则回退到基本方法
    width = 0
    for char in str(s):
        if '\u4e00' <= char <= '\u9fff':
            width += 2
        else:
            width += 1
    return width


def pad_str_to_center(s: str, total_width: int) -> str:
    """将字符串在指定总宽度内居中"""
    s = str(s)
    current_width = get_str_display_width(s)
    if current_width >= total_width:
        return s
    
    padding_total = total_width - current_width
    padding_left = padding_total // 2
    padding_right = padding_total - padding_left
    return ' ' * padding_left + s + ' ' * padding_right

