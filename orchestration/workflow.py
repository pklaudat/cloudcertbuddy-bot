from orchestration.agents.core import CustomAgent
from agent_framework import (
    MCPStreamableHTTPTool,
    WorkflowRunState
)
from agent_framework.orchestrations import (
    MagenticBuilder,
    MagenticPlanReviewRequest
)


def build_agentic_workflow():

    microsoft_learn_agent = CustomAgent(
        name="MicrosoftLearnSpecialist",
        description="""This agent interact with Microsoft Learn MCP and
        provide user guidance across the microsoft knowledge base.
        """,
        tools=[
            MCPStreamableHTTPTool(
                name="Microsoft Learn MCP",
                url="https://learn.microsoft.com/api/mcp",
                approval_mode="never_require",
                request_timeout=None,
            )
        ],
        prompt_file="microsoft_learn.md",
    )

    google_calendar_agent = CustomAgent(
        name="GoogleCalendar",
        description="""
        """,
        tools=[
            MCPStreamableHTTPTool(
                name="Google Calendar API MCP",
                url="",
                approval_mode="always_require",
            )
        ],
        prompt_file="google_calendar.md"
    )

    agent_manager = CustomAgent(
        name="CloudBuddyCert",
        description="""This agent coordinate the other agent responses
        and provide clear guidance to the user

        """,
        prompt_file=""
    )

    return MagenticBuilder(
        participants=[microsoft_learn_agent, google_calendar_agent],
        agent_manager=agent_manager,
        enable_plan_review=True,
        intermediate_outputs=True,
        max_round_count=5,
        max_stall_count=2,
        max_reset_count=2
    ).build()



async def process_event_stream(message: str):

    worfklow = build_agentic_workflow()
    plan_review_request: MagenticPlanReviewRequest | None = None
    async for event in worfklow.run(message=message, stream=True):
        if event.type == "request_info" and event.request_type is MagenticPlanReviewRequest:
            plan_review_request = event.data
            print(f"Captured plan review request: {event.request_id}")

        if event.type == "status" and event.state is WorkflowRunState.IDLE_WITH_PENDING_REQUESTS:
            break

    
    if not plan_review_request:
        print("No plan review requested.")
        return 





