from typing import cast, Any
from agent_framework import (
    MCPStreamableHTTPTool,
    WorkflowBuilder,
    WorkflowExecutor,
    Message,
    Executor,
    AgentExecutor,
    Workflow,
)
from agent_framework.orchestrations import SequentialBuilder
from orchestration.agents import state
from orchestration.agents.core import CustomAgent
from orchestration.agents.dispatcher import Dispatcher
from orchestration.agents.student_readiness import StudentReadinessEval
from orchestration.agents.aggregator import Aggregator
from orchestration.agents import models


def certification_preparation_workflow():

    MAX_ITERATIONS = 200

    workflow_dispatcher = Dispatcher()

    human_validation = StudentReadinessEval()

    learn_path_curator = CustomAgent(
        name="learn-path-curator",
        description="Learn Path Curator for Microsoft Certification",
        tools=[
            MCPStreamableHTTPTool(
                name="Microsoft Learn MCP",
                url="https://learn.microsoft.com/api/mcp",
                approval_mode="never_require",
                request_timeout=30,
                description="Microsoft Learn official MCP server.",
            )
        ],
        output_format=state.LearningPath,
        prompt_file="learn_path_curator.md",
        model=models.LEARNING_PATH_CURATOR_AGENT,
    )

    study_plan_generator = CustomAgent(
        name="study-plan-generator",
        description="Study Plan Generator Agent",
        prompt_file="study_plan_generator.md",
        output_format=state.StudyPlan,
        model=models.STUDY_PLAN_GENERATOR_AGENT,
    )

    engagement_agent = CustomAgent(
        name="engagement-agent",
        description="Study Plan Engagement Agent",
        prompt_file="engagement_agent.md",
        model=models.ENGAGEMENT_AGENT_MODEL,
        output_format=state.WorkflowState,
    )

    readiness_assessment = CustomAgent(
        name="readiness-assessment",
        description="Study Plan readiness assessment agent",
        prompt_file="readiness_assessment.md",
        model=models.READINESS_ASSESSMENT_AGENT,
        output_format=state.WorkflowState,
    )

    aggregator = Aggregator()

    return (
        WorkflowBuilder(
            name="MicrosoftCertificationPreparationAssistant",
            max_iterations=MAX_ITERATIONS,
            start_executor=workflow_dispatcher,
        )
        .add_edge(workflow_dispatcher, learn_path_curator)
        .add_chain([learn_path_curator, study_plan_generator, engagement_agent])
        .add_edge(engagement_agent, human_validation)
        .add_edge(human_validation, readiness_assessment)
        .add_edge(readiness_assessment, aggregator)
        .add_edge(aggregator, human_validation)
        .add_edge(aggregator, workflow_dispatcher)
    ).build()


async def run(message: str):

    workflow = certification_preparation_workflow()

    events = await workflow.run(message, stream=True)
    outputs = events.get_outputs()
    if outputs:
        print("===== Final Conversation =====")
        messages: list[Message] | Any = outputs[0]
        for i, msg in enumerate(messages, start=1):
            name = msg.author_name or (
                "assistant" if msg.role == "assistant" else "user"
            )
            print(f"{'-' * 60}\n{i:02d} [{name}]\n{msg.text}")
