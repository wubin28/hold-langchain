#!/bin/bash
# LangChain批评演示 - 快速启动脚本
# 适用于macOS iTerm2/zsh环境

set -e  # 遇到错误立即退出

echo "=================================="
echo "LangChain批评演示 - 快速启动向导"
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

echo "正在安装OpenAI库（用于DeepSeek API）..."
pip install -q "openai>=1.0.0,<2.0.0"

echo "正在安装LangChain..."
pip install -q langchain langchain-openai langchain-community

echo "正在安装SerpAPI（Agent演示需要）..."
pip install -q google-search-results

echo "✅ 依赖安装完成"

# 检查API密钥
echo ""
echo "📍 步骤4: 检查API密钥..."

if [ -z "$DEEPSEEK_API_KEY" ]; then
    echo "⚠️  未检测到DEEPSEEK_API_KEY环境变量"
    echo ""
    echo "请输入你的DeepSeek API密钥（可以从 https://platform.deepseek.com 获取）："
    read -s DEEPSEEK_API_KEY
    export DEEPSEEK_API_KEY
    echo ""
    echo "✅ API密钥已设置（当前会话有效）"
    echo ""
else
    echo "✅ 检测到DEEPSEEK_API_KEY"
fi

if [ -z "$SERPAPI_API_KEY" ]; then
    echo "⚠️  未检测到SERPAPI_API_KEY（Agent演示需要）"
    echo ""
    echo "是否现在设置SERPAPI_API_KEY？(y/n)"
    echo "（可以从 https://serpapi.com 注册获取免费密钥，跳过则无法运行Agent演示）"
    read -r answer
    if [ "$answer" = "y" ] || [ "$answer" = "Y" ]; then
        echo "请输入你的SerpAPI密钥："
        read -s SERPAPI_API_KEY
        export SERPAPI_API_KEY
        echo ""
        echo "✅ SerpAPI密钥已设置"
    else
        echo "⏭️  跳过SerpAPI设置（Agent演示将无法运行）"
    fi
else
    echo "✅ 检测到SERPAPI_API_KEY"
fi

# 显示菜单
echo ""
echo "=================================="
echo "🎯 准备完成！请选择要运行的演示："
echo "=================================="
echo ""
echo "1. 运行主演示 - 缺点1-3对比"
echo "   （过度使用对象类、Prompt模板复杂、对话记忆复杂）"
echo ""
echo "2. 运行Agent演示 - 缺点4-5对比"
echo "   （Agent性能问题、实现不透明）"
echo ""
echo "3. 运行全部演示"
echo ""
echo "4. 退出"
echo ""
echo -n "请输入选项 (1-4): "
read -r choice

case $choice in
    1)
        echo ""
        echo "🚀 运行主演示..."
        echo ""
        python3 langchain_critique_demo.py
        ;;
    2)
        echo ""
        echo "🚀 运行Agent演示..."
        echo ""
        python3 langchain_agent_performance_demo.py
        ;;
    3)
        echo ""
        echo "🚀 运行全部演示..."
        echo ""
        python3 langchain_critique_demo.py
        echo ""
        echo "=================================="
        echo "按Enter继续运行Agent演示..."
        read -r
        python3 langchain_agent_performance_demo.py
        ;;
    4)
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
echo "   - 查看详细文档: cat README.md"
echo "   - 退出虚拟环境: deactivate"
echo ""
