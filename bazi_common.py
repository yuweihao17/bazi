
import sys
from typing import Tuple, List, Optional, Dict, Any
from datetime import datetime, timedelta
import importlib.util


def configure_console() -> None:
    """Keep CLI diagnostics printable on Windows code pages and redirected output."""
    for stream in (sys.stdin, sys.stdout, sys.stderr):
        reconfigure = getattr(stream, "reconfigure", None)
        if reconfigure is None:
            continue
        try:
            # UTF-8 keeps Chinese output and status markers readable when the
            # process is launched from PowerShell or its output is redirected.
            reconfigure(encoding="utf-8", errors="replace")
        except (OSError, ValueError):
            pass


configure_console()
try:
    from wcwidth import wcswidth
except ImportError:
    wcswidth = None

try:
    from lunar_python import Lunar, LunarYear  # type: ignore
except ImportError:
    Lunar = None
    LunarYear = None

GAN = ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸']
ZHI = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥']
JIAZI_CYCLE = [f"{GAN[i % 10]}{ZHI[i % 12]}" for i in range(60)]

LUNAR_MONTH_NAMES: Dict[int, str] = {
    1: "正月", 2: "二月", 3: "三月", 4: "四月", 5: "五月", 6: "六月",
    7: "七月", 8: "八月", 9: "九月", 10: "十月", 11: "冬月", 12: "腊月"
}

def format_lunar_dt_from_object(lunar_obj: Any, hour: int) -> str:
    """
    根据lunar-python的Lunar对象，格式化完整的农历日期时间字符串。

    Args:
        lunar_obj: lunar-python库中的Lunar实例。
        hour: 当前的小时数。

    Returns:
        格式化后的农历日期时间字符串 (e.g., "2024年正月十五 14:00")。
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


NAYIN_MAP = {
    '甲子': '海中金', '乙丑': '海中金', '丙寅': '炉中火', '丁卯': '炉中火', '戊辰': '大林木', '己巳': '大林木', '庚午': '路旁土', '辛未': '路旁土', '壬申': '剑锋金', '癸酉': '剑锋金',
    '甲戌': '山头火', '乙亥': '山头火', '丙子': '涧下水', '丁丑': '涧下水', '戊寅': '城头土', '己卯': '城头土', '庚辰': '白蜡金', '辛巳': '白蜡金', '壬午': '杨柳木', '癸未': '杨柳木',
    '甲申': '泉中水', '乙酉': '泉中水', '丙戌': '屋上土', '丁亥': '屋上土', '戊子': '霹雳火', '己丑': '霹雳火', '庚寅': '松柏木', '辛卯': '松柏木', '壬辰': '长流水', '癸巳': '长流水',
    '甲午': '沙中金', '乙未': '沙中金', '丙申': '山下火', '丁酉': '山下火', '戊戌': '平地木', '己亥': '平地木', '庚子': '壁上土', '辛丑': '壁上土', '壬寅': '金箔金', '癸卯': '金箔金',
    '甲辰': '覆灯火', '乙巳': '覆灯火', '丙午': '天河水', '丁未': '天河水', '戊申': '大驿土', '己酉': '大驿土', '庚戌': '钗钏金', '辛亥': '钗钏金', '壬子': '桑柘木', '癸丑': '桑柘木',
    '甲寅': '大溪水', '乙卯': '大溪水', '丙辰': '沙中土', '丁巳': '沙中土', '戊午': '天上火', '己未': '天上火', '庚申': '石榴木', '辛酉': '石榴木', '壬戌': '大海水', '癸亥': '大海水',
}


def get_24_solar_terms(year: int) -> List[Tuple[str, datetime]]:
    """
    获取指定年份的二十四节气时间（使用近似平均日期）。

    Args:
        year: 公历年份。

    Returns:
        一个包含 (节气名, datetime对象) 的元组列表，按时间排序。
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
    计算大运起始时间，遵循“3天=1岁”的传统规则。

    Args:
        birth_datetime: 包含公历年、月、日、时的datetime对象。
        gender: 性别 ("男" or "女")。
        year_stem: 出生年份的天干。
        debug: 是否打印详细的计算过程。

    Returns:
        一个包含五个整数的元组：
        (起运岁数, 起运月数, 起运日数, 起运时辰数, 用于计算大运年份的四舍五入岁数)。
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
    """
    根据月柱、性别和年干，生成八步大运的干支顺序。

    Args:
        month_pillar: 月柱的干支 (e.g., "甲子")。
        gender: 性别 ("男" or "女")。
        year_stem: 年柱的天干 (e.g., "癸")。

    Returns:
        一个包含八个干支字符串的列表，代表八步大运。
    """
    try:
        current_index = JIAZI_CYCLE.index(month_pillar)
    except ValueError:
        current_index = 0

    yang_stems = ['甲', '丙', '戊', '庚', '壬']
    is_yang_year = year_stem in yang_stems
    direction = 1 if (is_yang_year and gender == '男') or (not is_yang_year and gender == '女') else -1

    return [JIAZI_CYCLE[(current_index + (i + 1) * direction) % 60] for i in range(8)]


