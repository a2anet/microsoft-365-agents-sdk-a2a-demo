import uuid
from datetime import datetime, timezone

from a2a.server.agent_execution.agent_executor import AgentExecutor
from a2a.server.agent_execution.context import RequestContext
from a2a.server.events.event_queue import EventQueue
from a2a.types import (
    Message,
    TaskState,
    TaskStatus,
    TaskStatusUpdateEvent,
    TextPart,
)


class EchoAgentExecutor(AgentExecutor):

    async def execute(
        self, context: RequestContext, event_queue: EventQueue
    ) -> None:
        user_text = context.get_user_input()
        task_id = context.task_id
        context_id = context.context_id

        agent_message = Message(
            role="agent",
            message_id=str(uuid.uuid4()),
            parts=[TextPart(text=f"[A2A Agent] {user_text}")],
            task_id=task_id,
            context_id=context_id,
        )

        final_update = TaskStatusUpdateEvent(
            task_id=task_id,
            context_id=context_id,
            status=TaskStatus(
                state=TaskState.completed,
                message=agent_message,
                timestamp=datetime.now(timezone.utc).isoformat(),
            ),
            final=True,
        )
        await event_queue.enqueue_event(final_update)

    async def cancel(
        self, context: RequestContext, event_queue: EventQueue
    ) -> None:
        status_update = TaskStatusUpdateEvent(
            task_id=context.task_id,
            context_id=context.context_id or str(uuid.uuid4()),
            status=TaskStatus(
                state=TaskState.canceled,
                timestamp=datetime.now(timezone.utc).isoformat(),
            ),
            final=True,
        )
        await event_queue.enqueue_event(status_update)
