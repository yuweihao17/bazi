"""完整八字计算器的兼容启动入口。

历史版本同时保留了 ``main.py`` 和 ``bazi_calculator.py`` 两个实现，导致
默认启动时跳过 AI、八字反查和完整流年分析。现在由优化版计算器提供唯一
运行实现，本文件保留旧模块名和常用函数入口，避免已有脚本失效。
"""

from typing import Tuple

import bazi_common
from bazi_calculator import *  # noqa: F401,F403 - 兼容历史公共函数
from bazi_calculator import calc_bazi_from_lunar as _calc_bazi_from_lunar
from bazi_calculator import main as _full_main


def ensure_lunar_python() -> bool:
    """兼容旧入口的依赖检查函数。"""
    try:
        bazi_common.ensure_lunar_python()
    except SystemExit:
        return False
    return True


def calc_bazi_from_lunar(
    year: int,
    month: int,
    day: int,
    hour: int,
    is_leap: bool = False,
) -> Tuple[str, str, str, str]:
    """兼容旧版的闰月参数，同时使用统一计算实现。"""
    lunar_month = -abs(month) if is_leap else month
    return _calc_bazi_from_lunar(year, lunar_month, day, hour)


def main() -> None:
    """启动包含详细排盘、AI、反查、大运和流年分析的完整应用。"""
    _full_main()


if __name__ == "__main__":
    main()
