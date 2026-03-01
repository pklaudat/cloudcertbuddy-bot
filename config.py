#!/usr/bin/env python3
import os
from microsoft_agents.hosting.core import AgentAuthConfiguration, AuthTypes


class TeamsBotConfig:
    """Teams Bot Default Configuration"""

    PORT = 3978


    AUTH_TYPE = AuthTypes.user_managed_identity
    TENANT_ID = os.getenv("MicrosoftAppTenantId")
    CLIENT_ID = os.getenv("MicrosoftAppId")
    CLIENT_SECRET = os.getenv("MicrosoftAppSecret")


class AiServicesConfig:
    MODEL_PROVIDER = "OPENAI"
    MICROSOFT_LEARN_MCP_ENDPOINT = "https://learn.microsoft.com/api/mcp"
    MICROSOFT_LEARN_CATALOG_API_ENDPOINT = ""
    GOOGLE_CALENDAR_MCP_ENDPOINT = ""
    AI_FOUNDRY_PROJECT_ENDPOINT = os.getenv("AI_FOUNDRY_PROJECT_ENDPOINT", "")
    CONTENT_SAFETY_ENDPOINT = os.getenv("AI_SERVICES_ENDPOINT", "")

