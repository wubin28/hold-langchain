import os
from typing import List, Dict
from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_react_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.tools import Tool, StructuredTool
from langchain_core.pydantic_v1 import BaseModel, Field

# 定义结构化输出模型
class Recipe(BaseModel):
    """Recipe information"""
    recipe_id: str = Field(description="The unique recipe ID")
    name: str = Field(description="The recipe name")
    category: str = Field(description="Recipe category")

class RecipeSearchResult(BaseModel):
    """Search result with multiple recipes"""
    recipes: List[Recipe] = Field(description="List of recipes found")
    query: str = Field(description="Original search query")

# 创建返回结构化数据的工具
def search_recipes_structured(query: str) -> str:
    """搜索食谱并返回结构化数据"""
    # 模拟搜索结果
    recipes = [
        {"recipe_id": "recipe|167188", "name": "Creamy Strawberry Pie", "category": "dessert"},
        {"recipe_id": "recipe|1488243", "name": "Summer Strawberry Pie", "category": "dessert"},
        {"recipe_id": "recipe|299514", "name": "Pudding Cake", "category": "dessert"},
    ]
    
    # 格式化输出，确保包含所有必需字段
    result = f"Search query: {query}\n\nRecipes found:\n"
    for recipe in recipes:
        result += f"\n**Recipe ID**: {recipe['recipe_id']}\n"
        result += f"**Recipe Name**: {recipe['name']}\n"
        result += f"**Category**: {recipe['category']}\n"
        result += "---\n"
    
    return result

tools = [
    Tool(
        name="SearchRecipes",
        func=search_recipes_structured,
        description="Search for recipes. Returns Recipe ID, Recipe Name, and Category for each result. ALWAYS include ALL fields in your response."
    )
]

system_prompt = """You are a helpful recipe assistant.

CRITICAL RULES:
1. When Recipe data is present in the Observation, you MUST include the Recipe ID, Recipe Name, and Category for ALL recipes in your response.
2. Format each recipe as:
   - Recipe ID: [id]
   - Name: [name]
   - Category: [category]
3. Never omit the Recipe ID - this is required for the system to function.
4. List all recipes provided in the Observation."""

prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt + "\n\nYou have access to the following tools:\n\n{tools}\n\nUse the following format:\n\nQuestion: the input question you must answer\nThought: you should always think about what to do\nAction: the action to take, should be one of [{tool_names}]\nAction Input: the input to the action\nObservation: the result of the action\n... (this Thought/Action/Action Input/Observation can repeat N times)\nThought: I now know the final answer\nFinal Answer: the final answer to the original input question"),
    MessagesPlaceholder(variable_name="chat_history", optional=True),
    ("human", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad"),
])

llm = ChatOpenAI(
    model="deepseek-chat",
    temperature=0,
    openai_api_key=os.environ.get("DEEPSEEK_API_KEY"),
    openai_api_base="https://api.deepseek.com"
)

agent = create_react_agent(llm, tools, prompt)

agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,
    handle_parsing_errors=True,
    return_intermediate_steps=True  # ✅ 关键：返回中间步骤以获取工具输出
)

print("=" * 80)
print("Testing Structured Output in LangChain v1.0")
print("=" * 80)

result = agent_executor.invoke({"input": "Find me some dessert recipes"})

print("\n" + "=" * 80)
print("📋 Final Agent Output:")
print("=" * 80)
print(result["output"])

print("\n" + "=" * 80)
print("🔧 Intermediate Steps (Tool Outputs):")
print("=" * 80)
for i, (action, observation) in enumerate(result["intermediate_steps"], 1):
    print(f"\nStep {i}:")
    print(f"Tool: {action.tool}")
    print(f"Input: {action.tool_input}")
    print(f"Output:\n{observation}")

# 验证Recipe ID是否存在于输出中
output = result["output"]
if "recipe|" in output:
    print("\n✅ SUCCESS: Recipe IDs are present in the output!")
    # 提取所有Recipe ID
    import re
    recipe_ids = re.findall(r'recipe\|\d+', output)
    print(f"Found {len(recipe_ids)} Recipe IDs: {recipe_ids}")
else:
    print("\n⚠️  WARNING: Recipe IDs might be missing from the output")

