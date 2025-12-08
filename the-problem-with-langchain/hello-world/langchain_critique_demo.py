#!/usr/bin/env python3
"""
LangChain Hello World 缺点对比演示
演示文章中提到的每个缺点，并与OpenAI官方库进行对比
"""

import os
import sys
import time

# 检查OpenAI API密钥
if not os.environ.get("OPENAI_API_KEY"):
    print("❌ 错误：请设置OPENAI_API_KEY环境变量")
    print("   export OPENAI_API_KEY='your-api-key-here'")
    sys.exit(1)

print("=" * 80)
print("LangChain Hello World 缺点对比演示")
print("=" * 80)
print()

# ============================================================================
# 缺点1: 过度使用对象类，无明显代码优势
# ============================================================================
print("📌 缺点1: 过度使用对象类，无明显代码优势")
print("-" * 80)

print("\n🔴 LangChain方式 (使用多个对象类):")
print("代码:")
print("""
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage

chat = ChatOpenAI(temperature=0)
result = chat.predict_messages([HumanMessage(content="Translate: I love programming to French")])
print(result.content)
""")

try:
    from langchain.chat_models import ChatOpenAI
    from langchain.schema import HumanMessage
    
    print("\n执行结果:")
    start = time.time()
    chat = ChatOpenAI(temperature=0)
    result = chat.predict_messages([HumanMessage(content="Translate this sentence from English to French. I love programming.")])
    elapsed = time.time() - start
    print(f"✅ {result.content}")
    print(f"⏱️  耗时: {elapsed:.2f}秒")
except Exception as e:
    print(f"❌ LangChain执行失败: {e}")
    print("提示: 请确保已安装 langchain 和 langchain-openai")

print("\n" + "=" * 80)
print("\n🟢 OpenAI官方库方式 (简洁直接):")
print("代码:")
print("""
import openai

messages = [{"role": "user", "content": "Translate: I love programming to French"}]
response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages, temperature=0)
print(response["choices"][0]["message"]["content"])
""")

try:
    import openai
    
    print("\n执行结果:")
    start = time.time()
    messages = [{"role": "user", "content": "Translate this sentence from English to French. I love programming."}]
    response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages, temperature=0)
    elapsed = time.time() - start
    print(f"✅ {response['choices'][0]['message']['content']}")
    print(f"⏱️  耗时: {elapsed:.2f}秒")
except Exception as e:
    print(f"❌ OpenAI执行失败: {e}")

print("\n💡 分析: 两种方式代码量相当，但LangChain引入了额外的对象类，增加了复杂度")
print()

# ============================================================================
# 缺点2: Prompt模板过于复杂
# ============================================================================
print("\n" + "=" * 80)
print("📌 缺点2: Prompt模板过于复杂 (实际上只是f-strings的包装)")
print("-" * 80)

print("\n🔴 LangChain方式 (多层嵌套的模板类):")
print("代码:")
print("""
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)

template = "You are a helpful assistant that translates {input_language} to {output_language}."
system_message_prompt = SystemMessagePromptTemplate.from_template(template)
human_template = "{text}"
human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)

chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])
messages = chat_prompt.format_messages(
    input_language="English", 
    output_language="French", 
    text="I love programming."
)
print(messages)
""")

try:
    from langchain.prompts.chat import (
        ChatPromptTemplate,
        SystemMessagePromptTemplate,
        HumanMessagePromptTemplate,
    )
    
    print("\n执行结果:")
    template = "You are a helpful assistant that translates {input_language} to {output_language}."
    system_message_prompt = SystemMessagePromptTemplate.from_template(template)
    human_template = "{text}"
    human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)
    
    chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])
    messages = chat_prompt.format_messages(
        input_language="English", 
        output_language="French", 
        text="I love programming."
    )
    print("✅ 生成的消息:")
    for msg in messages:
        print(f"   - {type(msg).__name__}: {msg.content}")
except Exception as e:
    print(f"❌ LangChain执行失败: {e}")

print("\n" + "=" * 80)
print("\n🟢 Python原生f-strings方式 (简单直接):")
print("代码:")
print("""
input_language = "English"
output_language = "French"
text = "I love programming."

system_content = f"You are a helpful assistant that translates {input_language} to {output_language}."
human_content = f"{text}"

messages = [
    {"role": "system", "content": system_content},
    {"role": "user", "content": human_content}
]
print(messages)
""")

print("\n执行结果:")
input_language = "English"
output_language = "French"
text = "I love programming."

system_content = f"You are a helpful assistant that translates {input_language} to {output_language}."
human_content = f"{text}"

messages = [
    {"role": "system", "content": system_content},
    {"role": "user", "content": human_content}
]
print("✅ 生成的消息:")
for msg in messages:
    print(f"   - {msg['role']}: {msg['content']}")

print("\n💡 分析: LangChain的prompt模板只是f-strings的包装，但增加了3个额外的类和多行代码")
print()

# ============================================================================
# 缺点3: 对话记忆管理过于复杂
# ============================================================================
print("\n" + "=" * 80)
print("📌 缺点3: 对话记忆管理过于复杂")
print("-" * 80)

