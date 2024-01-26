from pydantic import BaseModel, Field


class JobOpportunity(BaseModel):
    """Job Opportunity class defines the Base Class for all job opportunities"""

    job_title: str = Field(default="Couldn't find the job title")
    company: str = Field(default="Couldn't find the company")
    location: str = Field(default="Couldn't find the job location")
    age: str = Field(
        default="Couldn't find the time has passed since the job was posted"
    )
    url_employer: str = Field(default="Couldn't find the site of the employer")
    url_offer: str = Field(default="Couldn't find the site of the offer")
