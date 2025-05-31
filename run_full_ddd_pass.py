#!/usr/bin/env python3
"""
Full DDD Pass Execution Script with Orchestrator and SWE-bench Agent

This script executes a comprehensive Documentation-Driven Development (DDD) pass
using the LangGraph orchestrator and Augment SWE-bench agent integration.

Usage:
    python run_full_ddd_pass.py [--task "custom task"] [--mode complete|incremental] [--cleanup]
"""

import argparse
import logging
import os
import sys
import time
from pathlib import Path
from typing import Dict, Any

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

try:
    from agents.orchestrator import create_orchestrator_graph, ORCHESTRATOR_METADATA
    from agents.orchestrator.token_tracker import TokenTracker
    from agents.orchestrator.tools import VectorSearchTool
except ImportError as e:
    print(f"❌ Failed to import orchestrator components: {e}")
    print("Please ensure all dependencies are installed and the project is properly set up.")
    sys.exit(1)


def setup_logging(verbose: bool = False) -> logging.Logger:
    """Set up logging configuration."""
    level = logging.DEBUG if verbose else logging.INFO

    # Create logs directory if it doesn't exist
    logs_dir = Path(".agent3d-tmp/logs")
    logs_dir.mkdir(parents=True, exist_ok=True)

    # Configure logging
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(logs_dir / f"full_ddd_pass_{int(time.time())}.log"),
            logging.StreamHandler(sys.stdout)
        ]
    )

    return logging.getLogger(__name__)


def check_prerequisites() -> Dict[str, bool]:
    """Check if all prerequisites are met for running the full DDD pass."""
    checks = {}

    # Check if we're in a valid Agent3D project
    checks["agent3d_project"] = Path("AGENT-GUIDELINES.yml").exists()

    # Check if docs directory exists
    checks["docs_directory"] = Path("docs").exists()

    # Check if DDD-STATUS file exists
    checks["ddd_status"] = Path("docs/DDD-STATUS.yml").exists()

    # Check if passes configuration exists
    checks["passes_config"] = Path("passes.yml").exists()

    # Check if SWE-bench agent is available
    try:
        from agents.swebench.agent import SWEBenchAgent
        checks["swebench_agent"] = True
    except ImportError:
        checks["swebench_agent"] = False

    # Check if LangGraph is available
    try:
        import langgraph
        checks["langgraph"] = True
    except ImportError:
        checks["langgraph"] = False

    # Check for required environment variables (either Gemini or Anthropic)
    checks["api_key_available"] = "GOOGLE_API_KEY" in os.environ or "ANTHROPIC_API_KEY" in os.environ

    return checks


def print_prerequisites_status(checks: Dict[str, bool], logger: logging.Logger):
    """Print the status of prerequisites."""
    logger.info("🔍 Checking prerequisites for Full DDD Pass...")

    all_passed = True
    for check_name, passed in checks.items():
        status = "✅" if passed else "❌"
        logger.info(f"  {status} {check_name.replace('_', ' ').title()}")
        if not passed:
            all_passed = False

    if not all_passed:
        logger.error("❌ Some prerequisites are not met. Please address the issues above.")
        return False

    logger.info("✅ All prerequisites met!")
    return True


def initialize_ddd_status_for_complete_mode(logger: logging.Logger):
    """Initialize DDD status for complete mode execution."""
    logger.info("🔄 Initializing DDD status for complete mode...")

    ddd_status_path = Path("docs/DDD-STATUS.yml")

    # Empty the DDD status file as per Agent Guidelines
    try:
        with open(ddd_status_path, 'w') as f:
            f.write("")  # Empty file for fresh start
        logger.info("✅ DDD-STATUS.yml emptied for fresh evaluation")
    except Exception as e:
        logger.error(f"❌ Failed to initialize DDD status: {e}")
        raise


