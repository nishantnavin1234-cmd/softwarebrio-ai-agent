from pydantic import BaseModel, Field


class TeamMember(BaseModel):
    name: str
    role: str
    linkedin_url: str | None


class CompanyIntelligence(BaseModel):
    company_overview: str
    target_audience: str
    contact_emails: list[str]
    team_members: list[TeamMember]
    confidence_score: float = Field(ge=0.0, le=1.0)