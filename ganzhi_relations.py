from itertools import combinations
from typing import List, Set

# 天干关系
TIANGAN_HE = {
    frozenset(['甲', '己']): '甲己合化土',
    frozenset(['乙', '庚']): '乙庚合化金',
    frozenset(['丙', '辛']): '丙辛合化水',
    frozenset(['丁', '壬']): '丁壬合化木',
    frozenset(['戊', '癸']): '戊癸合化火'
}
TIANGAN_KE = {
    ('庚', '甲'): '庚甲相克', ('辛', '乙'): '辛乙相克', ('壬', '丙'): '壬丙相克', ('癸', '丁'): '癸丁相克', ('甲', '戊'): '甲戊相克',
    ('乙', '己'): '乙己相克', ('丙', '庚'): '丙庚相克', ('丁', '辛'): '丁辛相克', ('戊', '壬'): '戊壬相克', ('己', '癸'): '己癸相克'
}

# 地支关系
DIZHI_SANHUI = {
    frozenset(['寅', '卯', '辰']): '寅卯辰三会木局',
    frozenset(['巳', '午', '未']): '巳午未三会火局',
    frozenset(['申', '酉', '戌']): '申酉戌三会金局',
    frozenset(['亥', '子', '丑']): '亥子丑三会水局'
}
DIZHI_SANHE = {
    frozenset(['申', '子', '辰']): '申子辰三合水局',
    frozenset(['亥', '卯', '未']): '亥卯未三合木局',
    frozenset(['寅', '午', '戌']): '寅午戌三合火局',
    frozenset(['巳', '酉', '丑']): '巳酉丑合金局'
}
DIZHI_HETUJU = {frozenset(['辰', '戌', '丑', '未']): '辰戌丑未合土局'}
DIZHI_LIUHE = {
    frozenset(['子', '丑']): '子丑合化土', frozenset(['寅', '亥']): '寅亥合化木', frozenset(['卯', '戌']): '卯戌合化火',
    frozenset(['辰', '酉']): '辰酉合化金', frozenset(['巳', '申']): '巳申合化水', frozenset(['午', '未']): '午未合化火'
}
DIZHI_BANHE = {
    frozenset(['申', '子']): '申子半合水局', frozenset(['子', '辰']): '子辰半合水局',
    frozenset(['亥', '卯']): '亥卯半合木局', frozenset(['卯', '未']): '卯未半合木局',
    frozenset(['寅', '午']): '寅午半合火局', frozenset(['午', '戌']): '午戌半合火局',
    frozenset(['巳', '酉']): '巳酉半合金局', frozenset(['酉', '丑']): '酉丑半合金局'
}
DIZHI_ANHE = {
    frozenset(['卯', '申']): '卯申暗合', frozenset(['午', '亥']): '午亥暗合',
    frozenset(['子', '巳']): '子巳暗合', frozenset(['寅', '午']): '寅午暗合'
}
DIZHI_GONGHE = {
    frozenset(['申', '辰']): '申辰拱合子', frozenset(['寅', '戌']): '寅戌拱合午',
    frozenset(['亥', '未']): '亥未拱合卯', frozenset(['巳', '丑']): '巳丑拱合酉'
}
DIZHI_XING = {
    frozenset(['丑', '未', '戌']): '丑未戌三刑',
    frozenset(['寅', '巳', '申']): '寅巳申三刑',
    frozenset(['子', '卯']): '子卯相刑'
}
DIZHI_ZIXING = {'辰': '辰辰自刑', '午': '午午自刑', '酉': '酉酉自刑', '亥': '亥亥自刑'}
DIZHI_LIUCHONG = {
    frozenset(['子', '午']): '子午相冲', frozenset(['丑', '未']): '丑未相冲', frozenset(['寅', '申']): '寅申相冲',
    frozenset(['卯', '酉']): '卯酉相冲', frozenset(['辰', '戌']): '辰戌相冲', frozenset(['巳', '亥']): '巳亥相冲'
}
DIZHI_LIUPO = {
    frozenset(['子', '酉']): '子酉相破', frozenset(['寅', '亥']): '寅亥相破', frozenset(['卯', '午']): '卯午相破',
    frozenset(['辰', '丑']): '辰丑相破', frozenset(['巳', '申']): '巳申相破', frozenset(['未', '戌']): '未戌相破'
}
DIZHI_LIUHAI = {
    frozenset(['子', '未']): '子未相害', frozenset(['丑', '午']): '丑午相害', frozenset(['寅', '巳']): '寅巳相害',
    frozenset(['申', '亥']): '申亥相害', frozenset(['卯', '辰']): '卯辰相害', frozenset(['酉', '戌']): '酉戌相害'
}

