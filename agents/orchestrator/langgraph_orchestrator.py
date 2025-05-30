"""
LangGraph Orchestrator for Agent3D Framework

This module implements a LangGraph-based orchestrator that coordinates
specialized agents within the Agent3D DDD framework.
"""

from typing import TypedDict, Annotated, Literal, Dict, Any
import operator
import logging
import time
from datetime import datetime
from pathlib import Path

try:
    from langgraph.graph import StateGraph, END
    LANGGRAPH_AVAILABLE = True
except ImportError as e:
    # Fallback for when LangGraph is not available
    LANGGRAPH_AVAILABLE = False
    StateGraph = None
    END = None

from .tools import DDDAnalysisTool, SWEBenchTool, QualityGatesTool, DDDExecutionPlanTool, VectorSearchTool
from .token_tracker import TokenTracker
from .cleanup_tool import TestFileCleanupTool


class OrchestratorState(TypedDict):
    """State definition for the Agent3D file-focused orchestrator workflow."""

    # Core task information
    task: str
    task_type: str
    complexity: str

    # Scan and planning results
    scan_results: dict
    execution_plan: dict

    # File processing state
    file_queue: Annotated[list, operator.add]
    completed_files: Annotated[list, operator.add]
    current_file: dict

    # Validation results
    validation_result: dict

    # Communication
    messages: Annotated[list, operator.add]

    # DDD-specific state
    ddd_context: dict
    quality_requirements: list

    # Execution metadata
    current_step: str
    iteration_count: int
    max_iterations: int


