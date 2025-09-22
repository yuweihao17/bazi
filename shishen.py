#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
十神（Shishen）计算模块
- 根据天干的五行和阴阳关系，计算十神
- 提供地支藏干（Hidden Stems）信息
"""

# 藏干信息
HIDDEN_STEMS = {
    '子': ['癸'], '丑': ['己', '癸', '辛'], '寅': ['甲', '丙', '戊'], '卯': ['乙'],
    '辰': ['戊', '乙', '癸'], '巳': ['丙', '庚', '戊'], '午': ['丁', '己'], '未': ['己', '丁', '乙'],
    '申': ['庚', '壬', '戊'], '酉': ['辛'], '戌': ['戊', '辛', '丁'], '亥': ['壬', '甲']
}

# 天干五行
GAN_WUXING = {
    '甲': '木', '乙': '木', '丙': '火', '丁': '火', '戊': '土',
    '己': '土', '庚': '金', '辛': '金', '壬': '水', '癸': '水'
}

# 天干阴阳
GAN_YINYANG = {
    '甲': '阳', '丙': '阳', '戊': '阳', '庚': '阳', '壬': '阳',
    '乙': '阴', '丁': '阴', '己': '阴', '辛': '阴', '癸': '阴'
}

# 五行生克关系
WUXING_SHENG = {'金': '水', '水': '木', '木': '火', '火': '土', '土': '金'}
WUXING_KE = {'金': '木', '木': '土', '土': '水', '水': '火', '火': '金'}

# 十神定义表
# 键: (关系, 阴阳属性)
# 关系: 我克, 克我, 我生, 生我, 同我
# 阴阳属性: 同, 异
SHISHEN_MAP = {
    ('克我', '异'): '正官', ('克我', '同'): '七杀',
    ('我克', '异'): '正财', ('我克', '同'): '偏财',
    ('生我', '异'): '正印', ('生我', '同'): '偏印',
    ('同我', '异'): '劫财', ('同我', '同'): '比肩',
    ('我生', '异'): '伤官', ('我生', '同'): '食神',
}

def get_shishen(other_gan: str, day_master_gan: str) -> str:
    """
    计算一个天干相对于日主天干的十神关系
    
    Args:
        other_gan: 待计算关系的天干
        day_master_gan: 日主的天干（日元）
        
    Returns:
        str: 十神名称
    """
    if other_gan not in GAN_WUXING or day_master_gan not in GAN_WUXING:
        return ""

    if other_gan == day_master_gan:
        return "比肩" # 日主自身为比肩

    other_wuxing = GAN_WUXING[other_gan]
    master_wuxing = GAN_WUXING[day_master_gan]
    
    other_yinyang = GAN_YINYANG[other_gan]
    master_yinyang = GAN_YINYANG[day_master_gan]

    relation = ""
    if WUXING_KE.get(master_wuxing) == other_wuxing:
        relation = "我克"
    elif WUXING_KE.get(other_wuxing) == master_wuxing:
        relation = "克我"
    elif WUXING_SHENG.get(master_wuxing) == other_wuxing:
        relation = "我生"
    elif WUXING_SHENG.get(other_wuxing) == master_wuxing:
        relation = "生我"
    elif other_wuxing == master_wuxing:
        relation = "同我"

    yinyang_relation = "同" if other_yinyang == master_yinyang else "异"
    
    return SHISHEN_MAP.get((relation, yinyang_relation), "")