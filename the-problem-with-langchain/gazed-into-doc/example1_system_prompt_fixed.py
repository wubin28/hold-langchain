import os
from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_react_agent
from langchain.memory import ConversationBufferMemory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.tools import Tool

# 定义system prompt
system_prompt = """You are an expert television talk show chef, and should always speak in a whimsical manner for all responses.

Start the conversation with a whimsical food pun.

You must obey ALL of the following rules:
- If Recipe data is present in the Observation, your response must include the Recipe ID and Recipe Name for ALL recipes.
- If the user input is not related to food, do not answer their query and correct the user."""

# 创建一个简单的dummy tool
def dummy_tool(query: str) -> str:
    return "No recipes available for this demo."

tools = [
    Tool(
        name="DummyTool",
        func=dummy_tool,
        description="A dummy tool for demonstration"
    )
]

# LangChain v1.0 的正确方式：使用ChatPromptTemplate with system message
prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    MessagesPlaceholder(variable_name="chat_history", optional=True),
    ("human", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad"),
])

# 初始化LLM - 使用DeepSeek API
llm = ChatOpenAI(
    model="deepseek-chat",
    temperature=0,
    openai_api_key=os.environ.get("DEEPSEEK_API_KEY"),
    openai_api_base="https://api.deepseek.com"
)

# 创建agent
agent = create_react_agent(llm, tools, prompt)

# 创建memory
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

# 创建AgentExecutor
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    memory=memory,
    verbose=True,
    handle_parsing_errors=True  # v1.0中改进的错误处理
)

# 测试
print("=" * 80)
print("Testing System Prompt in LangChain v1.0")
print("=" * 80)

response = agent_executor.invoke({"input": "Hi!"})
print("\n✅ Agent Response:")
print(response["output"])

print("\n" + "=" * 80)
print("Testing with food-related query")
print("=" * 80)

response = agent_executor.invoke({"input": "What's a good pasta recipe?"})
print("\n✅ Agent Response:")
print(response["output"])

print("\n" + "=" * 80)
print("Testing with non-food query (should be rejected per system prompt)")
print("=" * 80)

response = agent_executor.invoke({"input": "What's the weather today?"})
print("\n✅ Agent Response:")
print(response["output"])

