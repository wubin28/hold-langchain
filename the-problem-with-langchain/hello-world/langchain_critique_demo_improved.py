#!/usr/bin/env python3
"""
LangChain 缺点改进演示 - 使用DeepSeek官方库的优雅解决方案
展示如何用DeepSeek官方库（OpenAI SDK）优雅地解决LangChain的3个主要缺点
"""

import os
import sys
import time
from typing import Any, cast

# 检查DeepSeek API密钥
if not os.environ.get("DEEPSEEK_API_KEY"):
    print("❌ 错误：请设置DEEPSEEK_API_KEY环境变量")
    print("   export DEEPSEEK_API_KEY='your-api-key-here'")
    sys.exit(1)

try:
    from openai import OpenAI
except ImportError:
    OpenAI = None  # type: ignore
    print("❌ 错误：请先安装openai库")
    print("   pip install openai")
    sys.exit(1)

print("=" * 80)
print("LangChain 缺点改进演示 - DeepSeek官方库优雅解决方案")
print("=" * 80)
print()

# 初始化DeepSeek客户端
client = OpenAI(
    api_key=os.environ.get("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com"
)

# ============================================================================
# 改进方案1: 简洁的对象使用 - 无需额外的消息对象包装
# ============================================================================
print("✨ 改进方案1: 简洁直接的API调用")
print("-" * 80)
print("问题: LangChain需要创建ChatOpenAI对象和HumanMessage对象")
print("解决: DeepSeek官方库直接使用字典，简洁明了")
print()

print("代码示例:")
print("""
from openai import OpenAI

client = OpenAI(
    api_key=os.environ.get("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com"
)

# 直接使用字典，无需创建额外的消息对象
messages = [{"role": "user", "content": "Translate this sentence from English to French. I love programming."}]
response = client.chat.completions.create(
    model="deepseek-chat",
    messages=messages,
    temperature=0
)
print(response.choices[0].message.content)
""")

print("\n执行结果:")
start = time.time()

# 实际执行
messages: list[dict[str, Any]] = [
    {"role": "user", "content": "Translate this sentence from English to French. I love programming."}
]
response = client.chat.completions.create(
    model="deepseek-chat",
    messages=cast(Any, messages),
    temperature=0
)

elapsed = time.time() - start
print(f"✅ {response.choices[0].message.content}")
print(f"⏱️  耗时: {elapsed:.2f}秒")

print("\n💡 优势:")
print("   ✓ 无需学习额外的对象类（ChatOpenAI、HumanMessage）")
print("   ✓ 代码更短、更直观")
print("   ✓ 使用标准的OpenAI API，通用性强")
print("   ✓ 易于调试和维护")
print()

# ============================================================================
# 改进方案2: 使用Python原生f-strings - 无需复杂的模板类
# ============================================================================
print("\n" + "=" * 80)
print("✨ 改进方案2: Python原生f-strings构建Prompt")
print("-" * 80)
print("问题: LangChain使用ChatPromptTemplate、SystemMessagePromptTemplate等多层嵌套")
print("解决: 直接使用Python f-strings，简单高效")
print()

print("代码示例:")
print("""
# 使用f-strings构建prompt
input_language = "English"
output_language = "French"
text = "I love programming."

messages = [
    {
        "role": "system",
        "content": f"You are a helpful assistant that translates {input_language} to {output_language}."
    },
    {
        "role": "user",
        "content": text
    }
]

response = client.chat.completions.create(
    model="deepseek-chat",
    messages=messages,
    temperature=0
)
print(response.choices[0].message.content)
""")

print("\n执行结果:")
start = time.time()

# 实际执行
input_language = "English"
output_language = "French"
text = "I love programming."

messages = [
    {
        "role": "system",
        "content": f"You are a helpful assistant that translates {input_language} to {output_language}."
    },
    {
        "role": "user",
        "content": text
    }
]

response = client.chat.completions.create(
    model="deepseek-chat",
    messages=cast(Any, messages),
    temperature=0
)

elapsed = time.time() - start
print(f"✅ {response.choices[0].message.content}")
print(f"⏱️  耗时: {elapsed:.2f}秒")

print("\n💡 优势:")
print("   ✓ 无需学习ChatPromptTemplate、SystemMessagePromptTemplate等复杂类")
print("   ✓ 使用Python开发者熟悉的f-strings")
print("   ✓ 代码更少、更易读")
print("   ✓ 灵活性更高，可以轻松组合复杂的prompt")
print()

# ============================================================================
# 改进方案3: 简单列表管理对话历史 - 无需复杂的记忆管理类
# ============================================================================
print("\n" + "=" * 80)
print("✨ 改进方案3: 使用简单列表管理对话历史")
print("-" * 80)
print("问题: LangChain使用RunnableWithMessageHistory、MessagesPlaceholder等复杂概念")
print("解决: 直接使用Python列表保存消息历史，简单透明")
print()

print("代码示例:")
print("""
# 使用简单的列表保存对话历史
conversation_history = [
    {
        "role": "system",
        "content": "The following is a friendly conversation between a human and an AI. "
                   "The AI is talkative and provides lots of specific details from its context."
    }
]

# 第一轮对话
user_input = "Hi there!"
conversation_history.append({"role": "user", "content": user_input})

response = client.chat.completions.create(
    model="deepseek-chat",
    messages=conversation_history,
    temperature=0
)

assistant_response = response.choices[0].message.content
conversation_history.append({"role": "assistant", "content": assistant_response})
print(f"AI: {assistant_response}")

# 第二轮对话
user_input = "What's 2+2?"
conversation_history.append({"role": "user", "content": user_input})

response = client.chat.completions.create(
    model="deepseek-chat",
    messages=conversation_history,
    temperature=0
)

assistant_response = response.choices[0].message.content
conversation_history.append({"role": "assistant", "content": assistant_response})
print(f"AI: {assistant_response}")

# 查看完整的对话历史
print(f"\\n对话历史共 {len(conversation_history)} 条消息")
""")

print("\n执行结果:")
start = time.time()

# 实际执行
conversation_history: list[dict[str, Any]] = [
    {
        "role": "system",
        "content": "The following is a friendly conversation between a human and an AI. "
                   "The AI is talkative and provides lots of specific details from its context."
    }
]

# 第一轮对话
user_input = "Hi there!"
conversation_history.append({"role": "user", "content": user_input})
print(f"👤 User: {user_input}")

response = client.chat.completions.create(
    model="deepseek-chat",
    messages=cast(Any, conversation_history),
    temperature=0
)

assistant_response = response.choices[0].message.content
conversation_history.append({"role": "assistant", "content": assistant_response})
elapsed = time.time() - start
print(f"🤖 AI: {assistant_response}")
print(f"⏱️  耗时: {elapsed:.2f}秒")

# 第二轮对话
print()
user_input = "What's 2+2?"
conversation_history.append({"role": "user", "content": user_input})
print(f"👤 User: {user_input}")

start = time.time()
response = client.chat.completions.create(
    model="deepseek-chat",
    messages=cast(Any, conversation_history),
    temperature=0
)

assistant_response = response.choices[0].message.content
conversation_history.append({"role": "assistant", "content": assistant_response})
elapsed = time.time() - start
print(f"🤖 AI: {assistant_response}")
print(f"⏱️  耗时: {elapsed:.2f}秒")

# 展示对话历史
print(f"\n📝 完整对话历史 ({len(conversation_history)} 条消息):")
for i, msg in enumerate(conversation_history):
    role_emoji = "🤖" if msg["role"] == "assistant" else "👤" if msg["role"] == "user" else "⚙️"
    content_preview = msg["content"][:60] + "..." if len(msg["content"]) > 60 else msg["content"]
    print(f"   {i+1}. {role_emoji} [{msg['role']}] {content_preview}")

print("\n💡 优势:")
print("   ✓ 无需学习RunnableWithMessageHistory、MessagesPlaceholder等概念")
print("   ✓ 对话历史清晰可见，易于调试")
print("   ✓ 可以轻松实现自定义的历史管理策略（如限制长度、保存到数据库等）")
print("   ✓ 完全掌控数据流，不依赖黑盒抽象")
print()

# ============================================================================
# 进阶示例: 实现对话历史管理的实用模式
# ============================================================================
print("\n" + "=" * 80)
print("🚀 进阶示例: 实现实用的对话历史管理")
print("-" * 80)
print()

class SimpleConversation:
    """简单的对话管理类 - 展示如何优雅地封装对话逻辑"""
    
    def __init__(self, client: OpenAI, system_prompt: str = "", max_history: int = 20):
        """
        初始化对话
        
        Args:
            client: OpenAI客户端实例
            system_prompt: 系统提示词
            max_history: 最大保留的历史消息数（不包括system消息）
        """
        self.client = client
        self.max_history = max_history
        self.messages: list[dict[str, Any]] = []
        
        if system_prompt:
            self.messages.append({"role": "system", "content": system_prompt})
    
    def chat(self, user_input: str, temperature: float = 0.7) -> str:
        """
        发送消息并获取回复
        
        Args:
            user_input: 用户输入
            temperature: 温度参数
            
        Returns:
            AI的回复内容
        """
        # 添加用户消息
        self.messages.append({"role": "user", "content": user_input})
        
        # 调用API
        response = self.client.chat.completions.create(
            model="deepseek-chat",
            messages=cast(Any, self.messages),
            temperature=temperature
        )
        
        # 获取AI回复
        assistant_response = response.choices[0].message.content or ""
        self.messages.append({"role": "assistant", "content": assistant_response})
        
        # 限制历史长度（保留system消息）
        self._trim_history()
        
        return assistant_response
    
    def _trim_history(self):
        """保持历史消息在限制范围内"""
        # 找到system消息
        system_messages = [msg for msg in self.messages if msg["role"] == "system"]
        other_messages = [msg for msg in self.messages if msg["role"] != "system"]
        
        # 如果超过最大历史数，保留最近的消息
        if len(other_messages) > self.max_history:
            other_messages = other_messages[-self.max_history:]
        
        # 重新组合
        self.messages = system_messages + other_messages
    
    def get_history(self) -> list[dict[str, Any]]:
        """获取对话历史"""
        return self.messages.copy()
    
    def clear_history(self, keep_system: bool = True):
        """清除对话历史"""
        if keep_system:
            system_messages = [msg for msg in self.messages if msg["role"] == "system"]
            self.messages = system_messages
        else:
            self.messages = []

print("代码示例:")
print("""
class SimpleConversation:
    def __init__(self, client, system_prompt="", max_history=20):
        self.client = client
        self.max_history = max_history
        self.messages = []
        if system_prompt:
            self.messages.append({"role": "system", "content": system_prompt})
    
    def chat(self, user_input, temperature=0.7):
        self.messages.append({"role": "user", "content": user_input})
        response = self.client.chat.completions.create(
            model="deepseek-chat",
            messages=self.messages,
            temperature=temperature
        )
        assistant_response = response.choices[0].message.content
        self.messages.append({"role": "assistant", "content": assistant_response})
        self._trim_history()
        return assistant_response
    
    def _trim_history(self):
        # 保持历史长度在限制范围内
        system_messages = [msg for msg in self.messages if msg["role"] == "system"]
        other_messages = [msg for msg in self.messages if msg["role"] != "system"]
        if len(other_messages) > self.max_history:
            other_messages = other_messages[-self.max_history:]
        self.messages = system_messages + other_messages

# 使用示例
conv = SimpleConversation(
    client,
    system_prompt="You are a helpful math tutor.",
    max_history=10
)

response = conv.chat("What is 5 + 3?")
print(response)
""")

print("\n执行结果:")

# 实际使用
conv = SimpleConversation(
    client,
    system_prompt="You are a helpful and concise math tutor.",
    max_history=10
)

# 测试对话
test_inputs = [
    "What is 5 + 3?",
    "What about if I multiply that by 2?",
    "And divide by 4?"
]

for user_input in test_inputs:
    print(f"\n👤 User: {user_input}")
    start = time.time()
    response = conv.chat(user_input, temperature=0)
    elapsed = time.time() - start
    print(f"🤖 AI: {response}")
    print(f"⏱️  耗时: {elapsed:.2f}秒")

print(f"\n📝 最终对话历史: {len(conv.get_history())} 条消息")

print("\n💡 进阶方案的优势:")
print("   ✓ 封装了常用的对话管理逻辑")
print("   ✓ 自动管理历史长度，避免token溢出")
print("   ✓ 代码简洁（不到50行），易于理解和修改")
print("   ✓ 完全透明，没有隐藏的魔法")
print("   ✓ 可以轻松扩展（如添加流式输出、保存到数据库等）")

# ============================================================================
# 总结对比
# ============================================================================
print("\n" + "=" * 80)
print("📊 总结：DeepSeek官方库 vs LangChain")
print("=" * 80)
print("""
┌────────────────────┬──────────────────────────┬─────────────────────────┐
│ 功能               │ LangChain方式            │ DeepSeek官方库方式      │
├────────────────────┼──────────────────────────┼─────────────────────────┤
│ 基本调用           │ ChatOpenAI + HumanMessage│ 简单字典 + OpenAI客户端 │
│                    │ (需要学习2个新类)        │ (标准OpenAI API)        │
├────────────────────┼──────────────────────────┼─────────────────────────┤
│ Prompt构建         │ ChatPromptTemplate +     │ Python原生f-strings     │
│                    │ SystemMessagePromptTemplate│ (无需额外学习)         │
│                    │ + HumanMessagePromptTemplate│                       │
│                    │ (需要学习3个新类)        │                         │
├────────────────────┼──────────────────────────┼─────────────────────────┤
│ 对话历史管理       │ RunnableWithMessageHistory│ 简单的Python列表        │
│                    │ + MessagesPlaceholder +  │ (完全透明、易于调试)    │
│                    │ InMemoryChatMessageHistory│                        │
│                    │ (需要学习多个复杂概念)   │                         │
├────────────────────┼──────────────────────────┼─────────────────────────┤
│ 学习曲线           │ 陡峭（大量抽象概念）     │ 平缓（标准Python+API）  │
├────────────────────┼──────────────────────────┼─────────────────────────┤
│ 代码可读性         │ 较差（多层抽象）         │ 优秀（简洁直观）        │
├────────────────────┼──────────────────────────┼─────────────────────────┤
│ 调试难度           │ 困难（黑盒抽象）         │ 简单（透明可控）        │
├────────────────────┼──────────────────────────┼─────────────────────────┤
│ 灵活性             │ 受框架限制               │ 完全自由                │
├────────────────────┼──────────────────────────┼─────────────────────────┤
│ API稳定性          │ 频繁变化（v0.x→v1.x      │ 稳定（标准OpenAI API）  │
│                    │ 很多API被废弃）          │                         │
└────────────────────┴──────────────────────────┴─────────────────────────┘

🎯 核心结论:

1. ✅ 缺点1（过度使用对象类）已解决
   → DeepSeek官方库使用简单字典，无需额外的对象包装

2. ✅ 缺点2（Prompt模板复杂）已解决
   → 使用Python原生f-strings，简洁高效

3. ✅ 缺点3（对话记忆管理复杂）已解决
   → 使用简单的Python列表，完全透明可控

💡 建议:

对于简单到中等复杂度的LLM应用，直接使用DeepSeek官方库（或OpenAI SDK）是更好的选择：
  • 代码更少、更清晰
  • 学习成本更低
  • 调试更容易
  • 性能更可控
  • API更稳定

只有在需要LangChain的特定高级功能时（如复杂的工具链、特殊的数据处理流程等），
才考虑引入LangChain的额外复杂度。
""")

print("=" * 80)
print("✅ 改进演示完成!")
print("=" * 80)
