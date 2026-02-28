#!/usr/bin/env python3
import os
from microsoft_agents.hosting.core import AgentAuthConfiguration, AuthTypes


class TeamsBotConfig(AgentAuthConfiguration):
    """Teams Bot Default Configuration"""

    PORT = 3978

    PROJECT_ENDPOINT = os.getenv("AI_SERVICES_PROJECT_ENDPOINT")

    def __init__(self) -> None:
        self.AUTH_TYPE = AuthTypes.user_managed_identity
        self.TENANT_ID = os.getenv("MicrosoftAppTenantId", "")
        self.CLIENT_ID = os.getenv("MicrosoftAppId", "")


class AiServicesConfig:
    MODEL_PROVIDER = "OPENAI"
    MICROSOFT_LEARN_MCP_ENDPOINT = "https://learn.microsoft.com/api/mcp"
    MICROSOFT_LEARN_CATALOG_API_ENDPOINT = ""
    GOOGLE_CALENDAR_MCP_ENDPOINT = ""
    AI_FOUNDRY_PROJECT_ENDPOINT = os.getenv("AI_FOUNDRY_PROJECT_ENDPOINT", "")
    CONTENT_SAFETY_ENDPOINT = os.getenv("AI_SERVICES_ENDPOINT", "")


class AgentModelsConfig:
    DISPATCHER = "gpt-4o-mini"
    ENGAGEMENT_AGENT_MODEL = "gpt-4o-mini"
    LEARNING_PATH_CURATOR_AGENT = "gpt-4o-mini"
    READINESS_ASSESSMENT_AGENT = "gpt-4o-mini"
    STUDY_PLAN_GENERATOR_AGENT = "gpt-4o-mini"
