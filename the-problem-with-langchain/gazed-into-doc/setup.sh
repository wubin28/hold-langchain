#!/bin/bash

# LangChain v1.0 Examples Setup Script

echo "=================================="
echo "LangChain v1.0 Examples Setup"
echo "=================================="
echo ""

# Check Python version
echo "Checking Python version..."
python3 --version

# Create virtual environment
echo ""
echo "Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo ""
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo ""
echo "Upgrading pip..."
pip install --upgrade pip

# Install requirements
echo ""
echo "Installing requirements..."
pip install -r requirements.txt

echo ""
echo "=================================="
echo "Setup Complete!"
echo "=================================="
echo ""
echo "Next steps:"
echo "1. Activate the virtual environment:"
echo "   source venv/bin/activate"
echo "2. Set your DeepSeek API key (for current session only):"
echo "   export DEEPSEEK_API_KEY='your-api-key'"
echo "   Or use the quickstart.sh script which will prompt for it securely"
echo "3. Run examples using the quickstart script:"
echo "   ./quickstart.sh"
echo "   Or run any example directly:"
echo "   python example1_system_prompt_fixed.py"
echo ""

