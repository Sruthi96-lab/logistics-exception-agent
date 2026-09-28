from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from app.agent import LogisticsExceptionAgent
from app.models import (
    Incident,
    AgentResponse,
    ResolveIncident,
    ResolveResponse,
)


app = FastAPI(
    title="Logistics Exception Agent",
    description=(
        "AI agent that learns from previous logistics "
        "incidents using Hindsight."
    ),
    version="1.0.0",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


agent = LogisticsExceptionAgent()


@app.get("/")
def root():
    return FileResponse("static/index.html")


# -----------------------------------------
# Process a new logistics incident
# -----------------------------------------

@app.post(
    "/api/incident",
    response_model=AgentResponse
)
def process_incident(
    incident: Incident
):
    return agent.process_incident(incident)


# -----------------------------------------
# Resolve an existing incident
# -----------------------------------------

@app.post(
    "/api/incident/resolve",
    response_model=ResolveResponse
)
def resolve_incident(
    incident: ResolveIncident
):

    memory_text = (
        f"Incident {incident.incident_id} "
        f"Exception Type: {incident.exception_type} | "
        f"was resolved by: {incident.resolution}. "
        f"Outcome: {incident.outcome}."
    )

    # Save the actual resolution and outcome
    # into Hindsight for future learning.
    agent.memory.save_incident(memory_text)

    return ResolveResponse(
        incident_id=incident.incident_id,
        status="Resolved",
        resolution=incident.resolution,
        outcome=incident.outcome,
        message=(
            "Resolution and actual outcome were saved "
            "to Hindsight memory for future learning."
        ),
    )


# -----------------------------------------
# Serve frontend files
# -----------------------------------------

app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static"
)