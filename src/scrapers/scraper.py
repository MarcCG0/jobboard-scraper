from abc import ABC, abstractmethod
from typing import Any, List


class BaseScraper(ABC):
    ALLOWED_SUBCLASSES = ["LinkedInScraper", "IndeedScraper", "InfoJobsScraper"]

    def __init__(self, base_url: str):
        self.base_url = base_url

        if self.__class__.__name__ not in self.ALLOWED_SUBCLASSES:
            raise ValueError(
                f"{self.__class__.__name__} is not an allowed subclass of BaseScraper"
            )

    @abstractmethod
    def scrape(self, **kwargs: Any) -> List[Any]:
        pass