def calculate_dayun_years(birth_year: int, start_age: int) -> List[int]:
    """
    根据出生年份和起运岁数，计算八步大运对应的公历年份。

    Args:
        birth_year: 公历出生年份。
        start_age: 起运岁数（传统算法，0岁起）。

    Returns:
        一个包含八个公历年份的列表。
    """
    return [birth_year + start_age + i * 10 for i in range(8)]


def get_dayun_ages(start_age: int) -> List[int]:
    """
    根据起运岁数，计算八步大运开始时的实际年龄。

    Args:
        start_age: 起运岁数（传统算法，0岁起）。

    Returns:
        一个包含八个年龄的列表。
    """
    return [start_age + 1 + i * 10 for i in range(8)]


def get_liunian_for_dayun(dayun_ganzhi: str, start_year: int, start_age: int) -> List[Tuple[str, int, int]]:
    """
    计算指定大运内的十年流年信息。

    Args:
        dayun_ganzhi: 大运的干支 (e.g., "甲子")。
        start_year: 该大运开始的公历年份。
        start_age: 开始该大运时的实际年龄。

    Returns:
        一个包含 (流年干支, 公历年份, 年龄) 的元组列表。
    """
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
    """
    检查指定的Python库是否已安装，如果未安装则打印安装提示并退出程序。

    Args:
        dependencies: 一个包含 (库名, 安装命令) 的元组列表。
    """
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
    """
    (旧版函数) 检查 `lunar-python` 库是否安装。
    """
    ensure_dependencies([("lunar_python", "pip install lunar-python>=1.2.13")])


