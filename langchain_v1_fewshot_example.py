"""
LangChain v1.0 Few-Shot Learning 示例
演示三种实现方式的对比
"""

# 方式1: 使用原生 Python (最简单,最推荐)
def method1_native_python():
    """使用原生 Python 实现 few-shot prompt - 最简洁的方式"""
    print("=" * 60)
    print("方式1: 原生 Python (推荐)")
    print("=" * 60)
    
    def generate_few_shot_prompt(pairs):
        prompt = "Give the antonym of every input\n\n"
        for pair in pairs:
            input_word = pair['input']
            output_word = pair['output']
            prompt += f"Input: {input_word}\nOutput: {output_word}\n\n"
        return prompt
    
    pairs = [
        {"input": "happy", "output": "sad"},
        {"input": "tall", "output": "short"},
        {"input": "energetic", "output": "lethargic"},
        {"input": "sunny", "output": "gloomy"},
        {"input": "windy", "output": "calm"},
        {"input": "big", "output": ""}  # 留空让模型填充
    ]
    
    prompt = generate_few_shot_prompt(pairs)
    print(prompt)
    return prompt


# 方式2: 使用 ChatPromptTemplate (LangChain v1.0 推荐的简化方式)
def method2_chat_prompt_template():
    """使用 ChatPromptTemplate - LangChain v1.0 的简化方式"""
    print("=" * 60)
    print("方式2: ChatPromptTemplate (LangChain v1.0 简化方式)")
    print("=" * 60)
    
    from langchain_core.prompts import ChatPromptTemplate
    
    # 直接在 system message 中包含 few-shot 示例
    examples = """Input: happy
Output: sad

Input: tall
Output: short

Input: energetic
Output: lethargic

Input: sunny
Output: gloomy

Input: windy
Output: calm"""
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", f"Give the antonym of every input\n\n{examples}"),
        ("human", "Input: {{adjective}}\nOutput:")
    ])
    
    formatted = prompt.format(adjective="big")
    print(formatted)
    return formatted


# 方式3: 使用 FewShotChatMessagePromptTemplate (传统方式,较复杂)
def method3_fewshot_template():
    """使用 FewShotChatMessagePromptTemplate - 传统但复杂的方式"""
    print("=" * 60)
    print("方式3: FewShotChatMessagePromptTemplate (传统方式,较复杂)")
    print("=" * 60)
    
    from langchain_core.prompts import (
        ChatPromptTemplate,
        FewShotChatMessagePromptTemplate
    )
    
    # 定义示例
    examples = [
        {"input": "happy", "output": "sad"},
        {"input": "tall", "output": "short"},
        {"input": "energetic", "output": "lethargic"},
        {"input": "sunny", "output": "gloomy"},
        {"input": "windy", "output": "calm"}
    ]
    
    # 定义示例模板
    example_prompt = ChatPromptTemplate.from_messages([
        ("human", "Input: {input}"),
        ("ai", "Output: {output}")
    ])
    
    # 创建 few-shot 模板
    few_shot_prompt = FewShotChatMessagePromptTemplate(
        example_prompt=example_prompt,
        examples=examples
    )
    
    # 组装最终提示
    final_prompt = ChatPromptTemplate.from_messages([
        ("system", "Give the antonym of every input"),
        few_shot_prompt,
        ("human", "Input: {adjective}\nOutput:")
    ])
    
    formatted = final_prompt.format_messages(adjective="big")
    for msg in formatted:
        print(f"{msg.type}: {msg.content}")
    
    return formatted


# 方式4: 在 v1.0 Agent 中使用 few-shot (实际应用场景)
def method4_agent_with_fewshot():
    """
    在 LangChain v1.0 的 create_agent 中使用 few-shot
    这是 v1.0 最推荐的使用方式
    """
    print("=" * 60)
    print("方式4: 在 v1.0 Agent 中使用 few-shot")
    print("=" * 60)
    
    # 注意: 这个示例展示结构,实际运行需要 API key
    few_shot_examples = """
Examples:
Input: happy
Output: sad

Input: tall  
Output: short

Input: energetic
Output: lethargic
"""
    
    system_prompt = f"""You are an antonym assistant. 
Give the antonym of every input following these examples:

{few_shot_examples}

Now provide the antonym for the user's input."""
    
    print(system_prompt)
    print("\n在 v1.0 中使用示例:")
    print("""
from langchain.agents import create_agent

agent = create_agent(
    model="claude-sonnet-4-5-20250929",  # 或其他模型
    tools=[],  # 如需要可添加工具
    system_prompt=system_prompt  # 直接在 system_prompt 中包含 few-shot
)

# 运行 agent
result = agent.invoke({
    "messages": [{"role": "user", "content": "Input: big"}]
})
""")


def main():
    """运行所有示例"""
    print("\n" + "=" * 60)
    print("LangChain v1.0 Few-Shot Learning 对比示例")
    print("=" * 60 + "\n")
    
    # 运行各种方式
    method1_native_python()
    print("\n")
    
    method2_chat_prompt_template()
    print("\n")
    
    method3_fewshot_template()
    print("\n")
    
    method4_agent_with_fewshot()
    
    # 总结
    print("\n" + "=" * 60)
    print("总结与建议")
    print("=" * 60)
    print("""
1. 最简单: 方式1 (原生 Python)
   - 无需学习额外 API
   - 代码最短,最直观
   - 适合简单场景

2. LangChain v1.0 推荐: 方式2 或 方式4
   - 方式2: 使用 ChatPromptTemplate,在 system message 中直接包含示例
   - 方式4: 在 create_agent 的 system_prompt 中包含示例
   - 平衡了简洁性和 LangChain 集成

3. 不推荐: 方式3 (FewShotChatMessagePromptTemplate)
   - 过度抽象
   - 代码复杂
   - 违反"容易让人把事情做对"的原则
   
LangChain v1.0 的核心改进不在提示模板层面,
而是在 Agent 架构上。建议优先使用 create_agent 抽象,
在 system_prompt 中直接编写 few-shot 示例。
""")


if __name__ == "__main__":
    main()