from pydantic import BaseModel
from typing import Optional


class Incident(BaseModel):
    incident_id: str
    exception_type: str
    description: str
    location: Optional[str] = None
    priority: str = "Medium"
    status: str = "Open"
    resolution: Optional[str] = None


class ResolveIncident(BaseModel):
    incident_id: str
    exception_type: str
    resolution: str
    outcome: str


class AgentResponse(BaseModel):
    incident_id: str
    analysis: str
    recommended_action: str
    similar_incidents: list[str]


class ResolveResponse(BaseModel):
    incident_id: str
    status: str
    resolution: str
    outcome: str
    message: str