def read_int(prompt: str, min_value: Optional[int] = None, max_value: Optional[int] = None) -> int:
    """
    提示用户输入一个整数，并进行范围验证。

    Args:
        prompt: 显示给用户的提示信息。
        min_value: 允许的最小值（包含）。
        max_value: 允许的最大值（包含）。

    Returns:
        用户输入的有效整数。
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
        except EOFError:
            print("\n程序已退出")
            sys.exit(0)
        except KeyboardInterrupt:
            print("\n程序已取消")
            sys.exit(0)


def read_choice(prompt: str, choices: List[str]) -> str:
    """
    提示用户从给定选项中选择一个，支持大小写不敏感匹配。

    Args:
        prompt: 显示给用户的提示信息。
        choices: 一个包含有效选项字符串的列表。

    Returns:
        用户选择的有效选项。
    """
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
        except EOFError:
            print("\n程序已退出")
            sys.exit(0)


def get_gender_input() -> str:
    """
    提示用户输入性别（男/女）。

    Returns:
        用户选择的性别 ("男" or "女")。
    """
    print("\n【性别信息】")
    return read_choice("请输入性别（男/女）：", ["男", "女"])


def get_solar_input() -> Tuple[int, int, int, int]:
    """
    引导用户输入公历年、月、日、时，并进行基本验证。

    Returns:
        一个包含 (年, 月, 日, 小时) 的元组。
    """
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
    """
    引导用户输入农历年、月、日、时，并处理闰月及日期有效性校验。

    Returns:
        一个包含 (年, 月, 日, 小时) 的元组，其中月份若为闰月则为负数。
    """
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
    """
    显示程序的欢迎横幅和基本使用说明。
    """
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


def display_bazi_chart(pillars: List[Dict[str, str]], day_master: str, gender: str) -> None:
    """Display the detailed four/five/six-pillar chart shared by both CLIs."""
    # Local imports keep the common input/calculation helpers lightweight and
    # avoid coupling callers that only need calendar conversion.
    from changsheng import get_changsheng_state
    from shishen import HIDDEN_STEMS, get_shishen

    col_width = 12
    label_col_width = 6
    gender_char = "男" if gender == "男" else "女"
    chart_data: List[Dict[str, Any]] = []
    max_hidden_stems = 0

    for pillar in pillars:
        ganzhi = pillar.get("ganzhi", "")
        if len(ganzhi) < 2:
            raise ValueError(f"无效的干支：{ganzhi!r}")
        gan, zhi = ganzhi[0], ganzhi[1]
        hidden = [f"{stem} {get_shishen(stem, day_master)}" for stem in HIDDEN_STEMS.get(zhi, [])]
        max_hidden_stems = max(max_hidden_stems, len(hidden))
        chart_data.append({
            "name": pillar.get("name", ""),
            "main_star": f"元{gender_char}" if pillar.get("name") == "日柱" else get_shishen(gan, day_master),
            "gan": gan,
            "zhi": zhi,
            "hidden": hidden,
            "xing_yun": get_changsheng_state(day_master, zhi),
            "zi_zuo": get_changsheng_state(gan, zhi),
            "nayin": NAYIN_MAP.get(ganzhi, ""),
        })

    def print_row(data_key: str, label: str) -> None:
        row_items = [pad_str_to_center(item[data_key], col_width) for item in chart_data]
        label_padding = " " * max(0, label_col_width - get_str_display_width(label))
        print(f"{label}{label_padding}{''.join(row_items)}")

    total_width = label_col_width + col_width * len(chart_data)
    print("-" * total_width)
    print_row("name", "")
    print_row("main_star", "主星")
    print_row("gan", "天干")
    print_row("zhi", "地支")
    print("-" * total_width)

    for index in range(max_hidden_stems):
        row_items = [
            pad_str_to_center(item["hidden"][index] if index < len(item["hidden"]) else "", col_width)
            for item in chart_data
        ]
        label = "藏干" if index == 0 else ""
        label_padding = " " * max(0, label_col_width - get_str_display_width(label))
        print(f"{label}{label_padding}{''.join(row_items)}")

    print_row("xing_yun", "星运")
    print_row("zi_zuo", "自坐")
    print_row("nayin", "纳音")
    print("-" * total_width)


def get_str_display_width(s: str) -> int:
    """
    计算字符串在终端中的显示宽度，优先使用 `wcwidth` 库以兼容中文字符。

    Args:
        s: 待计算的字符串。

    Returns:
        字符串的显示宽度。
    """
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
    """
    将字符串在指定的总宽度内进行居中对齐。

    Args:
        s: 待对齐的字符串。
        total_width: 目标总宽度。

    Returns:
        经过居中对齐处理后的新字符串。
    """
    s = str(s)
    current_width = get_str_display_width(s)
    if current_width >= total_width:
        return s
    
    padding_total = total_width - current_width
    padding_left = padding_total // 2
    padding_right = padding_total - padding_left
    return ' ' * padding_left + s + ' ' * padding_right


def pad_str(s: str, total_width: int) -> str:
    """
    将字符串进行左对齐，通过在右侧填充空格来达到指定的总显示宽度。

    Args:
        s: 待对齐的字符串。
        total_width: 目标总宽度。

    Returns:
        经过左对齐处理后的新字符串。
    """
    s = str(s)
    current_width = get_str_display_width(s)
    padding = ' ' * max(0, total_width - current_width)
    return s + padding

