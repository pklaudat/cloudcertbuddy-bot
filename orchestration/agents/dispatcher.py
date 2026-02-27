import json
from agent_framework import (
    Executor,
    handler,
    WorkflowContext,
)
from orchestration.agents.core import StudentInput
from orchestration.guardrails.content_satety import ContentSatefy


class Dispatcher(Executor):

    def __init__(self, id="dispatcher"):
        self.guardrail = ContentSatefy()
        super().__init__(id)

    @handler
    async def process_input(self, message: str, ctx: WorkflowContext[str]):
        safe_message = await self.guardrail.is_safe(message)

        if not safe_message.get("safe", True):
            ctx.yield_output(json.dumps({
                "blocked_categories": safe_message.get("blocked_categories", []),
                "message": "This input has been filtered."
            }))

        

        