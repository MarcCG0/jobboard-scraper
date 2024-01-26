from typing import Annotated, Union

from pydantic import BaseModel, Field

from src.integrations.indeed import IndeedIntegration
from src.integrations.infojobs import InfoJobsIntegration
from src.integrations.linkedin import LinkedInIntegration

IntegrationType = Annotated[
    Union[
        IndeedIntegration,
        LinkedInIntegration,
        InfoJobsIntegration,
    ],
    Field(discriminator="integration_type"),
]


class Integration(BaseModel):
    integration_instance: IntegrationType
