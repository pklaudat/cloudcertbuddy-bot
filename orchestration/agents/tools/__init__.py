from agent_framework import (
    Executor,
    WorkflowContext,
    tool
)
from msal import ConfidentialClientApplication


@tool(
    name="user_profile_assessment",
    description="""Fetch the Microsoft Learn user profile information
    such as the completed modules, the applied skills badges and the 
    certifications.
    """,
)
def user_profile_assessment(user_assertion: str):
    certifications = f"https://learn.microsoft.com/api/certification/dashboardsummary/?locale=en-us&learnAssessmentMerger=false"


# def acquire_obo_token(user_assertion, scopes: list[str] = ""):
#     app = msal.ConfidentialClientApplication(
#         CLIENT_ID,
#         authority=AUTHORITY,
#         client_credential=CLIENT_SECRET,
#     )

#     result = app.acquire_token_on_behalf_of(
#         user_assertion=user_assertion,
#         scopes=["https://graph.microsoft.com/.default"],
#     )

#     if "access_token" in result:
#         return result["access_token"]
#     else:
#         raise Exception(result)