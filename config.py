#!/usr/bin/env python3
import os
from microsoft_agents.hosting.core import AgentAuthConfiguration, AuthTypes

""" Bot Configuration """


class DefaultConfig(AgentAuthConfiguration):
    """Teams Bot Default Configuration"""

    PORT = 3978

    PROJECT_ENDPOINT = os.getenv("AI_SERVICES_PROJECT_ENDPOINT")

    def __init__(self) -> None:
        self.AUTH_TYPE = AuthTypes.user_managed_identity
        self.TENANT_ID = os.getenv("MicrosoftAppTenantId", "")
        self.CLIENT_ID = os.getenv("MicrosoftAppId", "")


class McpConfig:

    MICROSOFT_LEARN_MCP_ENDPOINT = "https://learn.microsoft.com/api/mcp"
    MICROSOFT_LEARN_CATALOG_API_ENDPOINT = ""
    GOOGLE_CALENDAR_MCP_ENDPOINT = ""