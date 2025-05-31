#!/bin/bash
# Agent3D Full DDD Pass Execution Wrapper
#
# This script provides a convenient wrapper for executing the Full DDD Pass
# using the LangGraph orchestrator and SWE-bench agent integration.

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to show usage
show_usage() {
    cat << EOF
Agent3D Full DDD Pass Execution

Usage: $0 [OPTIONS]

OPTIONS:
    -t, --task TASK         Task description (default: comprehensive pass)
    -m, --mode MODE         Execution mode: complete|incremental (default: complete)
    -c, --cleanup           Enable cleanup after execution (default)
    --no-cleanup            Disable cleanup after execution
    -v, --verbose           Enable verbose logging
    -h, --help              Show this help message

EXAMPLES:
    $0                                          # Run comprehensive DDD pass
    $0 -t "Implement user authentication"      # Run with custom task
    $0 -m incremental --no-cleanup             # Incremental mode without cleanup
    $0 -t "Refactor API endpoints" -v          # Verbose execution

ENVIRONMENT:
    ANTHROPIC_API_KEY       Required for Claude API access
    PYTHONPATH              Will be set automatically

For more information, see: docs/QUICK-START.md
EOF
}

# Function to check prerequisites
check_prerequisites() {
    print_status "Checking prerequisites..."

    # Check if we're in the right directory
    if [[ ! -f "AGENT-GUIDELINES.yml" ]]; then
        print_error "Not in an Agent3D project directory (AGENT-GUIDELINES.yml not found)"
        print_error "Please run this script from the Agent3D project root"
        exit 1
    fi

    # Check Python
    if ! command -v python3 &> /dev/null; then
        print_error "Python 3 is required but not installed"
        exit 1
    fi

    # Check virtual environment
    if [[ -d "venv" ]]; then
        print_status "Activating virtual environment..."
        source venv/bin/activate
    else
        print_warning "No virtual environment found (venv/). Consider creating one."
    fi

    # Check API key (either Google or Anthropic)
    if [[ -z "${GOOGLE_API_KEY}" && -z "${ANTHROPIC_API_KEY}" ]]; then
        print_error "Either GOOGLE_API_KEY or ANTHROPIC_API_KEY environment variable is required"
        print_error "For Gemini: export GOOGLE_API_KEY=your_google_api_key"
        print_error "For Claude: export ANTHROPIC_API_KEY=your_anthropic_api_key"
        exit 1
    fi

    if [[ -n "${GOOGLE_API_KEY}" ]]; then
        print_success "Using Google Gemini API"
    elif [[ -n "${ANTHROPIC_API_KEY}" ]]; then
        print_success "Using Anthropic Claude API"
    fi

    # Check if the main script exists
    if [[ ! -f "run_full_ddd_pass.py" ]]; then
        print_error "Main execution script not found: run_full_ddd_pass.py"
        exit 1
    fi

    print_success "Prerequisites check passed"
}

# Function to setup environment
setup_environment() {
    print_status "Setting up execution environment..."

    # Load environment keys if available
    if [[ -f ~/.env.keys.sh ]]; then
        print_status "Loading environment keys from ~/.env.keys.sh"
        source ~/.env.keys.sh
    fi

    # Create temporary directory
    mkdir -p .agent3d-tmp/logs

    # Set Python path
    export PYTHONPATH="${SCRIPT_DIR}:${PYTHONPATH}"

    print_success "Environment setup complete"
}

# Function to run the DDD pass
run_ddd_pass() {
    local task="$1"
    local mode="$2"
    local cleanup="$3"
    local verbose="$4"

    print_status "Starting Full DDD Pass execution..."
    print_status "Task: $task"
    print_status "Mode: $mode"
    print_status "Cleanup: $cleanup"

    # Build command arguments
    local cmd_args=()
    cmd_args+=("--task" "$task")
    cmd_args+=("--mode" "$mode")

    if [[ "$cleanup" == "true" ]]; then
        cmd_args+=("--cleanup")
    else
        cmd_args+=("--no-cleanup")
    fi

    if [[ "$verbose" == "true" ]]; then
        cmd_args+=("--verbose")
    fi

    # Execute the main script
    print_status "Executing: python3 run_full_ddd_pass.py ${cmd_args[*]}"

    if python3 run_full_ddd_pass.py "${cmd_args[@]}"; then
        print_success "Full DDD Pass completed successfully!"
        return 0
    else
        print_error "Full DDD Pass failed!"
        return 1
    fi
}

# Main execution
main() {
    # Default values
    local task="Execute comprehensive DDD pass for project alignment and quality improvement"
    local mode="complete"
    local cleanup="true"
    local verbose="false"

    # Parse command line arguments
    while [[ $# -gt 0 ]]; do
        case $1 in
            -t|--task)
                task="$2"
                shift 2
                ;;
            -m|--mode)
                mode="$2"
                if [[ "$mode" != "complete" && "$mode" != "incremental" ]]; then
                    print_error "Invalid mode: $mode. Must be 'complete' or 'incremental'"
                    exit 1
                fi
                shift 2
                ;;
            -c|--cleanup)
                cleanup="true"
                shift
                ;;
            --no-cleanup)
                cleanup="false"
                shift
                ;;
            -v|--verbose)
                verbose="true"
                shift
                ;;
            -h|--help)
                show_usage
                exit 0
                ;;
            *)
                print_error "Unknown option: $1"
                show_usage
                exit 1
                ;;
        esac
    done

    # Show banner
    echo
    echo "🎯 Agent3D Full DDD Pass Execution"
    echo "=================================="
    echo

    # Run the process
    check_prerequisites
    setup_environment

    if run_ddd_pass "$task" "$mode" "$cleanup" "$verbose"; then
        echo
        print_success "🎉 Full DDD Pass execution completed!"
        echo
        print_status "Next steps:"
        print_status "1. Review the execution logs in .agent3d-tmp/logs/"
        print_status "2. Check the updated documentation and code"
        print_status "3. Run tests to validate changes"
        print_status "4. Commit changes if satisfied with results"
        echo
        exit 0
    else
        echo
        print_error "❌ Full DDD Pass execution failed!"
        echo
        print_status "Troubleshooting:"
        print_status "1. Check the logs in .agent3d-tmp/logs/ for details"
        print_status "2. Verify all prerequisites are met"
        print_status "3. Check API key and network connectivity"
        print_status "4. Try running with --verbose for more information"
        echo
        exit 1
    fi
}

# Handle interruption gracefully
trap 'echo; print_warning "Execution interrupted by user"; exit 130' INT

# Run main function
main "$@"
