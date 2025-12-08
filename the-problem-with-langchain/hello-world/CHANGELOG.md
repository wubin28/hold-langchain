# 更新日志

## 2025-12-08 (晚) - LangChain 1.x API 兼容性修复

### 🔄 主要变更

修复了 LangChain 1.x 版本带来的 API 不兼容问题。这次修复正好印证了文章的核心观点：**LangChain API 不稳定，学习成本高**。

#### 1. 修复缺点1演示 - 消息导入路径变更
- **旧导入**: `from langchain.schema import HumanMessage`
- **新导入**: `from langchain_core.messages import HumanMessage`
- **原因**: LangChain 1.x 移除了 `langchain.schema` 模块

#### 2. 修复缺点2演示 - Prompt模板路径变更
- **旧导入**: `from langchain.prompts.chat import ChatPromptTemplate, ...`
- **新导入**: `from langchain_core.prompts.chat import ChatPromptTemplate, ...`
- **原因**: Prompt 相关类移至 `langchain_core.prompts` 模块

#### 3. 修复缺点3演示 - 对话链API完全重写
- **旧API已废弃**:
  ```python
  from langchain.chains import ConversationChain
  from langchain.memory import ConversationBufferMemory
  conversation = ConversationChain(memory=memory, prompt=prompt, llm=llm)
  response = conversation.predict(input="Hi there!")
  ```
- **新API**:
  ```python
  from langchain_core.runnables.history import RunnableWithMessageHistory
  from langchain_core.chat_history import InMemoryChatMessageHistory
  with_message_history = RunnableWithMessageHistory(chain, get_session_history, ...)
  response = with_message_history.invoke({"input": "Hi there!"}, config={...})
  ```
- **影响**: ConversationChain 和 ConversationBufferMemory 在 LangChain 1.x 中已被完全移除

#### 4. 修复Agent演示 - Agent API已废弃
- **旧API已废弃**:
  ```python
  from langchain.agents import load_tools, initialize_agent, AgentType
  tools = load_tools(["serpapi", "llm-math"], llm=llm)
  agent = initialize_agent(tools, chat, agent=AgentType.CHAT_ZERO_SHOT_REACT_DESCRIPTION)
  ```
- **新API**: 需要手动实现 ReAct 循环或使用更复杂的新 API
- **原因**: `load_tools` 和 `initialize_agent` 在 LangChain 1.x 中已被移除

#### 5. 更新依赖安装
- 在 `quickstart.sh` 中添加 `langchain-core` 依赖
- 完整依赖列表: `langchain`, `langchain-core`, `langchain-openai`, `langchain-community`

### 🐛 修复的问题

1. **缺点1演示失败**
   - 错误: `No module named 'langchain.schema'`
   - 修复: 使用 `langchain_core.messages`

2. **缺点2演示失败**
   - 错误: `No module named 'langchain.prompts'`
   - 修复: 使用 `langchain_core.prompts.chat`

3. **缺点3演示失败**
   - 错误: `No module named 'langchain.chains'`
   - 修复: 使用新的 `RunnableWithMessageHistory` API

4. **Agent演示失败**
   - 错误: `cannot import name 'load_tools' from 'langchain.agents'`
   - 修复: 简化为手动实现的 ReAct 循环演示

### 💡 这次修复的讽刺意味

这次修复过程本身就完美地证明了文章批评 LangChain 的观点：

1. **API 极不稳定**: 短短几个月内，ConversationChain、load_tools 等核心 API 就被完全移除
2. **学习成本高**: 每次更新都需要重新学习新的 API 模式
3. **文档滞后**: 许多教程和示例代码已经无法运行
4. **过度抽象**: 新API（如 RunnableWithMessageHistory）比旧API更加复杂

### ✅ 测试状态

- [x] 所有导入语句已修复
- [x] 代码结构验证通过
- [x] 缺点2演示（不需要API调用）运行成功
- [ ] 完整演示（需要真实 API 密钥）待用户测试

### 📝 对开发者的建议

基于这次修复经验，我们建议：
1. 避免过度依赖快速迭代的抽象框架
2. 优先使用稳定的底层 API（如 OpenAI SDK）
3. 如果使用 LangChain，固定版本号并做好 API 变更的准备

---

## 2025-12-08 (早) - API 兼容性更新

### 🔄 主要变更

#### 1. 更新 OpenAI 库版本
- **旧版本**: `openai==0.28.1`
- **新版本**: `openai>=1.0.0,<2.0.0`
- **原因**: 修复与 langchain-openai 的依赖冲突，使用最新的 OpenAI API

#### 2. 更新 LangChain 依赖
- **旧版本**: `langchain==0.0.350`, `langchain-openai==0.0.2`
- **新版本**: `langchain`, `langchain-openai`, `langchain-community` (最新稳定版)
- **原因**: 修复导入错误和兼容性问题

### 📝 文件修改

#### quickstart.sh
- 更新依赖安装命令以使用新版本
- 移除固定的旧版本号

#### langchain_critique_demo.py
- 更新 OpenAI API 调用方式：
  ```python
  # 旧版 API
  import openai
  openai.api_base = "https://api.deepseek.com"
  response = openai.ChatCompletion.create(...)
  
  # 新版 API
  from openai import OpenAI
  client = OpenAI(api_key="...", base_url="https://api.deepseek.com")
  response = client.chat.completions.create(...)
  ```

- 更新 LangChain 导入和使用：
  ```python
  # 旧版导入
  from langchain.chat_models import ChatOpenAI
  chat.predict_messages(...)
  
  # 新版导入
  from langchain_openai import ChatOpenAI
  chat.invoke(...)
  ```

#### langchain_agent_performance_demo.py
- 同步更新 OpenAI 和 LangChain API 调用方式
- 更新示例代码以反映新的 API 使用方式

#### README.md
- 添加快速启动脚本说明
- 更新依赖安装步骤
- 更新 API 配置示例
- 添加新的常见问题解答（OpenAI API 版本错误）

### 🐛 修复的问题

1. **依赖冲突**
   - 错误: `langchain-openai 0.0.2 requires openai<2.0.0,>=1.6.1, but you have openai 0.28.1`
   - 修复: 安装兼容版本的 openai 库

2. **LangChain 导入错误**
   - 错误: `cannot import name '_signature' from 'langchain_community.chat_models.baichuan'`
   - 修复: 更新到最新版本的 langchain-community

3. **OpenAI API 调用错误**
   - 错误: `You tried to access openai.ChatCompletion, but this is no longer supported in openai>=1.0.0`
   - 修复: 更新所有代码以使用新版 OpenAI API

### ⚡ 向后不兼容的变更

如果你之前使用旧版本：

1. 需要重新安装依赖：
   ```bash
   pip uninstall openai langchain langchain-openai
   pip install "openai>=1.0.0,<2.0.0" langchain langchain-openai langchain-community
   ```

2. 代码中的 API 调用方式已更改，不兼容旧版本

### ✅ 测试状态

- [x] quickstart.sh 脚本依赖安装正常
- [ ] LangChain 演示正常运行（待测试）
- [ ] DeepSeek API 演示正常运行（待测试）
- [ ] Agent 演示正常运行（待测试）

### 📚 相关资源

- [OpenAI Python Library v1.0.0 Migration Guide](https://github.com/openai/openai-python/discussions/742)
- [LangChain OpenAI Integration](https://python.langchain.com/docs/integrations/platforms/openai)
