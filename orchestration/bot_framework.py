from os import environ
from dotenv import load_dotenv
from microsoft_agents.hosting.core import (
    AgentApplication,
    TurnState,
    TurnContext,
    MemoryStorage,
)
from microsoft_agents.hosting.core import AgentAuthConfiguration, AuthTypes
from dotenv import load_dotenv
from microsoft_agents.hosting.core.connector import ConnectorClient
from microsoft_agents.hosting.fastapi import CloudAdapter
from microsoft_agents.authentication.msal import MsalConnectionManager, MsalAuth

load_dotenv()

agent_config: dict[str, AgentAuthConfiguration] = {
    "SERVICE_CONNECTION": {
        "auth_type": AuthTypes.client_secret,
        "client_id": environ.get("CONNECTIONS__SERVICE_CONNECTION__SETTINGS__CLIENTID"),
        "client_secret": environ.get(
            "CONNECTIONS__SERVICE_CONNECTION__SETTINGS__CLIENTSECRET"
        ),
        "tenant_id": environ.get("CONNECTIONS__SERVICE_CONNECTION__SETTINGS__TENANTID"),
    },
}

print(agent_config)
# print(agents_sdk_config)

AGENT_APP = AgentApplication[TurnState](
    storage=MemoryStorage(),
    adapter=CloudAdapter(
        connection_manager=MsalConnectionManager(
            connections_configurations=agent_config
        )
    ),
    # connection_manager=MsalConnectionManager(connections_configurations=agent_config)),
    # connection_manager=MsalConnectionManager(connections_configurations=agent_config))
)


async def _help(context: TurnContext, _: TurnState):
    await context.send_activity(
        "Hi Sir, I'm Skywalker your assistant on Teams 🚀. "
        "Type /help for help or send a message to see any feature in action."
    )


AGENT_APP.conversation_update("membersAdded")(_help)

AGENT_APP.message("/help")(_help)


@AGENT_APP.activity("message")
async def on_message(context: TurnContext, _):
    await context.send_activity(f"you said: {context.activity.text}")
