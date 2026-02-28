import os
import datetime
from typing import Optional
from dataclasses import dataclass
from azure.identity import DefaultAzureCredential
from agent_framework import Agent
from agent_framework.azure import AzureAIAgentClient
from agent_framework.openai import OpenAIChatClient
from config import AiServicesConfig


class CustomAgent(Agent):

    _client = None

    def __init__(self, name, description, prompt_file, model, tools=[]):
        instructions = self._load_instructions(prompt_file)
        client = self.get_client(model)
        super().__init__(
            client=client,
            instructions=instructions,
            id=name,
            name=name,
            description=description,
            tools=tools,
        )

    def _load_instructions(self, prompt_file: str) -> str:
        prompt_path = os.path.join(os.path.dirname(__file__), "prompts",  "system", prompt_file)
        if not os.path.exists(prompt_path):
            raise FileNotFoundError(f"Prompt file '{prompt_path}' does not exist")

        with open(prompt_path, "r", encoding="utf-8") as file:
            return file.read()

    @classmethod
    def get_client(cls, model):
        if cls._client is None:
            match AiServicesConfig.MODEL_PROVIDER:
                case "OPENAI":
                    cls._client = OpenAIChatClient(
                        model_id=model,
                    )
                case "AZURE":
                    cls._client = AzureAIAgentClient(
                        credential=DefaultAzureCredential(),
                        project_endpoint=AiServicesConfig.AI_FOUNDRY_PROJECT_ENDPOINT,
                        model_deployment_name=model,
                    )

        return cls._client
