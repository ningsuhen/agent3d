@echo off
setlocal enabledelayedexpansion

REM VS Code DDD Navigator Extension Install Script (Windows)
REM This script builds and installs the DDD Navigator extension to VS Code

echo 🚀 Installing VS Code DDD Navigator Extension...

REM Check if we're in the right directory
if not exist "package.json" (
    echo ❌ Error: package.json not found. Please run this script from the vscode-ddd-navigator directory.
    pause
    exit /b 1
)

REM Check if Node.js is installed
node --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Error: Node.js is not installed. Please install Node.js first.
    echo    Visit: https://nodejs.org/
    pause
    exit /b 1
)

REM Check if npm is installed
npm --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Error: npm is not installed. Please install npm first.
    pause
    exit /b 1
)

REM Check if VS Code is installed
code --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Error: VS Code CLI is not available. Please ensure VS Code is installed and 'code' command is in PATH.
    echo    In VS Code: Ctrl+Shift+P → 'Shell Command: Install code command in PATH'
    pause
    exit /b 1
)

REM Check if vsce is installed
vsce --version >nul 2>&1
if errorlevel 1 (
    echo 📦 Installing vsce (VS Code Extension Manager)...
    npm install -g vsce
)

echo 📋 Checking dependencies...

REM Install dependencies
echo 📦 Installing npm dependencies...
npm install

REM Install TypeScript if not available
tsc --version >nul 2>&1
if errorlevel 1 (
    echo 📦 Installing TypeScript...
    npm install -g typescript
)

echo 🔨 Building extension...

REM Compile TypeScript
npm run compile

REM Check if compilation was successful
if not exist "out" (
    echo ❌ Error: Compilation failed. 'out' directory not found.
    pause
    exit /b 1
)

echo 📦 Packaging extension...

REM Package the extension
vsce package

REM Find the generated .vsix file
for %%f in (*.vsix) do set VSIX_FILE=%%f

if "!VSIX_FILE!"=="" (
    echo ❌ Error: No .vsix file found. Packaging may have failed.
    pause
    exit /b 1
)

echo 📥 Installing extension to VS Code...

REM Install the extension
code --install-extension "!VSIX_FILE!"

if errorlevel 0 (
    echo ✅ Successfully installed DDD Navigator extension!
    echo.
    echo 🎉 Installation Complete!
    echo.
    echo 📖 Next Steps:
    echo    1. Restart VS Code to activate the extension
    echo    2. Open a markdown file with test cases (TC-####) or requirements (REQ-###)
    echo    3. Try Ctrl+Click on identifiers to navigate
    echo    4. Use Ctrl+Shift+T to quick-navigate to test cases
    echo    5. Use Ctrl+Shift+R to quick-navigate to requirements
    echo.
    echo 📁 Example files are available in the 'example' directory
    echo ⚙️  Configure the extension via VS Code Settings → Extensions → DDD Navigator
    echo.
    echo 🔧 Commands available:
    echo    - DDD Navigator: Go to Test Case (Ctrl+Shift+T)
    echo    - DDD Navigator: Go to Requirement (Ctrl+Shift+R)
    echo    - DDD Navigator: Go to Feature (Ctrl+Shift+F)
    echo    - DDD Navigator: Show Related Items
    echo    - DDD Navigator: Refresh Index
) else (
    echo ❌ Error: Failed to install extension to VS Code.
    pause
    exit /b 1
)

REM Clean up
echo 🧹 Cleaning up...
del "!VSIX_FILE!" >nul 2>&1

echo 🎯 Ready to use! Open VS Code and start navigating your documentation!
pause
