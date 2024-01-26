import time
from typing import Any, List

from bs4 import BeautifulSoup
from cloudscraper import CloudScraper, create_scraper
from requests import Response

from src.logs import LOGGER
from src.models.jobopportunity.models import JobOpportunity
from src.scrapers.scraper import BaseScraper


class IndeedScraper(BaseScraper):
    def __init__(self):
        super().__init__(
            "https://es.indeed.com/jobs?q={}&l={}&from=searchOnHP&start={}&vjk=6c06afa18c62bdbd"
        )

    def scrape(self, **kwargs: Any) -> List[JobOpportunity]:
        """Given the desired settings for a job offer,
        scrapes indeed for the specified jobs
        """
        if "keywords" not in kwargs:
            raise ValueError(
                "Missing required argument: 'keywords' that stands for the information you want to scrape."
            )
        if "location" not in kwargs:
            raise ValueError(
                "Missing required argument: 'location' that stands for place you want to scrape the positions from."
            )

        keywords = kwargs.get("keywords")
        location = kwargs.get("location")
        scraper: CloudScraper = create_scraper()
        jobs: List[JobOpportunity] = []
        number = 0
        while True and number < 50:
            time.sleep(1)
            url: str = self.base_url.format(keywords, location, number)
            response: Response = scraper.get(url)
            soup: BeautifulSoup = BeautifulSoup(response.text, "html.parser")

            job_listings = soup.find_all("div", class_="job_seen_beacon")

            if not job_listings:  # Whenever we cannot find more jobs stop scraping.
                break
            LOGGER.info(f"Scraping page {number//10} from indeed")
            for job in job_listings:
                title_element = job.find(
                    "span", id=lambda x: x and x.startswith("jobTitle")
                )
                title = (
                    title_element.get_text(strip=True)
                    if title_element
                    else "No Title Found"
                )
                company_element = job.find("span", {"data-testid": "company-name"})
                company = (
                    company_element.get_text()
                    if company_element
                    else "No Company Found"
                )
                location_element = job.find("div", {"data-testid": "text-location"})
                location_found = (
                    location_element.get_text()
                    if location_element
                    else "No Location Found"
                )
                a_tag = job.find("a", {"id": lambda x: x and x.startswith("job_")})
                url_offer = (
                    "https://es.indeed.com" + a_tag.get("href")
                    if a_tag
                    else "Not found URL offer"
                )
                inner_span = job.find("span", class_="visually-hidden")
                age = (
                    inner_span.find_next_sibling(text=True)
                    if inner_span.find_next_sibling(text=True)
                    else 'Couldn"t find age of the add'
                )
                jobs.append(
                    JobOpportunity(
                        job_title=title,
                        company=company,
                        location=location_found,
                        url_offer=url_offer,
                        age=age,
                    )
                )

            # Repeat the process while we still have more pages to check
            number += 10
        return jobs


# TESTING
# scraper = IndeedScraper().scrape(keywords = "Software Engineer", location = "Barcelona")

# print(scraper)
