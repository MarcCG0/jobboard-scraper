from typing import Any, Dict, List

from src.integrations.common import IntegrationType
from src.integrations.gen_common import Integration
from src.models.jobopportunity.models import JobOpportunity
from src.runner.load_runner import PsqlDBLoader
from src.scrapers.indeed import IndeedScraper
from src.scrapers.infojobs import InfoJobsScraper
from src.scrapers.linkedin import LinkedInScraper


class ScraperRunner:
    def __init__(
        self,
        integration_target: List[Integration],
        **kwargs: Dict[str, Any],
    ):
        self.integration_target = integration_target
        if "keywords" not in kwargs:
            raise ValueError("Missing keywords in ScraperRunner initialization")
        elif "location" not in kwargs:
            raise ValueError("Missing location in ScraperRunner initialization")

        self.keywords = kwargs.get("keywords")
        self.location = kwargs.get("location")
        self.loader = PsqlDBLoader(
            database_host="localhost",  # FIXME: this works when running it with docker-compose otherwise use localhost, db
            database_name="jobopportunities",
            user="marc",
            password="password",
            table_name="job_opportunities",
        )

    def load(self, scraped_positions: List[JobOpportunity]):
        """Load the job opportunities to db"""
        self.loader.load_jobs(scraped_positions)

    def run(self):
        """Given a desired list of integration targets,
        return a list of jobs from those targets
        """

        for integration in self.integration_target:
            scraped_positions: List[JobOpportunity]
            if (
                integration.integration_instance.integration_type
                == IntegrationType.LINKEDIN
            ):
                scraped_positions = LinkedInScraper().scrape(
                    keywords=self.keywords, location=self.location
                )
            elif (
                integration.integration_instance.integration_type
                == IntegrationType.INDEED
            ):
                scraped_positions = IndeedScraper().scrape(
                    keywords=self.keywords, location=self.location
                )
            elif (
                integration.integration_instance.integration_type
                == IntegrationType.INFOJOBS
            ):
                scraped_positions = InfoJobsScraper().scrape(
                    keywords=self.keywords, location=self.location
                )
            else:
                raise ValueError(f"Integration: {integration} does not exist")

            self.load(scraped_positions=scraped_positions)