class Agent3DOrchestratorGraph:
    """
    LangGraph-based orchestrator for Agent3D framework.

    Coordinates multiple specialized agents to execute complex tasks
    while maintaining DDD compliance and quality standards.
    """

    def __init__(
        self,
        logger: logging.Logger = None,
        max_iterations: int = 5,
        enable_swebench: bool = True,
    ):
        """Initialize the orchestrator.

        Args:
            logger: Logger for orchestrator operations
            max_iterations: Maximum workflow iterations
            enable_swebench: Whether to enable SWE-bench agent
        """
        self.logger = logger or logging.getLogger(__name__)
        self.max_iterations = max_iterations
        self.enable_swebench = enable_swebench

        # Initialize tools
        self.ddd_tool = DDDAnalysisTool()
        self.quality_tool = QualityGatesTool()
        self.execution_plan_tool = DDDExecutionPlanTool(logger)
        self.vector_search_tool = VectorSearchTool(logger)
        self.token_tracker = TokenTracker(logger)
        self.cleanup_tool = TestFileCleanupTool(logger)

        # Initialize vector database for current directory
        self._initialize_vector_database()

        if self.enable_swebench:
            try:
                self.swebench_tool = SWEBenchTool()
            except Exception as e:
                self.logger.warning(f"SWE-bench agent not available: {e}")
                self.enable_swebench = False

        # Create the workflow graph
        self.graph = self._create_graph() if LANGGRAPH_AVAILABLE else None

        if not LANGGRAPH_AVAILABLE:
            self.logger.warning("LangGraph not available. Orchestrator will use fallback mode.")

    def _initialize_vector_database(self):
        """Initialize the vector database for the current repository."""
        try:
            current_dir = Path.cwd()
            self.logger.info(f"🔍 Initializing vector database for: {current_dir}")

            # Index the current repository
            result = self.vector_search_tool.initialize_and_index_repository(str(current_dir))

            if result["status"] == "success":
                stats = result["stats"]
                self.logger.info(
                    f"✅ Vector database initialized: {stats['chunks_created']} chunks "
                    f"from {stats['files_processed']} files"
                )
            elif result["status"] == "empty":
                self.logger.warning("⚠️ Vector database initialized but no content indexed")
            else:
                self.logger.error(f"❌ Vector database initialization failed: {result.get('error', 'Unknown error')}")

        except Exception as e:
            self.logger.error(f"Failed to initialize vector database: {e}")
            # Continue without vector search capabilities

    def execute_task_with_monitoring(self, task: str, cleanup_after: bool = True) -> Dict[str, Any]:
        """Execute a task with full monitoring and optional cleanup.

        Args:
            task: Task description
            cleanup_after: Whether to clean up test files after execution

        Returns:
            Execution results with monitoring data
        """
        self.logger.info(f"🚀 Starting monitored task execution: {task}")

        # Reset token tracking for this task
        self.token_tracker.reset_session()

        # Record start time
        start_time = time.time()

        try:
            # Execute the main task
            result = self.execute_task(task)

            # Add monitoring data
            result["monitoring"] = {
                "execution_time": time.time() - start_time,
                "token_usage": self.token_tracker.get_session_stats(),
                "vector_db_stats": self.vector_search_tool.get_repository_overview() if self.vector_search_tool.is_indexed else None
            }

            # Perform cleanup if requested
            if cleanup_after:
                cleanup_results = self.cleanup_test_files()
                result["cleanup"] = cleanup_results

            # Print summary
            self._print_execution_summary(result)

            return result

        except Exception as e:
            self.logger.error(f"Task execution failed: {e}")

            # Still provide monitoring data even on failure
            result = {
                "status": "failed",
                "error": str(e),
                "monitoring": {
                    "execution_time": time.time() - start_time,
                    "token_usage": self.token_tracker.get_session_stats(),
                    "vector_db_stats": self.vector_search_tool.get_repository_overview() if self.vector_search_tool.is_indexed else None
                }
            }

            if cleanup_after:
                cleanup_results = self.cleanup_test_files()
                result["cleanup"] = cleanup_results

            return result

    def cleanup_test_files(self, dry_run: bool = False) -> Dict[str, Any]:
        """Clean up test files and temporary artifacts.

        Args:
            dry_run: If True, only simulate cleanup

        Returns:
            Cleanup results
        """
        self.logger.info(f"🧹 {'Simulating' if dry_run else 'Starting'} test file cleanup...")

        try:
            # Scan for cleanup candidates
            candidates = self.cleanup_tool.scan_for_cleanup_candidates()

            # Perform cleanup (focusing on generated test files)
            cleanup_categories = ["generated_files", "temp_directories"]
            results = self.cleanup_tool.cleanup_files(
                candidates,
                categories=cleanup_categories,
                dry_run=dry_run
            )

            if not dry_run and results["total_freed"] > 0:
                self.logger.info(f"✅ Cleanup completed: Freed {results['total_freed']:,} bytes")

            return results

        except Exception as e:
            self.logger.error(f"Cleanup failed: {e}")
            return {"error": str(e), "total_freed": 0}

    def _print_execution_summary(self, result: Dict[str, Any]):
        """Print a comprehensive execution summary."""
        print("\n" + "="*70)
        print("📊 TASK EXECUTION SUMMARY")
        print("="*70)

        # Basic execution info
        status = result.get("status", "unknown")
        print(f"🎯 Status: {status}")

        if "monitoring" in result:
            monitoring = result["monitoring"]

            # Execution time
            exec_time = monitoring.get("execution_time", 0)
            print(f"⏱️  Execution time: {exec_time:.2f}s")

            # Token usage
            if "token_usage" in monitoring:
                token_stats = monitoring["token_usage"]
                print(f"\n🔢 Token Usage:")
                print(f"   📞 API calls: {token_stats.get('total_calls', 0)}")
                print(f"   🎯 Total tokens: {token_stats.get('total_tokens', 0):,}")
                print(f"   💰 Estimated cost: ${token_stats.get('total_cost', 0):.4f}")

            # Vector database stats
            if "vector_db_stats" in monitoring and monitoring["vector_db_stats"]:
                vdb_stats = monitoring["vector_db_stats"]
                print(f"\n🔍 Vector Database:")
                print(f"   📁 Files indexed: {vdb_stats.get('total_files', 0)}")
                print(f"   📊 Chunks: {vdb_stats.get('total_chunks', 0)}")
                print(f"   🔧 Semantic search: {'✅' if vdb_stats.get('capabilities', {}).get('semantic_search') else '❌'}")

        # File processing results
        if "completed_files" in result:
            files = result["completed_files"]
            print(f"\n📁 Files Processed: {len(files)}")
            for file_info in files[:5]:  # Show first 5
                status_icon = "✅" if file_info.get("status") == "completed" else "❌"
                print(f"   {status_icon} {file_info.get('path', 'unknown')}")

            if len(files) > 5:
                print(f"   ... and {len(files) - 5} more files")

        # Cleanup results
        if "cleanup" in result:
            cleanup = result["cleanup"]
            if cleanup.get("total_freed", 0) > 0:
                print(f"\n🧹 Cleanup:")
                print(f"   🗑️  Files deleted: {len(cleanup.get('deleted_files', []))}")
                print(f"   📂 Directories deleted: {len(cleanup.get('deleted_directories', []))}")
                print(f"   💾 Space freed: {cleanup.get('total_freed', 0):,} bytes")

        # Messages
        if "messages" in result:
            messages = result["messages"]
            if messages:
                print(f"\n📝 Key Messages:")
                for message in messages[-3:]:  # Show last 3 messages
                    print(f"   • {message}")

        print("="*70)

    def _create_graph(self):
        """Create the LangGraph workflow."""
        if not LANGGRAPH_AVAILABLE:
            raise ImportError("LangGraph is required for orchestrator functionality")

        workflow = StateGraph(OrchestratorState)

        # Add nodes for file-focused processing
        workflow.add_node("scan_and_plan", self._scan_and_plan_node)
        workflow.add_node("process_file", self._process_file_node)
        workflow.add_node("validate_integration", self._validate_integration_node)
        workflow.add_node("finalization", self._finalization_node)

        # Add edges
        workflow.add_edge("scan_and_plan", "process_file")

        # Conditional edges for file processing
        workflow.add_conditional_edges(
            "process_file",
            self._should_process_next_file,
            {
                "next_file": "process_file",
                "validate": "validate_integration"
            }
        )

        # Conditional edges for validation
        workflow.add_conditional_edges(
            "validate_integration",
            self._should_continue_or_end,
            {
                "continue": "process_file",
                "finalize": "finalization",
                "end": END
            }
        )

        workflow.add_edge("finalization", END)
        workflow.set_entry_point("scan_and_plan")

        return workflow.compile()

    def _scan_and_plan_node(self, state: OrchestratorState) -> dict:
        """Scan codebase and create file-by-file execution plan."""
        self.logger.info(f"Scan & Plan node: Analyzing task '{state['task']}'")

        try:
            # Analyze task with DDD framework
            ddd_analysis = self.ddd_tool.analyze_task(state["task"])

            # Find or create DDD execution plan
            execution_plan_info = self.execution_plan_tool.find_or_create_execution_plan(
                task=state["task"],
                context=ddd_analysis
            )

            # Run drift scanner to identify files needing changes
            scan_results = self._run_drift_scanner(state["task"], ddd_analysis)

            # Create file queue with priorities
            file_queue = []
            for file_path in scan_results.get("files_to_modify", []):
                file_context = self._analyze_file_context(file_path, state["task"], ddd_analysis)
                file_queue.append({
                    "path": file_path,
                    "priority": file_context["priority"],
                    "changes_needed": file_context["changes"],
                    "dependencies": file_context["dependencies"],
                    "context": file_context
                })

            # Sort by priority and dependencies
            file_queue = self._sort_files_by_priority(file_queue)

            execution_plan = {
                "total_files": len(file_queue),
                "estimated_complexity": scan_results.get("complexity", "medium"),
                "quality_gates": ddd_analysis["quality_requirements"],
                "file_processing_order": [f["path"] for f in file_queue],
                "use_swebench": self.enable_swebench and len(file_queue) > 0,
                "ddd_execution_plan": execution_plan_info  # Include DDD execution plan
            }

            return {
                "scan_results": scan_results,
                "execution_plan": execution_plan,
                "file_queue": file_queue,
                "completed_files": [],
                "task_type": ddd_analysis["primary_type"],
                "complexity": ddd_analysis["complexity"],
                "ddd_context": ddd_analysis["context"],
                "quality_requirements": ddd_analysis["quality_requirements"],
                "ddd_execution_plan_info": execution_plan_info,  # Store for later use
                "current_step": "process_file",
                "messages": [
                    f"📋 Scan completed. {len(file_queue)} files to process. "
                    f"Task type: {ddd_analysis['primary_type']}. "
                    f"DDD Plan: {execution_plan_info['plan_name']} ({execution_plan_info['status']})"
                ]
            }

        except Exception as e:
            self.logger.error(f"Scan and planning failed: {e}")
            return {
                "messages": [f"❌ Scan and planning failed: {str(e)}"],
                "current_step": "error"
            }

    def _process_file_node(self, state: OrchestratorState) -> dict:
        """Process individual file using SWE-bench agent."""
        file_queue = state.get("file_queue", [])
        completed_files = state.get("completed_files", [])

        if not file_queue:
            self.logger.info("No more files to process")
            return {
                "current_step": "validate",
                "messages": ["✅ All files processed"]
            }

        # Get next file to process
        current_file = file_queue[0]  # Don't pop yet, in case of failure
        file_path = current_file["path"]

        self.logger.info(f"Processing file: {file_path}")

        try:
            if self.enable_swebench:
                # Get DDD execution plan context for SWE-bench agent
                ddd_execution_plan_info = state.get("ddd_execution_plan_info", {})
                execution_context = self.execution_plan_tool.get_execution_context_for_swebench(
                    plan_info=ddd_execution_plan_info,
                    file_path=file_path
                )

                # Create file-specific instruction for SWE-bench agent
                file_instruction = self._create_file_instruction(
                    original_task=state["task"],
                    file_context=current_file,
                    global_context=state["execution_plan"],
                    execution_context=execution_context
                )

                # Update execution plan status
                self.execution_plan_tool.update_execution_plan_status(
                    plan_info=ddd_execution_plan_info,
                    checkpoint="implementation",
                    task=f"Process {file_path}",
                    status="in_progress"
                )

                # Execute SWE-bench agent on this specific file
                swebench_result = self.swebench_tool.process_file(
                    file_path=file_path,
                    instruction=file_instruction,
                    context={**current_file["context"], **execution_context}
                )

                # Update execution plan status on completion
                final_status = "completed" if swebench_result.get("status") == "completed" else "failed"
                self.execution_plan_tool.update_execution_plan_status(
                    plan_info=ddd_execution_plan_info,
                    checkpoint="implementation",
                    task=f"Process {file_path}",
                    status=final_status
                )
            else:
                # Use fallback processing
                swebench_result = self._process_file_fallback(current_file, state)

            # Record completion and remove from queue
            completed_file = {
                **current_file,
                "result": swebench_result,
                "status": swebench_result.get("status", "completed"),
                "changes_made": swebench_result.get("changes", [])
            }

            # Update state
            new_file_queue = file_queue[1:]  # Remove processed file
            new_completed_files = completed_files + [completed_file]

            return {
                "file_queue": new_file_queue,
                "completed_files": new_completed_files,
                "current_file": completed_file,
                "current_step": "process_file" if new_file_queue else "validate",
                "messages": [
                    f"✅ Processed {file_path}: {swebench_result.get('status', 'completed')} "
                    f"({len(new_completed_files)}/{len(new_completed_files) + len(new_file_queue)})"
                ]
            }

        except Exception as e:
            self.logger.error(f"File processing failed for {file_path}: {e}")
            return {
                "messages": [f"❌ Failed to process {file_path}: {str(e)}"],
                "current_step": "error"
            }

    def _validate_integration_node(self, state: OrchestratorState) -> dict:
        """Validate all file changes and ensure integration works."""
        completed_files = state.get("completed_files", [])
        execution_plan = state.get("execution_plan", {})

        self.logger.info(f"Validation & Integration node: Validating {len(completed_files)} files")

        try:
            # Run integration validation
            integration_result = self._validate_file_integration(completed_files)

            # Run DDD compliance checks
            ddd_compliance = self._validate_ddd_compliance(completed_files, execution_plan)

            # Run quality gates
            quality_result = self.quality_tool.validate_result(
                result={"completed_files": completed_files},
                requirements=execution_plan.get("quality_gates", []),
                context=state["ddd_context"]
            )

            validation_result = {
                "integration_passed": integration_result["passed"],
                "ddd_compliance_passed": ddd_compliance["passed"],
                "quality_gates_passed": quality_result["passed"],
                "overall_passed": all([
                    integration_result["passed"],
                    ddd_compliance["passed"],
                    quality_result["passed"]
                ]),
                "issues": (
                    integration_result.get("issues", []) +
                    ddd_compliance.get("issues", []) +
                    quality_result.get("issues", [])
                ),
                "files_processed": len(completed_files),
                "summary": f"Processed {len(completed_files)} files",
                "can_retry": len(integration_result.get("issues", [])) == 0  # Only retry if no integration issues
            }

            return {
                "validation_result": validation_result,
                "current_step": "decision",
                "messages": [
                    f"🔍 Validation: {'PASSED' if validation_result['overall_passed'] else 'FAILED'} "
                    f"({len(completed_files)} files processed)"
                ]
            }

        except Exception as e:
            self.logger.error(f"Integration validation failed: {e}")
            return {
                "validation_result": {
                    "overall_passed": False,
                    "error": str(e),
                    "can_retry": False
                },
                "messages": [f"❌ Integration validation failed: {str(e)}"],
                "current_step": "decision"
            }

    def _validate_file_integration(self, completed_files: list) -> dict:
        """Validate that all file changes work together."""
        # This would run integration tests, check for conflicts, etc.
        # For now, return a simple validation

        issues = []

        # Check for any failed file processing
        failed_files = [f for f in completed_files if f.get("status") == "failed"]
        if failed_files:
            issues.extend([f"Failed to process {f['path']}" for f in failed_files])

        # Check for files that modified other files unexpectedly
        for file_info in completed_files:
            other_files = file_info.get("other_files_modified", [])
            if other_files:
                issues.append(f"{file_info['path']} unexpectedly modified: {', '.join(other_files)}")

        return {
            "passed": len(issues) == 0,
            "issues": issues,
            "summary": f"Integration validation {'passed' if len(issues) == 0 else 'failed'}"
        }

    def _validate_ddd_compliance(self, completed_files: list, execution_plan: dict) -> dict:
        """Validate DDD compliance across all files."""
        # This would check DDD-specific requirements
        # For now, return a simple validation

        issues = []

        # Check that all files were processed successfully
        successful_files = [f for f in completed_files if f.get("status") in ["completed", "completed_mock"]]
        if len(successful_files) != len(completed_files):
            issues.append("Not all files were processed successfully")

        # Check for DDD identifier usage (placeholder)
        files_with_identifiers = 0
        for file_info in completed_files:
            if file_info.get("validation", {}).get("ddd_compliant", False):
                files_with_identifiers += 1

        if files_with_identifiers == 0 and execution_plan.get("total_files", 0) > 0:
            issues.append("No DDD compliance indicators found in processed files")

        return {
            "passed": len(issues) == 0,
            "issues": issues,
            "summary": f"DDD compliance {'passed' if len(issues) == 0 else 'failed'}"
        }

    def _validation_node(self, state: OrchestratorState) -> dict:
        """Validation node: Validate results against DDD standards."""
        self.logger.info("Validation node: Checking DDD compliance and quality")

        try:
            execution_result = state["execution_result"]
            quality_requirements = state["quality_requirements"]

            # Run quality gates
            validation_result = self.quality_tool.validate_result(
                result=execution_result,
                requirements=quality_requirements,
                ddd_context=state["ddd_context"]
            )

            # Update iteration count
            iteration_count = state.get("iteration_count", 0) + 1

            return {
                "validation_result": validation_result,
                "iteration_count": iteration_count,
                "current_step": "decision",
                "messages": [
                    f"✅ Validation completed. Passed: {validation_result['passed']}, "
                    f"Issues: {len(validation_result.get('issues', []))}, "
                    f"Iteration: {iteration_count}"
                ]
            }

        except Exception as e:
            self.logger.error(f"Validation failed: {e}")
            return {
                "validation_result": {"passed": False, "error": str(e)},
                "messages": [f"❌ Validation failed: {str(e)}"],
                "current_step": "decision"
            }

    def _finalization_node(self, state: OrchestratorState) -> dict:
        """Finalization node: Prepare final results and cleanup."""
        self.logger.info("Finalization node: Preparing final results")

        try:
            # Prepare final summary
            summary = {
                "task": state["task"],
                "task_type": state["task_type"],
                "complexity": state["complexity"],
                "iterations": state.get("iteration_count", 0),
                "final_status": state["validation_result"]["passed"],
                "execution_result": state["execution_result"],
                "validation_result": state["validation_result"],
                "timestamp": datetime.now().isoformat()
            }

            return {
                "execution_result": {
                    **state["execution_result"],
                    "final_summary": summary
                },
                "messages": [
                    f"🎉 Task completed successfully! "
                    f"Iterations: {summary['iterations']}, "
                    f"Status: {'PASSED' if summary['final_status'] else 'FAILED'}"
                ]
            }

        except Exception as e:
            self.logger.error(f"Finalization failed: {e}")
            return {
                "messages": [f"❌ Finalization failed: {str(e)}"]
            }

    def _should_continue(self, state: OrchestratorState) -> Literal["continue", "finalize", "end"]:
        """Determine whether to continue, finalize, or end the workflow."""
        validation_result = state.get("validation_result", {})
        iteration_count = state.get("iteration_count", 0)
        max_iterations = state.get("max_iterations", self.max_iterations)

        # Check if validation passed
        if validation_result.get("passed", False):
            return "finalize"

        # Check if we've hit max iterations
        if iteration_count >= max_iterations:
            self.logger.warning(f"Max iterations ({max_iterations}) reached")
            return "end"

        # Check if there are critical errors
        if validation_result.get("critical_errors", False):
            self.logger.error("Critical errors detected, ending workflow")
            return "end"

        # Continue with another iteration
        return "continue"

    def _execute_with_ddd_tools(self, state: OrchestratorState) -> dict:
        """Execute task using standard DDD tools."""
        # This is a placeholder for DDD tool execution
        # In a real implementation, this would use Agent3D's existing tools

        task = state["task"]
        plan = state["plan"]

        result = {
            "agent_used": "ddd_tools",
            "status": "completed",
            "changes": [],
            "documentation_updates": [],
            "summary": f"Executed task '{task}' using DDD tools"
        }

        return result

    def _should_process_next_file(self, state: OrchestratorState) -> Literal["next_file", "validate"]:
        """Determine if there are more files to process."""
        file_queue = state.get("file_queue", [])
        return "next_file" if file_queue else "validate"

    def _should_continue_or_end(self, state: OrchestratorState) -> Literal["continue", "finalize", "end"]:
        """Determine whether to continue, finalize, or end the workflow."""
        validation_result = state.get("validation_result", {})
        iteration_count = state.get("iteration_count", 0)
        max_iterations = state.get("max_iterations", self.max_iterations)

        # Check if validation passed
        if validation_result.get("overall_passed", False):
            return "finalize"

        # Check if we've hit max iterations
        if iteration_count >= max_iterations:
            self.logger.warning(f"Max iterations ({max_iterations}) reached")
            return "end"

        # Check if there are critical errors
        if validation_result.get("critical_errors", False):
            self.logger.error("Critical errors detected, ending workflow")
            return "end"

        # Check if we can retry (some issues might be fixable)
        if validation_result.get("can_retry", True):
            return "continue"

        # End if no retry possible
        return "end"

    def _run_drift_scanner(self, task: str, ddd_analysis: dict) -> dict:
        """Run drift scanner to identify files needing changes using vector database."""
        self.logger.info(f"🔍 Running intelligent drift scanner for task: {task}")

        try:
            # Use vector database to find relevant files
            if self.vector_search_tool.is_indexed:
                relevant_files = self.vector_search_tool.find_relevant_files(task, max_files=15)

                if relevant_files:
                    # Extract file paths and sort by relevance
                    files_to_modify = [file_info["file_path"] for file_info in relevant_files]

                    # Log the intelligent discovery
                    self.logger.info(f"📊 Vector search found {len(files_to_modify)} relevant files:")
                    for i, file_info in enumerate(relevant_files[:5]):  # Show top 5
                        score = file_info["relevance_score"]
                        path = file_info["file_path"]
                        self.logger.info(f"  {i+1}. {path} (score: {score:.3f})")

                    return {
                        "files_to_modify": files_to_modify,
                        "complexity": ddd_analysis.get("complexity", "medium"),
                        "estimated_time": f"{len(files_to_modify) * 3} minutes",
                        "discovery_method": "vector_search",
                        "relevance_scores": {f["file_path"]: f["relevance_score"] for f in relevant_files}
                    }
                else:
                    self.logger.warning("⚠️ Vector search returned no relevant files")
            else:
                self.logger.warning("⚠️ Vector database not indexed, falling back to pattern matching")

        except Exception as e:
            self.logger.error(f"Vector search failed: {e}, falling back to pattern matching")

        # Fallback to pattern-based discovery
        return self._fallback_drift_scanner(task, ddd_analysis)

    def _fallback_drift_scanner(self, task: str, ddd_analysis: dict) -> dict:
        """Fallback drift scanner using pattern matching."""
        task_lower = task.lower()
        files_to_modify = []

        if "test" in task_lower:
            files_to_modify.extend(["test_module.py", "test_utils.py"])
        if "documentation" in task_lower or "doc" in task_lower:
            files_to_modify.extend(["README.md", "docs/API.md"])
        if "refactor" in task_lower:
            files_to_modify.extend(["main.py", "utils.py"])
        if "api" in task_lower:
            files_to_modify.extend(["api.py", "routes.py"])

        # Default files if no specific pattern matched
        if not files_to_modify:
            if ddd_analysis.get("primary_type") == "coding":
                files_to_modify = ["main.py"]
            else:
                files_to_modify = ["README.md"]

        return {
            "files_to_modify": files_to_modify,
            "complexity": ddd_analysis.get("complexity", "medium"),
            "estimated_time": f"{len(files_to_modify) * 5} minutes",
            "discovery_method": "pattern_matching"
        }

    def _analyze_file_context(self, file_path: str, task: str, ddd_analysis: dict) -> dict:
        """Analyze context for a specific file using vector database insights."""
        file_ext = file_path.split('.')[-1] if '.' in file_path else ''

        # Get detailed file context from vector database
        vector_context = {}
        if self.vector_search_tool.is_indexed:
            try:
                vector_context = self.vector_search_tool.get_file_context(file_path)
                if "error" not in vector_context:
                    self.logger.debug(f"📊 Vector context for {file_path}: {vector_context.get('total_chunks', 0)} chunks")
            except Exception as e:
                self.logger.warning(f"Failed to get vector context for {file_path}: {e}")

        # Determine file type (prefer vector database info)
        if vector_context and "language" in vector_context:
            file_type = vector_context["language"]
        else:
            file_type = "unknown"
            if file_ext in ["py"]:
                file_type = "python"
            elif file_ext in ["md", "rst"]:
                file_type = "markdown"
            elif file_ext in ["yml", "yaml"]:
                file_type = "yaml"
            elif file_ext in ["js", "ts"]:
                file_type = "javascript"

        # Determine priority based on file type and task
        priority = "medium"
        if "test" in file_path.lower():
            priority = "high" if "test" in task.lower() else "low"
        elif file_path.lower() in ["readme.md", "main.py", "index.py"]:
            priority = "high"

        # Determine changes needed
        changes_needed = []
        if ddd_analysis.get("primary_type") == "coding":
            changes_needed.append("Code implementation")
        if "documentation" in ddd_analysis.get("task_types", []):
            changes_needed.append("Documentation updates")
        if "testing" in ddd_analysis.get("task_types", []):
            changes_needed.append("Test cases")

        return {
            "type": file_type,
            "priority": priority,
            "changes": changes_needed or ["General updates"],
            "dependencies": [],  # Could be enhanced to detect actual dependencies
            "estimated_complexity": ddd_analysis.get("complexity", "medium")
        }

    def _sort_files_by_priority(self, file_queue: list) -> list:
        """Sort files by priority and dependencies."""
        priority_order = {"high": 0, "medium": 1, "low": 2}

        # Sort by priority, then by filename for consistency
        sorted_files = sorted(
            file_queue,
            key=lambda f: (
                priority_order.get(f.get("priority", "medium"), 1),
                f.get("path", "")
            )
        )

        return sorted_files

    def _create_file_instruction(self, original_task: str, file_context: dict, global_context: dict, execution_context: dict = None) -> str:
        """Create file-specific instruction for SWE-bench agent."""
        file_path = file_context["path"]
        changes_needed = ", ".join(file_context.get("changes_needed", []))
        priority = file_context.get("priority", "medium")

        # Extract execution plan information
        exec_plan = execution_context.get("execution_plan", {}) if execution_context else {}
        ddd_compliance = execution_context.get("ddd_compliance", {}) if execution_context else {}

        instruction = f"""
FOCUSED FILE MODIFICATION TASK

Target File: {file_path}
Priority: {priority}
Original Task: {original_task}

File-Specific Requirements:
- Changes Needed: {changes_needed}
- File Type: {file_context.get('context', {}).get('type', 'unknown')}
- Dependencies: {', '.join(file_context.get('dependencies', []))}

Global Context:
- Total Files: {global_context.get('total_files', 1)}
- Complexity: {global_context.get('estimated_complexity', 'medium')}
- Quality Gates: {', '.join(global_context.get('quality_gates', []))}

DDD EXECUTION PLAN CONTEXT:
- Plan Title: {exec_plan.get('title', 'Implementation Plan')}
- Plan Scope: {exec_plan.get('scope', 'File-focused implementation')}
- Success Criteria: {'; '.join(exec_plan.get('success_criteria', []))}
- Plan File: {exec_plan.get('plan_file', 'N/A')}

DDD COMPLIANCE REQUIREMENTS:
- Documentation Sync Required: {ddd_compliance.get('documentation_sync', True)}
- Test Coverage Required: {ddd_compliance.get('test_coverage', True)}
- Quality Gates: {', '.join(ddd_compliance.get('quality_gates', []))}

IMPORTANT CONSTRAINTS FOR AGENT3D INTEGRATION:
1. ONLY modify the specified file: {file_path}
2. Do NOT modify other files unless absolutely necessary
3. Maintain existing file structure and patterns
4. Follow DDD principles for any documentation updates
5. Ensure changes are atomic and focused
6. Use proper Agent3D identifier patterns (TC-, FT-, etc.) if applicable
7. Update inline documentation if code changes affect it
8. FOLLOW THE DDD EXECUTION PLAN REQUIREMENTS ABOVE

QUALITY REQUIREMENTS:
- Maintain code quality and style consistency
- Add appropriate comments for complex changes
- Ensure backward compatibility where possible
- Follow existing naming conventions
- Meet all success criteria from the execution plan
- Ensure DDD compliance as specified

If you need to modify other files, explain why and ask for confirmation.

Focus on making precise, targeted changes to {file_path} only while following the DDD execution plan.
"""
        return instruction

    def _process_file_fallback(self, file_info: dict, state: OrchestratorState) -> dict:
        """Fallback file processing when SWE-bench agent is not available."""
        file_path = file_info["path"]

        return {
            "file_path": file_path,
            "status": "completed_fallback",
            "agent_used": "fallback_agent",
            "changes": [f"Fallback processing of {file_path}"],
            "summary": f"Fallback processing completed for {file_path}",
            "task": state["task"]
        }

    def execute_task(self, task: str, context: dict = None) -> dict:
        """Execute a task using the orchestrator workflow.

        Args:
            task: The task to execute
            context: Optional context information

        Returns:
            Execution result dictionary
        """
        if not LANGGRAPH_AVAILABLE:
            return self._fallback_execution(task, context)

        # Initialize state for file-focused processing
        initial_state = OrchestratorState(
            task=task,
            task_type="unknown",
            complexity="medium",
            scan_results={},
            execution_plan={},
            file_queue=[],
            completed_files=[],
            current_file={},
            validation_result={},
            messages=[],
            ddd_context=context or {},
            quality_requirements=[],
            current_step="scan_and_plan",
            iteration_count=0,
            max_iterations=self.max_iterations
        )

        try:
            # Execute the workflow
            final_state = self.graph.invoke(initial_state)
            return final_state

        except Exception as e:
            self.logger.error(f"Orchestrator execution failed: {e}")
            return {
                "error": str(e),
                "status": "failed",
                "messages": [f"❌ Orchestrator failed: {str(e)}"]
            }

    def _fallback_execution(self, task: str, context: dict = None) -> dict:
        """Fallback execution when LangGraph is not available."""
        self.logger.info("Using fallback execution mode")

        try:
            # Simple sequential execution
            ddd_analysis = self.ddd_tool.analyze_task(task)

            if ddd_analysis.get("requires_coding", False) and self.enable_swebench:
                result = self.swebench_tool.execute_task(task, context or {}, {})
            else:
                result = {"status": "completed", "agent_used": "fallback"}

            validation = self.quality_tool.validate_result(result, [], context or {})

            return {
                "execution_result": result,
                "validation_result": validation,
                "status": "completed_fallback",
                "messages": ["✅ Task completed using fallback mode"]
            }

        except Exception as e:
            return {
                "error": str(e),
                "status": "failed",
                "messages": [f"❌ Fallback execution failed: {str(e)}"]
            }


def create_orchestrator_graph(
    logger: logging.Logger = None,
    max_iterations: int = 5,
    enable_swebench: bool = True
) -> Agent3DOrchestratorGraph:
    """Create and return a configured orchestrator graph.

    Args:
        logger: Logger for orchestrator operations
        max_iterations: Maximum workflow iterations
        enable_swebench: Whether to enable SWE-bench agent

    Returns:
        Configured orchestrator graph
    """
    return Agent3DOrchestratorGraph(
        logger=logger,
        max_iterations=max_iterations,
        enable_swebench=enable_swebench
    )