print("\n🔴 LangChain方式 (多个概念: ConversationBufferMemory, MessagesPlaceholder等):")
print("代码:")
print("""
from langchain.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate
)
from langchain.chains import ConversationChain
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory

prompt = ChatPromptTemplate.from_messages([
    SystemMessagePromptTemplate.from_template(
        "The following is a friendly conversation between a human and an AI."
    ),
    MessagesPlaceholder(variable_name="history"),
    HumanMessagePromptTemplate.from_template("{input}")
])

llm = ChatOpenAI(temperature=0)
memory = ConversationBufferMemory(return_messages=True)
conversation = ConversationChain(memory=memory, prompt=prompt, llm=llm)

response = conversation.predict(input="Hi there!")
print(response)
""")

try:
    from langchain.prompts import (
        ChatPromptTemplate,
        MessagesPlaceholder,
        SystemMessagePromptTemplate,
        HumanMessagePromptTemplate
    )
    from langchain.chains import ConversationChain
    from langchain.chat_models import ChatOpenAI
    from langchain.memory import ConversationBufferMemory
    
    print("\n执行结果:")
    start = time.time()
    
    prompt = ChatPromptTemplate.from_messages([
        SystemMessagePromptTemplate.from_template(
            "The following is a friendly conversation between a human and an AI. "
            "The AI is talkative and provides lots of specific details from its context."
        ),
        MessagesPlaceholder(variable_name="history"),
        HumanMessagePromptTemplate.from_template("{input}")
    ])
    
    llm = ChatOpenAI(temperature=0)
    memory = ConversationBufferMemory(return_messages=True)
    conversation = ConversationChain(memory=memory, prompt=prompt, llm=llm)
    
    response = conversation.predict(input="Hi there!")
    elapsed = time.time() - start
    print(f"✅ {response}")
    print(f"⏱️  耗时: {elapsed:.2f}秒")
    
    # 继续对话
    response2 = conversation.predict(input="What's 2+2?")
    print(f"✅ {response2}")
    
except Exception as e:
    print(f"❌ LangChain执行失败: {e}")

print("\n" + "=" * 80)
print("\n🟢 OpenAI官方库方式 (使用简单的列表):")
print("代码:")
print("""
import openai

messages = [{
    "role": "system", 
    "content": "The following is a friendly conversation between a human and an AI."
}]

# 第一轮对话
user_message = "Hi there!"
messages.append({"role": "user", "content": user_message})
response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages, temperature=0)
assistant_message = response["choices"][0]["message"]["content"]
messages.append({"role": "assistant", "content": assistant_message})
print(assistant_message)

# 第二轮对话
user_message2 = "What's 2+2?"
messages.append({"role": "user", "content": user_message2})
response2 = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages, temperature=0)
assistant_message2 = response2["choices"][0]["message"]["content"]
messages.append({"role": "assistant", "content": assistant_message2})
print(assistant_message2)
""")

try:
    import openai
    
    print("\n执行结果:")
    start = time.time()
    
    messages = [{
        "role": "system", 
        "content": "The following is a friendly conversation between a human and an AI. "
                   "The AI is talkative and provides lots of specific details from its context."
    }]
    
    # 第一轮对话
    user_message = "Hi there!"
    messages.append({"role": "user", "content": user_message})
    response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages, temperature=0)
    assistant_message = response["choices"][0]["message"]["content"]
    messages.append({"role": "assistant", "content": assistant_message})
    elapsed = time.time() - start
    print(f"✅ {assistant_message}")
    print(f"⏱️  耗时: {elapsed:.2f}秒")
    
    # 第二轮对话
    user_message2 = "What's 2+2?"
    messages.append({"role": "user", "content": user_message2})
    response2 = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages, temperature=0)
    assistant_message2 = response2["choices"][0]["message"]["content"]
    messages.append({"role": "assistant", "content": assistant_message2})
    print(f"✅ {assistant_message2}")
    
    print(f"\n📝 当前对话历史 ({len(messages)} 条消息):")
    for i, msg in enumerate(messages):
        print(f"   {i+1}. [{msg['role']}] {msg['content'][:50]}...")
    
except Exception as e:
    print(f"❌ OpenAI执行失败: {e}")

print("\n💡 分析: OpenAI官方库代码更少，逻辑更清晰，能直接看到消息的保存位置和时机")
print("   LangChain引入了ConversationBufferMemory、MessagesPlaceholder等概念，增加了学习成本")

# ============================================================================
# 总结
# ============================================================================
print("\n" + "=" * 80)
print("📊 总结")
print("=" * 80)
print("""
文章作者的核心观点:

1. ❌ LangChain引入了大量抽象层（对象类、模板类、记忆类等）
2. ❌ 这些抽象没有带来明显的代码优势，反而增加了复杂度
3. ❌ 很多功能用Python原生特性（如f-strings）或OpenAI官方库就能简单实现
4. ❌ 文档不够透明，隐藏了重要的性能细节（如Agent每步都调用API）
5. ❌ 如果quickstart就这么复杂，实际使用会更痛苦

作者认为: "如果nitpicks（吹毛求疵的问题）比实际好处还多，这个库就不值得使用"
""")

print("=" * 80)
print("演示完成!")
print("=" * 80)
