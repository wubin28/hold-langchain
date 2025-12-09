import os
from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_react_agent
from langchain.memory import ConversationBufferMemory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.tools import Tool

# 使用一个可能导致非JSON输出的system prompt
system_prompt = """You are a whimsical chef who LOVES to use exclamation marks and emoji!!!  🎉🍕

Always respond with enthusiasm and creativity! Use lots of expressions!

When using tools, maintain your enthusiastic personality throughout!!!"""

def search_recipes(query: str) -> str:
    """搜索食谱"""
    return f"Found recipes for: {query}\n- Recipe 1\n- Recipe 2"

tools = [
    Tool(
        name="SearchRecipes",
        func=search_recipes,
        description="Search for recipes based on user query"
    )
]

# 创建prompt - ReAct agent 需要包含 tools 和 tool_names 变量
prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt + "\n\nYou have access to the following tools:\n\n{tools}\n\nUse the following format:\n\nQuestion: the input question you must answer\nThought: you should always think about what to do\nAction: the action to take, should be one of [{tool_names}]\nAction Input: the input to the action\nObservation: the result of the action\n... (this Thought/Action/Action Input/Observation can repeat N times)\nThought: I now know the final answer\nFinal Answer: the final answer to the original input question"),
    MessagesPlaceholder(variable_name="chat_history", optional=True),
    ("human", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad"),
])

llm = ChatOpenAI(
    model="deepseek-chat",
    temperature=0.7,
    openai_api_key=os.environ.get("DEEPSEEK_API_KEY"),
    openai_api_base="https://api.deepseek.com"
)  # 更高的temperature测试稳定性

agent = create_react_agent(llm, tools, prompt)
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

# 关键改进：handle_parsing_errors 参数
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    memory=memory,
    verbose=True,
    handle_parsing_errors=True,  # ✅ v1.0 改进：自动处理解析错误
    max_iterations=5  # 限制重试次数
)

print("=" * 80)
print("Testing JSON Parsing Robustness in LangChain v1.0")
print("=" * 80)
print("\n🧪 Test 1: Simple greeting (might cause whimsical output)")

try:
    response = agent_executor.invoke({"input": "Hi there!"})
    print("\n✅ Success! Response:")
    print(response["output"])
except Exception as e:
    print(f"\n❌ Error: {e}")

print("\n" + "=" * 80)
print("🧪 Test 2: Recipe search (should use tool)")
print("=" * 80)

try:
    response = agent_executor.invoke({"input": "Find me some pasta recipes"})
    print("\n✅ Success! Response:")
    print(response["output"])
except Exception as e:
    print(f"\n❌ Error: {e}")

print("\n" + "=" * 80)
print("🧪 Test 3: Multiple requests to test stability")
print("=" * 80)

queries = [
    "Tell me about desserts!",
    "What's your favorite ingredient?",
    "Search for chicken recipes"
]

for i, query in enumerate(queries, 1):
    print(f"\nQuery {i}: {query}")
    try:
        response = agent_executor.invoke({"input": query})
        print(f"✅ Success: {response['output'][:100]}...")
    except Exception as e:
        print(f"❌ Error: {e}")

