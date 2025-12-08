#!/usr/bin/env python3
"""
LangChain Agent 性能问题演示（针对旧版API的批评）

注意：本演示基于对旧版 LangChain (0.x) Agent API 的批评。
旧版API（如 initialize_agent, AgentType.CHAT_ZERO_SHOT_REACT_DESCRIPTION）已在 LangChain 1.x 中废弃。

原批评的核心问题：
- 旧版 agent.run() 会触发多次隐藏的 API 调用，文档未明确说明
- 用户难以预测成本和性能影响

LangChain 1.x 的变化：
- 旧的高层 Agent API 已废弃
- 现在需要手动实现 Agent 循环或使用 LangGraph
- 这使得 API 调用变得更透明（如本代码中的两次 llm.invoke()）
- 但也意味着失去了原本的"简化"优势

本演示手动实现简化版 ReAct 循环，说明 Agent 模式的多次 API 调用特性。
"""

import os
import sys
import time

# 检查API密钥
if not os.environ.get("DEEPSEEK_API_KEY"):
    print("❌ 错误：请设置DEEPSEEK_API_KEY环境变量")
    sys.exit(1)

# 设置为DeepSeek API
os.environ["OPENAI_API_KEY"] = os.environ["DEEPSEEK_API_KEY"]
os.environ["OPENAI_API_BASE"] = "https://api.deepseek.com"

if not os.environ.get("SERPAPI_API_KEY"):
    print("⚠️  警告：未设置SERPAPI_API_KEY环境变量")
    print("   Agent演示需要SerpAPI密钥，可以从 https://serpapi.com 获取")
    print("   export SERPAPI_API_KEY='your-serpapi-key-here'")
    print()

print("=" * 80)
print("LangChain Agent 性能问题演示")
print("=" * 80)
print()

print("📌 原批评：Agent每个步骤都单独调用API，但文档未明确说明")
print("   (此批评主要针对旧版 LangChain 0.x 的 Agent API)")
print("-" * 80)
print()

print("🔴 旧版 LangChain Agent 的问题:")
print("代码演变 (展示API变化及透明度问题):")
print("""
# 旧API（已废弃）:
# from langchain.agents import load_tools, initialize_agent, AgentType
# agent = initialize_agent(tools, llm, agent=AgentType.CHAT_ZERO_SHOT_REACT_DESCRIPTION)

# 新API（LangChain 1.x）:
from langchain_openai import ChatOpenAI
from langchain_community.tools import Tool
from langchain_core.prompts import PromptTemplate

llm = ChatOpenAI(temperature=0, model="deepseek-chat")

# 定义工具
def calculator(expression: str) -> str:
    return str(eval(expression))

tools = [Tool(name="Calculator", func=calculator, description="for math")]

# 创建Agent需要手动实现ReAct循环...
# 即使是这样的简单示例，在新版本中也变得更加复杂！
""")

# 尝试运行Agent演示
try:
    from langchain_openai import ChatOpenAI
    from langchain_community.tools import Tool
    from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
    from langchain_core.messages import HumanMessage, AIMessage
    import json
    
    print("\n执行结果:")
    print("⏱️  开始计时...")
    start = time.time()
    
    llm = ChatOpenAI(
        temperature=0,
        model="deepseek-chat",
        openai_api_key=os.environ.get("DEEPSEEK_API_KEY"),
        openai_api_base="https://api.deepseek.com"
    )
    
    # 定义一个简单的计算工具
    def calculator(expression: str) -> str:
        """计算数学表达式"""
        try:
            result = eval(expression)
            return str(result)
        except Exception as e:
            return f"Error: {e}"
    
    # 手动实现简单的ReAct循环来演示多次API调用
    system_prompt = """You are a helpful assistant with access to a Calculator tool.
When you need to calculate something, respond ONLY with JSON: {"tool": "Calculator", "input": "expression"}
Otherwise, provide the final answer directly."""
    
    messages = [
        HumanMessage(content=system_prompt),
        HumanMessage(content="What is 25 multiplied by 4?")
    ]
    
    print("\n🤖 第1次API调用 - 让AI决定是否使用工具:")
    print("-" * 80)
    response1 = llm.invoke(messages)
    print(f"AI响应: {response1.content[:100]}...")
    api_calls = 1
    
    # 检查是否需要使用工具
    try:
        if "{" in response1.content and "tool" in response1.content.lower():
            # AI想使用工具
            messages.append(AIMessage(content=response1.content))
            
            # 执行计算
            result = calculator("25*4")
            messages.append(HumanMessage(content=f"Calculator result: {result}"))
            
            print(f"\n🤖 第2次API调用 - 提供工具结果，获取最终答案:")
            print("-" * 80)
            response2 = llm.invoke(messages)
            print(f"AI响应: {response2.content[:100]}...")
            api_calls += 1
            final_answer = response2.content
        else:
            final_answer = response1.content
    except:
        final_answer = response1.content
    
    print("-" * 80)
    
    elapsed = time.time() - start
    print(f"\n✅ 最终答案: {final_answer}")
    print(f"⏱️  总耗时: {elapsed:.2f}秒")
    print(f"📊 总API调用次数: {api_calls}次")
    
    print("\n💡 分析:")
    print(f"   1. 这个简单的数学问题需要{api_calls}次API调用")
    print("   2. 每次调用都会产生延迟和费用")
    print("   3. 在本演示中，两次 llm.invoke() 调用是明确可见的（透明）")
    print("   4. 但在旧版 LangChain 中，agent.run() 会隐藏这些调用")
    print("   5. LangChain 1.x 废弃了旧的 Agent API，现在需要手动实现")
    print("   6. 这使得调用更透明，但也失去了原本的简化优势")
    
