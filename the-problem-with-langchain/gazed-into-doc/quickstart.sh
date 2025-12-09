#!/bin/bash
# LangChain v1.0 示例演示 - 快速启动脚本
# 适用于macOS iTerm2/zsh环境

set -e  # 遇到错误立即退出

echo "=================================="
echo "LangChain v1.0 示例演示 - 快速启动向导"
echo "=================================="
echo ""

# 检查Python
echo "📍 步骤1: 检查Python环境..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    echo "✅ 找到Python: $PYTHON_VERSION"
else
    echo "❌ 未找到Python3，请先安装Python 3.8+"
    exit 1
fi

# 检查虚拟环境
echo ""
echo "📍 步骤2: 设置虚拟环境..."
if [ ! -d "venv" ]; then
    echo "创建虚拟环境..."
    python3 -m venv venv
    echo "✅ 虚拟环境创建成功"
else
    echo "✅ 虚拟环境已存在"
fi

# 激活虚拟环境
echo "激活虚拟环境..."
source venv/bin/activate
echo "✅ 虚拟环境已激活"

# 安装依赖
echo ""
echo "📍 步骤3: 安装依赖包..."

# 设置环境变量以支持Python 3.13
export PYO3_USE_ABI3_FORWARD_COMPATIBILITY=1

echo "正在升级pip..."
pip install --upgrade pip -q

echo "正在安装依赖包（从requirements.txt）..."
pip install -q -r requirements.txt

echo "✅ 依赖安装完成"

# 检查API密钥
echo ""
echo "📍 步骤4: 检查API密钥..."

if [ -z "$DEEPSEEK_API_KEY" ]; then
    echo "⚠️  未检测到DEEPSEEK_API_KEY环境变量"
    echo ""
    echo "请输入你的DeepSeek API密钥（可以从 https://platform.deepseek.com/api_keys 获取）："
    read -s DEEPSEEK_API_KEY
    export DEEPSEEK_API_KEY
    echo ""
    echo "✅ API密钥已设置（当前会话有效）"
    echo ""
else
    echo "✅ 检测到DEEPSEEK_API_KEY"
fi

# 显示菜单
echo ""
echo "=================================="
echo "🎯 准备完成！请选择要运行的演示："
echo "=================================="
echo ""
echo "1. 示例1 - System Prompt修复"
echo "   （展示LangChain v1.0如何正确支持system prompt）"
echo ""
echo "2. 示例2 - JSON解析稳定性"
echo "   （展示结构化输出和错误处理）"
echo ""
echo "3. 示例3 - 结构化输出"
echo "   （使用Pydantic模型定义输出格式）"
echo ""
echo "4. 示例4 - DeepSeek Function Calling"
echo "   （展示函数调用能力）"
echo ""
echo "5. 示例5 - 完整Recipe Bot"
echo "   （综合示例：从原料推荐食谱）"
echo ""
echo "6. 运行全部示例"
echo ""
echo "7. 退出"
echo ""
echo -n "请输入选项 (1-7): "
read -r choice

case $choice in
    1)
        echo ""
        echo "🚀 运行示例1 - System Prompt修复..."
        echo ""
        python3 example1_system_prompt_fixed.py
        ;;
    2)
        echo ""
        echo "🚀 运行示例2 - JSON解析稳定性..."
        echo ""
        python3 example2_json_parsing_robust.py
        ;;
    3)
        echo ""
        echo "🚀 运行示例3 - 结构化输出..."
        echo ""
        python3 example3_structured_output.py
        ;;
    4)
        echo ""
        echo "🚀 运行示例4 - DeepSeek Function Calling..."
        echo ""
        python3 example4_function_calling.py
        ;;
    5)
        echo ""
        echo "🚀 运行示例5 - 完整Recipe Bot..."
        echo ""
        python3 example5_complete_recipe_bot.py
        ;;
    6)
        echo ""
        echo "🚀 运行全部示例..."
        echo ""
        echo "=================================="
        echo "示例1 - System Prompt修复"
        echo "=================================="
        python3 example1_system_prompt_fixed.py
        echo ""
        echo "=================================="
        echo "按Enter继续运行示例2..."
        read -r
        echo ""
        echo "=================================="
        echo "示例2 - JSON解析稳定性"
        echo "=================================="
        python3 example2_json_parsing_robust.py
        echo ""
        echo "=================================="
        echo "按Enter继续运行示例3..."
        read -r
        echo ""
        echo "=================================="
        echo "示例3 - 结构化输出"
        echo "=================================="
        python3 example3_structured_output.py
        echo ""
        echo "=================================="
        echo "按Enter继续运行示例4..."
        read -r
        echo ""
        echo "=================================="
        echo "示例4 - DeepSeek Function Calling"
        echo "=================================="
        python3 example4_function_calling.py
        echo ""
        echo "=================================="
        echo "按Enter继续运行示例5..."
        read -r
        echo ""
        echo "=================================="
        echo "示例5 - 完整Recipe Bot"
        echo "=================================="
        python3 example5_complete_recipe_bot.py
        ;;
    7)
        echo "👋 再见！"
        exit 0
        ;;
    *)
        echo "❌ 无效选项"
        exit 1
        ;;
esac

echo ""
echo "=================================="
echo "✅ 演示完成！"
echo "=================================="
echo ""
echo "💡 提示："
echo "   - 要重新运行，请执行: ./quickstart.sh"
echo "   - 查看详细分析: cat analysis-and-langchain-v1-examples.md"
echo "   - 查看README: cat README.md"
echo "   - 退出虚拟环境: deactivate"
echo ""
