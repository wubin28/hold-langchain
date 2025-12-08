# LangChain Hello World 缺点对比演示 - 运行指南

## 📋 概述

本项目包含两个Python脚本，用于演示2023年那篇批评LangChain文章中提到的所有缺点，并与DeepSeek API直接调用进行对比。

### 脚本说明

1. **langchain_critique_demo.py** - 主演示脚本
   - 缺点1: 过度使用对象类
   - 缺点2: Prompt模板过于复杂
   - 缺点3: 对话记忆管理过于复杂

2. **langchain_agent_performance_demo.py** - Agent性能问题演示
   - 缺点4: 每个Thought/Action/Observation步骤都单独调用API
   - 缺点5: Agent实现不透明

## 🚀 快速开始（推荐）

**最简单的方式：使用自动化脚本**

```bash
# 1. 进入项目目录
cd the-problem-with-langchain/hello-world

# 2. 运行快速启动脚本
./quickstart.sh
```

脚本会自动：
- ✅ 检查 Python 环境
- ✅ 创建并激活虚拟环境
- ✅ 安装所有依赖
- ✅ 引导你设置 API 密钥
- ✅ 提供交互式菜单选择要运行的演示

---

## 📖 手动运行步骤（可选）

如果你想手动设置环境，可以按照以下步骤：

### 步骤1: 环境准备

```bash
# 1. 打开iTerm2终端

# 2. 检查Python版本（需要Python 3.8+）
python3 --version

# 3. 创建项目目录
mkdir ~/langchain-critique-demo
cd ~/langchain-critique-demo

# 4. 创建Python虚拟环境（推荐）
python3 -m venv venv

# 5. 激活虚拟环境
source venv/bin/activate

# 激活后，你的终端提示符前面会出现 (venv)
```

### 步骤2: 安装依赖

```bash
# 安装OpenAI库（用于DeepSeek API兼容）
# 注意：使用最新版本 1.x
pip install "openai>=1.0.0,<2.0.0"

# 安装LangChain相关库
pip install langchain langchain-openai langchain-community

# 如果要运行Agent演示，还需要安装（可选）
pip install google-search-results  # SerpAPI的Python库

# 验证安装
pip list | grep -E "openai|langchain"
```

**注意：** 新版本的 `openai` 库（>= 1.0.0）API 与旧版本有显著差异，本项目已更新为使用新版 API。

### 步骤3: 配置API密钥

```bash
# 设置DeepSeek API密钥（必需）
# 可以从 https://platform.deepseek.com 注册获取
export DEEPSEEK_API_KEY='your-deepseek-api-key-here'

# 设置SerpAPI密钥（可选，仅Agent演示需要）
# 可以从 https://serpapi.com 注册获取免费密钥
export SERPAPI_API_KEY='your-serpapi-key-here'

# 验证环境变量
echo $DEEPSEEK_API_KEY
```

**永久设置（可选）：**

```bash
# 将API密钥添加到 ~/.zshrc 文件
echo 'export DEEPSEEK_API_KEY="your-deepseek-api-key-here"' >> ~/.zshrc
echo 'export SERPAPI_API_KEY="your-serpapi-key-here"' >> ~/.zshrc

# 重新加载配置
source ~/.zshrc
```

### 步骤4: 下载脚本文件

将以下两个文件保存到 `~/langchain-critique-demo/` 目录：
- `langchain_critique_demo.py`
- `langchain_agent_performance_demo.py`

```bash
# 确保文件具有执行权限
chmod +x langchain_critique_demo.py
chmod +x langchain_agent_performance_demo.py
```

### 步骤5: 运行演示

#### 运行主演示（缺点1-3）

```bash
# 确保虚拟环境已激活
source venv/bin/activate

# 运行主演示脚本
python3 langchain_critique_demo.py
```

**预期输出：**
- 你会看到每个缺点的详细对比
- LangChain方式 vs DeepSeek API直接调用方式
- 实际运行结果和耗时
- 详细的分析说明

#### 运行Agent性能演示（缺点4-5）

```bash
# 运行Agent演示脚本（需要SERPAPI_API_KEY）
python3 langchain_agent_performance_demo.py
```

**预期输出：**
- Agent的详细执行过程（verbose=True）
- 每个Thought/Action/Observation步骤
- 总耗时和API调用次数分析

## 📝 运行示例截图

### 主演示输出示例