def _find_relations(items: List[str], relation_map: dict, size: int) -> List[str]:
    """通用关系查找器"""
    found = []
    unique_items = list(set(items))
    if len(unique_items) < size:
        return found
    
    for combo in combinations(unique_items, size):
        key = frozenset(combo)
        if key in relation_map:
            found.append(relation_map[key])
    return found

def analyze_ganzhi_relations(*pillars: str) -> str:
    """
    分析多个干支之间的作用关系
    遵循特定顺序：合 -> 克，六合 -> 三合 -> 土局 -> 三会 -> ...
    """
    if not pillars:
        return "天干：无\n地支：无"
        
    gans = [p[0] for p in pillars]
    zhis = [p[1] for p in pillars]
    
    # 1. 天干分析 (修正：移除used_gans，允许一个天干参与多种关系)
    tiangan_results = []
    
    # 天干合
    if len(gans) >= 2:
        # 使用list(set(gans))避免因重复天干导致重复查找
        for g1, g2 in combinations(list(set(gans)), 2):
            key = frozenset([g1, g2])
            if key in TIANGAN_HE:
                tiangan_results.append(TIANGAN_HE[key])
    
    # 天干克
    if len(gans) >= 2:
        # 遍历所有排列以检查克制关系
        for g1, g2 in combinations(gans, 2):
            if (g1, g2) in TIANGAN_KE:
                tiangan_results.append(TIANGAN_KE[(g1, g2)])
            elif (g2, g1) in TIANGAN_KE:
                tiangan_results.append(TIANGAN_KE[(g2, g1)])

    # 2. 地支分析 (修正：调整检查顺序)
    dizhi_results = []
    unique_zhis = list(set(zhis))
    
    # 六合
    dizhi_results.extend(_find_relations(unique_zhis, DIZHI_LIUHE, 2))
    
    # 三合
    san_he = _find_relations(unique_zhis, DIZHI_SANHE, 3)
    dizhi_results.extend(san_he)

    # 土局
    he_tu_ju = _find_relations(unique_zhis, DIZHI_HETUJU, 4)
    dizhi_results.extend(he_tu_ju)
    
    # 三会
    san_hui = _find_relations(unique_zhis, DIZHI_SANHUI, 3)
    dizhi_results.extend(san_hui)
    
    # 半合 (如果完整的三合局不存在)
    is_san_he_present = bool(san_he)
    if not is_san_he_present:
        dizhi_results.extend(_find_relations(unique_zhis, DIZHI_BANHE, 2))
        
    # 暗合
    dizhi_results.extend(_find_relations(unique_zhis, DIZHI_ANHE, 2))
    
    # 拱合
    dizhi_results.extend(_find_relations(unique_zhis, DIZHI_GONGHE, 2))
    
    # 刑 (三刑)
    dizhi_results.extend(_find_relations(unique_zhis, DIZHI_XING, 3))
    # 刑 (二刑)
    dizhi_results.extend(_find_relations(unique_zhis, DIZHI_XING, 2))
    
    # 自刑
    for zhi in DIZHI_ZIXING:
        if zhis.count(zhi) >= 2:
            dizhi_results.append(DIZHI_ZIXING[zhi])
            
    # 六冲
    dizhi_results.extend(_find_relations(unique_zhis, DIZHI_LIUCHONG, 2))
    
    # 六破
    dizhi_results.extend(_find_relations(unique_zhis, DIZHI_LIUPO, 2))
    
    # 六害
    dizhi_results.extend(_find_relations(unique_zhis, DIZHI_LIUHAI, 2))
    
    # 3. 格式化输出
    # 去重并保持顺序
    unique_tiangan_results = list(dict.fromkeys(tiangan_results))
    unique_dizhi_results = list(dict.fromkeys(dizhi_results))
    
    tiangan_str = f"天干：{', '.join(unique_tiangan_results) or '无作用关系'}"
    dizhi_str = f"地支：{', '.join(unique_dizhi_results) or '无作用关系'}"
    
    return f"{tiangan_str}\n{dizhi_str}"