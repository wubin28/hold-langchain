# LangChain 2023 Problems vs v1.0 Solutions

这个项目分析了2023年对LangChain的批评，并展示了这些问题在LangChain v1.0中的修复状态。

## 文件说明

- `the-problem-with-langchain-gazed-into-doc.md` - 原始文章（2023年7月）
- `analysis-and-langchain-v1-examples.md` - 完整分析和v1.0示例说明
- `example1_system_prompt_fixed.py` - System Prompt修复示例
- `example2_json_parsing_robust.py` - JSON解析稳定性示例
- `example3_structured_output.py` - 结构化输出示例
- `example4_function_calling.py` - DeepSeek Function Calling示例
- `example5_complete_recipe_bot.py` - 完整Recipe Bot示例

## 快速开始

### 1. 创建虚拟环境

```bash
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 运行示例

**推荐方式：使用快速启动脚本**

```bash
./quickstart.sh
```

脚本会提示你输入DeepSeek API Key（输入时不显示在屏幕上，确保安全）。

**或者手动设置环境变量并运行：**

```bash
# 设置DeepSeek API Key（仅当前会话有效）
export DEEPSEEK_API_KEY='your-api-key-here'

# 示例1: System Prompt修复
python example1_system_prompt_fixed.py

# 示例2: JSON解析稳定性
python example2_json_parsing_robust.py

# 示例3: 结构化输出
python example3_structured_output.py

# 示例4: Function Calling
python example4_function_calling.py

# 示例5: 完整Recipe Bot
python example5_complete_recipe_bot.py
```

## 主要发现

### ✅ 已修复的问题
1. System Prompt支持 - 完全修复
2. JSON解析脆弱性 - 大幅改善
3. 文档质量 - 显著改善
4. 结构化输出 - 通过OpenAI Functions解决

### ⚠️ 部分改善的问题
5. 保证特定字段输出 - 需要使用intermediate_steps
6. 代码复杂度 - 有所改善但仍然存在

详见 `analysis-and-langchain-v1-examples.md` 获取完整分析。

## 依赖版本

- Python 3.8+
- LangChain 0.3.11
- DeepSeek API (deepseek-chat)

## API Key 安全

本项目已配置为安全处理API密钥：
- 不会将API密钥保存到文件中
- 不会在终端输出API密钥
- 仅支持通过环境变量或安全的终端输入方式提供API密钥
- 获取DeepSeek API Key: https://platform.deepseek.com/api_keys

## License

本项目仅用于学习和研究目的。

