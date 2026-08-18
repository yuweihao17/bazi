# 四柱八字计算器

默认入口是 `main.py`，它转发到完整的 `bazi_calculator.py`，不要再直接使用早期的简化排盘逻辑。

## 运行

```powershell
python main.py
```

支持：

- 公历和农历输入，包含闰月识别
- 四柱详细排盘：主星、十神、藏干、十二长生、自坐、纳音
- 原局、五柱大运、六柱流年的干支关系分析
- 起运时间、八步大运和十年流年查询
- 输入四柱后在 1800-2100 年反查匹配出生时间
- AI 原局分析、大运趋势、大运影响和具体流年分析

## AI 配置

AI 使用 OpenAI 兼容接口。至少设置一个 API 密钥环境变量：

```powershell
$env:BAZI_AI_API_KEY = "你的 API 密钥"
$env:BAZI_AI_BASE_URL = "https://api.siliconflow.cn/v1/"
$env:BAZI_AI_MODEL = "deepseek-ai/DeepSeek-V3.1"
python main.py
```

也兼容 `SILICONFLOW_API_KEY` 和 `OPENAI_API_KEY`。未配置 AI 时，基础排盘、大运、流年和反查仍可正常使用，选择 AI 分析时会给出提示并继续运行。
