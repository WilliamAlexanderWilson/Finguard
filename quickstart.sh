#!/bin/bash

# FinGuard Quick Start Script
# This script helps you get started with FinGuard

echo "======================================"
echo "   FinGuard Quick Start Setup"
echo "======================================"
echo ""

# Check Python version
echo "Checking Python version..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found. Please install Python 3.8 or higher."
    exit 1
fi

PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
echo "✅ Python $PYTHON_VERSION detected"
echo ""

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt
echo "✅ Dependencies installed"
echo ""

# Run tests
echo "Running tests..."
python3 tests/test_categorization.py
if [ $? -eq 0 ]; then
    echo "✅ Tests passed"
else
    echo "❌ Tests failed"
    exit 1
fi
echo ""

# Run demo
echo "Running demo with sample data..."
python3 examples/demo.py
echo ""

echo "======================================"
echo "   Setup Complete! ✨"
echo "======================================"
echo ""
echo "Next steps:"
echo "  1. Try categorizing your own data:"
echo "     python3 skill/scripts/categorize_transactions.py your_data.csv output.csv"
echo ""
echo "  2. Install the Claude skill:"
echo "     - Create a .skill file from the skill/ directory"
echo "     - Upload to Claude via Settings → Skills"
echo ""
echo "  3. Read the documentation:"
echo "     - docs/USER_GUIDE.md - How to use FinGuard"
echo "     - docs/QUICK_REFERENCE.md - Command cheat sheet"
echo ""
echo "  4. Check out PORTFOLIO_SHOWCASE.md for interview prep"
echo ""
echo "Happy bookkeeping! 🚀"
