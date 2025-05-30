"""
Token Usage Tracking for Claude API Calls

This module provides comprehensive token usage tracking for the orchestrator
to monitor and optimize Claude API usage.
"""

import time
import logging
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from pathlib import Path
import json


@dataclass
class APICall:
    """Represents a single API call with token usage."""
    timestamp: float
    operation: str  # e.g., "task_analysis", "file_modification", "quality_check"
    model: str
    input_tokens: int
    output_tokens: int
    total_tokens: int
    cost_estimate: float
    duration: float
    success: bool
    error_message: Optional[str] = None
    context: Dict[str, Any] = field(default_factory=dict)


class TokenTracker:
    """Tracks token usage across all Claude API calls."""
    
    def __init__(self, logger: logging.Logger = None):
        self.logger = logger or logging.getLogger(__name__)
        self.calls: List[APICall] = []
        self.session_start = time.time()
        
        # Token pricing (as of 2024 - update as needed)
        self.pricing = {
            "claude-3-5-sonnet-20241022": {
                "input": 0.003,   # per 1K tokens
                "output": 0.015   # per 1K tokens
            },
            "claude-3-sonnet-20240229": {
                "input": 0.003,
                "output": 0.015
            },
            "claude-3-haiku-20240307": {
                "input": 0.00025,
                "output": 0.00125
            }
        }
    
    def start_call(self, operation: str, model: str = "claude-3-5-sonnet-20241022", 
                   context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Start tracking a new API call.
        
        Args:
            operation: Description of the operation
            model: Claude model being used
            context: Additional context information
            
        Returns:
            Call tracking context
        """
        call_context = {
            "operation": operation,
            "model": model,
            "start_time": time.time(),
            "context": context or {}
        }
        
        self.logger.debug(f"🔄 Starting API call: {operation}")
        return call_context
    
    def end_call(self, call_context: Dict[str, Any], input_tokens: int, 
                 output_tokens: int, success: bool = True, 
                 error_message: str = None) -> APICall:
        """End tracking an API call and record usage.
        
        Args:
            call_context: Context from start_call
            input_tokens: Number of input tokens used
            output_tokens: Number of output tokens generated
            success: Whether the call was successful
            error_message: Error message if call failed
            
        Returns:
            APICall record
        """
        end_time = time.time()
        duration = end_time - call_context["start_time"]
        total_tokens = input_tokens + output_tokens
        
        # Calculate cost estimate
        model = call_context["model"]
        cost_estimate = self._calculate_cost(model, input_tokens, output_tokens)
        
        # Create API call record
        api_call = APICall(
            timestamp=call_context["start_time"],
            operation=call_context["operation"],
            model=model,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            total_tokens=total_tokens,
            cost_estimate=cost_estimate,
            duration=duration,
            success=success,
            error_message=error_message,
            context=call_context["context"]
        )
        
        self.calls.append(api_call)
        
        # Log the call
        status = "✅" if success else "❌"
        self.logger.info(
            f"{status} API call completed: {api_call.operation} "
            f"({input_tokens}+{output_tokens}={total_tokens} tokens, "
            f"${cost_estimate:.4f}, {duration:.2f}s)"
        )
        
        return api_call
    
    def _calculate_cost(self, model: str, input_tokens: int, output_tokens: int) -> float:
        """Calculate estimated cost for the API call."""
        if model not in self.pricing:
            # Default to Sonnet pricing if model not found
            model = "claude-3-5-sonnet-20241022"
        
        pricing = self.pricing[model]
        input_cost = (input_tokens / 1000) * pricing["input"]
        output_cost = (output_tokens / 1000) * pricing["output"]
        
        return input_cost + output_cost
    
    def get_session_stats(self) -> Dict[str, Any]:
        """Get statistics for the current session."""
        if not self.calls:
            return {
                "total_calls": 0,
                "total_tokens": 0,
                "total_cost": 0.0,
                "session_duration": time.time() - self.session_start
            }
        
        total_tokens = sum(call.total_tokens for call in self.calls)
        total_input_tokens = sum(call.input_tokens for call in self.calls)
        total_output_tokens = sum(call.output_tokens for call in self.calls)
        total_cost = sum(call.cost_estimate for call in self.calls)
        successful_calls = sum(1 for call in self.calls if call.success)
        
        # Group by operation
        operations = {}
        for call in self.calls:
            op = call.operation
            if op not in operations:
                operations[op] = {
                    "count": 0,
                    "tokens": 0,
                    "cost": 0.0,
                    "avg_duration": 0.0
                }
            operations[op]["count"] += 1
            operations[op]["tokens"] += call.total_tokens
            operations[op]["cost"] += call.cost_estimate
            operations[op]["avg_duration"] += call.duration
        
        # Calculate averages
        for op_stats in operations.values():
            if op_stats["count"] > 0:
                op_stats["avg_duration"] /= op_stats["count"]
        
        # Group by model
        models = {}
        for call in self.calls:
            model = call.model
            if model not in models:
                models[model] = {"count": 0, "tokens": 0, "cost": 0.0}
            models[model]["count"] += 1
            models[model]["tokens"] += call.total_tokens
            models[model]["cost"] += call.cost_estimate
        
        return {
            "total_calls": len(self.calls),
            "successful_calls": successful_calls,
            "failed_calls": len(self.calls) - successful_calls,
            "total_tokens": total_tokens,
            "input_tokens": total_input_tokens,
            "output_tokens": total_output_tokens,
            "total_cost": total_cost,
            "session_duration": time.time() - self.session_start,
            "operations": operations,
            "models": models,
            "avg_tokens_per_call": total_tokens / len(self.calls) if self.calls else 0,
            "avg_cost_per_call": total_cost / len(self.calls) if self.calls else 0
        }
    
    def get_recent_calls(self, limit: int = 10) -> List[APICall]:
        """Get the most recent API calls."""
        return self.calls[-limit:] if self.calls else []
    
    def export_session_data(self, file_path: str = None) -> str:
        """Export session data to JSON file.
        
        Args:
            file_path: Path to save the data (optional)
            
        Returns:
            Path to the exported file
        """
        if file_path is None:
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            file_path = f"token_usage_{timestamp}.json"
        
        # Prepare data for export
        export_data = {
            "session_info": {
                "start_time": self.session_start,
                "end_time": time.time(),
                "duration": time.time() - self.session_start
            },
            "statistics": self.get_session_stats(),
            "calls": [
                {
                    "timestamp": call.timestamp,
                    "operation": call.operation,
                    "model": call.model,
                    "input_tokens": call.input_tokens,
                    "output_tokens": call.output_tokens,
                    "total_tokens": call.total_tokens,
                    "cost_estimate": call.cost_estimate,
                    "duration": call.duration,
                    "success": call.success,
                    "error_message": call.error_message,
                    "context": call.context
                }
                for call in self.calls
            ]
        }
        
        # Save to file
        with open(file_path, 'w') as f:
            json.dump(export_data, f, indent=2)
        
        self.logger.info(f"📊 Token usage data exported to: {file_path}")
        return file_path
    
    def print_summary(self):
        """Print a formatted summary of token usage."""
        stats = self.get_session_stats()
        
        print("\n" + "="*60)
        print("🔢 TOKEN USAGE SUMMARY")
        print("="*60)
        
        print(f"📞 Total API Calls: {stats['total_calls']}")
        print(f"   ✅ Successful: {stats['successful_calls']}")
        print(f"   ❌ Failed: {stats['failed_calls']}")
        
        print(f"\n🎯 Token Usage:")
        print(f"   📥 Input tokens: {stats['input_tokens']:,}")
        print(f"   📤 Output tokens: {stats['output_tokens']:,}")
        print(f"   📊 Total tokens: {stats['total_tokens']:,}")
        print(f"   📈 Avg per call: {stats['avg_tokens_per_call']:.1f}")
        
        print(f"\n💰 Cost Estimates:")
        print(f"   💵 Total cost: ${stats['total_cost']:.4f}")
        print(f"   📈 Avg per call: ${stats['avg_cost_per_call']:.4f}")
        
        print(f"\n⏱️  Timing:")
        print(f"   🕐 Session duration: {stats['session_duration']:.1f}s")
        
        if stats['operations']:
            print(f"\n📋 Operations Breakdown:")
            for op, op_stats in stats['operations'].items():
                print(f"   • {op}: {op_stats['count']} calls, "
                      f"{op_stats['tokens']:,} tokens, "
                      f"${op_stats['cost']:.4f}")
        
        if stats['models']:
            print(f"\n🤖 Models Used:")
            for model, model_stats in stats['models'].items():
                print(f"   • {model}: {model_stats['count']} calls, "
                      f"{model_stats['tokens']:,} tokens, "
                      f"${model_stats['cost']:.4f}")
        
        print("="*60)
    
    def reset_session(self):
        """Reset the current session data."""
        self.calls.clear()
        self.session_start = time.time()
        self.logger.info("🔄 Token tracking session reset")
