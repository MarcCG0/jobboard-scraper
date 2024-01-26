from typing import Literal

from src.integrations.common import BaseIntegrationType, IntegrationType


class InfoJobsIntegration(BaseIntegrationType):
    integration_type: Literal[IntegrationType.INFOJOBS] = IntegrationType.INFOJOBS
