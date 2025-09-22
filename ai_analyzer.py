#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
AI 八字解读模块
- 使用 SiliconFlow API 和 DeepSeek 模型
- 提供流式输出的 AI 解读功能
"""

import sys
from typing import List, Dict, Any, Optional

# 尝试导入 OpenAI，如果失败则设为 None
try:
    from openai import OpenAI
except ImportError:
    OpenAI = None

import bazi_common

# --- 配置信息 ---
API_KEY: str = "sk-wcuxdzqlzbbcrgrpbcweehgcbofyhroupikdlbhlpzcikply"
BASE_URL: str = "https://api.siliconflow.cn/v1/"
MODEL_NAME: str = "deepseek-ai/DeepSeek-V3.1"

# --- 提示词模板 ---
PROMPT_TEMPLATES: Dict[str, str] = {
    "bazi_yuanju": """
    请作为一位专业的命理分析师，根据以下四柱八字原局信息，进行解读。
    请重点分析日主的性格、事业、财运、健康等方面，并指出原局中的主要优势和潜在问题。
    
    八字信息如下：
    - 性别：{gender}
    - 年柱: {year_pillar}
    - 月柱: {month_pillar}
    - 日柱: {day_pillar} (日主: {day_master})
    - 时柱: {hour_pillar}
    - 原局干支作用关系: {relations}

    请以自然、流畅的语言进行解读，避免过于专业化的术语堆砌。
    """,
    
    "dayun_yingxiang": """
    请作为一位专业的命理分析师，解读当前大运对八字原局的影响。
    请分析这十年大运期间，命主可能面临的主要机遇和挑战，尤其是在事业、财运、感情等方面可能发生的变化。

    八字及大运信息如下：
    - 性别：{gender}
    - 原局四柱: {year_pillar} {month_pillar} {day_pillar} {hour_pillar}
    - 当前大运: {dayun_pillar}
    - 五柱（原局+大运）作用关系: {relations}

    请结合作用关系的变化进行分析。
    """,

    "liunian_fenxi": """
    请作为一位专业的命理分析师，对当前流年进行详细分析。
    请重点解读在 {dayun_pillar} 大运的 {liunian_pillar} 流年，命主具体会遇到哪些事件或运势变化。
    分析应结合流年、大运与原局共同作用产生的刑冲合化等关系。

    完整信息如下：
    - 性别：{gender}
    - 原局四柱: {year_pillar} {month_pillar} {day_pillar} {hour_pillar}
    - 当前大运: {dayun_pillar}
    - 当前流年: {liunian_pillar}
    - 六柱（原局+大运+流年）作用关系: {relations}

    请给出具体、有针对性的分析和建议。
    """
}

def get_ai_interpretation(analysis_type: str, data: Dict[str, Any]) -> None:
    """
    先询问用户，然后调用 AI 模型获取八字解读，并以流式输出打印到控制台。

    Args:
        analysis_type: 分析类型 ('bazi_yuanju', 'dayun_yingxiang', 'liunian_fenxi')。
        data: 包含所有填充模板所需信息的字典。
    """
    # 询问用户是否需要AI解读
    do_ai_analysis = bazi_common.read_choice("\n是否需要 AI 智能解读？(y/n): ", ['y', 'n'])
    if do_ai_analysis.lower() != 'y':
        return

    if OpenAI is None:
        print("\n❌ AI 解读功能需要 openai 库。请先安装：pip install openai")
        return

    if analysis_type not in PROMPT_TEMPLATES:
        print("❌ 错误：无效的 AI 分析类型。")
        return

    try:
        client = OpenAI(base_url=BASE_URL, api_key=API_KEY)
        
        prompt = PROMPT_TEMPLATES[analysis_type].format(**data)
        messages = [{"role": "user", "content": prompt}]
        
        print("\n" + "=" * 20 + " AI 智能解读 " + "=" * 20)
        print("正在思考中，请稍候...")
        
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=messages,
            stream=True,
            max_tokens=4096,
        )
        
        full_content = ""
        for chunk in response:
            if chunk.choices and chunk.choices[0].delta and chunk.choices[0].delta.content:
                content_piece = chunk.choices[0].delta.content
                full_content += content_piece
                print(content_piece, end='', flush=True)
        
        print("\n" + "=" * 52)
        
        if not full_content.strip():
            print("AI 未返回有效内容，可能是网络问题或 API 限制。")

    except ImportError:
        print("\n❌ AI 解读功能需要 openai 库。请先安装：pip install openai")
    except Exception as e:
        print(f"\n❌ AI 解读时发生错误：{e}", file=sys.stderr)