def create_execution_context(mode: str, task: str) -> Dict[str, Any]:
    """Create execution context for the orchestrator."""
    return {
        "execution_mode": mode,
        "task_description": task,
        "ddd_framework": "agent3d",
        "orchestrator_version": ORCHESTRATOR_METADATA["version"],
        "timestamp": time.time(),
        "project_root": str(Path.cwd()),
        "quality_requirements": [
            "ddd_compliance",
            "documentation_sync",
            "test_coverage",
            "code_quality"
        ]
    }


def execute_full_ddd_pass(
    task: str,
    mode: str,
    cleanup: bool,
    logger: logging.Logger
) -> Dict[str, Any]:
    """Execute the full DDD pass using the orchestrator."""

    logger.info(f"🚀 Starting Full DDD Pass execution...")
    logger.info(f"   Task: {task}")
    logger.info(f"   Mode: {mode}")
    logger.info(f"   Cleanup: {cleanup}")

    # Initialize for complete mode if needed
    if mode == "complete":
        initialize_ddd_status_for_complete_mode(logger)

    # Create execution context
    context = create_execution_context(mode, task)

    # Create orchestrator
    logger.info("🔧 Initializing LangGraph orchestrator with SWE-bench agent...")
    orchestrator = create_orchestrator_graph(
        logger=logger,
        max_iterations=3,  # Reduce iterations to avoid quota issues
        enable_swebench=True
    )

    # Execute the task with monitoring
    logger.info("⚡ Executing task with full monitoring...")
    result = orchestrator.execute_task_with_monitoring(
        task=task,
        cleanup_after=cleanup
    )

    return result


def print_execution_summary(result: Dict[str, Any], logger: logging.Logger):
    """Print a detailed execution summary."""
    logger.info("\n" + "="*80)
    logger.info("📊 FULL DDD PASS EXECUTION SUMMARY")
    logger.info("="*80)

    # Basic status
    status = result.get("status", "unknown")
    logger.info(f"🎯 Overall Status: {status}")

    # Monitoring information
    if "monitoring" in result:
        monitoring = result["monitoring"]

        # Execution time
        exec_time = monitoring.get("execution_time", 0)
        logger.info(f"⏱️  Total Execution Time: {exec_time:.2f} seconds")

        # Token usage
        if "token_usage" in monitoring:
            token_stats = monitoring["token_usage"]
            logger.info(f"\n💰 Resource Usage:")
            logger.info(f"   📞 API Calls: {token_stats.get('total_calls', 0)}")
            logger.info(f"   🎯 Total Tokens: {token_stats.get('total_tokens', 0):,}")
            logger.info(f"   💵 Estimated Cost: ${token_stats.get('total_cost', 0):.4f}")

        # Vector database stats
        if "vector_db_stats" in monitoring and monitoring["vector_db_stats"]:
            vdb_stats = monitoring["vector_db_stats"]
            logger.info(f"\n🔍 Vector Database:")
            logger.info(f"   📁 Files Indexed: {vdb_stats.get('total_files', 0)}")
            logger.info(f"   📊 Code Chunks: {vdb_stats.get('total_chunks', 0)}")

    # File processing results
    if "completed_files" in result:
        files = result["completed_files"]
        logger.info(f"\n📁 Files Processed: {len(files)}")

        successful = [f for f in files if f.get("status") == "completed"]
        failed = [f for f in files if f.get("status") == "failed"]

        logger.info(f"   ✅ Successful: {len(successful)}")
        logger.info(f"   ❌ Failed: {len(failed)}")

        if failed:
            logger.info("   Failed files:")
            for file_info in failed[:3]:  # Show first 3 failed files
                logger.info(f"     • {file_info.get('path', 'unknown')}")

    # Cleanup results
    if "cleanup" in result:
        cleanup = result["cleanup"]
        if cleanup.get("total_freed", 0) > 0:
            logger.info(f"\n🧹 Cleanup Results:")
            logger.info(f"   🗑️  Files Deleted: {len(cleanup.get('deleted_files', []))}")
            logger.info(f"   📂 Directories Deleted: {len(cleanup.get('deleted_directories', []))}")
            logger.info(f"   💾 Space Freed: {cleanup.get('total_freed', 0):,} bytes")

    # Messages
    if "messages" in result and result["messages"]:
        logger.info(f"\n📝 Key Messages:")
        for message in result["messages"][-5:]:  # Show last 5 messages
            logger.info(f"   • {message}")

    logger.info("="*80)


