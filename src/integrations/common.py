from abc import ABC
from enum import Enum

from pydantic import BaseModel


class IntegrationType(str, Enum):
    LINKEDIN = "LINKEDIN"
    INDEED = "INDEED"
    INFOJOBS = "INFOJOBS"


class BaseIntegrationType(BaseModel, ABC):
    integration_type: IntegrationType