```
================================================================================
LangChain Hello World 缺点对比演示
================================================================================

📌 缺点1: 过度使用对象类，无明显代码优势
--------------------------------------------------------------------------------

🔴 LangChain方式 (使用多个对象类):
代码:
...
执行结果:
✅ J'adore la programmation.
⏱️  耗时: 1.23秒

================================================================================

🟢 DeepSeek API直接调用方式 (简洁直接):
代码:
...
执行结果:
✅ J'adore la programmation.
⏱️  耗时: 1.18秒

💡 分析: 两种方式代码量相当，但LangChain引入了额外的对象类，增加了复杂度
```

## ⚠️ 常见问题

### 问题1: ImportError: cannot import name 'ChatOpenAI'

**解决方案：**
```bash
# LangChain最近版本结构有变化，需要从langchain-openai导入
pip install langchain-openai
```

确保使用正确的导入：
```python
# ✅ 正确的导入方式
from langchain_openai import ChatOpenAI

# ❌ 已弃用的导入方式
from langchain.chat_models import ChatOpenAI
```

### 问题1a: OpenAI API 版本错误

**错误信息：** `You tried to access openai.ChatCompletion, but this is no longer supported in openai>=1.0.0`

**解决方案：**
```bash
# 确保安装的是 openai >= 1.0.0
pip install --upgrade "openai>=1.0.0,<2.0.0"
```

更新代码以使用新版 API：
```python
# ❌ 旧版 API (已弃用)
import openai
response = openai.ChatCompletion.create(...)

# ✅ 新版 API (正确)
from openai import OpenAI
client = OpenAI(api_key="...", base_url="...")
response = client.chat.completions.create(...)
```

### 问题2: openai.error.RateLimitError

**解决方案：**
- 检查API密钥是否有效
- 检查账户余额
- 添加延时或重试机制

### 问题3: SSL证书错误

**解决方案：**
```bash
# 更新证书
pip install --upgrade certifi

# 或者使用代理
export https_proxy=http://127.0.0.1:7890
```

### 问题4: Agent演示无法运行

**原因：** 缺少SERPAPI_API_KEY

**解决方案：**
1. 访问 https://serpapi.com 注册账号
2. 获取免费API密钥（每月100次免费查询）
3. 设置环境变量：`export SERPAPI_API_KEY='your-key'`

## 🎯 学习要点

通过这些演示，你将理解：

1. **抽象的代价**
   - LangChain引入的抽象层并不总是带来价值
   - 有时简单的原生Python代码更清晰

2. **透明度的重要性**
   - Agent每步都调用API这个关键信息应该明确告知
   - 隐藏的性能特征会导致意外成本

3. **选择工具的原则**
   - 评估库是否解决实际问题
   - 避免"为了用而用"

4. **Hello World的重要性**
   - 如果Hello World都很复杂，实际使用会更痛苦
   - 好的库应该降低而非提高学习曲线

## 📚 相关资源

- [DeepSeek官方网站](https://platform.deepseek.com)
- [DeepSeek API文档](https://platform.deepseek.com/api-docs)
- [LangChain官方文档](https://python.langchain.com/docs/get_started/introduction)
- [原文章讨论](https://news.ycombinator.com/item?id=36645575)

## 🔧 调试技巧

### 打印详细日志

```bash
# 启用LangChain的详细日志
export LANGCHAIN_VERBOSE=true
python3 langchain_critique_demo.py
```

### DeepSeek API配置

DeepSeek API兼容OpenAI格式，主要配置：

**新版 OpenAI API (>= 1.0.0):**
```python
from openai import OpenAI

client = OpenAI(
    api_key="your-deepseek-api-key",
    base_url="https://api.deepseek.com"
)

# 调用示例
response = client.chat.completions.create(
    model="deepseek-chat",
    messages=[{"role": "user", "content": "Hello"}]
)
```

**旧版 API (已弃用):**
```python
import openai

openai.api_base = "https://api.deepseek.com"
openai.api_key = "your-deepseek-api-key"
model = "deepseek-chat"
```

### 监控API调用次数

```python
# 在脚本中添加计数器
api_call_count = 0

# 在每次API调用后
api_call_count += 1
print(f"API调用次数: {api_call_count}")
```

## 🎓 延伸学习

完成这些演示后，建议尝试：

1. 直接使用DeepSeek API实现一个简单的Agent
2. 对比不同AI提供商（DeepSeek vs OpenAI）的性能
3. 测试不同prompt策略的效果
4. 评估其他AI框架（如LlamaIndex、Haystack）

## 📞 问题反馈

如果遇到任何问题：
1. 检查Python和依赖版本
2. 验证API密钥是否正确
3. 查看完整的错误堆栈信息
4. 参考常见问题部分

---

**祝你学习愉快！🚀**
