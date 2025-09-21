#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
天干地支作用关系分析模块
"""

def analyze_ganzhi_relations(year_pillar: str, month_pillar: str, day_pillar: str, hour_pillar: str) -> str:
    """
    分析八字中天干地支的作用关系
    
    Args:
        year_pillar: 年柱
        month_pillar: 月柱
        day_pillar: 日柱
        hour_pillar: 时柱
        
    Returns:
        str: 作用关系分析结果
    """
    # 提取天干和地支
    tiangan = [year_pillar[0], month_pillar[0], day_pillar[0], hour_pillar[0]]
    dizhi = [year_pillar[1], month_pillar[1], day_pillar[1], hour_pillar[1]]
    
    result = []
    result.append("作用关系分析：")
    result.append("-" * 50)
    
    # 天干关系分析
    tiangan_relations = analyze_tiangan_relations(tiangan)
    if tiangan_relations:
        result.append("天干关系：" + "，".join(tiangan_relations))
    
    # 地支关系分析
    dizhi_relations = analyze_dizhi_relations(dizhi)
    if dizhi_relations:
        result.append("地支关系：" + "，".join(dizhi_relations))
    
    if not tiangan_relations and not dizhi_relations:
        result.append("未发现明显的作用关系")
    
    return "\n".join(result)


def analyze_tiangan_relations(tiangan: list) -> list:
    """
    分析天干关系：先合再克
    """
    relations = []
    tiangan_set = set(tiangan)
    
    # 天干相合关系 - 按顺序检查
    he_pairs = [
        (['甲', '己'], '甲己合化土'),
        (['乙', '庚'], '乙庚合化金'),
        (['丙', '辛'], '丙辛合化水'),
        (['丁', '壬'], '丁壬合化木'),
        (['戊', '癸'], '戊癸合化火')
    ]
    
    for pair, desc in he_pairs:
        if pair[0] in tiangan_set and pair[1] in tiangan_set:
            relations.append(desc)
    
    # 天干相克关系 - 按顺序检查
    ke_pairs = [
        (['甲', '戊'], '甲戊相克'),
        (['乙', '己'], '乙己相克'),
        (['丙', '庚'], '丙庚相克'),
        (['丁', '辛'], '丁辛相克'),
        (['戊', '壬'], '戊壬相克'),
        (['己', '癸'], '己癸相克'),
        (['庚', '甲'], '庚甲相克'),
        (['辛', '乙'], '辛乙相克'),
        (['壬', '丙'], '壬丙相克'),
        (['癸', '丁'], '癸丁相克')
    ]
    
    for pair, desc in ke_pairs:
        if pair[0] in tiangan_set and pair[1] in tiangan_set:
            relations.append(desc)
    
    return relations


def analyze_dizhi_relations(dizhi: list) -> list:
    """
    分析地支关系：按顺序检查六合、三合、三会、暗合、拱合、相刑、六冲、六破、六害
    """
    relations = []
    dizhi_set = set(dizhi)
    
    # 1. 六合 - 避免重复
    liuhe_relations = [
        (['子', '丑'], '子丑合化土'),
        (['寅', '亥'], '寅亥合化木'),
        (['卯', '戌'], '卯戌合化火'),
        (['辰', '酉'], '辰酉合化金'),
        (['巳', '申'], '巳申合化水'),
        (['午', '未'], '午未合化火')
    ]
    
    for pair, desc in liuhe_relations:
        if pair[0] in dizhi_set and pair[1] in dizhi_set:
            relations.append(desc)
    
    # 2. 三合和半合（三合优先）
    sanhe_checks = [
        (['寅', '午', '戌'], '寅午戌合火局'),
        (['申', '子', '辰'], '申子辰合水局'),
        (['巳', '酉', '丑'], '巳酉丑合金局'),
        (['亥', '卯', '未'], '亥卯未合木局')
    ]
    
    # 记录已经形成三合的组合，避免重复输出半合
    formed_sanhe = set()
    
    for sanhe_list, desc in sanhe_checks:
        if all(zhi in dizhi_set for zhi in sanhe_list):
            relations.append(desc)
            # 记录已经形成的三合，用于后面排除半合
            for i in range(len(sanhe_list)):
                for j in range(i+1, len(sanhe_list)):
                    formed_sanhe.add(tuple(sorted([sanhe_list[i], sanhe_list[j]])))
    
    # 土局特殊处理 - 需要辰戌丑未四个都有，或者至少有三个形成特定组合
    tu_zhi = ['辰', '戌', '丑', '未']
    found_tu = [zhi for zhi in tu_zhi if zhi in dizhi_set]
    
    # 土局成立的条件：
    # 1. 四个土支都有：辰戌丑未
    # 2. 或者有辰戌冲、丑未冲的组合形成特殊格局
    if len(found_tu) == 4:
        relations.append('辰戌丑未合土局')
    elif len(found_tu) == 3:
        # 三个土支的情况，需要特定组合才能成土局
        # 这里可以根据具体的命理规则来判断
        # 暂时不添加土局判断，避免误判
        pass
    
    # 3. 三会
    sanhui_checks = [
        (['寅', '卯', '辰'], '寅卯辰三会木局'),
        (['巳', '午', '未'], '巳午未三会火局'),
        (['申', '酉', '戌'], '申酉戌三会金局'),
        (['亥', '子', '丑'], '亥子丑三会水局')
    ]
    
    for sanhui_list, desc in sanhui_checks:
        if all(zhi in dizhi_set for zhi in sanhui_list):
            relations.append(desc)
    
    # 4. 半合关系（只有在不形成三合的情况下才输出）
    banhe_relations = [
        (['申', '子'], '申子半合水局'),
        (['子', '辰'], '子辰半合水局'),
        (['寅', '午'], '寅午半合火局'),
        (['午', '戌'], '午戌半合火局'),
        (['亥', '卯'], '亥卯半合木局'),
        (['卯', '未'], '卯未半合木局'),
        (['巳', '酉'], '巳酉半合金局'),
        (['酉', '丑'], '酉丑半合金局')
    ]
    
    # 使用集合来去重
    added_banhe = set()
    for pair, desc in banhe_relations:
        if (pair[0] in dizhi_set and pair[1] in dizhi_set and 
            tuple(sorted(pair)) not in formed_sanhe):
            # 避免重复添加相同的半合关系
            sorted_pair = tuple(sorted(pair))
            if sorted_pair not in added_banhe:
                relations.append(desc)
                added_banhe.add(sorted_pair)
    
    # 5. 暗合
    anhe_relations = [
        (['卯', '申'], '卯申暗合'),
        (['午', '亥'], '午亥暗合'),
        (['子', '巳'], '子巳暗合'),
        (['寅', '午'], '寅午暗合')
    ]
    
    for pair, desc in anhe_relations:
        if pair[0] in dizhi_set and pair[1] in dizhi_set:
            relations.append(desc)
    
    # 6. 拱合
    gonghe_checks = [
        (['申', '辰'], '申辰拱合子'),
        (['寅', '戌'], '寅戌拱合午'),
        (['亥', '未'], '亥未拱合卯'),
        (['巳', '丑'], '巳丑拱合酉')
    ]
    
    for gonghe_list, desc in gonghe_checks:
        if all(zhi in dizhi_set for zhi in gonghe_list):
            relations.append(desc)
    
    # 7. 相刑
    # 子卯相刑
    if '子' in dizhi_set and '卯' in dizhi_set:
        relations.append('子卯相刑')
    
    # 三刑
    sanxing_checks = [
        (['寅', '巳', '申'], '寅巳申三刑'),
        (['丑', '未', '戌'], '丑未戌三刑')
    ]
    
    for sanxing_list, desc in sanxing_checks:
        if all(zhi in dizhi_set for zhi in sanxing_list):
            relations.append(desc)
    
    # 自刑
    zixing_zhi = ['辰', '午', '酉', '亥']
    zhi_count = {}
    for zhi in dizhi:
        zhi_count[zhi] = zhi_count.get(zhi, 0) + 1
    
    for zhi, count in zhi_count.items():
        if count >= 2 and zhi in zixing_zhi:
            relations.append(f'{zhi}{zhi}自刑')
    
    # 8. 六冲
    liuchong_relations = [
        (['子', '午'], '子午相冲'),
        (['丑', '未'], '丑未相冲'),
        (['寅', '申'], '寅申相冲'),
        (['卯', '酉'], '卯酉相冲'),
        (['辰', '戌'], '辰戌相冲'),
        (['巳', '亥'], '巳亥相冲')
    ]
    
    for pair, desc in liuchong_relations:
        if pair[0] in dizhi_set and pair[1] in dizhi_set:
            relations.append(desc)
    
    # 9. 六破
    liupo_relations = [
        (['子', '酉'], '子酉相破'),
        (['寅', '亥'], '寅亥相破'),
        (['卯', '午'], '卯午相破'),
        (['辰', '丑'], '辰丑相破'),
        (['巳', '申'], '巳申相破'),
        (['未', '戌'], '未戌相破')
    ]
    
    for pair, desc in liupo_relations:
        if pair[0] in dizhi_set and pair[1] in dizhi_set:
            relations.append(desc)
    
    # 10. 六害
    liuhai_relations = [
        (['子', '未'], '子未相害'),
        (['丑', '午'], '丑午相害'),
        (['寅', '巳'], '寅巳相害'),
        (['申', '亥'], '申亥相害'),
        (['卯', '辰'], '卯辰相害'),
        (['酉', '戌'], '酉戌相害')
    ]
    
    for pair, desc in liuhai_relations:
        if pair[0] in dizhi_set and pair[1] in dizhi_set:
            relations.append(desc)
    
    return relations


# 测试函数
if __name__ == "__main__":
    # 测试2004年案例
    year_pillar = "癸未"
    month_pillar = "乙丑"
    day_pillar = "戊申"
    hour_pillar = "乙卯"
    
    print("测试八字：癸未 乙丑 戊申 乙卯")
    print("=" * 50)
    result = analyze_ganzhi_relations(year_pillar, month_pillar, day_pillar, hour_pillar)
    print(result)