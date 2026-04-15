from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional


# CrewAI compatibility layer
try:
    from crewai import Agent as CrewAgent  # type: ignore
    from crewai import Crew as Crew
    from crewai import Task as CrewTask
    from crewai import Process as Process
    CREWAI_AVAILABLE = True
except Exception:
    CREWAI_AVAILABLE = False

    class CrewAgent:
        def __init__(self, role: str, goal: str, backstory: str = "", verbose: bool = False, **kwargs: Any) -> None:
            self.role = role
            self.goal = goal
            self.backstory = backstory
            self.verbose = verbose
            self.kwargs = kwargs

    class CrewTask:
        def __init__(
            self,
            description: str,
            agent: CrewAgent,
            expected_output: str = "",
            callback: Optional[Callable[..., Any]] = None,
            **kwargs: Any,
        ) -> None:
            self.description = description
            self.agent = agent
            self.expected_output = expected_output
            self.callback = callback
            self.kwargs = kwargs

    class Process:
        sequential = "sequential"

    class Crew:
        def __init__(self, agents: List[CrewAgent], tasks: List[CrewTask], process: str = "sequential", verbose: bool = False, **kwargs: Any) -> None:
            self.agents = agents
            self.tasks = tasks
            self.process = process
            self.verbose = verbose
            self.kwargs = kwargs

        def kickoff(self, inputs: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
            return {"status": "stubbed", "inputs": inputs or {}}


# AutoGen compatibility layer
try:
    from autogen import AssistantAgent, UserProxyAgent, GroupChat, GroupChatManager  # type: ignore
    AUTOGEN_AVAILABLE = True
except Exception:
    AUTOGEN_AVAILABLE = False

    class AssistantAgent:
        def __init__(self, name: str, system_message: str = "", llm_config: Optional[dict] = None, **kwargs: Any) -> None:
            self.name = name
            self.system_message = system_message
            self.llm_config = llm_config or {}
            self.kwargs = kwargs

    class UserProxyAgent:
        def __init__(self, name: str, human_input_mode: str = "NEVER", code_execution_config: Any = False, **kwargs: Any) -> None:
            self.name = name
            self.human_input_mode = human_input_mode
            self.code_execution_config = code_execution_config
            self.kwargs = kwargs

        def initiate_chat(self, manager: "GroupChatManager", message: str) -> Any:
            return type("ChatResult", (), {"summary": manager.run(message)})()

    class GroupChat:
        def __init__(self, agents: List[Any], messages: Optional[List[dict]] = None, max_round: int = 8, **kwargs: Any) -> None:
            self.agents = agents
            self.messages = messages or []
            self.max_round = max_round
            self.kwargs = kwargs

    class GroupChatManager:
        def __init__(self, groupchat: GroupChat, llm_config: Optional[dict] = None, **kwargs: Any) -> None:
            self.groupchat = groupchat
            self.llm_config = llm_config or {}
            self.kwargs = kwargs

        def run(self, message: str) -> str:
            names = [getattr(a, "name", getattr(a, "role", "agent")) for a in self.groupchat.agents]
            return (
                "Stubbed AutoGen discussion completed. "
                f"Participants: {', '.join(names)}. "
                "Recommendation synthesized from deterministic workflow outputs."
            )
