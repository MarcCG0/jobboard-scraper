from typing import Literal

from src.integrations.common import BaseIntegrationType, IntegrationType


class IndeedIntegration(BaseIntegrationType):
    integration_type: Literal[IntegrationType.INDEED] = IntegrationType.INDEED
