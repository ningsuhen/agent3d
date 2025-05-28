#!/bin/bash

# VS Code DDD Navigator Extension Install Script
# This script builds and installs the DDD Navigator extension to VS Code

set -e  # Exit on any error

echo "🚀 Installing VS Code DDD Navigator Extension..."

# Check if we're in the right directory
if [ ! -f "package.json" ]; then
    echo "❌ Error: package.json not found. Please run this script from the vscode-ddd-navigator directory."
    exit 1
fi

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Error: Node.js is not installed. Please install Node.js first."
    echo "   Visit: https://nodejs.org/"
    exit 1
fi

# Check if npm is installed
if ! command -v npm &> /dev/null; then
    echo "❌ Error: npm is not installed. Please install npm first."
    exit 1
fi

# Check if VS Code is installed
CODE_CMD=""
if command -v code &> /dev/null; then
    CODE_CMD="code"
elif [ -f "/Applications/Visual Studio Code.app/Contents/Resources/app/bin/code" ]; then
    CODE_CMD="/Applications/Visual Studio Code.app/Contents/Resources/app/bin/code"
else
    echo "❌ Error: VS Code CLI is not available. Please ensure VS Code is installed and 'code' command is in PATH."
    echo "   In VS Code: Cmd/Ctrl+Shift+P → 'Shell Command: Install code command in PATH'"
    exit 1
fi

echo "✅ Found VS Code at: $CODE_CMD"

# Check if vsce (VS Code Extension Manager) is installed
if ! command -v vsce &> /dev/null; then
    echo "📦 Installing vsce (VS Code Extension Manager)..."
    npm install -g vsce
fi

echo "📋 Checking dependencies..."

# Install dependencies
echo "📦 Installing npm dependencies..."
npm install

# Install TypeScript if not available
if ! command -v tsc &> /dev/null; then
    echo "📦 Installing TypeScript..."
    npm install -g typescript
fi

echo "🔨 Building extension..."

# Compile TypeScript
npm run compile

# Check if compilation was successful
if [ ! -d "out" ]; then
    echo "❌ Error: Compilation failed. 'out' directory not found."
    exit 1
fi

echo "📦 Packaging extension..."

# Package the extension
vsce package

# Find the generated .vsix file
VSIX_FILE=$(find . -name "*.vsix" -type f | head -n 1)

if [ -z "$VSIX_FILE" ]; then
    echo "❌ Error: No .vsix file found. Packaging may have failed."
    exit 1
fi

echo "📥 Installing extension to VS Code..."

# Install the extension
if "$CODE_CMD" --install-extension "$VSIX_FILE"; then
    echo "✅ Successfully installed DDD Navigator extension!"
    echo ""
    echo "🎉 Installation Complete!"
    echo ""
    echo "📖 Next Steps:"
    echo "   1. Restart VS Code to activate the extension"
    echo "   2. Open a markdown file with test cases (TC-####) or requirements (REQ-###)"
    echo "   3. Try Ctrl+Click on identifiers to navigate"
    echo "   4. Use Ctrl+Shift+T to quick-navigate to test cases"
    echo "   5. Use Ctrl+Shift+R to quick-navigate to requirements"
    echo ""
    echo "📁 Example files are available in the 'example' directory"
    echo "⚙️  Configure the extension via VS Code Settings → Extensions → DDD Navigator"
    echo ""
    echo "🔧 Commands available:"
    echo "   - DDD Navigator: Go to Test Case (Ctrl+Shift+T)"
    echo "   - DDD Navigator: Go to Requirement (Ctrl+Shift+R)"
    echo "   - DDD Navigator: Go to Feature (Ctrl+Shift+F)"
    echo "   - DDD Navigator: Show Related Items"
    echo "   - DDD Navigator: Refresh Index"
else
    echo "❌ Error: Failed to install extension to VS Code."
    exit 1
fi

# Clean up
echo "🧹 Cleaning up..."
rm -f "$VSIX_FILE"

echo "🎯 Ready to use! Open VS Code and start navigating your documentation!"
