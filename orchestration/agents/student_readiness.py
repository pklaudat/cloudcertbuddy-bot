import json
import os
from string import Template
from agent_framework import (
    Executor,
    WorkflowContext,
    handler,
    response_handler,
    AgentResponse,
    AgentExecutorResponse,
    Message,
)
from agent_framework.orchestrations import AgentRequestInfoResponse
from orchestration.agents import state


class StudentReadinessEval(Executor):

    def __init__(self, id="student-readiness-eval"):
        super().__init__(id=id)

    @handler
    async def handle(self, study_plan: AgentExecutorResponse, ctx: WorkflowContext):
        study_plan_content = json.loads(study_plan.agent_response.text)

        if (
            study_plan_content.get("generated_study_plan", {}).get("total_hours") < 1
            or len(study_plan_content.get("generated_study_plan").get("sessions")) < 1
        ):
            await ctx.yield_output(
                "no study sessions found, moving to the beginning of chain to curate a learning path for the student again."
            )

        structured_input = state.StudyPlan(**study_plan_content.get("generated_study_plan", {}))

        prompt = "Are you ready to take the trainings?"
        prompt += (
            f"=> certification: {structured_input.target_exam}"
            if structured_input.target_exam
            else ""
        )
        prompt += f"=> Study Sessions:"
        prompt += "".join(
            [
                f"\n - {session.title} - duration: {session.duration_hours} h"
                for session in structured_input.sessions
                if session.title
            ]
        )

        await ctx.request_info(
            request_data=state.StudentReadinessCheck(
                prompt=prompt,
                current_state=state.WorkflowState(**study_plan_content)
            ),
            response_type=str,
        )

    @response_handler
    async def on_human_response(
        self, request: state.StudentReadinessCheck, response: str, ctx: WorkflowContext[str]
    ):
        message = f"""
        This is the current learning path: {request.current_state.model_dump_json()}
        
        This the student opnion about the learning path: {response}"""

        await ctx.send_message(message)