except Exception as e:
    print(f"❌ 演示执行失败: {e}")
    print("\n💡 说明:")
    print("   本演示手动实现了简化版 ReAct 循环")
    print("   旧版 LangChain Agent API 已废弃，正好印证了 API 不稳定的批评")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 80)
print("\n🟢 如果用DeepSeek API直接实现类似功能:")
print("代码思路:")
print("""
from openai import OpenAI

client = OpenAI(
    api_key=os.environ.get("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com"
)

# 一次性构造完整的提示词，包含工具描述
system_prompt = '''
You are a helpful assistant with access to these tools:
1. Search: Search the web for information
2. Calculator: Perform mathematical calculations

When you need to use a tool, respond with JSON: {"tool": "tool_name", "input": "..."}
Otherwise, provide the final answer.
'''

# 第一次调用：让AI决定需要什么工具
messages = [
    {"role": "system", "content": system_prompt},
    {"role": "user", "content": "What is 25 multiplied by 4?"}
]

response1 = client.chat.completions.create(model="deepseek-chat", messages=messages)
# AI可能响应: {"tool": "Calculator", "input": "25 * 4"}

# 执行计算

# 第二次调用：提供计算结果，让AI给出最终答案
messages.append({"role": "assistant", "content": response1.choices[0].message.content})
messages.append({"role": "user", "content": "Calculation result: 100"})

response2 = client.chat.completions.create(model="deepseek-chat", messages=messages)
# AI给出最终答案
""")

print("\n💡 分析:")
print("   - 直接使用API时，你需要手动实现Agent循环")
print("   - 但你会清楚地知道每次API调用的时机和成本")
print("   - 旧版 LangChain 隐藏了这些细节，可能导致意外的高成本和慢响应")
print("   - LangChain 1.x 现在也需要类似的手动实现，但增加了额外的抽象层")

print("\n" + "=" * 80)
print("📊 关键问题总结")
print("=" * 80)
print("""
❌ 旧版 LangChain (0.x) Agent 的问题:
   1. agent.run() 隐藏了多次 API 调用（不透明）
   2. 一个简单查询可能产生3-5次API调用
   3. 文档中没有明确说明这一点
   4. 用户可能会惊讶于高昂的API费用和长时间的响应延迟
   5. AgentType.CHAT_ZERO_SHOT_REACT_DESCRIPTION 这样的命名很晦涩

🔄 LangChain 1.x 的变化:
   1. 旧的高层 Agent API (initialize_agent) 已废弃
   2. 现在需要手动实现 Agent 循环或使用 LangGraph
   3. API 调用变得更透明（如本演示中的明确 llm.invoke()）
   4. 但这也意味着失去了原本的"开箱即用"简化优势
   5. 开发者需要写更多代码来实现相同功能

✅ 透明度的重要性:
   - 开发者应该明确知道何时、为何调用API
   - 成本和性能影响应该是可预测的
   - 抽象不应该隐藏关键的性能特征
   - LangChain 1.x 在这方面有所改进，但代价是复杂度增加
""")

print("\n" + "=" * 80)
print("演示完成!")
print("=" * 80)
