from agent_framework import Executor, WorkflowContext, tool
import msal
import httpx
from pydantic import BaseModel
from config import TeamsBotConfig


@tool(
    name="user_profile_assessment",
    description="""Fetch the Microsoft Learn user profile information
    such as the completed modules, the applied skills badges and the 
    certifications.
    """,
    max_invocations=3,
    approval_mode="always_require",
)
async def user_profile_assessment(token: str) -> list[dict]:

    print("Call user profile assessment tool...")

    token = await acquire_obo_token(
        token, [TeamsBotConfig.MICROSOFT_LEARN_OFFICIAL_CLIENT_ID]
    )

    certifications_url = f"https://learn.microsoft.com/api/certification/dashboardsummary/?locale=en-us&learnAssessmentMerger=false"

    async with httpx.AsyncClient() as client:
        response = client.get(
            url=certifications_url, headers={"authorization": f"Bearer {token}"}
        )

    print(response)
    print(dir(response))

    return response


async def acquire_obo_token(user_assertion: str, scopes: list[str] = []) -> str:
    app = msal.ConfidentialClientApplication(
        client_id=TeamsBotConfig.CLIENT_ID,
        client_credential=TeamsBotConfig.CLIENT_SECRET,
    )

    result = app.acquire_token_on_behalf_of(
        user_assertion=user_assertion, scopes=scopes
    )

    if "access_token" in result:
        return result["access_token"]
    else:
        raise Exception(result)
