#!/usr/bin/env python3
import os
from microsoft_agents.hosting.core import AuthTypes
from dotenv import load_dotenv

load_dotenv()


class TeamsBotConfig:
    """Teams Bot Default Configuration"""

    PORT = 3978

    AUTH_TYPE = AuthTypes.user_managed_identity
    TENANT_ID = os.getenv("CONNECTIONS__SERVICE_CONNECTION__SETTINGS__TENANTID")
    CLIENT_ID = os.getenv("CONNECTIONS__SERVICE_CONNECTION__SETTINGS__CLIENT")
    CLIENT_SECRET = os.getenv("CONNECTIONS__SERVICE_CONNECTION__SETTINGS__CLIENTSECRET")
    MICROSOFT_LEARN_OFFICIAL_CLIENT_ID = os.getenv("MicrosoftLearnOfficialClientId")


class AiServicesConfig:
    MODEL_PROVIDER = "OPENAI"
    MICROSOFT_LEARN_MCP_ENDPOINT = "https://learn.microsoft.com/api/mcp"
    MICROSOFT_LEARN_CATALOG_API_ENDPOINT = ""
    GOOGLE_CALENDAR_MCP_ENDPOINT = ""
    AI_FOUNDRY_PROJECT_ENDPOINT = os.getenv("AI_FOUNDRY_PROJECT_ENDPOINT", "")
    CONTENT_SAFETY_ENDPOINT = os.getenv("AI_SERVICES_ENDPOINT", "")
