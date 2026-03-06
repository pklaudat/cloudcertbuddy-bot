import json
from agent_framework import (
    Executor, 
    handler,
    response_handler,
    AgentExecutorResponse, 
    WorkflowContext
)


class Aggregator(Executor):
    def __init__(self, id="aggregator"):
        super().__init__(id=id)

    @handler
    async def handle(self, final_plan: AgentExecutorResponse, ctx: WorkflowContext):
        content = json.loads(final_plan.agent_response.text)

        readiness = content.get("readiness", {}).get("status", "pending").strip().lower()

        if readiness == "modify":
            await ctx.send_message(final_plan.agent_response.text, target_id="workflow-dispatcher")
        elif readiness == "pending":
            await ctx.send_message(final_plan.agent_response.text, target_id="student-readiness-eval")
        else:
            await ctx.yield_output(final_plan.agent_response.text)
        

    