def load_environment_keys():
    """Load environment keys from ~/.env.keys.sh if available."""
    env_keys_path = os.path.expanduser("~/.env.keys.sh")
    if os.path.exists(env_keys_path):
        try:
            # Read and execute the shell script to extract environment variables
            import subprocess
            result = subprocess.run(
                f"source {env_keys_path} && env",
                shell=True,
                capture_output=True,
                text=True,
                executable="/bin/bash"
            )
            if result.returncode == 0:
                for line in result.stdout.split('\n'):
                    if '=' in line and not line.startswith('_'):
                        key, value = line.split('=', 1)
                        os.environ[key] = value
                print(f"✅ Loaded environment keys from {env_keys_path}")
            else:
                print(f"⚠️ Failed to load environment keys: {result.stderr}")
        except Exception as e:
            print(f"⚠️ Error loading environment keys: {e}")


def main():
    """Main entry point for the Full DDD Pass execution."""
    # Load environment keys first
    load_environment_keys()

    parser = argparse.ArgumentParser(
        description="Execute a Full DDD Pass using Orchestrator and SWE-bench Agent",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python run_full_ddd_pass.py
  python run_full_ddd_pass.py --task "Implement user authentication system"
  python run_full_ddd_pass.py --mode incremental --no-cleanup
  python run_full_ddd_pass.py --task "Refactor API endpoints" --verbose
        """
    )

    parser.add_argument(
        "--task",
        default="Execute comprehensive DDD pass for project alignment and quality improvement",
        help="Task description for the DDD pass (default: comprehensive pass)"
    )

    parser.add_argument(
        "--mode",
        choices=["complete", "incremental"],
        default="complete",
        help="Execution mode: complete (fresh start) or incremental (targeted) (default: complete)"
    )

    parser.add_argument(
        "--cleanup",
        action="store_true",
        default=True,
        help="Clean up temporary files after execution (default: True)"
    )

    parser.add_argument(
        "--no-cleanup",
        action="store_false",
        dest="cleanup",
        help="Skip cleanup of temporary files"
    )

    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose logging"
    )

    args = parser.parse_args()

    # Set up logging
    logger = setup_logging(args.verbose)

    logger.info("🎯 Agent3D Full DDD Pass Execution")
    logger.info(f"   Orchestrator Version: {ORCHESTRATOR_METADATA['version']}")
    logger.info(f"   LangGraph Version: {ORCHESTRATOR_METADATA['langgraph_version']}")

    try:
        # Check prerequisites
        checks = check_prerequisites()
        if not print_prerequisites_status(checks, logger):
            sys.exit(1)

        # Execute the full DDD pass
        result = execute_full_ddd_pass(
            task=args.task,
            mode=args.mode,
            cleanup=args.cleanup,
            logger=logger
        )

        # Print summary
        print_execution_summary(result, logger)

        # Exit with appropriate code
        if result.get("status") in ["completed", "completed_fallback"]:
            logger.info("🎉 Full DDD Pass completed successfully!")
            sys.exit(0)
        else:
            logger.error("❌ Full DDD Pass failed!")
            sys.exit(1)

    except KeyboardInterrupt:
        logger.info("⚠️ Execution interrupted by user")
        sys.exit(130)
    except Exception as e:
        logger.error(f"❌ Unexpected error: {e}")
        if args.verbose:
            import traceback
            logger.error(traceback.format_exc())
        sys.exit(1)


if __name__ == "__main__":
    main()
