import os
from string import Template
from agent_framework import Executor, handler, WorkflowContext, ChatOptions, Message
from agent_framework.openai import OpenAIChatClient
from orchestration.agents.state import StudentInput
from orchestration.guardrails.content_satety import ContentSatefy
from orchestration.agents import models


class Dispatcher(Executor):

    def __init__(self, id="workflow-dispatcher"):
        self.guardrail = ContentSatefy()
        self.client = OpenAIChatClient(model_id=models.DISPATCHER)
        super().__init__(id)

    @handler
    async def handle(self, message: str, ctx: WorkflowContext[str]):
        # safe_message = await self.guardrail.is_safe(message)

        # if not safe_message.get("safe", True):
        #     await ctx.send_message(
        #         json.dumps(
        #             {
        #                 "blocked_categories": safe_message.get(
        #                     "blocked_categories", []
        #                 ),
        #                 "message": "This input has been filtered.",
        #             }
        #         )
        #     )

        student_input = await self.extract_student_input(message)

        prompt_path = os.path.join(
            os.path.dirname(__file__), "prompts", "user", "learn_path_curator.md"
        )
        if not os.path.exists(prompt_path):
            raise FileNotFoundError(f"Prompt file '{prompt_path}' does not exist")

        with open(prompt_path, "r", encoding="utf-8") as file:
            content = file.read()

        input_content = student_input.model_dump()

        prompt = Template(content).substitute(
            topics=",".join(input_content.get("topics", [])),
            experience_level=input_content.get("experience_level", "unknown"),
            certification=input_content.get("certification", "unknown"),
        )

        await ctx.send_message(prompt)

    async def extract_student_input(self, raw_message: str) -> StudentInput:
        message = Message("user", text=raw_message)

        llm_response = await self.client.get_response(
            messages=[message],
            options=ChatOptions(
                model_id=models.DISPATCHER,
                response_format=StudentInput,
                temperature=0.3,
                top_p=0.6,
            ),
        )

        if isinstance(llm_response.value, StudentInput):
            return llm_response.value
        else:
            return StudentInput(topics=[])
