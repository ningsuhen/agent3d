"""
Augment SWE-bench Agent - Agent3D Integration

This module integrates the #1 open-source SWE-bench Verified agent (65.4% success rate)
into the Agent3D Documentation-Driven Development framework.

The SWE-bench agent is a specialized coding agent designed for complex software
engineering tasks including:
- Bug fixes in existing codebases
- Feature implementation with tests  
- Code refactoring and optimization
- Multi-step software engineering problems

Original repository: https://github.com/augmentcode/augment-swebench-agent
"""

from .agent import SWEBenchAgent

__all__ = ["SWEBenchAgent"]

# Version information
__version__ = "1.0.0"
__agent3d_integration__ = "1.0.0"

# Agent metadata for Agent3D framework
AGENT_METADATA = {
    "name": "swebench_agent",
    "description": "Specialized software engineering agent with 65.4% SWE-bench Verified success rate",
    "version": __version__,
    "agent3d_integration": __agent3d_integration__,
    "capabilities": [
        "complex_coding_tasks",
        "bug_fixes",
        "feature_implementation", 
        "code_refactoring",
        "test_writing",
        "multi_step_problem_solving"
    ],
    "tools": [
        "bash_tool",
        "str_replace_editor",
        "sequential_thinking",
        "complete_tool"
    ],
    "requirements": [
        "anthropic>=0.47.0",
        "rich>=13.9.4",
        "termcolor>=2.5.0",
        "jsonschema>=4.23.0"
    ],
    "docker_support": True,
    "max_turns": 200,
    "max_tokens_per_turn": 32768,
    "benchmark_performance": {
        "swebench_verified": 65.4,
        "rank": "#1 open-source"
    }
}
