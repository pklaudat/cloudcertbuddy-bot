import os, json
import datetime
from pydantic import BaseModel
from dataclasses import dataclass
from azure.identity import DefaultAzureCredential
from agent_framework import Agent
from agent_framework.azure import AzureAIAgentClient
from agent_framework.openai import OpenAIResponsesClient
from config import AiServicesConfig


class CustomAgent(Agent):

    _client = None

    def __init__(
        self,
        name,
        description,
        prompt_file,
        model,
        tools=[],
        output_format: BaseModel | None = None,
    ):
        instructions = self._load_instructions(prompt_file, output_format)
        client = self.get_client(model)
        super().__init__(
            client=client,
            instructions=instructions,
            id=name,
            name=name,
            description=description,
            tools=tools,
        )

    def _load_instructions(
        self, prompt_file: str, output_format: BaseModel | None
    ) -> str:
        prompt_path = os.path.join(
            os.path.dirname(__file__), "prompts", "system", prompt_file
        )
        if not os.path.exists(prompt_path):
            raise FileNotFoundError(f"Prompt file '{prompt_path}' does not exist")

        with open(prompt_path, "r", encoding="utf-8") as file:
            prompt_content = file.read()

        if output_format:
            prompt_content += f"""
            Output your response as JSON:

            {json.dumps(output_format.model_json_schema(), indent=2)}
            """

        return prompt_content

    @classmethod
    def get_client(cls, model):
        if cls._client is None:
            match AiServicesConfig.MODEL_PROVIDER:
                case "OPENAI":
                    cls._client = OpenAIResponsesClient(
                        model_id=model,
                    )
                case "AZURE":
                    cls._client = AzureAIAgentClient(
                        credential=DefaultAzureCredential(),
                        project_endpoint=AiServicesConfig.AI_FOUNDRY_PROJECT_ENDPOINT,
                        model_deployment_name=model,
                    )

        return cls._client
