from agent_framework import WorkflowContext, Executor, handler, AgentExecutorResponse


class ReadinessAssessment(Executor):

    def __init__(self, id: str = "readinessassessment"):
        super().__init__(id=id)

    @handler
    async def handle(
        self, text: AgentExecutorResponse, ctx: WorkflowContext[list[str]]
    ):
        print(f"executor id: {text.executor_id}")
        print(f"agent response: {text.agent_response}")

        await ctx.yield_output([text.agent_response])
