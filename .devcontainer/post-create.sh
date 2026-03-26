#!/bin/bash
set -e

echo ""
echo "=============================================="
echo "  Setting up ABA Clinical Agent..."
echo "=============================================="
echo ""

# Install system dependencies
echo "[1/5] Installing system packages..."
sudo apt-get update -qq && sudo apt-get install -y -qq poppler-utils > /dev/null 2>&1
echo "  OK: poppler-utils (PDF analysis)"

# Install Claude Code CLI
echo "[2/5] Installing Claude Code..."
npm install -g @anthropic-ai/claude-code > /dev/null 2>&1
echo "  OK: Claude Code CLI"

# Install Python dependencies
echo "[3/5] Installing Python packages..."
pip install -q openpyxl
echo "  OK: openpyxl (Excel reports)"

# Run language setup
LANG=${ABA_LANG:-en}
echo "[4/5] Setting up language: $LANG..."
python scripts/setup.py --lang "$LANG" --force-vault

# Copy settings template
echo "[5/5] Configuring permissions..."
if [ ! -f .claude/settings.local.json ]; then
  cp .claude/settings.local.json.example .claude/settings.local.json
  echo "  OK: settings.local.json created from template"
else
  echo "  SKIP: settings.local.json already exists"
fi

echo ""
echo "=============================================="
echo ""
echo "  ABA Clinical Agent is ready!"
echo ""
echo "  Quick start:"
echo "    1. Set your API key (if not already done):"
echo "       export ANTHROPIC_API_KEY=sk-ant-..."
echo ""
echo "    2. Launch the system:"
echo "       claude"
echo ""
echo "    3. Or use the one-click starter:"
echo "       bash scripts/start.sh"
echo ""
echo "  Need help? See docs/hosted-quickstart.md"
echo ""
echo "=============================================="
echo ""
