import os
from typing import List
from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.tools import StructuredTool
from langchain_core.pydantic_v1 import BaseModel, Field

# 定义工具输入模型
class RecipeSearchInput(BaseModel):
    query: str = Field(description="The search query for recipes")

# 定义工具输出模型
class RecipeInfo(BaseModel):
    recipe_id: str
    name: str
    category: str

def search_recipes_typed(query: str) -> List[dict]:
    """搜索食谱并返回结构化列表"""
    return [
        {"recipe_id": "recipe|167188", "name": "Creamy Strawberry Pie", "category": "dessert"},
        {"recipe_id": "recipe|1488243", "name": "Summer Strawberry Pie", "category": "dessert"},
        {"recipe_id": "recipe|299514", "name": "Pudding Cake", "category": "dessert"},
    ]

# 创建结构化工具
recipe_search_tool = StructuredTool.from_function(
    func=search_recipes_typed,
    name="SearchRecipes",
    description="Search for recipes based on a query. Returns a list of recipes with ID, name, and category.",
    args_schema=RecipeSearchInput,
    return_direct=False
)

tools = [recipe_search_tool]

system_prompt = """You are a helpful recipe assistant.

When presenting recipe search results:
1. Always include the Recipe ID for each recipe (format: recipe|XXXXX)
2. Include the recipe name
3. Include the category
4. Present them in a clear, formatted list"""

# 使用OpenAI Functions专用的prompt
prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    MessagesPlaceholder(variable_name="chat_history", optional=True),
    ("human", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad"),
])

# 使用支持function calling的模型
llm = ChatOpenAI(
    model="deepseek-chat",
    temperature=0,
    openai_api_key=os.environ.get("DEEPSEEK_API_KEY"),
    openai_api_base="https://api.deepseek.com"
)

# ✅ 使用OpenAI Functions agent（更可靠的结构化输出）
agent = create_openai_functions_agent(llm, tools, prompt)

agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,
    return_intermediate_steps=True
)

print("=" * 80)
print("Testing DeepSeek Function Calling in LangChain v1.0")
print("=" * 80)
print("This approach uses DeepSeek's native function calling for reliable structured output\n")

result = agent_executor.invoke({"input": "Find me dessert recipes"})

print("\n" + "=" * 80)
print("📋 Final Output:")
print("=" * 80)
print(result["output"])

print("\n" + "=" * 80)
print("🔧 Raw Tool Output (Structured Data):")
print("=" * 80)
for i, (action, observation) in enumerate(result["intermediate_steps"], 1):
    print(f"\nStep {i} - Tool: {action.tool}")
    print(f"Structured Output: {observation}")

# 验证
import re
recipe_ids = re.findall(r'recipe\|\d+', result["output"])
print(f"\n✅ Extracted {len(recipe_ids)} Recipe IDs from final output: {recipe_ids}")

