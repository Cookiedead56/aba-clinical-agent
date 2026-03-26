#!/bin/bash
# ABA Clinical Agent - One-click launcher
# Usage: bash scripts/start.sh

# Check for API key
if [ -z "$ANTHROPIC_API_KEY" ]; then
  echo ""
  echo "  No API key found."
  echo ""
  echo "  Please set your Anthropic API key first:"
  echo "    export ANTHROPIC_API_KEY=sk-ant-your-key-here"
  echo ""
  echo "  Or add it as a Codespace Secret:"
  echo "    https://github.com/settings/codespaces"
  echo "    Secret name: ANTHROPIC_API_KEY"
  echo ""
  exit 1
fi

# Check if Claude Code is installed
if ! command -v claude &> /dev/null; then
  echo "Installing Claude Code..."
  npm install -g @anthropic-ai/claude-code
fi

# Launch Claude Code
echo ""
echo "Starting ABA Clinical Agent..."
echo ""
claude
