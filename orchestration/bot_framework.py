from os import environ
from dotenv import load_dotenv
from microsoft_agents.activity import Activity, ActivityTypes
from microsoft_agents.hosting.core import (
    AgentApplication,
    TurnState,
    TurnContext,
    MemoryStorage,
    AgentAuthConfiguration,
    AuthTypes,
)
from dotenv import load_dotenv
from microsoft_agents.hosting.core.connector import ConnectorClient
from microsoft_agents.hosting.fastapi import CloudAdapter
from microsoft_agents.authentication.msal import MsalConnectionManager, MsalAuth
from agent_framework import Message

from orchestration.agents.core import CustomAgent
from orchestration.agents import models



agent_config: dict[str, AgentAuthConfiguration] = {
    "SERVICE_CONNECTION": AgentAuthConfiguration(
        auth_type=AuthTypes.client_secret,
        client_id=CONNECTIONS__SERVICE_CONNECTION__SETTINGS__CLIENT,
        client_secret=CONNECTIONS__SERVICE_CONNECTION__SETTINGS__CLIENTSECRET,
        tenant_id=CONNECTIONS__SERVICE_CONNECTION__SETTINGS__TENANTID,
    )
}


AGENT_APP = AgentApplication[TurnState](
    storage=MemoryStorage(),
    adapter=CloudAdapter(
        connection_manager=MsalConnectionManager(
            connections_configurations=agent_config
        )
    ),
)


async def _help(context: TurnContext, _: TurnState):
    await context.send_activity(
        "Hi Sir, I'm Cloud Buddy Cert Bot your Microsoft Certification Preparation assistant on Teams 🚀. "
        "Type /help for help or send a message to see any feature in action."
    )


AGENT_APP.conversation_update("membersAdded")(_help)

AGENT_APP.message("/help")(_help)


@AGENT_APP.activity("message")
async def on_message(context: TurnContext, _):
    session = await context.send_activity(f"Processing your message ...")

    agent = CustomAgent(
        name="CloudCertBuddy",
        description="The cloud cert buddy agent",
        prompt_file="cloud_buddy_cert.md",
        model=models.CLOUD_CERT_BUDDY_AGENT,
        tools=[],
    )

    message = ""

    async for event in agent.run(
        messages=[Message("user", context.activity.text)], stream=True
    ):
        if event.contents:
            for content in event.contents:
                print(content)
                if hasattr(content, "text") and content.text != "" and content.text != None:
                    message += content.text

                    current_activity = Activity(
                        id=session.id, type=ActivityTypes.message, text=message
                    )
                    await context.update_activity(current_activity)
