import logging
import os

from a2a.client import ClientFactory, ClientConfig, create_text_message_object
from a2a.client.client import ClientEvent
from a2a.types import Message as A2AMessage
from a2a.utils import get_message_text

from microsoft_agents.hosting.aiohttp import CloudAdapter
from microsoft_agents.hosting.core import (
    AgentApplication,
    MemoryStorage,
    TurnContext,
    TurnState,
)

logger = logging.getLogger(__name__)

A2A_AGENT_URL = os.environ.get("A2A_AGENT_URL", "http://localhost:8000")

AGENT_APP = AgentApplication[TurnState](
    storage=MemoryStorage(), adapter=CloudAdapter()
)


async def _help(context: TurnContext, _: TurnState):
    await context.send_activity(
        "This bot bridges Microsoft Teams to an A2A agent.\n\n"
        "Send any message and it will be forwarded to the A2A agent, "
        "which will respond back through Teams.\n\n"
        "Type /help to see this message again."
    )


AGENT_APP.conversation_update("membersAdded")(_help)
AGENT_APP.message("/help")(_help)


@AGENT_APP.activity("message")
async def on_message(context: TurnContext, _: TurnState):
    user_text = context.activity.text
    if not user_text:
        await context.send_activity("Please send a text message.")
        return

    try:
        client = await ClientFactory.connect(
            agent=A2A_AGENT_URL,
            client_config=ClientConfig(streaming=False),
        )

        message = create_text_message_object(content=user_text)

        response_text = None
        async for event in client.send_message(message):
            if isinstance(event, A2AMessage):
                response_text = get_message_text(event)
            elif isinstance(event, tuple):
                task, _ = event
                if task.status and task.status.message:
                    response_text = get_message_text(task.status.message)

        if response_text:
            await context.send_activity(response_text)
        else:
            await context.send_activity("The A2A agent did not return a response.")

    except Exception:
        logger.exception("Failed to communicate with A2A agent")
        await context.send_activity(
            "Could not reach the A2A agent. Make sure it is running "
            f"at {A2A_AGENT_URL}."
        )
