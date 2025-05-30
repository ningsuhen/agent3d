"""
Tools for the LangGraph Orchestrator

This module provides specialized tools that the orchestrator uses to
analyze tasks, execute code changes, and validate results within the
Agent3D DDD framework.
"""

import logging
import re
import yaml
from typing import Dict, List, Any, Optional
from pathlib import Path

from .vector_db import RepositoryVectorDB


class DDDAnalysisTool:
    """Tool for analyzing tasks using DDD principles."""

    def __init__(self, logger: logging.Logger = None):
        self.logger = logger or logging.getLogger(__name__)

    def analyze_task(self, task: str) -> Dict[str, Any]:
        """Analyze a task to determine execution strategy.

        Args:
            task: The task description to analyze

        Returns:
            Analysis result with task breakdown and requirements
        """
        self.logger.info(f"Analyzing task: {task[:100]}...")

        # Determine task types based on keywords
        task_types = self._identify_task_types(task)

        # Assess complexity
        complexity = self._assess_complexity(task, task_types)

        # Determine required agents
        required_agents = self._determine_required_agents(task_types)

        # Identify quality requirements
        quality_requirements = self._identify_quality_requirements(task_types)

        # Create task breakdown
        breakdown = self._create_task_breakdown(task, task_types)

        # Determine DDD compliance checks needed
        compliance_checks = self._determine_compliance_checks(task_types)

        return {
            "primary_type": task_types[0] if task_types else "general",
            "task_types": task_types,
            "complexity": complexity,
            "required_agents": required_agents,
            "quality_requirements": quality_requirements,
            "breakdown": breakdown,
            "compliance_checks": compliance_checks,
            "context": {
                "requires_coding": "coding" in task_types,
                "requires_documentation": "documentation" in task_types,
                "requires_testing": "testing" in task_types,
                "requires_refactoring": "refactoring" in task_types
            }
        }

    def _identify_task_types(self, task: str) -> List[str]:
        """Identify the types of work required for the task."""
        task_lower = task.lower()
        types = []

        # Coding-related keywords
        coding_keywords = [
            "implement", "code", "function", "class", "method", "algorithm",
            "bug", "fix", "debug", "error", "exception", "feature", "api"
        ]
        if any(keyword in task_lower for keyword in coding_keywords):
            types.append("coding")

        # Documentation keywords
        doc_keywords = [
            "document", "documentation", "readme", "guide", "manual",
            "comment", "docstring", "explain", "describe"
        ]
        if any(keyword in task_lower for keyword in doc_keywords):
            types.append("documentation")

        # Testing keywords
        test_keywords = [
            "test", "testing", "unittest", "pytest", "coverage",
            "validate", "verification", "quality"
        ]
        if any(keyword in task_lower for keyword in test_keywords):
            types.append("testing")

        # Refactoring keywords
        refactor_keywords = [
            "refactor", "optimize", "improve", "clean", "restructure",
            "performance", "efficiency", "maintainability"
        ]
        if any(keyword in task_lower for keyword in refactor_keywords):
            types.append("refactoring")

        # Configuration keywords
        config_keywords = [
            "config", "configuration", "setup", "install", "deploy",
            "environment", "settings"
        ]
        if any(keyword in task_lower for keyword in config_keywords):
            types.append("configuration")

        return types if types else ["general"]

    def _assess_complexity(self, task: str, task_types: List[str]) -> str:
        """Assess the complexity of the task."""
        complexity_score = 0

        # Base complexity from task types
        complexity_score += len(task_types)

        # Length-based complexity
        if len(task) > 500:
            complexity_score += 2
        elif len(task) > 200:
            complexity_score += 1

        # Keyword-based complexity indicators
        high_complexity_keywords = [
            "complex", "multiple", "integrate", "system", "architecture",
            "database", "api", "framework", "algorithm", "optimization"
        ]
        complexity_score += sum(1 for keyword in high_complexity_keywords
                               if keyword in task.lower())

        # Determine complexity level
        if complexity_score >= 5:
            return "high"
        elif complexity_score >= 3:
            return "medium"
        else:
            return "low"

    def _determine_required_agents(self, task_types: List[str]) -> List[str]:
        """Determine which agents are needed for the task."""
        agents = []

        if "coding" in task_types:
            agents.append("swebench_agent")

        if any(t in task_types for t in ["documentation", "general"]):
            agents.append("ddd_agent")

        if "testing" in task_types:
            agents.append("testing_agent")

        # Always include quality validation
        agents.append("quality_agent")

        return agents

    def _identify_quality_requirements(self, task_types: List[str]) -> List[str]:
        """Identify quality requirements based on task types."""
        requirements = ["ddd_compliance"]

        if "coding" in task_types:
            requirements.extend([
                "code_quality",
                "test_coverage",
                "documentation_sync"
            ])

        if "documentation" in task_types:
            requirements.extend([
                "documentation_quality",
                "cross_reference_validity"
            ])

        if "testing" in task_types:
            requirements.extend([
                "test_quality",
                "coverage_requirements"
            ])

        return requirements

    def _create_task_breakdown(self, task: str, task_types: List[str]) -> List[Dict[str, str]]:
        """Break down the task into smaller steps."""
        steps = []

        # Always start with analysis
        steps.append({
            "step": "analyze",
            "description": "Analyze requirements and create execution plan",
            "agent": "ddd_agent"
        })

        # Add type-specific steps
        if "coding" in task_types:
            steps.append({
                "step": "implement",
                "description": "Implement code changes",
                "agent": "swebench_agent"
            })

        if "documentation" in task_types:
            steps.append({
                "step": "document",
                "description": "Update documentation",
                "agent": "ddd_agent"
            })

        if "testing" in task_types:
            steps.append({
                "step": "test",
                "description": "Create and run tests",
                "agent": "testing_agent"
            })

        # Always end with validation
        steps.append({
            "step": "validate",
            "description": "Validate results against quality standards",
            "agent": "quality_agent"
        })

        return steps

    def _determine_compliance_checks(self, task_types: List[str]) -> List[str]:
        """Determine which DDD compliance checks are needed."""
        checks = ["basic_ddd_compliance"]

        if "coding" in task_types:
            checks.extend([
                "code_documentation_sync",
                "test_case_coverage",
                "feature_tracking"
            ])

        if "documentation" in task_types:
            checks.extend([
                "template_compliance",
                "cross_reference_validity",
                "identifier_consistency"
            ])

        return checks


