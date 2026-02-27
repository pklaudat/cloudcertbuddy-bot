import os
from dataclasses import dataclass
from azure.identity import DefaultAzureCredential
from agent_framework_azure_ai import (
    AzureAIAgentClient,
)
from agent_framework import Agent
from config import AiServicesConfig


@dataclass
class StudentInput:
    topics_to_learn: list[str]
    target_certification: str
    days_until_exam: int


@dataclass
class LearningPath:
    title: str
    url: str
    estimated_hours: int
    modules: list[str]
    completed: bool


@dataclass
class CuratedLearningPath:
    paths: list[LearningPath]
    total_time: int


@dataclass
class StudyEvent:
    date: str
    target_modules: list[str]
    target_topics: list[str]
    completed_modules: list[str]
    completed_topics: list[str]


@dataclass
class StudyPlan:
    plan: list[StudyEvent]
    planned_time: int
    completed_time: int
    learning_path: CuratedLearningPath
    target_certification_date: str
    target_certification: str


class CustomAgent(Agent):

    _client = None

    def __init__(self, client, instructions, id, name, description, tools, prompt_file):
        instructions = self._load_instructions(prompt_file)
        client = self.get_client()
        super().__init__(
            client=client,
            instructions=instructions,
            id=id,
            name=name,
            description=description,
            tools=tools,
        )

    def _load_instructions(self, prompt_file: str) -> str:
        prompt_path = os.path.join(
            os.path.dirname(__file__), "..", "prompt", prompt_file
        )
        if not os.path.exists(prompt_path):
            raise FileNotFoundError(f"Prompt file '{prompt_file}' does not exist")

        with open(prompt_path, "r", encoding="utf-8") as file:
            return file.read()

    @classmethod
    def get_client(cls):
        if cls._client is None:
            cls._client = AzureAIAgentClient(
                credential=DefaultAzureCredential(),
                project_endpoint=AiServicesConfig.AI_FOUNDRY_PROJECT_ENDPOINT,
            )
        return cls._instance
