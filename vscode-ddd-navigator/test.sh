#!/bin/bash

# VS Code DDD Navigator Extension Test Script
# This script runs the integration tests for the extension

set -e  # Exit on any error

echo "🧪 Running VS Code DDD Navigator Extension Tests..."

# Check if we're in the right directory
if [ ! -f "package.json" ]; then
    echo "❌ Error: package.json not found. Please run this script from the vscode-ddd-navigator directory."
    exit 1
fi

echo "📦 Installing test dependencies..."
npm install

echo "🔨 Compiling TypeScript..."
npm run compile

echo "🧹 Running linter..."
npm run lint

echo "🧪 Running integration tests..."
npm test

echo "✅ All tests completed successfully!"
echo ""
echo "📊 Test Coverage:"
echo "   - Identifier Index Tests: ✅"
echo "   - Definition Provider Tests: ✅"
echo "   - Hover Provider Tests: ✅"
echo "   - Reference Provider Tests: ✅"
echo "   - Performance Tests: ✅"
echo ""
echo "🎯 Test Scenarios Covered:"
echo "   - Basic test case formats (TC-0001)"
echo "   - Complex formats (TC-ENV-002, TC-BATCH-001)"
echo "   - Lowercase suffixes (TC-0003a)"
echo "   - Requirements (REQ-001, REQ-AUTH-001)"
echo "   - Cross-file references"
echo "   - Multiple file types (.md, .js)"
echo "   - Status indicators (✅, ⏸️)"
echo "   - Performance benchmarks"
