"""
Multi-Agent Orchestration Pattern
==================================

Demonstrates coordinating multiple specialized subagents using Claude Agent SDK.
This pattern is used in production for ADEV Dashboard managing 6 subagents.

Pattern Benefits:
- Separation of concerns (each agent has specific domain)
- Scalable (easily add new agents)
- Flexible routing (intelligent task distribution)

NOTE: This is a sanitized example showing the pattern, not production code.
"""

from anthropic import Anthropic
from typing import List, Dict, Any, Optional
import json


class SubAgent:
    """
    Base class for specialized subagents.

    Each subagent has:
    - name: Unique identifier
    - role: Description of responsibilities
    - tools: List of tool definitions for this agent
    """

    def __init__(
        self,
        name: str,
        role: str,
        tools: List[Dict[str, Any]],
        system_prompt: Optional[str] = None
    ):
        self.name = name
        self.role = role
        self.tools = tools
        self.system_prompt = system_prompt or f"You are a {role}."
        self.client = Anthropic()

    def execute(self, task: str, context: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Execute a task using this agent's specialized tools.

        Args:
            task: The task description
            context: Optional context from previous operations

        Returns:
            Dictionary with result and metadata
        """
        messages = [{"role": "user", "content": task}]

        if context:
            # Add context to system prompt
            context_str = json.dumps(context, indent=2)
            enhanced_prompt = f"{self.system_prompt}\n\nContext:\n{context_str}"
        else:
            enhanced_prompt = self.system_prompt

        try:
            response = self.client.messages.create(
                model="claude-sonnet-4",
                max_tokens=4096,
                system=enhanced_prompt,
                messages=messages,
                tools=self.tools
            )

            return {
                "success": True,
                "agent": self.name,
                "result": response.content,
                "usage": response.usage
            }

        except Exception as e:
            return {
                "success": False,
                "agent": self.name,
                "error": str(e)
            }


class AgentOrchestrator:
    """
    Coordinates multiple specialized agents.

    Responsibilities:
    - Route tasks to appropriate agent
    - Manage agent lifecycle
    - Aggregate results from multiple agents
    - Handle failures and retries
    """

    def __init__(self, subagents: List[SubAgent]):
        self.subagents = {agent.name: agent for agent in subagents}
        self.client = Anthropic()
        self.execution_history = []

    def route_task(self, task: str) -> str:
        """
        Determine which subagent should handle the task.

        Uses Claude to analyze the task and select the best agent.
        """
        agent_descriptions = "\n".join([
            f"- {name}: {agent.role}"
            for name, agent in self.subagents.items()
        ])

        routing_prompt = f"""
        Given the following task, which agent should handle it?

        Available agents:
        {agent_descriptions}

        Task: {task}

        Respond with ONLY the agent name, nothing else.
        """

        response = self.client.messages.create(
            model="claude-sonnet-4",
            max_tokens=50,
            messages=[{"role": "user", "content": routing_prompt}]
        )

        agent_name = response.content[0].text.strip()

        # Validate agent exists
        if agent_name not in self.subagents:
            # Fallback to first agent if routing fails
            agent_name = list(self.subagents.keys())[0]

        return agent_name

    def execute(
        self,
        task: str,
        preferred_agent: Optional[str] = None,
        context: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """
        Execute a task, routing to appropriate agent.

        Args:
            task: Task description
            preferred_agent: Override automatic routing
            context: Optional context for the agent

        Returns:
            Result dictionary with agent output and metadata
        """
        # Route to agent
        if preferred_agent and preferred_agent in self.subagents:
            agent_name = preferred_agent
        else:
            agent_name = self.route_task(task)

        # Execute with selected agent
        agent = self.subagents[agent_name]
        result = agent.execute(task, context)

        # Track execution
        self.execution_history.append({
            "task": task,
            "agent": agent_name,
            "success": result["success"],
            "timestamp": None  # Add timestamp in production
        })

        return result

    def execute_pipeline(self, tasks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Execute multiple tasks in sequence, passing context between them.

        Each task can reference results from previous tasks.

        Args:
            tasks: List of task dictionaries with 'description' and optional 'agent'

        Returns:
            List of results from each task
        """
        results = []
        context = {}

        for task_config in tasks:
            task = task_config["description"]
            preferred_agent = task_config.get("agent")

            # Execute with accumulated context
            result = self.execute(task, preferred_agent, context)
            results.append(result)

            # Update context for next task
            if result["success"]:
                context[f"task_{len(results)}"] = result["result"]

        return results


# ============================================
# Example Usage
# ============================================

def example_grant_research_system():
    """
    Example: Multi-agent system for grant research.

    This demonstrates the pattern used in EV_LV platform,
    but with generic grant research instead of specific tools.
    """

    # Define tool schemas (simplified examples)
    search_tools = [
        {
            "name": "search_grants",
            "description": "Search grant database by keywords and filters",
            "input_schema": {
                "type": "object",
                "properties": {
                    "keywords": {"type": "string"},
                    "category": {"type": "string"},
                    "amount_min": {"type": "number"}
                },
                "required": ["keywords"]
            }
        }
    ]

    eligibility_tools = [
        {
            "name": "check_eligibility",
            "description": "Check if a project qualifies for a grant",
            "input_schema": {
                "type": "object",
                "properties": {
                    "grant_id": {"type": "string"},
                    "project_type": {"type": "string"},
                    "location": {"type": "string"}
                },
                "required": ["grant_id", "project_type"]
            }
        }
    ]

    documentation_tools = [
        {
            "name": "generate_application",
            "description": "Generate grant application documents",
            "input_schema": {
                "type": "object",
                "properties": {
                    "grant_id": {"type": "string"},
                    "project_details": {"type": "object"}
                },
                "required": ["grant_id", "project_details"]
            }
        }
    ]

    # Create specialized agents
    grant_researcher = SubAgent(
        name="grant_researcher",
        role="Search and identify relevant grant opportunities",
        tools=search_tools,
        system_prompt="You are an expert at finding grant opportunities. Search databases and identify programs that match the user's needs."
    )

    eligibility_checker = SubAgent(
        name="eligibility_checker",
        role="Verify project eligibility for grants",
        tools=eligibility_tools,
        system_prompt="You are an expert at evaluating grant eligibility. Check requirements and determine if projects qualify."
    )

    documentation_writer = SubAgent(
        name="documentation_writer",
        role="Generate grant application documents",
        tools=documentation_tools,
        system_prompt="You are an expert grant writer. Create compelling applications that highlight project strengths."
    )

    # Create orchestrator
    orchestrator = AgentOrchestrator([
        grant_researcher,
        eligibility_checker,
        documentation_writer
    ])

    # Example 1: Single task routing
    print("Example 1: Single Task Routing")
    result = orchestrator.execute(
        "Find grants for EV charging station installation in Illinois"
    )
    print(f"Routed to: {result['agent']}")
    print(f"Success: {result['success']}\n")

    # Example 2: Pipeline execution
    print("Example 2: Multi-Step Pipeline")
    pipeline_tasks = [
        {
            "description": "Find renewable energy grants in the Midwest",
            "agent": "grant_researcher"
        },
        {
            "description": "Check eligibility for the top 3 grants found",
            "agent": "eligibility_checker"
        },
        {
            "description": "Generate application for the most suitable grant",
            "agent": "documentation_writer"
        }
    ]

    pipeline_results = orchestrator.execute_pipeline(pipeline_tasks)
    for i, result in enumerate(pipeline_results, 1):
        print(f"Step {i} - Agent: {result['agent']}, Success: {result['success']}")

    # Example 3: With context
    print("\nExample 3: Execution with Context")
    context = {
        "user_profile": {
            "organization": "Example Corp",
            "location": "Chicago, IL",
            "focus_area": "Clean Energy"
        }
    }
    result = orchestrator.execute(
        "Find grants we qualify for",
        context=context
    )
    print(f"Context-aware routing to: {result['agent']}")


if __name__ == "__main__":
    # NOTE: This requires ANTHROPIC_API_KEY environment variable
    # For demonstration purposes only
    print("Multi-Agent Orchestration Pattern Demo")
    print("=" * 50)
    print()

    # Uncomment to run (requires API key):
    # example_grant_research_system()

    print("Pattern demonstrated. See code for implementation details.")
