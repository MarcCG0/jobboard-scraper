import argparse
from typing import List

from src.integrations.gen_common import Integration
from src.integrations.indeed import IndeedIntegration
from src.integrations.linkedin import LinkedInIntegration
from src.integrations.infojobs import InfoJobsIntegration
from src.runner.scraper_runner import ScraperRunner

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Run the scraper with location and keywords."
    )
    parser.add_argument(
        "--location", required=True, help="Specify the location for the scraper."
    )
    parser.add_argument(
        "--keywords", required=True, help="Specify the keywords for the scraper."
    )
    args = parser.parse_args()
    location = args.location
    keywords = args.keywords
    integrations: List[Integration] = [
        Integration(integration_instance=IndeedIntegration()),
        Integration(integration_instance=LinkedInIntegration()),
        Integration(integration_instance=InfoJobsIntegration()),
    ]
    ScraperRunner(
        integration_target=integrations, location=location, keywords=keywords
    ).run()
