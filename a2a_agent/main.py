import os

import uvicorn

from a2a.server.apps import A2AStarletteApplication
from a2a.server.request_handlers.default_request_handler import (
    DefaultRequestHandler,
)
from a2a.server.tasks.inmemory_task_store import InMemoryTaskStore
from a2a.types import AgentCapabilities, AgentCard, AgentSkill

from a2a_agent.agent import EchoAgentExecutor

JSONRPC_URL = "/a2a/jsonrpc"


def main() -> None:
    port = int(os.environ.get("A2A_PORT", "8000"))

    agent_card = AgentCard(
        name="Echo A2A Agent",
        description="A simple echo agent that demonstrates the A2A protocol bridge with Microsoft 365 Agents SDK.",
        url=f"http://localhost:{port}{JSONRPC_URL}",
        version="1.0.0",
        protocol_version="0.3.0",
        capabilities=AgentCapabilities(
            streaming=True,
            push_notifications=False,
            state_transition_history=False,
        ),
        default_input_modes=["text"],
        default_output_modes=["text"],
        preferred_transport="JSONRPC",
        additional_interfaces=[
            {
                "url": f"http://localhost:{port}{JSONRPC_URL}",
                "transport": "JSONRPC",
            },
        ],
        skills=[
            AgentSkill(
                id="echo",
                name="Echo",
                description="Echoes back the user's message.",
                tags=["echo"],
                examples=["Hello!", "How are you?"],
            ),
        ],
        supports_authenticated_extended_card=False,
    )

    request_handler = DefaultRequestHandler(
        agent_executor=EchoAgentExecutor(),
        task_store=InMemoryTaskStore(),
    )

    server = A2AStarletteApplication(
        agent_card=agent_card,
        http_handler=request_handler,
    )

    app = server.build(rpc_url=JSONRPC_URL)

    print(f"A2A Agent running on http://localhost:{port}")
    uvicorn.run(app, host="127.0.0.1", port=port)


if __name__ == "__main__":
    main()
