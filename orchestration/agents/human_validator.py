from agent_framework import Executor, WorkflowContext, handler
from orchestration.agents.state import WorkflowState


class HumanValidator(Executor):

    def __init__(self, id="Human"):
        pass

    @handler
    async def handle(self, readiness_asssesment: WorkflowState, ctx: WorkflowContext):
        await ctx.request_info(readiness_asssesment, response_type=bool)
