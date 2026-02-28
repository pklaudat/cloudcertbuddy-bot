from typing import cast, Any
from agent_framework import (
    MCPStreamableHTTPTool,
    WorkflowRunState,
    WorkflowBuilder,
    Message,
)
from orchestration.agents.state import LearningPath, StudyPlan
from orchestration.agents.core import CustomAgent
from orchestration.agents.dispatcher import Dispatcher
from orchestration.agents.readiness_assessment import ReadinessAssessment
from orchestration.agents.human_validator import HumanValidator
from orchestration.agents import models


def certification_preparation_workflow():

    MAX_ITERATIONS = 3

    workflow_dispatcher = Dispatcher()

    readiness_assessment = ReadinessAssessment()

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
        output_format=LearningPath,
        prompt_file="learn_path_curator.md",
        model=models.LEARNING_PATH_CURATOR_AGENT,
    )

    study_plan_generator = CustomAgent(
        name="StudyPlanGenerator",
        description="Study Plan Generator Agent",
        prompt_file="study_plan_generator.md",
        output_format=StudyPlan,
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
        .add_edge(learn_path_curator, study_plan_generator)
        .add_edge(study_plan_generator, readiness_assessment)
        # .add_edge(learn_path_curator, study_plan_generator)
        # .add_edge(study_plan_generator, engagement_agent)
        # .add_edge()
        # .add_chain([learn_path_curator, study_plan_generator, engagement_agent])
    ).build()


async def run(message: str):

    workflow = certification_preparation_workflow()

    events = await workflow.run(message)
    outputs = events.get_outputs()
    if outputs:
        print("===== Final Conversation =====")
        messages: list[Message] | Any = outputs[0]
        for i, msg in enumerate(messages, start=1):
            name = msg.author_name or (
                "assistant" if msg.role == "assistant" else "user"
            )
            print(f"{'-' * 60}\n{i:02d} [{name}]\n{msg.text}")

    # outputs = events.get_outputs()
    # async for event in worfklow.run(message=message, stream=True):
    #     output_data = cast(list[Message], event.data)
    #     if isinstance(output_data, list):
    #         for item in output_data:
    #             if isinstance(item, Message) and item.text:
    #                 print(f"\n[Final Answer]: {item.text}")
