from typing import cast
from agent_framework import (
    MCPStreamableHTTPTool,
    WorkflowRunState,
    WorkflowBuilder,
    Message
)

from orchestration.agents.core import CustomAgent
from orchestration.agents.dispatcher import Dispatcher
from orchestration.agents.human_validator import HumanValidator
from orchestration.agents import models


def certification_preparation_workflow():

    MAX_ITERATIONS = 3

    workflow_dispatcher = Dispatcher()

    learn_path_curator = CustomAgent(
        name="LearnPathCurator",
        description="Learn Path Curator for Microsoft Certification",
        tools=[
            MCPStreamableHTTPTool(
                name="Microsoft Learn MCP",
                url="https://learn.microsoft.com/api/mcp",
                approval_mode="never_require",
                request_timeout=None,
                description="Microsoft Learn official MCP server.",
            )
        ],
        prompt_file="learn_path_curator.md",
        model=models.LEARNING_PATH_CURATOR_AGENT,
    )

    study_plan_generator = CustomAgent(
        name="StudyPlanGenerator",
        description="Study Plan Generator Agent",
        # tools=[
        #     MCPStreamableHTTPTool(
        #         name="Google Calendar API MCP",
        #         url="",
        #         approval_mode="always_require",
        #     )
        # ],
        prompt_file="study_plan_generator.md",
        model=models.STUDY_PLAN_GENERATOR_AGENT,
    )

    engagement_agent = CustomAgent(
        name="EngagementAgent",
        description="Study Plan Engagement Agent",
        prompt_file="engagement_agent.md",
        model=models.ENGAGEMENT_AGENT_MODEL,
    )


    return (
        WorkflowBuilder(
            name="MicrosoftCertificationPreparationAssistant",
            max_iterations=MAX_ITERATIONS,
            start_executor=workflow_dispatcher,
        )
        .add_edge(workflow_dispatcher, learn_path_curator)
        # .add_chain([learn_path_curator, study_plan_generator, engagement_agent])
    ).build()


async def run(message: str):

    worfklow = certification_preparation_workflow()
    async for event in worfklow.run(message=message, stream=True):
        output_data = cast(list[Message], event.data)
        if isinstance(output_data, list):
            for item in output_data:
                if isinstance(item, Message) and item.text:
                    print(f"\n[Final Answer]: {item.text}")
