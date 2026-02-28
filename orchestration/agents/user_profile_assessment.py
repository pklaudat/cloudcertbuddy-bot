from agent_framework import (
    Executor,
    WorkflowContext,
    handle
)


class UserProfileAssessment(Executor):

    @handle
    async def handle(self, request: str, ctx: WorkflowContext):
        pass