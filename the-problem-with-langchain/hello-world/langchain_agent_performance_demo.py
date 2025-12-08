#!/usr/bin/env python3
"""
LangChain Agent 性能问题演示
演示文章中提到的缺点4: 每个Thought/Action/Observation步骤都单独调用API，导致性能问题
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

print("📌 缺点4: Agent每个步骤都单独调用API，但文档未明确说明")
print("-" * 80)
print()

print("🔴 LangChain Agent方式:")
print("代码:")
print("""
from langchain.agents import load_tools, initialize_agent, AgentType
from langchain_openai import ChatOpenAI, OpenAI

chat = ChatOpenAI(
    temperature=0,
    model="deepseek-chat",
    openai_api_base="https://api.deepseek.com"
)
llm = OpenAI(
    temperature=0,
    model="deepseek-chat",
    openai_api_base="https://api.deepseek.com"
)
tools = load_tools(["serpapi", "llm-math"], llm=llm)

agent = initialize_agent(
    tools, 
    chat, 
    agent=AgentType.CHAT_ZERO_SHOT_REACT_DESCRIPTION, 
    verbose=True
)

# 注意：这个查询会产生多次API调用！
result = agent.run("What is 25 multiplied by 4?")
""")

if os.environ.get("SERPAPI_API_KEY"):
    try:
        from langchain.agents import load_tools, initialize_agent, AgentType
        from langchain_openai import ChatOpenAI, OpenAI
        
        print("\n执行结果:")
        print("⏱️  开始计时...")
        start = time.time()
        
        chat = ChatOpenAI(
            temperature=0,
            model="deepseek-chat",
            openai_api_key=os.environ.get("DEEPSEEK_API_KEY"),
            openai_api_base="https://api.deepseek.com"
        )
        llm = OpenAI(
            temperature=0,
            model="deepseek-chat",
            openai_api_key=os.environ.get("DEEPSEEK_API_KEY"),
            openai_api_base="https://api.deepseek.com"
        )
        tools = load_tools(["serpapi", "llm-math"], llm=llm)
        
        agent = initialize_agent(
            tools, 
            chat, 
            agent=AgentType.CHAT_ZERO_SHOT_REACT_DESCRIPTION, 
            verbose=True
        )
        
        print("\n🤖 Agent开始执行...")
        print("-" * 80)
        # 使用更简单的问题，因为DeepSeek可能不支持所有工具
        result = agent.run("What is 25 multiplied by 4?")
        print("-" * 80)
        
        elapsed = time.time() - start
        print(f"\n✅ 最终答案: {result}")
        print(f"⏱️  总耗时: {elapsed:.2f}秒")
        
        print("\n💡 分析:")
        print("   从verbose=True的输出可以看到:")
        print("   1. 每个 Thought -> Action -> Observation 都是一个独立的循环")
        print("   2. 每个循环都会调用一次API")
        print("   3. 这个例子中至少进行了2-3次API调用:")
        print("      - 第1次: 决定使用计算工具")
        print("      - 第2次: 得到计算结果后，给出最终答案")
        print("   4. 但LangChain文档并未明确说明这一点！")
        
    except Exception as e:
        print(f"❌ LangChain Agent执行失败: {e}")
        import traceback
        traceback.print_exc()
else:
    print("\n⚠️  跳过Agent演示（需要SERPAPI_API_KEY）")
    print("\n💡 如果运行此演示，你会看到:")
    print("   - Agent会执行多个 Thought -> Action -> Observation 循环")
    print("   - 每个循环都会调用一次API")
    print("   - 总耗时会比你预期的长很多")
    print("   - 但文档中并未明确说明这个性能特征！")

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
print("   - LangChain隐藏了这些细节，可能导致意外的高成本和慢响应")

print("\n" + "=" * 80)
print("📊 关键问题总结")
print("=" * 80)
print("""
❌ LangChain的问题:
   1. Agent的每个推理步骤都会调用API
   2. 一个简单查询可能产生3-5次API调用
   3. 文档中没有明确说明这一点
   4. 用户可能会惊讶于高昂的API费用和长时间的响应延迟
   5. AgentType.CHAT_ZERO_SHOT_REACT_DESCRIPTION 这样的命名很晦涩

✅ 透明度的重要性:
   - 开发者应该明确知道何时、为何调用API
   - 成本和性能影响应该是可预测的
   - 抽象不应该隐藏关键的性能特征
""")

print("\n" + "=" * 80)
print("演示完成!")
print("=" * 80)
