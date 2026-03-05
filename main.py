from os import environ
import uvicorn
from fastapi import FastAPI, Request
from dotenv import load_dotenv
from microsoft_agents.hosting.fastapi import (
    start_agent_process,
    JwtAuthorizationMiddleware,
)
from agent_framework_devui import serve
from orchestration.bot_framework import AGENT_APP
from orchestration.workflow import certification_preparation_workflow

app = FastAPI(title="PK Bot", version="0.0.1")


@app.post("/api/messages")
async def entrypoint(req: Request):
    return await start_agent_process(
        request=req, agent_application=AGENT_APP, adapter=AGENT_APP.adapter
    )


@app.get("/api/health")
async def health_check():
    return {"status": "OK"}


if __name__ == "__main__":
    try:
        wf = certification_preparation_workflow()
        serve(entities=[wf], instrumentation_enabled=True)
        # uvicorn.run(app, host="0.0.0.0", port=environ.get("PORT", 3978))
    except Exception as error:
        raise error
