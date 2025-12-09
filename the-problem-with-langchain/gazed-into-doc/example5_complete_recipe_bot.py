import os
import re
from typing import List, Dict, Any
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain.memory import ConversationBufferMemory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.tools import StructuredTool
from langchain_core.pydantic_v1 import BaseModel, Field

load_dotenv()

# 模拟recipe数据库
RECIPE_DB = {
    "dessert": [
        {"recipe_id": "recipe|167188", "name": "Creamy Strawberry Pie", "category": "dessert", "difficulty": "easy"},
        {"recipe_id": "recipe|1488243", "name": "Summer Strawberry Pie", "category": "dessert", "difficulty": "medium"},
        {"recipe_id": "recipe|299514", "name": "Pudding Cake", "category": "dessert", "difficulty": "easy"},
    ],
    "dinner": [
        {"recipe_id": "recipe|1774221", "name": "Crab Dip Your Guests will Like", "category": "dinner", "difficulty": "easy"},
        {"recipe_id": "recipe|836179", "name": "Easy Chicken Casserole", "category": "dinner", "difficulty": "easy"},
        {"recipe_id": "recipe|1980633", "name": "Easy Microwave Curry Doria", "category": "dinner", "difficulty": "easy"},
    ]
}

# 工具函数
def search_recipes(query: str) -> str:
    """根据查询搜索食谱"""
    query_lower = query.lower()
    results = []
    
    # 简单的关键词匹配
    for category, recipes in RECIPE_DB.items():
        if category in query_lower or any(word in query_lower for word in ["dinner", "dessert", "meal"]):
            results.extend(recipes)
    
    # 如果没有匹配，返回dessert作为默认
    if not results:
        results = RECIPE_DB["dessert"]
    
    # 格式化输出
    output = f"Found {len(results)} recipes for: {query}\n\n"
    for recipe in results[:3]:  # 限制3个结果
        output += f"Recipe ID: {recipe['recipe_id']}\n"
        output += f"Recipe Name: {recipe['name']}\n"
        output += f"Category: {recipe['category']}\n"
        output += f"Difficulty: {recipe['difficulty']}\n"
        output += "---\n"
    
    return output

# 创建工具
tools = [
    StructuredTool.from_function(
        func=search_recipes,
        name="SearchRecipes",
        description="Search for recipes based on keywords like 'dessert', 'dinner', etc. Returns Recipe ID, name, category, and difficulty."
    )
]

# System prompt - 结合趣味性和结构化要求
system_prompt = """You are an expert television talk show chef who speaks in a whimsical, enthusiastic manner! 🎪👨‍🍳

IMPORTANT RULES:
1. Start conversations with a fun food pun or whimsical greeting
2. When Recipe data is provided by tools, you MUST include the Recipe ID, Recipe Name, Category, and Difficulty for ALL recipes
3. If the user asks about non-food topics, politely redirect them back to cooking and food
4. Maintain your whimsical personality throughout the conversation
5. Format recipe lists clearly and include ALL provided information

Remember: You're here to make cooking fun and informative!"""

# 创建prompt with memory support
prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    MessagesPlaceholder(variable_name="chat_history", optional=True),
    ("human", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad"),
])

# 初始化组件
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7)  # 稍高的temperature增加趣味性
agent = create_openai_functions_agent(llm, tools, prompt)
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    memory=memory,
    verbose=True,
    handle_parsing_errors=True,
    return_intermediate_steps=True,
    max_iterations=3
)

# 交互式聊天循环
def chat():
    print("=" * 80)
    print("🎪 Whimsical Recipe Chef Bot - LangChain v1.0")
    print("=" * 80)
    print("Type 'quit' to exit\n")
    
    # 测试场景
    test_queries = [
        "Hi there!",
        "What's a fun and easy dinner?",
        "Tell me about the weather",  # 应该被拒绝
        "Show me some dessert recipes",
        "quit"
    ]
    
    for query in test_queries:
        if query.lower() == 'quit':
            print("\n👋 Goodbye! Happy cooking!")
            break
        
        print(f"\n{'='*80}")
        print(f"👤 User: {query}")
        print(f"{'='*80}\n")
        
        try:
            result = agent_executor.invoke({"input": query})
            response = result["output"]
            
            print(f"🤖 Chef: {response}\n")
            
            # 验证Recipe ID
            if result.get("intermediate_steps"):
                for action, observation in result["intermediate_steps"]:
                    if "Recipe ID" in str(observation):
                        recipe_ids = re.findall(r'recipe\|\d+', response)
                        if recipe_ids:
                            print(f"✅ Verified Recipe IDs in response: {recipe_ids}")
                        else:
                            print(f"⚠️  Warning: Recipe IDs may be missing from response")
        
        except Exception as e:
            print(f"❌ Error: {e}")
        
        print()

if __name__ == "__main__":
    chat()

