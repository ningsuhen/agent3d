"""
LangGraph Orchestrator for Agent3D Framework

This module provides a LangGraph-based orchestrator that coordinates multiple
specialized agents, including the Augment SWE-bench agent, within the Agent3D
Documentation-Driven Development framework.

The orchestrator uses a state-based workflow to:
1. Plan tasks using DDD analysis
2. Execute tasks with appropriate specialized agents
3. Validate results against DDD quality standards
4. Ensure documentation and code remain synchronized
"""

from .langgraph_orchestrator import (
    Agent3DOrchestratorGraph,
    OrchestratorState,
    create_orchestrator_graph,
)
from .tools import (
    DDDAnalysisTool,
    SWEBenchTool,
    QualityGatesTool,
)

__all__ = [
    "Agent3DOrchestratorGraph",
    "OrchestratorState", 
    "create_orchestrator_graph",
    "DDDAnalysisTool",
    "SWEBenchTool",
    "QualityGatesTool",
]

# Version information
__version__ = "1.0.0"
__langgraph_version__ = "0.2.0"

# Orchestrator metadata
ORCHESTRATOR_METADATA = {
    "name": "agent3d_orchestrator",
    "description": "LangGraph-based orchestrator for Agent3D with SWE-bench integration",
    "version": __version__,
    "langgraph_version": __langgraph_version__,
    "capabilities": [
        "task_planning",
        "agent_coordination", 
        "quality_validation",
        "ddd_compliance",
        "multi_agent_workflows"
    ],
    "supported_agents": [
        "swebench_agent",
        "ddd_analysis_agent",
        "quality_gates_agent"
    ],
    "workflow_patterns": [
        "PLAN → EXECUTE → VALIDATE",
        "ANALYZE → CODE → TEST → DOCUMENT",
        "SCAN → DRAFT → REVIEW → SYNC"
    ],
    "requirements": [
        "langgraph>=0.2.0",
        "langchain>=0.3.0",
        "anthropic>=0.47.0"
    ]
}
