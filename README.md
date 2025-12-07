# LangChain v1.0 Few-Shot Learning 示例

## Quickstart on macOS

```
python3 -m venv .venv

source .venv/bin/activate

pip install --upgrade pip

pip install langchain

python langchain_v1_fewshot_example.py

deactivate

```

## 概述

本项目展示了在 LangChain v1.0 中实现 few-shot learning 的多种方式,并对比了技术雷达对 LangChain 的评价在 v1.0 中的适用性。

## 关键发现

### 技术雷达评价的适用性

**ThoughtWorks 技术雷达的批评在 v1.0 中:**

✅ **已改进**:
- 简化了包结构,核心功能与遗留功能分离
- 聚焦于 `create_agent` 核心抽象
- 基于 LangGraph 的稳定运行时
- 承诺在 2.0 前无破坏性变更

❌ **仍然存在**:
- `FewShotPromptTemplate` 等组件的 API 设计复杂度未改变
- 需要导入多个组件、定义多个模板变量的问题依旧
- 过度抽象,掩盖底层实现的问题在某些组件中仍存在

### Few-Shot Learning 问题

文档中讨论的 few-shot learning 案例问题**在 v1.0 中依然存在**:

- `FewShotPromptTemplate` 仍保留在 `langchain_core.prompts` 中
- API 设计基本未变
- 仍需要多层嵌套的模板定义

**但是**: LangChain v1.0 的重心已转移,不再推荐使用这些复杂的提示模板组件。

## 文件说明

1. **langchain_v1_fewshot_example.py**
   - 对比演示 4 种实现 few-shot learning 的方式
   - 纯教学示例,无需 API key
   - 展示代码复杂度对比

2. **langchain_v1_complete_example.py**
   - 完整可运行示例
   - 包含实际 LLM 调用
   - 需要 API key

## 安装要求

### 基础安装

```bash
# 安装核心包
pip install langchain --break-system-packages

# 如果要运行实际 LLM 调用示例,选择安装一个:
pip install langchain-openai --break-system-packages  # OpenAI
# 或
pip install langchain-anthropic --break-system-packages  # Anthropic
```

### Python 版本要求

- Python 3.10+ (LangChain v1.0 不再支持 Python 3.9)

## 运行步骤

### 方式 1: 仅查看对比示例(无需 API key)

```bash
python langchain_v1_fewshot_example.py
```

这个示例会展示:
- 原生 Python 实现
- ChatPromptTemplate 实现
- FewShotChatMessagePromptTemplate 实现
- 在 v1.0 Agent 中的使用方式
- 各方式的对比分析

### 方式 2: 运行完整示例(需要 API key)

```bash
# 设置 API key (选择一个)
export OPENAI_API_KEY="your-openai-api-key"
# 或
export ANTHROPIC_API_KEY="your-anthropic-api-key"

# 运行示例
python langchain_v1_complete_example.py
```

这个示例会:
- 展示所有实现方式
- 实际调用 LLM 测试效果
- 显示详细对比分析

## 推荐方式

基于 LangChain v1.0 的设计理念,推荐以下方式:

### 1. 简单场景 - 原生 Python

```python
def generate_few_shot_prompt(pairs):
    prompt = "Give the antonym of every input\n\n"
    for pair in pairs:
        prompt += f"Input: {pair['input']}\nOutput: {pair['output']}\n\n"
    return prompt

pairs = [
    {"input": "happy", "output": "sad"},
    {"input": "tall", "output": "short"},
    # ... 更多示例
]

prompt = generate_few_shot_prompt(pairs)
```

**优点**: 简单、直观、无需学习额外 API

### 2. LangChain 场景 - ChatPromptTemplate

```python
from langchain_core.prompts import ChatPromptTemplate

examples = """Input: happy
Output: sad

Input: tall
Output: short"""

prompt = ChatPromptTemplate.from_messages([
    ("system", f"Give the antonym of every input\n\n{examples}"),
    ("human", "Input: {word}\nOutput:")
])
```

**优点**: 平衡了简洁性和 LangChain 集成

### 3. LangChain v1.0 Agent - system_prompt

```python
from langchain.agents import create_agent

system_prompt = """You are an antonym assistant.

Examples:
Input: happy → sad
Input: tall → short

Give the antonym following the format."""

agent = create_agent(
    model="claude-sonnet-4-5-20250929",
    tools=[],
    system_prompt=system_prompt
)
```

**优点**: 符合 v1.0 设计理念,简洁高效

### ❌ 不推荐 - FewShotPromptTemplate

```python
# 不推荐:代码过于复杂
from langchain_core.prompts import PromptTemplate, FewShotPromptTemplate

example_prompt = PromptTemplate(
    input_variables=["input", "output"],
    template="Input: {input}\nOutput: {output}"
)

prompt = FewShotPromptTemplate(
    examples=examples,
    example_prompt=example_prompt,
    prefix="Give the antonym of every input",
    suffix="Input: {adjective}\nOutput:",
    input_variables=["adjective"]
)
```

**缺点**: 
- 需要导入多个组件
- 需要定义多个模板
- 代码复杂度高
- 违反"容易让人把事情做对"的原则

## 代码复杂度对比

| 实现方式 | 代码行数 | 导入数量 | 模板层次 | 推荐度 |
|---------|---------|---------|---------|--------|
| 原生 Python | 5-8 | 0 | 0 | ⭐⭐⭐⭐⭐ |
| ChatPromptTemplate | 8-12 | 1 | 1 | ⭐⭐⭐⭐ |
| v1.0 Agent 风格 | 10-15 | 1-2 | 1 | ⭐⭐⭐⭐⭐ |
| FewShotPromptTemplate | 20-30 | 2-3 | 2-3 | ⭐ |

## 总结

1. **技术雷达的批评部分仍然适用**: 
   - FewShotPromptTemplate 等组件的设计问题未解决
   - 但 v1.0 通过架构转型选择了新的方向

2. **Few-shot learning 问题依然存在**:
   - 文档中的复杂性问题在 v1.0 中未改善
   - 但 v1.0 提供了更简洁的替代方案

3. **实用建议**:
   - 优先使用原生 Python 或 ChatPromptTemplate
   - 在 Agent 场景中,直接在 system_prompt 包含示例
   - 避免使用 FewShotPromptTemplate
   - 关注 v1.0 的新方向(create_agent + LangGraph)

4. **LangChain v1.0 的价值**:
   - 不在于提示模板工具
   - 而在于 Agent 抽象和 LangGraph 运行时
   - 提供了生产级的持久化、可观测性等特性

## 参考资源

- [LangChain v1.0 官方公告](https://blog.langchain.com/langchain-langgraph-1dot0/)
- [LangChain v1.0 迁移指南](https://docs.langchain.com/oss/python/migrate/langchain-v1)
- [LangChain v1.0 文档](https://docs.langchain.com/)
- [ThoughtWorks 技术雷达](https://www.thoughtworks.com/radar)

## 许可

示例代码仅供学习参考使用。