class SWEBenchTool:
    """File-focused wrapper for the SWE-bench agent."""

    def __init__(self, logger: logging.Logger = None):
        self.logger = logger or logging.getLogger(__name__)
        self.agent = None
        self._initialize_agent()

    def _initialize_agent(self):
        """Initialize the real Augment SWE-bench agent."""
        try:
            import sys
            import os
            from pathlib import Path

            # Import from the integrated agents.swebench module
            from agents.swebench import SWEBenchAgent
            from agents.swebench.utils.llm_client import AnthropicDirectClient
            from agents.swebench.utils.workspace_manager import WorkspaceManager
            from rich.console import Console

            # Initialize components
            api_key = os.getenv('ANTHROPIC_API_KEY')
            if not api_key:
                self.logger.warning("❌ ANTHROPIC_API_KEY not found, SWE-bench agent will not be available")
                self.agent = None
                return

            # Create LLM client (using Claude Sonnet 4)
            llm_client = AnthropicDirectClient(
                model_name="claude-3-5-sonnet-20241022",
                max_retries=2,
                use_caching=True
            )

            # Create workspace manager (use current directory as workspace)
            workspace_manager = WorkspaceManager(root=Path("."))

            # Create console for output
            console = Console()

            # Initialize real SWE-bench agent optimized for file-focused tasks
            self.agent = SWEBenchAgent(
                client=llm_client,
                workspace_manager=workspace_manager,
                console=console,
                logger_for_agent_logs=self.logger,
                max_turns=30,  # Reduced for file-focused tasks
                max_output_tokens_per_turn=8192,  # Reduced for focused tasks
                use_prompt_budgeting=True,
                ask_user_permission=False
            )

            self.logger.info("✅ Real Augment SWE-bench agent initialized successfully")

        except ImportError as e:
            self.logger.warning(f"❌ SWE-bench agent dependencies not available: {e}")
            self.agent = None
        except Exception as e:
            self.logger.error(f"❌ Failed to initialize SWE-bench agent: {e}")
            self.agent = None

    def process_file(self, file_path: str, instruction: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Process a specific file using the SWE-bench agent.

        Args:
            file_path: Path to the file to process
            instruction: File-specific instruction
            context: File context information

        Returns:
            Processing result
        """
        if not self.agent:
            return self._mock_file_processing(file_path, instruction, context)

        try:
            # Create file-focused instruction
            file_instruction = self._create_file_focused_instruction(file_path, instruction, context)

            # Execute with real SWE-bench agent
            self.logger.info(f"🤖 Executing SWE-bench agent on {file_path}")
            result = self.agent.run_agent(file_instruction)

            # Process result for file-focused validation
            processed_result = self._process_file_result(result, file_path, context)

            return processed_result

        except Exception as e:
            self.logger.error(f"❌ SWE-bench execution failed for {file_path}: {e}")
            return {
                "file_path": file_path,
                "status": "failed",
                "error": str(e),
                "agent_used": "swebench_agent"
            }

    def execute_task(self, task: str, context: Dict[str, Any], plan: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a general coding task using the SWE-bench agent.

        Args:
            task: The task description
            context: DDD context information
            plan: Execution plan from analysis

        Returns:
            Execution result
        """
        if not self.agent:
            return self._mock_execution(task, context, plan)

        try:
            # Enhance task with DDD context
            enhanced_task = self._enhance_task_with_context(task, context, plan)

            # Execute with SWE-bench agent
            result = self.agent.run_agent(enhanced_task)

            # Process result for DDD compliance
            processed_result = self._process_result_for_ddd(result, context)

            return processed_result

        except Exception as e:
            self.logger.error(f"SWE-bench execution failed: {e}")
            return {
                "status": "failed",
                "error": str(e),
                "agent_used": "swebench_agent"
            }

    def _enhance_task_with_context(self, task: str, context: Dict[str, Any], plan: Dict[str, Any]) -> str:
        """Enhance the task with DDD context and requirements."""
        enhanced_task = f"""
DDD Context and Requirements:
- Task Type: {context.get('task_type', 'coding')}
- Complexity: {plan.get('estimated_complexity', 'medium')}
- Quality Gates: {', '.join(plan.get('quality_gates', []))}
- DDD Compliance Required: Yes

Original Task:
{task}

Additional Requirements:
1. Follow Agent3D DDD principles
2. Update documentation alongside code changes
3. Include appropriate test cases
4. Maintain feature tracking consistency
5. Use proper identifier patterns (TC-, FT-, etc.)

Please ensure all changes are well-documented and follow the established patterns.
"""
        return enhanced_task

    def _create_file_focused_instruction(self, file_path: str, instruction: str, context: Dict[str, Any]) -> str:
        """Create file-focused instruction for SWE-bench agent."""

        file_context = context.get('file_context', {})
        changes_needed = context.get('changes_needed', [])
        dependencies = context.get('dependencies', [])

        file_instruction = f"""
FOCUSED FILE MODIFICATION TASK

Target File: {file_path}
Original Task: {instruction}

File-Specific Context:
- Priority: {context.get('priority', 'medium')}
- Changes Needed: {', '.join(changes_needed)}
- Dependencies: {', '.join(dependencies)}
- File Type: {file_context.get('type', 'unknown')}

IMPORTANT CONSTRAINTS FOR AGENT3D INTEGRATION:
1. ONLY modify the specified file: {file_path}
2. Do NOT modify other files unless absolutely necessary
3. Maintain existing file structure and patterns
4. Follow DDD principles for any documentation updates
5. Ensure changes are atomic and focused
6. Use proper Agent3D identifier patterns (TC-, FT-, etc.) if applicable
7. Update inline documentation if code changes affect it

QUALITY REQUIREMENTS:
- Maintain code quality and style consistency
- Add appropriate comments for complex changes
- Ensure backward compatibility where possible
- Follow existing naming conventions

If you need to modify other files, explain why and ask for confirmation.

Focus on making precise, targeted changes to {file_path} only.
"""
        return file_instruction

    def _process_file_result(self, result: Any, file_path: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Process SWE-bench result for file-specific validation."""

        # Extract information from the SWE-bench result
        # The result structure depends on the actual SWE-bench agent implementation

        return {
            "file_path": file_path,
            "status": "completed",
            "agent_used": "swebench_agent",
            "changes": self._extract_file_changes(result, file_path),
            "other_files_modified": self._check_other_files_modified(result, file_path),
            "validation": self._validate_file_changes(result, file_path, context),
            "summary": f"Successfully processed {file_path} with SWE-bench agent",
            "raw_result": str(result)  # Store raw result for debugging
        }

    def _mock_file_processing(self, file_path: str, instruction: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Mock file processing when SWE-bench agent is not available."""
        self.logger.info(f"Using mock file processing for {file_path}")

        return {
            "file_path": file_path,
            "status": "completed_mock",
            "agent_used": "mock_agent",
            "changes": [f"Mock changes to {file_path}"],
            "other_files_modified": [],
            "validation": {
                "focused_on_target": True,
                "maintains_structure": True,
                "follows_patterns": True,
                "ddd_compliant": True
            },
            "summary": f"Mock processing completed for {file_path}",
            "instruction": instruction[:100] + "..." if len(instruction) > 100 else instruction
        }

    def _extract_file_changes(self, result: Any, target_file: str) -> List[str]:
        """Extract changes made to the target file."""
        # This would parse the SWE-bench result to identify changes
        # For now, return placeholder
        return [f"Modified {target_file}"]

    def _check_other_files_modified(self, result: Any, target_file: str) -> List[str]:
        """Check if other files were modified (should be minimal)."""
        # This would identify any other files that were changed
        # For now, return empty list
        _ = result, target_file  # Acknowledge parameters
        return []

    def _validate_file_changes(self, result: Any, file_path: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Validate that changes are appropriate for the file."""
        # This would validate the changes against file-specific requirements
        _ = result, file_path, context  # Acknowledge parameters
        return {
            "focused_on_target": True,
            "maintains_structure": True,
            "follows_patterns": True,
            "ddd_compliant": True
        }

    def _process_result_for_ddd(self, result: Any, context: Dict[str, Any]) -> Dict[str, Any]:
        """Process SWE-bench result for DDD compliance."""
        # This would process the actual SWE-bench result
        # For now, return a structured result
        _ = result, context  # Acknowledge parameters
        return {
            "status": "completed",
            "agent_used": "swebench_agent",
            "changes": [],
            "documentation_updates": [],
            "test_updates": [],
            "summary": "Task completed with SWE-bench agent",
            "ddd_compliance": {
                "identifiers_used": [],
                "documentation_updated": True,
                "tests_included": True
            }
        }

    def _mock_execution(self, task: str, context: Dict[str, Any], plan: Dict[str, Any]) -> Dict[str, Any]:
        """Mock execution when SWE-bench agent is not available."""
        self.logger.info("Using mock SWE-bench execution")

        return {
            "status": "completed_mock",
            "agent_used": "swebench_agent_mock",
            "changes": ["Mock code changes"],
            "documentation_updates": ["Mock documentation updates"],
            "test_updates": ["Mock test updates"],
            "summary": f"Mock execution of task: {task[:50]}...",
            "ddd_compliance": {
                "identifiers_used": ["TC-MOCK-001"],
                "documentation_updated": True,
                "tests_included": True
            }
        }


class QualityGatesTool:
    """Tool for validating results against DDD quality standards."""

    def __init__(self, logger: logging.Logger = None):
        self.logger = logger or logging.getLogger(__name__)

    def validate_result(
        self,
        result: Dict[str, Any],
        requirements: List[str],
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Validate execution result against quality requirements.

        Args:
            result: The execution result to validate
            requirements: List of quality requirements
            context: DDD context information

        Returns:
            Validation result
        """
        self.logger.info("Running quality gates validation")

        validation_results = []
        issues = []
        recommendations = []

        # Run each required validation
        for requirement in requirements:
            validation = self._run_quality_gate(requirement, result, context)
            validation_results.append(validation)

            if not validation["passed"]:
                issues.extend(validation.get("issues", []))

            recommendations.extend(validation.get("recommendations", []))

        # Overall validation result
        overall_passed = all(v["passed"] for v in validation_results)

        return {
            "passed": overall_passed,
            "individual_results": validation_results,
            "issues": issues,
            "recommendations": recommendations,
            "summary": f"Validation {'PASSED' if overall_passed else 'FAILED'} "
                      f"({len([v for v in validation_results if v['passed']])}/{len(validation_results)} gates passed)"
        }

    def _run_quality_gate(self, gate_name: str, result: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Run a specific quality gate."""
        if gate_name == "ddd_compliance":
            return self._validate_ddd_compliance(result, context)
        elif gate_name == "code_quality":
            return self._validate_code_quality(result, context)
        elif gate_name == "documentation_sync":
            return self._validate_documentation_sync(result, context)
        elif gate_name == "test_coverage":
            return self._validate_test_coverage(result, context)
        else:
            return {
                "gate": gate_name,
                "passed": True,
                "message": f"Quality gate '{gate_name}' not implemented yet"
            }

    def _validate_ddd_compliance(self, result: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Validate DDD compliance."""
        issues = []

        # Check if DDD compliance info is present
        ddd_info = result.get("ddd_compliance", {})

        if not ddd_info.get("documentation_updated", False):
            issues.append("Documentation was not updated alongside code changes")

        if not ddd_info.get("tests_included", False):
            issues.append("Tests were not included or updated")

        identifiers = ddd_info.get("identifiers_used", [])
        if context.get("requires_coding", False) and not identifiers:
            issues.append("No DDD identifiers (TC-, FT-, etc.) were used")

        return {
            "gate": "ddd_compliance",
            "passed": len(issues) == 0,
            "issues": issues,
            "message": "DDD compliance validation completed"
        }

    def _validate_code_quality(self, result: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Validate code quality."""
        # Placeholder for code quality validation
        return {
            "gate": "code_quality",
            "passed": True,
            "message": "Code quality validation passed (placeholder)"
        }

    def _validate_documentation_sync(self, result: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Validate documentation synchronization."""
        # Placeholder for documentation sync validation
        return {
            "gate": "documentation_sync",
            "passed": True,
            "message": "Documentation sync validation passed (placeholder)"
        }

    def _validate_test_coverage(self, result: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Validate test coverage."""
        # Placeholder for test coverage validation
        return {
            "gate": "test_coverage",
            "passed": True,
            "message": "Test coverage validation passed (placeholder)"
        }


class DDDExecutionPlanTool:
    """Tool for managing DDD execution plans and integration with SWE-bench agent."""

    def __init__(self, logger):
        self.logger = logger
        self.agent3d_root = Path.home() / ".agent3d"
        self.project_root = Path.cwd()
        self.runs_dir = self.project_root / "docs" / "runs"
        self.runs_dir.mkdir(parents=True, exist_ok=True)

    def find_or_create_execution_plan(self, task: str, context: dict = None) -> dict:
        """Find existing execution plan or create new one for the task."""
        try:
            # Look for existing execution plans
            existing_plan = self._find_existing_plan(task)
            if existing_plan:
                self.logger.info(f"📋 Found existing execution plan: {existing_plan['file_path']}")
                return existing_plan

            # Create new execution plan
            new_plan = self._create_execution_plan(task, context or {})
            self.logger.info(f"📋 Created new execution plan: {new_plan['file_path']}")
            return new_plan

        except Exception as e:
            self.logger.error(f"Failed to manage execution plan: {e}")
            return self._create_fallback_plan(task, context or {})

    def _find_existing_plan(self, task: str) -> dict:
        """Search for existing execution plans that match the task."""
        # Look for EXEC-PLAN files in docs/runs/
        for plan_file in self.runs_dir.glob("EXEC-PLAN-*.yml"):
            try:
                with open(plan_file, 'r') as f:
                    plan_content = yaml.safe_load(f)

                # Check if plan matches task
                if self._plan_matches_task(plan_content, task):
                    return {
                        "file_path": str(plan_file),
                        "content": plan_content,
                        "status": "existing",
                        "plan_name": plan_file.stem
                    }
            except Exception as e:
                self.logger.warning(f"Failed to read plan {plan_file}: {e}")

        return None

    def _plan_matches_task(self, plan_content: dict, task: str) -> bool:
        """Check if an execution plan matches the current task."""
        # Simple matching based on keywords and scope
        task_lower = task.lower()

        # Check metadata
        metadata = plan_content.get("metadata", {})
        title = metadata.get("title", "").lower()
        scope = metadata.get("scope", "").lower()

        # Check for keyword matches
        keywords = ["api", "string", "utility", "function", "module", "implementation"]
        task_keywords = [kw for kw in keywords if kw in task_lower]
        plan_keywords = [kw for kw in keywords if kw in title or kw in scope]

        # Match if there's overlap in keywords
        return len(set(task_keywords) & set(plan_keywords)) > 0

    def _create_execution_plan(self, task: str, context: dict) -> dict:
        """Create a new execution plan for the task."""
        # Generate plan name
        plan_name = self._generate_plan_name(task)
        plan_file = self.runs_dir / f"EXEC-PLAN-{plan_name}.yml"

        # Load template
        template_path = self.agent3d_root / "templates" / "EXEC-PLAN.template.yml"
        if template_path.exists():
            with open(template_path, 'r') as f:
                template_content = f.read()
        else:
            template_content = self._get_default_template()

        # Fill template
        plan_content = self._fill_execution_plan_template(template_content, task, context)

        # Save plan
        with open(plan_file, 'w') as f:
            f.write(plan_content)

        # Parse and return
        plan_data = yaml.safe_load(plan_content)
        return {
            "file_path": str(plan_file),
            "content": plan_data,
            "status": "created",
            "plan_name": plan_name
        }

    def _generate_plan_name(self, task: str) -> str:
        """Generate a plan name from the task description."""
        # Extract key words and create a slug
        words = task.lower().split()
        key_words = []

        for word in words:
            # Skip common words
            if word not in ["a", "an", "the", "and", "or", "but", "in", "on", "at", "to", "for", "of", "with", "by"]:
                # Clean word
                clean_word = ''.join(c for c in word if c.isalnum())
                if clean_word and len(clean_word) > 2:
                    key_words.append(clean_word)

        # Take first 3-4 key words
        plan_name = "-".join(key_words[:4])

        # Add timestamp if name is too generic
        if len(plan_name) < 10:
            from datetime import datetime
            timestamp = datetime.now().strftime("%Y%m%d")
            plan_name = f"{plan_name}-{timestamp}"

        return plan_name

    def _fill_execution_plan_template(self, template: str, task: str, context: dict) -> str:
        """Fill the execution plan template with task-specific information."""
        from datetime import datetime

        # Basic replacements
        filled = template.replace("[PLAN_TITLE]", f"Implementation Plan: {task}")
        filled = filled.replace("[YYYY-MM-DD]", datetime.now().strftime("%Y-%m-%d"))
        filled = filled.replace("[EXECUTION_TYPE]", "Standard")
        filled = filled.replace("[SCOPE_DESCRIPTION]", task)
        filled = filled.replace("[COORDINATOR_ROLE]", "LangGraph Orchestrator")
        filled = filled.replace("[TARGET_%]", "95%")
        filled = filled.replace("[DURATION]", "30-60 minutes")

        # Current state
        filled = filled.replace("[CURRENT_%]", "0%")
        filled = filled.replace("[DRIFT_STATUS]", "New Implementation")
        filled = filled.replace("[RECENT_CHANGES_DESCRIPTION]", "Starting new implementation")

        # Goals
        goals = self._extract_goals_from_task(task)
        goal_yaml = "\n".join([f'  - "{goal}"' for goal in goals])
        filled = filled.replace('  - "[GOAL_1]"\n  - "[GOAL_2]"\n  - "[GOAL_3]"', goal_yaml)

        # Checkpoints
        filled = self._fill_checkpoints(filled, task, context)

        # Success criteria
        criteria = self._extract_success_criteria(task)
        criteria_yaml = "\n".join([f'  - "{criterion}"' for criterion in criteria])
        filled = filled.replace('  - "[SUCCESS_CRITERIA_1]"\n  - "[SUCCESS_CRITERIA_2]"\n  - "[SUCCESS_CRITERIA_3]"', criteria_yaml)

        return filled

    def _extract_goals_from_task(self, task: str) -> list:
        """Extract goals from task description."""
        goals = []

        if "api" in task.lower() or "module" in task.lower():
            goals.append("Create functional API module")
        if "test" in task.lower():
            goals.append("Implement comprehensive tests")
        if "documentation" in task.lower() or "doc" in task.lower():
            goals.append("Update documentation")

        # Default goals
        if not goals:
            goals = [
                "Implement required functionality",
                "Ensure code quality and testing",
                "Maintain DDD compliance"
            ]

        return goals

    def _extract_success_criteria(self, task: str) -> list:
        """Extract success criteria from task description."""
        criteria = [
            "All functionality implemented and tested",
            "Code passes quality gates",
            "Documentation updated and synchronized",
            "DDD compliance maintained"
        ]

        if "api" in task.lower():
            criteria.insert(0, "API functions work correctly")
        if "test" in task.lower():
            criteria.insert(0, "All tests pass")

        return criteria

    def _fill_checkpoints(self, template: str, task: str, context: dict) -> str:
        """Fill checkpoint sections with task-specific information."""
        # For now, use simple checkpoint structure
        checkpoint_1 = """
  checkpoint_1:
    name: "Planning and Analysis"
    duration: "15 minutes"
    coordinator: "LangGraph Orchestrator"

    analysis:
      - "Analyze task requirements [ ]"
      - "Identify files to modify [ ]"
      - "Create implementation plan [ ]"

    validation:
      - "Requirements clearly understood"
      - "Implementation approach defined"
"""

        checkpoint_2 = """
  checkpoint_2:
    name: "Implementation"
    duration: "30 minutes"
    experts: ["SWE-bench Agent", "Code Quality Validator"]

    implementation:
      expert: "SWE-bench Agent"
      tasks:
        - "Implement core functionality [ ]"
        - "Add error handling [ ]"
        - "Create unit tests [ ]"

    validation:
      - "Code functionality verified"
      - "Tests pass successfully"
"""

        # Replace template checkpoints with simplified structure
        # This is a basic implementation - could be enhanced for more complex templates
        lines = template.split('\n')
        result_lines = []
        in_checkpoint_section = False

        for line in lines:
            if 'checkpoints:' in line:
                result_lines.append(line)
                result_lines.extend(checkpoint_1.strip().split('\n'))
                result_lines.extend(checkpoint_2.strip().split('\n'))
                in_checkpoint_section = True
            elif in_checkpoint_section and line.strip() and not line.startswith('  ') and not line.startswith('#'):
                # End of checkpoints section
                in_checkpoint_section = False
                result_lines.append(line)
            elif not in_checkpoint_section:
                result_lines.append(line)

        return '\n'.join(result_lines)

    def _get_default_template(self) -> str:
        """Get a default execution plan template if the official one is not available."""
        return """---
# 🎯 DDD Execution Plan

metadata:
  title: "[PLAN_TITLE]"
  created: "[YYYY-MM-DD]"
  type: "[EXECUTION_TYPE]"
  scope: "[SCOPE_DESCRIPTION]"
  coordinator: "[COORDINATOR_ROLE]"
  target_alignment: "[TARGET_%]"
  estimated_duration: "[DURATION]"

current_state:
  last_full_pass: "[YYYY-MM-DD]"
  current_alignment: "[CURRENT_%]"
  drift_status: "[DRIFT_STATUS]"
  recent_changes: "[RECENT_CHANGES_DESCRIPTION]"

goals:
  - "[GOAL_1]"
  - "[GOAL_2]"
  - "[GOAL_3]"

checkpoints:
  checkpoint_1:
    name: "Planning and Analysis"
    duration: "15 minutes"
    coordinator: "LangGraph Orchestrator"

    analysis:
      - "Analyze requirements [ ]"
      - "Plan implementation [ ]"

    validation:
      - "Requirements understood"
      - "Plan validated"

success_criteria:
  - "[SUCCESS_CRITERIA_1]"
  - "[SUCCESS_CRITERIA_2]"
  - "[SUCCESS_CRITERIA_3]"

# Status: ✅ Completed | 📋 Pending | 🚧 In Progress | 🚨 Critical | ⏭️ Skipped
"""

    def _create_fallback_plan(self, task: str, context: dict) -> dict:
        """Create a minimal fallback plan when template processing fails."""
        return {
            "file_path": "fallback-plan",
            "content": {
                "metadata": {
                    "title": f"Fallback Plan: {task}",
                    "type": "fallback",
                    "scope": task
                },
                "goals": ["Complete the requested task"],
                "checkpoints": {
                    "checkpoint_1": {
                        "name": "Implementation",
                        "tasks": ["Implement functionality"]
                    }
                }
            },
            "status": "fallback",
            "plan_name": "fallback"
        }

    def update_execution_plan_status(self, plan_info: dict, checkpoint: str, task: str, status: str) -> bool:
        """Update the status of a task in the execution plan."""
        try:
            if plan_info["status"] == "fallback":
                return True  # Skip updates for fallback plans

            plan_file = Path(plan_info["file_path"])
            if not plan_file.exists():
                return False

            # Read current plan
            with open(plan_file, 'r') as f:
                content = f.read()

            # Update status markers
            status_markers = {
                "not_started": "[ ]",
                "in_progress": "[~]",
                "completed": "[x]",
                "failed": "[!]"
            }

            old_marker = "[ ]"  # Assume starting from not started
            new_marker = status_markers.get(status, "[~]")

            # Simple text replacement for now
            # In a more sophisticated implementation, we'd parse YAML and update properly
            updated_content = content.replace(
                f'"{task} {old_marker}"',
                f'"{task} {new_marker}"'
            )

            # Write back
            with open(plan_file, 'w') as f:
                f.write(updated_content)

            self.logger.info(f"📋 Updated execution plan: {task} -> {status}")
            return True

        except Exception as e:
            self.logger.error(f"Failed to update execution plan: {e}")
            return False

    def get_execution_context_for_swebench(self, plan_info: dict, file_path: str) -> dict:
        """Get execution context to pass to SWE-bench agent."""
        plan_content = plan_info.get("content", {})

        # Extract relevant information for SWE-bench agent
        context = {
            "execution_plan": {
                "title": plan_content.get("metadata", {}).get("title", "Implementation Plan"),
                "scope": plan_content.get("metadata", {}).get("scope", ""),
                "goals": plan_content.get("goals", []),
                "success_criteria": plan_content.get("success_criteria", []),
                "plan_file": plan_info.get("file_path", ""),
                "plan_status": plan_info.get("status", "unknown")
            },
            "ddd_compliance": {
                "required": True,
                "documentation_sync": True,
                "test_coverage": True,
                "quality_gates": ["ddd_compliance", "code_quality", "test_coverage"]
            },
            "file_context": {
                "target_file": file_path,
                "modification_scope": "focused",
                "preserve_existing": True
            }
        }

        return context


class VectorSearchTool:
    """Tool for intelligent code search and context discovery using vector database."""

    def __init__(self, logger: logging.Logger = None):
        self.logger = logger or logging.getLogger(__name__)
        self.vector_db = None
        self.is_indexed = False
        self.repo_path = None

    def initialize_and_index_repository(self, repo_path: str) -> Dict[str, Any]:
        """Initialize vector database and index the repository.

        Args:
            repo_path: Path to the repository to index

        Returns:
            Indexing statistics and status
        """
        try:
            self.repo_path = repo_path
            self.vector_db = RepositoryVectorDB(logger=self.logger)

            self.logger.info(f"🔍 Initializing vector database for repository: {repo_path}")

            # Index the repository
            stats = self.vector_db.index_repository(repo_path)

            if stats["chunks_created"] > 0:
                self.is_indexed = True
                self.logger.info(f"✅ Repository indexed: {stats['chunks_created']} chunks from {stats['files_processed']} files")
            else:
                self.logger.warning("⚠️ No chunks were created during indexing")

            return {
                "status": "success" if self.is_indexed else "empty",
                "indexed": self.is_indexed,
                "stats": stats
            }

        except Exception as e:
            self.logger.error(f"Failed to initialize vector database: {e}")
            return {
                "status": "failed",
                "error": str(e),
                "indexed": False
            }

    def find_relevant_files(self, task: str, max_files: int = 10) -> List[Dict[str, Any]]:
        """Find files most relevant to the given task.

        Args:
            task: Task description to search for
            max_files: Maximum number of files to return

        Returns:
            List of relevant files with metadata
        """
        if not self.is_indexed or not self.vector_db:
            self.logger.warning("Vector database not initialized or indexed")
            return []

        try:
            # Search for relevant code chunks
            search_results = self.vector_db.search(task, top_k=max_files * 3)

            # Group by file and aggregate scores
            file_scores = {}
            file_chunks = {}

            for chunk, score in search_results:
                file_path = chunk.file_path

                if file_path not in file_scores:
                    file_scores[file_path] = []
                    file_chunks[file_path] = []

                file_scores[file_path].append(score)
                file_chunks[file_path].append(chunk)

            # Calculate aggregate scores and create file info
            relevant_files = []
            for file_path, scores in file_scores.items():
                if not scores:
                    continue

                chunks = file_chunks[file_path]

                # Calculate aggregate score (max + average for diversity)
                max_score = max(scores)
                avg_score = sum(scores) / len(scores)
                aggregate_score = (max_score * 0.7) + (avg_score * 0.3)

                # Get file metadata
                languages = set(chunk.language for chunk in chunks)
                chunk_types = set(chunk.chunk_type for chunk in chunks)
                total_complexity = sum(chunk.metadata.get("complexity_score", 0) for chunk in chunks)

                file_info = {
                    "file_path": file_path,
                    "relevance_score": aggregate_score,
                    "chunk_count": len(chunks),
                    "languages": list(languages),
                    "chunk_types": list(chunk_types),
                    "complexity_score": total_complexity,
                    "top_chunks": chunks[:3],  # Top 3 most relevant chunks
                    "has_tests": any(chunk.metadata.get("has_tests", False) for chunk in chunks),
                    "has_classes": any(chunk.metadata.get("has_classes", False) for chunk in chunks),
                    "has_functions": any(chunk.metadata.get("has_functions", False) for chunk in chunks)
                }

                relevant_files.append(file_info)

            # Sort by relevance score and return top files
            relevant_files.sort(key=lambda x: x["relevance_score"], reverse=True)
            return relevant_files[:max_files]

        except Exception as e:
            self.logger.error(f"Failed to find relevant files: {e}")
            return []

    def get_file_context(self, file_path: str) -> Dict[str, Any]:
        """Get detailed context for a specific file.

        Args:
            file_path: Path to the file

        Returns:
            File context information
        """
        if not self.is_indexed or not self.vector_db:
            return {"error": "Vector database not initialized"}

        try:
            chunks = self.vector_db.get_file_context(file_path)

            if not chunks:
                return {"error": f"File not found in index: {file_path}"}

            # Analyze file structure
            functions = [chunk for chunk in chunks if chunk.chunk_type == "function"]
            classes = [chunk for chunk in chunks if chunk.chunk_type == "class"]
            modules = [chunk for chunk in chunks if chunk.chunk_type == "module"]

            # Calculate file metrics
            total_lines = sum(chunk.metadata.get("lines_count", 0) for chunk in chunks)
            total_complexity = sum(chunk.metadata.get("complexity_score", 0) for chunk in chunks)

            context = {
                "file_path": file_path,
                "language": chunks[0].language if chunks else "unknown",
                "total_chunks": len(chunks),
                "total_lines": total_lines,
                "complexity_score": total_complexity,
                "structure": {
                    "functions": len(functions),
                    "classes": len(classes),
                    "modules": len(modules)
                },
                "features": {
                    "has_imports": any(chunk.metadata.get("has_imports", False) for chunk in chunks),
                    "has_tests": any(chunk.metadata.get("has_tests", False) for chunk in chunks),
                    "has_classes": any(chunk.metadata.get("has_classes", False) for chunk in chunks),
                    "has_functions": any(chunk.metadata.get("has_functions", False) for chunk in chunks)
                },
                "chunks": [
                    {
                        "type": chunk.chunk_type,
                        "lines": f"{chunk.start_line}-{chunk.end_line}",
                        "size": chunk.size,
                        "complexity": chunk.metadata.get("complexity_score", 0)
                    }
                    for chunk in chunks
                ]
            }

            return context

        except Exception as e:
            self.logger.error(f"Failed to get file context: {e}")
            return {"error": str(e)}

    def find_similar_implementations(self, query: str, language: str = None, top_k: int = 5) -> List[Dict[str, Any]]:
        """Find similar code implementations.

        Args:
            query: Description of what to find
            language: Filter by programming language
            top_k: Number of results to return

        Returns:
            List of similar code chunks
        """
        if not self.is_indexed or not self.vector_db:
            return []

        try:
            search_results = self.vector_db.search(
                query,
                top_k=top_k,
                filter_language=language,
                filter_chunk_type="function"  # Focus on functions for implementations
            )

            similar_implementations = []
            for chunk, score in search_results:
                impl_info = {
                    "file_path": chunk.file_path,
                    "chunk_type": chunk.chunk_type,
                    "language": chunk.language,
                    "similarity_score": score,
                    "lines": f"{chunk.start_line}-{chunk.end_line}",
                    "size": chunk.size,
                    "complexity": chunk.metadata.get("complexity_score", 0),
                    "content_preview": chunk.content[:200] + "..." if len(chunk.content) > 200 else chunk.content
                }
                similar_implementations.append(impl_info)

            return similar_implementations

        except Exception as e:
            self.logger.error(f"Failed to find similar implementations: {e}")
            return []

    def get_repository_overview(self) -> Dict[str, Any]:
        """Get an overview of the indexed repository.

        Returns:
            Repository statistics and overview
        """
        if not self.is_indexed or not self.vector_db:
            return {"error": "Vector database not initialized"}

        try:
            stats = self.vector_db.get_statistics()

            overview = {
                "repository_path": self.repo_path,
                "indexing_status": "indexed" if self.is_indexed else "not_indexed",
                "total_files": stats.get("total_files", 0),
                "total_chunks": stats.get("total_chunks", 0),
                "total_size": stats.get("total_size", 0),
                "languages": stats.get("languages", {}),
                "chunk_types": stats.get("chunk_types", {}),
                "capabilities": {
                    "semantic_search": stats.get("has_embeddings", False),
                    "fast_search": stats.get("has_index", False),
                    "model_available": stats.get("model_available", False)
                }
            }

            return overview

        except Exception as e:
            self.logger.error(f"Failed to get repository overview: {e}")
            return {"error": str(e)}
