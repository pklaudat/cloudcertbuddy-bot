from orchestration.agents.core import CustomAgent
from agent_framework import (
    MCPStreamableHTTPTool,
    Workflow
)


def run():

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

    cloudcertbuddy_agent = CustomAgent(
        name="CloudBuddyCert",
        description="""This agent coordinate the other agent responses
        and provide clear guidance to the user

        """,
        prompt_file=""
    )

    workflow = Workflow()
