#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
AI 八字解读模块
- 使用 SiliconFlow API 和 DeepSeek 模型
- 提供流式输出的 AI 解读功能
- 通过会话管理实现上下文连续解读
"""

import sys
from typing import List, Dict, Any, Optional, Set

# 尝试导入 OpenAI，如果失败则设为 None
try:
    from openai import OpenAI
except ImportError:
    OpenAI = None

import bazi_common

class AIAnalyzer:
    """
    一个管理与AI模型的会话、生成八字解读的类。
    通过维护一个对话历史，实现连续、有上下文的分析。
    """
    API_KEY: str = "sk-wcuxdzqlzbbcrgrpbcweehgcbofyhroupikdlbhlpzcikply"
    BASE_URL: str = "https://api.siliconflow.cn/v1/"
    MODEL_NAME: str = "deepseek-ai/DeepSeek-V3.1"

    PROMPT_TEMPLATES: Dict[str, str] = {
        "bazi_yuanju": """
        请作为一位专业的命理分析师，根据以下【四柱八字原局】信息，进行一次详细、精准的静态分析。
        
        **你的任务严格限制在分析出生时刻的静态信息，禁止推演、计算或提及任何未来的大运、流年信息。**

        请重点分析以下几个方面：
        1. **五行强弱**: 分析命局中金、木、水、火、土的分布与力量对比。
        2. **格局喜忌**: 判断命局的核心格局（如身强/身弱，以及特殊格局），并明确指出喜用神和忌神。
        3. **性格特质**: 基于日主和十神组合，深入分析命主的性格、优点和潜在的缺点。
        4. **六亲关系**: 简要分析与父母、兄弟、配偶、子女的关系。
        5. **原局解读**: 综合分析原局所体现的事业潜力、财富层次和健康隐患。

        八字信息如下：
        - 性别：{gender}
        - 年柱: {year_pillar}
        - 月柱: {month_pillar}
        - 日柱: {day_pillar} (日主: {day_master})
        - 时柱: {hour_pillar}
        - 原局干支作用关系: {yuanju_relations}

        **请直接开始分析，不要在回答的开头或结尾添加任何自我介绍、问候语或免责声明。**
        """,
        
        "bazi_dayun_trend": """
        我们已经对命主的原局进行了初步分析。现在，请你基于之前的分析，对命主未来八步大运的整体人生趋势进行宏观展望。

        **个人信息**:
        - 性别：{gender}
        - 日主（元神）：{day_master}

        **八字原局**:
        - 年柱：{year_pillar}
        - 月柱：{month_pillar}
        - 日柱：{day_pillar}
        - 时柱：{hour_pillar}

        **未来八步大运**:
        {dayun_list_str}

        **分析要求**:
        1.  **阶段分析**: 结合每一步大运，简要分析其干支与原局的相互作用，预测青年、中年、晚年等不同人生阶段可能出现的机遇、挑战以及人生重点。
        2.  **总结建议**: 给出一些宏观的人生建议。
        
        请不要重复原局的性格、格局等基础信息，直接进入大运趋势分析。
        **请直接开始分析，不要在回答的开头或结尾添加任何自我介绍、问候语或免责声明。**
        """,

        "dayun_yingxiang": """
        在之前对原局分析的基础上，现在请深入解读当前这步大运对命局的具体影响。

        八字及大运信息如下：
        - 性别：{gender}
        - 原局四柱: {year_pillar} {month_pillar} {day_pillar} {hour_pillar}
        - 当前大运: {dayun_pillar} (从 {dayun_start_age} 岁到 {dayun_end_age} 岁，即公历 {start_year} 年至 {end_year} 年)
        - 五柱（原局+大运）作用关系: {dayun_relations}

        **分析必须严格限制在 {start_year} 年至 {end_year} 年这个时间范围内，禁止提及此范围之外的任何年份。**
        请重点分析这十年大运期间，命主可能面临的主要机遇和挑战，尤其是在事业、财运、感情等方面可能发生的变化。请避免重复原局的基础分析。
        **请直接开始分析，不要在回答的开头或结尾添加任何自我介绍、问候语或免责声明。**
        """,

        "liunian_fenxi": """
        在之前对命局和大运分析的基础上，请你现在聚焦于某一具体流年进行详细分析。

        完整信息如下：
        - 性别：{gender}
        - 原局四柱: {year_pillar} {month_pillar} {day_pillar} {hour_pillar}
        - 当前大运: {dayun_pillar} (从 {dayun_start_age} 岁到 {dayun_end_age} 岁)
        - 所查流年: {liunian_pillar} ({liunian_year}年, 命主 {liunian_age} 岁)
        - 六柱（原局+大运+流年）作用关系: {liunian_relations}

        请重点解读在特定大运的这个流年里，命主具体会遇到哪些事件或运势变化。分析应结合流年、大运与原局的共同作用，给出具体、有针对性的分析和建议。不要重复之前已经分析过的原局和大运的整体情况。
        **请直接开始分析，不要在回答的开头或结尾添加任何自我介绍、问候语或免责声明。**
        """
    }

    def __init__(self):
        if OpenAI is None:
            raise ImportError("openai 库未安装，请执行 'pip install openai' 进行安装。")
        self.API_KEY = self.API_KEY # 确保 API_KEY 被正确设置
        self.BASE_URL = self.BASE_URL # 确保 BASE_URL 被正确设置
        self.MODEL_NAME = self.MODEL_NAME # 确保 MODEL_NAME 被正确设置
        self.PROMPT_TEMPLATES = self.PROMPT_TEMPLATES # 确保 PROMPT_TEMPLATES 被正确设置
        self.client = OpenAI(base_url=self.BASE_URL, api_key=self.API_KEY)
        self.history: List[Dict[str, str]] = []
        self.completed_analyses: Set[str] = set() # 状态跟踪器

    def _get_prompt(self, analysis_type: str) -> Optional[str]:
        """安全地获取提示词模板。"""
        return self.PROMPT_TEMPLATES.get(analysis_type)

    def has_analysis_been_done(self, analysis_type: str) -> bool:
        """检查特定类型的分析是否已在状态跟踪器中。"""
        return analysis_type in self.completed_analyses

    def reset_history(self) -> None:
        """清空对话历史和状态跟踪器，开始新的分析会话。"""
        self.history = []
        self.completed_analyses.clear()

    def _interpret_stream(self, analysis_type: str, data: Dict[str, Any], is_dependency: bool = False) -> bool:
        """内部函数，执行API调用并处理流式输出。"""
        prompt_template = self._get_prompt(analysis_type)
        if not prompt_template:
            print(f"❌ 错误：未找到分析类型 '{analysis_type}' 的模板。")
            return False

        try:
            # 填充模板，对于缺失的键，.format会报错，这可以帮助调试
            prompt = prompt_template.format(**data)
            
            # 将当前请求添加到历史记录中
            current_messages = self.history + [{"role": "user", "content": prompt}]
            
            if not is_dependency:
                print("\n" + "=" * 20 + " AI 智能解读 " + "=" * 20)
            print("正在思考中，请稍候...")
            
            response = self.client.chat.completions.create(
                model=self.MODEL_NAME,
                messages=current_messages,
                stream=True,
                max_tokens=4096,
            )
            
            full_content = ""
            sys.stdout.flush()
            
            line_buffer = ""
            disclaimer_keywords = ["DeepSeek", "仅供参考", "玄学", "命理非", "命理是", "提醒您", "AI生成"]

            for chunk in response:
                if chunk.choices and chunk.choices[0].delta and chunk.choices[0].delta.content:
                    content_piece = chunk.choices[0].delta.content
                    line_buffer += content_piece
                    
                    while '\n' in line_buffer:
                        line, line_buffer = line_buffer.split('\n', 1)
                        if not any(keyword in line for keyword in disclaimer_keywords):
                            sys.stdout.write(line + '\n')
                            sys.stdout.flush()
                            full_content += line + '\n'
            
            if line_buffer and not any(keyword in line_buffer for keyword in disclaimer_keywords):
                sys.stdout.write(line_buffer)
                sys.stdout.flush()
                full_content += line_buffer
            
            if not full_content.endswith('\n'):
                print()

            if not is_dependency:
                print("=" * 52)
            
            if not full_content.strip():
                print("AI 未返回有效内容，可能是网络问题或 API 限制。")
                return False
            else:
                self.history.append({"role": "user", "content": prompt})
                self.history.append({"role": "assistant", "content": full_content.strip()})
                self.completed_analyses.add(analysis_type) # 记录已完成的分析
                return True
                
        except KeyError as e:
            print(f"\n❌ AI 解读时发生错误：缺少必要的参数来填充模板 - {e}", file=sys.stderr)
            return False
        except Exception as e:
            print(f"\n❌ AI 解读时发生错误：{e}", file=sys.stderr)
            return False

    def get_interpretation(self, analysis_type: str, data: Dict[str, Any], dependencies: List[str] = []) -> None:
        """
        公开方法，处理用户交互和依赖分析。
        """
        do_ai_analysis = bazi_common.read_choice("\n是否需要 AI 智能解读？(y/n): ", ['y', 'n'])
        if do_ai_analysis.lower() != 'y':
            return

        # 检查并执行依赖分析
        for dep in dependencies:
            if not self.has_analysis_been_done(dep):
                print(f"\n---\n为了进行当前分析，需要先进行 [{dep.replace('bazi_', '').replace('_', ' ')}] 的基础分析。")
                if not self._interpret_stream(dep, data, is_dependency=True):
                    print(f"❌ 依赖分析 [{dep}] 失败，无法继续。")
                    return

        # 执行当前请求的分析
        self._interpret_stream(analysis_type, data)