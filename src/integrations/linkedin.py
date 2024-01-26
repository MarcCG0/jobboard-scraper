from typing import Literal

from src.integrations.common import BaseIntegrationType, IntegrationType


class LinkedInIntegration(BaseIntegrationType):
    integration_type: Literal[IntegrationType.LINKEDIN] = IntegrationType.LINKEDIN
